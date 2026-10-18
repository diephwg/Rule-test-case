# Review bộ test case — DEV-3648 Giỏ hàng có sản phẩm hết hàng

| Thông tin | Giá trị |
|---|---|
| Bộ được review | `testcases.csv` **v1.1** (39 case, sinh lúc 2026-10-16 22:23, theo bộ rules đã sửa) + `analysis.md` v1.1 |
| Nguồn đối chiếu | Jira DEV-3648 (đọc lại 2026-10-16), 2 ảnh đính kèm (lần này **đã đọc được cả hai** — `_extracted/jira-DEV-3648-attachments.md`) |
| Người review | AI agent (Claude), theo `rules/05` §Review |
| Review trước | `review.v1.0.md` (review bản v1.0, đã lỗi thời — phần lớn phát hiện đã được sửa ở v1.1, xem §8) |

## 1. Tóm tắt

| Mục | Kết quả |
|---|---|
| Tổng case | 39 (P1 15 · P2 17 · P3 6 · P4 1) |
| Validator | 0 ERROR · 0 WARNING |
| Mức sẵn sàng (validator) | Ready 22 · Needs Clarification 17 · CO Pending 7 |
| Mức sẵn sàng (sau review) | **Ready 20 · Needs Clarification 19**. TC-CART-031 và TC-CART-039 đang có expected dựa trên giả định chưa ghi Q/AS (F-01, F-03) |
| Phát hiện | Critical 1 · Major 8 · Minor 9 · Suggestion 2 |
| Đề xuất bổ sung | 5 case (`testcases-additional.csv`, TC-CART-040…044), 8 điều kiện mới (CO-47…54, trong đó 3 Pending), 5 câu hỏi mới (Q-13…17) |

**Kết luận:** chất lượng viết tốt và truy vết đầy đủ: mọi mệnh đề *Then* của AC01–AC10 đều có ít nhất một case (§2.2). Bộ test **chưa nên bàn giao dưới dạng Ready**, vì:
1. Có 2 case báo Ready nhưng expected dựa trên giả định chưa được đánh dấu.
2. Bảng quyết định DT2 (revalidate khi bấm "Mua hàng") thiếu 3 tổ hợp rủi ro cao, liên quan trực tiếp đến luồng checkout.
3. SETUP-02 (cách đổi tồn kho) chưa có quy trình. 32/39 case cần đặt Saleable Qty (9 case đổi tồn kho ngay trong lúc chạy), nên tester mới chưa chạy được.

Sau khi xử lý các mục *Bắt buộc* ở §7, bộ test bàn giao được dưới dạng **bản nháp có kiểm soát** (Ready + Needs Clarification).

## 2. Chỉ số bao phủ

### 2.1 Bốn chỉ số theo `rules/05`

| # | Chỉ số | Hiện tại (v1.1) | Sau khi nhận đề xuất review | Mẫu số |
|---|---|---|---|---|
| 1 | Req_ID có case | 18/18 | 18/18 | AC01–10, BR-01–03, IMP-01–05 |
| 2 | Điều kiện kiểm thử có case | 39/39 | 44/44 | CO trừ Pending. Mẫu số tăng từ 39 lên 44: review phát hiện 5 điều kiện **thiết kế được** mà v1.1 chưa lập |
| 3 | Theo kỹ thuật | DT 7/7 · ST 10/10 · UC 9/9 · EG 6/6 · BVA 4/4 · EP/CRUD/CL 1/1 | DT 10/10 · ST 11/11 · EG 7/7 | **Lưu ý:** DT2 thiếu 3 rule khả thi (F-04, F-05, F-06), nên "7/7" của v1.1 đúng với bảng đã lập nhưng bảng đó chưa đủ |
| 4 | Đang chờ | Pending 7 · NC 17 · Q mở 12 · AS 5 · IMP 5 | Pending 10 · NC 22 · Q mở 17 · AS 5 · IMP 5 | – |

Chỉ số 2 của v1.1 là **39/39**. Con số này chỉ có nghĩa "100%" trên **danh sách điều kiện do chính AI lập**. Đây là lý do chính phải bổ sung đối chiếu ở mức mệnh đề (§2.2) và đề xuất rule RG-03.

### 2.2 Bao phủ theo mệnh đề nguồn (người review tự đếm)

Mẫu số: 52 mệnh đề *Then* / dòng bảng / Business Rule tách từ AC01–AC10. ✔ = có case với oracle đã xác nhận cho chính mệnh đề đó; ⚠ = chỉ có case với oracle tạm.

| AC | Số mệnh đề | ✔ | ⚠ | Mệnh đề ⚠ / ghi chú |
|---|---|---|---|---|
| AC01 | 4 | 4 | 0 | Tick/untick có TC-012 (Ready); TC-001 phụ thuộc Q-02 |
| AC02 | 5 | 4 | 1 | Câu thông báo OOS (Q-01/AS-01) |
| AC03 | 7 | 7 | 0 | |
| AC04 | 6 | 6 | 0 | Bảng 4 dòng + 2 Business Rule |
| AC05 | 6 | 5 | 1 | Câu thông báo dưới từng SP (Q-01) |
| AC06 | 5 | 3 | 2 | Tự điều chỉnh khi tồn kho giảm; checkout sau điều chỉnh (thời điểm phát hiện: Q-04/AS-03) |
| AC07 | 3 | 3 | 0 | Phân vùng qty < 1 đang Pending (Q-05) |
| AC08 | 7 | 7 | 0 | Đủ mệnh đề, nhưng **thiếu tổ hợp** (§4) |
| AC09 | 4 | 3 | 1 | Có hàng trở lại (Q-06, nguồn ghi "có thể được Enable") |
| AC10 | 5 | 3 | 2 | Giữ thứ tự tương đối của 2 nhóm (Q-15 mới) |
| **Tổng** | **52** | **45** | **7** | 52/52 có case · 45/52 có oracle đã xác nhận |

Ngoài phạm vi AC nhưng thuộc Epic (đang Pending, chưa có case): checkbox "Tất cả sản phẩm", Gift-popup/Amasty, Bundle/Set, guest, badge mini-cart.

## 3. Bảng phát hiện

| ID | TC / CO / Req | Mức | Vấn đề | Căn cứ | Đề xuất sửa |
|---|---|---|---|---|---|
| F-01 | TC-CART-031, TC-CART-008 / AC10 | **Critical** | Expected khẳng định thứ tự hiển thị A-C-E-B-D, dựa trên giả định "thứ tự thêm = thứ tự trước khi sắp xếp". Giả định này chỉ ghi chữ tự do ở Notes, không có Q/AS, nên validator tính TC-031 là **Ready**. Magento/theme có thể hiển thị mới → cũ. | AC10 không định nghĩa "thứ tự trước khi hệ thống sắp xếp"; `rules/05` anti-pattern "Trình bày giả định như yêu cầu" | Thêm Q-15 (+ AS-06 nếu cần chạy trước). Đánh dấu `[Cần xác nhận Q-15]` ở TC-031 và TC-008. Hoặc viết lại expected theo **thứ tự quan sát ở bước trước** (chụp thứ tự khi tất cả còn hàng, rồi đổi tồn kho) để không phụ thuộc Q-15 |
| F-02 | TC-CART-008 / AC03 | Major | Expected bước 1 "nút Mua hàng Enable" chỉ đúng khi SP còn hàng **được tick sẵn** (AS-02/Q-02). Case không ghi AS-02, và AS-02 chỉ liệt kê TC-001. Khi Q-01 được trả lời, case sẽ chuyển sang Ready sai. | `analysis.md` §14 AS-02 | Thêm `[Giả định AS-02]` vào TC-008, cập nhật danh sách "Case bị ảnh hưởng" của AS-02. Hoặc bỏ assertion này khỏi bước 1 (TC-009 đã kiểm tra) |
| F-03 | TC-CART-039 / CO-40 / AC02 | Major | Oracle UI lấy từ mockup `image-20260812`. Theo chính analysis §12, mockup này là **hiện trạng cũ**: SP OOS ở đầu danh sách, câu "Số lượng sản phẩm không có sẵn". Dù vậy case vẫn báo Ready. Ngoài ra, ảnh thứ 2 được ghi "chưa đọc được, ảnh hưởng UI", nhưng thực ra chỉ là ảnh chụp ticket DEV-3656, không phải mockup. | `_extracted/jira-DEV-3648-attachments.md` | Đánh dấu `[Cần xác nhận Q-01]`, hoặc tạo Q hỏi "có thiết kế UI mới cho thông báo OOS không". Cập nhật danh mục nguồn: ảnh 2 *Đã đọc*, không ảnh hưởng UI. Ảnh 2 (DEV-3656) xác nhận lại câu "Sản phẩm hiện đang hết hàng", là căn cứ bổ sung cho AS-01 |
| F-04 | CO mới CO-47 / AC08 | Major | DT2 chỉ xét SP **được tick**. Chưa có điều kiện cho trường hợp SP **không được tick** đổi tồn kho đúng lúc bấm "Mua hàng". AC08 ghi "Nếu tất cả SP được chọn vẫn đủ stock → tiếp tục Checkout", nhưng dòng sau lại ghi "Nếu có SP không còn đủ…" (không nói "được chọn"). Đây là chỗ dễ có lỗi chặn checkout không cần thiết. | DEV-3648 AC08 | Thêm điều kiện C "SP thay đổi có được tick không" vào DT2. Thêm Q-16 và **TC-CART-042** |
| F-05 | CO mới CO-49, CO-50 / AC02 × AC04 | Major | Không case nào kiểm tra trường hợp **SP được tick duy nhất** chuyển sang hết hàng. TC-007, TC-024, TC-026 đều còn SP khác được tick, nên nút "Mua hàng" luôn Enable. Nếu nút không chuyển sang Disable, bộ test không phát hiện được. | AC04 Business Rule; analysis §15 (rủi ro P1 "SP OOS lọt vào Checkout") | **TC-CART-041** (đường revalidate, đề xuất từ v1.0 nhưng chưa được nhận) và **TC-CART-043** (đường tải lại) |
| F-06 | CO mới CO-48 / AC08 DT2 | Major | Tổ hợp R2 + R3 (một dòng hết hàng, một dòng thiếu số lượng, cùng lúc) khả thi. Analysis bỏ qua với lý do "CO-26 kiểm tra SP khác giữ nguyên", nhưng CO-26 chỉ có **một** loại thay đổi. Đây là lý do không đúng theo `rules/02` §DT bước 2. | analysis §9 ghi chú dưới DT2 | **TC-CART-040** (đề xuất từ v1.0, đã chỉnh theo SETUP) |
| F-07 | SETUP-02; 32/39 case | Major | SETUP-02 ghi "cách đổi tồn kho cụ thể cần dev/QA lead xác nhận (MSI…)". Tester mới không biết cách đưa Saleable Qty về 0/1/2: Saleable Qty = Qty − reservation, khác với Qty trên form sản phẩm. `report.md` lại ghi "chạy được toàn bộ 39 case". Mức sẵn sàng hiện chỉ đo **oracle**, chưa đo **khả năng thực thi**. | `rules/03` §Tái tạo được; analysis §17 | Xin dev viết quy trình SETUP-02 cụ thể: màn hình admin hoặc API, nguồn/stock, cách xử lý reservation, cách reset. Sửa câu trong report. Xem rule RG-02 |
| F-08 | SETUP-01; TC-002, 006, 016, 033 | Major | Fixture lấy giá từ mockup nhưng SETUP ghi "map sang SKU thật". Nếu SKU thật có giá khác thì expected tiền sai. SP-C/SP-D có Giá ≠ Tạm tính (5.530.000 → 3.318.000; 2.640.000 → 1.584.000, giảm 40%) nhưng SETUP không mô tả khuyến mãi. Phép tính TC-033 (34.878.000 ₫) phụ thuộc khuyến mãi đó. Tên ghi "KENZO **Cornate**", trong khi mockup là "KENZO **Cartoon** Unisex". | Ảnh `image-20260812`; analysis §17 | SETUP-01 ghi rõ cho từng SP: SKU, giá gốc, giá bán/khuyến mãi (catalog rule/special price), tồn kho. Expected tiền tham chiếu "giá bán của SP-x theo SETUP-01" hoặc tester điền sau khi map. Sửa tên KENZO |
| F-09 | AC07, BR-02 | Major | Thiếu 2 nhóm phân vùng. (1) AC07 chỉ nêu SP **đang được tick**; đổi qty của SP **bỏ tick** thì chưa rõ. (2) "Hết hàng" mới chỉ xét Saleable Qty = 0. Magento còn có Stock Status = Out of Stock thủ công khi qty > 0, backorder, Out-of-Stock Threshold, SP bị disable. Các trường hợp này hệ thống có thể xử lý khác nhau (EP phải chia theo cách xử lý). | `rules/02` §EP mục 1 | Q-13, Q-14. CO-52, CO-53 để `Pending` |
| F-10 | TC-CART-003 ↔ TC-CART-023 | Minor | Trùng về ngữ nghĩa: cùng dữ liệu (SP-A, SP-C qty 1 được tick), cùng hành động, cùng kết quả (sang Checkout đủ 2 SP). TC-023 chỉ thêm assertion "không có banner". | `rules/05` §Trùng lặp | Giữ TC-023, chuyển `AC01;BR-01` và CO-03 sang TC-023. Đặt TC-003 `Obsolete` (không xoá) |
| F-11 | TC-CART-005, TC-CART-007 | Minor | Priority P2, trong khi hai case này là chốt chặn cho rủi ro "SP OOS lọt vào Checkout", mà chính bảng rủi ro §15 xếp P1. | analysis §15 | Đánh giá lại theo rủi ro. Đề xuất P1 |
| F-12 | TC-CART-015 | Minor | Test_Type = `Security`, nhưng case không có vector tấn công hay phân quyền, chỉ là đường điều hướng khác. | – | `Functional`. Xem rule RG-07 |
| F-13 | TC-CART-018 | Minor | Step ghi "nút + **hoặc** nhập 2". Đây là hai kênh nhập (hai luồng code) gộp trong một case. Mockup không có nút +/- (chỉ có ô số). | Ảnh `image-20260812` | Chỉ giữ kênh có trên UI thực tế. Nếu có cả nút +/- thì tách thành case riêng |
| F-14 | TC-CART-005 | Minor | Bước 2 "click ảnh/tên SP-B rồi quay lại Giỏ hàng" không rõ đang kiểm tra mục tiêu gì. | `rules/03` §Một mục tiêu | Bỏ, hoặc nêu mục tiêu: trạng thái tick không bị reset sau khi điều hướng |
| F-15 | TC-CART-028 | Minor | Expected "4. Ở mọi bước…" gom các assertion của bước 1–3 vào số 4. | `rules/03` Expected đánh số theo bước | `1. …` `2. …` `3. …` `4. …` |
| F-16 | Preconditions 39 case | Minor | Mọi case đều có "thay đổi tồn kho theo SETUP-02", kể cả case không cần đổi tồn kho (001–003, 010–012, 019–023, 038…). Tester dễ hiểu là case nào cũng cần admin. | – | Chỉ tham chiếu SETUP-02 khi case thật sự đổi tồn kho |
| F-17 | TC-CART-035 | Minor | Notes "Cần xác nhận SP-C tick hay không" không có Q-ID. Case cũng thiếu địa chỉ giao hàng / quy trình đặt COD. | `rules/03` §Notes | Tạo Q mới (hoặc gộp vào Q-06). Thêm SETUP-03 "đặt hàng COD" (địa chỉ, phí ship) |
| F-18 | analysis §0, §12 | Minor | Danh mục nguồn chưa cập nhật: ảnh 2 thực chất là DEV-3656, không phải mockup. Tổng "TỔNG (8 SẢN PHẨM) 55.870.000 ₫" trên mockup không cộng ra từ các dòng hiển thị (3 dòng được tick = 20.682.000; cả 4 dòng = 56.962.000), nên mockup không dùng được làm oracle tổng tiền. | `_extracted/jira-DEV-3648-attachments.md` | Cập nhật §0, §12. Bổ sung vào Q-07 |
| F-19 | Phạm vi | Minor | Không có điều kiện / N/A nào cho mobile web / responsive. Front-row có giao diện mobile thì checkbox và nút "Mua hàng" cố định là khu vực dễ lỗi. | `rules/04` §H | Ghi `N/A - lý do` hoặc tạo Q về nền tảng hỗ trợ |
| S-01 | CO-51 | Suggestion | Vào thẳng URL `/checkout` khi Cart có SP bỏ tick / OOS, bỏ qua bước chọn lọc và revalidate. Rủi ro lọt SP khi tách quote (DEV-3654). TC-015 chỉ xét Cart toàn OOS. | EG | **TC-CART-044** |
| S-02 | CO-54 | Suggestion | Cùng Cart mở ở 2 tab/thiết bị, trạng thái tick khác nhau. | EG, liên quan Q-09 | Q-17, CO Pending |

## 4. Điều kiện kiểm thử đề xuất bổ sung (thêm vào analysis §16)

| Cond_ID | Req_ID | Điều kiện | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-47 | AC08 | DT2: SP **không được tick** thay đổi tồn kho lúc bấm Mua hàng | DT | TC-CART-042 | Q-16 |
| CO-48 | AC08; BR-02; BR-03 | DT2-R4: một SP hết hàng + một SP thiếu số lượng cùng lúc | DT | TC-CART-040 | |
| CO-49 | AC04; AC08 | DT2-R2 khi SP được tick duy nhất hết hàng → nút Disable sau revalidate | DT | TC-CART-041 | |
| CO-50 | AC02; AC04 | SP được tick duy nhất chuyển OOS khi tải lại → nút Disable | ST | TC-CART-043 | AS-03 |
| CO-51 | AC03 | Vào thẳng URL Checkout khi Cart có SP bỏ tick / OOS | EG | TC-CART-044 | Q-12 |
| CO-52 | AC07 | Đổi qty của SP đang bỏ tick | EP | | Pending - Q-13 |
| CO-53 | AC02; BR-02 | Phân vùng "hết hàng" khác Saleable Qty = 0 | EP | | Pending - Q-14 |
| CO-54 | AC01 | Cart ở 2 tab/thiết bị | EG | | Pending - Q-17 |

Đã kiểm chứng: ghép `testcases.csv` + `testcases-additional.csv` rồi chạy validator với bản analysis có thêm CO-47…54 và Q-13…17 → **0 ERROR · 0 WARNING**, `--previous` không mất ID.

## 5. Trùng lặp (đã xét ngữ nghĩa)

| Nhóm | Kết luận |
|---|---|
| TC-003 ↔ TC-023 | **Trùng** → gộp (F-10) |
| TC-013 ↔ TC-014 | Không trùng: 013 kiểm tra không checkout được, 014 kiểm tra hiển thị. Chỉ chung 1 assertion "nút Disable" |
| TC-016 ↔ TC-017, TC-024 ↔ TC-027 | Không trùng: cùng các bước đầu nhưng mục tiêu khác (điều chỉnh / tiếp tục checkout) |
| TC-021 ↔ TC-022 | Không trùng: biên max+1 và đại diện phân vùng invalid xa |

## 6. Câu hỏi mới cho BA/PO

| ID | Câu hỏi | Liên quan | Mức độ |
|---|---|---|---|
| Q-13 | AC07 chỉ nêu SP đang được tick: đổi qty của SP **đang bỏ tick** có kiểm tra Saleable Qty không, có tự tick lại không? | AC07 | Major |
| Q-14 | "Hết hàng" xác định thế nào: chỉ Saleable Qty = 0, hay cả Stock Status = Out of Stock khi qty > 0, backorder, Out-of-Stock Threshold, SP bị disable/xoá? | AC02, BR-02 | Major |
| Q-15 | "Thứ tự trước khi hệ thống sắp xếp" (AC10) là thứ tự thêm vào Cart, cũ → mới hay mới → cũ? | AC10 | Major |
| Q-16 | AC08: SP **không được tick** thay đổi tồn kho lúc bấm Mua hàng thì vẫn sang Checkout hay reload Cart + banner? | AC08 | Major |
| Q-17 | Cart mở ở 2 tab/thiết bị với trạng thái tick khác nhau: bấm Mua hàng ở tab nào thì lấy lựa chọn nào? | AC01 | Minor |

Kèm yêu cầu cho **dev/QA lead**: quy trình SETUP-02 (đổi Saleable Qty trên môi trường test và cách reset).

## 7. Việc cần làm trước khi bàn giao tester

**Bắt buộc (sửa bộ test, khoảng 1–2 giờ):**
1. F-01, F-02, F-03: thêm marker Q/AS cho TC-008, 031, 039; cập nhật AS-02 và danh mục nguồn.
2. F-04, F-05, F-06: nhận TC-CART-040…043 vào `testcases.csv`, thêm CO-47…50 và Q-16.
3. F-07, F-08: có quy trình SETUP-02 từ dev; hoàn thiện fixture SETUP-01 (SKU, giá bán, khuyến mãi).
4. F-10: gộp TC-003 vào TC-023 (TC-003 → Obsolete).
5. Sửa `report.md`: mức sẵn sàng và câu "chạy được toàn bộ 39 case".
6. Gửi Q-01…Q-17 cho BA/PO. Ưu tiên Q-01, Q-02, Q-04, Q-15, Q-16 vì chúng mở khóa nhiều case nhất.

**Nên làm:** F-09, F-11…F-19, S-01, S-02.

## 8. Trạng thái các phát hiện của review v1.0

| Review v1.0 | Trạng thái ở v1.1 |
|---|---|
| R-01 chỉ số coverage, R-02 ép Positive/Negative, R-07 regression TC-034, R-11 rule quá cứng, R-12 đánh số Expected | Đã sửa (R-12 còn TC-028 — F-15) |
| R-03 phụ thuộc Q chưa đánh dấu | Phần lớn đã sửa; còn TC-008, 031, 039 (F-01…F-03) |
| R-04 DT2 thiếu tổ hợp | **Chưa sửa** (F-06). TC-040 đề xuất chưa được nhận |
| R-05 setup khó tái tạo | Đã có SETUP-01/02, nhưng nội dung chưa đủ (F-07, F-08) |
| R-06 danh mục nguồn | Đã có danh mục; nội dung ảnh 2 sai (F-03, F-18) |
| R-08 validator | Đã sửa phần lớn; còn lỗ hổng ở RG-01 |
| R-09 TC-003/023 | **Chưa xử lý** (F-10) |
| R-10 ví dụ LOGIN | Ví dụ đã qua validator (0 ERROR · 0 WARNING) |

## 9. Đề xuất hoàn thiện bộ rule (rút ra từ review này)

Đây là các lỗ hổng mà **rules + validator hiện tại không bắt được**. Chính chúng là nguyên nhân của F-01…F-08.

| ID | Ưu tiên | Lỗ hổng | Đề xuất | File |
|---|---|---|---|---|
| RG-01 | **Bắt buộc** | Notes có chữ tự do "cần xác nhận…" nhưng không có Q-ID thì validator vẫn tính case là Ready (TC-031, TC-035). Danh sách "Case bị ảnh hưởng" của AS không được đối chiếu với marker trong case (TC-008 thiếu ở AS-02). | Validator: (a) WARNING khi Notes chứa `cần xác nhận / giả định / chưa rõ / TBD` mà không kèm `Q-xx`/`AS-xx`; (b) WARNING hai chiều giữa cột "Case bị ảnh hưởng" của AS và marker `[Giả định AS-xx]` trong case. Rules/03 §Notes: "mọi phụ thuộc phải có ID — không ghi phụ thuộc bằng chữ tự do" | `scripts/validate_testcases.py`, `rules/03` |
| RG-02 | **Bắt buộc** | Mức sẵn sàng chỉ đo **oracle**, chưa đo **khả năng thực thi**: SETUP chưa có cách làm vẫn được tính Ready, và report khẳng định "chạy được toàn bộ". | Thêm cột *Trạng thái* cho bảng SETUP: `Sẵn sàng / Cần chuẩn bị / Chưa rõ cách làm`. Case tham chiếu SETUP ở trạng thái "Chưa rõ cách làm" → Design_Status `Blocked - SETUP-xx`. Thêm vào DoD: không bàn giao khi còn SETUP "Chưa rõ cách làm" mà không ghi rõ trong report | `rules/01` §Mức sẵn sàng, `rules/05` DoD, `templates/analysis-template.md`, validator |
| RG-03 | **Bắt buộc** | Chỉ số 2 dùng mẫu số là danh sách CO do AI tự lập, nên dễ báo 100% dù bảng quyết định còn thiếu rule (F-04…F-06). | Analysis có thêm bảng **Mệnh đề nguồn → CO** (vd. `AC08-c3 → CO-25, CO-26`), mỗi mệnh đề Then/BR một dòng. Validator báo mệnh đề chưa gắn CO, và report có thêm chỉ số "mệnh đề có oracle đã xác nhận" (như §2.2) | `rules/02` §UC, `rules/05` §Chỉ số, template, validator |
| RG-04 | **Bắt buộc** | Rules/02 §DT không nhắc đến điều kiện áp dụng trên **tập phần tử** (giỏ hàng nhiều dòng, danh sách). Vì vậy bị sót trường hợp phần tử *không được chọn* và trường hợp nhiều phần tử rơi vào các rule khác nhau cùng lúc. Ngoài ra, việc bỏ tổ hợp khả thi chưa bắt buộc phải có lý do được review. | Bổ sung vào §DT: "Khi điều kiện áp dụng cho từng phần tử của một tập: xét phần tử được chọn **và không được chọn**; xét tổ hợp ≥2 phần tử thuộc các rule khác nhau; xét trường hợp phần tử duy nhất thoả điều kiện thay đổi". Tổ hợp khả thi bị loại phải ghi lý do **chứng minh** rằng hành vi không đổi | `rules/02` §DT, `rules/04` §E |
| RG-05 | Nên có | Mockup / ảnh được dùng làm oracle mà chưa phân loại là thiết kế mới hay hiện trạng / bug (F-03). Ảnh "chưa đọc được" thì bị đoán ảnh hưởng. | Rules/01 Bước 1: mỗi ảnh ghi *loại* (`Thiết kế mới / Hiện trạng / Bug / Ảnh chụp tài liệu`). Ảnh hiện trạng không dùng làm oracle cho hành vi mới. Nguồn Jira: thử tải attachment qua MCP (`downloadJiraIssueAttachment`) trước khi ghi "chưa đọc được" | `rules/01`, `CLAUDE.md` |
| RG-06 | Nên có | Expected có số tiền nhưng fixture không mô tả giá, khuyến mãi, thuế (F-08). | Rules/03 §Tái tạo được: "Expected có số tiền → SETUP phải ghi giá gốc, giá bán, khuyến mãi/thuế áp dụng. Nếu dữ liệu còn phải map sang SKU thật thì expected tham chiếu biến của fixture, không hard-code từ mockup" | `rules/03` |
| RG-07 | Nên có | Không có định nghĩa cách chọn `Test_Type` (F-12). | Bảng ngắn: Security = có vector tấn công/phân quyền/lộ dữ liệu; Integration = qua ranh giới hệ thống/module khác; Validation = kiểm tra ràng buộc dữ liệu nhập… | `rules/03` |
| RG-08 | Nên có | Không có checklist theo nghiệp vụ e-commerce / tồn kho (F-09, S-01, S-02). | `rules/04` thêm §J *Giỏ hàng & tồn kho*: định nghĩa hết hàng (stock status, backorder, threshold, reservation), các kênh cùng hiển thị giỏ (cart page / mini-cart / URL checkout trực tiếp), đa tab/thiết bị, giá khuyến mãi, thay đổi tồn kho giữa các bước | `rules/04` |
| RG-09 | Nên có | Review cũ nằm cạnh bộ test mới mà không ghi phiên bản. Case đề xuất (TC-040/041) bị bỏ quên qua 1 vòng sinh lại. | tc-review: `review.md` ghi phiên bản/thời điểm của bộ test được review. tc-generate: khi sinh lại, đọc `testcases-additional.csv` và review cũ; report phải có mục *Đề xuất review: đã nhận / từ chối (lý do)* | `.agents/skills/tc-review`, `tc-generate`, `templates/report-template.md` |
| RG-10 | Nên có | Repo chưa có hướng dẫn **cho tester** khi nhận bộ test: đọc Design_Status thế nào, case Needs Clarification bị Fail thì ghi bug hay ghi câu hỏi, cập nhật Status, khi nào chạy lại. | Thêm `docs/huong-dan-tester.md` (1 trang), và sheet *Hướng dẫn* trong xlsx | `README.md`, `scripts/export_xlsx.py` |
