# Báo cáo bộ test case — DASHBOARD-DOANH-THU (Dashboard Doanh thu & Đơn hàng)

| Thông tin | Giá trị |
|---|---|
| Nguồn | `input/DASHBOARD-DOANH-THU/Tài liệu dashboard doanh thu đơn hàng.docx` (PRD + FRD Incentive + FRD Sales Metrics + định dạng migrate + 3 mockup) — xem Danh mục nguồn trong `analysis.md` |
| Ngày tạo | 2026-10-18 |
| Phiên bản | v1.1 (v1.0 + xử lý phản biện độc lập) |
| File | `testcases.csv`, `testcases.xlsx`, `analysis.md`, `review.md`; bản trước: `testcases.v1.0.csv`, `testcases-additional.v1.0.csv` |

## 1. Mức sẵn sàng

| Mức | Số lượng | Ghi chú |
|---|---|---|
| Ready | 134 | Expected có căn cứ đã xác nhận, chạy được khi SETUP *Cần chuẩn bị* đã làm |
| Needs Clarification | 39 | Phụ thuộc Q mở / AS chưa xác nhận — expected tạm thời |
| Blocked | 59 | Phụ thuộc SETUP *Chưa rõ cách làm* |
| SETUP chưa sẵn sàng | 4 | SETUP-03 (đẩy đơn kiểm soát qua HUB — dev), SETUP-04 (cấu hình Threshold Brand — dev), SETUP-06 (nơi xem Incentive — dev/BA, Q-09), SETUP-10 (công cụ import migrate — dev) |
| Điều kiện Pending | 16 | Chờ Q-08, 11, 20, 21, 25, 27–30, 36, 40–43, 46, 51 |
| Nguồn chưa đọc được | 4 | Prototype HTML/Figma; Confluence (FR-CSD-002, BRD); bảng Brand Incentive Config (SharePoint) |

**Kết luận:** 134/232 case chạy và đánh giá được ngay sau khi chuẩn bị tài khoản (SETUP-01), bộ dữ liệu QA (SETUP-02, mất ≥ 5 ngày lịch) và quyền đọc DB (SETUP-08). 39 case cần BA chốt câu hỏi (quan trọng nhất Q-01 đơn 0đ, Q-02 ngưỡng đơn vị Ngày). 59 case Blocked, gồm **toàn bộ nhóm Incentive (32) và Migrate (3)** — chưa có nơi hiển thị Incentive (Q-09) và chưa có cách cấu hình Threshold.

### Theo nhóm

| Nhóm | Ready | Needs Clarification | Blocked |
|---|---|---|---|
| 01. Bộ lọc kỳ & thuế | 7 | 5 | 0 |
| 02. Phạm vi dữ liệu & phân quyền | 13 | 3 | 7 |
| 03. Sales | 4 | 3 | 10 |
| 04. Transactions | 3 | 1 | 0 |
| 05. Frequency | 3 | 2 | 0 |
| 06. Coupon % | 2 | 1 | 0 |
| 07. AOV | 6 | 1 | 0 |
| 08. UPT | 3 | 2 | 0 |
| 09. Avg Spending/Customer | 6 | 1 | 0 |
| 10. Định dạng & nhãn | 9 | 2 | 2 |
| 11. Cảnh báo động | 0 | 3 | 2 |
| 12. Biểu đồ Sales theo thời gian | 39 | 9 | 3 |
| 13. Bộ chọn Store & lọc CA | 11 | 1 | 0 |
| 14. Xếp hạng Top/Bottom | 5 | 1 | 0 |
| 15. Bảng breakdown | 14 | 4 | 0 |
| 16. Incentive | 0 | 0 | 32 |
| 17. Migrate | 0 | 0 | 3 |
| 18. Phi chức năng | 9 | 0 | 0 |

## 1a. Lộ trình chạy liền mạch

Cột `Module` đánh số 01–18 theo thứ tự chạy; lọc Excel theo `Module` và `Design_Status`.

| Đợt | Chuẩn bị | Chạy nhóm | Lý do gom |
|---|---|---|---|
| 0. Ngày đầu | SETUP-01 (tài khoản), SETUP-07 (môi trường ~100 store), SETUP-08 (truy vấn đối soát), SETUP-09 (DevTools). Bắt đầu tạo SETUP-02 từ ngày D−1 (Thứ Sáu) | 01 Bộ lọc → 12 Biểu đồ (case dùng dữ liệu thật, kỳ cố định 2025–2026) → 13 Store → 14 Xếp hạng → 15 Bảng → 18 Phi chức năng; ở 10 Định dạng: case dùng dữ liệu thật (DISP-007, 008, 010, 011, 012, 013) | Chỉ cần đăng nhập U-CRM / U-RM-HER, không phụ thuộc dữ liệu QA. Đăng nhập U-CRM một lần chạy liên tục |
| 1. Sau D+3 | SETUP-02 hoàn tất (đối chiếu bảng 17.1 / 17.2 trong `analysis.md`) | 02 Phạm vi (đăng nhập lần lượt U-SM12 → U-CA-A → U-CA-B → U-MULTI → U-SM1) → 03 Sales → 04 Transactions → 05 Frequency → 06 Coupon → 07 AOV → 08 UPT → 09 Avg Spending → 10 Định dạng (phần dữ liệu QA) → 11 Cảnh báo → 12 Biểu đồ (case ST1/ST2 theo D) → 15 Bảng (TABLE-006, 010, 011, 013, 016) | Cùng một bộ dữ liệu ST1/ST2/ST3; với U-SM12 chọn kỳ D rồi kiểm 8 KPI liên tiếp theo bảng 17.2 |
| 2. Ngày chạy T | SETUP-12 (OB7, RC-T tạo trong ngày) | CHART-036, CHART-038 | Cần cột "hôm nay" |
| 3. Khi dev cung cấp | SETUP-03 / 04 / 05 / 06 / 10 / 11 | 03 Sales (header bất thường), 02 (ecom, giờ biên), 10 (950, half-up), 11 (VAT = 0), 12 (cột bằng nhau, cột rất nhỏ, trục < 1 triệu) → 16 Incentive → 17 Migrate | Phụ thuộc đẩy dữ liệu HUB / cấu hình |

## 2. Chỉ số bao phủ (từ validator)

| # | Chỉ số | Giá trị | Mẫu số |
|---|---|---|---|
| 1 | Req_ID có case tham chiếu | 26/26 | 27 yêu cầu trừ 1 N/A (NFR-INC-001 — chờ Q-20) |
| 2 | Mệnh đề nguồn có case · có case Ready | 212/212 · 131/212 | 227 mệnh đề trừ 1 N/A, 14 Pending |
| 3 | Điều kiện kiểm thử có case | 233/233 | 252 CO trừ 3 N/A, 16 Pending |
| 4 | Theo kỹ thuật · nguồn mở rộng | BVA 39/39 · CL 21/21 · DT 43/43 · EG 10/10 · EP 100/100 · PERM 11/11 · ST 9/9 · IX 33 dòng (CO 31, Pending 2) · EV 24 dòng (CO 15, N/A 3, Pending 6) · ma trận trạng thái 3 × 9 ô đều có kết luận | |
| 5 | Đang chờ | Pending 16 CO · Needs Clarification 39 · Blocked 59 · Q mở 51 · AS chưa xác nhận 9 · SETUP chưa rõ cách làm 4 | – |

Chỉ số 2 chỉ chứng minh mỗi mệnh đề đã tách có ≥ 1 case; việc tách đủ mệnh đề đã được phản biện độc lập kiểm tra (mục 6a).

## 3. Thống kê (tham khảo)

| Chỉ số | Giá trị |
|---|---|
| Tổng test case | 232 |
| Theo Priority | P1: 56 · P2: 91 · P3: 71 · P4: 14 |
| Theo Scenario | Positive: 120 · Negative: 24 · Boundary: 39 · Edge: 49 |
| Theo Test_Type | Functional 156 · UI 39 · Integration 13 · Security 10 · Validation 5 · Accessibility 3 · Performance 3 · Compatibility 2 · Usability 1 |
| Ứng viên tự động hoá | Đa số Candidate; Yes: đối soát API/phân quyền/hiệu năng |

## 4. Câu hỏi còn mở (ưu tiên Blocker/Major)

| ID | Câu hỏi (rút gọn) | Mức độ | Ảnh hưởng |
|---|---|---|---|
| Q-01 | Đơn 0đ có là transaction? Nguồn mâu thuẫn (BR-SPM-006 nói có; công thức net_amount > 0, AC-SPM-002-13, mockup "93 đơn 0đ không tính" nói không) | Blocker | AS-01: TRX-004, FREQ-005, CPN-002, AOV-007, UPT-004, FLT-007, SCOPE-005, DISP-011 |
| Q-09 | Incentive hiển thị ở đâu, drill-down thế nào | Blocker | Toàn bộ nhóm 16 (Blocked qua SETUP-06) |
| Q-02 | Ngày bấm được: 2–31 (PRD) hay 2–62 (FRD)? | Major | AS-02: CHART-005, 014, 017 |
| Q-03 | Chưa kết thúc có cần kỳ lọc kéo tới hôm nay? | Major | AS-03: CHART-004, 051 |
| Q-05 | Thuế mặc định | Major | FLT-011 |
| Q-07 | Thông báo lỗi khi > 366 ngày | Major | FLT-009 |
| Q-10 | Base giá trị dòng của Incentive; % chia hay tiền hoa hồng | Major | Nhóm 16 |
| Q-11 | Bảng Brand Incentive Config đầy đủ | Major | CO Pending |
| Q-13 | Khách chỉ có đơn trả có vào Total Customers? | Major | AS-06: FREQ-003, AVGS-004 |
| Q-14, Q-16 | Ecom ở Toàn Tam Sơn; B2B trong Sales | Major | SCOPE-010, SALES-016, đối soát dữ liệu thật |
| Q-17 | Dòng dịch vụ trong UPT | Major | UPT-003 |
| Q-18 | Nhận diện đơn trả, total/tax_total của đơn trả | Major | SALES-002, 005, 012 |
| Q-19 | FR-SPM-010/011 đã được business chấp thuận? | Major | Rủi ro phạm vi nhóm 12–15 |
| Q-20, Q-21, Q-30, Q-31, Q-36, Q-38, Q-40, Q-41, Q-42 | Refund Incentive; record migrate lỗi; bill 0 nhân viên; đơn trả ở mức Cá nhân; Position rời nhau; ví dụ 02/08–14/10 sai; KPI mức Cá nhân; cơ sở Discount %; quyền xem Incentive | Major | Xem `analysis.md` §13 |

Câu hỏi Minor: Q-04, 06, 08, 12, 15, 22–29, 32–35, 37, 39, 43–51 (xem `analysis.md` §13).

## 5. Giả định đang dùng

| ID | Nội dung | Trạng thái |
|---|---|---|
| AS-01 | Đơn 0đ là transaction | Chưa xác nhận |
| AS-02 | Ngày bấm được khi kỳ 2–62 ngày | Chưa xác nhận |
| AS-03 | Chưa kết thúc chỉ khi kỳ lọc chạm hôm nay | Chưa xác nhận |
| AS-04 | Mặc định Sau thuế | Chưa xác nhận |
| AS-05 | Mặc định Tháng này; Tuần này = Thứ Hai → hôm nay | Chưa xác nhận |
| AS-06 | Khách chỉ có đơn trả không vào Total Customers | Chưa xác nhận |
| AS-07 | Cảnh báo ẩn khi không có đơn liên quan | Chưa xác nhận |
| AS-08 | Nhãn chip Brand theo BR-SPM-020 | Chưa xác nhận |
| AS-09 | Ecom không tính ở Toàn Tam Sơn | Chưa xác nhận |

Danh sách case bị ảnh hưởng: `analysis.md` §14.

## 6. Review nghiệp vụ

- Đã tự review theo `rules/05` §Review: có. Đã tính lại mọi con số kỳ vọng ở bảng 17.2 (phản biện độc lập cũng tính lại, không phát hiện sai số).
- Đã đổi một case xếp hạng sang dữ liệu QA để kết quả tất định (RANK-005), làm rõ dữ liệu TC-INC-030.

## 6a. Phản biện độc lập

| Cách chạy | Subagent mới (general-purpose) chạy `tc-review`, chỉ nhận đường dẫn; đọc nguồn + mockup trước. Kết quả chi tiết: `review.md` |
|---|---|

| Phát hiện | Mức | Kết luận | Thay đổi |
|---|---|---|---|
| R-01 Position "hợp" thay vì "lớn nhất" | Critical | Đã sửa | SCOPE-006 dùng Position lồng nhau (SM ST1 + RM BR-1); CO Pending Q-36 |
| R-02 CHART-037 phụ thuộc AS-03 khi tuần chứa hôm nay | Critical | Đã sửa | Thêm điều kiện hôm nay ≥ D+9; thêm CHART-051 (ngày tương đối, AS-03) |
| R-03 T = D+3 làm sai 7 case; dòng T không reset được | Major | Đã sửa | Ràng buộc D+3 ≤ hôm nay − 1; tách SETUP-12 có cách reset |
| R-04 Đối soát dữ liệu thật chưa gắn Q-01/Q-16 | Major | Đã sửa | Marker trên FLT-007, SCOPE-005 |
| R-05 Tab Brand theo Position hay tập chọn | Major | Đã sửa | Q-37; marker TABLE-008; thêm TABLE-017 |
| R-06 Ví dụ 02/08–14/10 tính sai; thiếu Tháng bấm được ở 32–120 ngày | Major | Đã sửa | Q-38; thêm CHART-050 |
| R-07 Ví dụ trục Y 6 khoảng chia | Major | Đã sửa | Q-39; CHART-033/034 viết theo quy tắc |
| R-08 Thiếu "không phụ thuộc PIC" | Major | Đã sửa | Tách FR-SPM-001-c1a/c1b; thêm SCOPE-020 |
| R-09 Thiếu vai trò SM 1 store | Major | Đã sửa | U-SM1 trong SETUP-01; thêm SCOPE-021 |
| R-10 KPI mức Cá nhân chưa định nghĩa | Major | Đã sửa | Q-40; CO Pending; marker SCOPE-003 |
| R-11 Thiếu BR-SPM-021 câu cuối | Major | Đã sửa | Mệnh đề FR-SPM-011-c23; thêm STORE-012 |
| R-12 Vế Sales của AC-SPM-001-04 | Major | Đã sửa | Tách c13a/c13b; thêm TABLE-016 |
| R-13 DT3-R1 gộp B2B có PIC | Major | Đã sửa | DT3-R1b; thêm INC-031 |
| R-14 Cơ sở tính Discount % | Major | Đã sửa | Q-41; CO Pending; marker INC-002…010, 025, 027 |
| R-15 Quyền xem Incentive | Major | Đã sửa | Q-42; CO Pending; hàng Incentive trong §10 |
| R-16 SETUP-02 khó tái tạo | Major | Đã sửa một phần | Hướng dẫn chọn giá; nếu không đạt thì tính lại kỳ vọng theo công thức 17.2; nêu thời gian ≥ 5 ngày. Vẫn để *Cần chuẩn bị* (tester tự làm được trên POS) |
| R-17, R-23, R-26, R-29, R-30, R-31 | Minor | Đã sửa | Q-43, Q-46, Q-47, Q-48, Q-49, Q-51 (+ CO Pending khi có mệnh đề) |
| R-18 Thiếu biên dưới kỳ | Minor | Đã sửa | Thêm SCOPE-022 |
| R-19 tax_total âm | Minor | Đã sửa | Thêm SALES-017 |
| R-20 Định dạng nhãn giá trị từ mockup | Minor | Đã sửa | CHART-026 bỏ assert định dạng; Q-44 |
| R-21 CHART-004 phụ thuộc ngày chạy | Minor | Đã sửa | CHART-051 thay thế phần AS-03 |
| R-22 Assert nút preset không xác định | Minor | Đã sửa | Bỏ assert; Q-45 |
| R-24 Mockup "93 đơn 0đ không tính" | Minor | Đã sửa | Bổ sung vào Q-01 |
| R-25 Số liệu mockup không nhất quán | Minor | Đã sửa | CHART-034, DISP-008 không còn dùng số mockup làm kỳ vọng |
| R-27 Thiếu sự kiện/kênh | Minor | Đã sửa | Cột "Đổi Store/CA" trong ma trận trạng thái; EV-22…24 |
| R-28 Thiếu cặp tương tác | Minor | Đã sửa | IX-29…33; thêm ALERT-005, TABLE-018 |
| R-32 Ngày gán kỳ Incentive | Minor | Đã sửa | Q-50; marker INC-026…029 |
| R-33 Bill PIC vắng Chopard + BOSS | Suggestion | Đã sửa | Thêm INC-032 |
| R-34 Đối chiếu dòng phụ thẻ KPI | Suggestion | Từ chối | Nội dung dòng phụ (tử/mẫu) không có trong văn bản nguồn, chỉ thấy ở mockup; DISP-010 đã kiểm dòng phụ có nguồn (giá trị cách nhìn thuế còn lại). Xem lại khi có prototype HTML |
| R-35 Chưa đăng nhập | Suggestion | Đã sửa | Thêm SCOPE-023; EV-11 có CO |

Sau khi sửa: validator 0 ERROR, 0 WARNING (chạy với `--previous testcases.v1.0.csv`, không mất ID).

## 7. Cảnh báo validator chưa sửa & giải trình

Không có.

## 8. Rủi ro & khuyến nghị

- **Mâu thuẫn nguồn ở Transactions (Q-01)** ảnh hưởng 5/8 KPI. Cần BA chốt trước sprint test; bộ dữ liệu chính đã tách đơn 0đ sang ngày D+3 để phần lớn case KPI không phụ thuộc Q-01.
- **Incentive chưa test được** (32 case Blocked): cần UI/API hiển thị Incentive (Q-09), cách cấu hình Threshold (SETUP-04) và bảng cấu hình Brand đầy đủ (Q-11).
- **FR-SPM-010/011 chưa được business chấp thuận (Q-19)**: 87 case nhóm 12–15 có thể phải sửa nếu thiết kế đổi.
- **SETUP-02 mất ≥ 5 ngày lịch** vì đơn phải hoàn tất đúng ngày; nên bắt đầu ngay, song song chạy đợt 0.
- Mockup có số liệu không nhất quán và hiển thị số không tách nghìn (Q-04) — không dùng mockup làm oracle cho số liệu.

## 9. Thay đổi so với phiên bản trước

| Loại | Test case | Lý do |
|---|---|---|
| Thêm | TC-SCOPE-020…023, TC-SALES-017, TC-ALERT-005, TC-CHART-050, 051, TC-STORE-012, TC-TABLE-016…018, TC-INC-031, 032 | Phản biện độc lập R-xx |
| Sửa | TC-SCOPE-003, 005, 006; TC-FLT-007; TC-TABLE-008; TC-CHART-026, 033, 034, 036, 037, 038; TC-DISP-008; TC-INC-002…010, 025…029 | Phản biện độc lập R-xx (marker, expected, điều kiện) |
| Obsolete | – | – |
