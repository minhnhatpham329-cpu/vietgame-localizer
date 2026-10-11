---
name: vietgame-localizer
description: Dịch, Việt hóa/localize game sang tiếng Việt, biên tập bản Việt và tạo patch bản dịch; giữ ngữ cảnh, xưng hô và tiến độ qua nhiều lượt chat. Dùng cả khi tiếp tục bản dịch hoặc cải tiến quy trình này; kiến thức từng game lưu riêng. Không dùng cho bản vá mã nguồn không liên quan bản dịch.
---

# VietGame Localizer v9.2

Dùng nguồn + PATCH + STATE để dịch trong chat. Đọc
[quy trình chính](references/chat-workflow.md) khi bắt đầu áp dụng skill;
ở các lượt tiếp, dùng quy trình đã có cùng STATE và nguồn hiện hành.
Khi dịch hội thoại hoặc biên tập bản Việt AI, đọc thêm
[cách phân xử nghĩa và câu Việt](references/language-review.md) ở lần đầu;
đó là phần dùng để chọn bản dịch, không chỉ là checklist sau khi viết.

| Khi cần | Đọc hoặc dùng |
|---|---|
| Tra xa, nối lượt, nguồn thay đổi, sổ lớn | [Ngữ cảnh và trạng thái](references/context-and-state.md) |
| Hội thoại, xưng hô, mơ hồ, giọng hoặc biên tập bản Việt AI | [Phân xử nghĩa và câu Việt](references/language-review.md) |
| Có bản sửa của user hoặc cần áp dụng bài học từ lượt trước | [Học từ bản sửa](references/learning-from-edits.md) |
| Kiểm key, định dạng, placeholder, markup | [Kiểm kỹ thuật](references/technical-checks.md) |
| Tạo STATE | [Mẫu STATE](assets/chat-state.md) |
| User cần hướng dẫn tự chứa để dán sang chat khác | [Bản TXT được sinh tự động](assets/chat-instructions.txt) |
| User cần lời nhắc tiếp lượt | [Lời nhắc ngắn](assets/chat-turn.txt) |
| Tìm căn cứ thiết kế hoặc cải tiến skill | [Nghiên cứu](references/research.md), [đánh giá](references/evaluation.md) |

Không nạp toàn bộ tài liệu cho một đoạn dịch đơn giản. Công cụ cục bộ chỉ hỗ
trợ đọc, kiểm và xuất file; không cần dịch vụ bộ nhớ, đăng ký nguồn hay engine
riêng để dịch. Không tự apply patch vào game.

Khi sửa skill, sửa tài liệu nguồn rồi chạy `scripts/build_chat_prompt.py`;
không sửa tay bản TXT được sinh. Kiểm cấu trúc skill, bản TXT có khớp nguồn,
test của helper bị ảnh hưởng và một tình huống dịch mới theo tài liệu đánh giá.
Giữ lore, glossary và dữ liệu thử ngoài gói skill dùng chung.
