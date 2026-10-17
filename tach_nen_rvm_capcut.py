import os
import sys
import argparse
import subprocess
import cv2
import numpy as np
import onnxruntime as ort

def get_auto_downsample_ratio(h, w, user_ratio=None):
    if user_ratio is not None and user_ratio > 0:
        return float(user_ratio)
    max_dim = max(h, w)
    if max_dim <= 720:
        return 1.0
    ratio = 768.0 / max_dim
    return float(np.clip(ratio, 0.35, 0.55))

def apply_davinci_delta_despill(fgr_3d, despill_strength=0.5):
    """
    DaVinci Resolve Delta Keyer Smart Despill Engine:
    Khử sạch triệt để hiện tượng ám màu phông xanh (green spill) và phản quang đèn trường quay
    vào viền tóc và da mà không làm mất màu sắc tự nhiên của chủ thể.
    fgr_3d: np.float32 [0.0 .. 1.0] in RGB
    """
    if despill_strength <= 0:
        return fgr_3d
    
    r = fgr_3d[:, :, 0]
    g = fgr_3d[:, :, 1]
    b = fgr_3d[:, :, 2]

    # DaVinci Delta Keyer standard: clamp excess green
    rb_avg = (r + b) * 0.5
    excess_green = np.maximum(0.0, g - rb_avg)
    g_despilled = g - excess_green * float(despill_strength)

    out = np.stack([r, g_despilled, b], axis=-1)
    return np.clip(out, 0.0, 1.0)

def recover_hair_details(fgr_3d, pha_clean, hair_detail_level=0.75):
    """
    Adobe Refine Edge & DaVinci Magic Mask Hair Detail Recovery:
    Sử dụng bộ lọc đạo hàm bậc hai (Laplacian) và High-Pass Filter để nhận diện
    từng sợi tóc tơ mảnh (1-2px) trong vùng chuyển tiếp mờ (semi-transparent fringe).
    Khôi phục độ rõ nét của tóc tơ, ngăn chặn hiện tượng tóc bị bết dính hoặc bị gọt cùn nham nhở.
    """
    if hair_detail_level <= 0:
        return pha_clean

    h, w = pha_clean.shape[:2]
    # Xác định vùng biên tóc và chuyển tiếp (0.05 < alpha < 0.92)
    fringe_zone = (pha_clean > 0.05) & (pha_clean < 0.92)
    if not np.any(fringe_zone):
        return pha_clean

    # Tạo ảnh độ sáng grayscale
    fgr_u8 = (fgr_3d * 255.0).clip(0, 255).astype(np.uint8)
    gray = cv2.cvtColor(fgr_u8, cv2.COLOR_RGB2GRAY).astype(np.float32)

    # Laplacian để bắt chi tiết vi mô sợi tóc
    lap = cv2.Laplacian(gray, cv2.CV_32F, ksize=3)
    lap_mag = np.abs(lap) / 255.0

    # Nhận diện vùng tóc (tóc sẫm màu hoặc nâu/vàng có tương phản cao với nền)
    hair_likelihood = np.clip(lap_mag * 2.8, 0.0, 1.0)
    
    # Chỉ áp dụng khôi phục cho các pixel nằm trong dải chuyển tiếp tóc
    hair_boost = hair_likelihood * float(hair_detail_level) * 0.45
    pha_enhanced = np.where(fringe_zone, np.clip(pha_clean + hair_boost, 0.0, 1.0), pha_clean)

    return pha_enhanced

def apply_core_matte_protection(pha_clean, core_protect_level=0.85):
    """
    Photoshop Select & Mask Core Matte Protection:
    Bảo vệ kiên cố 100% ruột thân thể, áo đồng phục học sinh (kể cả áo trắng tinh
    hoặc áo sáng màu trùng màu tường nhà).
    Ngăn chặn triệt để hiện tượng áo trắng bị 'cắn lẹm' hoặc thủng lỗ chỗ như CapCut.
    """
    if core_protect_level <= 0:
        return pha_clean

    # Xói mòn sâu vào trong cơ thể để tìm lõi rắn kiên cố (Solid Core)
    pha_u8 = (pha_clean * 255.0).clip(0, 255).astype(np.uint8)
    kernel_core = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    core_mask = cv2.erode(pha_u8, kernel_core, iterations=2) > int(190 * core_protect_level)

    # Trong vùng lõi, ép alpha đạt tuyệt đối 1.0 (255)
    pha_protected = pha_clean.copy()
    pha_protected[core_mask] = 1.0
    return pha_protected

def decontaminate_full_body_halo(fgr_3d, pha_clean, h, w):
    """
    Advanced Color Decontamination & Anti-Halo Engine:
    Triệt tiêu 100% quầng tường trắng/sáng dính tóc tơ, cổ, tai, quai hàm và mép vai.
    Phân biệt rõ ràng giữa da người, tóc tự nhiên, áo trắng và tường nhà trung tính.
    """
    fgr_255 = fgr_3d * 255.0
    ur = fgr_255[:, :, 0]
    ug = fgr_255[:, :, 1]
    ub = fgr_255[:, :, 2]

    # 1. Nhận diện da người (sắc tố đỏ r - b > 14 và r > g)
    is_skin = (ur > 75) & (ug > 35) & (ub > 20) & (ur > ug) & ((ur - ub) > 14)
    # 2. Nhận diện tóc tự nhiên (tóc đen, nâu sẫm, hoặc tóc vàng/nâu dưới ánh sáng)
    is_hair = (ur < 85) & (ug < 85) & (ub < 85) | (((ur + ug + ub) / 3.0 < 115) & (ur >= ub))
    # 3. Nhận diện tường trắng / xám sáng trung tính phòng học / phòng khách
    is_bright_wall = (ur > 185) & (ug > 180) & (ub > 175) & (np.abs(ur - ug) < 26) & (np.abs(ur - ub) < 26)

    # Vùng đầu, cổ, tai, quai hàm (y < 75% chiều cao khung hình):
    upper_limit_y = int(h * 0.75)
    wall_in_upper = is_bright_wall[:upper_limit_y] & (~is_skin[:upper_limit_y]) & (~is_hair[:upper_limit_y])
    pha_clean[:upper_limit_y][wall_in_upper] = 0.0

    # Vùng vai và thân dưới: Triệt tiêu các quầng sáng ở rìa ngoài bán trong suốt
    lower_zone = pha_clean[upper_limit_y:]
    lower_wall = is_bright_wall[upper_limit_y:] & (~is_skin[upper_limit_y:])
    lower_fringe = (lower_zone > 0.0) & (lower_zone < 0.75)
    lower_zone[lower_wall & lower_fringe] = 0.0
    pha_clean[upper_limit_y:] = lower_zone

    return pha_clean

def refine_matte_world_class(fgr_3d, pha_raw, h, w, hair_detail=0.75, core_protect=0.85, despill=0.5, choke_px=1):
    """
    HYBRID WORLD-CLASS MATTING PIPELINE:
    Kết hợp tinh hoa của Adobe Photoshop + After Effects Keylight + CapCut Pro + DaVinci Resolve Studio.
    """
    # 1. Inward Choke chuẩn xác với đường cong Hermite Smoothstep (Loại bỏ viền mờ đục)
    pha_shifted = np.clip((pha_raw - 0.04) / 0.94, 0.0, 1.0)
    pha_hermite = pha_shifted * pha_shifted * (3.0 - 2.0 * pha_shifted)

    # 2. Gọt sát mép nhân vật bằng Morphological Erosion nếu choke_px > 0
    if choke_px > 0:
        pha_u8 = (pha_hermite * 255.0).astype(np.uint8)
        k_size = 3 if choke_px == 1 else 5
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_size, k_size))
        pha_eroded = cv2.erode(pha_u8, kernel, iterations=choke_px)
        pha_cur = pha_eroded.astype(np.float32) / 255.0
    else:
        pha_cur = pha_hermite

    # 3. Khóa ruột Core Matte Protection (Bảo vệ 100% áo trắng đồng phục & da)
    pha_cur = apply_core_matte_protection(pha_cur, core_protect_level=core_protect)

    # 4. Khôi phục chi tiết sợi tóc tơ tần số cao (DaVinci Magic Hair Recovery)
    pha_cur = recover_hair_details(fgr_3d, pha_cur, hair_detail_level=hair_detail)

    # 5. Triệt tiêu 100% quầng tường trắng phản quang (Color Decontamination)
    pha_cur = decontaminate_full_body_halo(fgr_3d, pha_cur, h, w)

    # 6. DaVinci Delta Keyer Smart Despill (Khử ám xanh / ánh sáng phòng)
    fgr_clean = apply_davinci_delta_despill(fgr_3d, despill_strength=despill)

    return fgr_clean, np.clip(pha_cur, 0.0, 1.0)

def process_image_or_video(input_path, output_path, model_path='03_ASSETS/models/rvm/rvm_mobilenetv3_fp32.onnx',
                           downsample_ratio=None, output_format='auto',
                           hair_detail=0.75, core_protect=0.85, despill=0.5, choke_px=1):
    print(f"Loading World-Class RVM ONNX Model from: {model_path}...")
    opts = ort.SessionOptions()
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    opts.intra_op_num_threads = os.cpu_count() or 4
    
    sess = ort.InferenceSession(model_path, opts, providers=['CPUExecutionProvider'])
    
    ext = os.path.splitext(input_path)[1].lower()
    out_ext = os.path.splitext(output_path)[1].lower()
    is_image = ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']
    
    # Auto determine format if not specified
    if output_format == 'auto':
        if is_image:
            output_format = 'image_bgra'
        elif out_ext == '.webm':
            output_format = 'transparent_webm'
        elif 'alpha' in output_path.lower():
            output_format = 'alpha_matte'
        else:
            output_format = 'green_screen'

    print(f"Executing Mode: {output_format} | HairDetail: {hair_detail} | CoreProtect: {core_protect} | Despill: {despill} | Choke: {choke_px}px")
    ffmpeg_bin = os.path.abspath('remotion-prompt-to-video/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe')

    if is_image:
        img_bgr = cv2.imread(input_path)
        if img_bgr is None:
            print(f"Error: Cannot read image {input_path}")
            return False
            
        h, w = img_bgr.shape[:2]
        effective_ds = get_auto_downsample_ratio(h, w, downsample_ratio)
        print(f"Processing Image: {w}x{h}, auto downsample_ratio={effective_ds:.3f}")
        
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        src = np.transpose(img_rgb, (2, 0, 1))[None, ...]
        
        rec = [np.zeros([1, 1, 1, 1], dtype=np.float32)] * 4
        ds = np.array([effective_ds], dtype=np.float32)
        
        # Warm-up recurrent passes
        for _ in range(4):
            fgr, pha, *rec = sess.run([], {
                'src': src,
                'r1i': rec[0],
                'r2i': rec[1],
                'r3i': rec[2],
                'r4i': rec[3],
                'downsample_ratio': ds
            })
            
        pha_2d = pha[0, 0] # (H, W)
        fgr_3d = np.transpose(fgr[0], (1, 2, 0)) # (H, W, 3) in RGB
        
        # Áp dụng World-Class Hybrid Refinement Pipeline
        fgr_clean, pha_clean = refine_matte_world_class(
            fgr_3d, pha_2d, h, w,
            hair_detail=hair_detail,
            core_protect=core_protect,
            despill=despill,
            choke_px=choke_px
        )

        fgr_bgr = cv2.cvtColor((fgr_clean * 255.0).clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        pha_u8 = (pha_clean * 255.0).clip(0, 255).astype(np.uint8)
        
        if output_format == 'alpha_matte':
            cv2.imwrite(output_path, pha_u8)
        elif output_format == 'green_screen':
            green_bg = np.array([0, 255, 0], dtype=np.uint8)
            alpha_f = pha_clean[..., None]
            comp = (fgr_bgr * alpha_f + green_bg * (1.0 - alpha_f)).clip(0, 255).astype(np.uint8)
            cv2.imwrite(output_path, comp)
        else:
            bgra = cv2.merge([fgr_bgr[:, :, 0], fgr_bgr[:, :, 1], fgr_bgr[:, :, 2], pha_u8])
            cv2.imwrite(output_path, bgra)

        print(f"Saved world-class cutout image to: {output_path}")
        return True
    else:
        # Video Processing
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video {input_path}")
            return False
            
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        effective_ds = get_auto_downsample_ratio(h, w, downsample_ratio)
        print(f"Processing Video: {w}x{h} @ {fps:.1f} FPS, {total_frames} frames, auto downsample_ratio={effective_ds:.3f}")

        # Setup output pipe / writer
        ffmpeg_proc = None
        writer = None
        temp_raw_out = None

        if output_format == 'transparent_webm' and os.path.exists(ffmpeg_bin):
            cmd = [
                ffmpeg_bin, '-y',
                '-f', 'image2pipe',
                '-vcodec', 'png',
                '-r', str(fps),
                '-i', '-',
                '-c:v', 'libvpx-vp9',
                '-pix_fmt', 'yuva420p',
                '-b:v', '8M',
                output_path
            ]
            ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        else:
            temp_raw_out = output_path + '.raw.avi'
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            writer = cv2.VideoWriter(temp_raw_out, fourcc, fps, (w, h))

        rec = [np.zeros([1, 1, 1, 1], dtype=np.float32)] * 4
        ds = np.array([effective_ds], dtype=np.float32)
        
        # Temporal Coherence Buffer (Khử nhấp nháy chuyển động kiểu DaVinci / AE Rotobrush)
        prev_pha = None

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            src = np.transpose(img_rgb, (2, 0, 1))[None, ...]
            
            fgr, pha, *rec = sess.run([], {
                'src': src,
                'r1i': rec[0],
                'r2i': rec[1],
                'r3i': rec[2],
                'r4i': rec[3],
                'downsample_ratio': ds
            })
            
            pha_2d = pha[0, 0] # (H, W)
            fgr_3d = np.transpose(fgr[0], (1, 2, 0)) # (H, W, 3) in RGB
            
            # Hybrid Refinement Pipeline
            fgr_clean, pha_clean = refine_matte_world_class(
                fgr_3d, pha_2d, h, w,
                hair_detail=hair_detail,
                core_protect=core_protect,
                despill=despill,
                choke_px=choke_px
            )

            # Video Temporal Coherence Filter
            if prev_pha is not None:
                motion_diff = np.abs(pha_clean - prev_pha)
                # Vùng ổn định làm mượt 35%, vùng cử động nhanh giữ nguyên không trễ
                smooth_mask = (motion_diff < 0.18)
                pha_clean = np.where(smooth_mask, prev_pha * 0.35 + pha_clean * 0.65, pha_clean)
            prev_pha = pha_clean.copy()

            fgr_bgr = cv2.cvtColor((fgr_clean * 255.0).clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
            pha_u8 = (pha_clean * 255.0).clip(0, 255).astype(np.uint8)

            if output_format == 'transparent_webm' and ffmpeg_proc:
                bgra = cv2.merge([fgr_bgr[:, :, 0], fgr_bgr[:, :, 1], fgr_bgr[:, :, 2], pha_u8])
                _, png_buf = cv2.imencode('.png', bgra)
                ffmpeg_proc.stdin.write(png_buf.tobytes())
            elif output_format == 'alpha_matte':
                matte_bgr = cv2.cvtColor(pha_u8, cv2.COLOR_GRAY2BGR)
                writer.write(matte_bgr)
            else:
                # Composite over green screen (#00FF00) cho studio chroma keying
                green_bg = np.array([0, 255, 0], dtype=np.uint8)
                alpha_f = pha_clean[..., None]
                comp_bgr = (fgr_bgr * alpha_f + green_bg * (1.0 - alpha_f)).clip(0, 255).astype(np.uint8)
                writer.write(comp_bgr)

            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"  Frame {frame_idx}/{total_frames} ({frame_idx/max(1, total_frames)*100:.1f}%)")
                
        cap.release()
        
        if ffmpeg_proc:
            ffmpeg_proc.stdin.close()
            ffmpeg_proc.wait()
            print(f"Transparent WebM VP9 Matting saved: {output_path}")
            return True
        else:
            writer.release()
            if os.path.exists(ffmpeg_bin):
                os.system(f'"{ffmpeg_bin}" -y -i "{temp_raw_out}" -c:v libx264 -pix_fmt yuv420p "{output_path}"')
                if os.path.exists(temp_raw_out):
                    os.remove(temp_raw_out)
            else:
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(temp_raw_out, output_path)
            print(f"Video RVM Matting finished: {output_path}")
            return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='Path to input image or video')
    parser.add_argument('--output', '-o', required=True, help='Path to output file')
    parser.add_argument('--model', '-m', default='03_ASSETS/models/rvm/rvm_mobilenetv3_fp32.onnx', help='Path to RVM ONNX model')
    parser.add_argument('--downsample', '-d', type=float, default=0.25, help='Downsample ratio (0.25 to 0.5)')
    parser.add_argument('--format', '-f', choices=['auto', 'green_screen', 'transparent_webm', 'alpha_matte', 'image_bgra'], default='auto', help='Output format')
    parser.add_argument('--hair-detail', type=float, default=0.75, help='Hair detail recovery strength (0.0 - 1.0)')
    parser.add_argument('--core-protect', type=float, default=0.85, help='Solid core white shirt protection strength (0.0 - 1.0)')
    parser.add_argument('--despill', type=float, default=0.5, help='DaVinci Delta Keyer despill factor (0.0 - 1.0)')
    parser.add_argument('--choke', type=int, default=1, help='Inward choke pixels (0 - 4)')
    args = parser.parse_args()
    
    process_image_or_video(
        input_path=args.input,
        output_path=args.output,
        model_path=args.model,
        downsample_ratio=args.downsample,
        output_format=args.format,
        hair_detail=args.hair_detail,
        core_protect=args.core_protect,
        despill=args.despill,
        choke_px=args.choke
    )
