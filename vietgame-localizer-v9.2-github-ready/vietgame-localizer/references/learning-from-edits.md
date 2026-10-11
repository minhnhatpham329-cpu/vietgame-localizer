# Học từ bản sửa có phạm vi

Dùng khi user sửa/chốt câu, cung cấp bản biên tập tin cậy hoặc yêu cầu cải
thiện bản AI. Tri thức lưu vào STATE/kho của dự án, được đọc lại khi áp dụng;
không gọi đó là huấn luyện model hay hứa nhớ ngoài dữ liệu truy cập được.

## Từ bản sửa đến bài học dùng lại

Đọc nguồn, ngữ cảnh, bản cũ và bản user chọn. Hỏi bằng hành động: bản sửa đã
đổi **cách hiểu**, **cách gọi**, **khái niệm**, hay chỉ **cách diễn đạt**? Một
câu có thể đổi nhiều phần; giữ chúng riêng nếu phạm vi áp dụng khác nhau.

| Loại thay đổi | Lưu gì | Không suy ra |
|---|---|---|
| Sửa người làm/tham chiếu/phủ định | Kết luận đúng và câu nguồn phân xử; key phụ thuộc cần rà | Từ nào cũng phải thay bằng từ nào |
| Sửa xưng hô | Chiều cặp, tự xưng/gọi ai, tình huống hiệu lực, căn cứ/user chốt | Tuổi/giới/huyết thống hoặc chiều ngược khi chưa xác định |
| Chốt thuật ngữ | Khái niệm, nghĩa/cách dùng và biến thể cho phép | Mọi occurrence cùng chữ nguồn là cùng nghĩa |
| Chọn giọng/cách nói | Mẫu nguồn–Việt và cảnh phù hợp; lựa chọn riêng hay chỉ dẫn rộng được user nói rõ | Toàn nhân vật/game phải theo một mẫu từ một ví dụ |

User chọn một câu là chốt câu đó; chỉ mở rộng thành sở thích toàn dự án khi
họ nói rõ hoặc có căn cứ đủ trong các bản sửa cùng phạm vi. Nếu bản sửa có
vẻ đổi nghĩa, giữ yêu cầu user và chỉ ra chỗ khác nguồn cần làm rõ; không tự
biến nó thành fact truyện hay áp sang câu khác trước khi phân xử.

## Một mục học gọn, chỉ khi có ích

Lưu vào sổ lâu dài, không tạo file mới cho từng câu:

`ID | bài học | áp dụng khi | không áp dụng khi | key nguồn + bản chốt | ai chốt/trạng thái | key đã dùng/cần rà`

Điều kiện không áp dụng là ranh giới, không bắt viết phản ví dụ giả cho mọi
mục. Chỉ ghi cái có tác động: người nghe khác, cách dùng thuật ngữ khác, cảnh
công khai khác riêng tư, nhánh khác, nguồn sửa hoặc bản dịch chưa được duyệt.
Một key có thể đủ xác lập lựa chọn cụ thể; không đủ chứng minh luật ngôn ngữ chung.

Ví dụ cơ chế: user đổi “charge” thành “xung phong” trong lệnh tấn công.
Bài học gắn động tác chiến đấu đó; occurrence nói phí dịch vụ hoặc nạp điện
cần phân xử lại. Không chép nghĩa/giọng/tên từ ví dụ này vào glossary game.

## Dùng bài học ở lượt sau

Tra bằng identity/cặp/khái niệm hoặc loại lỗi đang gặp, rồi mở nguồn neo và
bản user chốt. So điều kiện áp dụng với câu mới trước khi dùng. Chỉ giống chữ
hoặc cùng tên nhân vật là chưa đủ. Nếu phù hợp, giữ phần đã chốt và diễn đạt
phần mới theo nguồn; không chép nguyên câu rồi thay tên/số máy móc.

Khi muốn nâng một sửa cá biệt thành hướng dẫn dùng lặp lại, tìm thêm một câu
thật cùng cơ chế và một trường hợp ranh giới nếu nguồn có, kiểm xem cách xử lý
có chuyển giao đúng không. Chưa có thì giữ bài học hẹp hoặc tạm thời; không
bịa dữ liệu thử hay dừng dịch để kiếm đủ ví dụ. Chốt tên riêng/quy ước cụ thể
của user được lưu ngay trong phạm vi đã yêu cầu.

Lần đầu áp dụng vào trường hợp mới, đối chiếu lại nguồn và cách người chơi
sẽ hiểu. Câu mới do AI tạo chỉ là ứng viên áp dụng; không tự nâng thành mẫu
đã được user chấp nhận. Một ví dụ dùng được không làm ranh giới bài học tự rộng hơn.

Khi user sửa ngược, kiểm xem bài học sai hay tình huống mới nằm ngoài phạm vi.
Sai thì đánh dấu bị thay và rà key đã dùng; phạm vi khác thì thêm biến thể,
không xóa quy ước cũ. Gom các sửa cùng nguyên nhân thành một mục, giữ ví dụ neo
đủ phân xử thay vì tích lũy hàng trăm quy tắc gần trùng nhau.

Không mang lore, cặp xưng hô hoặc sở thích riêng một game vào skill dùng chung.
Chỉ sửa hướng dẫn chung khi user yêu cầu và lỗi cho thấy cơ chế còn thiếu; khi
đó kiểm thêm tình huống khác để tránh sửa vừa khít một câu rồi làm hỏng câu khác.
