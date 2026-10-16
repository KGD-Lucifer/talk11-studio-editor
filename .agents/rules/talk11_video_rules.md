---
description: "TALK11 Student News Community — Video Tutorial Ruleset V1.0 (40 Rules Source of Truth)"
globs: ["*"]
---

# TALK11 STUDENT NEWS COMMUNITY
## VIDEO TUTORIAL RULESET — V1.0

> Bộ luật nền cố định dùng cho Antigravity/AI khi tạo video hướng dẫn cho TALK11 Student News Community.
> Mục tiêu: mọi video hướng dẫn phải dễ hiểu, dễ quay bằng điện thoại, phù hợp học sinh tiểu học–THCS và không lệch khỏi định hướng cộng đồng.

---

# RULE 01 — Mục tiêu video
Video hướng dẫn phải giúp học sinh sau khi xem xong biết rõ:
**Làm gì → nói gì → quay cảnh nào → quay như thế nào → video dài bao lâu → nộp thế nào.**
Tiêu chuẩn cuối cùng: Học sinh phải có khả năng tự quay sản phẩm bằng điện thoại sau khi xem hướng dẫn.

# RULE 02 — Video hướng dẫn không phải quảng cáo
Không biến tutorial thành video giới thiệu trung tâm. Brand TALK11 chỉ đóng vai trò nhận diện nhẹ.
- Không: giới thiệu dài, bán hàng, CTA đăng ký học, logo xuất hiện quá nhiều.
- Được: logo ngắn ở đầu/cuối (1-2s), watermark nhỏ nếu cần, CTA cuối: “Gửi sản phẩm của bạn tới TALK11 Student News.”

# RULE 03 — Một video chỉ giải quyết một nhiệm vụ
Mỗi tutorial chỉ được hướng dẫn: **1 format + 1 chủ đề chính.**
Ví dụ đúng: Phóng viên nhí — My School.

# RULE 04 — Luôn cho xem sản phẩm mẫu trước khi dạy
Trong 5–10 giây đầu phải cho học sinh thấy: “Video cuối cùng của em có thể trông như thế này.” Sau đó mới giải thích từng bước.

# RULE 05 — Cấu trúc tutorial mặc định
```text
1. HOOK (0-3s)
2. VIDEO MẪU (3-10s)
3. NHIỆM VỤ HÔM NAY (10-20s)
4. CẢNH 1, CẢNH 2, CẢNH 3... (20-75s)
5. CÂU THOẠI MẪU
6. GOOD vs AVOID (75-95s)
7. CHECKLIST (95-110s)
8. CTA NỘP BÀI (110-120s)
```

# RULE 06 — Hướng dẫn bằng cảnh quay, không bằng lý thuyết
Phải chuyển thành cảnh cụ thể (Góc máy, Bố cục, Lời thoại, B-roll). Mọi storyboard phải đủ cụ thể để người không biết quay video vẫn làm được.

# RULE 07 — Mỗi cảnh phải có đủ thông tin
```yaml
scene_number:
duration:
purpose:
location:
subject:
action:
camera_angle:
framing:
dialogue_or_voiceover:
on_screen_text:
b_roll:
technical_note:
```

# RULE 08 — Điện thoại là thiết bị mặc định
Giả định học sinh chỉ có smartphone. Không yêu cầu máy quay, gimbal, đèn studio, mic chuyên nghiệp.

# RULE 09 — Góc máy phải đơn giản
Mặc định: Camera ngang tầm mắt. Khung hình: medium close-up (ngực lên hoặc eo lên).

# RULE 10 — Không lạm dụng camera movement
Ưu tiên: static → pan nhẹ → walking shot đơn giản → B-roll.

# RULE 11 — Ánh sáng
Mặt hướng về nguồn sáng (cửa sổ, bóng râm ngoài trời). Không quay ngược sáng với cửa sổ sau lưng.

# RULE 12 — Âm thanh quan trọng hơn hình quá đẹp
1. nghe rõ lời; 2. ít tiếng ồn; 3. đứng gần điện thoại; 4. nói chậm và rõ. Nếu ồn: quay trước thu voice-over sau.

# RULE 13 — B-roll phải có lý do
Chỉ chèn cảnh B-roll liên quan trực tiếp đến điều học sinh đang nói.

# RULE 14 — Không biến học sinh thành diễn viên quảng cáo
Tự nhiên, gần đời thật, không đọc thoại cứng, không bắt trẻ tạo biểu cảm thương mại.

# RULE 15 — Không yêu cầu học thuộc script
Script chỉ là Sample Script. Luôn ghi: “Em có thể thay đổi câu nói theo ý của mình.”

# RULE 16 — Tiếng Anh phải theo năng lực trẻ
Beginner (3-5 câu đơn) | A1 (30-60s) | A1-A2 (60-90s) | A2+ (Reporter/Interview/Vlog) | B1+ (Presentation/Debate).

# RULE 17 — Tiếng Việt trong tutorial phải cực kỳ dễ hiểu
Không dùng thuật ngữ hàn lâm. Nếu dùng phải giải thích ngay bằng 1 câu ngắn (VD: B-roll = cảnh minh họa cho điều em nói).

# RULE 18 — Text trên màn hình phải ít
Một cảnh chỉ nên có: 1 headline + 1 dòng phụ nếu cần.

# RULE 19 — Mọi lời quan trọng phải có subtitle
Narrator Việt → sub Việt. Student nói Anh → sub Anh. Có thể kèm nghĩa Việt nhỏ.

# RULE 20 — Luôn có GOOD vs AVOID
Dùng ví dụ cụ thể (Camera ngang mắt vs dưới cằm, Mặt hướng cửa sổ vs ngược sáng). Dùng từ "AVOID / NÊN TRÁNH", không phán xét.

# RULE 21 — Checklist cuối video là bắt buộc
Đúng chủ đề, đúng thời lượng, tiếng nghe rõ, hình đủ sáng, có tiếng Anh, không lộ riêng tư, footage hợp lệ, phụ huynh đồng ý.

# RULE 22 — Chủ đề phải quay được trong đời thật
Trường học, Gia đình, Bản thân, Địa phương, Trải nghiệm, Kiến thức gần gũi.

# RULE 23 — Format chính của TALK11 Community
Phóng viên nhí, Phỏng vấn, Vlog, Hướng dẫn viên nhí, MC/Presenter, Student Talk, Mini Podcast, Storytelling, Photo Story, Debate, Dubbing.

# RULE 24 — Ưu tiên format dễ trước
Photo Story → Vlog ngắn → Reporter ngắn → Interview.

# RULE 25 — Branding TALK11 nhẹ
Màu chính: Orange #FF6B00. Nền: White #FFFFFF hoặc Dark thanh lịch #0F172A. Accent: Yellow/Cyan. Style: clean / modern / friendly / educational / minimal.

# RULE 26 — Tutorial không được quá “trẻ con”
Đối tượng có cả THCS. Không dùng cartoon babyish, sticker quá nhiều, nhấp nháy, font hoạt hình rối rắm. Phải thân thiện nhưng hiện đại.

# RULE 27 — Ưu tiên footage thật
Video thật của học sinh/TALK11 → stock footage phù hợp → graphic/minh họa → AI footage chỉ khi cần.

# RULE 28 — Quyền riêng tư trẻ em
Không quay: địa chỉ nhà, số điện thoại, biển số xe, bảng điểm, vị trí thời gian thực, thông tin nhạy cảm.

# RULE 29 — Người khác xuất hiện trong video
Phải xin phép bạn học, giáo viên, người thân trước khi ghi hình và xuất bản.

# RULE 30 — Bản quyền video
Không dùng workflow tải video YouTube xóa logo. Footage phải có quyền sử dụng hoặc open-license rõ ràng.

# RULE 31 — Video mẫu nước ngoài chỉ dùng REFERENCE ONLY
Chỉ học format, góc máy, cách kể. Không copy nguyên văn/footage/logo.

# RULE 32 — Default aspect ratio
Mặc định: **9:16 vertical** (TikTok/Reels/Shorts). Có thể dùng 16:9 cho presentation/debate nếu ghi rõ.

# RULE 33 — Video mẫu có chất lượng “đủ tốt để bắt chước”
Đẹp hơn video điện thoại thông thường một chút nhưng học sinh vẫn tự làm được.

# RULE 34 — Không lấy viral làm mục tiêu
Không theo trend nguy hiểm, câu view, prank. Ưu tiên giao tiếp, trải nghiệm, sản phẩm thật.

# RULE 35 — CTA cuối video
“Bây giờ đến lượt bạn! Quay video của bạn và gửi cho TALK11 Student News.”

# RULE 36 — Output bắt buộc từ AI
```yaml
VIDEO_TUTORIAL:
  title:
  target_student:
  english_level:
  format:
  objective:
  final_student_output:
  duration:
  aspect_ratio:
  storyboard:
    - scene_number:
      duration:
      location:
      subject:
      action:
      camera_angle:
      framing:
      dialogue_or_voiceover:
      on_screen_text:
      b_roll:
      technical_note:
  full_sample_script:
  good_vs_avoid:
  filming_checklist:
  privacy_copyright_checklist:
  submission_checklist:
```

# RULE 37 — Nếu thiếu thông tin
AI tự dùng default (smartphone, 9:16, 60-120s, clean modern educational minimal, light branding, A1-A2, subtitles: true).

# RULE 38 — Thứ tự ưu tiên khi rules xung đột
1. An toàn trẻ em → 2. Quyền riêng tư → 3. Bản quyền → 4. Học sinh làm được → 5. Đúng nhiệm vụ → 6. Dễ hiểu → 7. Nội dung → 8. Kỹ thuật → 9. Thẩm mỹ → 10. Branding. *(Nếu đẹp vs dễ làm → Dễ làm thắng).*

# RULE 39 — Self-check bắt buộc
Tự kiểm tra 12 tiêu chí trước khi trả kết quả.

# RULE 40 — 5 luật cốt lõi nhất
1. Một tutorial = một nhiệm vụ.
2. Dạy bằng từng cảnh cụ thể.
3. Học sinh quay được bằng điện thoại.
4. Tiếng Anh vừa trình độ, không ép hoàn hảo.
5. Xem xong là tự làm được ngay.
