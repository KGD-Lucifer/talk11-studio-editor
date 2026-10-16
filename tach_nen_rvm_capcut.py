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

def decontaminate_neck_nook(fgr_3d, pha_clean, h, w):
    """
    Step 5B: Triệt tiêu 100% quầng tường trắng dính tóc tơ/tóc con ở cổ, tai và quai hàm.
    Phát hiện các điểm ảnh tường trắng trung tính không phải da người và không phải tóc,
    loại bỏ khỏi mặt nạ alpha.
    """
    neck_limit_y = int(h * 0.72)
    upper_fgr = fgr_3d[:neck_limit_y] * 255.0
    ur = upper_fgr[:, :, 0]
    ug = upper_fgr[:, :, 1]
    ub = upper_fgr[:, :, 2]

    # Nhận diện da người (luôn có sắc tố đỏ r - b > 15 và r > g)
    is_skin = (ur > 80) & (ug > 40) & (ub > 25) & (ur > ug) & ((ur - ub) > 15)
    # Nhận diện tóc sẫm màu
    is_hair = (ur < 80) & (ug < 80) & (ub < 80)
    # Nhận diện tường trắng / xám sáng phòng thực tế
    is_bright_wall = (ur > 188) & (ug > 180) & (ub > 175) & (np.abs(ur - ug) < 28) & (np.abs(ur - ub) < 28)

    wall_mask = is_bright_wall & (~is_skin) & (~is_hair)
    pha_clean[:neck_limit_y][wall_mask] = 0.0
    return pha_clean

def process_image_or_video(input_path, output_path, model_path='03_ASSETS/models/rvm/rvm_mobilenetv3_fp32.onnx', downsample_ratio=None, output_format='auto'):
    print(f"Loading RVM ONNX Model from: {model_path}...")
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

    print(f"Executing Mode: {output_format}")
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
        
        # Inward Choke + Hermite
        pha_clean = np.clip((pha_2d - 0.05) / 0.93, 0.0, 1.0)
        pha_clean = pha_clean * pha_clean * (3.0 - 2.0 * pha_clean)
        pha_clean = decontaminate_neck_nook(fgr_3d, pha_clean, h, w)

        fgr_bgr = cv2.cvtColor((fgr_3d * 255.0).clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
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

        print(f"Saved cutout image to: {output_path}")
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
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

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
            
            # Gọt sát mép người & Hermite curve
            pha_clean = np.clip((pha_2d - 0.05) / 0.93, 0.0, 1.0)
            pha_clean = pha_clean * pha_clean * (3.0 - 2.0 * pha_clean)
            
            # Morphological erosion (1px) loại bỏ hoàn toàn viền lem
            pha_u8 = (pha_clean * 255.0).astype(np.uint8)
            pha_eroded = cv2.erode(pha_u8, kernel, iterations=1)
            pha_clean = pha_eroded.astype(np.float32) / 255.0

            # Step 5B Neck Nook Decontamination
            pha_clean = decontaminate_neck_nook(fgr_3d, pha_clean, h, w)
            pha_3d = pha_clean[..., None]

            fgr_bgr = cv2.cvtColor((fgr_3d * 255.0).clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
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
                green_bg = np.array([0.0, 1.0, 0.0], dtype=np.float32)
                comp_rgb = (fgr_3d * pha_3d + green_bg * (1.0 - pha_3d)) * 255.0
                comp_bgr = cv2.cvtColor(comp_rgb.clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
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
    args = parser.parse_args()
    
    process_image_or_video(args.input, args.output, args.model, args.downsample, args.format)
