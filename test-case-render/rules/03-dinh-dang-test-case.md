# 03 — Định dạng test case

File chuẩn: `output/<FEATURE>/testcases.csv` — UTF-8 (có BOM để Excel đọc đúng tiếng Việt), phân cách `,`, ô có xuống dòng/dấu phẩy đặt trong `"..."`. Header lấy nguyên từ `templates/testcases-template.csv`. Số cột, tiền tố Title, thang Priority là **quy ước nội bộ**.

## Các cột (đúng thứ tự)

| # | Cột | Bắt buộc | Giá trị / Quy tắc |
|---|---|---|---|
| 1 | `TC_ID` | ✔ | `TC-<MODULE>-<NNN>` (vd. `TC-LOGIN-001`). Duy nhất, ổn định — xem §ID |
| 2 | `Module` | ✔ | Tên module/màn hình (vd. `Đăng nhập`, `Giỏ hàng`) |
| 3 | `Req_ID` | ✔ | ID yêu cầu trong `analysis.md`; nhiều ID cách nhau `;`. Chỉ ghi yêu cầu mà case **thực sự kiểm tra một mệnh đề của nó** |
| 4 | `Title` | ✔ | Bắt đầu bằng **"Kiểm tra"** (tiếng Anh: **"Verify"**). Nêu *điều kiện* + *kết quả kỳ vọng*. ≤ 150 ký tự |
| 5 | `Test_Type` | ✔ | `Functional` · `UI` · `Validation` · `Integration` · `API` · `Security` · `Performance` · `Accessibility` · `Compatibility` · `Usability` |
| 6 | `Scenario` | ✔ | `Positive` · `Negative` · `Boundary` · `Edge` — chọn theo §Scenario |
| 7 | `Technique` | ✔ | `EP` · `BVA` · `DT` · `ST` · `UC` · `PW` · `CRUD` · `PERM` · `EG` · `CL` (kỹ thuật chính) |
| 8 | `Priority` | ✔ | `P1` · `P2` · `P3` · `P4` — theo rủi ro, §Priority |
| 9 | `Preconditions` | (nên có) | Trạng thái hệ thống/dữ liệu/tài khoản **trước** khi chạy, tái tạo được; hoặc `Theo SETUP-xx` + phần khác biệt. Nhiều ý → đánh số `1.` `2.` |
| 10 | `Test_Data` | | Giá trị cụ thể: `Email: user01@test.com; Mật khẩu: Abc@1234` |
| 11 | `Steps` | ✔ | Đánh số `1.` `2.` … mỗi dòng **một hành động**, câu mệnh lệnh |
| 12 | `Expected_Result` | ✔ | Kết quả quan sát được. Nhiều điểm kiểm tra → đánh số theo bước: `3. Hiển thị ...`. Mỗi số bước xuất hiện **một** dòng, tăng dần; nhiều assertion ở cùng một bước thì gộp trên một dòng, ngăn cách bằng `;` (validator WARN khi số lặp) |
| 13 | `Automation` | | `Yes` · `No` · `Candidate` |
| 14 | `Status` | | Kết quả **thực thi**: `Not Run` (mặc định) · `Pass` · `Fail` · `Blocked` · `Skipped` · `Obsolete`. Không dùng để ghi mức sẵn sàng thiết kế |
| 15 | `Notes` | | Đánh dấu phụ thuộc (§Notes), rule DT, ghi chú cập nhật, regression bug |

Mức sẵn sàng thiết kế (*Ready / Needs Clarification / Blocked*) **không** là một cột trong CSV — validator tự tính từ `Notes` + `Req_ID` + `SETUP-xx` tham chiếu + `analysis.md`, bản Excel hiển thị thành cột `Design_Status` (`rules/01` §Mức sẵn sàng).

## Scenario — cách chọn nhãn

`Scenario` là **một nhãn phân loại** để lọc và thống kê; **không** dùng để chứng minh bao phủ (bao phủ đo bằng `CO-xx`). Chọn theo thứ tự ưu tiên, dừng ở nhãn đầu tiên khớp:

1. **`Boundary`** — dữ liệu chính của case là một giá trị biên của phân vùng có thứ tự (dù hệ thống chấp nhận hay chặn nó). Ghi rõ biên ở Title/Test_Data.
2. **`Edge`** — tình huống bất thường không phải biên: đồng thời, thời điểm (đổi tồn kho giữa chừng), lặp thao tác, trạng thái chuyển tiếp hiếm.
3. **`Negative`** — hệ thống phải **chặn / từ chối / báo lỗi / xử lý ngoại lệ**.
4. **`Positive`** — hệ thống **cho phép** và hoàn thành hành động.

Không đổi nhãn để cân bằng tỷ lệ. Một yêu cầu chỉ có case `Positive` là bình thường nếu các điều kiện "bị chặn / không hợp lệ" không áp dụng — ghi lý do ở điều kiện kiểm thử.

## Priority — theo rủi ro

Priority = ảnh hưởng khi lỗi × khả năng xảy ra × mức quan trọng của luồng nghiệp vụ (xem *Đánh giá rủi ro* trong `analysis.md`).

| Mức | Ý nghĩa | Ví dụ |
|---|---|---|
| `P1` Critical | Luồng nghiệp vụ cốt lõi; lỗi gây mất tiền, mất/sai dữ liệu, lỗ hổng bảo mật, chặn hoàn toàn tính năng | Đăng nhập đúng, thanh toán, sản phẩm hết hàng lọt vào đơn |
| `P2` High | Chức năng chính, validation quan trọng, luồng thay thế thường gặp | Sai mật khẩu, khoá tài khoản sau N lần |
| `P3` Medium | Chức năng phụ, biên ít gặp, thông báo, sắp xếp/lọc | Sắp xếp danh sách |
| `P4` Low | Thẩm mỹ, chính tả, căn lề, tooltip | Màu nút |

Phân bổ Priority chỉ là **thống kê hỗ trợ review**. **Không tăng/hạ Priority hoặc thêm case để đạt một tỷ lệ.** Nếu phân bổ trông bất thường, xem lại *đánh giá rủi ro*, không xem lại con số.

## Notes — đánh dấu phụ thuộc

| Đánh dấu | Khi nào | Ảnh hưởng |
|---|---|---|
| `[Cần xác nhận Q-xx]` | Expected/bước phụ thuộc câu hỏi chưa trả lời | Case = *Needs Clarification* |
| `[Giả định AS-xx]` | Expected dựa trên giả định tạm | Case = *Needs Clarification* tới khi AS được xác nhận |
| (Req_ID là `IMP-xx`) | Case kiểm tra kỳ vọng đề xuất | Case = *Needs Clarification* tới khi IMP được xác nhận |
| (Preconditions tham chiếu `SETUP-xx` *Chưa rõ cách làm*) | Chưa có cách tạo trạng thái / dữ liệu cần thiết | Case = *Blocked* tới khi SETUP có quy trình |
| `Regression DEV-xxxx` | Case kiểm tra lại bug đã biết | – |
| `DT1-R3` | Rule của bảng quyết định | – |

**Mọi phụ thuộc phải có ID.** Không ghi phụ thuộc bằng chữ tự do ("cần xác nhận…", "chưa rõ…", "giả định…", "TBD") — validator không đọc được câu chữ, nên case sẽ bị tính *Ready* sai. Thiếu câu hỏi → tạo `Q-xx` trước, rồi gắn marker.

**Rà theo từng assertion:** với mỗi dòng Expected và mỗi Precondition, hỏi *"điều này còn đúng với mọi câu trả lời có thể của các `Q-xx` đang mở không?"* — gồm cả giả định ngầm như giá trị mặc định (đã chọn sẵn?), thứ tự hiển thị, thời điểm hệ thống cập nhật, câu thông báo. Không → gắn marker và ghi `TC_ID` vào cột *Case bị ảnh hưởng* của `AS-xx` (validator đối chiếu hai chiều). Nếu viết được expected **không phụ thuộc** câu hỏi (vd. so với thứ tự quan sát ở bước trước thay vì thứ tự tự đoán), ưu tiên cách đó.

## Văn phong

**Trong `Expected_Result`, ngoặc kép chỉ dùng cho văn bản nguyên văn từ nguồn** (nhãn UI, thông điệp, mã lỗi). Validator đối chiếu các chuỗi trong ngoặc kép ở `Expected_Result` với tài liệu đã trích xuất. Ở `Steps`, ngoặc kép dùng được cho nhãn UI (nguyên văn) và giá trị nhập (dữ liệu test) — validator **không** đối chiếu `Steps`. Thông điệp chưa biết nguyên văn → mô tả không ngoặc kép + `[Cần xác nhận Q-xx]`. Dữ liệu test trong Expected (vd. mật khẩu đã nhập) không đặt trong ngoặc kép — tham chiếu `Test_Data`.

**Title** — `Kiểm tra <hành vi> khi <điều kiện>`:
- ✅ `Kiểm tra hiển thị lỗi "Email không đúng định dạng" khi nhập email thiếu ký tự @`
- ❌ `Test email` · `Kiểm tra email sai`

**Steps** — mệnh lệnh, dùng đúng tên nhãn UI:
- ✅ `1. Nhập "user01@test.com" vào ô "Email"` `2. Nhấn nút "Đăng nhập"`
- ❌ `1. Nhập thông tin và đăng nhập`

**Expected_Result** — quan sát được, đo được:
- ✅ `1. Hiển thị thông báo "Sai email hoặc mật khẩu" dưới ô Mật khẩu` `2. Vẫn ở màn hình Đăng nhập`
- ❌ `Hệ thống hoạt động bình thường` · `Hiển thị lỗi` · `Như mong đợi` · `Đăng nhập thành công` (thành công nghĩa là gì?)
- Khi liên quan, kiểm tra **UI** (hiển thị gì), **dữ liệu** (lưu/đổi gì) và **hệ quả** (email, log, trạng thái), kèm **cách xác minh** nếu không nhìn thấy trực tiếp trên UI (màn hình khác, API, DB, admin).

## Tái tạo được — Preconditions, Test_Data, SETUP

Tester mới phải chạy được case mà không cần hỏi. Mỗi case mô tả, hoặc tham chiếu `SETUP-xx` có nội dung xác định trong `analysis.md`:
- tài khoản / vai trò; dữ liệu định danh (SKU, mã đơn…); cấu hình nghiệp vụ; mốc thời gian; điều kiện môi trường;
- **cách chuẩn bị và reset** khi case làm thay đổi trạng thái dùng chung (tồn kho, khoá tài khoản…);
- cách xác minh expected nếu cần công cụ ngoài UI.

Chỉ tham chiếu `SETUP-xx` mà case **thật sự cần** (không đặt mọi SETUP vào mọi case) — vì trạng thái của SETUP quyết định case có bị *Blocked* không.

Case **không phụ thuộc** việc chạy case khác trước. Dữ liệu minh hoạ do tester tự chuẩn bị (vd. `SP-A`, `customer01@test.com`) phải được ghi là *cần chuẩn bị* trong `SETUP-xx`, phân biệt với dữ liệu đã xác nhận đang tồn tại trên môi trường. Nhãn UI và quy tắc nghiệp vụ vẫn phải có căn cứ từ nguồn.

## Một mục tiêu — tách / gộp

> Một test case kiểm tra **một mục tiêu nghiệp vụ hoặc một điều kiện kiểm thử xác định**. Được phép có nhiều assertion cùng chứng minh mục tiêu đó. **Tách** khi các mục tiêu có thể thành công/thất bại độc lập và việc gộp làm khó xác định kết quả, chạy lại hoặc báo lỗi.

- Mỗi giá trị không hợp lệ (EP invalid) → 1 case riêng.
- Giá trị hợp lệ khác nhau **cùng phân vùng và cùng ngữ cảnh** → chọn 1 giá trị đại diện.
- UI tĩnh: gộp theo **thành phần và mục tiêu quan sát được** (vd. "nhãn + placeholder của form Đăng nhập" là một mục tiêu; "thông báo lỗi hiển thị đúng vị trí" là mục tiêu khác). Không áp hạn mức số case UI mỗi màn hình.
- Chống trùng lặp: xem `rules/05` §Trùng lặp.

## ID — duy nhất và ổn định

- `TC_ID` duy nhất, **không tái sử dụng**, **không đánh số lại**, **không lấp khoảng trống**.
- Case mới dùng **số tiếp theo theo lịch sử ID của module** (kể cả ID đã Obsolete và ID trong `testcases-additional`). Validator chỉ đối chiếu với `--previous`; phần lịch sử ID ngoài file đó do người sinh tự rà.
- Case bị loại giữ ID, `Status = Obsolete`, `Notes` ghi lý do + phiên bản.
- Khoảng trống số thứ tự là bình thường.

## Ví dụ (CSV)

```csv
TC_ID,Module,Req_ID,Title,Test_Type,Scenario,Technique,Priority,Preconditions,Test_Data,Steps,Expected_Result,Automation,Status,Notes
TC-LOGIN-001,Đăng nhập,FR-01,Kiểm tra đăng nhập thành công với email và mật khẩu đúng,Functional,Positive,UC,P1,"Theo SETUP-01
1. Đang ở màn hình Đăng nhập","Email: user01@test.com; Mật khẩu: Abc@1234","1. Nhập ""user01@test.com"" vào ô ""Email""
2. Nhập ""Abc@1234"" vào ô ""Mật khẩu""
3. Nhấn nút ""Đăng nhập""","3. Chuyển tới màn hình ""Trang chủ""",Candidate,Not Run,
TC-LOGIN-005,Đăng nhập,FR-03,Kiểm tra chặn đăng nhập khi mật khẩu có 7 ký tự (dưới biên min 8),Validation,Boundary,BVA,P2,"Theo SETUP-01
1. Đang ở màn hình Đăng nhập","Email: user01@test.com; Mật khẩu: Abc@123 (7 ký tự)","1. Nhập email và mật khẩu theo Test_Data
2. Nhấn nút ""Đăng nhập""","2. Hiển thị lỗi ""Mật khẩu phải từ 8 đến 32 ký tự""; vẫn ở màn hình Đăng nhập",Candidate,Not Run,
```
