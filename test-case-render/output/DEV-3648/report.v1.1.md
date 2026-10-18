# Báo cáo bộ test case — DEV-3648 Giỏ hàng có sản phẩm hết hàng

| Thông tin | Giá trị |
|---|---|
| Nguồn | Jira [DEV-3648](https://sts-technical.atlassian.net/browse/DEV-3648) — xem Danh mục nguồn trong `analysis.md` |
| Ngày tạo | 2026-10-16 (v1.1 — áp dụng bộ rules đã sửa theo `output/RULES-REVIEW/review.md`; một phần phát hiện của `review.md` cùng thư mục) |
| File | `testcases.csv`, `testcases.xlsx`, `analysis.md`, `_extracted/jira-DEV-3648.md` |

## 1. Mức sẵn sàng

| Mức | Số lượng | Ghi chú |
|---|---|---|
| Ready | 22 case | Expected dựa trên AC01–AC10 / BR-01–03, không phụ thuộc câu hỏi mở |
| Needs Clarification | 17 case | TC-CART-001, 004, 007, 008, 014, 015, 016, 017, 024, 029, 032 (chờ Q/AS); 033–038 (dựa trên IMP-01…05 *Đề xuất*) |
| Điều kiện Pending | 7 | CO-23 (Q-05), CO-41 (Q-03), CO-42 (Q-09), CO-43 (Q-10), CO-44, CO-45, CO-46 (Q-08) |
| Nguồn chưa đọc được | 2 | Ảnh `image-20260923-104852.png` (ảnh hưởng UI, AC02/AC10, TC-CART-039); testcase DEV-3363 (Gift-popup, CO-44) |

**Kết luận:** chạy được toàn bộ 39 case. 22 case đánh giá Pass/Fail được ngay. 17 case có expected **tạm thời**: kết quả Fail ở các case này có thể do giả định sai chứ không phải lỗi sản phẩm, nên cần BA/PO trả lời Q-01, Q-02, Q-04, Q-06, Q-07 và xác nhận IMP-01…05. Phần Gift-popup, Bundle, checkbox "Tất cả sản phẩm" và guest **chưa có case**.

## 2. Chỉ số bao phủ (từ validator)

| # | Chỉ số | Giá trị | Mẫu số |
|---|---|---|---|
| 1 | Req_ID có case tham chiếu | 18/18 | AC01–AC10, BR-01–03, IMP-01–05 |
| 2 | Điều kiện kiểm thử có case | 39/39 | CO-01…46 trừ 7 Pending |
| 3 | Bao phủ theo kỹ thuật | ST 10/10 · UC 9/9 · DT 7/7 · EG 6/6 · BVA 4/4 · EP 1/1 · CRUD 1/1 · CL 1/1 | CO theo kỹ thuật (DT1 R1–R4, DT2 R1–R3; biên qty 4/5/6; 6 chuyển trạng thái + 1 chuyển đổi không hợp lệ) |
| 4 | Đang chờ | Pending 7 · Needs Clarification 17 · Q mở 12 · AS chưa xác nhận 5 · IMP chưa xác nhận 5 | – |

Chỉ số 1 chỉ cho biết mỗi yêu cầu có ít nhất một case. Mức bao phủ thực tế được đo bằng chỉ số 2–3 trên 46 điều kiện đã lập, và **không tính** 7 điều kiện Pending.

## 3. Thống kê (tham khảo, không phải chỉ tiêu)

| Chỉ số | Giá trị |
|---|---|
| Tổng số test case | 39 |
| Theo Priority | P1: 15 · P2: 17 · P3: 6 · P4: 1 |
| Theo Scenario | Positive: 18 · Negative: 9 · Boundary: 6 · Edge: 6 |
| Theo Test_Type | Functional: 29 · Validation: 5 · Integration: 2 · UI: 2 · Security: 1 |
| Ứng viên tự động hoá | 37 (Candidate) |

## 4. Câu hỏi còn mở (cần BA/PO trả lời)

| ID | Câu hỏi | Mức độ | Case / điều kiện bị ảnh hưởng |
|---|---|---|---|
| Q-01 | Thông báo SP hết hàng: "Sản phẩm hiện đang hết hàng" hay "Số lượng sản phẩm không có sẵn."? | Major | TC-CART-004, 007, 008, 014, 024, 029, 037 |
| Q-02 | SP còn hàng có được tick sẵn khi vào Cart? | Major | TC-CART-001 |
| Q-03 | Hành vi checkbox "Tất cả sản phẩm" (có trong mockup, không có trong AC) | Major | TC-CART-014, CO-41 |
| Q-04 | Tồn kho thay đổi được phát hiện realtime hay chỉ khi reload / bấm Mua hàng? | Major | TC-CART-007, 016, 017 |
| Q-06 | SP có hàng trở lại: tự tick lại không, quay về vị trí nào? | Major | TC-CART-029 |
| Q-07 | "TỔNG (N SẢN PHẨM)" đếm theo dòng hay qty, có tính quà tặng không, hiển thị gì khi không chọn SP nào? | Major | TC-CART-033, 034 |
| Q-08 | Đặc tả Gift-popup/Amasty, Bundle/Set, Mini-cart | Major | TC-CART-036, CO-44, 45, 46 |
| Q-05, Q-09, Q-10, Q-11, Q-12 | qty tối thiểu; guest; banner (vị trí / tiếng Anh); thứ tự SP mới hết hàng; vào thẳng URL Checkout | Minor | CO-23, CO-42, TC-CART-024, 032, 015 |

## 5. Giả định & yêu cầu ngầm định đang dùng

| ID | Nội dung | Trạng thái | Case bị ảnh hưởng |
|---|---|---|---|
| AS-01 | Thông báo OOS = "Sản phẩm hiện đang hết hàng" | Chưa xác nhận | TC-CART-004, 007, 008, 024, 029, 037 |
| AS-02 | SP còn hàng được tick sẵn | Chưa xác nhận | TC-CART-001 |
| AS-03 | Thay đổi tồn kho thấy được sau F5 hoặc khi bấm Mua hàng | Chưa xác nhận | TC-CART-007, 016, 017 |
| AS-04 | SP có hàng trở lại → checkbox Enable, bỏ tick | Chưa xác nhận | TC-CART-029 |
| AS-05 | TỔNG (N) đếm theo tổng qty | Chưa xác nhận | TC-CART-033 |
| IMP-01…05 | Tóm tắt đơn hàng, SP còn lại sau đặt hàng, mini-cart, không lặp thông báo, double-click | Đề xuất | TC-CART-033 … 038 |

## 6. Review nghiệp vụ

- Đã tự review theo `rules/05` §Review.
- Đã tự tính lại phép tính trong TC-CART-033: 2 × 15.780.000 + 3.318.000 = 34.878.000 ₫; sau khi bỏ tick SP-C: 31.560.000 ₫.
- Thay đổi ở v1.1 so với v1.0:
  - **Priority:** TC-CART-017 và TC-CART-027 được đưa lại lên P1. Ở v1.0 hai case này bị hạ xuống P2 để qua ngưỡng tỷ lệ P1 của validator. Theo đánh giá rủi ro, lỗi ở đây chặn khách checkout, nên giữ P1.
  - **Scenario:** đổi nhãn theo quy tắc `rules/03`:
    - TC-CART-018: Negative → Boundary
    - TC-CART-022: Edge/BVA → Negative/EP (999 là giá trị đại diện của phân vùng không hợp lệ, không phải giá trị biên)
    - TC-CART-036: Negative → Edge
  - **Ghi chú:** bỏ đánh dấu Q-05 ở TC-CART-022, vì case này không phụ thuộc câu hỏi đó.
- Còn mở: dữ liệu test (SETUP-01, SETUP-02) cần tester map sang SKU thật. Cách đổi tồn kho trên Magento cần dev/QA lead xác nhận.

## 7. Cảnh báo validator chưa sửa & giải trình

Không có (0 ERROR · 0 WARNING; đã đối chiếu văn bản trong ngoặc kép với `_extracted/jira-DEV-3648.md`).

## 8. Rủi ro & khuyến nghị

- Bổ sung case cho CO-41…46 khi có trả lời Q-03, Q-08, Q-09, Q-10. Tester có thể tham khảo testcase DEV-3363 trên SharePoint.
- Đối chiếu ảnh `image-20260923-104852.png` với TC-CART-039 và AC10.
- Mockup đặt SP hết hàng ở đầu danh sách, mâu thuẫn AC10 → nên cập nhật mockup.

## 9. Thay đổi so với phiên bản trước

| Loại | Test case | Lý do |
|---|---|---|
| Sửa Priority P2 → P1 | TC-CART-017, 027 | Đánh giá theo rủi ro (R-06), không theo tỷ lệ |
| Sửa Scenario | TC-CART-018, 022, 036 | Quy tắc chọn nhãn mới (R-01) |
| Sửa Preconditions | Tất cả | Tham chiếu SETUP-01 / SETUP-02 (R-10) |
| Sửa Notes | TC-CART-022 | Bỏ phụ thuộc Q-05 không đúng |
| Sửa Notes | TC-CART-007, 008, 024, 029 | Thêm `[Giả định AS-01]` — các case này khẳng định câu thông báo hết hàng đang tranh luận (Q-01); bản trước báo Ready là sai |
| Sửa Preconditions/Steps | TC-CART-017, 018, 027 | Bỏ phụ thuộc "đã xảy ra revalidate / đã tự điều chỉnh" — mỗi case tự tạo trạng thái cần thiết |
| Sửa Test_Data | TC-CART-033 | SP-A qty 2 để phân biệt cách đếm theo dòng và theo tổng qty (Q-07) |
| Sửa Notes | TC-CART-034 | Không ghi là regression DEV-3746/3770 vì case không tái hiện điều kiện quà tặng / Set |
| Sửa Expected | Nhiều case | Bỏ đánh số kép kiểu `1. 2.` |
| Obsolete | – | Không có; ID giữ nguyên (đã kiểm bằng `--previous`) |
