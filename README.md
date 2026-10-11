# VietGame Localizer

**Skill Việt hóa game bằng AI, chú trọng ngữ cảnh, xưng hô và tiến độ qua nhiều lượt dịch.**

Vietnamese game localization skill for AI agents, with context-aware forms of address,
scoped terminology, and resumable translation through PATCH + STATE.

**Phiên bản: 9.2 · [MIT License](LICENSE)**

## Skill giúp gì?

- Theo dõi ai nói với ai và cách xưng hô theo từng chiều; giữ quy ước khi nhân vật quay lại sau câu chen ngang.
- Phân biệt vai hành động, lời trích, nhánh truyện và thông tin chưa được tiết lộ.
- Giữ thuật ngữ theo khái niệm và ngữ cảnh; học từ bản sửa đã được người dùng chốt trong đúng phạm vi.
- Giao bản dịch dạng **PATCH** cùng **STATE** ghi tiến độ, quy ước và điểm còn cần làm rõ.
- Kiểm key, placeholder, tag và escape bằng helper Python tùy chọn.

Skill gồm hướng dẫn và công cụ hỗ trợ, sử dụng model AI bạn đang có. Nó không tự
trích xuất tài nguyên hay cài bản dịch vào game; bản dịch vẫn cần được biên tập và thử trong game.

## Cài vào Codex

Dán yêu cầu sau vào Codex:

```text
Dùng $skill-installer cài skill từ repository
https://github.com/minhnhatpham329-cpu/vietgame-localizer
với đường dẫn skill là vietgame-localizer.
```

Hoặc tải repo bằng **Code → Download ZIP**, giải nén và sao chép cả thư mục
`vietgame-localizer` vào thư mục skill người dùng `~/.agents/skills/`.
Trên Windows, vị trí này là `%USERPROFILE%\.agents\skills\`.

Thư mục được cài phải có `vietgame-localizer/SKILL.md` cùng các thư mục con.
Giữ nguyên cấu trúc khi sao chép. Nếu chưa thấy skill xuất hiện, khởi động lại Codex.
Xem [tài liệu OpenAI chính thức về skill](https://learn.chatgpt.com/docs/build-skills).

## Bắt đầu dịch

Đính kèm nguồn có key và ngữ cảnh bạn có, rồi dùng yêu cầu như sau:

```text
Dùng $vietgame-localizer để Việt hóa nguồn tôi gửi.
Game: [tên game và build nếu biết].
Mỗi lượt dịch 1.000 key, hoặc phần còn lại nếu ít hơn.
Giữ key, định dạng, placeholder và tag của nguồn.
Xuất PATCH và STATE để tiếp tục lượt sau.
Quy ước xưng hô/thuật ngữ đã chốt: [nếu có].
```

Các mục trong ngoặc vuông là thông tin bạn thay theo dự án. Bạn có thể chọn quy mô
khác; skill không bắt mỗi lượt phải dịch 1.000 key.

Trong cùng chat, nói **“tiếp”** để nối công việc khi nguồn và STATE vẫn truy cập được.
Khi chuyển chat, mang theo hướng dẫn, nguồn, STATE mới nhất và các file mà STATE dẫn tới.

## Dùng dưới dạng prompt trong chat

Nếu không cài skill, dùng [bản hướng dẫn TXT tự chứa](vietgame-localizer/assets/chat-instructions.txt):

1. Mở file, sao chép nội dung hoặc đính kèm vào chat mà model có thể đọc.
2. Gửi nguồn, yêu cầu dịch và quy ước dự án.
3. Giữ PATCH và STATE để nối lượt; chuyển chat thì cung cấp lại các file cần thiết.

Cách dùng này phụ thuộc khả năng đọc file và làm theo hướng dẫn của model.
Helper kiểm kỹ thuật chỉ chạy khi môi trường có Python và các script tương ứng.

## Kiểm kỹ thuật tùy chọn

Từ thư mục skill `vietgame-localizer/`, chạy bằng Python 3.10 trở lên:

```bash
python -B -X utf8 scripts/check_patch.py --source SELECTED_SOURCE.txt --patch PATCH.txt --format idpipe --tokens brace,printf,tags,escapes
```

`SELECTED_SOURCE.txt` phải là tập key dự kiến của lượt dịch, lấy độc lập từ nguồn.
Helper hỗ trợ `idpipe` và `jsonl`; chỉ bật nhóm token phù hợp cú pháp dự án.
Xem [phạm vi và giới hạn của helper](vietgame-localizer/references/technical-checks.md).
Kiểm kỹ thuật không chứng nhận bản dịch đúng nghĩa hoặc xưng hô.

## Cấu trúc repository

```text
README.md
LICENSE
vietgame-localizer/
├── SKILL.md
├── agents/
├── assets/
├── references/
├── scripts/
└── tests/
```

## Chất lượng và đóng góp

V9.2 đã được thử bằng các tình huống tổng hợp và kiểm nối lượt; phản hồi thực tế
được dùng để cải tiến. Chưa có benchmark độc lập trên nhiều game chứng minh mức
tăng chất lượng chung. [Cách đánh giá](vietgame-localizer/references/evaluation.md)
và [căn cứ thiết kế](vietgame-localizer/references/research.md) được lưu trong repo.

Bạn có thể [mở Issue](https://github.com/minhnhatpham329-cpu/vietgame-localizer/issues)
kèm câu nguồn, ngữ cảnh, bản dịch, cách sửa đề xuất và phiên bản skill/model.
Ví dụ ngắn đủ tái hiện lỗi sẽ giúp cải tiến nhanh hơn. Hãy chia sẻ repo cho người
đang Việt hóa game, và Star nếu skill hữu ích với bạn.

Để kiểm khi sửa skill, chạy trong `vietgame-localizer/`:

```bash
python -B -X utf8 scripts/build_chat_prompt.py --check
python -B -X utf8 -m unittest discover -s tests -p "test_*.py"
```

Khi sửa tài liệu nguồn, sinh lại bản TXT bằng `scripts/build_chat_prompt.py`.
Tên trước đây của skill là `game-viethoa-patch-translator`; bản công khai này
dùng tên `vietgame-localizer`, giữ quy trình dịch V9.2.
