---
description: "Quy tắc phối hợp đồng hành và kiểm tra chéo giữa Antigravity và ChatGPT (Dual-AI Consensus Protocol)"
globs: ["*"]
---

# QUY TẮC ĐỒNG HÀNH & KIỂM TRA CHÉO (ANTIGRAVITY ⟷ CHATGPT)

> **Mục tiêu tối thượng:** Đảm bảo mọi tính năng, nâng cấp và sửa lỗi trong dự án TALK11 Broadcast Studio đều phải được kiểm tra chéo (Cross-check) giữa Antigravity và ChatGPT. Không áp dụng code một chiều; sai cùng sửa, đạt đồng thuận kép (Dual-Approval Pass) thì mới nghiệm thu bản chính thức.

---

## 1. PHÂN VAI & TRÁCH NHIỆM

| Tiêu chí | **Antigravity (Pair Programmer trên máy)** | **ChatGPT (AI Phản biện & Đóng góp ý tưởng)** |
| :--- | :--- | :--- |
| **Vị trí** | Trực tiếp trong IDE, thao tác file, terminal, git, test tự động. | Phân tích logic, đề xuất giải pháp kiến trúc, phản biện thuật toán. |
| **Nguồn dữ liệu** | File local & môi trường runtime thực tế. | Đọc mã nguồn mới nhất trên GitHub (`talk11-studio-editor`). |
| **Trọng trách chính** | Thẩm định thực tế, viết code, chạy test tự động (CDP/Headless), phát hiện bug ngầm, push GitHub. | Review kiến trúc, phát hiện thiếu sót logic, đóng góp ý tưởng sáng tạo. |

---

## 2. QUY TRÌNH KIỂM TRA CHÉO 4 BƯỚC (STANDARD PROTOCOL)

```text
[Ý tưởng / Yêu cầu]
        │
        ▼
1. CHATGPT & BẠN ĐỀ XUẤT ──► Antigravity phân tích khả thi & kiến trúc
        │
        ▼
2. ANTIGRAVITY THỰC THI ──► Viết code + chạy test tự động (CDP Edge, 0 console error)
        │
        ▼
3. ĐỒNG BỘ GITHUB ────────► Push commit lên repo để ChatGPT đọc và phản biện lại
        │
        ▼
4. KIỂM TRA CHÉO & PHÊ DUYỆT:
   ├─ Nếu ChatGPT phát hiện lỗi/góp ý: Antigravity lập tức thẩm định, sửa và test lại
   └─ Nếu cả Antigravity (Test Pass) và ChatGPT (Review Pass): BẢN CHÍNH THỨC HOÀN TẤT
```

---

## 3. NGUYÊN TẮC BẮT BUỘC KHI LÀM VIỆC

1. **Cập nhật GitHub sau mỗi bước hoàn thành:**
   Mỗi khi hoàn tất một tính năng hoặc sửa lỗi, Antigravity phải tự động đồng bộ sang tất cả các file HTML (qua `sync_all_htmls.js`) và `git push` lên GitHub `main` để ChatGPT luôn có dữ liệu mới nhất.
2. **Minh bạch lỗi & Phản biện kỹ thuật:**
   Nếu ChatGPT đưa ra gợi ý chưa tối ưu (ví dụ: gây tràn bộ nhớ, gián đoạn 60fps, hoặc xung đột DOM), Antigravity phải giải thích rõ nguyên nhân kỹ thuật và đưa ra phương án tối ưu thay thế để cùng chốt.
3. **Cung cấp Review Checklist cho người dùng:**
   Sau mỗi lần nâng cấp, Antigravity sẽ chuẩn bị sẵn câu lệnh/checklist súc tích để người dùng copy nhanh sang ChatGPT kiểm tra chéo.
4. **Tiêu chuẩn "DUAL PASS":**
   Một bản nâng cấp chỉ được coi là hoàn tất khi:
   - ✅ **Antigravity Gate:** Mã nguồn chạy thực tế không lỗi, test CDP 100% xanh.
   - ✅ **ChatGPT Gate:** ChatGPT xem xét code trên GitHub và xác nhận đạt yêu cầu logic.
