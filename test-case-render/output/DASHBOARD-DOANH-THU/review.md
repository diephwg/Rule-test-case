# Review bộ test case — DASHBOARD-DOANH-THU

| Thông tin | Giá trị |
|---|---|
| Người review | AI agent (Claude) — phản biện độc lập, không chung ngữ cảnh với người sinh |
| Ngày | 2026-10-18 |
| Bộ được review | `output/DASHBOARD-DOANH-THU/testcases.csv` (218 case, v1.0) + `analysis.md` v1.0 |
| Nguồn đối chiếu | `_extracted/Tài liệu dashboard doanh thu đơn hàng.docx.md` (đọc toàn bộ 1 378 dòng) + mockup image1–3 (xem trực tiếp) |
| Thứ tự đọc | Nguồn + mockup trước → tự tách mệnh đề, tự tính lại ví dụ → sau đó mới đọc `analysis.md`, `testcases.csv` |
| Bảng ánh xạ cột | Không cần — CSV đúng 15 cột chuẩn của `templates/testcases-template.csv` |

## 1. Tóm tắt

**Kết quả chính:** bộ test có cấu trúc và truy vết tốt (validator 0 ERROR · 0 WARNING). Mọi con số trong bảng 17.2 và trong các case tính trên SETUP-02 đều đúng khi tính lại (mục 5). Tuy vậy review tìm thấy **2 lỗi Critical**: một expected suy diễn ngược với câu chữ của nguồn, và một expected phụ thuộc giả định AS-03 nhưng không được đánh dấu. Ngoài ra có **14 lỗi Major**: các nhánh nguồn chưa có case (CA không phụ thuộc PIC, vai trò 1 store, B2B có PIC, quyền xem Incentive…), các phụ thuộc chưa đánh dấu, một lỗi trong ví dụ trục Y, và ràng buộc ngày của SETUP-02 cho phép dữ liệu chồng nhau làm sai 7 case.

| Chỉ số (rules/05 §Chỉ số) | Theo validator | Ghi chú của reviewer |
|---|---|---|
| 1. Req_ID có case | 26/26 (N/A 1) | Đồng ý |
| 2. Mệnh đề nguồn có case · có case Ready | 202/202 · Ready 128/202 (N/A 1, Pending 7) | Mẫu số thiếu ít nhất 3 mệnh đề (R-08 tách FR-SPM-001-c1; R-11; R-31). Phần Sales của AC-SPM-001-04 chưa có case (R-12). Theo mẫu số của reviewer: **≈ 201/205** |
| 3. Điều kiện kiểm thử có case | 219/219 (N/A 3, Pending 9) | Mẫu số do người thiết kế đặt — khi lệch thì tin chỉ số 2 |
| 4. Theo kỹ thuật / IX / EV | BVA 37/37 · CL 21/21 · DT 38/38 · EG 9/9 · EP 96/96 · PERM 9/9 · ST 9/9; IX 28 dòng (Pending 1); EV 21 dòng (N/A 3, Pending 4) | Thiếu các dòng IX/EV/ST nêu ở R-27, R-28 và R-05 |
| 5. Phần đang chờ | Ready 134 · Needs Clarification 29 · Blocked 55; Q mở 35; AS 9; SETUP *Chưa rõ cách làm*: 03, 04, 06, 10 | Có **5 case đang tính Ready** nhưng mang phụ thuộc chưa đánh dấu (TC-SCOPE-006, TC-CHART-037, TC-FLT-007, TC-TABLE-008, TC-CHART-026). TC-CHART-033 có expected sai. 7 case ở R-03 có thể sai do dữ liệu chồng nhau |

**Mức sẵn sàng:** *Bản nháp dùng được, chưa đạt Definition of Done.* Phải xử lý 2 Critical và 14 Major (đặc biệt R-01…R-05, R-16) trước khi coi 134 case Ready là đã có oracle xác nhận.

| Mức | Số phát hiện |
|---|---|
| Critical | 2 |
| Major | 14 |
| Minor | 16 |
| Suggestion | 3 |
| **Tổng** | **35** |

**Top 5 cần xử lý trước**
1. **R-01 (Critical)** — TC-SCOPE-006 kỳ vọng phạm vi là *hợp* các Position. Nguồn ghi "lấy **phạm vi lớn nhất** Position được cấp" (FR-SPM-001).
2. **R-02 (Critical)** — TC-CHART-037 kỳ vọng tuần chứa D+2 là "xám Bị cắt". SETUP-02 cho phép tuần đó chứa hôm nay, và khi đó BR-SPM-017 (FRD) cho kết quả "Chưa kết thúc". Case không gắn [Giả định AS-03].
3. **R-03 (Major)** — ràng buộc ngày của SETUP-02 (`D+2 ≤ hôm nay − 1`) cho phép T = D+3. Khi đó OB7 (50 000 000, ngày T, ST2) rơi vào cùng ngày với OB5/OB6, làm sai 7 case ST2 · D+3.
4. **R-04 (Major)** — TC-FLT-007 (Ready) và TC-SCOPE-005 đối soát Transactions/Sales thật với truy vấn "số đơn bán hợp lệ". Dữ liệu thật có đơn 0đ (mockup: "93 đơn 0đ không tính") và đơn B2B, nên kết quả phụ thuộc Q-01 và Q-16 mà case không đánh dấu.
5. **R-08 / R-13 / R-15 (Major)** — các nhánh nguồn chưa có case: CA *không phụ thuộc PIC*, B2B có PIC trên bill, và quyền xem Incentive theo vai trò.

## 2. Kết quả validator

- `testcases.csv` + `analysis.md`: **0 ERROR · 0 WARNING**. Chỉ xác nhận cấu trúc và truy vết.
- `testcases-additional.csv`:
  - Chạy riêng, không kèm analysis: 0 ERROR · 0 WARNING (cấu trúc).
  - Ghép với bộ gốc rồi chạy cùng `--analysis --previous`: **2 ERROR · 12 WARNING**, đều do review mới đề xuất:
    - 2 ERROR: Q-37, Q-38 là câu hỏi mới, chưa có trong `analysis.md`.
    - 11 WARNING: case mới chưa có dòng CO.
    - 1 WARNING: TC-CHART-051 chưa nằm trong danh sách *Case bị ảnh hưởng* của AS-03.
  - Các lỗi này hết khi người sinh nhận đề xuất và cập nhật `analysis.md` (thêm Q-36…Q-50, CO, AS-03). Reviewer không sửa `analysis.md` theo đúng phạm vi được giao.

## 3. Bảng phát hiện

| ID | TC_ID / CO / Req_ID | Mức | Vấn đề | Căn cứ | Đề xuất sửa |
|---|---|---|---|---|---|
| R-01 | TC-SCOPE-006 · CO-18 · FR-SPM-001-c5 | Critical | Expected "Danh sách gồm ST1 và toàn bộ store của Brand BR-2 (**hợp** các Position)" là suy diễn. U-MULTI có 2 phạm vi rời nhau (SM ST1 thuộc BR-1; RM BR-2). Nguồn nói lấy phạm vi *lớn nhất*, tức là chọn một phạm vi, không phải hợp. Case đang tính Ready. | FR-SPM-001: "Quy tắc chọn mức: lấy **phạm vi lớn nhất Position được cấp**; người xem chỉ thu hẹp, không mở rộng" | Tạo **Q-36** (phạm vi lớn nhất hay hợp khi các Position rời nhau? "lớn nhất" đo theo mức hay theo số store?). Đặt AS + gắn `[Giả định AS-xx]` vào TC-SCOPE-006. Thêm biến thể Position lồng nhau (SM ST1 + RM BR-1 chứa ST1) để có case Ready theo đúng câu chữ |
| R-02 | TC-CHART-037 · CO-129 · DT1-R2 | Critical | Đơn vị Tuần, kỳ D+1–D+2. Cột tuần chứa D+2 (Thứ Hai D+2 … Chủ Nhật D+8) **chứa hôm nay** khi T ∈ [D+3, D+8], và SETUP-02 cho phép điều này (D+2 ≤ T−1, T−D ≤ 30). Khi đó PRD → xám, BR-SPM-017 → "Chưa kết thúc" (sọc). Expected "màu xám Bị cắt" được viết như yêu cầu, không gắn marker. Case đang tính Ready | BR-SPM-017: "Bucket chứa hôm nay (kể cả bucket Ngày…)"; PRD mục 4: "và kỳ lọc kéo tới hôm nay"; Q-03/AS-03 | Gắn `[Giả định AS-03]` và thêm TC-CHART-037 vào AS-03. Hoặc thêm precondition T ≥ D+9 để cột cuối không chứa hôm nay. Bổ sung TC-CHART-051 (ngày tương đối) để kiểm AS-03 có chủ đích |
| R-03 | SETUP-02 / bảng 17.1 · TC-TRX-004, TC-FREQ-005, TC-CPN-002, TC-AOV-007, TC-UPT-004, TC-AVGS-005, TC-SALES-006, TC-CHART-038 | Major | (1) Ràng buộc `D+2 ≤ hôm nay − 1` cho phép **T = D+3**. Khi đó OB7 (ST2, 50 000 000, K8, ngày T) cùng ngày với OB5/OB6, nên ST2 · D+3 thành Sales 52 000 000, Transactions 3, Coupon 33.3%, AOV 17 333 333, UPT 1.67, Frequency 1.50, Avg 26 000 000. 7 case kỳ D+3 sai. (2) OB7, RC-T phải tạo vào **chính ngày chạy**. Chạy lại vào ngày khác thì OB7 cũ (50 000 000) vẫn nằm trong kỳ "D – hôm nay", nên TC-CHART-038 có thể không còn cột hôm nay là cao nhất. SETUP-02 ghi "Không xoá; các case chỉ đọc" nhưng không có cách reset cho dòng T | Bảng 17.1, cột SETUP-02 "Cách reset" | Sửa ràng buộc thành **D+3 ≤ hôm nay − 1**. Tách OB7/RC-T thành SETUP riêng, có cách reset: huỷ (VO) OB7/RC-T cũ trước khi tạo mới, hoặc dùng store test ST4 riêng cho mỗi lần chạy |
| R-04 | TC-FLT-007 (Ready), TC-SCOPE-005 · CO-07, CO-17 | Major | Expected "Sales và Transactions bằng kết quả truy vấn SETUP-08" / "Transactions = số đơn bán hợp lệ". Truy vấn phải chọn có tính đơn 0đ (Q-01), đơn B2B (Q-16), đơn ecom (Q-14) hay không. Mockup cho thấy dữ liệu thật **có** đơn 0đ ("93 đơn 0đ không tính"). TC-FLT-007 không có marker nào. TC-SCOPE-005 chỉ có AS-09 | FR-SPM-003 (mâu thuẫn net_amount > 0 / BR-SPM-006); OQ-SPM-05; mockup image2/3 thẻ Transactions | Gắn `[Giả định AS-01]`, `[Cần xác nhận Q-16]` (và `[Giả định AS-09]` cho TC-FLT-007). Ghi rõ điều kiện WHERE của truy vấn ở SETUP-08. Hoặc chuyển TC-FLT-007 sang dữ liệu SETUP-02 (không có 0đ/B2B) để thành Ready thật |
| R-05 | TC-TABLE-008 (Ready), TC-STORE-003 · CO-175 · FR-SPM-011-c14 | Major | "Tab Brand chỉ khi **phạm vi** có > 1 Brand": chưa rõ phạm vi là Position hay tập store đang chọn. AC-SPM-011-11 dùng phạm vi Position (RM Hermès). Mockup image2 (đang chọn Brand Hermès) **không có** tab Theo Brand, tức hiểu theo tập đang chọn. TC-TABLE-008 khẳng định ẩn tab Theo Brand khi U-SM12 (Position 2 Brand) chọn riêng ST1, nhưng không gắn marker. Chưa có case CRM chọn chip 1 Brand | BR-SPM-023; AC-SPM-011-11; image2 | Tạo **Q-37**. Gắn marker cho phần "không có tab Theo Brand" của TC-TABLE-008. Thêm dòng IX "tập store đang chọn × tab Brand". Bổ sung TC-TABLE-017 |
| R-06 | CO-100, CO-103…105 · TC-CHART-005, 014, 015 · Q-02 | Major | Ví dụ đối chiếu của nguồn có lỗi mà Q-02 chưa nêu. Dòng *Custom 02/08–14/10*: kỳ chạm **12** tuần lịch (27/07 … 12/10), không phải "11 cột"; kỳ chạm 3 tháng lịch (T8, T9, T10) nên Tháng phải **bấm được**, nhưng cột "Bấm được" chỉ ghi "Ngày, Tuần". Không case nào kiểm tra Tháng bấm được trong dải tự chọn Tuần (32–120 ngày). Dev làm theo bảng ví dụ sẽ khoá sai nút Tháng mà không bị phát hiện | PRD Logic hiển thị mục 3 Bước 1 (Tháng: 2 → 13 tháng lịch) và mục 8 (ví dụ đối chiếu); tự tính: 12/10 − 27/07 = 77 ngày = 11 khoảng tuần → 12 cột | Tạo **Q-38**. Bổ sung TC-CHART-050 (32 ngày, Tháng bấm được). Thêm assert số cột tuần vào TC-CHART-005 (số tuần lịch kỳ chạm tới, tính theo ngày chạy) |
| R-07 | TC-CHART-033 · CO-134 | Major | Ví dụ trong expected "−10 Tr, 0, 10 Tr … 50 Tr" cho **6 khoảng chia**, mâu thuẫn với "khoảng 4–5 khoảng chia" ngay trong cùng expected. Với dải −6 600 000 … 42 600 000, bước "đẹp" phù hợp là 20 Tr (−20, 0, 20, 40, 60 = 4 khoảng). Nguồn cũng tự mâu thuẫn: PRD "4–5 khoảng chia", BR-SPM-018 "khoảng 4 mốc" (= 3 khoảng). Chưa có Q | PRD mục 6 Trục; BR-SPM-018 | Tạo **Q-39**. Bỏ ví dụ 10 Tr hoặc sửa thành bộ mốc thoả 4–5 khoảng. Assert theo quy tắc (bội 1/2/2.5/5×10ⁿ, có 0, số khoảng chia trong miền đã chốt) |
| R-08 | FR-SPM-001-c1 · CO-15 · TC-SCOPE-003 | Major | Mệnh đề c1 gộp 2 khẳng định độc lập: "không giới hạn theo PIC" và "không thấy số của người khác". Case chỉ kiểm tra vế sau. Chưa có case CA là PIC của khách nhưng không đứng tên bill (không được thấy), và ngược lại. Nguồn nhấn mạnh tính độc lập với PIC 3 lần | PRD Phạm vi theo vai trò "(…không phụ thuộc PIC)"; FR-SPM-001 bảng mức Cá nhân; BR-SPM-002; Assumptions PRD dòng 26–28 | Tách c1 thành c1a/c1b. Bổ sung TC-SCOPE-020 |
| R-09 | FR-SPM-001 bảng mức phạm vi · SETUP-01 · ma trận phân quyền §10 | Major | Mức "**1 store** (Store Manager 1 store)" là một phân vùng vai trò của nguồn, nhưng SETUP-01 không có tài khoản này và §10 không có cột riêng. Trạng thái mặc định (nhãn tên store, không bỏ được, xếp hạng CA, không tab Store, lọc CA mở) chỉ được kiểm gián tiếp bằng thao tác thu hẹp của U-SM12 | FR-SPM-001 dòng "1 store"; BR-SPM-020…023 | Thêm U-SM1 vào SETUP-01 và cột vào §10. Bổ sung TC-SCOPE-021 |
| R-10 | Bảng 17.2 dòng CA-A/CA-B · TC-SCOPE-003 · REQ-UI-05 | Major | Ở mức Cá nhân, nguồn chỉ nói bill được tính trọn vào "Sales/Transactions/UPT". Total Customers, Frequency, Coupon %, AOV, Avg Spending của CA chưa định nghĩa (FR-CSD-002 theo phạm vi nào?). Bảng 17.2 để "–" mà không có Q. TC-SCOPE-003 khẳng định "không có bộ chọn store mở rộng" mà không có nguồn | BR-SPM-002; FR-SPM-004/008 (mẫu số "cùng phạm vi") | Tạo **Q-40** (8 thẻ KPI và bộ lọc Store/CA hiển thị gì ở mức Cá nhân). Thêm Pending CO. Gắn `[Cần xác nhận Q-40]` vào phần bộ chọn store của TC-SCOPE-003 |
| R-11 | BR-SPM-021 · FR-SPM-011-c8 · TC-STORE-009 | Major | Thiếu mệnh đề: "Người xem vẫn duyệt được Client Advisor qua tab 'Theo Client Advisor' của bảng" khi lọc CA bị khoá (> 5 store). Bảng *Mệnh đề nguồn* không có, không có case | BR-SPM-021 câu cuối | Thêm mệnh đề FR-SPM-011-c23 + CO. Bổ sung TC-STORE-012 |
| R-12 | FR-SPM-001-c13 · CO-16 · TC-SCOPE-004 | Major | AC-SPM-001-04 có 2 vế: "Mỗi người thấy trọn giá trị bill; **Sales A + Sales B > Sales store**". Case chỉ kiểm Transactions với lý do Sales phụ thuộc Q-31 (gán đơn trả). Nhưng SETUP-02 có sẵn dữ liệu không có đơn trả (ST3 ngày D: OC1 3 CA, OC2 CA-D), nên vế Sales kiểm được mà không phụ thuộc Q-31 | AC-SPM-001-04; BR-SPM-002; bảng 17.1 | Tách c13 thành c13a (trọn bill) và c13b (tổng Sales). Bổ sung TC-TABLE-016 (CA-D 25 000 000; CA-E, CA-F 15 000 000; Tổng 25 000 000) |
| R-13 | DT3-R1 · CO-194 · TC-INC-012 | Major | DT3-R1 gộp cột "PIC trên bill = –" cho B2B mà **không chứng minh** hành vi không đổi. Sơ đồ luồng bước 3 chỉ rẽ theo "Customer có PIC tại store?" và không có nhánh B2B, nên rủi ro hiện thực B2B có PIC đi nhánh FR-INC-004 là thật. TC-INC-012 không nêu PIC của khách B2B | FR-INC-003 Xử lý (B2B → N/A "áp dụng cho mọi Brand"); sơ đồ §2 FRD Incentive; rules/02 §DT mục 5 | Thêm rule DT3-R1b (B2B + có PIC trên bill). Bổ sung TC-INC-031 |
| R-14 | FR-INC-002 · CO-184…187 · TC-INC-004, TC-INC-005 · Q-12 | Major | Discount % = (Gross − Net) ÷ Gross. Gross là "giá gốc trước giảm giá", Net là "thực thu" (theo FRD Sales thì có gồm VAT?). Nếu khác cơ sở thuế thì Discount % lệch khoảng 8–10 điểm, nên biên 29.99% / 30.00% của TC-INC-004/005 không tạo được có kiểm soát trên POS. Gross = 0 nằm trong Q-12 nhưng không có Pending CO. Discount âm (Net > Gross) chưa xét. TC-INC-005 không gắn Q nào về cơ sở tính | FR-INC-002 Input; FRD Sales: net_amount gồm VAT | Tạo **Q-41** (cơ sở thuế của Gross/Net; Gross = 0; Discount < 0). Thêm Pending CO. Gắn `[Cần xác nhận Q-41]` vào TC-INC-004…007, TC-INC-009, TC-INC-010, TC-INC-025, TC-INC-027 |
| R-15 | REQ-BSP-01 · FR-INC-005 · §10 ma trận phân quyền | Major | Ai được xem Incentive của ai (CRM, RM, SM, CA xem của mình?) chưa được phân tích. §10 không có hàng Incentive, Q-09 chỉ hỏi vị trí hiển thị. Đây là số tiền thưởng cá nhân, rủi ro lộ dữ liệu cao. Chưa có case chặn qua API | User story REQ-BSP-01 ("Là SM/Retail Manager"); BR-SPM-001 (không UI nào lộ số của nhân viên ngoài phạm vi) | Tạo **Q-42**. Thêm hàng Incentive vào §10 và CO PERM. Ít nhất Pending CO, và CO chặn API cho CA xem Incentive người khác |
| R-16 | SETUP-02 (trạng thái *Cần chuẩn bị*) · khoảng 60 case dùng bộ ST1/ST2/ST3 | Major | Bộ dữ liệu yêu cầu total chính xác (12 525 500; 9 474 500; R1 trả 1 sp = 5 400 000…), nhưng tạo trên POS thì total do giá sản phẩm + VAT quyết định, khoản hoàn do ERP tính. SETUP không chỉ định sản phẩm/giá nào cho ra các total đó. Đơn phải hoàn tất đúng các ngày D−1…D+3 thật (không lùi ngày), nên chuẩn bị mất ≥ 5 ngày lịch. Trạng thái "Cần chuẩn bị" (tester tự làm được) không khớp thực tế | rules/03 §Tái tạo được; rules/01 Bước 3.7 | Bổ sung bảng sản phẩm test/giá/VAT cho từng đơn hoặc dùng SETUP-03 (đẩy payload). Nếu chưa có thì hạ trạng thái xuống *Chưa rõ cách làm*. Cho phép expected tính từ total thực tế lấy qua SETUP-08 (như đã làm với tax_total) |
| R-17 | FR-SPM-009 · CO-84 · TC-DISP-006 | Minor | Half-up với số âm (AOV/Avg Spending âm có phần lẻ ,5: −1 250 000.5 → −1 250 001 hay −1 250 000?) chưa có Q/case. TC-DISP-006 chỉ kiểm số dương | FR-SPM-009 (half-up; số âm giữ dấu) | Tạo **Q-43**. Thêm case BVA sau khi có trả lời |
| R-18 | FR-SPM-001-c11 · CO-23, CO-24 | Minor | BVA kỳ chỉ có biên trên (23:50 ngày cuối; 00:00:30 ngày sau). Thiếu biên dưới (00:00:00 ngày đầu thuộc kỳ; 23:59:59 ngày trước không thuộc). Giá trị 23:50 cũng không phải điểm biên (23:59:59) | FR-SPM-001 Xác định kỳ | Bổ sung TC-SCOPE-022. Cân nhắc đổi 23:50 → 23:59:59 |
| R-19 | FR-SPM-002-c13 · CO-44…46 | Minor | Mệnh đề nêu "tax_total **âm** hay lớn hơn total" nhưng chỉ có CO cho "lớn hơn total". Phân vùng âm chưa có case | BR-SPM-014 gạch "Kiểm tra chéo" | Thêm CO. Bổ sung TC-SALES-017 |
| R-20 | TC-CHART-026 (Ready) | Minor | Expected "nhãn giá trị (dạng rút gọn như trục, ví dụ 29 Tỷ)" lấy từ mockup. Nguồn không nêu định dạng, còn PRD nói trục Y "chỉ rút gọn ở nhãn trục; số đầy đủ nằm ở tooltip và thẻ KPI". Đây là giả định ngầm, không có marker | PRD mục 5–6; image2/3 | Tạo **Q-44** và gắn marker. Hoặc chỉ assert "có nhãn giá trị" |
| R-21 | TC-CHART-004 | Minor | Precondition "Hôm nay ≥ 13/10/2026" với kỳ cố định 11/10–12/10: Q-03 chỉ bộc lộ khi hôm nay nằm trong 12/10–18/10. Hôm nay là 18/10/2026 nên từ ngày mai case không còn kiểm AS-03 (luôn pass theo cả hai cách hiểu) | Q-03/AS-03 | Chuyển sang ngày tương đối (xem TC-CHART-051) |
| R-22 | TC-FLT-007 | Minor | Expected "không preset nào ở trạng thái đang chọn trừ khi trùng Tháng trước" không xác định: kỳ 01/09–30/09/2026 **chính là** Tháng trước vào tháng 10/2026. Nguồn không nói nút preset có sáng khi khoảng Custom trùng preset | PRD khối 1 | Tạo **Q-45**. Tạm thời bỏ assert này |
| R-23 | FR-SPM-010-c35 · CO-118, CO-140 · TC-CHART-012 | Minor | Tooltip "Hoàn trả đã trừ" khi xem Trước thuế: hiển thị khoản hoàn trước thuế hay sau thuế? Nguồn không nói. TC-CHART-012 chỉ kiểm Sales | PRD mục 7; BR-SPM-019 | Tạo **Q-46**. Thêm assert sau khi có trả lời |
| R-24 | Q-01 · AS-01 · §12 Quan sát UI | Minor | Mockup image2/3, dòng phụ thẻ TRANSACTIONS ghi "**93 đơn 0đ không tính**" — bằng chứng trực tiếp ngược với AS-01 và với nhãn bắt buộc "gồm đơn 0đ". §12 không ghi các dòng phụ KPI (UPT "10 689 sản phẩm / 4 531 đơn", Coupon "1 017 / 4 531 giao dịch"…), và Q-01 không dẫn bằng chứng này | image2, image3 | Bổ sung vào Q-01 và §12; nêu cho BA khi hỏi Q-01 (Blocker) |
| R-25 | §12 · TC-CHART-034, TC-DISP-008 | Minor | Mockup có số liệu không nhất quán: image2 đang chọn "Brand Hermès (2 store)" nhưng KPI và xếp hạng vẫn là số 100 store, có store Patek/Chopard. Ở image3 tab Theo Brand, Σ Sales 10 dòng = 301 872 754 000 ≠ dòng Tổng 301 852 754 000 (lệch 20 000 000), trong khi Σ Transactions = 4 531 khớp. Phân trang 1/7 trong khi chỉ có 10 Brand. TC-CHART-034 (trục "0, 10 Tỷ, 20 Tỷ, 30 Tỷ") và TC-DISP-008 (ví dụ 301 852 754 000) lấy giá trị mockup làm kỳ vọng cho dữ liệu thật | image2, image3 (tự cộng lại) | Ghi chú mockup không dùng làm oracle cho số liệu. Đổi expected TC-CHART-034 thành quy tắc thay vì giá trị cụ thể |
| R-26 | REQ-UI-01 · CO-01…06 | Minor | PRD Assumptions ghi "Kế thừa bộ lọc thời gian chung (**Day/Week/Month/Custom**)…", nhưng khối 1 có 5 preset khác (Hôm nay / Tuần này / Tháng này / Tháng trước / Năm này). FR-SPM-001 dẫn OQ-SPM-09. Chưa có Q | PRD Assumptions dòng 24; FR-SPM-001 Xác định kỳ | Tạo **Q-47** |
| R-27 | §8.1 ma trận trạng thái · §9b EV | Minor | Ma trận trạng thái đơn vị biểu đồ thiếu cột sự kiện "Đổi Store / Client Advisor" (kỳ không đổi → kỳ vọng Không đổi) và "Tải lại F5" (Q-27). Bảng EV thiếu nút Back, tab/phiên thứ hai, URL có tham số lọc | rules/02 §ST; rules/04 §B | Thêm cột/dòng với kết luận (CO / N/A / Pending) |
| R-28 | §9a IX | Minor | Thiếu các cặp tương tác: lọc CA × panel xếp hạng / bảng; đổi thuế × thứ tự sắp xếp và cột # của bảng; bộ lọc Store/CA × số đơn trả trong cảnh báo Cross-period ("Có N đơn trả…") | BR-SPM-021…023; PRD khối 2 | Thêm IX và CO tương ứng |
| R-29 | FR-SPM-011-c6 · CO-147…153 | Minor | Nhãn bộ chọn khi người xem *không phải* CRM chọn toàn bộ phạm vi (U-SM12 cả 2 store; RM Hermès cả 14 store): "N store đã chọn" hay "Brand Hermès · 14 store"? Nguồn chỉ cho ví dụ CRM | BR-SPM-020 | Tạo **Q-48** |
| R-30 | FR-SPM-010-c28 · TC-CHART-030, TC-CHART-004 | Minor | "'Đủ kỳ' và 'Cao nhất' luôn có" trong chú giải mâu thuẫn với trường hợp không có cột > 0 (TC-CHART-030) hoặc không có cột Đủ kỳ (Tuần 11/10–12/10: 2 cột xám). Chưa có Q, case không assert chú giải | PRD mục 5 đoạn chú giải | Tạo **Q-49** |
| R-31 | FR-SPM-009 "Số có thể thay đổi sau khi kỳ kết thúc" | Minor | Thiếu mệnh đề "tài khoản khách được gộp (ảnh hưởng chỉ số theo khách)"; bảng mệnh đề chỉ có "đơn về chậm từ HUB" (c14) | FR-SPM-009 | Thêm mệnh đề. CO có thể Pending vì chưa có cách tạo (SETUP) |
| R-32 | FR-INC-005 · TC-INC-028 | Minor | Incentive "theo kỳ báo cáo": bill gán vào kỳ theo ngày nào (ngày hoàn tất bill, UTC+7?). TC-INC-028 ngầm dùng "ngày F" | FR-INC-005; JSONL order_date "là ngày dùng để ghi nhận doanh thu/hoa hồng" | Tạo **Q-50**. Gắn marker vào TC-INC-028 |
| R-33 | DT3 · tập phần tử dòng sản phẩm | Suggestion | Chưa có bill nhiều dòng khác nhóm Brand khi **PIC vắng** (Chopard: PIC vẫn 70%; BOSS: PIC 0%). Đây là trường hợp ≥ 2 phần tử thuộc rule khác nhau trên cùng bill, dễ lỗi khi tra cấu hình theo bill thay vì theo dòng | AC-INC-004-04, -06; AC-INC-001-01 | Bổ sung TC-INC-032 |
| R-34 | REQ-UI-02 · EV kênh thứ hai | Suggestion | Dòng phụ trên thẻ KPI (mockup: tử/mẫu "4 531 đơn / 2 440 khách", "1 017 / 4 531 giao dịch") là kênh hiển thị thứ hai của cùng con số, chưa có case đối chiếu nhất quán | image2/3 | Thêm case CL đối chiếu dòng phụ với thẻ (sau khi xác nhận nội dung dòng phụ) |
| R-35 | EV-11 | Suggestion | "Truy cập URL khi chưa đăng nhập: N/A - cơ chế chung" là lý do yếu với một dashboard có số liệu nhạy cảm (rules/04 §D) | rules/04 §D | Thêm 1 case smoke PERM (chưa đăng nhập → chuyển trang đăng nhập, API trả 401) |

## 4. Phụ thuộc chưa đánh dấu — tổng hợp theo case

| TC_ID | Assertion phụ thuộc | Marker cần thêm |
|---|---|---|
| TC-SCOPE-006 | "hợp các Position" | `[Giả định AS-xx]` + Q-36 (R-01) |
| TC-CHART-037 | cột tuần chứa D+2 "xám" | `[Giả định AS-03]` (R-02) |
| TC-FLT-007 | Transactions/Sales = truy vấn | `[Giả định AS-01]` `[Cần xác nhận Q-16]` `[Giả định AS-09]` (R-04) |
| TC-SCOPE-005 | "Transactions = số đơn bán hợp lệ"; Sales gồm B2B | `[Giả định AS-01]` `[Cần xác nhận Q-16]` (R-04) |
| TC-TABLE-008 | "không có tab Theo Brand" | `[Cần xác nhận Q-37]` (R-05) |
| TC-SCOPE-003 | "Không có bộ chọn store mở rộng" | `[Cần xác nhận Q-40]` (R-10) |
| TC-INC-004…007, 009, 010, 025, 027 | Discount % tính trên Gross/Net | `[Cần xác nhận Q-41]` (R-14) |
| TC-CHART-026 | nhãn giá trị dạng rút gọn | `[Cần xác nhận Q-44]` (R-20) |
| TC-FLT-007 | trạng thái nút preset | `[Cần xác nhận Q-45]` hoặc bỏ assert (R-22) |
| TC-INC-028 | ngày gán kỳ của bill | `[Cần xác nhận Q-50]` (R-32) |

## 5. Kiểm tra phép tính

**Bảng 17.2 (Sau thuế) — tự tính lại từ bảng 17.1: cả 13 dòng đúng.**

| Phạm vi · kỳ | Tính lại | Kết luận |
|---|---|---|
| ST1 · D | Bán O1+O2+O3+O5+O6 = 48 000 000 (O7 VO, O8 nháp loại); trả R1 5 400 000 → 42 600 000; Trx 5; khách K1, K2, K3, K7 = 4; coupon O2, O6 = 2/5 = 40.0%; AOV 8 520 000; qty 10 − 1 = 9 → 1.80; Freq 1.25; Avg 10 650 000 | Đúng |
| ST1 · D+1 | −1 600 000 − 5 000 000 = −6 600 000; Trx 0 → các tỷ lệ "—" | Đúng (Total Customers 0 phụ thuộc AS-06) |
| ST1 · D+2 | 3 × 1 000 000 + 2 000 000 = 5 000 000; Trx 4; khách 2; AOV 1 250 000; UPT 1.00; Freq 2.00; Avg 2 500 000 | Đúng |
| ST2 · D | 4 000 000 + 6 000 000 − 6 000 000 = 4 000 000; Trx 2; coupon 1/2; qty 1 + 2 − 2 = 1 → 0.50 | Đúng |
| ST2 · D+1 | 4 000 000 − 4 000 000 = 0; Trx 1; UPT (3 − 1)/1 = 2.00; khách 1 (AS-06) | Đúng |
| ST2 · D+2 | 1 000 000 − 4 000 000 = −3 000 000; UPT (1 − 3)/1 = −2.00 | Đúng |
| ST2 · D+3 | 0 + 2 000 000; Trx 2 (AS-01); UPT 4/2 = 2.00; Avg 1 000 000. *Nếu Q-01 = không tính 0đ*: Trx 1, Coupon 0.0%, AOV 2 000 000, UPT 3.00, Freq 0.50; Avg không đổi | Đúng — **trừ khi T = D+3 (R-03)** |
| ST3 · D | 25 000 000; Trx 2; khách 1; UPT (6 + 4)/2 = 5.00; Avg 25 000 000 | Đúng |
| ST3 · D+1 | 8 000 000; coupon 2/3 = 66.666…% → 66.7%; AOV 2 666 666.67 → 2 666 667; UPT 5/3 = 1.666… → 1.67 (2.33 nếu tính dịch vụ); Freq 1.50; Avg 4 000 000 | Đúng |
| ST3 · D+2 | 2 000 000 − 2 500 000 = −500 000; UPT (1 − 1)/1 = 0.00; khách 1 (AS-06; nếu đếm K10: Freq 0.50, Avg −250 000) | Đúng |
| ST1 + ST2 · D | 46 600 000; Trx 7; khách {K1, K2, K3, K7, K9} = 5; coupon 3/7 = 42.857% → 42.9%; AOV 6 657 142.86 → 6 657 143; UPT 10/7 = 1.4286 → 1.43; Freq 1.40; Avg 9 320 000 | Đúng |
| CA-A · D / CA-B · D | CA-A: O1, O2, O5, O6 = 4, coupon 2/4; CA-B: O2, O3 = 2, coupon 1/2 | Đúng |

**Số trong case — đã tính lại, đúng:** TC-SALES-001…012, 015 (−200 000); TC-CPN-001 (80.0% / 60.0% là giá trị sai được nêu để phân biệt); TC-UPT-001…003; TC-DISP-006 (1 250 000.5 → 1 250 001); TC-TABLE-003 (100/15 → 7 trang, trang cuối 10 dòng); TC-TABLE-006, 010; TC-RANK-005; TC-INC-001…030 (gồm TC-INC-026: 7 + 10 + 3 = 20 000 000; 3 + 3 = 6 000 000); TC-MIG-002 (9 800 000 × 1.75% = 171 500; × 0.75% = 73 500).

Lịch và đếm cột của biểu đồ đã kiểm theo lịch 2025–2026: TC-CHART-002, 003, 009 (10 tuần), 013–025 (vd. 06/01/2025 là T2, 05/01/2025 là CN; 366 ngày chạm 53/54 tuần; 01/05–28/08 = 120 ngày, 18 tuần; 06/07–13/09 = 70 ngày, 10 tuần), TC-FLT-008/009 (366/367 ngày): **đúng**.

**Sai:** TC-CHART-033 (R-07). Bảng ví dụ của nguồn, dòng 02/08–14/10: thực tế 12 cột tuần và Tháng bấm được (R-06). Ví dụ §2.4 của FRD đã kiểm: AOV 6 833 333 / 6 254 209, Avg 8 200 000 / 7 505 050 đúng; AC-SPM-004-01 (Trx 5) lệch AC-SPM-003-01 (Trx 6) — đã nằm trong Q-01. Mockup: AOV 301 852 754 000 / 4 531 = 66 619 456, Frequency 1.86, Avg 123 710 145, trước thuế 60 857 736 / 113 010 821 đều khớp; chỉ Σ Sales tab Theo Brand lệch 20 000 000 (R-25).

## 6. Điều kiện kiểm thử chưa được bao phủ

| Điều kiện | Nguồn | Phát hiện | Case đề xuất |
|---|---|---|---|
| CA là PIC của khách nhưng không đứng tên bill → không thấy bill | PRD vai trò; FR-SPM-001; BR-SPM-002 | R-08 | TC-SCOPE-020 |
| Vai trò Store Manager 1 store (trạng thái mặc định) | FR-SPM-001 | R-09 | TC-SCOPE-021 |
| Biên dưới kỳ 00:00:00 / 23:59:59 ngày trước | FR-SPM-001 | R-18 | TC-SCOPE-022 |
| tax_total âm → log | BR-SPM-014 | R-19 | TC-SALES-017 |
| Tháng bấm được trong dải tự chọn Tuần | PRD mục 3 Bước 1 | R-06 | TC-CHART-050 |
| Tuần chứa hôm nay nhưng kỳ dừng trước hôm nay (ngày tương đối) | PRD mục 4 vs BR-SPM-017 | R-02, R-21 | TC-CHART-051 |
| > 5 store vẫn duyệt CA qua tab | BR-SPM-021 | R-11 | TC-STORE-012 |
| Tổng Sales các CA > dòng Tổng (vế Sales của AC-SPM-001-04) | AC-SPM-001-04 | R-12 | TC-TABLE-016 |
| Chọn chip 1 Brand → tab Theo Brand | BR-SPM-023; image2 | R-05 | TC-TABLE-017 |
| B2B có PIC trên bill → N/A | FR-INC-003 | R-13 | TC-INC-031 |
| Bill PIC vắng, dòng Chopard + dòng BOSS | AC-INC-004-04/06 | R-33 | TC-INC-032 |
| Phạm vi nhiều Position rời nhau | FR-SPM-001 | R-01 | Pending - Q-36 |
| Quyền xem Incentive theo vai trò; chặn API | REQ-BSP-01; BR-SPM-001 | R-15 | Pending - Q-42 |
| Chỉ số mức Cá nhân ngoài Sales/Transactions/UPT | BR-SPM-002 | R-10 | Pending - Q-40 |
| Discount % — cơ sở thuế, Gross = 0, Discount âm | FR-INC-002 | R-14 | Pending - Q-41 |
| Half-up số âm | FR-SPM-009 | R-17 | Pending - Q-43 |
| Hoàn trả trong tooltip theo cách nhìn thuế | BR-SPM-019 | R-23 | Pending - Q-46 |
| Gộp tài khoản khách làm đổi số kỳ cũ | FR-SPM-009 | R-31 | Pending (SETUP chưa có) |
| IX: lọc CA × xếp hạng/bảng; thuế × sắp xếp/cột #; bộ lọc × số đơn trả của cảnh báo | — | R-28 | Thêm CO sau khi người sinh xét |
| ST/EV: đổi Store khi đang chọn tay; Back; tab thứ hai; URL có tham số | rules/04 §B | R-27 | Thêm dòng có kết luận |

## 7. Trùng lặp (đã xét ngữ nghĩa)

Validator báo **0 ứng viên trùng lặp**. Reviewer xét thêm các nhóm có cùng Precondition/Test_Data, kết luận **không trùng**:

- TC-SALES-001, TC-SCOPE-007, TC-SCOPE-008, TC-TRX-001, TC-AOV-001, TC-UPT-001, TC-AVGS-001, TC-CPN-001, TC-FREQ-001, TC-DISP-002, TC-DISP-004: cùng bộ ST1 · D nhưng mỗi case nhắm một mục tiêu/phân vùng khác (VO, nháp, khách lẻ, từng chỉ số, định dạng). Giữ nguyên.
- TC-STORE-008, TC-RANK-006, TC-TABLE-008: cùng thao tác "chỉ chọn ST1" nhưng kiểm 3 khối khác nhau (KPI, panel xếp hạng, tab bảng). Giữ nguyên. Riêng TC-STORE-008 có assert trùng với 2 case kia — có thể rút gọn, không bắt buộc.

## 8. Câu hỏi phát sinh (đề xuất thêm vào `analysis.md` §13)

| ID | Câu hỏi | Liên quan | Mức độ |
|---|---|---|---|
| Q-36 | Tài khoản có nhiều Position với phạm vi rời nhau (vd. SM ST1 + Retail Manager Brand BR-2): áp **một** phạm vi lớn nhất (đo theo mức hay theo số store?) hay **hợp** các phạm vi? | FR-SPM-001; TC-SCOPE-006 | Major |
| Q-37 | "Tab Brand chỉ khi phạm vi có > 1 Brand": phạm vi là phạm vi Position hay tập store đang chọn? (image2 ẩn tab Theo Brand khi chọn chip Hermès) | BR-SPM-023; TC-TABLE-008 | Minor |
| Q-38 | Ví dụ đối chiếu dòng Custom 02/08–14/10: xác nhận 12 cột tuần (27/07 … 12/10) và nút Tháng bấm được (chạm 3 tháng lịch) theo bảng quy tắc Bước 1? | PRD Logic hiển thị mục 3, 8 | Major |
| Q-39 | Trục Y: "khoảng 4–5 khoảng chia" (PRD) hay "khoảng 4 mốc" (BR-SPM-018)? | FR-SPM-010 | Minor |
| Q-40 | Mức Cá nhân: Total Customers, Frequency, Coupon %, AOV, Avg Spending tính trên tập nào? Bộ chọn Store và lọc Client Advisor hiển thị gì cho Client Advisor? | BR-SPM-002; REQ-UI-05 | Major |
| Q-41 | Discount % dòng: Gross Value và Net Amount cùng cơ sở thuế không (Net có gồm VAT)? Xử lý Gross = 0 và Discount âm (Net > Gross)? | FR-INC-002 | Major |
| Q-42 | Vai trò nào được xem Incentive của ai (CRM, RM, SM, CA)? Áp Position Rule ở tầng truy vấn như BR-SPM-001? | REQ-BSP-01; FR-INC-005 | Major |
| Q-43 | Làm tròn half-up với số âm có phần lẻ ,5: ra xa 0 (−x.5 → −(x+1)) hay về +∞? | FR-SPM-009 | Minor |
| Q-44 | Nhãn giá trị trên đầu cột cao nhất hiển thị rút gọn (Tr/Tỷ như trục) hay số đầy đủ? | PRD mục 5; BR-SPM-018 | Minor |
| Q-45 | Khi khoảng Từ ngày – Đến ngày nhập tay trùng một preset (vd. đúng tháng trước), nút preset có ở trạng thái đang chọn không? | REQ-UI-01 | Minor |
| Q-46 | Tooltip "Hoàn trả đã trừ" hiển thị theo cách nhìn thuế đang chọn hay luôn sau thuế? | BR-SPM-019 | Minor |
| Q-47 | Bộ preset kỳ (Hôm nay / Tuần này / Tháng này / Tháng trước / Năm này) có thay cho bộ lọc chung Day/Week/Month/Custom kế thừa BRD không (OQ-SPM-09)? | PRD Assumptions; FR-SPM-001 | Minor |
| Q-48 | Nhãn bộ chọn Store khi người xem không phải CRM chọn toàn bộ phạm vi của mình (vd. SM 2 store; RM Hermès 14 store)? | BR-SPM-020 | Minor |
| Q-49 | Chú giải "Đủ kỳ"/"Cao nhất luôn có" có giữ nguyên khi không có cột Đủ kỳ hoặc không có cột > 0 không? | PRD mục 5 | Minor |
| Q-50 | Incentive gán vào kỳ báo cáo theo ngày nào (ngày hoàn tất bill, UTC+7, hay order_date)? | FR-INC-005 | Minor |

## 9. Case đề xuất bổ sung

File `output/DASHBOARD-DOANH-THU/testcases-additional.csv` — **11 case**, ID tiếp nối số lớn nhất theo lịch sử của từng module, `Notes` có `[Đề xuất review]` và mã phát hiện:

TC-SCOPE-020 (R-08) · TC-SCOPE-021 (R-09) · TC-SCOPE-022 (R-18) · TC-SALES-017 (R-19) · TC-CHART-050 (R-06, Q-38) · TC-CHART-051 (R-02/R-21, AS-03) · TC-STORE-012 (R-11) · TC-TABLE-016 (R-12) · TC-TABLE-017 (R-05, Q-37) · TC-INC-031 (R-13) · TC-INC-032 (R-33)

Người sinh cần làm khi nhận các case này:
- thêm Q-36…Q-50, CO tương ứng, mệnh đề mới (R-08, R-11, R-12, R-31) vào `analysis.md`;
- thêm TC-CHART-051 vào AS-03;
- thêm tài khoản U-SM1 vào SETUP-01;
- chạy lại validator với `--previous testcases.v1.0-pre-review.csv`.

**Không sửa `testcases.csv` và `analysis.md` gốc** — mọi đề xuất sửa nằm ở mục 3 và mục 4.
