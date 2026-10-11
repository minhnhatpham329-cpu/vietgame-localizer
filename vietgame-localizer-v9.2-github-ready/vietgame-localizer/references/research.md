# Căn cứ thiết kế — V9.2, cập nhật 2026-10-01

Các nguồn dưới đây hỗ trợ lựa chọn thiết kế. Phần áp dụng là điều chỉnh cho
skill; không chuyển điểm số từ nghiên cứu thành cam kết chất lượng game Việt.
Không cài framework, model, dịch vụ hay chép mã repo vào gói.

| Nguồn primary | Điều rút ra và áp dụng | Giới hạn |
|---|---|---|
| [Tan et al., ACL 2026 — What Does LLM Refinement Actually Improve?](https://aclanthology.org/2026.acl-long.268/) | Trong thí nghiệm literary MT, dịch theo tài liệu rồi sửa theo đoạn cho kết quả vững; tăng chủ yếu fluency, đúng nghĩa cải thiện hạn chế. Skill đọc theo cảnh, sửa cụm cần sửa và đối chiếu lại nguồn. | Không phải thử nghiệm game Việt; không suy rằng thêm vòng tự chấm dài sẽ tốt hơn. |
| [Pombal et al., TACL 2026 — Context-aware Translation-mediated Conversations](https://aclanthology.org/2026.tacl-1.26/), [repo tác giả](https://github.com/zeppombal/context-aware-mt) | Ngữ cảnh lượt gốc giúp dịch hội thoại trong các thử nghiệm của bài. Skill giữ câu neo nguồn bên cạnh bản Việt để nối lượt, không dùng bản Việt cũ làm bằng chứng ngược. | Bài có huấn luyện và thiết lập đánh giá riêng; skill không triển khai TowerChat hoặc chiến lược sinh nhiều ứng viên của repo. |
| [Peng et al., WMT 2025 — Self-Retrieval from Distant Contexts](https://aclanthology.org/2025.wmt-1.13/) | Ngữ cảnh xa có ích trong một số bài thử. Skill tìm theo quyết định đang thiếu, xác minh identity/nhánh trước khi dùng. | Lợi ích tùy dữ liệu/model; tìm bằng key/từ khóa không phải triển khai thuật toán SELF-RAMT. |
| [Ki & Carpuat, Findings NAACL 2024 — Post-editing with Error Annotations](https://aclanthology.org/2024.findings-naacl.265/) | Lợi ích từ feedback chi tiết khi chỉ prompt không rõ ràng trong thiết lập nghiên cứu. Skill chỉ ghi lỗi cần xử lý theo key, không bắt mọi câu tự lập MQM dài. | Cặp ngôn ngữ/model cụ thể, không cấm mọi hình thức phản hồi chi tiết. |
| [MQM Council — Scoring Models](https://www.themqm.org/mqm-pillars/the-mqm-scoring-models/) | Severity theo tác động tới hiểu/dùng nội dung; khác sở thích vẫn có thể là bản dịch chấp nhận được. Skill ưu tiên lỗi nghĩa/gameplay trước biên tập tùy ý. | Không tự đặt điểm chất lượng chung hoặc ngưỡng phần trăm từ vài câu. |
| [Weblate — Checks and fixups](https://docs.weblate.org/en/latest/user/checks.html), [repo checker ICU](https://github.com/WeblateOrg/weblate/blob/main/weblate/checks/icu.py) | Kiểm theo định dạng và công bố phần chưa kiểm; tránh tự sửa toàn cục. Helper cục bộ dùng lựa chọn token tường minh. | Không cài Weblate và không có đầy đủ parser/checker của Weblate. |
| [Unicode ICU — Formatting Messages](https://unicode-org.github.io/icu/userguide/format_parse/messages/) | Message lồng/nhánh và quoting cần hiểu cấu trúc. Giữ selector, offset, vai biến; dùng parser đúng runtime khi xác nhận cú pháp. | Helper brace đơn không kiểm ICU, không suy cấu trúc plural của mọi game từ ngôn ngữ đích. |

Các quyết định giữ STATE đầy đủ, đối chiếu tập key, lưu scope xưng hô và sinh
bản hướng dẫn TXT từ một nguồn là thiết kế của skill, không phải kết quả mà
các paper đã kiểm định. Các repo hữu ích để tham khảo cách làm/đánh giá; thêm
hệ thống training, database hay memory server chưa có lợi ích được chứng minh
cho công việc dịch trong chat này.

Chất lượng đã được user thử trong sử dụng thực tế là phản hồi có giá trị. Khi
báo thay đổi, tách phản hồi đó khỏi test helper và bài thử quy trình mới; không
gắn nhãn benchmark độc lập cho kết quả chưa được đánh giá theo thiết kế ấy.

## Bổ sung ngôn ngữ trong V9.2

Nguồn nghiên cứu được đối chiếu 2026-09-30; thiết kế và thử hành vi tiếp tục
ngày 2026-10-01.

[Bawden et al., NAACL 2018](https://aclanthology.org/N18-1118/) đánh giá hiện
tượng diễn ngôn bằng test theo ngữ cảnh; [Voita et al., ACL 2019](https://aclanthology.org/P19-1116/)
tập trung vào deixis, ellipsis và liên kết từ vựng. Các bài này là căn cứ để
kiểm bản dịch trong tương tác và bằng tình huống phân biệt, không chỉ câu đứng
riêng. Chúng không kiểm định cách xưng hô Việt hoặc chứng minh workflow này.

Thiết kế mới của skill: chọn từng thành phần xưng hô; phân biệt lời mời đổi
cách gọi với việc đã nhận lời; giữ trọng tâm đính chính; kiểm hàm ý do câu Việt
thêm vào; học bản sửa bằng điều kiện áp dụng và trường hợp ranh giới. Đây là
các thao tác biên tập được đề xuất, cần kiểm trên đầu ra thực. Không tự nhận là
thuật toán đã được nghiên cứu chứng minh hoặc một model được huấn luyện thêm.
