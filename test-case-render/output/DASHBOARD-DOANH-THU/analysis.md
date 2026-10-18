# Phân tích yêu cầu — DASHBOARD-DOANH-THU (Dashboard Doanh thu & Đơn hàng)

| Thông tin | Giá trị |
|---|---|
| Người phân tích | AI agent (Claude) |
| Ngày | 2026-10-18 |
| Phiên bản phân tích | v1.1 — v1.0 + xử lý phản biện độc lập (`review.md`, R-01…R-35) |

## 0. Danh mục nguồn

| Nguồn | Phiên bản / ngày | Trạng thái | Bản trích xuất | Phần bị ảnh hưởng nếu chưa đọc đủ |
|---|---|---|---|---|
| `input/DASHBOARD-DOANH-THU/Tài liệu dashboard doanh thu đơn hàng.docx` — gồm PRD Dashboard, FRD Incentive, FRD Sales & Order Metrics, đặc tả JSONL migrate | Không ghi phiên bản (bản chép từ `docs/` ngày 2026-10-18) | Đã đọc | `_extracted/Tài liệu dashboard doanh thu đơn hàng.docx.md` | – |
| Ảnh nhúng image1–image3 (mockup Dashboard: toàn trang, bộ lọc + KPI + biểu đồ + bảng Theo Store, bảng Theo Brand) | – | Đã đọc (xem trực tiếp) | `_extracted/…_media/media/image1–3.png` | – |
| Ảnh image4–image10 | – | Đã đọc — chỉ là icon tiêu đề mục (emoji) | – | – |
| Prototype `business-sales-dashboard.html`, link Figma | – | Chưa đọc được (không có file / connector chưa kết nối) | – | Chi tiết tương tác UI ngoài mockup: Q-23, Q-24, Q-32 |
| Confluence PRD/FRD (link trong tài liệu), FR-CSD-002 (Total Customers), BRD Cockpit §4.2–4.3 | – | Chưa đọc được (Atlassian chưa kết nối) | – | Định nghĩa Total Customers (Q-13); Phụ lục A của FRD không có trong tài liệu → bộ dữ liệu test tự thiết kế (SETUP-02) |
| Bảng Brand Incentive Config §6.1 (SharePoint Excel) | – | Chưa đọc được | – | Tổ hợp cấu hình ngoài AC (CO Pending - Q-11) |

## 1. Tóm tắt tính năng

Dashboard Doanh thu & Đơn hàng (Phân hệ 1 MOSAIC v2 Cockpit) cho CRM Team, Retail Manager, Store Manager và Client Advisor xem 8 chỉ số hiệu suất bán hàng (Sales, Transactions, Total Customers, Coupon %, AOV, UPT, Frequency, Avg Spending/Customer) trong đúng phạm vi Position, theo kỳ lọc và cách nhìn Sau thuế/Trước thuế; kèm biểu đồ Sales theo thời gian, xếp hạng Top/Bottom 10, bảng breakdown theo Store/Brand/Client Advisor ở quy mô ~100 store. Tài liệu cũng đặc tả cách tính Incentive cho nhân viên đứng tên trên bill (Discount Threshold Gate, chia theo PIC/Other CA theo Brand) và định dạng JSONL để bên thứ ba migrate dữ liệu hoa hồng.

## 2. Phạm vi

**In-scope:** bộ lọc kỳ/store/Client Advisor/thuế; phạm vi dữ liệu theo vai trò (UI + tầng truy vấn); công thức và hiển thị 8 chỉ số; cảnh báo động; biểu đồ Sales theo thời gian; xếp hạng; bảng breakdown; Incentive (FR-INC-001…005, NFR-INC-002); quy tắc migrate có hành vi hệ thống; NFR phản hồi < 400ms, breakpoint, hover/focus.

**Out-of-scope:** core logic Segment/Loyalty/PIC (chỉ hiển thị); Sales by Staff (MTD); payroll; Store Incentive (Corporate sale Hermès); Sold Quantity/Average Price; công thức Frequency trong FRD Incentive; drill-down/export tuỳ ý; cơ chế đồng bộ ERP/HUB; quy tắc kiểm tra trước bàn giao của bên thứ ba (mục *Kiểm tra trước khi bàn giao* của định dạng migrate — trách nhiệm bên xuất dữ liệu).

**Lưu ý phạm vi:** FR-SPM-010 và FR-SPM-011 là Should-have, *đề xuất thiết kế* chờ OQ-SPM-17/18 (Q-19); mockup đã hiện thực các phần này nên case vẫn được viết theo PRD/FRD hiện tại.

## 3. Tác nhân & phân quyền

| Vai trò | Mô tả | Quyền chính (Position Rule) |
|---|---|---|
| CRM Team | Toàn Tam Sơn | Mọi đơn mọi store (trừ ecom — AS-09); có xếp hạng, bảng |
| Retail Manager | Các store của 1 Brand | Gộp/chọn trong store của Brand; không có tab Theo Brand |
| Store Manager | 1 hoặc nhiều store được gán | Gộp/chọn trong store được gán |
| Client Advisor (mức Cá nhân) | Đơn có tên mình trong list_employees[] | Trọn bill, không chia, không phụ thuộc PIC; chỉ biểu đồ thời gian, không xếp hạng, bảng thay bằng thẻ |

## 4. Danh sách yêu cầu

> PRD REQ-BSP-01…08 được hiện thực bởi: REQ-BSP-01 → FR-INC-001…005; REQ-BSP-03 → FR-SPM-003; 04 → FR-SPM-004; 05 → FR-SPM-005; 06 → FR-SPM-006; 07 → FR-SPM-007; 08 → FR-SPM-008. Truy vết theo FR để tránh trùng mẫu số.

| Req_ID | Mô tả | Nguồn | Rủi ro | Ghi chú |
|---|---|---|---|---|
| REQ-UI-01 | Bộ lọc Kỳ xem (5 preset) + Từ ngày – Đến ngày (lịch chọn khoảng, tối đa 366 ngày, báo lỗi giữ kỳ cũ) | PRD §Design — Cấu trúc màn hình, khối 1 | High |  |
| REQ-UI-02 | Bộ chuyển Giá trị tiền Sau thuế/Trước thuế; thẻ KPI tiền có nhãn thuế, số đầy đủ, dòng phụ số còn lại, icon i | PRD §Design — khối 1; Quy tắc hiển thị | High |  |
| REQ-UI-03 | Cảnh báo động: đơn trả cross-period; đơn VAT = 0 khi xem trước thuế | PRD §Design — khối 2 | Medium |  |
| REQ-UI-04 | Hai nhóm thẻ KPI: Doanh thu và giao dịch (4 thẻ), Chỉ số bình quân (4 thẻ) | PRD §Design — khối 3, 4 | Medium |  |
| REQ-UI-05 | Vai trò Cá nhân: chỉ biểu đồ thời gian, không xếp hạng; bảng thay bằng thẻ giải thích | PRD §Design — khối 5, 6 | High |  |
| REQ-UI-06 | Hover state, focus ring, tooltip hiện cả khi focus bàn phím | PRD §Design — Quy tắc hiển thị (Hover/focus/keyboard) | Low |  |
| REQ-UI-07 | Breakpoint ≥1280px; 768–1279px thu sidebar về icon, KPI 2 cột, biểu đồ 1 cột | PRD §Design — Quy tắc hiển thị | Low |  |
| NFR-SPM-006 | Chọn store, tìm kiếm, sắp xếp, phân trang, đổi thuế phản hồi dưới 400ms | PRD §Design — Quy tắc hiển thị | Medium |  |
| FR-SPM-001 | Phạm vi dữ liệu theo Position Rule, kỳ lọc, tập đơn sale_in_scope / return_in_scope (BR-SPM-001, 002) | FRD Sales Metrics §3 FR-SPM-001 | High |  |
| FR-SPM-002 | Sales sau thuế / trước thuế (BR-SPM-003, 004, 014) | FRD Sales Metrics §3 FR-SPM-002 | High |  |
| FR-SPM-003 | Transactions (REQ-BSP-03; BR-SPM-005, 006) | FRD Sales Metrics §3 FR-SPM-003 | High |  |
| FR-SPM-004 | Frequency (REQ-BSP-04; BR-SPM-012) | FRD Sales Metrics §3 FR-SPM-004 | Medium |  |
| FR-SPM-005 | Coupon % (REQ-BSP-05; BR-SPM-008, 008a) | FRD Sales Metrics §3 FR-SPM-005 | Medium |  |
| FR-SPM-006 | AOV sau thuế / trước thuế (REQ-BSP-06; BR-SPM-009, 010) | FRD Sales Metrics §3 FR-SPM-006 | High |  |
| FR-SPM-007 | UPT (REQ-BSP-07; BR-SPM-011) | FRD Sales Metrics §3 FR-SPM-007 | Medium |  |
| FR-SPM-008 | Avg Spending/Customer sau thuế / trước thuế (REQ-BSP-08; BR-SPM-013) | FRD Sales Metrics §3 FR-SPM-008 | Medium |  |
| FR-SPM-009 | Quy tắc hiển thị chung: chia 0, định dạng số, nhãn giải thích, snapshot thuế | FRD Sales Metrics §3 FR-SPM-009; PRD §Design Quy tắc hiển thị | Medium |  |
| FR-SPM-010 | Biểu đồ Sales theo thời gian Ngày/Tuần/Tháng (BR-SPM-015…019) + Logic hiển thị PRD | FRD Sales Metrics FR-SPM-010; PRD §Logic hiển thị — Biểu đồ | Medium | Should-have, chờ OQ-SPM-17 (Q-19) |
| FR-SPM-011 | Hiển thị quy mô ~100 store: bộ chọn store, lọc Client Advisor, xếp hạng Top/Bottom, bảng breakdown (BR-SPM-020…023) | FRD Sales Metrics FR-SPM-011; PRD §Design khối 1, 5, 6 | Medium | Should-have, chờ OQ-SPM-18 (Q-19) |
| FR-INC-001 | Xác định sản phẩm & Brand từng dòng trên bill | FRD Incentive §3 FR-INC-001 | High |  |
| FR-INC-002 | Discount Threshold Gate theo từng dòng (BR-INC-001) | FRD Incentive §3 FR-INC-002 | High |  |
| FR-INC-003 | Khách có PIC hay không; B2B; chia đều khi không có PIC (BR-INC-002) | FRD Incentive §3 FR-INC-003 | High |  |
| FR-INC-004 | Tỷ lệ chia theo Brand Config: PIC / Other CA (BR-INC-003, 004) | FRD Incentive §3 FR-INC-004 | High |  |
| FR-INC-005 | Tổng hợp Incentive theo nhân viên theo kỳ (BR-INC-005) | FRD Incentive §3 FR-INC-005 | High |  |
| NFR-INC-001 | Điều chỉnh Incentive khi bill bị huỷ/hoàn trả | FRD Incentive §4 | High | N/A - cơ chế chưa chốt trong FRD (OQ-INC-004); điều kiện Pending - Q-20 |
| NFR-INC-002 | Incentive truy vết được về đúng bill/dòng gốc từ HUB | FRD Incentive §4 | Medium |  |
| REQ-MIG-01 | Định dạng JSONL migrate dữ liệu hoa hồng: bỏ qua đơn trả, bung salerep_ids, giá trị theo dòng đơn | Mục Quy tắc xuất dữ liệu / Field bắt buộc (cuối tài liệu) | Medium |  |

## 4a. Mệnh đề nguồn

| Clause_ID | Req_ID | Mệnh đề (bám sát nguyên văn) | CO | Ghi chú |
|---|---|---|---|---|
| REQ-UI-01-c1 | REQ-UI-01 | Kỳ xem có 5 preset: Hôm nay / Tuần này / Tháng này / Tháng trước / Năm này | CO-01; CO-02; CO-03; CO-04; CO-05; CO-06 |  |
| REQ-UI-01-c2 | REQ-UI-01 | Từ ngày – Đến ngày: lịch chọn khoảng | CO-07 |  |
| REQ-UI-01-c3 | REQ-UI-01 | Khoảng chọn tối đa 366 ngày | CO-08; CO-09 |  |
| REQ-UI-01-c4 | REQ-UI-01 | Vượt giới hạn: báo lỗi, giữ kỳ cũ | CO-09 |  |
| REQ-UI-01-c5 | REQ-UI-01 | Kỳ mặc định khi mở dashboard (mockup: Tháng này) | CO-10 |  |
| REQ-UI-01-c6 | REQ-UI-01 | Từ ngày lớn hơn Đến ngày / ngày tương lai |  | Pending - Q-08 |
| REQ-UI-02-c1 | REQ-UI-02 | Bộ chuyển Giá trị tiền: Sau thuế / Trước thuế (góc phải bộ lọc) | CO-01; CO-11 |  |
| REQ-UI-02-c2 | REQ-UI-02 | Mỗi thẻ KPI tiền (Sales, AOV, Avg Spending/Customer) có nhãn Sau thuế / Trước thuế theo bộ chuyển | CO-85 |  |
| REQ-UI-02-c3 | REQ-UI-02 | Số chính hiển thị đầy đủ (tách nghìn bằng khoảng trắng, không viết tắt) | CO-86 |  |
| REQ-UI-02-c4 | REQ-UI-02 | Kèm dòng phụ ghi số còn lại (cách nhìn thuế kia) | CO-87 |  |
| REQ-UI-02-c5 | REQ-UI-02 | Thẻ đếm/tỷ lệ (Transactions, UPT, Coupon %, Frequency) không đổi khi chuyển thuế | CO-88 |  |
| REQ-UI-02-c6 | REQ-UI-02 | Mỗi thẻ có icon i giải thích công thức | CO-89 |  |
| REQ-UI-03-c1 | REQ-UI-03 | Cảnh báo: đơn trả của đơn bán kỳ trước đã trừ vào kỳ này (Cross-period) | CO-92; CO-93 |  |
| REQ-UI-03-c3 | REQ-UI-03 | Số đơn trong cảnh báo theo phạm vi store đang chọn | CO-237 |  |
| REQ-UI-03-c2 | REQ-UI-03 | Cảnh báo: đơn VAT = 0 khi xem trước thuế | CO-94; CO-95 |  |
| REQ-UI-04-c1 | REQ-UI-04 | KPI Doanh thu và giao dịch: 4 thẻ Sales, Transactions, Total Customers, Coupon % | CO-91 |  |
| REQ-UI-04-c2 | REQ-UI-04 | KPI Chỉ số bình quân: 4 thẻ AOV, UPT, Frequency, Avg Spending/Customer | CO-91 |  |
| REQ-UI-05-c1 | REQ-UI-05 | Vai trò Cá nhân chỉ có biểu đồ thời gian, không có xếp hạng | CO-29 |  |
| REQ-UI-05-c2 | REQ-UI-05 | Vai trò Cá nhân thay bảng bằng thẻ giải thích tính trọn bill mình đứng tên | CO-29 |  |
| REQ-UI-06-c1 | REQ-UI-06 | Mọi phần tử bấm được có hover state | CO-226 |  |
| REQ-UI-06-c2 | REQ-UI-06 | Focus ring rõ khi điều hướng bàn phím | CO-227 |  |
| REQ-UI-06-c3 | REQ-UI-06 | Tooltip hiện cả khi focus bàn phím | CO-228 |  |
| REQ-UI-07-c1 | REQ-UI-07 | Breakpoint ≥1280px | CO-223 |  |
| REQ-UI-07-c2 | REQ-UI-07 | 768–1279px: sidebar thu về icon, KPI 2 cột, biểu đồ xếp 1 cột | CO-224 |  |
| NFR-SPM-006-c1 | NFR-SPM-006 | Đổi thuế phản hồi dưới 400ms | CO-220 |  |
| NFR-SPM-006-c2 | NFR-SPM-006 | Chọn store phản hồi dưới 400ms | CO-221 |  |
| NFR-SPM-006-c3 | NFR-SPM-006 | Tìm kiếm, sắp xếp, phân trang phản hồi dưới 400ms | CO-222 |  |
| FR-SPM-001-c1a | FR-SPM-001 | Mức Cá nhân: đơn có tên người xem trong list_employees[]; không thấy số cấp store hay của người khác (AC-SPM-001-03) | CO-15 |  |
| FR-SPM-001-c1b | FR-SPM-001 | Mức Cá nhân không giới hạn / không phụ thuộc PIC | CO-230 |  |
| FR-SPM-001-c1c | FR-SPM-001 | Các thẻ KPI khác (Total Customers, Frequency, Coupon %, AOV, Avg Spending) và bộ lọc ở mức Cá nhân |  | Pending - Q-40 |
| FR-SPM-001-c15 | FR-SPM-001 | Mức 1 store (Store Manager 1 store): mọi đơn tại store | CO-231 |  |
| FR-SPM-001-c16 | FR-SPM-001 | Nhiều Position có phạm vi rời nhau |  | Pending - Q-36 |
| FR-SPM-001-c2 | FR-SPM-001 | Store Manager nhiều store: chỉ gồm đơn các store được cấp (AC-SPM-001-01) | CO-13 |  |
| FR-SPM-001-c3 | FR-SPM-001 | Chọn riêng 1 store: mọi chỉ số chỉ tính trên store đó (AC-SPM-001-02) | CO-14 |  |
| FR-SPM-001-c4 | FR-SPM-001 | Toàn Tam Sơn (CRM Team): mọi đơn của mọi store | CO-17 |  |
| FR-SPM-001-c5 | FR-SPM-001 | Lấy phạm vi lớn nhất Position được cấp; người xem chỉ thu hẹp, không mở rộng | CO-18; CO-148 |  |
| FR-SPM-001-c6 | FR-SPM-001 | Đơn VO (đã huỷ) không vào sale_in_scope (AC-SPM-001-07) | CO-19 |  |
| FR-SPM-001-c7 | FR-SPM-001 | Đơn nháp / đang xử lý không vào sale_in_scope (AC-SPM-001-07) | CO-20 |  |
| FR-SPM-001-c8 | FR-SPM-001 | return_in_scope theo ngày hoàn tất đơn trả, không xét ngày đơn bán gốc | CO-34 |  |
| FR-SPM-001-c9 | FR-SPM-001 | Đơn từ warehouse ecom 1000332, 1000333 không vào phạm vi store nào (AC-SPM-001-06) | CO-21 |  |
| FR-SPM-001-c10 | FR-SPM-001 | Ecom ở mức Toàn Tam Sơn: mặc định không tính (OQ-SPM-06) | CO-22 |  |
| FR-SPM-001-c11 | FR-SPM-001 | Kỳ = [00:00:00 ngày bắt đầu, 23:59:59 ngày kết thúc] UTC+7 theo ngày hoàn tất (AC-SPM-001-05) | CO-23; CO-24; CO-232 |  |
| FR-SPM-001-c17 | FR-SPM-001 | Chưa đăng nhập không truy cập được số liệu (BR-SPM-001) | CO-233 |  |
| FR-SPM-001-c12 | FR-SPM-001 | BR-SPM-001: cố truy cập store ngoài phạm vi qua filter/API bị từ chối, không trả số (AC-SPM-001-08) | CO-25; CO-26; CO-27 |  |
| FR-SPM-001-c13a | FR-SPM-001 | BR-SPM-002: bill nhiều Client Advisor — mỗi người thấy trọn bill (AC-SPM-001-04) | CO-16; CO-244 |  |
| FR-SPM-001-c13b | FR-SPM-001 | Sales A + Sales B > Sales store phần bill chung (AC-SPM-001-04) | CO-244 |  |
| FR-SPM-001-c14 | FR-SPM-001 | Đơn list_employees = [] tính ở store/Brand/Tam Sơn, không ở mức Cá nhân của ai (AC-SPM-001-09) | CO-28 |  |
| FR-SPM-002-c1 | FR-SPM-002 | Sales sau thuế = Σ total đơn bán − Σ total đơn trả (AC-SPM-002-01) | CO-32 |  |
| FR-SPM-002-c2 | FR-SPM-002 | Sales trước thuế = Σ(total − tax_total) đơn bán − Σ(total − tax_total) đơn trả (AC-SPM-002-07, 08) | CO-33 |  |
| FR-SPM-002-c3 | FR-SPM-002 | Đơn trả khác kỳ trừ vào kỳ của ngày trả; kỳ của đơn bán giữ nguyên (AC-SPM-002-02, BR-SPM-004) | CO-34 |  |
| FR-SPM-002-c4 | FR-SPM-002 | Sales có thể âm, hiển thị đúng giá trị âm, không về 0 (AC-SPM-002-03) | CO-35 |  |
| FR-SPM-002-c5 | FR-SPM-002 | Header lệch (subtotal = 0, tax_total = 0, total > 0): dùng total/tax_total ERP, ghi log cảnh báo thiếu VAT (AC-SPM-002-04) | CO-36 |  |
| FR-SPM-002-c6 | FR-SPM-002 | Đơn đã tính sau đó chuyển VO tự rời khỏi Sales (AC-SPM-002-05) | CO-37 |  |
| FR-SPM-002-c7 | FR-SPM-002 | Đơn bán đã trả toàn bộ trong kỳ đóng góp 0 ở cả hai cách nhìn (AC-SPM-002-06) | CO-38 |  |
| FR-SPM-002-c8 | FR-SPM-002 | Ví dụ thật subtotal 11 386 818, tax 1 138 682, total 12 525 500 (AC-SPM-002-09) | CO-39 |  |
| FR-SPM-002-c9 | FR-SPM-002 | Đơn có giảm giá: trước thuế = total − tax_total, không phải subtotal (AC-SPM-002-10) | CO-40 |  |
| FR-SPM-002-c10 | FR-SPM-002 | Đơn nhiều thuế suất: dùng tax_total ERP, không chia 1 thuế suất chung (AC-SPM-002-11) | CO-41 |  |
| FR-SPM-002-c11 | FR-SPM-002 | Đơn trả: trừ total ở sau thuế, trừ total − tax_total ở trước thuế (AC-SPM-002-12) | CO-42 |  |
| FR-SPM-002-c12 | FR-SPM-002 | Đơn 0đ không đóng góp vào Sales ở cả hai cách nhìn (AC-SPM-002-13, phần Sales) | CO-43 |  |
| FR-SPM-002-c13 | FR-SPM-002 | Kiểm tra chéo: lệch công thức header vượt 1đ hoặc tax_total âm/lớn hơn total → ghi log, số vẫn theo ERP | CO-44; CO-45; CO-46; CO-236 |  |
| FR-SPM-002-c14 | FR-SPM-002 | Đơn B2B có tính vào Sales (OQ-SPM-05, đề xuất: tính) | CO-47 |  |
| FR-SPM-003-c1 | FR-SPM-003 | Mỗi đơn đếm 1, không phụ thuộc số dòng, số nhân viên (AC-SPM-003-02) | CO-49 |  |
| FR-SPM-003-c2 | FR-SPM-003 | Đơn trả không làm giảm Transactions (AC-SPM-003-03, BR-SPM-005) | CO-50 |  |
| FR-SPM-003-c3 | FR-SPM-003 | Kỳ không có đơn: Transactions hiển thị 0, không phải — (AC-SPM-003-04) | CO-79 |  |
| FR-SPM-003-c4 | FR-SPM-003 | Đơn của khách lẻ đếm như mọi đơn (AC-SPM-003-05) | CO-48 |  |
| FR-SPM-003-c5 | FR-SPM-003 | Đơn 0đ là transaction (BR-SPM-006, AC-SPM-003-01, 06) — mâu thuẫn với công thức net_amount > 0 | CO-51 |  |
| FR-SPM-004-c1 | FR-SPM-004 | Frequency = Transactions ÷ Total Customers (AC-SPM-004-02) | CO-52 |  |
| FR-SPM-004-c2 | FR-SPM-004 | Tài khoản Khách lẻ chung đếm 1 ở mẫu số, góp nhiều đơn ở tử số (AC-SPM-004-03) | CO-53 |  |
| FR-SPM-004-c3 | FR-SPM-004 | Total Customers = 0 → hiển thị — (AC-SPM-004-04) | CO-79 |  |
| FR-SPM-004-c4 | FR-SPM-004 | Khách chỉ có đơn trả trong kỳ không vào Total Customers (AC-SPM-004-05) | CO-54 |  |
| FR-SPM-004-c5 | FR-SPM-004 | Mẫu số là đúng customer_in_period của FR-CSD-002 | CO-55 |  |
| FR-SPM-004-c6 | FR-SPM-004 | Khách chỉ có đơn 0đ vẫn có 1 transaction (BR-SPM-012) | CO-56 |  |
| FR-SPM-005-c1 | FR-SPM-005 | Coupon % = số transaction có coupon ÷ Transactions × 100% (AC-SPM-005-01) | CO-57 |  |
| FR-SPM-005-c2 | FR-SPM-005 | Đơn dùng nhiều coupon vẫn đếm 1 (AC-SPM-005-02) | CO-57 |  |
| FR-SPM-005-c3 | FR-SPM-005 | Đơn giảm 100% bằng coupon vào cả tử và mẫu số (AC-SPM-005-03) | CO-58 |  |
| FR-SPM-005-c4 | FR-SPM-005 | Giảm giá theo chương trình không kèm mã không tính là coupon (AC-SPM-005-04) | CO-57 |  |
| FR-SPM-005-c5 | FR-SPM-005 | Transactions = 0 → — (AC-SPM-005-05) | CO-79 |  |
| FR-SPM-005-c6 | FR-SPM-005 | Đơn có coupon bị trả toàn bộ vẫn trong tử và mẫu số (AC-SPM-005-06) | CO-59 |  |
| FR-SPM-005-c7 | FR-SPM-005 | Nguồn field nhận diện coupon (vouchers[], discount_lines[], SF_Loyalty_Discount kèm Voucher Code) |  | Pending - Q-33 |
| FR-SPM-006-c1 | FR-SPM-006 | AOV sau thuế = Sales sau thuế ÷ Transactions; gồm đơn khách lẻ (AC-SPM-006-01, 04) | CO-60 |  |
| FR-SPM-006-c2 | FR-SPM-006 | AOV trước thuế = Sales trước thuế ÷ Transactions; ≤ AOV sau thuế, cùng mẫu số (AC-SPM-006-06, 07) | CO-61 |  |
| FR-SPM-006-c3 | FR-SPM-006 | Đơn trả của đơn kỳ trước kéo AOV về 0 (AC-SPM-006-02) | CO-62 |  |
| FR-SPM-006-c4 | FR-SPM-006 | Kỳ chỉ có đơn trả: Transactions = 0 → AOV — (AC-SPM-006-03) | CO-63 |  |
| FR-SPM-006-c5 | FR-SPM-006 | AOV × Transactions = Sales ở từng cách nhìn (AC-SPM-006-05) | CO-64 |  |
| FR-SPM-006-c6 | FR-SPM-006 | AOV có thể âm khi Sales âm | CO-65 |  |
| FR-SPM-006-c7 | FR-SPM-006 | Đơn 0đ kéo AOV xuống (BR-SPM-006) | CO-66 |  |
| FR-SPM-007-c1 | FR-SPM-007 | UPT = net_qty ÷ Transactions; net_qty trừ số lượng đơn trả kể cả cross-period (AC-SPM-007-01, 03) | CO-67 |  |
| FR-SPM-007-c2 | FR-SPM-007 | Dòng dịch vụ (không barcode) không tính vào net_qty (AC-SPM-007-02, BR-SPM-011) | CO-69 |  |
| FR-SPM-007-c3 | FR-SPM-007 | Transactions = 0 → — (AC-SPM-007-04) | CO-79 |  |
| FR-SPM-007-c4 | FR-SPM-007 | Đơn 0đ góp số lượng vào tử và +1 mẫu số (AC-SPM-007-05) | CO-70 |  |
| FR-SPM-007-c5 | FR-SPM-007 | Dòng phí ship productparent_id 1051644 bị loại (AC-SPM-007-06) | CO-68 |  |
| FR-SPM-007-c6 | FR-SPM-007 | Dòng giảm giá trong discount_lines[] không cộng số lượng (AC-SPM-007-07) | CO-67 |  |
| FR-SPM-007-c7 | FR-SPM-007 | UPT có thể âm khi trả nhiều hơn bán | CO-71 |  |
| FR-SPM-008-c1 | FR-SPM-008 | Avg Spending sau thuế = Sales sau thuế ÷ Total Customers; gồm khách lẻ (AC-SPM-008-01, 02) | CO-72 |  |
| FR-SPM-008-c2 | FR-SPM-008 | Avg Spending trước thuế = Sales trước thuế ÷ Total Customers (AC-SPM-008-09) | CO-73 |  |
| FR-SPM-008-c3 | FR-SPM-008 | Mẫu số bằng đúng Total Customers ở FR-CSD-002 (AC-SPM-008-03) | CO-55 |  |
| FR-SPM-008-c4 | FR-SPM-008 | Khách trả toàn bộ trong kỳ vẫn ở mẫu số (AC-SPM-008-04) | CO-74 |  |
| FR-SPM-008-c5 | FR-SPM-008 | Khách chỉ có đơn trả không ở mẫu số nhưng khoản hoàn vẫn trừ ở tử số (AC-SPM-008-05) | CO-75 |  |
| FR-SPM-008-c6 | FR-SPM-008 | Khách chỉ có đơn 0đ ở mẫu số (AC-SPM-008-06) | CO-76 |  |
| FR-SPM-008-c7 | FR-SPM-008 | Total Customers = 0 → — (AC-SPM-008-07) | CO-79 |  |
| FR-SPM-008-c8 | FR-SPM-008 | Cấp gộp nhiều store đếm khách 1 lần (AC-SPM-008-08) | CO-77 |  |
| FR-SPM-008-c9 | FR-SPM-008 | Avg Spending = Frequency × AOV (BR-CSD-004, nguyên tắc #5) | CO-78 |  |
| FR-SPM-009-c1 | FR-SPM-009 | Mẫu số 0: Frequency, Coupon %, AOV, UPT, Avg Spending hiển thị —; Transactions, Sales hiển thị 0 (AC-SPM-009-01, 10) | CO-79 |  |
| FR-SPM-009-c2 | FR-SPM-009 | UPT, Frequency 2 chữ số thập phân (AC-SPM-009-02) | CO-80 |  |
| FR-SPM-009-c3 | FR-SPM-009 | Coupon % 1 chữ số thập phân, half-up (AC-SPM-009-03) | CO-81 |  |
| FR-SPM-009-c4 | FR-SPM-009 | Tiền 0 chữ số lẻ, tách nghìn bằng khoảng trắng (AC-SPM-009-04) | CO-82 |  |
| FR-SPM-009-c5 | FR-SPM-009 | Số âm giữ dấu −, không đổi về 0, tô màu Error (AC-SPM-009-05) | CO-35 |  |
| FR-SPM-009-c6 | FR-SPM-009 | Số dưới 1 000 không tách nhóm (AC-SPM-009-06) | CO-83 |  |
| FR-SPM-009-c7 | FR-SPM-009 | Mọi số tiền có nhãn Sau thuế / Trước thuế (AC-SPM-009-07) | CO-85 |  |
| FR-SPM-009-c8 | FR-SPM-009 | Chuyển cách nhìn thuế không đổi Transactions, Frequency, Coupon %, UPT (AC-SPM-009-08) | CO-88 |  |
| FR-SPM-009-c9 | FR-SPM-009 | Hai cách nhìn cùng snapshot, chuyển không cần tải lại dữ liệu (AC-SPM-009-09) | CO-12 |  |
| FR-SPM-009-c10 | FR-SPM-009 | Nhãn giải thích bắt buộc trên thẻ Sales, Transactions, Frequency, Avg Spending | CO-90 |  |
| FR-SPM-009-c11 | FR-SPM-009 | Bảng theo nhân viên có ghi chú tổng nhân viên có thể lớn hơn tổng store | CO-177 |  |
| FR-SPM-009-c12 | FR-SPM-009 | Bảng theo store cấp gộp ghi chú Avg Spending, Frequency không cộng dồn | CO-178 |  |
| FR-SPM-009-c13 | FR-SPM-009 | Làm tròn half-up chỉ ở bước hiển thị trên số gốc | CO-84 |  |
| FR-SPM-009-c14 | FR-SPM-009 | Số kỳ cũ có thể đổi khi đơn về chậm từ HUB | CO-31 |  |
| FR-SPM-009-c15 | FR-SPM-009 | Số kỳ cũ có thể đổi khi tài khoản khách được gộp |  | Pending - Q-51 |
| FR-SPM-009-c16 | FR-SPM-009 | Half-up với số âm có phần lẻ ,5 |  | Pending - Q-43 |
| FR-SPM-010-c1 | FR-SPM-010 | Mỗi cột = Sales ròng của bucket theo cách nhìn thuế đang chọn | CO-140 |  |
| FR-SPM-010-c2 | FR-SPM-010 | Đơn bán vào bucket theo ngày hoàn tất; đơn trả theo ngày hoàn tất đơn trả (AC-SPM-010-07) | CO-120 |  |
| FR-SPM-010-c3 | FR-SPM-010 | Tuần từ Thứ Hai đến Chủ Nhật; Tháng là tháng dương lịch | CO-98; CO-112 |  |
| FR-SPM-010-c4 | FR-SPM-010 | Σ Sales các bucket = Sales kỳ; Σ Transactions bucket = Transactions kỳ (AC-SPM-010-04) | CO-119 |  |
| FR-SPM-010-c5 | FR-SPM-010 | Tự chọn đơn vị: ≤31 ngày Ngày; 32–120 ngày Tuần; >120 ngày Tháng | CO-102; CO-103; CO-104; CO-105 |  |
| FR-SPM-010-c6 | FR-SPM-010 | Kỳ 1 ngày: không vẽ, hiện thông báo; cả 3 đơn vị khoá (AC-SPM-010-05) | CO-101 |  |
| FR-SPM-010-c7 | FR-SPM-010 | Ngày bấm được khi kỳ 2–62 ngày (FRD) / 2–31 ngày (PRD) — mâu thuẫn | CO-106; CO-107; CO-103 |  |
| FR-SPM-010-c8 | FR-SPM-010 | Tuần bấm được khi kỳ chạm 2–53 tuần lịch (đếm cả tuần chỉ chạm 1 ngày) | CO-108; CO-99; CO-109; CO-110 |  |
| FR-SPM-010-c9 | FR-SPM-010 | Tháng bấm được khi kỳ chạm 2–13 tháng lịch | CO-108; CO-111; CO-112; CO-238 |  |
| FR-SPM-010-c10 | FR-SPM-010 | Đơn vị không khả dụng bị khoá kèm tooltip Không khả dụng với kỳ đang chọn, không bị ẩn | CO-113 |  |
| FR-SPM-010-c11 | FR-SPM-010 | Đã bấm tay và còn khả dụng → giữ; nhãn Đã chọn tay; nút đang dùng luôn active | CO-114; CO-115 |  |
| FR-SPM-010-c12 | FR-SPM-010 | Đổi kỳ làm đơn vị tay hết khả dụng → quay về tự chọn (AC-SPM-010-06) | CO-116 |  |
| FR-SPM-010-c13 | FR-SPM-010 | Lựa chọn tay không được ghi nhớ khi hết khả dụng | CO-117 |  |
| FR-SPM-010-c14 | FR-SPM-010 | Đơn vị tự động không bấm được → lấy đơn vị đầu tiên bấm được (Ngày → Tuần → Tháng) |  | N/A - không có kỳ hợp lệ (≤366 ngày) nào làm đơn vị tự động bị khoá: ≤31 ngày luôn bấm được Ngày, 32–120 ngày luôn chạm ≥5 tuần, >120 ngày luôn chạm ≥4 tháng |
| FR-SPM-010-c15 | FR-SPM-010 | Cột Chưa kết thúc: chứa hôm nay (AC-SPM-010-01) | CO-96 |  |
| FR-SPM-010-c16 | FR-SPM-010 | Chưa kết thúc chỉ khi kỳ lọc kéo tới hôm nay (PRD) — FRD không nêu điều kiện này | CO-99; CO-239 |  |
| FR-SPM-010-c17 | FR-SPM-010 | Bị cắt theo kỳ lọc: bucket đầu/cuối phủ một phần tuần/tháng, cột xám | CO-98 |  |
| FR-SPM-010-c18 | FR-SPM-010 | Vừa chưa kết thúc vừa bị cắt → Chưa kết thúc (AC-SPM-010-02) | CO-100 |  |
| FR-SPM-010-c19 | FR-SPM-010 | Cột Ngày không bao giờ bị cắt; kỳ đã khép không có cột Chưa kết thúc | CO-97 |  |
| FR-SPM-010-c20 | FR-SPM-010 | Cột âm màu Error, mọc xuống dưới đường 0; trục Y mở xuống âm (AC-SPM-010-08) | CO-121 |  |
| FR-SPM-010-c21 | FR-SPM-010 | Cột cao nhất viền vàng 2px, chỉ khi giá trị > 0 | CO-122; CO-124 |  |
| FR-SPM-010-c22 | FR-SPM-010 | Nhiều cột cao nhất bằng nhau → đánh dấu cột đầu tiên | CO-123 |  |
| FR-SPM-010-c23 | FR-SPM-010 | Nhãn giá trị trên cột cao nhất chỉ khi ≤ 16 cột | CO-126; CO-127 |  |
| FR-SPM-010-c24 | FR-SPM-010 | Nền xám nhạt Thứ Bảy/Chủ Nhật chỉ ở đơn vị Ngày | CO-97; CO-98 |  |
| FR-SPM-010-c25 | FR-SPM-010 | Cột bằng 0 không vẽ thân; cột khác 0 rất nhỏ cao tối thiểu 1px | CO-124; CO-125 |  |
| FR-SPM-010-c26 | FR-SPM-010 | Ưu tiên màu nền: Chưa kết thúc > Âm > Bị cắt > Đủ kỳ | CO-128; CO-129 |  |
| FR-SPM-010-c27 | FR-SPM-010 | Viền vàng cao nhất đè viền nét đứt Chưa kết thúc | CO-130 |  |
| FR-SPM-010-c28 | FR-SPM-010 | Chú giải chỉ liệt kê trạng thái thực sự xuất hiện; Đủ kỳ và Cao nhất luôn có | CO-131; CO-132 |  |
| FR-SPM-010-c29 | FR-SPM-010 | Dòng ghi chú dưới chú giải: Sales ròng, cách nhìn thuế, quy ước tuần (chỉ Tuần), cột đỏ, trục Y rút gọn | CO-131; CO-132 |  |
| FR-SPM-010-c30 | FR-SPM-010 | Trục Y luôn có mốc 0; khoảng chia đẹp (1, 2, 2.5, 5 × 10ⁿ), khoảng 4–5 khoảng chia | CO-133; CO-134 |  |
| FR-SPM-010-c31 | FR-SPM-010 | Nhãn trục Y: ≥1 triệu N Tr, ≥1 tỷ N Tỷ (≥10 tỷ không lẻ), dưới 1 triệu số đầy đủ | CO-133; CO-134; CO-135 |  |
| FR-SPM-010-c32 | FR-SPM-010 | Nhãn trục X: Ngày dd/mm; Tuần dd/mm–dd/mm khi ≤10 cột, ≥11 cột chỉ dd/mm Thứ Hai; Tháng Tn, thêm /yy khi vắt 2 năm | CO-97; CO-136; CO-137; CO-112 |  |
| FR-SPM-010-c33 | FR-SPM-010 | Nhãn dày ẩn xen kẽ, không xoay; nhãn đầu luôn hiện; cột ẩn nhãn vẫn có tooltip; chữ trục ≥ 11px | CO-138 |  |
| FR-SPM-010-c34 | FR-SPM-010 | Biểu đồ vẽ đúng chiều rộng thật khi đổi kích thước cửa sổ | CO-139 |  |
| FR-SPM-010-c35 | FR-SPM-010 | Tooltip: khoảng thời gian (Ngày dd/mm/yyyy (Thứ)), Sales đầy đủ, Transactions, Hoàn trả đã trừ | CO-140 |  |
| FR-SPM-010-c36 | FR-SPM-010 | Tooltip Tuần/Tháng: khoảng ngày đã bị cắt theo kỳ lọc + nhãn Bị cắt theo kỳ lọc | CO-141 |  |
| FR-SPM-010-c37 | FR-SPM-010 | Tooltip cột chưa kết thúc có nhãn Chưa kết thúc (AC-SPM-010-10) | CO-142 |  |
| FR-SPM-010-c42 | FR-SPM-010 | Hoàn trả đã trừ trong tooltip theo cách nhìn thuế nào |  | Pending - Q-46 |
| FR-SPM-010-c38 | FR-SPM-010 | Tooltip bám con trỏ, tự lật sang trái khi sát mép phải | CO-143 |  |
| FR-SPM-010-c39 | FR-SPM-010 | Đổi thuế: giá trị cột và trục Y tính lại; đơn vị và trạng thái cột giữ nguyên; nhãn panel ghi cách nhìn thuế (AC-SPM-010-09) | CO-118 |  |
| FR-SPM-010-c40 | FR-SPM-010 | Phạm vi vai trò/Store/Client Advisor áp dụng cho biểu đồ như thẻ KPI | CO-144 |  |
| FR-SPM-010-c41 | FR-SPM-010 | Trạng thái cột phân biệt bằng hình thức, không chỉ bằng màu | CO-229 |  |
| FR-SPM-011-c1 | FR-SPM-011 | Bộ chọn store tìm kiếm theo tên store hoặc Brand (AC-SPM-011-03) | CO-150 |  |
| FR-SPM-011-c2 | FR-SPM-011 | Chip chọn nhanh theo Brand kèm số store (AC-SPM-011-02) | CO-149 |  |
| FR-SPM-011-c3 | FR-SPM-011 | Nút chọn tất cả, bộ đếm đã chọn / tổng | CO-154 |  |
| FR-SPM-011-c4 | FR-SPM-011 | Mặc định chọn toàn bộ phạm vi Position; chỉ thu hẹp | CO-147; CO-148 |  |
| FR-SPM-011-c5 | FR-SPM-011 | Luôn giữ ít nhất 1 store (AC-SPM-011-04) | CO-151 |  |
| FR-SPM-011-c6 | FR-SPM-011 | Nhãn nút: Toàn Tam Sơn · N store / Brand X · N store / tên store / N store đã chọn | CO-147; CO-149; CO-152; CO-153 |  |
| FR-SPM-011-c7 | FR-SPM-011 | Mọi chỉ số, biểu đồ, bảng tính lại trên tập store đã chọn | CO-155 |  |
| FR-SPM-011-c8 | FR-SPM-011 | Lọc Client Advisor chỉ khả dụng khi ≤ 5 store; ngoài ngưỡng khoá kèm gợi ý (AC-SPM-011-05, 06) | CO-156; CO-157; CO-147 |  |
| FR-SPM-011-c9 | FR-SPM-011 | Bộ lọc Client Advisor liệt kê CA của các store đã chọn kèm tên store (AC-SPM-011-06) | CO-157 |  |
| FR-SPM-011-c10 | FR-SPM-011 | Chọn Client Advisor: số liệu chỉ gồm bill người đó đứng tên | CO-158 |  |
| FR-SPM-011-c11 | FR-SPM-011 | Xếp hạng Top 10 / Bottom 10 store theo Sales cách nhìn thuế đang chọn, hạng thực, tên store + Brand (AC-SPM-011-07) | CO-160; CO-161; CO-162 |  |
| FR-SPM-011-c12 | FR-SPM-011 | Chỉ store có phát sinh trong kỳ (≥1 đơn bán hoặc đơn trả) được xếp hạng | CO-163; CO-164 |  |
| FR-SPM-011-c13 | FR-SPM-011 | Phạm vi còn 1 store → xếp hạng Client Advisor của store đó | CO-165 |  |
| FR-SPM-011-c14 | FR-SPM-011 | Bảng 3 tab; tab Store chỉ khi > 1 store; tab Brand chỉ khi > 1 Brand (AC-SPM-011-11) | CO-174; CO-175; CO-176 |  |
| FR-SPM-011-c15 | FR-SPM-011 | Phân trang 15/30/50 (mặc định 15), hiển thị từ–đến / tổng (AC-SPM-011-01) | CO-167; CO-168; CO-169 |  |
| FR-SPM-011-c16 | FR-SPM-011 | Tìm kiếm theo tên, Brand hoặc store; sắp xếp theo mọi cột | CO-180; CO-173 |  |
| FR-SPM-011-c17 | FR-SPM-011 | Cột # là hạng thực trên toàn phạm vi, không đổi theo tìm kiếm/trang (AC-SPM-011-08) | CO-170; CO-173 |  |
| FR-SPM-011-c18 | FR-SPM-011 | Cột Sales có thanh dữ liệu nền so với dòng lớn nhất | CO-181 |  |
| FR-SPM-011-c19 | FR-SPM-011 | Dòng Tổng luôn tính trên toàn phạm vi, không phụ thuộc tìm kiếm hay trang (AC-SPM-011-09) | CO-171 |  |
| FR-SPM-011-c20 | FR-SPM-011 | Σ Sales, Σ Transactions các dòng Store = dòng Tổng; Total Customers, Frequency, Avg không cộng dồn (AC-SPM-011-10) | CO-172 |  |
| FR-SPM-011-c21 | FR-SPM-011 | Tab Client Advisor: tổng Sales các dòng có thể > dòng Tổng, có ghi chú vàng | CO-177 |  |
| FR-SPM-011-c22 | FR-SPM-011 | Store/Client Advisor không phát sinh trong kỳ không có dòng; có ghi chú ở bảng | CO-179 |  |
| FR-SPM-011-c23 | FR-SPM-011 | Lọc CA bị khoá vẫn duyệt được Client Advisor qua tab Theo Client Advisor (BR-SPM-021) | CO-243 |  |
| FR-SPM-011-c24 | FR-SPM-011 | Tab Brand theo tập store đang chọn (chip 1 Brand) | CO-245 |  |
| FR-SPM-011-c25 | FR-SPM-011 | Đổi thuế khi bảng đang sắp theo Sales: thứ tự và cột # theo Sales mới | CO-246 |  |
| FR-INC-001-c1 | FR-INC-001 | Mỗi dòng giữ brand_id riêng, xét Threshold Gate độc lập theo Brand của dòng (AC-INC-001-01) | CO-183 |  |
| FR-INC-002-c1 | FR-INC-002 | Discount % < Threshold → dòng đủ điều kiện (AC-INC-002-01) | CO-184 |  |
| FR-INC-002-c2 | FR-INC-002 | Discount % ≥ Threshold → dòng không tính Incentive (AC-INC-002-02) | CO-185; CO-187 |  |
| FR-INC-002-c3 | FR-INC-002 | Biên Threshold cấu hình (ví dụ 30%): ngay dưới ngưỡng đủ điều kiện, bằng ngưỡng bị loại | CO-186; CO-187 |  |
| FR-INC-002-c4 | FR-INC-002 | Hai dòng cùng Brand xét độc lập (AC-INC-002-03) | CO-188 |  |
| FR-INC-002-c5 | FR-INC-002 | Hai dòng khác Brand: dòng A vẫn tính dù dòng B bị loại (AC-INC-002-04) | CO-189 |  |
| FR-INC-002-c6 | FR-INC-002 | BR-INC-001: Threshold mặc định 100%, cấu hình độc lập từng Brand, đổi 1 Brand không ảnh hưởng Brand khác | CO-190 |  |
| FR-INC-002-c7 | FR-INC-002 | Toàn bộ dòng của bill bị loại → bill không tính Incentive cho ai | CO-191 |  |
| FR-INC-003-c1 | FR-INC-003 | B2C không PIC: chia đều tổng dòng đủ điều kiện cho mọi nhân viên đứng tên (AC-INC-003-01, BR-INC-002) | CO-192; CO-193 |  |
| FR-INC-003-c2 | FR-INC-003 | B2B: CA Incentive = N/A, không cộng vào ai, mọi Brand (AC-INC-003-02) | CO-194 |  |
| FR-INC-003-c3 | FR-INC-003 | Khách có PIC → chuyển FR-INC-004 (AC-INC-003-03) | CO-197 |  |
| FR-INC-003-c4 | FR-INC-003 | PIC xác định tại thời điểm bill phát sinh (snapshot), không phải PIC hiện tại | CO-195 |  |
| FR-INC-003-c5 | FR-INC-003 | PIC xác định tại Store phát sinh bill | CO-196 |  |
| FR-INC-003-c6 | FR-INC-003 | Bill không có nhân viên đứng tên (list_employees = []) |  | Pending - Q-30 |
| FR-INC-003-c7 | FR-INC-003 | B2B có PIC trên bill vẫn N/A (áp dụng mọi Brand) | CO-247 |  |
| FR-INC-002-c8 | FR-INC-002 | Cơ sở thuế của Gross/Net; Gross = 0; Discount âm |  | Pending - Q-41 |
| FR-INC-004-c1 | FR-INC-004 | Hanoia, PIC trên bill, có Other CA → PIC 70%, Other CA 30% (AC-INC-004-01) | CO-197 |  |
| FR-INC-004-c2 | FR-INC-004 | Hanoia, PIC không trên bill, có Other CA → PIC 0%, Other CA 100% (AC-INC-004-02) | CO-198 |  |
| FR-INC-004-c3 | FR-INC-004 | Kenzo/Marc Jacobs/Rimowa/Bang & Olufsen/Devialet/Tâm Sơn Living/Patek Philippe, PIC trên bill + Other CA → 100/0 (AC-INC-004-03) | CO-199 |  |
| FR-INC-004-c4 | FR-INC-004 | Chopard/Chaumet/Piaget/JLC/Buccellati, PIC không trên bill + Other CA → 70/30 (AC-INC-004-04) | CO-200 |  |
| FR-INC-004-c5 | FR-INC-004 | Loewe/BV/TB/Sandro/Maje/MK/Longchamp, PIC trên bill + Other CA → 50/50 (AC-INC-004-05) | CO-201 |  |
| FR-INC-004-c6 | FR-INC-004 | BOSS/BOSS Green/HUGO/FL/ADLV, PIC không trên bill + Other CA → 0/100 (AC-INC-004-06) | CO-202 |  |
| FR-INC-004-c7 | FR-INC-004 | Hermès, PIC trên bill, không Other CA → PIC 100% (AC-INC-004-07) | CO-203 |  |
| FR-INC-004-c8 | FR-INC-004 | Hermès, PIC + 2 Other CA → 50% / 25% / 25% (AC-INC-004-08, BR-INC-004) | CO-204 |  |
| FR-INC-004-c9 | FR-INC-004 | Hanoia, PIC + 3 Other CA → 70% / 10% / 10% / 10% (AC-INC-004-11) | CO-205 |  |
| FR-INC-004-c10 | FR-INC-004 | BR-INC-003: Brand chưa có dòng cấu hình tường minh, PIC đơn độc → 100% (AC-INC-004-09) | CO-206 |  |
| FR-INC-004-c11 | FR-INC-004 | Dòng bị loại ở FR-INC-002 không tra Brand Config, không ảnh hưởng dòng khác (AC-INC-004-10) | CO-207 |  |
| FR-INC-004-c12 | FR-INC-004 | PIC không trên bill và không có Other CA |  | Pending - Q-30 |
| FR-INC-004-c14 | FR-INC-004 | Bill nhiều dòng khác nhóm Brand khi PIC vắng: tra cấu hình theo từng dòng | CO-248 |  |
| FR-INC-004-c13 | FR-INC-004 | Các tổ hợp Brand × PIC trên bill × Other CA khác (bảng cấu hình §6.1 trên SharePoint) |  | Pending - Q-11 |
| FR-INC-005-c1 | FR-INC-005 | Cộng dồn Incentive của từng nhân viên theo kỳ từ nhiều bill (AC-INC-005-01) | CO-208 |  |
| FR-INC-005-c2 | FR-INC-005 | Dòng bị loại không xuất hiện trong tổng của ai; dòng khác vẫn tính (AC-INC-005-02) | CO-209 |  |
| FR-INC-005-c3 | FR-INC-005 | BR-INC-005: bill Corporate Sale / B2B không đóng góp vào tổng | CO-194 |  |
| FR-INC-005-c4 | FR-INC-005 | Dùng chung bộ lọc thời gian của Cockpit | CO-210 |  |
| FR-INC-005-c5 | FR-INC-005 | Tổng Incentive/nhân viên/kỳ có thể drill-down theo Brand | CO-211 |  |
| FR-INC-005-c6 | FR-INC-005 | Vai trò nào được xem Incentive của ai; chặn qua API |  | Pending - Q-42 |
| NFR-INC-001-c1 | NFR-INC-001 | Bill đã tính Incentive bị huỷ/hoàn trả → Incentive điều chỉnh tương ứng |  | Pending - Q-20 |
| NFR-INC-002-c1 | NFR-INC-002 | Mọi Incentive hiển thị truy vết được về đúng 1 bill/dòng sản phẩm gốc | CO-212 |  |
| REQ-MIG-01-c1 | REQ-MIG-01 | Record có m_rma_id khác null bị bỏ qua (đơn trả hàng) | CO-216 |  |
| REQ-MIG-01-c2 | REQ-MIG-01 | Mỗi phần tử salerep_ids bung thành một bản ghi hoa hồng nhân viên | CO-217 |  |
| REQ-MIG-01-c3 | REQ-MIG-01 | Giá tiền là giá trị của dòng đơn, không phải tổng đơn | CO-218 |  |
| REQ-MIG-01-c4 | REQ-MIG-01 | Record vi phạm quy tắc (salerep_ids rỗng, thiếu cả 2 ID, trùng ID + role, số dạng chuỗi) |  | Pending - Q-21 |

## 5. Quy tắc nghiệp vụ

Các BR của nguồn được tách thành mệnh đề của FR chứa chúng (mục 4a), không lập Req_ID riêng để tránh đếm trùng:

- BR-SPM-001 → FR-SPM-001-c12 · BR-SPM-002 → FR-SPM-001-c13, FR-SPM-011-c21 · BR-SPM-003 → FR-SPM-002-c5, c13 · BR-SPM-004 → FR-SPM-002-c3, c4 · BR-SPM-005 → FR-SPM-003-c2 · BR-SPM-006 → FR-SPM-003-c5 (mâu thuẫn, Q-01) · BR-SPM-008/008a → FR-SPM-005-c1…c6 · BR-SPM-009 → FR-SPM-006-c5 · BR-SPM-010 → FR-SPM-006-c1 · BR-SPM-011 → FR-SPM-007-c2 · BR-SPM-012 → FR-SPM-004-c4, c6 · BR-SPM-013 → FR-SPM-008-c4…c8 · BR-SPM-014 → FR-SPM-002-c2, c9…c11, FR-SPM-009-c7…c9 · BR-SPM-015…019 → FR-SPM-010 · BR-SPM-020…023 → FR-SPM-011
- BR-INC-001 → FR-INC-002-c6 · BR-INC-002 → FR-INC-003-c1 · BR-INC-003 → FR-INC-004-c10 · BR-INC-004 → FR-INC-004-c8, c9 · BR-INC-005 → FR-INC-005-c2, c3

## 6. Yêu cầu ngầm định

Không thêm IMP: các kỳ vọng ngoài nguồn được đưa thành câu hỏi (Q) hoặc ghi N/A.

## 7. Từ điển dữ liệu

| Trường / chỉ số | Kiểu | Giới hạn / Miền giá trị | Định dạng hiển thị | Mặc định | Nguồn |
|---|---|---|---|---|---|
| Kỳ xem | Preset | Hôm nay / Tuần này / Tháng này / Tháng trước / Năm này | – | Tháng này (AS-05) | PRD khối 1 |
| Từ ngày – Đến ngày | Khoảng ngày | 1–366 ngày; UTC+7; [00:00:00, 23:59:59] | dd/mm/yyyy | – | PRD khối 1; FR-SPM-001 |
| Store | Multi-select | ≥ 1 store trong phạm vi Position | Nhãn Toàn Tam Sơn · N store / Brand X · N store / tên store / N store đã chọn | Toàn phạm vi | BR-SPM-020 |
| Client Advisor | Bộ lọc | Chỉ khả dụng khi ≤ 5 store | Kèm tên store | – | BR-SPM-021 |
| Giá trị tiền | Toggle | Sau thuế / Trước thuế | – | Sau thuế (AS-04) | PRD khối 1 |
| Transactions, Total Customers | Số đếm | ≥ 0 | 0 chữ số lẻ; 0 khi trống | – | FR-SPM-009 |
| Sales, AOV, Avg Spending | Tiền VND | Có thể âm | 0 chữ số lẻ, tách nghìn khoảng trắng, dấu −, màu Error khi âm | – | FR-SPM-009 |
| Coupon % | Tỷ lệ | 0–100% | 1 chữ số lẻ, half-up; — khi mẫu số 0 | – | FR-SPM-009 |
| UPT, Frequency | Tỷ số | UPT có thể âm | 2 chữ số lẻ, dấu chấm; — khi mẫu số 0 | – | FR-SPM-009 |
| Mỗi trang (bảng) | Chọn | 15 / 30 / 50 | – | 15 | BR-SPM-023 |
| Discount % dòng | % | (Gross − Net) ÷ Gross × 100 | – | Threshold 100% | FR-INC-002 |

### 7.1 Phân vùng tương đương & giá trị biên

| Trường | Phân vùng hợp lệ | Phân vùng không hợp lệ | Biên · đơn vị bước · mức coverage |
|---|---|---|---|
| Độ dài khoảng ngày | 1–366 ngày | ≥ 367 ngày; Từ > Đến (Q-08) | 366 / 367 · ±1 ngày · 2-value |
| Đơn vị tự chọn | ≤31 → Ngày; 32–120 → Tuần; >120 → Tháng; 1 ngày → không vẽ | – | 1 / 2 / 31 / 32 / 120 / 121 · ±1 ngày · 2-value |
| Ngày khả dụng | 2–62 ngày (AS-02) | 1; ≥ 63 | 62 / 63 · ±1 ngày |
| Tuần khả dụng | 2–53 tuần lịch chạm | 1; 54 | 1 / 2 / 53 / 54 tuần |
| Tháng khả dụng | 2–13 tháng lịch chạm | 1; 14 (không tạo được với ≤ 366 ngày) | 1 / 2 / 13 tháng |
| Nhãn tuần | ≤ 10 cột → dd/mm–dd/mm | ≥ 11 cột → dd/mm | 10 / 11 cột |
| Nhãn giá trị cột cao nhất | ≤ 16 cột | ≥ 17 cột | 16 / 17 cột |
| Số store để lọc CA | 1–5 store | ≥ 6 store | 5 / 6 · ±1 store |
| Số store đã chọn | ≥ 1 | 0 (bị chặn) | 1 / 0 |
| Discount % so Threshold 30% | < 30% đủ điều kiện | ≥ 30% bị loại | 29.99% / 30.00% · ±0.01% (Q-12) |
| Discount % so Threshold 100% | < 100% | = 100% | 20% / 100% |
| Lệch công thức header | ≤ 1đ không log | > 1đ log | 1đ / 2đ |
| Giờ hoàn tất so kỳ | 23:50:00 ngày cuối kỳ | 00:00:30 ngày sau | ±1 ngày quanh 0h UTC+7 |

## 8. Trạng thái & chuyển đổi

Trạng thái chọn đơn vị biểu đồ (PRD *Logic hiển thị* mục 3, BR-SPM-015): **Tự chọn** (nhãn Tự chọn theo độ dài kỳ), **Đã chọn tay** (nhãn Đã chọn tay), **Không vẽ** (kỳ 1 ngày). Chuyển đổi không hợp lệ chọn kiểm tra: bấm đơn vị bị khoá (phải bị chặn).

### 8.1 Ma trận trạng thái

| Trạng thái \ Sự kiện | Bấm đơn vị khả dụng khác | Bấm đơn vị đang active | Bấm đơn vị bị khoá | Đổi kỳ, đơn vị đang dùng vẫn khả dụng | Đổi kỳ, đơn vị đang dùng bị khoá | Đổi sang kỳ 1 ngày | Đổi từ kỳ 1 ngày sang ≥ 2 ngày | Đổi thuế | Đổi Store / Client Advisor (kỳ giữ nguyên) |
|---|---|---|---|---|---|---|---|---|---|
| Tự chọn | → Đã chọn tay (PRD bước 2.1) · CO-114 | Q-29 | Bị chặn (PRD bước 1) · CO-113 | → Tự chọn, tính lại theo độ dài kỳ (PRD bước 2.2) · CO-102 | → Tự chọn đơn vị mới (PRD bước 2.2) · CO-105 | → Không vẽ (PRD bước 2.4) · CO-101 | Không khả thi - đang ở kỳ ≥ 2 ngày | Không đổi (AC-SPM-010-09) · CO-118 | Không đổi (đơn vị chỉ phụ thuộc kỳ — PRD bước 1, 2) |
| Đã chọn tay | → Đã chọn tay, đơn vị mới · CO-114 | Không đổi (nút đang dùng luôn active) | Bị chặn · CO-113 | Không đổi (PRD bước 2.1) · CO-115 | → Tự chọn (AC-SPM-010-06) · CO-116 | → Không vẽ · CO-117 | Không khả thi - đang ở kỳ ≥ 2 ngày | Không đổi (AC-SPM-010-09) · CO-118 | Không đổi (đơn vị chỉ phụ thuộc kỳ) · CO-144 |
| Không vẽ (kỳ 1 ngày) | Không khả thi - cả 3 đơn vị bị khoá | Không khả thi - không có đơn vị active | Bị chặn (AC-SPM-010-05) · CO-101 | Không khả thi - không có đơn vị đang dùng | Không khả thi - không có đơn vị đang dùng | Không đổi | → Tự chọn, không nhớ lựa chọn tay cũ (PRD bước 3) · CO-117 | Không đổi (không vẽ) | Không đổi (vẫn kỳ 1 ngày) |

## 9. Bảng quyết định

**DT1 — Trạng thái cột biểu đồ (BR-SPM-017 + PRD mục 4)**

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| C1: Cột chứa hôm nay VÀ kỳ lọc kéo tới hôm nay (AS-03) | Y | N | N | N |
| C2: Cột phủ một phần tuần/tháng do kỳ lọc | - | Y | N | - |
| C3: Đơn vị Ngày | - | N | - | Y |
| **Kết quả** | Chưa kết thúc (sọc + nét đứt) | Bị cắt (xám) | Đủ kỳ (đặc) | Không bao giờ Bị cắt |
| CO | CO-96; CO-100 | CO-98; CO-99 | CO-97 | CO-97 |

Tổ hợp R2 với C3 = Y không khả thi (cột Ngày không bị cắt — nguồn).

**DT2 — Ưu tiên hiển thị khi trùng trạng thái (PRD mục 5)**

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Chưa kết thúc | Y | N | N | Y |
| Âm | Y | Y | N | N |
| Bị cắt | - | Y | Y | - |
| Cao nhất | N | N | N | Y |
| **Hiển thị** | Sọc chéo | Đỏ | Xám | Sọc + viền vàng liền |
| CO | CO-128 | CO-129 | CO-129 | CO-130 |

Âm + Cao nhất không khả thi (cao nhất chỉ đánh dấu khi > 0).

**DT3 — Chia Incentive theo dòng đủ điều kiện (FR-INC-003, 004)**

| Rule | Khách | PIC trên bill | Other CA | Brand | Kết quả | CO |
|---|---|---|---|---|---|---|
| R1 | B2B không PIC | - | - | mọi Brand | N/A, không cộng ai | CO-194 |
| R1b | B2B có PIC | Có | Có | mọi Brand | N/A (không đi nhánh FR-INC-004) | CO-247 |
| R2 | B2C không PIC (hoặc PIC ở store khác) | - | ≥ 1 người | mọi Brand | Chia đều tổng dòng đủ điều kiện | CO-192; CO-193; CO-196 |
| R3 | Có PIC | Có | Có | Hanoia | 70 / 30 chia đều | CO-197; CO-205 |
| R4 | Có PIC | Không | Có | Hanoia | 0 / 100 | CO-198 |
| R5 | Có PIC | Có | Có | Kenzo, Marc Jacobs, Rimowa, B&O, Devialet, Tâm Sơn Living, Patek Philippe | 100 / 0 | CO-199 |
| R6 | Có PIC | Không | Có | Chopard, Chaumet, Piaget, JLC, Buccellati | 70 / 30 | CO-200 |
| R7 | Có PIC | Có | Có | Loewe, BV, TB, Sandro, Maje, MK, Longchamp | 50 / 50 | CO-201 |
| R8 | Có PIC | Không | Có | BOSS, BOSS Green, HUGO, FL, ADLV | 0 / 100 | CO-202 |
| R9 | Có PIC | Có | Không | Hermès và mọi Brand (BR-INC-003) | 100% | CO-203; CO-206 |
| R10 | Có PIC | Có | 2 người | Hermès | 50 / 25 / 25 | CO-204 |
| R11 | Có PIC | Không | Không | mọi Brand | ? | Pending - Q-30 |
| R12 | Tổ hợp Brand × PIC × Other CA khác | | | | theo §6.1 | Pending - Q-11 |

**DT4 — Discount Threshold Gate theo dòng (FR-INC-002):** Discount % < Threshold → đủ điều kiện; ≥ Threshold → loại. CO: CO-184; CO-185; CO-186; CO-187.

**Tập phần tử — dòng sản phẩm trên bill (FR-INC-002 → 003/004/005)**

| Mục | Áp dụng? | CO / lý do |
|---|---|---|
| Phần tử ngoài tập được chọn chịu cùng sự kiện | Có — dòng bị loại không được dùng khi chia | CO-192; CO-207; CO-209 |
| Phần tử duy nhất thoả điều kiện chuyển sang không thoả (tập rỗng) | Có — mọi dòng bị loại | CO-191 |
| ≥ 2 phần tử thuộc các rule khác nhau cùng lúc | Có — 2 dòng khác Brand / khác Discount | CO-183; CO-188; CO-189 |
| Tập rỗng · 1 phần tử · tất cả phần tử cùng rule | 1 dòng: nhiều case; tập rỗng: bill 0 dòng không khả thi trên POS | CO-184; CO-203 |

**Tập phần tử — store được chọn (FR-SPM-011)**

| Mục | Áp dụng? | CO / lý do |
|---|---|---|
| Phần tử ngoài tập được chọn | Có — store ngoài phạm vi không xuất hiện | CO-27; CO-148 |
| Tập còn 1 / thành rỗng | Có — không bỏ được store cuối; 1 store đổi xếp hạng & tab | CO-151; CO-165; CO-174 |
| ≥ 2 phần tử khác nhóm (khác Brand, khách chung) | Có | CO-77; CO-176 |
| Store trong tập nhưng không phát sinh | Có | CO-163; CO-179 |

## 9a. Ma trận tương tác

| IX_ID | Thực thể / trạng thái | A — yêu cầu thay đổi | B — yêu cầu phụ thuộc | Câu hỏi kiểm thử | Kết luận |
|---|---|---|---|---|---|
| IX-01 | Cách nhìn thuế | REQ-UI-02 | FR-SPM-003, 004, 005, 007 | Đổi thuế, thẻ đếm/tỷ lệ còn giữ nguyên? | CO-88 |
| IX-02 | Cách nhìn thuế | REQ-UI-02 | FR-SPM-010 | Đổi thuế, biểu đồ đổi giá trị nhưng giữ đơn vị và trạng thái cột? | CO-118 |
| IX-03 | Cách nhìn thuế | REQ-UI-02 | FR-SPM-011 (xếp hạng) | Đổi thuế, thứ tự xếp hạng tính lại theo Sales thuế mới? | CO-162 |
| IX-04 | Cách nhìn thuế | REQ-UI-02 | FR-SPM-009 (nhãn), FR-SPM-011 (bảng) | Đổi thuế, mọi số tiền ở bảng/biểu đồ đổi nhãn? | CO-85 |
| IX-05 | Kỳ lọc | REQ-UI-01 | FR-SPM-010 (đơn vị chọn tay) | Đổi kỳ khi đơn vị chọn tay còn / hết khả dụng; kỳ 1 ngày làm tập đơn vị khả dụng rỗng | CO-115; CO-116; CO-117 |
| IX-06 | Kỳ lọc = 1 ngày | REQ-UI-01 | FR-SPM-010 | Tập đơn vị khả dụng rỗng → biểu đồ ẩn, KPI vẫn tính | CO-101 |
| IX-07 | Kỳ lọc | REQ-UI-01 | REQ-UI-03 | Đổi kỳ, cảnh báo Cross-period cập nhật / biến mất? | CO-92; CO-93 |
| IX-08 | Tập store đã chọn | FR-SPM-011 | FR-SPM-004, 008 (Total Customers) | Gộp store có khách chung → đếm 1 lần | CO-77; CO-172 |
| IX-09 | Tập store còn 1 phần tử | FR-SPM-011 (bộ chọn) | FR-SPM-011 (xếp hạng) | Còn 1 store → panel chuyển sang xếp hạng Client Advisor | CO-165 |
| IX-10 | Tập store còn 1 phần tử | FR-SPM-011 (bộ chọn) | FR-SPM-011 (bảng) | Còn 1 store → mất tab Theo Store; store cuối không bỏ được (tập rỗng bị chặn) | CO-174; CO-151 |
| IX-11 | Số Brand trong phạm vi | FR-SPM-001 (vai trò) | FR-SPM-011 (bảng) | Phạm vi 1 Brand → mất tab Theo Brand | CO-175 |
| IX-12 | Số store đã chọn | FR-SPM-011 (bộ chọn) | FR-SPM-011 (lọc CA) | Vượt / không vượt 5 store → khoá / mở lọc Client Advisor | CO-156; CO-157 |
| IX-13 | Lựa chọn Client Advisor | FR-SPM-011 (bộ chọn store) | FR-SPM-011 (lọc CA) | Đang lọc CA rồi chọn thêm vượt 5 store | Pending - Q-25 |
| IX-14 | Lựa chọn Client Advisor | FR-SPM-011 (lọc CA) | KPI, FR-SPM-010 | Lọc CA → KPI và biểu đồ chỉ còn bill của CA | CO-158; CO-144 |
| IX-15 | Từ khoá tìm kiếm bảng | FR-SPM-011 | FR-SPM-011 (cột #, dòng Tổng) | Tìm kiếm / đổi trang làm đổi cột # hoặc dòng Tổng? | CO-170; CO-171 |
| IX-16 | Thứ tự sắp xếp bảng | FR-SPM-011 | FR-SPM-011 (cột #) | Đổi cột sắp xếp → cột # theo thứ tự mới | CO-173 |
| IX-17 | Vai trò Cá nhân | FR-SPM-001 | FR-SPM-011, REQ-UI-05 | Vai trò Cá nhân → không có xếp hạng, bảng thay bằng thẻ | CO-29 |
| IX-18 | Trạng thái đơn (CO → VO) | FR-SPM-002 | FR-SPM-003, KPI dẫn xuất | Đơn đã tính chuyển VO → rời Sales và Transactions | CO-37 |
| IX-19 | Đơn trả | FR-SPM-002 (trừ Sales) | FR-SPM-003 (Transactions) | Đơn trả toàn bộ → Transactions không giảm | CO-50; CO-59 |
| IX-20 | Đơn trả | FR-SPM-002 | FR-SPM-004, 008 (Total Customers) | Khách chỉ có đơn trả → không vào mẫu số nhưng hoàn vẫn trừ | CO-54; CO-75 |
| IX-21 | Đơn 0đ | FR-SPM-003 | FR-SPM-004, 005, 006, 007 | Đơn 0đ thay đổi mẫu số Transactions → các tỷ lệ | CO-58; CO-66; CO-70; CO-56 |
| IX-22 | Sales âm | FR-SPM-002 | FR-SPM-010, FR-SPM-011 (xếp hạng) | Sales âm → cột đỏ, trục âm; store chỉ có đơn trả vẫn xếp hạng | CO-121; CO-164 |
| IX-23 | Đơn trả cross-period | FR-SPM-002 | FR-SPM-010 (bucket) | Đơn trả trừ vào bucket ngày trả | CO-120 |
| IX-24 | Cờ is_incentive_eligible từng dòng | FR-INC-002 | FR-INC-003, 004 | Dòng bị loại → không vào tổng chia đều / không tra config | CO-192; CO-207 |
| IX-25 | Tập dòng đủ điều kiện rỗng | FR-INC-002 | FR-INC-005 | Mọi dòng bị loại → bill không đóng góp Incentive | CO-191 |
| IX-26 | Loại khách B2B | FR-INC-003 (loại khỏi Incentive) | FR-SPM-002 (tính vào Sales) | Cùng bill B2B: Incentive N/A nhưng Sales vẫn tính | CO-194; CO-47 |
| IX-27 | PIC của khách | pic-management (đổi PIC) | FR-INC-003 | Đổi PIC sau khi bill phát sinh | CO-195 |
| IX-29 | Lựa chọn Client Advisor | FR-SPM-011 (lọc CA) | FR-SPM-011 (xếp hạng, bảng) | Đang lọc CA, panel xếp hạng và bảng hiển thị gì? | Pending - Q-25 |
| IX-30 | Cách nhìn thuế | REQ-UI-02 | FR-SPM-011 (sắp xếp, cột #) | Đổi thuế khi bảng đang sắp theo Sales | CO-246 |
| IX-31 | Tập store đã chọn | FR-SPM-011 | REQ-UI-03 (số đơn trong cảnh báo) | Đổi store, số đơn trả cross-period trong cảnh báo đổi theo | CO-237 |
| IX-32 | Tập store chỉ 1 Brand | FR-SPM-011 (chip Brand) | FR-SPM-011 (tab Brand) | Chip 1 Brand → tab Theo Brand | CO-245 |
| IX-33 | Vai trò Cá nhân × PIC | PIC State Machine | FR-SPM-001 (mức Cá nhân) | CA là PIC nhưng không đứng tên bill | CO-230 |
| IX-28 | Threshold theo Brand | FR-INC-002 (đổi ngưỡng 1 Brand) | FR-INC-002 (Brand khác) | Hạ ngưỡng Brand X không ảnh hưởng Brand khác | CO-190 |

## 9b. Sự kiện kích hoạt & kênh

| EV_ID | Hành vi | Sự kiện kích hoạt / kênh | Kết luận |
|---|---|---|---|
| EV-01 | KPI + bộ lọc | Lần đầu vào màn hình (kỳ và thuế mặc định) | CO-10; CO-11 |
| EV-02 | KPI | Đổi preset / khoảng ngày | CO-07; CO-04 |
| EV-03 | KPI, biểu đồ, bảng | Đổi store / chip Brand | CO-155; CO-149 |
| EV-04 | KPI, biểu đồ, xếp hạng | Đổi cách nhìn thuế (cùng snapshot, không tải lại) | CO-12 |
| EV-05 | Bộ lọc | Tải lại trang (F5) | Pending - Q-27 |
| EV-06 | Số liệu | Đơn mới đồng bộ từ HUB khi đang mở dashboard | Pending - Q-28 |
| EV-07 | Số liệu kỳ cũ | Đơn về chậm từ HUB; đơn chuyển VO sau khi đã tính | CO-31; CO-37 |
| EV-08 | Phạm vi | Gọi thẳng API với store ngoài phạm vi | CO-25 |
| EV-09 | Phạm vi Cá nhân | Client Advisor gọi API số cấp store / CA khác | CO-26 |
| EV-10 | Phạm vi | Đăng xuất – đăng nhập vai trò khác cùng trình duyệt | CO-30 |
| EV-11 | Phạm vi | Truy cập URL dashboard / API khi chưa đăng nhập | CO-233 |
| EV-12 | Phiên | Phiên hết hạn khi đang thao tác | N/A - cơ chế phiên chung của MOSAIC, tài liệu không đặc tả |
| EV-13 | Tooltip | Rê chuột vào cột / icon i | CO-140; CO-89 |
| EV-14 | Tooltip | Focus bằng bàn phím | CO-228 |
| EV-15 | Biểu đồ | Đổi kích thước cửa sổ / breakpoint | CO-139; CO-224 |
| EV-16 | Biểu đồ kỳ chạm hôm nay | Qua 0h khi đang mở dashboard | Pending - Q-28 |
| EV-17 | Số Cá nhân | Kênh thứ hai: tab Theo Client Advisor của quản lý vs dashboard Cá nhân | CO-16; CO-177 |
| EV-18 | Total Customers | Kênh thứ hai: dashboard Khách hàng (FR-CSD-002) | CO-55 |
| EV-19 | Sales | Kênh thứ hai: tổng bucket biểu đồ, dòng Tổng bảng, panel xếp hạng | CO-119; CO-172; CO-160 |
| EV-20 | Bảng | Export / drill-down tuỳ ý | N/A - Out of Scope PRD: không export pivot, không drill-down tùy biến |
| EV-22 | Bộ lọc | Nút Back của trình duyệt | Pending - Q-27 |
| EV-23 | Bộ lọc | URL có tham số lọc (chia sẻ link) | Pending - Q-27 |
| EV-24 | Số liệu | Tab / phiên thứ hai cùng tài khoản | N/A - dashboard chỉ đọc, không có thao tác ghi; mỗi tab tự giữ bộ lọc |
| EV-21 | Incentive | Kênh hiển thị Incentive trên dashboard | Pending - Q-09 |

## 10. Ma trận phân quyền

| Hành động \ Vai trò | CRM Team | Retail Manager | Store Manager | Client Advisor |
|---|---|---|---|---|
| Xem số toàn Tam Sơn | ✔ | ✘ | ✘ | ✘ |
| Xem số store của Brand mình | ✔ | ✔ | Chỉ store được gán | ✘ |
| Xem số cấp store được gán | ✔ | ✔ | ✔ | ✘ |
| Xem bill mình đứng tên (trọn bill) | – | – | – | ✔ |
| Panel xếp hạng, bảng breakdown | ✔ | ✔ | ✔ | ✘ (thẻ giải thích) |
| Gọi API số ngoài phạm vi | ✘ | ✘ | ✘ | ✘ |
| Xem Incentive của nhân viên | Q-42 | Q-42 | Q-42 | Q-42 |

Store Manager 1 store (U-SM1): như cột Store Manager nhưng phạm vi chỉ 1 store — CO CO-231.

## 11. Tích hợp & phụ thuộc

- ERP/POS → HUB → Mosaic: đơn bán, đơn trả (m_rma_id), dòng sản phẩm, list_employees[]; Mosaic dùng nguyên total/tax_total.
- FR-CSD-002 (dashboard Khách hàng): định nghĩa Total Customers — đối chiếu chéo ở CO CO-55.
- PIC State Machine (pic-management), Product Master (product_id → brand_id), Brand Incentive Config (§6.1).
- Log cảnh báo của job tính số (VAT thiếu, lệch công thức header).

## 12. Quan sát UI (từ mockup)

| Màn hình | Thành phần | Ghi chú / chênh lệch so với văn bản |
|---|---|---|
| Dashboard (image1–3) | Tabs Business, Sales by Staff, Customer, Product, Task, Appointment, Event; tab đang gạch chân là Appointment | Không rõ dashboard thuộc tab nào (Q-32) |
| Bộ lọc | KỲ XEM 5 nút; TỪ NGÀY – ĐẾN NGÀY 01/10/2026 – 14/10/2026 + icon lịch; STORE dropdown Tất cả store (100 store) / Brand Hermès (2 store); GIÁ TRỊ TIỀN Sau thuế (đang chọn) / Trước thuế | Mockup không hiện bộ lọc Client Advisor; nhãn Brand Hermès (2 store) khác BR-SPM-020 (Q-34) |
| Cảnh báo | Khung nền xanh: Có 212 đơn trả của đơn bán kỳ trước đã trừ vào Sales kỳ này… Transactions không bị trừ khi có đơn trả | Văn bản nguồn không có nội dung nguyên văn (Q-23) |
| KPI | DOANH THU VÀ GIAO DỊCH · 100 store: SALES (badge Sau thuế, dòng phụ Trước thuế), TRANSACTIONS, TOTAL CUSTOMERS, COUPON %; CHỈ SỐ BÌNH QUÂN: AOV, UPT, FREQUENCY, AVG SPENDING / CUSTOMER; icon i cạnh tên | Số chính SALES 301852754000, TRANSACTIONS 4531 không tách nghìn — trái quy tắc (Q-04) |
| Biểu đồ | SALES THEO THỜI GIAN; nút Ngày (active) / Tuần / Tháng (mờ); nhãn Tự chọn theo độ dài kỳ · Sau thuế; trục 0, 10 Tỷ, 20 Tỷ, 30 Tỷ; cột 10/10 viền vàng nhãn 29 Tỷ; cột 14/10 viền nét đứt; chú giải Đủ kỳ, Chưa kết thúc, Cao nhất, Nền xám… | Khớp PRD |
| Xếp hạng | XẾP HẠNG STORE THEO SALES; Top 10 (active) / Bottom 10; hạng, tên store, Brand, Sales tách nghìn | Ghi chú cuối panel về 100 store có phát sinh |
| Bảng | Tab Theo Store / Theo Brand / Theo Client Advisor; ô tìm kiếm; cột #, STORE, BRAND, SALES▼ (Sau thuế), TRANSACTIONS, AOV, UPT, COUPON %, TOTAL CUSTOMERS, FREQUENCY, AVG SPENDING / CUSTOMER; dòng Tổng (mỗi đơn tính 1 lần); 1–15 / 100 store; Mỗi trang 15; 1/7 | Mặc định sắp Sales giảm dần (quan sát); số trong bảng không tách nghìn (Q-04) |

## 13. Câu hỏi làm rõ

| ID | Câu hỏi | Liên quan | Mức độ | Trả lời |
|---|---|---|---|---|
| Q-01 | Đơn bán hợp lệ Net Amount = 0 có là transaction không? Mockup thẻ TRANSACTIONS ghi 93 đơn 0đ không tính (ngược nhãn bắt buộc gồm đơn 0đ). BR-SPM-006, AC-SPM-003-01/06, AC-SPM-005-03, AC-SPM-007-05, AC-SPM-008-06 nói CÓ; công thức FR-SPM-003 (net_amount > 0), sơ đồ §2.1 (loại đơn 0đ), BR-SPM-014 gạch đầu dòng 6 và AC-SPM-002-13 nói KHÔNG; AC-SPM-004-01 (Transactions = 5) lệch AC-SPM-003-01 (= 6) trên cùng Phụ lục A | FR-SPM-003…008 | Blocker | (chờ) |
| Q-02 | Đơn vị Ngày bấm được khi kỳ 2→31 ngày (PRD Logic hiển thị) hay 2→62 ngày (BR-SPM-015, AC-SPM-010-03)? Ví dụ Custom 02/08–14/10 (74 ngày) ghi Ngày bấm được — mâu thuẫn cả hai | FR-SPM-010 | Major | (chờ) |
| Q-03 | Trạng thái Chưa kết thúc có cần điều kiện kỳ lọc kéo tới hôm nay (PRD, ví dụ 11/10–12/10) không? BR-SPM-017 chỉ nêu bucket chứa hôm nay | FR-SPM-010 | Major | (chờ) |
| Q-04 | Mockup hiển thị số không tách nghìn (thẻ Sales 301852754000, Transactions 4531, các cột bảng) trong khi quy tắc yêu cầu tách nghìn bằng khoảng trắng — theo quy tắc? Số đếm ≥ 1 000 có tách nghìn không? | FR-SPM-009 | Minor | (chờ) |
| Q-05 | Cách nhìn thuế mặc định khi mở dashboard (OQ-SPM-15)? Mockup đang chọn Sau thuế | REQ-UI-02 | Major | (chờ) |
| Q-06 | Kỳ mặc định khi mở dashboard (mockup: Tháng này)? Preset Tuần này kết thúc ở hôm nay hay Chủ Nhật? | REQ-UI-01 | Minor | (chờ) |
| Q-07 | Chọn khoảng > 366 ngày: nội dung và vị trí thông báo lỗi? (nguồn chỉ ghi báo lỗi giữ kỳ cũ) | REQ-UI-01 | Major | (chờ) |
| Q-08 | Từ ngày > Đến ngày, hoặc chọn ngày tương lai: lịch có chặn không, thông báo gì? | REQ-UI-01 | Minor | (chờ) |
| Q-09 | Incentive (REQ-BSP-01) hiển thị ở đâu trên dashboard (khối, cột, tab Sales by Staff?) và drill-down theo Brand thế nào? Mockup không có khối Incentive | FR-INC-005 | Blocker | (chờ) |
| Q-10 | Giá trị dòng dùng làm base chia Incentive là trường nào (Net Amount dòng sau thuế, trước thuế hay total_amount)? Số hiển thị là phần doanh số được chia hay tiền hoa hồng (format migrate có incentive_percent)? | FR-INC-003, 004 | Major | (chờ) |
| Q-11 | Cần bảng Brand Incentive Config đầy đủ (§6.1, SharePoint — chưa đọc được) cho các tổ hợp Brand × PIC trên bill × Other CA không có trong AC | FR-INC-004 | Major | (chờ) |
| Q-12 | Discount % có làm tròn trước khi so Threshold không (29.995%)? Gross Value dòng = 0 xử lý thế nào? | FR-INC-002 | Minor | (chờ) |
| Q-13 | customer_in_period: BR-SPM-012 nói khách chỉ có đơn trả/đơn huỷ vẫn có thể ở mẫu số; AC-SPM-004-05, AC-SPM-008-05 nói khách chỉ có đơn trả không vào Total Customers — đâu đúng? | FR-SPM-004, 008 | Major | (chờ) |
| Q-14 | Đơn ecom có tính ở mức Toàn Tam Sơn không (OQ-SPM-06, mặc định không tính) — đã chốt? | FR-SPM-001 | Major | (chờ) |
| Q-15 | Sales sau thuế có gồm phí ship không (OQ-SPM-03) — nhãn thẻ Sales cần ghi có/không gồm phí ship | FR-SPM-002, 009 | Minor | (chờ) |
| Q-16 | Đơn khách B2B có tính vào Sales và các chỉ số dashboard không (OQ-SPM-05, đề xuất: tính)? | FR-SPM-002 | Major | (chờ) |
| Q-17 | Dòng dịch vụ (không barcode, ví dụ khắc tên) có tính vào số lượng UPT không (OQ-SPM-07; BR-SPM-011 đang là giả định)? | FR-SPM-007 | Major | (chờ) |
| Q-18 | Xác nhận nhận diện đơn trả bằng m_rma_id (DQ-SPM-03) và bản ghi đơn trả có total/tax_total như đơn bán (DQ-SPM-09) | FR-SPM-002 | Major | (chờ) |
| Q-19 | FR-SPM-010 (biểu đồ) và FR-SPM-011 (quy mô 100 store) là đề xuất thiết kế chờ OQ-SPM-17, OQ-SPM-18 — business đã chấp thuận chưa? | FR-SPM-010, 011 | Major | (chờ) |
| Q-20 | NFR-INC-001: cơ chế điều chỉnh Incentive khi bill bị huỷ/hoàn trả (OQ-INC-004)? | NFR-INC-001 | Major | (chờ) |
| Q-21 | Migrate: hệ thống xử lý record vi phạm thế nào (salerep_ids rỗng, thiếu cả erp_user_id và erp_partner_id, trùng ID + incentive_role, order_status VO/IP, số dạng chuỗi)? | REQ-MIG-01 | Major | (chờ) |
| Q-22 | Corporate Sale (BR-INC-005) có đồng nghĩa với Business Account B2B (FR-INC-003) không? | FR-INC-005 | Minor | (chờ) |
| Q-23 | Cảnh báo động: nội dung nguyên văn; khi không có đơn liên quan thì ẩn hẳn? Cảnh báo VAT = 0 xuất hiện theo điều kiện nào (có ≥1 đơn tax_total = 0 và total > 0 trong kỳ)? | REQ-UI-03 | Minor | (chờ) |
| Q-24 | Nội dung ghi chú khi store/Client Advisor không phát sinh trong kỳ (BR-SPM-023)? | FR-SPM-011 | Minor | (chờ) |
| Q-25 | Đang lọc Client Advisor, người xem chọn thêm store vượt 5: lựa chọn CA bị xoá hay giữ? Khi đang lọc CA, panel xếp hạng và bảng hiển thị gì? | FR-SPM-011 | Minor | (chờ) |
| Q-26 | Chia đều không hết (10 000 000 ÷ 3): làm tròn thế nào, phần dư cho ai? | FR-INC-003 | Minor | (chờ) |
| Q-27 | Tải lại trang (F5), nút Back, URL có tham số: có giữ/khôi phục bộ lọc kỳ/store/thuế/đơn vị biểu đồ không? | REQ-UI-01 | Minor | (chờ) |
| Q-28 | Dữ liệu dashboard cập nhật theo chu kỳ nào khi có đơn mới từ HUB (realtime / khi tải lại / theo lịch)? | FR-SPM-009 | Minor | (chờ) |
| Q-29 | Bấm vào đơn vị đang được tự chọn có chuyển nhãn sang Đã chọn tay không? | FR-SPM-010 | Minor | (chờ) |
| Q-30 | Bill không có nhân viên đứng tên, hoặc PIC không trên bill và không có Other CA (Brand cho PIC 0%): Incentive tính thế nào? | FR-INC-003, 004 | Major | (chờ) |
| Q-31 | Đơn trả được tính vào mức Cá nhân / tab Client Advisor của ai (nhân viên của đơn bán gốc hay người thực hiện trả)? | FR-SPM-001 | Major | (chờ) |
| Q-32 | Dashboard Doanh thu & Đơn hàng nằm ở tab nào (mockup đang gạch chân tab Appointment, có tab Business)? | REQ-UI-04 | Minor | (chờ) |
| Q-33 | Field chuẩn nhận diện đơn có coupon (vouchers[], discount_lines[].coupon_id, SF_Loyalty_Discount kèm Voucher Code)? | FR-SPM-005 | Minor | (chờ) |
| Q-34 | Nhãn bộ chọn sau khi bấm chip Brand: 14 store đã chọn (AC-SPM-011-02) hay Brand Hermès · 14 store (BR-SPM-020); mockup ghi Brand Hermès (2 store)? | FR-SPM-011 | Minor | (chờ) |
| Q-36 | Tài khoản nhiều Position có phạm vi rời nhau (SM ST1 + Retail Manager Brand khác): áp một phạm vi lớn nhất (đo theo mức hay số store?) hay hợp các phạm vi? | FR-SPM-001 | Major | (chờ) |
| Q-37 | Tab Brand chỉ khi phạm vi có > 1 Brand: phạm vi Position hay tập store đang chọn (mockup image2 ẩn tab khi chọn Brand Hermès)? | FR-SPM-011 | Minor | (chờ) |
| Q-38 | Ví dụ đối chiếu Custom 02/08–14/10: thực tế chạm 12 tuần lịch (nguồn ghi 11 cột) và 3 tháng lịch (Tháng phải bấm được, nguồn chỉ ghi Ngày, Tuần) — xác nhận theo quy tắc Bước 1? | FR-SPM-010 | Major | (chờ) |
| Q-39 | Trục Y: khoảng 4–5 khoảng chia (PRD) hay khoảng 4 mốc (BR-SPM-018)? | FR-SPM-010 | Minor | (chờ) |
| Q-40 | Mức Cá nhân: Total Customers, Frequency, Coupon %, AOV, Avg Spending tính trên tập nào? Bộ chọn Store và lọc Client Advisor hiển thị gì cho Client Advisor? | FR-SPM-001 | Major | (chờ) |
| Q-41 | Discount % dòng: Gross Value và Net Amount cùng cơ sở thuế không? Xử lý Gross = 0 và Discount âm (Net > Gross)? | FR-INC-002 | Major | (chờ) |
| Q-42 | Vai trò nào được xem Incentive của ai (CRM, RM, SM, CA)? Có áp Position Rule ở tầng truy vấn như BR-SPM-001? | FR-INC-005 | Major | (chờ) |
| Q-43 | Half-up với số âm có phần lẻ ,5 (−1 250 000.5 → −1 250 001 hay −1 250 000)? | FR-SPM-009 | Minor | (chờ) |
| Q-44 | Nhãn giá trị trên cột cao nhất hiển thị rút gọn (Tr/Tỷ) hay số đầy đủ? | FR-SPM-010 | Minor | (chờ) |
| Q-45 | Khi khoảng nhập tay trùng một preset (vd. đúng tháng trước), nút preset có sáng không? | REQ-UI-01 | Minor | (chờ) |
| Q-46 | Tooltip Hoàn trả đã trừ hiển thị theo cách nhìn thuế đang chọn hay luôn sau thuế? | FR-SPM-010 | Minor | (chờ) |
| Q-47 | Bộ preset Hôm nay/Tuần này/Tháng này/Tháng trước/Năm này có thay bộ lọc chung Day/Week/Month/Custom kế thừa BRD (OQ-SPM-09)? | REQ-UI-01 | Minor | (chờ) |
| Q-48 | Nhãn bộ chọn Store khi người xem không phải CRM chọn toàn bộ phạm vi của mình (SM 2 store, RM Hermès 14 store)? | FR-SPM-011 | Minor | (chờ) |
| Q-49 | Chú giải Đủ kỳ / Cao nhất luôn có — giữ nguyên khi không có cột Đủ kỳ hoặc không có cột > 0? | FR-SPM-010 | Minor | (chờ) |
| Q-50 | Incentive gán vào kỳ báo cáo theo ngày nào (ngày hoàn tất bill UTC+7 hay order_date)? | FR-INC-005 | Minor | (chờ) |
| Q-51 | Gộp tài khoản khách làm đổi số kỳ cũ: cách gộp trên môi trường test và chỉ số nào thay đổi? | FR-SPM-009 | Minor | (chờ) |
| Q-35 | Hai store cùng Sales trong xếp hạng: thứ tự theo tiêu chí phụ nào? | FR-SPM-011 | Minor | (chờ) |

## 14. Giả định

> Giả định **tạm thời** khi Q chưa có trả lời. Trạng thái: `Chưa xác nhận` / `Đã xác nhận` / `Sai — đã sửa case`.

| ID | Giả định | Câu hỏi liên quan | Case bị ảnh hưởng | Trạng thái xác nhận |
|---|---|---|---|---|
| AS-01 | Đơn bán hợp lệ 0đ LÀ transaction (theo BR-SPM-006 in đậm và đa số AC) | Q-01 | TC-FLT-007, TC-SCOPE-005, TC-TRX-004, TC-FREQ-005, TC-CPN-002, TC-AOV-007, TC-UPT-004 | Chưa xác nhận |
| AS-02 | Ngày bấm được khi kỳ 2–62 ngày (theo BR-SPM-015 và AC-SPM-010-03) | Q-02 | TC-CHART-005, TC-CHART-014, TC-CHART-017 | Chưa xác nhận |
| AS-03 | Chưa kết thúc chỉ khi bucket chứa hôm nay VÀ kỳ lọc kéo tới hôm nay (theo PRD) | Q-03 | TC-CHART-004, TC-CHART-051 | Chưa xác nhận |
| AS-04 | Mặc định Sau thuế khi mở dashboard (theo mockup) | Q-05 | TC-FLT-011 | Chưa xác nhận |
| AS-05 | Kỳ mặc định Tháng này; Tuần này = Thứ Hai đến hôm nay (theo mockup và các ví dụ preset kết thúc ở hôm nay) | Q-06 | TC-FLT-003, TC-FLT-010 | Chưa xác nhận |
| AS-06 | Khách chỉ có đơn trả trong kỳ không vào Total Customers (theo AC-SPM-004-05, AC-SPM-008-05) | Q-13 | TC-FREQ-003, TC-AVGS-004 | Chưa xác nhận |
| AS-07 | Cảnh báo động ẩn khi kỳ không có đơn liên quan | Q-23 | TC-ALERT-002 | Chưa xác nhận |
| AS-08 | Nhãn sau khi bấm chip Brand theo BR-SPM-020: Brand <tên> · N store | Q-34 | TC-STORE-003 | Chưa xác nhận |
| AS-09 | Đơn ecom không tính ở mức Toàn Tam Sơn (mặc định FRD) | Q-14 | TC-FLT-007, TC-SCOPE-005, TC-SCOPE-010 | Chưa xác nhận |

## 15. Đánh giá rủi ro

| Khu vực | Khả năng (1–3) | Ảnh hưởng (1–3) | Điểm | Priority đề xuất |
|---|---|---|---|---|
| Phạm vi dữ liệu theo vai trò / lộ số qua API | 2 | 3 | 6 | P1 |
| Công thức Sales sau/trước thuế, đơn trả cross-period | 3 | 3 | 9 | P1 |
| Transactions & đơn 0đ (mâu thuẫn nguồn) | 3 | 3 | 9 | P1 |
| Incentive chia theo Brand/PIC (tiền thưởng nhân viên) | 3 | 3 | 9 | P1 |
| Chỉ số dẫn xuất AOV/UPT/Coupon/Frequency/Avg | 2 | 2 | 4 | P2 |
| Biểu đồ: chọn đơn vị, trạng thái cột, đối soát tổng | 2 | 2 | 4 | P2 (đối soát P1) |
| Bộ chọn store, xếp hạng, bảng quy mô 100 store | 2 | 2 | 4 | P2 |
| Định dạng số, nhãn, chú giải, tooltip | 2 | 1 | 2 | P3 |
| Thẩm mỹ (thanh dữ liệu, hover, lật tooltip) | 1 | 1 | 1 | P4 |

## 16. Điều kiện kiểm thử

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-01 | REQ-UI-01;REQ-UI-02 | Khối bộ lọc có đủ 5 preset, Từ ngày – Đến ngày, Store, Client Advisor, Giá trị tiền | CL | TC-FLT-001 |  |
| CO-02 | REQ-UI-01 | Preset Hôm nay → kỳ 1 ngày là hôm nay | EP | TC-FLT-002 |  |
| CO-03 | REQ-UI-01 | Preset Tuần này → Thứ Hai tuần hiện tại đến hôm nay | EP | TC-FLT-003 |  |
| CO-04 | REQ-UI-01 | Preset Tháng này → ngày 01 đến hôm nay | EP | TC-FLT-004 |  |
| CO-05 | REQ-UI-01 | Preset Tháng trước → trọn tháng dương lịch trước | EP | TC-FLT-005 |  |
| CO-06 | REQ-UI-01 | Preset Năm này → 01/01 đến hôm nay | EP | TC-FLT-006 |  |
| CO-07 | REQ-UI-01 | Chọn khoảng Từ ngày – Đến ngày hợp lệ → mọi khối tính theo kỳ mới | EP | TC-FLT-007 |  |
| CO-08 | REQ-UI-01 | Khoảng 366 ngày (biên trên) được chấp nhận | BVA | TC-FLT-008 |  |
| CO-09 | REQ-UI-01 | Khoảng 367 ngày bị chặn: báo lỗi, giữ kỳ cũ | BVA | TC-FLT-009 |  |
| CO-10 | REQ-UI-01 | Kỳ mặc định khi mở dashboard | EP | TC-FLT-010 |  |
| CO-11 | REQ-UI-02 | Cách nhìn thuế mặc định khi mở dashboard | EP | TC-FLT-011 |  |
| CO-12 | FR-SPM-009 | Đổi thuế không tải lại dữ liệu, hai cách nhìn cùng snapshot | EG | TC-FLT-012 |  |
| CO-13 | FR-SPM-001 | SM 2 store: số liệu chỉ gồm ST1 + ST2, không có ST3 | PERM | TC-SCOPE-001 |  |
| CO-14 | FR-SPM-001 | SM chọn riêng ST2: mọi chỉ số chỉ trên ST2 | EP | TC-SCOPE-002 |  |
| CO-15 | FR-SPM-001 | Client Advisor chỉ thấy bill mình đứng tên, không thấy số store/người khác | PERM | TC-SCOPE-003 |  |
| CO-16 | FR-SPM-001 | Bill 2 CA: mỗi người thấy trọn bill, tổng CA > store | DT | TC-SCOPE-004 |  |
| CO-17 | FR-SPM-001 | CRM Team thấy toàn Tam Sơn, khớp tổng truy vấn đối soát | PERM | TC-SCOPE-005 |  |
| CO-18 | FR-SPM-001 | Tài khoản nhiều Position nhận phạm vi lớn nhất | PERM | TC-SCOPE-006 |  |
| CO-19 | FR-SPM-001;FR-SPM-003 | Đơn VO không vào Sales/Transactions | EP | TC-SCOPE-007 |  |
| CO-20 | FR-SPM-001 | Đơn nháp/đang xử lý không vào Sales/Transactions | EP | TC-SCOPE-008 |  |
| CO-21 | FR-SPM-001 | Đơn ecom không vào phạm vi store nào | EP | TC-SCOPE-009 |  |
| CO-22 | FR-SPM-001 | Đơn ecom không tính ở Toàn Tam Sơn | EP | TC-SCOPE-010 |  |
| CO-23 | FR-SPM-001 | Đơn hoàn tất 23:50 ngày cuối kỳ (UTC+7) thuộc kỳ | BVA | TC-SCOPE-011 |  |
| CO-24 | FR-SPM-001 | Đơn hoàn tất 00:00 ngày sau kỳ (UTC+7) không thuộc kỳ | BVA | TC-SCOPE-012 |  |
| CO-25 | FR-SPM-001 | Gọi API với store ngoài phạm vi bị từ chối | PERM | TC-SCOPE-013 |  |
| CO-26 | FR-SPM-001 | Client Advisor gọi API lấy số store/CA khác bị từ chối | PERM | TC-SCOPE-014 |  |
| CO-27 | FR-SPM-001;FR-SPM-011 | Bộ chọn store không liệt kê/không tìm được store ngoài phạm vi | PERM | TC-SCOPE-015 |  |
| CO-28 | FR-SPM-001 | Đơn list_employees = [] có ở mức store, không ở mức Cá nhân | EP | TC-SCOPE-016 |  |
| CO-29 | REQ-UI-05;FR-SPM-011 | Giao diện vai trò Cá nhân: không xếp hạng, bảng thay bằng thẻ giải thích | PERM | TC-SCOPE-017 |  |
| CO-30 | FR-SPM-001 | Đăng xuất, đăng nhập vai trò khác không giữ phạm vi cũ | EG | TC-SCOPE-018 |  |
| CO-31 | FR-SPM-009 | Đơn về chậm từ HUB thuộc kỳ cũ làm số kỳ cũ thay đổi | EG | TC-SCOPE-019 |  |
| CO-32 | FR-SPM-002 | Sales sau thuế = Σ total bán − Σ total trả trên Bộ ST1-D | EP | TC-SALES-001 |  |
| CO-33 | FR-SPM-002 | Sales trước thuế = sau thuế − (Σ tax bán − Σ tax trả) | EP | TC-SALES-002 |  |
| CO-34 | FR-SPM-002;FR-SPM-001 | Đơn trả cross-period trừ ở kỳ ngày trả, kỳ đơn bán giữ nguyên | DT | TC-SALES-003 |  |
| CO-35 | FR-SPM-002;FR-SPM-009 | Kỳ chỉ có đơn trả → Sales âm, dấu −, màu Error | EP | TC-SALES-004 |  |
| CO-36 | FR-SPM-002 | Header subtotal = 0, tax = 0, total > 0 → dùng total, log thiếu VAT | EG | TC-SALES-007 |  |
| CO-37 | FR-SPM-002 | Đơn đã tính chuyển VO → tự rời khỏi Sales | ST | TC-SALES-008 |  |
| CO-38 | FR-SPM-002 | Đơn trả toàn bộ cùng kỳ đóng góp 0 hai cách nhìn | EP | TC-SALES-005 |  |
| CO-39 | FR-SPM-002 | Đơn thật 12 525 500 / tax 1 138 682 → sau thuế 12 525 500, trước thuế 11 386 818 | EP | TC-SALES-009 |  |
| CO-40 | FR-SPM-002 | Đơn giảm giá: trước thuế 11 000 000, không phải subtotal | EP | TC-SALES-010 |  |
| CO-41 | FR-SPM-002 | Đơn 2 thuế suất: trước thuế 15 000 000, không phải 14 909 091 | EG | TC-SALES-011 |  |
| CO-42 | FR-SPM-002 | Đơn trả 5 400 000 / tax 400 000 → −5 400 000 / −5 000 000 | EP | TC-SALES-012 |  |
| CO-43 | FR-SPM-002 | Đơn 0đ không làm đổi Sales hai cách nhìn | EP | TC-SALES-006 |  |
| CO-44 | FR-SPM-002 | Lệch công thức header đúng 1đ → không ghi log | BVA | TC-SALES-013 |  |
| CO-45 | FR-SPM-002 | Lệch công thức header 2đ → ghi log, số theo total ERP | BVA | TC-SALES-014 |  |
| CO-46 | FR-SPM-002 | tax_total lớn hơn total → ghi log, số theo ERP | EG | TC-SALES-015 |  |
| CO-47 | FR-SPM-002 | Đơn khách B2B tính vào Sales | EP | TC-SALES-016 |  |
| CO-48 | FR-SPM-003 | Bộ ST1-D: Transactions = 5 gồm đơn khách lẻ | EP | TC-TRX-001 |  |
| CO-49 | FR-SPM-003 | Đơn 6 dòng 3 nhân viên đóng góp đúng 1 | EP | TC-TRX-002 |  |
| CO-50 | FR-SPM-003 | Đơn trả toàn bộ vẫn đếm 1 | EP | TC-TRX-003 |  |
| CO-51 | FR-SPM-003 | Đơn 0đ đếm vào Transactions | DT | TC-TRX-004 |  |
| CO-52 | FR-SPM-004 | Bộ ST1-D: Frequency = 5 ÷ 4 = 1.25 | EP | TC-FREQ-001 |  |
| CO-53 | FR-SPM-004 | Khách lẻ chung 3 đơn + K1 1 đơn → 2.00 | EP | TC-FREQ-002 |  |
| CO-54 | FR-SPM-004 | Khách chỉ có đơn trả không vào mẫu số Frequency | DT | TC-FREQ-003 |  |
| CO-55 | FR-SPM-004;FR-SPM-008 | Mẫu số = Total Customers của FR-CSD-002 (dashboard Khách hàng) | EP | TC-FREQ-004 |  |
| CO-56 | FR-SPM-004 | Khách chỉ có đơn 0đ có 1 transaction | DT | TC-FREQ-005 |  |
| CO-57 | FR-SPM-005 | Bộ ST1-D: Coupon % = 40.0% (đơn 3 mã đếm 1; giảm giá không mã không tính) | EP | TC-CPN-001 |  |
| CO-58 | FR-SPM-005 | Đơn coupon 100% vào cả tử và mẫu | DT | TC-CPN-002 |  |
| CO-59 | FR-SPM-005 | Đơn có coupon trả toàn bộ vẫn ở tử và mẫu | EP | TC-CPN-003 |  |
| CO-60 | FR-SPM-006 | Bộ ST1-D: AOV sau thuế = 8 520 000 | EP | TC-AOV-001 |  |
| CO-61 | FR-SPM-006 | AOV trước thuế = Sales trước thuế ÷ 5, ≤ AOV sau thuế | EP | TC-AOV-002 |  |
| CO-62 | FR-SPM-006 | Đơn trả kỳ trước kéo AOV về 0 | EP | TC-AOV-003 |  |
| CO-63 | FR-SPM-006 | Kỳ chỉ có đơn trả → AOV — | EP | TC-AOV-004 |  |
| CO-64 | FR-SPM-006 | AOV × Transactions = Sales (dữ liệu thật) | EP | TC-AOV-005 |  |
| CO-65 | FR-SPM-006 | AOV âm khi Sales âm | EP | TC-AOV-006 |  |
| CO-66 | FR-SPM-006 | Đơn 0đ kéo AOV xuống | DT | TC-AOV-007 |  |
| CO-67 | FR-SPM-007 | Bộ ST1-D: UPT = 9 ÷ 5 = 1.80 (trừ đơn trả, không cộng dòng giảm giá) | EP | TC-UPT-001 |  |
| CO-68 | FR-SPM-007 | Dòng phí ship không cộng vào net_qty | EP | TC-UPT-002 |  |
| CO-69 | FR-SPM-007 | Dòng dịch vụ khắc tên không cộng vào net_qty | EP | TC-UPT-003 |  |
| CO-70 | FR-SPM-007 | Đơn 0đ góp số lượng và +1 mẫu số | DT | TC-UPT-004 |  |
| CO-71 | FR-SPM-007 | UPT âm khi số lượng trả > bán | EP | TC-UPT-005 |  |
| CO-72 | FR-SPM-008 | Bộ ST1-D: Avg Spending sau thuế = 10 650 000 | EP | TC-AVGS-001 |  |
| CO-73 | FR-SPM-008 | Avg Spending trước thuế = Sales trước thuế ÷ 4 | EP | TC-AVGS-002 |  |
| CO-74 | FR-SPM-008 | Khách trả toàn bộ vẫn ở mẫu số | EP | TC-AVGS-003 |  |
| CO-75 | FR-SPM-008 | Khách chỉ có đơn trả không ở mẫu số, khoản hoàn vẫn trừ tử số | DT | TC-AVGS-004 |  |
| CO-76 | FR-SPM-008 | Khách chỉ có đơn 0đ ở mẫu số | EP | TC-AVGS-005 |  |
| CO-77 | FR-SPM-008 | Gộp ST1 + ST2: khách K1 mua 2 store đếm 1 | DT | TC-AVGS-006 |  |
| CO-78 | FR-SPM-008 | Avg Spending = Frequency × AOV (dữ liệu thật) | EP | TC-AVGS-007 |  |
| CO-79 | FR-SPM-009;FR-SPM-003;FR-SPM-004;FR-SPM-005;FR-SPM-007;FR-SPM-008 | Kỳ không có đơn: tỷ lệ hiển thị —, đếm/tiền hiển thị 0, cả hai cách nhìn | EP | TC-DISP-001 |  |
| CO-80 | FR-SPM-009 | UPT, Frequency hiển thị 2 chữ số lẻ (1.80, 1.25) | EP | TC-DISP-002 |  |
| CO-81 | FR-SPM-009 | Coupon % 66.666…% hiển thị 66.7% | BVA | TC-DISP-003 |  |
| CO-82 | FR-SPM-009 | Tiền tách nghìn bằng khoảng trắng (8 520 000) | EP | TC-DISP-004 |  |
| CO-83 | FR-SPM-009 | Giá trị 950 hiển thị 950 không tách nhóm | BVA | TC-DISP-005 |  |
| CO-84 | FR-SPM-009 | Giá trị gốc ,5 làm tròn half-up ở bước hiển thị | BVA | TC-DISP-006 |  |
| CO-85 | FR-SPM-009;REQ-UI-02 | Mọi số tiền (thẻ, bảng, biểu đồ) có nhãn Sau thuế/Trước thuế | CL | TC-DISP-007 |  |
| CO-86 | REQ-UI-02 | Thẻ KPI tiền hiển thị số đầy đủ, không viết tắt | CL | TC-DISP-008 |  |
| CO-87 | REQ-UI-02 | Thẻ KPI tiền có dòng phụ ghi giá trị cách nhìn thuế còn lại | CL | TC-DISP-009 |  |
| CO-88 | FR-SPM-009;REQ-UI-02 | Đổi thuế không đổi Transactions, Frequency, Coupon %, UPT | EP | TC-DISP-010 |  |
| CO-89 | REQ-UI-02 | Mỗi thẻ có icon i giải thích công thức | CL | TC-DISP-011 |  |
| CO-90 | FR-SPM-009 | Nhãn giải thích Sales/Transactions/Frequency/Avg Spending | CL | TC-DISP-012 |  |
| CO-91 | REQ-UI-04 | Hai nhóm KPI 4 thẻ đúng tên | CL | TC-DISP-013 |  |
| CO-92 | REQ-UI-03 | Kỳ có đơn trả của đơn bán kỳ trước → cảnh báo Cross-period | EP | TC-ALERT-001 |  |
| CO-93 | REQ-UI-03 | Kỳ không có đơn trả cross-period → không có cảnh báo | EP | TC-ALERT-002 |  |
| CO-94 | REQ-UI-03 | Xem Trước thuế, kỳ có đơn VAT = 0 → cảnh báo | DT | TC-ALERT-003 |  |
| CO-95 | REQ-UI-03 | Xem Sau thuế cùng kỳ → không có cảnh báo VAT = 0 | DT | TC-ALERT-004 |  |
| CO-96 | FR-SPM-010 | Tháng này: Ngày tự chọn, cột hôm nay Chưa kết thúc | ST | TC-CHART-001, TC-CHART-006 |  |
| CO-97 | FR-SPM-010 | Kỳ 01/09–30/09/2026 đơn vị Ngày: 30 cột Đủ kỳ, nền T7/CN, nhãn dd/mm | DT | TC-CHART-002 |  |
| CO-98 | FR-SPM-010 | Kỳ 01/09–30/09/2026 đơn vị Tuần: 5 cột, 2 cột Bị cắt, không nền T7/CN | DT | TC-CHART-003 |  |
| CO-99 | FR-SPM-010 | Kỳ 11/10–12/10/2026 (CN–T2) đơn vị Tuần: 2 cột đều Bị cắt, không Chưa kết thúc | DT | TC-CHART-004 |  |
| CO-100 | FR-SPM-010 | Kỳ 74 ngày kết thúc hôm nay: Tuần tự chọn, tuần cuối vừa cắt vừa chưa kết thúc → sọc | DT | TC-CHART-005 |  |
| CO-101 | FR-SPM-010 | Kỳ 1 ngày: không vẽ, thông báo nguyên văn, 3 nút khoá | BVA | TC-CHART-007 |  |
| CO-102 | FR-SPM-010 | Kỳ 31 ngày → tự chọn Ngày | BVA | TC-CHART-013 |  |
| CO-103 | FR-SPM-010 | Kỳ 32 ngày → tự chọn Tuần; Ngày vẫn bấm được | BVA | TC-CHART-014 |  |
| CO-104 | FR-SPM-010 | Kỳ 120 ngày → tự chọn Tuần | BVA | TC-CHART-015 |  |
| CO-105 | FR-SPM-010 | Kỳ 121 ngày → tự chọn Tháng | BVA | TC-CHART-016 |  |
| CO-106 | FR-SPM-010 | Kỳ 62 ngày → Ngày bấm được (62 cột) | BVA | TC-CHART-017 |  |
| CO-107 | FR-SPM-010 | Kỳ 63 ngày → Ngày bị khoá | BVA | TC-CHART-018 |  |
| CO-108 | FR-SPM-010 | Kỳ chạm 1 tuần lịch, 1 tháng lịch → Tuần, Tháng bị khoá | BVA | TC-CHART-019 |  |
| CO-109 | FR-SPM-010 | Kỳ 366 ngày chạm 53 tuần → Tuần bấm được | BVA | TC-CHART-020 |  |
| CO-110 | FR-SPM-010 | Kỳ 366 ngày chạm 54 tuần → Tuần bị khoá | BVA | TC-CHART-021 |  |
| CO-111 | FR-SPM-010 | Kỳ 2 ngày vắt 2 tháng → Tháng bấm được, Tuần khoá | BVA | TC-CHART-022 |  |
| CO-112 | FR-SPM-010 | Kỳ chạm 13 tháng: Tháng tự chọn, nhãn Tn/yy, cột đầu/cuối Bị cắt | BVA | TC-CHART-023 |  |
| CO-113 | FR-SPM-010 | Bấm đơn vị bị khoá: không đổi, tooltip, nút không ẩn | ST | TC-CHART-011 |  |
| CO-114 | FR-SPM-010 | Bấm tay đơn vị khả dụng → Đã chọn tay, nút active | ST | TC-CHART-003 |  |
| CO-115 | FR-SPM-010 | Đổi kỳ, đơn vị tay vẫn khả dụng → giữ | ST | TC-CHART-009 |  |
| CO-116 | FR-SPM-010 | Đổi kỳ, đơn vị tay bị khoá → về Tự chọn | ST | TC-CHART-008 |  |
| CO-117 | FR-SPM-010 | Chọn tay → kỳ 1 ngày → kỳ dài lại: không nhớ lựa chọn tay | ST | TC-CHART-010 |  |
| CO-118 | FR-SPM-010 | Đổi thuế: giá trị cột đổi, đơn vị & trạng thái giữ | ST | TC-CHART-012 |  |
| CO-119 | FR-SPM-010 | Σ Sales, Σ Transactions bucket = KPI | EP | TC-CHART-047 |  |
| CO-120 | FR-SPM-010 | Đơn trả trừ vào bucket ngày trả, không vào bucket ngày bán | EP | TC-CHART-048 |  |
| CO-121 | FR-SPM-010 | Cột âm màu Error, mọc xuống, trục Y có phần âm | EP | TC-CHART-032 |  |
| CO-122 | FR-SPM-010 | Cột cao nhất (> 0) có viền vàng | EP | TC-CHART-028 |  |
| CO-123 | FR-SPM-010 | Hai cột cao nhất bằng nhau → viền vàng cột đầu | BVA | TC-CHART-029 |  |
| CO-124 | FR-SPM-010 | Mọi cột = 0: không thân cột, không viền vàng | BVA | TC-CHART-030 |  |
| CO-125 | FR-SPM-010 | Cột khác 0 rất nhỏ cao tối thiểu 1px | BVA | TC-CHART-031 |  |
| CO-126 | FR-SPM-010 | 16 cột → có nhãn giá trị cột cao nhất | BVA | TC-CHART-026 |  |
| CO-127 | FR-SPM-010 | 17 cột → không có nhãn giá trị | BVA | TC-CHART-027 |  |
| CO-128 | FR-SPM-010 | Cột âm + Chưa kết thúc → sọc chéo | DT | TC-CHART-036 |  |
| CO-129 | FR-SPM-010 | Cột âm + Bị cắt → đỏ; cột dương Bị cắt → xám | DT | TC-CHART-037 |  |
| CO-130 | FR-SPM-010 | Cột cao nhất đang chạy: sọc chéo + viền vàng liền | DT | TC-CHART-038 |  |
| CO-131 | FR-SPM-010 | Chú giải & ghi chú đơn vị Ngày kỳ đã khép | CL | TC-CHART-039 |  |
| CO-132 | FR-SPM-010 | Chú giải & ghi chú đơn vị Tuần có Bị cắt + Chưa kết thúc | CL | TC-CHART-040 |  |
| CO-133 | FR-SPM-010 | Trục Y thang Tỷ, mốc 0, khoảng chia đẹp | EP | TC-CHART-034 |  |
| CO-134 | FR-SPM-010 | Trục Y thang Tr có phần âm | EP | TC-CHART-033 |  |
| CO-135 | FR-SPM-010 | Trục Y < 1 triệu hiển thị số đầy đủ | EP | TC-CHART-035 |  |
| CO-136 | FR-SPM-010 | Tuần 10 cột → nhãn dd/mm–dd/mm | BVA | TC-CHART-024 |  |
| CO-137 | FR-SPM-010 | Tuần 11 cột → nhãn dd/mm Thứ Hai | BVA | TC-CHART-025 |  |
| CO-138 | FR-SPM-010 | Nhãn dày ẩn xen kẽ, không xoay, ≥11px, cột ẩn nhãn vẫn tooltip | CL | TC-CHART-041 |  |
| CO-139 | FR-SPM-010 | Đổi kích thước cửa sổ: vẽ lại theo chiều rộng thật | EG | TC-CHART-042 |  |
| CO-140 | FR-SPM-010 | Tooltip cột Ngày: dd/mm/yyyy (Thứ), Sales, Transactions, Hoàn trả | CL | TC-CHART-043 |  |
| CO-141 | FR-SPM-010 | Tooltip cột Tuần bị cắt: khoảng ngày đã cắt + nhãn | CL | TC-CHART-044 |  |
| CO-142 | FR-SPM-010 | Tooltip cột Chưa kết thúc có nhãn | CL | TC-CHART-045 |  |
| CO-143 | FR-SPM-010 | Tooltip lật sang trái khi sát mép phải | CL | TC-CHART-046 |  |
| CO-144 | FR-SPM-010;FR-SPM-011 | Biểu đồ theo Store/Client Advisor đang lọc | EP | TC-CHART-049 |  |
| CO-145 | FR-SPM-010 | Bấm vào đơn vị đang được tự chọn | ST |  | Pending - Q-29 |
| CO-146 | FR-SPM-010 | Kỳ chạm 14 tháng lịch | BVA |  | N/A - không tạo được: kỳ tối đa 366 ngày chạm nhiều nhất 13 tháng lịch |
| CO-147 | FR-SPM-011 | CRM: mặc định Toàn Tam Sơn · N store; lọc CA bị khoá | EP | TC-STORE-001 |  |
| CO-148 | FR-SPM-011 | Retail Manager Hermès: mặc định chỉ store Hermès, không thêm được store ngoài | PERM | TC-STORE-002 |  |
| CO-149 | FR-SPM-011 | Chip Brand Hermès → chỉ store Hermès được chọn, nhãn nút | EP | TC-STORE-003 |  |
| CO-150 | FR-SPM-011 | Tìm store theo tên và theo Brand | EP | TC-STORE-004 |  |
| CO-151 | FR-SPM-011 | Không bỏ được store cuối cùng | BVA | TC-STORE-005 |  |
| CO-152 | FR-SPM-011 | Chọn 1 store → nhãn là tên store | EP | TC-STORE-005 |  |
| CO-153 | FR-SPM-011 | Chọn 3 store → nhãn 3 store đã chọn | EP | TC-STORE-006 |  |
| CO-154 | FR-SPM-011 | Nút chọn tất cả và bộ đếm đã chọn / tổng | CL | TC-STORE-007 |  |
| CO-155 | FR-SPM-011 | Thu hẹp ST1 + ST2 → ST1: KPI, biểu đồ, bảng tính lại | EP | TC-STORE-008 |  |
| CO-156 | FR-SPM-011 | 6 store → lọc CA khoá + gợi ý | BVA | TC-STORE-009 |  |
| CO-157 | FR-SPM-011 | 5 store → lọc CA mở, liệt kê CA kèm tên store | BVA | TC-STORE-010 |  |
| CO-158 | FR-SPM-011 | Chọn CA-A → số liệu chỉ bill CA-A đứng tên | EP | TC-STORE-011 |  |
| CO-159 | FR-SPM-011 | Đang lọc CA rồi chọn thêm store vượt 5 | ST |  | Pending - Q-25 |
| CO-160 | FR-SPM-011 | Top 10: hạng 1–10 giảm dần theo Sales, có Brand | EP | TC-RANK-001 |  |
| CO-161 | FR-SPM-011 | Bottom 10: hạng thực N…N−9 tăng dần từ thấp | EP | TC-RANK-002 |  |
| CO-162 | FR-SPM-011 | Xếp hạng theo cách nhìn thuế đang chọn | EP | TC-RANK-003 |  |
| CO-163 | FR-SPM-011 | Store không phát sinh trong kỳ không được xếp hạng | EP | TC-RANK-004 |  |
| CO-164 | FR-SPM-011 | Store Sales âm (chỉ đơn trả) vẫn được xếp hạng ở cuối | EG | TC-RANK-005 |  |
| CO-165 | FR-SPM-011 | 1 store → xếp hạng Client Advisor | EP | TC-RANK-006 |  |
| CO-166 | FR-SPM-011 | Hai store cùng Sales: thứ tự hạng | EG |  | Pending - Q-35 |
| CO-167 | FR-SPM-011 | CRM: tab Theo Store mặc định, trang 1, 15 dòng, từ–đến / tổng | EP | TC-TABLE-001 |  |
| CO-168 | FR-SPM-011 | Đổi 30, 50 dòng/trang | EP | TC-TABLE-002 |  |
| CO-169 | FR-SPM-011 | Trang cuối hiển thị phần còn lại | BVA | TC-TABLE-003 |  |
| CO-170 | FR-SPM-011 | Tìm kiếm: cột # giữ hạng thực | EP | TC-TABLE-004 |  |
| CO-171 | FR-SPM-011 | Tìm kiếm + đổi trang: dòng Tổng không đổi | EP | TC-TABLE-005 |  |
| CO-172 | FR-SPM-011 | Σ Sales, Σ Transactions = Tổng; Σ Total Customers ≥ Tổng | EP | TC-TABLE-006 |  |
| CO-173 | FR-SPM-011 | Sắp xếp theo cột: thứ tự và cột # theo thứ tự sắp xếp | EP | TC-TABLE-007 |  |
| CO-174 | FR-SPM-011 | 1 store → không có tab Theo Store | EP | TC-TABLE-008 |  |
| CO-175 | FR-SPM-011 | Phạm vi 1 Brand → không có tab Theo Brand | EP | TC-TABLE-009 |  |
| CO-176 | FR-SPM-011 | Phạm vi 2 Brand → tab Theo Brand 2 dòng | EP | TC-TABLE-010 |  |
| CO-177 | FR-SPM-011;FR-SPM-009 | Tab Theo Client Advisor: Σ dòng > Tổng, ghi chú | EP | TC-TABLE-011 |  |
| CO-178 | FR-SPM-009 | Bảng store cấp gộp có ghi chú không cộng dồn Avg/Frequency | CL | TC-TABLE-012 |  |
| CO-179 | FR-SPM-011 | Store không phát sinh không có dòng, có ghi chú | EP | TC-TABLE-013 |  |
| CO-180 | FR-SPM-011 | Tìm theo Brand trong tab Theo Store | EP | TC-TABLE-014 |  |
| CO-181 | FR-SPM-011 | Thanh dữ liệu nền cột Sales | CL | TC-TABLE-015 |  |
| CO-182 | FR-SPM-011 | Đổi số dòng/trang khi đang ở trang > 1 thì về trang nào | EG |  | N/A - nguồn không nêu; rủi ro thấp, ghi nhận khi chạy thử thăm dò |
| CO-183 | FR-INC-001 | Bill 2 dòng Hanoia + Hermès: mỗi dòng chia theo Brand của dòng | DT | TC-INC-001 |  |
| CO-184 | FR-INC-002 | Discount 20% < Threshold 100% → đủ điều kiện | EP | TC-INC-002 |  |
| CO-185 | FR-INC-002 | Discount 100% = Threshold 100% → bị loại | BVA | TC-INC-003 |  |
| CO-186 | FR-INC-002 | Threshold 30%, Discount 29.99% → đủ điều kiện | BVA | TC-INC-004 |  |
| CO-187 | FR-INC-002 | Threshold 30%, Discount 30.00% → bị loại | BVA | TC-INC-005 |  |
| CO-188 | FR-INC-002 | 2 dòng cùng Brand X: 15% tính, 40% loại | DT | TC-INC-006 |  |
| CO-189 | FR-INC-002 | 2 dòng khác Brand: A tính, B loại | DT | TC-INC-007 |  |
| CO-190 | FR-INC-002 | Hạ Threshold Brand X không đổi ngưỡng Brand khác | EG | TC-INC-008 |  |
| CO-191 | FR-INC-002;FR-INC-005 | Mọi dòng bị loại → bill không đóng góp Incentive | DT | TC-INC-009 |  |
| CO-192 | FR-INC-003 | Không PIC, 2 CA, dòng đủ điều kiện 10 000 000 → mỗi CA 5 000 000 | DT | TC-INC-010 |  |
| CO-193 | FR-INC-003 | Không PIC, 3 nhân viên → chia đều 1/3 | DT | TC-INC-011 |  |
| CO-194 | FR-INC-003;FR-INC-005 | Khách B2B → Incentive N/A, không cộng vào ai | DT | TC-INC-012 |  |
| CO-195 | FR-INC-003 | Đổi PIC sau khi bill phát sinh → giữ PIC tại thời điểm bill | ST | TC-INC-013 |  |
| CO-196 | FR-INC-003 | Khách có PIC ở store khác store bill → coi như không PIC | DT | TC-INC-014 |  |
| CO-197 | FR-INC-004;FR-INC-003 | Hanoia PIC trên bill + Other CA → 70/30 | DT | TC-INC-015 |  |
| CO-198 | FR-INC-004 | Hanoia PIC không trên bill + Other CA → 0/100 | DT | TC-INC-016 |  |
| CO-199 | FR-INC-004 | Nhóm Kenzo… PIC trên bill + Other CA → 100/0 | DT | TC-INC-017 |  |
| CO-200 | FR-INC-004 | Nhóm Chopard… PIC không trên bill + Other CA → 70/30 | DT | TC-INC-018 |  |
| CO-201 | FR-INC-004 | Nhóm Loewe… PIC trên bill + Other CA → 50/50 | DT | TC-INC-019 |  |
| CO-202 | FR-INC-004 | Nhóm BOSS… PIC không trên bill + Other CA → 0/100 | DT | TC-INC-020 |  |
| CO-203 | FR-INC-004 | Hermès PIC đơn độc → 100% | DT | TC-INC-021 |  |
| CO-204 | FR-INC-004 | Hermès PIC + 2 Other CA → 50/25/25 | DT | TC-INC-022 |  |
| CO-205 | FR-INC-004 | Hanoia PIC + 3 Other CA → 70/10/10/10 | DT | TC-INC-023 |  |
| CO-206 | FR-INC-004 | Brand chưa có dòng cấu hình, PIC đơn độc → 100% | DT | TC-INC-024 |  |
| CO-207 | FR-INC-004 | Bill có PIC: dòng bị loại không chia, dòng khác chia bình thường | DT | TC-INC-025 |  |
| CO-208 | FR-INC-005 | Nhân viên có Incentive từ 3 bill → tổng cộng dồn | EP | TC-INC-026 |  |
| CO-209 | FR-INC-005 | Dòng bị loại không vào tổng của ai trong kỳ | EP | TC-INC-027 |  |
| CO-210 | FR-INC-005 | Bộ lọc kỳ áp dụng cho tổng Incentive | EP | TC-INC-028 |  |
| CO-211 | FR-INC-005 | Drill-down tổng Incentive theo Brand | EP | TC-INC-029 |  |
| CO-212 | NFR-INC-002 | Incentive truy vết về bill/dòng gốc | EP | TC-INC-030 |  |
| CO-213 | NFR-INC-001 | Bill đã tính Incentive bị hoàn trả | ST |  | Pending - Q-20 |
| CO-214 | FR-INC-003;FR-INC-004 | Bill 0 nhân viên / PIC vắng không Other CA | DT |  | Pending - Q-30 |
| CO-215 | FR-INC-004 | Tổ hợp cấu hình Brand ngoài AC | DT |  | Pending - Q-11 |
| CO-216 | REQ-MIG-01 | Record m_rma_id khác null bị bỏ qua | EP | TC-MIG-001 |  |
| CO-217 | REQ-MIG-01 | salerep_ids 2 phần tử → 2 bản ghi hoa hồng | EP | TC-MIG-002 |  |
| CO-218 | REQ-MIG-01 | Giá trị lưu theo dòng đơn, không phải tổng đơn | EP | TC-MIG-003 |  |
| CO-219 | REQ-MIG-01 | Record vi phạm quy tắc | EP |  | Pending - Q-21 |
| CO-220 | NFR-SPM-006 | Đổi thuế < 400ms | EP | TC-NFR-001 |  |
| CO-221 | NFR-SPM-006 | Chọn store / chip Brand < 400ms | EP | TC-NFR-002 |  |
| CO-222 | NFR-SPM-006 | Tìm kiếm, sắp xếp, phân trang bảng < 400ms | EP | TC-NFR-003 |  |
| CO-223 | REQ-UI-07 | Cửa sổ 1280px: bố cục đầy đủ | BVA | TC-NFR-004 |  |
| CO-224 | REQ-UI-07 | Cửa sổ 1279px và 768px: sidebar icon, KPI 2 cột, biểu đồ 1 cột | BVA | TC-NFR-005 |  |
| CO-225 | REQ-UI-07 | Cửa sổ dưới 768px | BVA |  | N/A - nguồn không định nghĩa bố cục dưới 768px |
| CO-226 | REQ-UI-06 | Hover state phần tử bấm được | CL | TC-NFR-006 |  |
| CO-227 | REQ-UI-06 | Focus ring khi Tab | CL | TC-NFR-007 |  |
| CO-228 | REQ-UI-06 | Tooltip khi focus bàn phím | CL | TC-NFR-008 |  |
| CO-229 | FR-SPM-010 | Trạng thái cột phân biệt được khi không có màu | CL | TC-NFR-009 |  |
| CO-230 | FR-SPM-001 | CA là PIC nhưng không đứng tên bill không thấy bill; người đứng tên thấy | DT | TC-SCOPE-020 |  |
| CO-231 | FR-SPM-001;FR-SPM-011 | Store Manager 1 store: nhãn tên store, xếp hạng CA, không tab Store | PERM | TC-SCOPE-021 |  |
| CO-232 | FR-SPM-001 | Biên dưới kỳ: 00:00:00 ngày đầu thuộc, 23:59:59 ngày trước không thuộc | BVA | TC-SCOPE-022 |  |
| CO-233 | FR-SPM-001 | Chưa đăng nhập: không xem được dashboard/API | PERM | TC-SCOPE-023 |  |
| CO-234 | FR-SPM-001 | Nhiều Position phạm vi rời nhau | PERM |  | Pending - Q-36 |
| CO-235 | FR-SPM-001 | KPI khác và bộ lọc ở mức Cá nhân | PERM |  | Pending - Q-40 |
| CO-236 | FR-SPM-002 | tax_total âm → log, số theo ERP | EG | TC-SALES-017 |  |
| CO-237 | REQ-UI-03 | Số đơn trả cross-period trong cảnh báo theo store đang chọn | EP | TC-ALERT-005 |  |
| CO-238 | FR-SPM-010 | Kỳ 32 ngày chạm 2 tháng: Tháng bấm được khi tự chọn Tuần | BVA | TC-CHART-050 |  |
| CO-239 | FR-SPM-010 | Kỳ kết thúc hôm qua, tuần cuối chứa hôm nay → Bị cắt, không sọc | DT | TC-CHART-051 |  |
| CO-240 | FR-SPM-010 | Hoàn trả trong tooltip theo cách nhìn thuế | CL |  | Pending - Q-46 |
| CO-241 | FR-SPM-009 | Half-up số âm ,5 | BVA |  | Pending - Q-43 |
| CO-242 | FR-SPM-009 | Gộp tài khoản khách làm đổi số kỳ cũ | EG |  | Pending - Q-51 |
| CO-243 | FR-SPM-011 | Lọc CA khoá vẫn duyệt CA qua tab bảng | EP | TC-STORE-012 |  |
| CO-244 | FR-SPM-011;FR-SPM-001 | Tab CA ST3: mỗi CA trọn Sales bill, Σ dòng > Tổng | DT | TC-TABLE-016 |  |
| CO-245 | FR-SPM-011 | Chip 1 Brand → không tab Theo Brand | EP | TC-TABLE-017 |  |
| CO-246 | FR-SPM-011 | Đổi thuế khi sắp theo Sales: thứ tự và # tính lại | EP | TC-TABLE-018 |  |
| CO-247 | FR-INC-003 | B2B có PIC trên bill vẫn N/A | DT | TC-INC-031 |  |
| CO-248 | FR-INC-004;FR-INC-001 | PIC vắng, dòng Chopard + dòng BOSS | DT | TC-INC-032 |  |
| CO-249 | FR-INC-002 | Cơ sở thuế Gross/Net, Gross = 0, Discount âm | EP |  | Pending - Q-41 |
| CO-250 | FR-INC-005 | Quyền xem Incentive theo vai trò, chặn API | PERM |  | Pending - Q-42 |
| CO-251 | REQ-UI-01 | F5 khi đang có bộ lọc | EG |  | Pending - Q-27 |
| CO-252 | FR-SPM-009 | Đơn mới đồng bộ từ HUB khi đang mở dashboard | EG |  | Pending - Q-28 |

## 17. Dữ liệu test & setup

> Case tham chiếu bằng `Theo SETUP-xx`. *Trạng thái*: `Sẵn sàng` · `Cần chuẩn bị` · `Chưa rõ cách làm` (case tham chiếu bị **Blocked**).

| Setup_ID | Dữ liệu / trạng thái | Cách tạo (điều khiển) | Cách xác minh (quan sát) | Cách reset | Nguồn dữ liệu | Trạng thái |
|---|---|---|---|---|---|---|
| SETUP-01 | Tài khoản: U-CRM (CRM Team, toàn Tam Sơn); U-RM-HER (Retail Manager Brand Hermès); U-SM12 (Store Manager ST1, ST2; không có ST3); U-SM1 (Store Manager chỉ ST1); U-CA-A, U-CA-B (Client Advisor tại ST1); U-MULTI (Position SM ST1 + Retail Manager Brand BR-1) | Admin gán Position Rule cho tài khoản test (menu Users / cấu hình Position) | Đăng nhập từng tài khoản, mở bộ chọn Store xem danh sách store | Không cần reset (không đổi dữ liệu) | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-02 | Bộ dữ liệu QA trên 3 store test ST1 (Brand BR-1), ST2 (Brand BR-2), ST3 (Brand BR-1) không có giao dịch thật. D là một Thứ Bảy, D+3 ≤ hôm nay − 1, hôm nay − D ≤ 30 (chuẩn bị mất ≥ 5 ngày lịch). Chi tiết đơn ở bảng 17.1 (trừ dòng T — xem SETUP-12) | Tạo đơn trên POS/ERP môi trường test theo đúng ngày trong bảng 17.1; chọn sản phẩm có giá niêm yết (đã gồm VAT) cho ra đúng total. Nếu không đạt đúng total: dùng giá thực tế, ghi lại total và tính lại kỳ vọng theo công thức ở 17.2 trước khi chạy | SETUP-08: truy vấn total, tax_total, trạng thái, ngày hoàn tất, list_employees từng đơn; ghi lại tax_total thực tế để tính expected trước thuế | Không xoá; các case chỉ đọc. Nếu tạo sai: huỷ đơn (VO) và tạo lại ở một ngày D mới | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-03 | Đơn có giá trị header/thời điểm kiểm soát chính xác: đơn hoàn tất 23:50:00 và 00:00:30 (UTC+7); đơn warehouse ecom 1000332; đơn list_employees = []; header bất thường (subtotal = 0, tax_total = 0, total > 0; lệch 1đ/2đ; tax_total > total); đơn 2 thuế suất; đơn total 950; đơn chuyển VO sau khi đã tính; 2 ngày Sales bằng nhau; ngày Sales rất nhỏ | Đẩy payload đơn qua HUB môi trường test hoặc sửa dữ liệu nguồn ERP — tài liệu không mô tả cách làm | SETUP-08 | Xoá/huỷ đơn test qua HUB | Cần dev cung cấp | Chưa rõ cách làm |
| SETUP-04 | Brand Incentive Config: hạ Discount Threshold của 1 Brand test (Brand X) xuống 30%; xem được dòng cấu hình các Brand trong AC | Cập nhật Brand Incentive Config — tài liệu chỉ nói cấu hình ở Excel liên kết, không nói hệ thống nạp cấu hình thế nào | Đọc cấu hình đang áp dụng (màn hình/API/DB) | Trả Threshold Brand X về 100% | Cần dev cung cấp | Chưa rõ cách làm |
| SETUP-05 | Khách B2C có PIC = U-CA-A tại ST1; khách B2C không có PIC; khách B2B (Business Account); khách có PIC ở ST2 nhưng không có PIC ở ST1 | Gán/đổi PIC qua chức năng quản lý PIC (pic-management); tạo khách B2B theo phân loại chuẩn | Xem PIC hiện tại của khách tại store trên trang khách hàng | Gỡ PIC / khôi phục PIC ban đầu | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-06 | Kênh quan sát số Incentive theo nhân viên/kỳ/Brand và theo dòng bill | Chưa có — mockup không có khối Incentive (Q-09) | Màn hình/API/DB do dev chỉ định | - | Cần dev cung cấp | Chưa rõ cách làm |
| SETUP-07 | Môi trường có dữ liệu ~100 store nhiều Brand (UAT / dữ liệu migrate), có Brand Hermès 14 store và Chopard | Xác nhận môi trường với QA lead | Bộ chọn Store hiển thị tổng số store; truy vấn SETUP-08 | Không đổi dữ liệu | Đã có trên môi trường (cần xác nhận) | Cần chuẩn bị |
| SETUP-08 | Truy vấn đối soát: đọc đơn bán/đơn trả (total, tax_total, subtotal, discount_total, trạng thái, ngày hoàn tất, warehouse, list_employees, dòng sản phẩm) theo store và kỳ; log cảnh báo của job tính số | Quyền đọc DB/API đơn hàng Mosaic môi trường test | Chạy truy vấn mẫu cho 1 đơn đã biết | Không đổi dữ liệu | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-09 | Trình duyệt Chrome bản mới, DevTools (Network, Performance, Device toolbar, Rendering → Emulate vision deficiencies) | Có sẵn | - | - | Sẵn sàng | Sẵn sàng |
| SETUP-10 | File JSONL mẫu migrate (mẫu trong tài liệu + biến thể) và công cụ/endpoint import migrate | Chưa có — tài liệu chỉ mô tả định dạng cho bên thứ ba | Bảng hoa hồng nhân viên sau import (DB) | Xoá bản ghi import test | Cần dev cung cấp | Chưa rõ cách làm |
| SETUP-12 | Đơn của ngày chạy T: ST2 OB7 (K8, 1 sp, 50 000 000); ST3 RC-T trả 1 sp của OC1 (2 500 000) | Tạo trên POS ngay ngày chạy test, trước khi chạy case | SETUP-08 | Trước mỗi lần chạy lại: huỷ (VO) OB7 của lần trước; RC-T dùng 1 sp còn lại của OC1 (OC1 còn tối đa 4 sp sau RC1) | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-11 | Bill Incentive trên POS: store test bán được sản phẩm Hanoia, Hermès, Kenzo… ; bill nhiều dòng nhiều Brand, nhiều nhân viên đứng tên, giảm giá theo dòng | Tạo bill trên POS môi trường test, chọn nhân viên đứng tên và giảm giá từng dòng | SETUP-08 (dòng, giá, giảm giá, nhân viên) | Huỷ bill test | Cần chuẩn bị | Cần chuẩn bị |

### 17.1 Bộ dữ liệu QA theo SETUP-02 (tạo trên POS, đơn hoàn tất đúng ngày)

D = một Thứ Bảy; D−1 Thứ Sáu; D+1 Chủ Nhật; D+2 Thứ Hai; D+3 Thứ Ba; T = ngày chạy test. Giá là total (đã gồm VAT). Khách K1–K13 là khách test, K7 = tài khoản Khách lẻ dùng chung. ST1, ST3 thuộc Brand BR-1; ST2 thuộc BR-2.

| Ngày | Store | Đơn | Khách | Số lượng / dòng | Total | Coupon | Đứng tên | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| D−1 | ST1 | O0 | K5 | 2 sp | 3 200 000 | – | CA-B | Đơn gốc của R2 |
| D | ST1 | O1 | K1 | 2 sp | 12 525 500 | – | CA-A | |
| D | ST1 | O2 | K2 | 2 sp | 10 000 000 | 3 mã | CA-A, CA-B | Bill chung |
| D | ST1 | O3 | K3 | 3 sp | 9 474 500 | – (giảm giá chương trình không mã) | CA-B | |
| D | ST1 | O5 | K7 | 1 sp | 8 000 000 | – | CA-A | Khách lẻ |
| D | ST1 | O6 | K2 | 2 sp | 8 000 000 | 1 mã | CA-A | |
| D | ST1 | O7 | K1 | 1 sp | 3 000 000 | – | CA-A | Huỷ → VO |
| D | ST1 | O8 | K3 | 1 sp | 2 000 000 | – | CA-B | Để chưa hoàn tất (nháp/đang xử lý) |
| D | ST1 | R1 | K3 | trả 1 sp của O3 | 5 400 000 | | | Đơn trả cùng kỳ |
| D+1 | ST1 | R2 | K5 | trả 1 sp của O0 | 1 600 000 | | | Cross-period |
| D+1 | ST1 | R3 | K2 | trả 1 sp của O2 | 5 000 000 | | | Cross-period |
| D+2 | ST1 | O10, O11, O12 | K7 | 1 sp mỗi đơn | 1 000 000 mỗi đơn | – | CA-A | |
| D+2 | ST1 | O13 | K1 | 1 sp | 2 000 000 | – | CA-A | |
| D | ST2 | OB1 | K1 | 1 sp | 4 000 000 | – | CA-C | K1 mua cả ST1 và ST2 |
| D | ST2 | OB2 + RB2 | K9 | 2 sp, trả toàn bộ cùng ngày | 6 000 000 | 1 mã | CA-C | |
| D+1 | ST2 | OB3 | K8 | 3 sp | 4 000 000 | – | CA-C | |
| D+1 | ST2 | RB3 | K1 | trả toàn bộ OB1 (1 sp) | 4 000 000 | | | |
| D+2 | ST2 | OB4 | K8 | 1 sp | 1 000 000 | – | CA-C | |
| D+2 | ST2 | RB4 | K8 | trả toàn bộ OB3 (3 sp) | 4 000 000 | | | |
| D+3 | ST2 | OB5 | K11 | 1 sp | 0 | coupon giảm 100% | CA-C | Đơn 0đ |
| D+3 | ST2 | OB6 | K8 | 3 sp | 2 000 000 | – | CA-C | |
| D | ST3 | OC1 | K10 | 6 dòng × 1 sp | 15 000 000 | – | CA-D, CA-E, CA-F | |
| D | ST3 | OC2 | K10 | 3 dòng (2 + 1 + 1 sp) + 1 dòng phí ship (1051644, SL 1) | 10 000 000 | – | CA-D | |
| D+1 | ST3 | OC3 | K12 | 3 sp + 1 dòng dịch vụ khắc tên SL 2 | 6 000 000 | – | CA-D | |
| D+1 | ST3 | OC4 | K12 | 1 sp | 1 000 000 | 1 mã | CA-D | |
| D+1 | ST3 | OC5 | K13 | 1 sp | 1 000 000 | 1 mã | CA-D | |
| D+2 | ST3 | OC6 | K12 | 1 sp | 2 000 000 | – | CA-D | |
| D+2 | ST3 | RC1 | K10 | trả 1 sp của OC1 | 2 500 000 | | | Khách chỉ có đơn trả trong ngày |
| T (SETUP-12) | ST2 | OB7 | K8 | 1 sp | 50 000 000 | – | CA-C | Cột cao nhất đang chạy |
| T (SETUP-12) | ST3 | RC-T | K10 | trả 1 sp của OC1 | 2 500 000 | | | Cột âm đang chạy |

### 17.2 Kết quả kỳ vọng tính sẵn (Sau thuế)

| Phạm vi · kỳ | Sales | Transactions | Total Customers | Coupon % | AOV | UPT | Frequency | Avg Spending |
|---|---|---|---|---|---|---|---|---|
| ST1 · D | 42 600 000 | 5 | 4 | 40.0% | 8 520 000 | 1.80 | 1.25 | 10 650 000 |
| ST1 · D+1 | −6 600 000 | 0 | 0 (AS-06) | — | — | — | — | — |
| ST1 · D+2 | 5 000 000 | 4 | 2 | 0.0% | 1 250 000 | 1.00 | 2.00 | 2 500 000 |
| ST2 · D | 4 000 000 | 2 | 2 | 50.0% | 2 000 000 | 0.50 | 1.00 | 2 000 000 |
| ST2 · D+1 | 0 | 1 | 1 (AS-06) | 0.0% | 0 | 2.00 | 1.00 | 0 |
| ST2 · D+2 | −3 000 000 | 1 | 1 | 0.0% | −3 000 000 | −2.00 | 1.00 | −3 000 000 |
| ST2 · D+3 (AS-01) | 2 000 000 | 2 | 2 | 50.0% | 1 000 000 | 2.00 | 1.00 | 1 000 000 |
| ST3 · D | 25 000 000 | 2 | 1 | 0.0% | 12 500 000 | 5.00 | 2.00 | 25 000 000 |
| ST3 · D+1 | 8 000 000 | 3 | 2 | 66.7% | 2 666 667 | 1.67 (Q-17) | 1.50 | 4 000 000 |
| ST3 · D+2 | −500 000 | 1 | 1 (AS-06) | 0.0% | −500 000 | 0.00 | 1.00 | −500 000 |
| ST1 + ST2 · D | 46 600 000 | 7 | 5 | 42.9% | 6 657 143 | 1.43 | 1.40 | 9 320 000 |
| CA-A · D | (Q-31) | 4 | (Q-40) | 50.0% (Q-40) | (Q-40) | (Q-40) | (Q-40) | (Q-40) |
| CA-B · D | (Q-31) | 2 | (Q-40) | 50.0% (Q-40) | (Q-40) | (Q-40) | (Q-40) | (Q-40) |

Giá trị Trước thuế: lấy tax_total thực tế của từng đơn qua SETUP-08 rồi tính theo FR-SPM-002 (POS không cho đặt tax_total tuỳ ý).
