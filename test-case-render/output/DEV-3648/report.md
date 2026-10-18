# Báo cáo bộ test case — DEV-3648 Giỏ hàng có sản phẩm hết hàng

| Thông tin | Giá trị |
|---|---|
| Nguồn | Jira [DEV-3648](https://sts-technical.atlassian.net/browse/DEV-3648) + 2 ảnh đính kèm — xem Danh mục nguồn trong `analysis.md` |
| Ngày tạo | 2026-10-16 — **v2.1**: sinh lại theo bộ rules mới (mệnh đề nguồn, ma trận tương tác, tập phần tử, ma trận trạng thái, sự kiện × kênh, trạng thái SETUP), rồi xử lý phản biện độc lập |
| File | `testcases.csv`, `testcases.xlsx` (thêm sheet *Clauses*), `analysis.md`, `review.md` (phản biện độc lập), `_extracted/` |
| Bản trước | `testcases.v1.1.csv`, `analysis.v1.1.md`, `report.v1.1.md`, `testcases.v2.0.csv` (trước phản biện) |

## 1. Mức sẵn sàng

| Mức | Số lượng | Ghi chú |
|---|---|---|
| Ready | 21 case | Chạy và đánh giá Pass/Fail được ngay — gồm 9 case P1 |
| Needs Clarification | 21 case | Expected tạm thời — phụ thuộc Q mở / AS / IMP (chi tiết cột `Design_Status` trong Excel) |
| Blocked | 11 case | TC-CART-024, 025, 026, 027, 040, 041, 042, 046, 050, 051, 052 — nhánh revalidate khi bấm "Mua hàng" **không tải lại**; chờ SETUP-03 (7 case P1) |
| SETUP chưa sẵn sàng | 1 | **SETUP-03** — cần dev xác nhận: tồn kho đổi trong admin có hiệu lực ngay với revalidate của phiên giỏ hàng đang mở không (indexer, cache). Một câu trả lời mở khoá 11 case |
| Điều kiện Pending | 18 | Chờ Q-03, 04, 05, 06, 08, 09, 10, 13, 14, 17, 18, 21, 22, 23, 24 (§4) |
| Nguồn chưa đọc được | 1 | Testcase DEV-3363 trên SharePoint (Gift-popup / Amasty — CO-44) |

**Kết luận:** 21/53 case chạy và đánh giá được ngay; 21 case chạy được nhưng expected chờ BA trả lời (ưu tiên Q-01, Q-02, Q-20); 11 case revalidate — nhóm rủi ro cao nhất, có bug DEV-3747 — chờ dev cung cấp quy trình SETUP-03. Phần Gift-popup, Bundle, checkbox "Tất cả sản phẩm", guest, mini-cart checkout **chưa có case** (Pending).

## 2. Chỉ số bao phủ (từ validator)

| # | Chỉ số | Giá trị | Mẫu số |
|---|---|---|---|
| 1 | Req_ID có case tham chiếu | 18/18 | AC01–10, BR-01–03, IMP-01–05 |
| 2 | Mệnh đề nguồn có case · có case Ready | **67/67 · 39/67** | 67 mệnh đề tách từ AC/BR/IMP (§4a); 28 mệnh đề chỉ được phủ bởi case NC / Blocked |
| 3 | Điều kiện kiểm thử có case | 54/54 | 72 CO trừ 18 Pending |
| 4 | Theo kỹ thuật · nguồn mở rộng | BVA 5/5 · DT 12/12 · ST 15/15 · UC 10/10 · EG 9/9 · EP/CRUD/CL 1/1 · IX 16 dòng (14 CO, 2 Pending) · EV 14 dòng (7 CO, 1 N/A, 6 Pending) | CO theo kỹ thuật; dòng IX/EV có kết luận |
| 5 | Đang chờ | Pending 18 · NC 21 · Blocked 11 · Q mở 24 · AS 7 · IMP 5 · SETUP chưa rõ 1 | – |

Chỉ số 2 là chỉ số nên dùng khi báo cáo bao phủ: mẫu số tách từ nguồn, không do người thiết kế tự đặt. "67/67" nghĩa là mọi mệnh đề có ít nhất một case; **39/67** là phần có oracle đã xác nhận và chạy được ngay.

## 3. Thống kê (tham khảo, không phải chỉ tiêu)

| Chỉ số | Giá trị |
|---|---|
| Tổng số test case | 53 đang dùng + 1 Obsolete (TC-CART-003) |
| Theo Priority | P1: 21 · P2: 24 · P3: 7 · P4: 1 |
| Theo Scenario | Positive: 20 · Negative: 12 · Boundary: 8 · Edge: 13 |
| Theo Test_Type | Functional: 44 · Validation: 5 · Integration: 2 · UI: 2 |
| Ứng viên tự động hoá | 53 (Candidate) |

## 4. Câu hỏi còn mở (cần BA/PO trả lời)

| ID | Câu hỏi (rút gọn) | Mức độ | Case / điều kiện bị ảnh hưởng |
|---|---|---|---|
| Q-01 | Câu thông báo SP hết hàng | Major | TC-004, 007, 014, 024, 029, 037, 040, 049 |
| Q-02 | SP còn hàng được tick sẵn khi vào Cart? | Major | TC-001 |
| Q-20 | Tick có được giữ qua tải lại / mở lại Cart? | Major | TC-007, 043, 045, 047 |
| Q-07 | TỔNG (N SẢN PHẨM) đếm theo dòng hay qty; khi không chọn SP nào | Major | TC-033, 034, 045, 046 |
| Q-15 | "Thứ tự trước khi sắp xếp" là thứ tự nào | Major | TC-031, 047, 054 |
| Q-16 | SP không được tick đổi tồn kho có làm reload Cart? | Major | TC-042 |
| Q-12 | Vào thẳng URL Checkout | Major | TC-015, 044 |
| Q-23 | Lối vào Checkout khác nút Mua hàng (mini-cart, Mua ngay) | Major | CO-71 (P1 khi có đặc tả) |
| Q-03, Q-04, Q-06, Q-08, Q-13, Q-14 | Checkbox "Tất cả"; phát hiện realtime; có hàng trở lại; Gift/Bundle/Mini-cart; đổi qty SP bỏ tick; định nghĩa hết hàng | Major | CO-41, 60, 57, 44–46, 52, 53; TC-029, 036 |
| Q-05, 09, 10, 11, 17, 18, 19, 21, 22, 24 | qty tối thiểu; guest / tick sau Back; banner tiếng Anh; vị trí SP mới hết hàng; 2 tab; sửa qty SP OOS; UI thông báo; hàng về < qty; SP bỏ tick thiếu hàng; vòng đời thông báo "đã điều chỉnh" | Minor | CO-23, 42, 61, 43, 54, 59, 69, 70, 72; TC-032, 035, 039 |

Cần **dev / QA lead**: quy trình SETUP-03 (xem §1).

## 5. Giả định & yêu cầu ngầm định đang dùng

| ID | Nội dung | Trạng thái | Case bị ảnh hưởng |
|---|---|---|---|
| AS-01 | Thông báo OOS = "Sản phẩm hiện đang hết hàng" | Chưa xác nhận | TC-004, 007, 024, 029, 037, 040 |
| AS-02 | SP còn hàng được tick sẵn | Chưa xác nhận | TC-001 |
| AS-03 | Phát hiện khi tải lại / bấm Mua hàng | Chưa xác nhận — **không còn case dùng** ở v2.1 | – |
| AS-04 | SP có hàng trở lại → Enable, bỏ tick | Chưa xác nhận | TC-029 |
| AS-05 | TỔNG (N) đếm theo tổng qty | Chưa xác nhận | TC-033, 045, 046 |
| AS-06 | Thứ tự trước khi sắp xếp = thứ tự quan sát khi tất cả còn hàng | Chưa xác nhận | TC-031, 047 |
| AS-07 | Tick của SP còn hàng được giữ qua tải lại | Chưa xác nhận | TC-007, 043, 045, 047 |
| IMP-01…05 | Tóm tắt đơn hàng, SP còn lại sau đặt hàng, mini-cart, không lặp thông báo, double-click | Đề xuất | TC-033–038, 045, 046 |

## 6. Review nghiệp vụ

- Đã tự review theo `rules/05` §Review; tự tính lại mọi phép tính: 2 × 15.780.000 + 3.318.000 = 34.878.000 ₫; 15.780.000 + 3.318.000 = 19.098.000 ₫; 2 × 15.780.000 = 31.560.000 ₫.
- Validator bắt được 2 lỗi trong lúc sinh v2.1 (đã sửa): ghi chú cập nhật nhắc mã `SETUP-03` / `AS-03` làm case bị tính Blocked / NC sai — phát hiện nhờ kiểm tra hai chiều AS ↔ case mới thêm.

## 6a. Phản biện độc lập

| Cách chạy | Subagent mới (Claude Code `Agent`, general-purpose), chỉ nhận đường dẫn file; đọc nguồn và tự tách mệnh đề **trước** khi đọc analysis; không được đọc review / report / bản cũ |
|---|---|

Kết quả trên v2.0: **1 Critical · 9 Major · 11 Minor · 2 Suggestion**, đề xuất 7 case. Chi tiết: `review.md`.

| Phát hiện | Mức | Kết luận | Thay đổi |
|---|---|---|---|
| F-01 Tick của dòng không bị tác động được coi là giữ nguyên sau tải lại — không đánh dấu, mâu thuẫn AS-02 | Critical | Đã sửa | Q-20, AS-07; marker ở TC-007, 043, 045, 047; TC-033 tick trong Steps |
| F-02 Case chỉ cần tải lại bị gắn SETUP-03 / AS-03 → Blocked/NC thừa | Major | Đã sửa | 9 case chuyển sang SETUP-02, bỏ AS-03; Blocked 17 → 11 (gồm 3 case mới); TC-016, 017 → Ready |
| F-03 Thiếu số lượng khi mở lại Cart (EV-01) | Major | Đã sửa | CO-62, TC-CART-048 (P1, Ready) |
| F-04 ≥2 rule khác nhau khi mở / tải lại Cart | Major | Đã sửa | CO-63, TC-CART-049 |
| F-05 DT2-R1 gộp "không đổi" với "giảm nhưng đủ"; thiếu biên = qty | Major | Đã sửa | DT2 tách R1a/R1b, CO-64, TC-CART-050 |
| F-06 Bấm Mua hàng lần 2 ở nhánh thiếu số lượng | Major | Đã sửa | CO-65, TC-CART-051 |
| F-07 Revalidate × đẩy xuống cuối × tick | Major | Đã sửa | IX-13, CO-66, TC-CART-052 |
| F-08 Xoá SP được tick duy nhất → nút Disable | Major | Đã sửa | IX-14, CO-67, TC-CART-053, ô ma trận E6 |
| F-11 Lối vào Checkout từ mini-cart | Major | Đã sửa | EV-14, Q-23, CO-71 Pending |
| F-12 Case revalidate không xác minh Cart chưa tự cập nhật | Major | Đã sửa | Thêm bước xác minh vào TC-024–027, 040–042, 046; SETUP-03 có cách xác minh |
| F-09, F-10, F-14 Ô ma trận trạng thái thiếu / trỏ sai câu hỏi | Minor | Đã sửa | Q-21, Q-22, Q-24; CO-69, 70, 72; thêm trạng thái "đã điều chỉnh" |
| F-13 SP thiếu số lượng không được xuống cuối | Minor | Đã sửa | IX-15, CO-68, TC-CART-054 |
| F-15 Mệnh đề gộp nhiều khẳng định | Minor | Đã sửa | Tách AC07-c3, AC08-c3/c4/c5 thành c3a… (validator chấp nhận hậu tố chữ) |
| F-16 TC-018 không tạo trạng thái "đã điều chỉnh" | Minor | Đã sửa | Viết lại Preconditions / Steps |
| F-17 "TỔNG (N SẢN PHẨM)" trong ngoặc kép không nguyên văn | Minor | Đã sửa | Bỏ ngoặc kép ở TC-033, 034, 045, 046 |
| F-18 Thứ tự Preconditions ngược | Minor | Đã sửa | Đưa SETUP-02 lên trước "Đang ở trang Giỏ hàng" |
| F-19 SETUP-02 cho phép đổi Stock Status | Minor | Đã sửa | Chỉ đổi Quantity |
| F-20 TC-030 expected mơ hồ | Minor | Đã sửa | |
| F-21 TC-039 gọi ảnh hiện trạng là mockup | Minor | Đã sửa | Đổi Title |
| F-22 Tổng tiền khi khách tự đổi qty dòng được / không được tick | Suggestion | Hoãn | Chờ IMP-01 được xác nhận rồi thêm 2 case (mỗi mục tiêu 1 case) |
| F-23 Cách xác nhận qty; race đổi qty + bấm Mua hàng | Suggestion | Hoãn | Cần xem UI thật (Enter / rời ô / nút cập nhật); tester ghi chú khi chạy TC-018–022 |

## 7. Cảnh báo validator chưa sửa & giải trình

Không có (0 ERROR · 0 WARNING; `--previous testcases.v1.1.csv` không mất ID).

## 8. Rủi ro & khuyến nghị

- **Ưu tiên 1:** dev trả lời SETUP-03 → mở khoá 11 case revalidate (7 P1, regression DEV-3747).
- **Ưu tiên 2:** BA trả lời Q-01, Q-02, Q-20, Q-07, Q-15, Q-16 → chuyển 15+ case sang Ready.
- Tồn kho đổi giữa trang Checkout và đặt hàng (EV-12) nằm ngoài phạm vi — cần bộ test Checkout riêng.
- Gift-popup / Bundle / mini-cart checkout: chờ đặc tả (Q-08, Q-23); DEV-3363 cần được export từ SharePoint vào `input/DEV-3648/`.

## 9. Thay đổi so với phiên bản trước (v1.1 → v2.1)

| Loại | Test case | Lý do |
|---|---|---|
| Obsolete | TC-CART-003 | Trùng ngữ nghĩa với TC-CART-023 (cùng dữ liệu, hành động, kết quả) — Req/CO chuyển sang 023 |
| Thêm | TC-CART-040…044 | Đề xuất review v1.1 (DT2-R4, tập phần tử, URL Checkout) |
| Thêm | TC-CART-045, 046, 047 | Ma trận tương tác mới (IX-03, IX-04, IX-09) |
| Thêm | TC-CART-048…054 | Phản biện độc lập v2.0 |
| Sửa Preconditions | Tất cả | Chỉ tham chiếu SETUP thật sự cần (SETUP-01 / 02 / 03 / 04) |
| Sửa marker | TC-007, 031, 035, 039, 043, 045, 047 | Phụ thuộc ẩn: thứ tự (Q-15/AS-06), tick sau tải lại (Q-20/AS-07), UI thông báo (Q-19), tick sau đặt hàng (Q-09) |
| Sửa nội dung | TC-005, 008, 010–012, 015, 018, 024–028, 030, 031, 033, 034, 039–042, 046 | Theo review v1.1 và phản biện độc lập (xem §6a) |
| Sửa Priority | TC-CART-005 | P2 → P1 — chốt chặn trực tiếp rủi ro P1 |
| Sửa Test_Type | TC-CART-015 | Security → Functional |
