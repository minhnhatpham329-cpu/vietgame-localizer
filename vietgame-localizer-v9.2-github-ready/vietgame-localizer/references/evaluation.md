# Kiểm khi sửa skill

Chọn kiểm theo thay đổi, không biến mỗi lượt dịch thành một dự án benchmark.
Unit test xác nhận helper làm đúng hợp đồng kỹ thuật; không chứng minh bản
Việt đúng nghĩa. Phản hồi sử dụng thực của user và đánh giá ngôn ngữ cần ghi
riêng, không phủ nhận chỉ vì chưa có điểm benchmark công khai.

Với thay đổi cách dịch, ưu tiên thử ngôn ngữ hơn thêm unit test không liên
quan. Có thể so V9.1/V9.2 trên cùng nguồn/bản Việt cũ với context riêng, chấm
đầu ra theo lỗi có chứng cứ. Nếu cả hai làm đúng, báo chưa thấy lợi thế của
bản mới trên mẫu đó. Không buộc phải tìm một lỗi để hợp thức hóa cập nhật.

Các trường hợp phân biệt cần có khi sửa phần này: chỉ cho phép đổi cách gọi
mà chưa nhận lời; cùng người khác vai xã hội; lời đáp sửa trọng tâm thay vì
toàn mệnh đề; từ Việt làm thêm tiền giả định; một bài học đúng ở câu mới nhưng
không được lan sang nghĩa khác. Dữ liệu/đáp án thử giữ ngoài skill.

## Kiểm gói và helper

```text
python -B -X utf8 scripts/build_chat_prompt.py --check
python -B -X utf8 -m unittest discover -s tests -p "test_*.py"
python -B -X utf8 <skill-creator>/scripts/quick_validate.py <skill-folder>
```

Kiểm link nội bộ và file cần phân phối; bỏ cache khỏi gói. Khi đổi hướng dẫn,
sinh lại `assets/chat-instructions.txt` bằng script trước `--check`. Không có
engine cũ trong gói chat thì không yêu cầu self-test engine đó.

Helper cần phát hiện mutation thiếu/thừa/trùng key, sai thứ tự, mất token,
token lặp, đổi vai printf, tag hỏng, giá trị null sai kiểu, định dạng không hỗ
trợ; đồng thời chấp nhận trường hợp hợp lệ như placeholder có tên đổi vị trí.
Fixture 1.000 record chỉ kiểm coverage kỹ thuật, không là dịch thử 1.000 câu.

## Thử hành vi mới, có giới hạn rõ

Với thay đổi lớn, dùng một tình huống chưa lấy làm ví dụ trong hướng dẫn. Nếu
có delegation được phép, giao agent độc lập yêu cầu thực tế, skill và nguồn
thô tối thiểu; không đưa đáp án, bẫy dự kiến hay kết luận của người sửa skill.
Giữ nguồn/đầu ra/test report ngoài thư mục skill.

Thử hai lượt: lượt đầu tạo PATCH + STATE; lượt sau chỉ có hướng dẫn, nguồn,
STATE và patch cần thiết. Kiểm lời đáp đầu lượt, cặp xưng hô quay lại sau chen
ngang, câu neo gốc và mục sổ của nhân vật tạm vắng. Có thể thử nguồn đổi hoặc
thông tin mới cần sửa ngược; giữ mức tiết lộ cũ. Một lượt dùng cùng lịch sử
không được gọi là thử khôi phục trong chat mới.

Đọc output thật, chấp nhận nhiều cách Việt đúng. Ghi lỗi nghĩa/hành động,
phủ định/điều kiện, xưng hô, mất mạch, lẫn nhánh/spoiler, thuật ngữ, tự nhiên,
và lỗi kỹ thuật. Ghi cả lỗi mới do biên tập và số câu chưa chốt; giữ mọi câu
khó lại không đồng nghĩa chất lượng tốt hơn. Không chấm theo khớp từ đơn thuần.

Muốn khẳng định tốt hơn V9 thì cần so cùng model/nguồn/ngân sách, giữ case
đánh giá ngoài tài liệu đã dùng sửa, và người chấm không biết nhãn bản khi có
thể. Một agent dịch và root đọc lại bài tự tạo là thử quy trình có reviewer,
không là benchmark độc lập trên nhiều game. Không tuyên bố mức tăng chất lượng
chỉ từ việc rút gọn dung lượng hay thêm quy tắc.
