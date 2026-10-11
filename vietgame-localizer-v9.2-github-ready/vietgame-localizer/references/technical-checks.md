# Kiểm kỹ thuật theo định dạng

Giữ key/resource/namespace, locale/build, encoding, escape và cấu trúc của
nguồn/đích thực tế. Key không bắt buộc là số. Không tự chuẩn hóa hoa/thường,
Unicode hoặc khoảng trắng có ý nghĩa. Chuỗi `None`, `null`, `[empty]` là văn
bản bình thường trừ khi định dạng dự án khai rõ marker; JSON null thật không
tự thành chuỗi rỗng. Không dùng số record/marker của game khác làm chuẩn.

## Những gì cần đối chiếu

- Key dự kiến, thiếu/thừa/trùng, thứ tự xuất; nội dung rỗng ngoài chủ ý.
- Placeholder có tên/index: bảo toàn tên, kiểu và số lần; có thể đổi vị trí
  nếu dialect cho phép. `%s`/`%d` không đánh số phải giữ đúng thứ tự đối số.
- Tag: nội dung được bảo vệ, thuộc tính quan trọng, cặp đóng/mở và lồng nhau.
  Tag khác engine không mặc nhiên là HTML.
- Escape/control: không mất, đổi loại hoặc double-escape. Phân biệt hai ký tự
  `\n` với newline thật; phân biệt xuống dòng trình bày với điều khiển bắt buộc.
- Bản xuất cuối mở lại được theo đúng parser; JSON/CSV/PO/plural phải giữ cấu
  trúc native. Có parser đúng engine thì dùng kiểm round-trip và cú pháp.

ICU/MessageFormat có nhánh lồng, selector, offset, quoting và `#`; regex
placeholder đơn không đủ kiểm nó. Dịch mỗi message/nhánh trong ngữ cảnh,
giữ liên kết biến–vai. Không tự xóa nhánh plural vì suy đoán về tiếng Việt;
đổi cấu trúc locale chỉ khi đã xác định runtime/build và hợp đồng đích.

## Helper tùy chọn khi có Python

`scripts/check_patch.py` dùng standard library, chỉ đọc file. Nó kiểm **nguồn
đúng phạm vi được giao**, không tự chọn batch hoặc hiểu nội dung truyện.

```text
python -B -X utf8 scripts/check_patch.py --source SELECTED_SOURCE.txt --patch PATCH.txt --format idpipe --tokens brace,printf,tags,escapes
```

`--source` phải là tập key dự kiến đã lấy từ nguồn gốc trước khi xem key của
patch. Không dựng nguồn kiểm bằng cách chỉ lấy những key patch đang có, vì như
vậy không phát hiện được phần bỏ sót. Giữ nguồn gốc và mapping của bản trích.
Nếu có key chưa chốt, kiểm patch hoàn tất bằng phạm vi đã trừ **danh sách key
chưa chốt tường minh** rồi đối chiếu tổng phạm vi ở STATE; không âm thầm loại key.

Hai dạng đầu vào hỗ trợ:

- `idpipe`: một record `key| text` mỗi dòng, tách dấu `|` đầu tiên; bỏ tối đa
  một dấu cách separator ngay sau nó. Phần text còn lại giữ nguyên. Dùng
  JSONL nếu key chứa `|` hoặc text cần newline thật.
- `jsonl`: mỗi dòng là object có đúng hai trường `key` và `text` kiểu string. Key ghép nhiều
  thành phần phải tạo không mất identity; không chỉ lấy đuôi key bị trùng.

Không truyền `--tokens` thì chỉ kiểm cấu trúc record/key; không nhận token đã
qua kiểm. Chỉ bật các nhóm đúng cú pháp dự án. `--literal` có thể lặp để bảo
vệ marker cụ thể; `--hard-newlines` kiểm số, kiểu và thứ tự newline thật khi đó là ràng buộc;
`--allow-reorder` chỉ dùng khi đích cho phép đảo thứ tự record.

Kết quả JSON ghi loại kiểm, số record, hash của bytes thật và các lỗi. Exit 0
là không thấy lỗi trong phạm vi check đã bật; exit 1 là mismatch; exit 2 là
đầu vào/cú pháp không hỗ trợ. Brace helper chỉ nhận placeholder đơn, không
nhận ICU/nesting/doubled brace là đã kiểm. Tag helper chỉ hỗ trợ một tập cú
pháp cơ bản; dùng parser engine khi cần. Bản chuyển thành JSONL không chứng
minh file native đã round-trip hoặc chạy đúng trong game.

Escape scanner đọc mọi dấu backslash, hỗ trợ các escape đơn thông dụng
(`\\`, `\n`, `\r`, `\t`, `\a`, `\b`, `\f`, `\v`, `\0`, quote, slash),
`\u` bốn hex và `\x` hai hex; escape lạ hoặc cụt báo unsupported. Printf
dang dở như `%1$`, `%*`, `%.` cũng báo unsupported. Phần trăm văn bản như
`50%` được đếm như ký tự literal; đây là quy ước helper, không parser đầy đủ
mọi dialect. Các phép đếm không xác định token còn gắn đúng người/vai nghĩa;
người dịch vẫn phải đối chiếu nội dung và cú pháp engine.

Nếu helper báo lỗi, đọc và sửa nguyên nhân rồi kiểm bản cuối. Nếu định dạng
không được hỗ trợ, dùng parser sẵn có phù hợp hoặc báo chưa kiểm loại đó;
không tắt check lỗi rồi gọi toàn bộ file “PASS”. Không có công cụ thì kiểm
trong khả năng đọc và nói rõ phạm vi. Helper không kiểm nghĩa, xưng hô, STATE
hay ép model luôn thực hiện quy trình; nó trả lỗi xác định khi thực sự được chạy.
