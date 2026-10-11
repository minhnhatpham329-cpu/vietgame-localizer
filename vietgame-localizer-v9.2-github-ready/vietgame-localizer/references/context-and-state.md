# Ngữ cảnh và trạng thái

Đọc khi gặp liên kết xa, nối lượt, nhánh truyện, nguồn thay đổi hoặc STATE lớn.

## Truy hồi có điểm dừng

| Vấn đề đang ảnh hưởng bản dịch | Căn cứ cần tìm |
|---|---|
| “I did”, “her”, vật hoặc chủ thể lược | Lời đề nghị/tiền ngữ thực sự, không chỉ vài dòng gần nhất |
| Tự xưng/gọi người nghe | Metadata, cặp có hướng, cảnh xác lập quy ước, người nghe/frame hiện tại |
| Từ đa nghĩa, tên/chức danh trùng | Concept và cách dùng trong cảnh; cùng chữ chưa là cùng identity |
| Mâu thuẫn hoặc tiết lộ muộn | Nguồn neo cũ + nguồn mới, nhánh, điều nhân vật biết ở từng cảnh |
| Câu dùng lại, key nhập nhánh | Các nơi gọi đã biết và điều kiện tới từng nơi |

Đọc trước tương tác để hiểu lời đáp; lấy cặp nguồn–Việt hiện hành khi cần giữ
giọng. Kết quả truy hồi là ứng viên, phải kiểm resource/key, identity, nhánh và
revision. Không đồng nhất điểm tương đồng với bằng chứng. Nguồn đa ngôn ngữ
chỉ đối chiếu khi đã nối đúng key/build; khác nghĩa cần ghi nhận và phân xử,
không chắp nửa câu mỗi locale thành một nội dung không có trong nguồn nào.

Khi thiếu căn cứ: nếu có câu Việt tự nhiên giữ đúng phạm vi nghĩa thì viết;
nếu chỉ khác cách diễn đạt hợp lệ thì theo quy ước/giọng; nếu khác nghĩa thì
tìm nguồn có thể phân xử. Không còn đầu mối thì giữ key chưa chốt và ghi câu
hỏi, nơi đã kiểm, kết quả, đầu mối cần thêm. Chỉ mở lại khi có căn cứ/phép đối
chiếu mới, không biến nhiều lần tóm tắt thành xác nhận.

Khi context chật, bỏ phần lặp/không liên quan trước. Giữ nguyên văn câu phân
xử, chủ thể, người nhận, phủ định và điều kiện; tóm tắt làm chỉ mục. Nguồn xa
giữ nhãn cảnh/nhánh; sắp nguồn theo diễn tiến đã xác minh, không theo thứ hạng
search. Không đặt số câu cố định thành cửa sổ tối ưu cho mọi cảnh.

## Khôi phục từ STATE

Đọc revision và parent; so nguồn/build/keyspace với hiện tại, mở patch thật
để lấy tập key đã giao và đoạn còn nối. Với nguồn không có key, chỉ số hàng chỉ
có giá trị trong chính bản trích xuất/build đã ghi nhận. Nguồn đổi thì cần bảng
đối chiếu được kiểm; không gán lại identity bằng text gần giống.

Nếu hai STATE cùng parent nhưng khác quyết định, đối chiếu bằng nguồn và patch;
không lấy file mới nhất theo ngày một cách máy móc. Không chỉ đưa delta rời khi
chat mới cần snapshot. Handover phải đủ để hiểu lời đáp đầu lượt mà không cần
lịch sử chat: lời đề nghị chưa đáp, ai làm gì, người/vật được lược, cặp đang nói
và câu neo nguồn–Việt. Đây là kiểm khả năng tiếp nối, không phải khai báo đã nhớ.

Giữ trạng thái của từng mục: có căn cứ, lựa chọn biên tập, giả thuyết, xung đột,
bị thay. Mục chưa đối chiếu không tự thành xác nhận qua các revision. Giọng/
thuật ngữ/cách gọi cần phạm vi dùng; quyết định quan trọng có ID và nhóm key
đã dùng để rà khi đổi. Không tạo hồ sơ phụ thuộc cho mọi câu UI.

Quy ước có biến thể công khai/riêng tư hoặc đóng vai phải ghi biến thể nào đang
có hiệu lực và dấu hiệu kết thúc; giữ cả quy ước cơ sở để lượt sau khôi phục.
Không chỉ lưu “hiện dùng tôi/ngài” rồi làm mất người nghe và lý do đổi. Điểm
kết thúc chưa rõ thì đánh dấu chưa rõ, không tự kéo biến thể sang mọi cảnh.

Khi lấy ví dụ nguồn–Việt để giữ giọng hoặc học cách gọi, lấy cả trạng thái ai
đã chốt và điều kiện áp dụng. Có mâu thuẫn thì phân xử phạm vi/căn cứ trước;
lượt mới hơn không tự đáng tin hơn. Cơ chế học cụ thể ở
[Học từ bản sửa](learning-from-edits.md).

## Cập nhật mà không viết lại quá khứ

| Nguồn mới | Xử lý |
|---|---|
| Làm rõ một tham chiếu từ trước | Rà key phụ thuộc, vẫn giữ mức tiết lộ ở cảnh cũ |
| Quan hệ đổi từ một cảnh | Thêm phạm vi mới, giữ quy ước phù hợp ở cảnh trước |
| Nhân vật chỉ tin/nói điều sai | Lưu ai tin/nói; giữ đúng điểm nhìn trong lời thoại |
| Sổ suy luận sai hoặc nguồn sửa | Đánh dấu mục bị thay, rà các key đã dùng và câu hỏi mở liên quan |
| Thêm lore không liên quan | Không mở lại toàn bộ bản dịch |

Ngày ghi nhận không là thời điểm sự kiện. Khi bản đồ phụ thuộc chưa đủ, tìm
thêm trong phạm vi liên quan và nêu giới hạn; không nhận đã tìm hết tự động.
Quy ước xưng hô cơ sở không bị ghi đè bởi một đoạn đóng vai hoặc nóng giận.

## Sổ lâu dài gọn và truy lại được

Sổ nhỏ giữ đủ trong STATE, kể cả nhân vật tạm vắng. Khi lớn đến mức cản đọc,
chuyển nhóm ít dùng sang kho có ID, nguồn neo và key phụ thuộc; chỉ rút khỏi
STATE sau khi file kho thật đã lưu và mở lại được. STATE giữ tên/phiên bản kho
và chỉ mục theo identity/cặp/chủ đề. Không chia hàng chục file theo batch.

Trước giao STATE mới, so mục cũ: mục còn dùng được giữ hoặc có đường tới kho;
mục đổi có căn cứ; vấn đề chưa giải còn nguyên; tình huống đã khép rời phần
hoạt động. Giữ lore và bản sửa riêng từng game, không đưa vào skill toàn cục.
