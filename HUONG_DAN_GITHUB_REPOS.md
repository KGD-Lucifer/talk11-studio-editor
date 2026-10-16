# TỔNG HỢP CÁC REPOSITORIES VÀ THƯ VIỆN GITHUB CHO TOOL TALK11 STUDIO & REMOTION

Tất cả các repository mã nguồn mở và thư viện quan trọng nhất từ GitHub liên quan đến **AI Tách Nền (Video Matting)**, **Phụ đề tự động (Dynamic Captions)**, **Hiệu ứng âm thanh & Sóng nhạc (Audiogram)** và **Remotion Engine** đã được tải về và tích hợp trực tiếp vào hệ thống:

---

## 1. Danh sách các Repository GitHub đã clone về thư mục `github_repositories/`

Thư mục: `TALK11_Community_Antigravity/github_repositories/`

| Tên Repository | Nguồn GitHub | Tính năng & Công dụng hỗ trợ Tool |
| :--- | :--- | :--- |
| **`RobustVideoMatting`** | [PeterL1n/RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting) | **AI tách nền video người không cần phông xanh số 1 thế giới (CVPR)**. Tách sợi tóc, mép áo, da mượt mà 100%, khử triệt để viền trắng và vật thể nền với ONNX/PyTorch. |
| **`MODNet`** | [ZHKKKe/MODNet](https://github.com/ZHKKKe/MODNet) | Mô hình Trimap-Free Portrait Matting thời gian thực. Tách chủ thể con người siêu nhẹ, tối ưu hóa cho video chân dung. |
| **`template-tiktok`** | [remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok) | Template Remotion chuyên nghiệp cho video ngắn TikTok/Reels: hiệu ứng phụ đề nảy chữ từng từ kiểu CapCut (word-by-word bouncing), emoji động, tích hợp Whisper AI. |
| **`template-audiogram`** | [remotion-dev/template-audiogram](https://github.com/remotion-dev/template-audiogram) | Hiển thị sóng âm thanh trực quan (Audio Waveform/Visualizer), tự động phân tích nhịp giọng nói người nói và tạo phụ đề đồng bộ. |
| **`mediapipe-samples`** | [google-ai-edge/mediapipe-samples](https://github.com/google-ai-edge/mediapipe-samples) | Kho mã nguồn mẫu và thư viện Vision Tasks chính thức của Google MediaPipe phục vụ Image/Video Selfie Segmentation trực tiếp trên trình duyệt. |

---

## 2. Thư viện Remotion chính thức đã cài đặt vào `remotion-prompt-to-video`

Đã tích hợp các package mới nhất từ hệ sinh thái GitHub của Remotion:

1. **`@remotion/video-matting`**: Tách nền video người tự động bằng AI (MODNet & BEN2-base) xuất ra video WebM trong suốt có kênh Alpha.
2. **`@remotion/captions`**: Xử lý phụ đề chữ chạy tự động, highlight từng từ chính xác theo timeline.
3. **`@remotion/media-utils`**: Đo biên độ âm thanh, phân tích tần số giọng nói, tự động lấy thông số video/audio.
4. **`@remotion/motion-blur`**: Hiệu ứng làm mờ chuyển động điện ảnh cho thanh chạy chữ thời sự và banner chuyển cảnh.
5. **`@remotion/transitions`**: Bộ hiệu ứng chuyển cảnh cao cấp (crossZoom, blurSlide, pushCut, dreamyZoom, filmBurn).
6. **`@remotion/noise`**: Tạo hiệu ứng hạt nhiễu nền và ánh sáng động tự nhiên.
7. **`@remotion/shapes` & `@remotion/paths`**: Dựng các hình khối vector và đường viền bảo vệ chủ thể.
8. **`@remotion/player`**: Bộ phát video tương tác trên nền web.

---

## 3. Lệnh CLI Tách Nền Video Bằng AI MODNet / BEN2 (Mới bổ sung)

Bạn có thể chạy lệnh tách nền cho bất kỳ file video nào trong terminal:

```bash
cd remotion-prompt-to-video
npm run matte -- --input <đường_dẫn_video.mp4> --output <video_trong_suot.webm> --model modnet
```

* Mô hình hỗ trợ:
  - `modnet`: Tối ưu hóa chuyên biệt cho con người (chủ thể MC/học sinh, giữ tóc và chi tiết da mượt như CapCut).
  - `ben2-base`: Tách nền đa năng cho cả người và đồ vật liên quan.

---

## 4. Cải tiến thuật toán AI Tách Nền Trong Trình Duyệt (`Tao_Khung_Thoi_Su_Talk11.html`)

Đã nâng cấp thuật toán tách nền theo phong cách CapCut:
1. **MediaPipe độ phân giải cao 256p** (thay vì 144p làm răng cưa bậc thang).
2. **Dynamic Room-Wall Sampling & Guided Matting**: Tự động đo màu tường phòng thực tế ở góc camera và triệt tiêu toàn bộ quầng trắng (white halo) quanh tóc và vai.
3. **Universal Foliage Eradication**: Quét toàn bộ khung hình để loại bỏ triệt để cành lá cây, hoa xanh bên cạnh mà không bị giới hạn vùng biên.
4. **Hermite S-Curve Smoothstep Feathering (`feather = 18`)**: Đường viền vô hình bảo vệ chủ thể, chuyển tiếp mềm mịn dưới cấp độ sub-pixel, loại bỏ hoàn toàn hiện tượng lem nhem.
5. **MediaPipe Offline**: Đã lưu toàn bộ file WASM và Binarypb vào thư mục nội bộ `03_ASSETS/mediapipe/`, chạy mượt mà ngay cả khi mất mạng.
