# 04 — Checklist bao phủ theo thành phần

Đây là danh sách **gợi ý điều kiện kiểm thử** cho mỗi màn hình / API — không phải danh sách bắt buộc. Với mỗi mục **liên quan và có rủi ro**, tạo điều kiện `CO-xx` trong `analysis.md`; mục liên quan nhưng không kiểm thử thì ghi `N/A - <lý do>`. Không tạo case chỉ để "đủ checklist".

Mục đánh dấu ⚠ mà tài liệu không nêu rõ hành vi → **không tự quyết định kết quả**: tạo `Q-xx`; nếu cần tiếp tục, dùng `IMP-xx` (kỳ vọng đề xuất, có cơ sở) hoặc `AS-xx` (giả định tạm) theo `rules/01` §2 — case dựa trên chúng là *Needs Clarification*.

## A. Trường nhập liệu

**Text / Textarea**
- Bắt buộc: để trống, chỉ nhập khoảng trắng
- Độ dài: min-1, min, max, max+1 (BVA); hành vi khi vượt max: chặn nhập hay báo lỗi ⚠
- Khoảng trắng đầu/cuối có được trim ⚠
- Ký tự đặc biệt, Unicode, tiếng Việt có dấu, emoji
- HTML/script injection hiển thị dạng text, không thực thi
- Paste nội dung dài

**Số (số lượng, tiền, %)**
- Biên min/max, 0, số âm, thập phân (số chữ số sau dấu phẩy), số rất lớn
- Chữ, ký tự đặc biệt, dấu phân cách hàng nghìn `1.000` vs `1,000` ⚠
- Định dạng hiển thị tiền tệ, làm tròn ⚠

**Email / SĐT / Mã số**
- Định dạng đúng; thiếu `@`, thiếu domain, có khoảng trắng, quá dài
- SĐT: đầu số, số chữ số, có/không `+84` ⚠
- Trùng với dữ liệu đã tồn tại (unique)

**Mật khẩu**
- Quy tắc độ mạnh (độ dài, hoa, thường, số, ký tự đặc biệt) — mỗi quy tắc vi phạm 1 test case
- Hiển thị dạng ẩn, nút ẩn/hiện; xác nhận mật khẩu không khớp
- Không lộ mật khẩu trong URL / log / thông báo lỗi

**Ngày / Giờ**
- Định dạng, ngày không tồn tại (31/02), năm nhuận 29/02
- Ngày quá khứ / tương lai / hôm nay theo quy tắc
- Khoảng ngày: từ > đến, bằng nhau, vượt khoảng tối đa
- Múi giờ ⚠

**Dropdown / Radio / Checkbox / Multi-select**
- Giá trị mặc định; danh sách đầy đủ, đúng thứ tự
- Không chọn (bắt buộc); chọn tối đa / vượt tối đa (multi-select)
- Dropdown phụ thuộc (chọn Tỉnh → nạp lại Huyện)

**Upload file**
- Định dạng cho phép / không cho phép (đổi đuôi file giả mạo)
- Dung lượng: 0 byte, max, max+1
- Số file tối đa; tên file có dấu, ký tự đặc biệt, rất dài
- Huỷ upload, upload lại, xem trước, xoá file đã upload

## B. Form & hành động

- Submit với dữ liệu hợp lệ → lưu đúng, hiển thị lại đúng sau reload
- Submit lỗi → giữ lại dữ liệu đã nhập, focus/scroll tới trường lỗi ⚠
- Nhiều lỗi cùng lúc → hiển thị tất cả hay lần lượt ⚠
- Double-click submit → không tạo trùng
- Nút Huỷ / Đóng / Back khi có dữ liệu chưa lưu → cảnh báo ⚠
- Phím Enter submit form; Tab chuyển trường đúng thứ tự
- Trạng thái nút: disabled khi chưa đủ điều kiện, loading khi đang xử lý

**Sự kiện kích hoạt & kênh** (bảng `EV-xx`, `rules/01` Bước 3.5 — **bắt buộc xét** cho mỗi hành vi chính, mỗi mục kết luận CO / N/A / Pending):
- *Khi nào hệ thống áp dụng hành vi:* lần đầu vào màn hình · tải lại (F5) · sau thao tác của người dùng trên màn hình · khi bấm hành động chính (submit / mua / lưu) · dữ liệu đổi ở nền trong lúc đang mở màn hình (realtime hay chỉ khi tải lại ⚠) · hết thời gian / phiên
- *Ở đâu cùng dữ liệu được truy cập:* màn hình chính · kênh hiển thị thứ hai (mini-cart, badge, widget, email, thông báo) · truy cập thẳng URL của bước sau (bỏ qua bước kiểm tra) · nút Back / lịch sử trình duyệt · tab / phiên / thiết bị thứ hai cùng tài khoản · đăng xuất – đăng nhập lại · API (khi có)
- Với mỗi tổ hợp: hành vi có được áp dụng nhất quán không? Dữ liệu ở kênh khác có đồng bộ không? Bước kiểm tra có bị bỏ qua được không?

## C. Danh sách / Bảng / Tìm kiếm

- Danh sách rỗng (empty state), 1 bản ghi, nhiều bản ghi
- Phân trang: trang đầu, trang cuối, đổi số bản ghi/trang, tổng số đúng
- Sắp xếp từng cột tăng/giảm; sắp xếp tiếng Việt có dấu
- Tìm kiếm: khớp chính xác, một phần, không phân biệt hoa thường ⚠, có dấu/không dấu ⚠, không có kết quả, ký tự đặc biệt
- Lọc: từng bộ lọc, kết hợp nhiều bộ lọc, xoá bộ lọc (reset)
- Xuất file (Excel/CSV/PDF): dữ liệu khớp với bộ lọc hiện tại

## D. Phân quyền & phiên

- Ma trận vai trò × hành động (xem `02` mục PERM)
- Truy cập trực tiếp URL / gọi API khi không có quyền → 403 / chuyển hướng
- Chưa đăng nhập truy cập trang cần đăng nhập
- Phiên hết hạn khi đang thao tác; đăng xuất rồi bấm Back
- Người dùng A không xem/sửa được dữ liệu của người dùng B (IDOR)

## E. Nghiệp vụ & dữ liệu

- Mọi quy tắc nghiệp vụ `BR-xx` (Decision Table)
- Mọi trạng thái và chuyển đổi (State Transition) — ma trận *Trạng thái × Sự kiện* không để ô trống
- Tương tác giữa yêu cầu (bảng `IX-xx`): yêu cầu A thay đổi dữ liệu mà yêu cầu B phụ thuộc — đặc biệt khi tập thoả điều kiện của B trở thành rỗng / 1 phần tử
- Tập phần tử (`rules/02` §DT *Tập phần tử*): phần tử ngoài tập chọn, phần tử duy nhất, ≥2 phần tử khác rule cùng lúc
- Tính toán: tổng tiền, thuế, chiết khấu, làm tròn — kiểm tra bằng con số cụ thể
- Đồng thời: 2 người cùng sửa / cùng mua món hàng cuối cùng
- Toàn vẹn dữ liệu: xoá bản ghi đang được tham chiếu; huỷ giao dịch giữa chừng → rollback

## F. Tích hợp & thông báo

- API ngoài thành công / lỗi 4xx / 5xx / timeout → hệ thống xử lý thế nào ⚠
- Email / SMS / push: được gửi, đúng người nhận, đúng nội dung, đúng thời điểm
- Job định kỳ / batch: chạy đúng lịch, xử lý dữ liệu đúng

## G. API (khi tài liệu có đặc tả API)

- Status code đúng cho từng trường hợp (200/201/400/401/403/404/409/422/500)
- Schema response; trường bắt buộc thiếu; sai kiểu dữ liệu
- Auth: thiếu token, token hết hạn, token của user khác
- Idempotency (gọi lại cùng request), phân trang, giới hạn tần suất (rate limit) ⚠

## H. Phi chức năng (chỉ khi tài liệu có yêu cầu hoặc rủi ro rõ)

- **Bảo mật cơ bản (OWASP):** XSS, SQL injection ở ô nhập, IDOR, dữ liệu nhạy cảm không lộ trong response/log, khoá tài khoản sau N lần sai
- **Hiệu năng:** thời gian phản hồi theo SLA trong tài liệu (ghi con số cụ thể)
- **Tương thích:** trình duyệt / thiết bị / độ phân giải được hỗ trợ (dùng Pairwise)
- **Responsive:** mobile / tablet / desktop
- **Accessibility (WCAG 2.1 AA):** điều hướng bằng bàn phím, label cho input, độ tương phản, alt cho ảnh
- **Đa ngôn ngữ:** chuyển ngôn ngữ, văn bản dài không vỡ layout, định dạng ngày/số theo locale

## I. UI tĩnh (gộp theo thành phần và mục tiêu quan sát được — `rules/03` §Một mục tiêu)

- Nhãn, placeholder, tooltip, dấu `*` bắt buộc đúng tài liệu/mockup
- Thứ tự trường, căn lề, chính tả
- So sánh với mockup/Figma nếu có — chênh lệch ghi vào *Câu hỏi làm rõ*
