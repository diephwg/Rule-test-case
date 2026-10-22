# 05 — Review & Quality Gate

## Hai lớp kiểm soát

| Lớp | Ai kiểm tra | Kiểm tra gì | Không chứng minh được gì |
|---|---|---|---|
| **Validator** (`scripts/validate_testcases.py`) | Công cụ | Cột, giá trị hợp lệ, ID duy nhất/ổn định, truy vết Req → Mệnh đề → CO → TC, mọi dòng IX/EV và ô ma trận trạng thái có kết luận, tham chiếu Q/AS/SETUP tồn tại, phụ thuộc ghi bằng chữ tự do, đối chiếu AS ↔ case, trạng thái SETUP, chuỗi trong ngoặc kép có trong nguồn, ứng viên trùng lặp, mức sẵn sàng | Expected đúng nghiệp vụ, mệnh đề/tương tác/kênh đã liệt kê **đủ**, kỹ thuật áp dụng đủ, dữ liệu tái tạo được, case thật sự độc lập |
| **Phản biện độc lập** (`rules/01` Bước 5.3) | Subagent / lượt review riêng, không chung ngữ cảnh với người sinh | Điều kiện còn thiếu, phụ thuộc chưa đánh dấu — đặc biệt các thứ người sinh không nghĩ tới nên validator cũng không thấy | – |
| **Review nghiệp vụ** | Agent tự review, sau đó tester/QA lead | Checklist §Review bên dưới | – |

> Validator xác nhận các điều kiện cấu trúc mà công cụ kiểm tra được. **0 ERROR là điều kiện cần, không phải đủ.** WARNING là ứng viên cần review — sửa khi đúng là vấn đề, ngược lại giải trình trong `report.md`; **không sửa nội dung chỉ để hết cảnh báo**.

## Tiêu chí bàn giao (Definition of Done)

- [ ] Danh mục nguồn đầy đủ; nguồn chưa đọc được có ghi phần bị ảnh hưởng
- [ ] `analysis.md` đủ các mục theo mẫu; mọi `IMP` / `AS` có cơ sở và trạng thái xác nhận
- [ ] Mọi yêu cầu (trừ N/A) đã tách mệnh đề nguồn; mọi mệnh đề có `CO-xx` (hoặc N/A / Pending)
- [ ] Đã lập ma trận tương tác (`IX-xx`), bảng sự kiện kích hoạt & kênh (`EV-xx`), ma trận trạng thái đầy đủ (khi có ST), bảng tập phần tử (khi có DT trên tập) — mọi dòng/ô có kết luận
- [ ] Mọi `CO-xx` có case, hoặc `N/A - lý do`, hoặc `Pending - Q-xx`
- [ ] Mọi case gắn với ≥1 `CO-xx`; không có case tạo ra chỉ để đủ nhãn/tỷ lệ
- [ ] Validator 0 ERROR; mọi WARNING đã xử lý hoặc giải trình
- [ ] Đã review nghiệp vụ theo §Review
- [ ] Đã chạy phản biện độc lập; mọi phát hiện có kết luận *Đã sửa / Từ chối — lý do*
- [ ] Mọi `SETUP-xx` có trạng thái; SETUP *Chưa rõ cách làm* được liệt kê trong report kèm người cần cung cấp
- [ ] `report.md` nêu 5 chỉ số bao phủ (§Chỉ số) và mức sẵn sàng; đã xuất `testcases.xlsx`

Bộ test có case *Needs Clarification* / *Blocked* hoặc điều kiện *Pending* **vẫn bàn giao được** dưới dạng bản nháp có ích — miễn là báo cáo nói rõ phần nào sẵn sàng và phần nào đang chờ. Không gọi cả bộ là "hoàn chỉnh" khi còn phần chờ.

## Chỉ số bao phủ — báo cáo tách biệt, ghi rõ mẫu số

| # | Chỉ số | Mẫu số | Nguồn số liệu |
|---|---|---|---|
| 1 | Req_ID có case tham chiếu | Yêu cầu trừ N/A và bị từ chối | Validator |
| 2 | **Mệnh đề nguồn** có case · có case *Ready* (oracle đã xác nhận) | Mệnh đề trừ N/A và Pending | Validator |
| 3 | Điều kiện kiểm thử có case | `CO-xx` trừ N/A và Pending | Validator |
| 4 | Bao phủ theo kỹ thuật (phân vùng, biên, rule DT, chuyển trạng thái… đã chọn) và theo nguồn mở rộng (`IX`, `EV` có kết luận) | `CO-xx` theo cột *Kỹ thuật*; dòng IX / EV | Validator |
| 5 | Phần đang chờ | Số `CO` Pending, case Needs Clarification / Blocked, Q mở, AS/IMP chưa xác nhận, SETUP *Chưa rõ cách làm* | Validator |

Chỉ số 3 và 4 có mẫu số do người thiết kế tự đặt, và Gate 4 buộc mọi `CO-xx` (không N/A / Pending) có case — nên sau gate chúng gần như luôn đạt 100%. Coi đây là **kiểm tra nhất quán nội bộ**, không phải bằng chứng bao phủ nguồn. Chỉ số 4 theo kỹ thuật còn bị lệch vì mỗi CO / case chỉ ghi **một** kỹ thuật chính dù thực tế có thể kết hợp.

Chỉ số 1 **không** chứng minh mọi mệnh đề của yêu cầu đã được kiểm tra — đó là việc của chỉ số 2. Chỉ số 2 dùng mẫu số tách từ nguồn nên khách quan hơn chỉ số 3 (mẫu số do người thiết kế tự đặt); khi hai chỉ số lệch nhau, tin chỉ số 2. Chỉ công bố phần trăm khi mẫu số đã rõ; chỉ số chưa đo được ghi **"chưa đánh giá"**.

## Anti-pattern — phải sửa

| Anti-pattern | Ví dụ sai | Sửa thành |
|---|---|---|
| Kết quả mơ hồ | "Hoạt động bình thường", "Hiển thị đúng", "Như mong đợi" | Mô tả cụ thể cái nhìn thấy / dữ liệu thay đổi |
| Dữ liệu mơ hồ | "Nhập email hợp lệ", "Nhập số lớn" | `user01@test.com`, `101 (max=100)` |
| Nhiều mục tiêu độc lập trong 1 case | Kiểm tra cả đăng nhập, đổi mật khẩu, đăng xuất | Tách theo mục tiêu (nhiều assertion cho **một** mục tiêu thì được) |
| Nhiều giá trị lỗi trong 1 case | Email sai + mật khẩu rỗng cùng lúc | 1 giá trị không hợp lệ / case |
| Phụ thuộc chuỗi | "Dùng tài khoản tạo ở TC-005" | Ghi trạng thái vào Preconditions hoặc `SETUP-xx` |
| Bịa thông điệp / giới hạn | Tự đặt "tối đa 255 ký tự", tự viết chuỗi lỗi trong ngoặc kép | `Q-xx` + mô tả không ngoặc kép |
| Trình bày giả định như yêu cầu | Expected dựa trên AS nhưng không đánh dấu; phụ thuộc ghi bằng chữ tự do "cần xác nhận…" | `Q-xx` + `[Giả định AS-xx]` / `[Cần xác nhận Q-xx]` → Needs Clarification |
| Chỉ phân tích từng yêu cầu riêng lẻ | Có case "OOS tự bỏ tick" và "nút Disable khi không có SP được tick" nhưng không có case SP được tick **duy nhất** hết hàng | Ma trận tương tác `IX-xx`; bảng tập phần tử |
| Báo "chạy được" khi chưa có cách tạo dữ liệu | Precondition "admin đặt tồn kho = 0" nhưng không ai biết cách làm | `SETUP-xx` *Chưa rõ cách làm* → case Blocked |
| Case hình thức | Thêm case Negative, đổi nhãn Scenario hoặc Priority để đủ tỷ lệ / hết cảnh báo | Bao phủ theo điều kiện áp dụng; ghi lý do khi không áp dụng |
| Expected chỉ lặp lại step | Step "Nhấn Lưu" → Expected "Đã nhấn Lưu" | Kết quả *hệ quả* của hành động |
| Test chi tiết triển khai | "Kiểm tra hàm validateEmail()" | Hành vi người dùng quan sát được |

## Trùng lặp

> Chỉ coi hai case là **trùng** khi chúng kiểm tra **cùng mục tiêu, cùng ngữ cảnh nghiệp vụ** (vai trò, trạng thái, kênh thao tác, dữ liệu liên quan), **cùng phân vùng/biên** và **cùng kết quả kỳ vọng**. Chỉ gộp khi việc gộp không làm mất coverage hoặc khả năng phát hiện lỗi riêng.

- Cùng bước nhưng khác biên (BVA min và max), khác vai trò, khác trạng thái → **không** trùng.
- Khi gộp: giữ case có truy vết đầy đủ hơn, chuyển `Req_ID`/`CO-xx` của case kia sang, đặt case kia `Obsolete` (không xoá).
- Cảnh báo "ứng viên trùng lặp" của validator chỉ so khớp văn bản — người review quyết định có trùng về ngữ nghĩa hay không.

## Review — checklist (dùng cho tự review và skill `tc-review`)

**Căn cứ**
- Mỗi expected trỏ được về nguồn, `IMP` hoặc `AS`? Chuỗi trong ngoặc kép là nguyên văn?
- Case dựa trên `IMP`/`AS`/`Q` mở đã được đánh dấu — **theo từng assertion**, kể cả giả định ngầm (giá trị mặc định, thứ tự, thời điểm cập nhật)?
- Phép tính trong expected đúng (tự tính lại)?

**Bao phủ**
- Mệnh đề nguồn đã tách **đủ** (đối chiếu lại từng câu của nguồn)? Có mệnh đề nào gộp hai khẳng định độc lập?
- Mỗi yêu cầu có đủ điều kiện kiểm thử áp dụng: luồng được phép, hành vi bị chặn, dữ liệu không hợp lệ, biên, ngoại lệ? Điều kiện bỏ qua có lý do?
- Ma trận tương tác có đủ cặp yêu cầu dùng chung thực thể? Bảng tập phần tử có phần tử ngoài tập chọn, phần tử duy nhất, ≥2 phần tử khác rule?
- Ma trận trạng thái không còn ô trống? Bảng sự kiện × kênh đã xét tải lại, URL trực tiếp, kênh hiển thị thứ hai, tab/phiên thứ hai?
- Tổ hợp khả thi bị loại có lý do **chứng minh** hành vi không đổi?
- Kỹ thuật được chọn đã bao phủ đủ mục của nó (mọi phân vùng, biên đã chọn, rule khả thi, chuyển đổi hợp lệ)?
- Luồng ngoại lệ (mất mạng, timeout, phiên hết hạn, huỷ giữa chừng) đã xét theo rủi ro?
- Phân quyền đã xét chặn qua URL/API khi có rủi ro?

**Thực thi được**
- Tester mới chạy được không cần hỏi? Dữ liệu/setup tái tạo được, có cách tạo trạng thái, cách xác minh, cách reset? Trạng thái SETUP ghi đúng thực tế?
- Case độc lập với thứ tự chạy?
- Expected quan sát/xác minh được (ghi cách xác minh nếu ngoài UI)?

**Priority & nhãn**
- Priority khớp đánh giá rủi ro (không khớp tỷ lệ)?
- Scenario chọn theo quy tắc `rules/03` §Scenario?

**Bảo trì**
- ID duy nhất, ổn định; case mới dùng số tiếp theo theo lịch sử; case loại bỏ là Obsolete (không xoá)
- Không hard-code dữ liệu dễ đổi khi không cần (ngày hiện tại → "ngày hiện tại + 1")

## Mức độ phát hiện khi review

| Mức | Nghĩa |
|---|---|
| `Critical` | Thiếu bao phủ điều kiện rủi ro cao, expected sai so với nguồn, giả định trình bày như yêu cầu |
| `Major` | Thiếu điều kiện áp dụng quan trọng, case không thực thi/tái tạo được |
| `Minor` | Văn phong, dữ liệu chưa cụ thể, Priority/nhãn lệch so với rủi ro |
| `Suggestion` | Đề xuất bổ sung theo kinh nghiệm (EG) |
