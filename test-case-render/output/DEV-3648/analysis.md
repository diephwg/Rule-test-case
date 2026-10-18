# Phân tích yêu cầu — DEV-3648 Giỏ hàng có sản phẩm hết hàng

| Thông tin | Giá trị |
|---|---|
| Người phân tích | AI agent (Claude) |
| Ngày | 2026-10-16 |
| Phiên bản phân tích | v2.1 — v2.0 (sinh lại theo bộ rules có mệnh đề nguồn, ma trận tương tác, tập phần tử, ma trận trạng thái, sự kiện × kênh, trạng thái SETUP) + xử lý phản biện độc lập (`review.md`). Bản trước: `analysis.v1.1.md` |

## 0. Danh mục nguồn

| Nguồn | Phiên bản / ngày | Trạng thái | Bản trích xuất | Phần bị ảnh hưởng nếu chưa đọc đủ |
|---|---|---|---|---|
| Jira [DEV-3648](https://sts-technical.atlassian.net/browse/DEV-3648) — Description AC01–AC10 | Updated 2026-10-16 10:43 | Đã đọc | `_extracted/jira-DEV-3648.md` | – |
| Ảnh `image-20260812-035015.png` (attachment 17062) | 2026-09-23 | Đã đọc — **ảnh hiện trạng trước tính năng** (SP hết hàng ở đầu danh sách, câu thông báo cũ), không dùng làm oracle cho hành vi mới | `_extracted/jira-DEV-3648-attachments.md`, `_extracted/attachments/` | – |
| Ảnh `image-20260923-104852.png` (attachment 17063) | 2026-09-23 | Đã đọc — ảnh chụp ticket con DEV-3656 (không phải mockup); nhắc lại câu thông báo AC02 | `_extracted/jira-DEV-3648-attachments.md` | – |
| Child tickets DEV-3649…3770 | – | Đọc một phần (tiêu đề; DEV-3656 đọc được mô tả qua ảnh) | `_extracted/jira-DEV-3648.md` | IMP-01…IMP-03; Gift-popup / Bundle / Mini-cart (CO-44…46) |
| Testcase tham chiếu DEV-3363 (SharePoint) | – | **Chưa đọc được** (không có connector SharePoint) | – | Gift-popup / Amasty (CO-44) |

## 1. Tóm tắt tính năng

Hiện tại, khi Cart có ≥1 sản phẩm hết hàng (OOS), hệ thống báo lỗi và ẩn nút "Mua hàng", nên khách phải tự xoá sản phẩm OOS mới checkout được. Tính năng mới cho phép **checkout chọn lọc**: khách tick sản phẩm còn hàng để mua. Sản phẩm OOS tự bỏ tick, bị khoá checkbox, vẫn nằm lại trong Cart và bị đẩy xuống cuối. Hệ thống tự điều chỉnh số lượng khi tồn kho không đủ (Insufficient Stock) và kiểm tra lại tồn kho khi bấm "Mua hàng".

## 2. Phạm vi

**In-scope:** trang Giỏ hàng — tick/untick, trạng thái OOS, nút "Mua hàng", điều chỉnh qty theo Saleable Qty, revalidate trước Checkout, sắp xếp OOS xuống cuối, khung Tóm tắt đơn hàng, sản phẩm còn lại sau khi đặt hàng, truy cập thẳng URL Checkout (chỉ kiểm tra danh sách sản phẩm).

**Out-of-scope / chờ đặc tả:** Gift-popup / Amasty (DEV-3649), Bundle / Set (DEV-3730, DEV-3769, DEV-3770), trang Checkout & thanh toán (ngoài danh sách sản phẩm được chuyển sang), khách vãng lai (Q-09). Các phần này có điều kiện kiểm thử ở trạng thái *Pending*.

## 3. Tác nhân & phân quyền

| Vai trò | Mô tả | Quyền chính |
|---|---|---|
| Khách hàng (đã đăng nhập) | Mua hàng trên Front-row | Xem Cart, tick/untick, đổi qty, xoá SP, Mua hàng |
| Admin Magento | Chuẩn bị dữ liệu | Thay đổi tồn kho, giá bán của sản phẩm test |

Không có khác biệt quyền giữa các khách hàng trong tài liệu → không lập ma trận phân quyền.

## 4. Danh sách yêu cầu

| Req_ID | Mô tả | Nguồn | Rủi ro | Ghi chú |
|---|---|---|---|---|
| AC01 | SP còn hàng tick/un-tick được; SP được tick vào Checkout; khách tiếp tục Checkout với SP đã chọn | DEV-3648 AC01 | High | |
| AC02 | SP OOS tự bỏ tick, checkbox Disable, không vào Checkout, giữ trong Cart, hiện "Sản phẩm hiện đang hết hàng" bên dưới | DEV-3648 AC02 | High | |
| AC03 | Cart A (còn) – B (OOS) – C (còn): chỉ A/C được chọn và sang Checkout, không cần xoá B | DEV-3648 AC03 | High | |
| AC04 | Nút "Mua hàng" Enable khi ≥1 SP còn hàng được tick, ngược lại Disable | DEV-3648 AC04 | High | Xem DT1 |
| AC05 | Tất cả SP OOS: uncheck + Disable, giữ trong Cart, thông báo dưới từng SP, nút "Mua hàng" Disable, không thể Checkout | DEV-3648 AC05 | High | |
| AC06 | Tồn kho giảm thấp hơn qty đang chọn: tự đưa qty về Saleable Qty, giữ tick, hiện "Sản phẩm này chỉ còn số lượng là 1", cho checkout tiếp | DEV-3648 AC06 | High | |
| AC07 | Khách đổi qty: ≤ Saleable Qty giữ nguyên; > Saleable Qty tự về Saleable Qty + thông báo, giữ tick | DEV-3648 AC07 | Medium | |
| AC08 | Bấm "Mua hàng" kiểm tra lại tồn kho; có SP không đủ → reload Cart + "Sản phẩm vừa được cập nhật lại." | DEV-3648 AC08 | High | Xem DT2 |
| AC09 | SP OOS không bị tự xoá; có hàng trở lại thì checkbox Enable lại | DEV-3648 AC09 | Medium | |
| AC10 | SP OOS bị đẩy xuống cuối Cart, giữ thứ tự tương đối của cả 2 nhóm | DEV-3648 AC10 | Medium | |

## 4a. Mệnh đề nguồn

| Clause_ID | Req_ID | Mệnh đề (bám sát nguyên văn) | CO | Ghi chú |
|---|---|---|---|---|
| AC01-c1 | AC01 | Sản phẩm còn hàng được phép tick/un-tick | CO-01 | |
| AC01-c2 | AC01 | Sản phẩm được tick được đưa vào danh sách Checkout | CO-02 | |
| AC01-c3 | AC01 | Button "Mua hàng" Enable khi có ít nhất một sản phẩm còn hàng được tick | CO-10 | |
| AC01-c4 | AC01 | Khách hàng có thể tiếp tục Checkout với các sản phẩm đã được chọn | CO-02; CO-03 | |
| AC02-c1 | AC02 | Sản phẩm hết hàng được tự động bỏ tick | CO-04; CO-07 | |
| AC02-c2 | AC02 | Checkbox của sản phẩm hết hàng được Disable | CO-04; CO-05 | |
| AC02-c3 | AC02 | Sản phẩm hết hàng không được đưa vào Checkout | CO-06 | |
| AC02-c4 | AC02 | Sản phẩm hết hàng vẫn được giữ lại trong Cart, không tự động xóa | CO-04; CO-29 | |
| AC02-c5 | AC02 | Hiển thị thông báo "Sản phẩm hiện đang hết hàng" bên dưới sản phẩm hết hàng | CO-04; CO-38; CO-40 | Câu thông báo: Q-01 |
| AC03-c1 | AC03 | Product B được tự động uncheck | CO-08 | |
| AC03-c2 | AC03 | Checkbox của Product B được Disable | CO-08 | |
| AC03-c3 | AC03 | Product A và Product C vẫn cho phép tick/un-tick | CO-08 | |
| AC03-c4 | AC03 | Product B vẫn được giữ lại trong Cart | CO-08 | |
| AC03-c5 | AC03 | Nếu Product A hoặc Product C được tick, button "Mua hàng" được Enable | CO-09 | |
| AC03-c6 | AC03 | Click "Mua hàng": chỉ các sản phẩm còn hàng và được tick được đưa sang Checkout | CO-09; CO-51 | |
| AC03-c7 | AC03 | Khách hàng không bắt buộc phải xóa Product B để tiếp tục Checkout | CO-09 | |
| AC04-c1 | AC04 | Có ≥ 1 sản phẩm còn hàng được tick → Enable | CO-10; CO-12 | DT1-R1 |
| AC04-c2 | AC04 | Không có sản phẩm còn hàng nào được tick → Disable | CO-11; CO-12; CO-49; CO-50 | DT1-R2 |
| AC04-c3 | AC04 | Tất cả sản phẩm đều hết hàng → Disable | CO-13; CO-67 | DT1-R3 |
| AC04-c4 | AC04 | Chỉ có sản phẩm hết hàng được tick: không xảy ra vì checkbox đã bị Disable | CO-05 | DT1-R4 |
| AC05-c1 | AC05 | Tất cả sản phẩm được tự động uncheck | CO-14 | |
| AC05-c2 | AC05 | Tất cả checkbox sản phẩm được Disable | CO-14 | |
| AC05-c3 | AC05 | Tất cả sản phẩm vẫn được giữ lại trong Cart | CO-14 | |
| AC05-c4 | AC05 | Hiển thị thông báo số lượng sản phẩm không có sẵn bên dưới từng sản phẩm | CO-14 | Câu thông báo: Q-01 |
| AC05-c5 | AC05 | Button "Mua hàng" được Disable | CO-13 | |
| AC05-c6 | AC05 | Khách hàng không thể Checkout | CO-13; CO-15 | |
| AC06-c1 | AC06 | Qty KH chọn > Saleable Qty: tự động điều chỉnh qty về available stock | CO-16; CO-62 | |
| AC06-c2 | AC06 | Keep tick box sản phẩm | CO-16; CO-18; CO-62 | |
| AC06-c3 | AC06 | Hiện message "Sản phẩm này chỉ còn số lượng là 1" | CO-16; CO-18; CO-62 | |
| AC06-c4 | AC06 | Cho phép tiếp tục checkout sau khi đã refresh số lượng về Saleable Qty | CO-17; CO-62 | |
| AC06-c5 | AC06 | Cố tình điều chỉnh số lượng lên nhiều hơn nữa → qty tự về Saleable Qty | CO-18 | |
| AC06-c6 | AC06 | Insufficient Stock khác với trường hợp hết hàng hoàn toàn | CO-16; CO-26; CO-48; CO-63; CO-68 | Phân biệt: giữ tick vs bỏ tick; không bị đẩy xuống cuối |
| AC07-c1 | AC07 | Hệ thống kiểm tra quantity mới không vượt quá tồn kho khả dụng | CO-19; CO-20; CO-21; CO-22 | Phạm vi chỉ SP đang được tick — SP bỏ tick: CO-52 |
| AC07-c2 | AC07 | Quantity ≤ Saleable Qty: giữ nguyên checkbox & cho phép checkout | CO-19; CO-20 | |
| AC07-c3a | AC07 | Quantity > Saleable Qty: tự điều chỉnh số lượng về avail qty | CO-21; CO-22 | |
| AC07-c3b | AC07 | Quantity > Saleable Qty: hiện thông báo "Sản phẩm này chỉ còn số lượng là..." | CO-21; CO-22 | |
| AC07-c3c | AC07 | Quantity > Saleable Qty: vẫn keep checkbox | CO-21; CO-22 | |
| AC08-c1 | AC08 | Click "Mua hàng": kiểm tra lại trạng thái tồn kho trước khi chuyển sang Checkout | CO-24; CO-25; CO-26 | |
| AC08-c2 | AC08 | Tất cả SP được chọn vẫn đủ stock → tiếp tục Checkout | CO-24; CO-47; CO-64 | |
| AC08-c3a | AC08 | Có SP không còn đủ quantity → Reload lại Cart | CO-25; CO-26; CO-48 | |
| AC08-c3b | AC08 | Có SP không còn đủ quantity → hiển thị thông báo chung "Sản phẩm vừa được cập nhật lại." | CO-25; CO-26; CO-48 | |
| AC08-c4a | AC08 | Stock = 0: Uncheck | CO-25; CO-49 | |
| AC08-c4b | AC08 | Stock = 0: Disable checkbox | CO-25; CO-49 | |
| AC08-c4c | AC08 | Stock = 0: message "Sản phẩm hiện đang hết hàng" | CO-25 | Q-01 |
| AC08-c5a | AC08 | Stock > 0 nhưng qty > Saleable Qty: tự điều chỉnh lại qty về số lượng còn avail | CO-26; CO-65 | |
| AC08-c5b | AC08 | Stock > 0 nhưng qty > Saleable Qty: message "Sản phẩm này chỉ còn số lượng là..." | CO-26 | |
| AC08-c5c | AC08 | Stock > 0 nhưng qty > Saleable Qty: keep checkbox | CO-26; CO-65 | |
| AC08-c6 | AC08 | Các SP khác vẫn hợp lệ giữ nguyên trạng thái lựa chọn | CO-27; CO-48 | |
| AC08-c7 | AC08 | Sau khi review/điều chỉnh, KH bấm Mua hàng để revalidate và Checkout lại | CO-28; CO-65 | |
| AC09-c1 | AC09 | Không tự động remove sản phẩm khỏi Cart | CO-29 | |
| AC09-c2 | AC09 | Sản phẩm vẫn được hiển thị trong Cart | CO-29 | |
| AC09-c3 | AC09 | Sản phẩm không thể được chọn để Checkout | CO-05; CO-06 | |
| AC09-c4 | AC09 | Khi có hàng trở lại, checkbox có thể được Enable lại theo logic kiểm tra tồn kho | CO-30; CO-69 | Tick / vị trí sau khi Enable: Q-06; hàng về < qty: Q-21 |
| AC10-c1 | AC10 | Các sản phẩm còn hàng được hiển thị ở phía trên | CO-32 | |
| AC10-c2 | AC10 | Các sản phẩm hết hàng được tự động di chuyển xuống cuối danh sách Cart | CO-08; CO-32; CO-68 | |
| AC10-c3 | AC10 | Thứ tự của các sản phẩm còn hàng được giữ nguyên như trước khi sắp xếp | CO-32; CO-58 | "Trước khi sắp xếp": Q-15 |
| AC10-c4 | AC10 | Thứ tự của các sản phẩm hết hàng được giữ nguyên như trước khi sắp xếp | CO-32 | Q-15 |
| AC10-c5 | AC10 | Còn hàng → hết hàng: tự động cập nhật vị trí xuống cuối Cart sau khi trạng thái tồn kho cập nhật | CO-33; CO-58; CO-66 | |
| BR-01-c1 | BR-01 | Enable khi có ít nhất một SP còn hàng và được tick | CO-10 | |
| BR-01-c2 | BR-01 | Disable khi không có SP nào đồng thời Còn hàng + Được tick | CO-11; CO-13; CO-49; CO-50; CO-67 | |
| BR-02-c1 | BR-02 | Saleable Qty = 0 → xử lý như hết hàng (uncheck, Disable, thông báo, xuống cuối) | CO-04; CO-07; CO-53; CO-63 | Định nghĩa "hết hàng": Q-14 |
| BR-03-c1 | BR-03 | 0 < Saleable Qty < qty → qty = Saleable Qty, giữ tick, thông báo số lượng | CO-16; CO-21; CO-26; CO-62; CO-63 | |
| IMP-01-c1 | IMP-01 | Tóm tắt đơn hàng chỉ tính SP còn hàng được tick | CO-34; CO-35; CO-55; CO-56 | |
| IMP-02-c1 | IMP-02 | SP không được chọn vẫn nằm lại trong Cart sau khi đặt hàng | CO-36 | |
| IMP-03-c1 | IMP-03 | Mini-cart vẫn hiển thị SP khi tất cả SP hết hàng | CO-37; CO-46 | |
| IMP-04-c1 | IMP-04 | Mỗi SP OOS chỉ hiển thị một thông báo, không lặp sau reload | CO-38 | |
| IMP-05-c1 | IMP-05 | Bấm "Mua hàng" 2 lần liên tiếp không gây lỗi / không nhân đôi SP | CO-39 | |

## 5. Quy tắc nghiệp vụ

| Req_ID | Điều kiện | Kết quả | Nguồn |
|---|---|---|---|
| BR-01 | Tồn tại ≥1 SP đồng thời *Còn hàng* + *Được tick* | Nút "Mua hàng" Enable; ngược lại Disable | AC04 Business Rule |
| BR-02 | Saleable Qty = 0 | OOS: uncheck, Disable, thông báo hết hàng, đẩy xuống cuối | AC02, AC08 ("Stock = 0"), AC10 |
| BR-03 | 0 < Saleable Qty < qty khách chọn | Insufficient Stock: qty = Saleable Qty, giữ tick, thông báo "Sản phẩm này chỉ còn số lượng là N" | AC06, AC07, AC08 |

## 6. Yêu cầu ngầm định

| Req_ID | Mô tả | Cơ sở | Trạng thái xác nhận |
|---|---|---|---|
| IMP-01 | Khung "Tóm tắt đơn hàng" (TỔNG (N SẢN PHẨM), tạm tính) chỉ tính SP còn hàng được tick, cập nhật khi tick / tồn kho / qty thay đổi | Bug DEV-3745, DEV-3746 (tiêu đề) | Đề xuất |
| IMP-02 | Sau khi đặt hàng, SP không được chọn (OOS hoặc bị untick) vẫn nằm lại trong Cart | Tiêu đề child DEV-3654 "giữ SP leftover sang quote mới khi checkout" | Đề xuất |
| IMP-03 | Mini-cart vẫn hiển thị SP khi tất cả SP trong Cart hết hàng | Child DEV-3653 + bug DEV-3768 | Đề xuất |
| IMP-04 | Mỗi SP OOS chỉ hiển thị **một** thông báo, không lặp sau reload | Bug DEV-3766 | Đề xuất |
| IMP-05 | Bấm "Mua hàng" 2 lần liên tiếp không gây lỗi / không nhân đôi sản phẩm | Error guessing | Đề xuất |

## 7. Từ điển dữ liệu

| Trường | Kiểu | Bắt buộc | Giới hạn / Miền giá trị | Mặc định | Thông điệp (nguyên văn, kèm nguồn) |
|---|---|---|---|---|---|
| Checkbox sản phẩm | Checkbox | – | Còn hàng: Enable · OOS: Disable + bỏ tick | ? (Q-02) | – |
| Checkbox "Tất cả sản phẩm" | Checkbox | – | ? (Q-03) | ? | – (chỉ có trong ảnh hiện trạng) |
| Số lượng (qty) | Ô nhập số nguyên (ảnh hiện trạng không có nút +/-) | Có | 1 ≤ qty ≤ Saleable Qty (min chưa nêu — Q-05); SP OOS có sửa được không — Q-18 | qty đã thêm | "Sản phẩm này chỉ còn số lượng là 1" (AC06), "Sản phẩm này chỉ còn số lượng là..." (AC07, AC08) |
| Trạng thái tồn kho | – | – | Saleable Qty = 0 → OOS (các trường hợp khác — Q-14) | – | "Sản phẩm hiện đang hết hàng" (AC02, AC08, DEV-3656) · "số lượng sản phẩm không có sẵn" (AC05) · "Số lượng sản phẩm không có sẵn" (ảnh hiện trạng) — Q-01 |
| Banner revalidate | – | – | Hiện khi Mua hàng phát hiện SP được chọn không đủ tồn kho | – | "Sản phẩm vừa được cập nhật lại." (AC08) |

### 7.1 Phân vùng tương đương & giá trị biên

| Trường | Phân vùng hợp lệ | Phân vùng không hợp lệ | Biên · đơn vị bước · mức coverage |
|---|---|---|---|
| qty so với Saleable Qty (= 5) | 1 ≤ qty ≤ 5 | qty > 5; qty < 1 (chưa xác nhận — Q-05) | 4/5/6 · ±1 · 3-value phía max (rủi ro tồn kho); đại diện invalid xa: 999 |
| Saleable Qty | > 0 (còn hàng) | = 0 (OOS); các cách "hết hàng" khác (Q-14) | 0/1 — biên 1 nằm trong AC06 (2 → 1) |
| Số SP còn hàng được tick | ≥ 1 | 0 | 0/1 · ±1 · 2-value |

## 8. Trạng thái & chuyển đổi — một dòng sản phẩm trong Cart

| Trạng thái hiện tại | Sự kiện | Guard | Trạng thái kế tiếp | Nguồn |
|---|---|---|---|---|
| Còn hàng – Tick | Khách untick | | Còn hàng – Untick | AC01 |
| Còn hàng – Untick | Khách tick | | Còn hàng – Tick | AC01 |
| Còn hàng – Tick | Tồn kho về 0, Cart tải lại / bấm Mua hàng | | OOS (untick, disable, xuống cuối) | AC02, AC08, AC10 |
| Còn hàng – Tick | Tồn kho giảm < qty | Saleable Qty > 0 | qty = Saleable Qty, vẫn Tick | AC06, AC08 |
| Còn hàng – Tick | Khách tăng qty > Saleable Qty | | qty = Saleable Qty, vẫn Tick | AC06, AC07 |
| OOS | Có hàng trở lại | Saleable Qty > 0 | Còn hàng (checkbox Enable; tick hay không — Q-06) | AC09 |

Chuyển đổi **không hợp lệ** chọn để kiểm tra: OOS → Tick (checkbox bị khoá) — rủi ro SP hết hàng lọt vào đơn.

### 8.1 Ma trận trạng thái

Sự kiện: E1 khách click checkbox · E2 khách nhập qty > Saleable Qty · E3 tồn kho về 0 · E4 tồn kho giảm còn 0 < Saleable Qty < qty · E5 tồn kho tăng lại (> 0) · E6 khách xoá dòng · E7 khách bấm "Mua hàng".

| Trạng thái \ Sự kiện | E1 click checkbox | E2 nhập qty > Saleable | E3 tồn kho = 0 | E4 0 < tồn kho < qty | E5 tồn kho tăng lại | E6 xoá dòng | E7 bấm Mua hàng |
|---|---|---|---|---|---|---|---|
| Còn hàng – Tick | → Còn hàng – Untick (AC01) · CO-01 | → Đã điều chỉnh: qty = Saleable, vẫn Tick (AC07) · CO-21 | → OOS (AC02, AC08) · CO-07; CO-25; CO-50 | → Đã điều chỉnh: qty = Saleable, vẫn Tick (AC06, AC08) · CO-16; CO-26; CO-62 | Không đổi (đã còn hàng) | → Xoá khỏi Cart; nếu là SP được tick duy nhất thì nút Disable (BR-01) · CO-67 | → Revalidate, sang Checkout nếu đủ (AC08) · CO-24; CO-64 |
| Còn hàng – Tick, đã điều chỉnh (đang hiện thông báo số lượng) | → Còn hàng – Untick (AC01) · CO-01 | → qty về Saleable, không giữ số khách chọn (AC06) · CO-18 | → OOS (AC02, AC08) · CO-25 | → điều chỉnh tiếp về Saleable mới (BR-03) · CO-26 | Q-24 (khôi phục qty ban đầu? thông báo còn hiện?) · CO-72 | → Xoá khỏi Cart (chức năng hiện có) · CO-67 | → Revalidate với qty đã điều chỉnh (AC08-c7) · CO-17; CO-65 |
| Còn hàng – Untick | → Còn hàng – Tick (AC01) · CO-01 | Q-13 · CO-52 | → OOS (AC02) · CO-04; CO-47 | Q-22 (có tự điều chỉnh khi tải trang? tick lại có kiểm tra ngay?) · CO-70 | Không đổi | → Xoá khỏi Cart (chức năng hiện có, ngoài phạm vi AC) | Không đưa SP này vào Checkout (AC01) · CO-02 |
| OOS | Bị chặn (AC02, AC04) · CO-05 | Q-18 (ô số lượng của SP OOS có sửa được không) · CO-59 | Không đổi (AC09) · CO-29 | Không khả thi - tồn kho đã bằng 0 | Saleable Qty ≥ qty: → Còn hàng, checkbox Enable (AC09); tick / vị trí: Q-06 · CO-30; CO-57 · 0 < Saleable Qty < qty: Q-21 · CO-69 | → Xoá khỏi Cart (ảnh hiện trạng có icon xoá) · CO-31 | Không đưa SP này vào Checkout (AC02) · CO-06 |

## 9. Bảng quyết định

**DT1 — Nút "Mua hàng" (AC04 / BR-01)**

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| C1: Cart có ≥1 SP còn hàng | Y | Y | N | – |
| C2: Có ≥1 SP còn hàng được tick | Y | N | – | – |
| C3: Chỉ SP OOS được tick | – | – | – | Y |
| **Nút "Mua hàng"** | Enable | Disable | Disable | Không khả thi (checkbox OOS bị Disable) — kiểm tra việc không tick được |

**DT2 — Kết quả khi bấm "Mua hàng" (AC08)** — xét theo **từng dòng** và theo cả tập

| | R1a | R1b | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|---|
| C1: Dòng có thay đổi tồn kho đang được tick | – (không có thay đổi) | Y | Y | Y | Y (2 dòng) | N |
| C2: Tồn kho mới của dòng được tick | – | Giảm nhưng Saleable Qty ≥ qty (biên = qty) | Saleable Qty = 0 | 0 < Saleable Qty < qty | Một dòng = 0, một dòng thiếu số lượng | – |
| **Kết quả** | Sang Checkout | Sang Checkout, không reload, không banner | Reload Cart + banner; dòng đó uncheck, Disable, thông báo hết hàng | Reload Cart + banner; qty = Saleable Qty, giữ tick, thông báo số lượng | Reload Cart + một banner; mỗi dòng xử lý theo kiểu của nó | Sang Checkout (AC08 "tất cả SP được chọn vẫn đủ stock") — có reload không: Q-16 |
| CO | CO-24 | CO-64 | CO-25 | CO-26 | CO-48 | CO-47 |

Tổ hợp bị loại: không có (v1.1 loại R4 với lý do "CO-26 kiểm tra SP khác giữ nguyên" — không chứng minh được hành vi không đổi, nên v2.0 đưa R4 vào).

**Tập phần tử** (DT1 và DT2 áp dụng cho từng dòng Cart; hành động tổng hợp: trạng thái nút "Mua hàng", banner chung, Tóm tắt đơn hàng):

| Mục | Áp dụng? | CO / lý do |
|---|---|---|
| Phần tử ngoài tập được chọn chịu cùng sự kiện | Có — dòng không được tick đổi tồn kho lúc bấm Mua hàng | CO-47 |
| Phần tử duy nhất thoả điều kiện chuyển sang không thoả (tập rỗng) | Có — dòng được tick duy nhất hết hàng: khi tải lại / khi bấm Mua hàng; bị khách xoá | CO-50; CO-49; CO-67 |
| ≥ 2 phần tử thuộc các rule khác nhau cùng lúc | Có — khi bấm Mua hàng (DT2-R4) và khi mở / tải lại Cart | CO-48; CO-63 |
| Tập rỗng · 1 phần tử · tất cả phần tử cùng rule | Tập rỗng (giỏ trống): N/A - không có nút Mua hàng, hành vi giỏ trống có sẵn, ngoài phạm vi · 1 phần tử OOS: N/A - cùng rule với "tất cả OOS" (CO-13, CO-14) · tất cả còn hàng được tick: CO-03 | CO-03; CO-13; CO-14 |

## 9a. Ma trận tương tác

| IX_ID | Thực thể / trạng thái | A — yêu cầu thay đổi | B — yêu cầu phụ thuộc | Câu hỏi kiểm thử | Kết luận |
|---|---|---|---|---|---|
| IX-01 | Trạng thái tick | AC02 (tự bỏ tick khi tải lại) | AC04 (nút Mua hàng) | SP được tick **duy nhất** hết hàng → tập "còn hàng + tick" rỗng → nút có chuyển Disable? | CO-50 |
| IX-02 | Trạng thái tick | AC08 (revalidate bỏ tick) | AC04 | Sau revalidate, SP được tick duy nhất bị bỏ tick → nút Disable? | CO-49 |
| IX-03 | Trạng thái tick | AC02 (SP chuyển OOS) | IMP-01 (Tóm tắt đơn hàng) | Tổng tiền / N có loại SP vừa hết hàng ra không? | CO-55 |
| IX-04 | Số lượng | AC06 / AC08 (tự điều chỉnh qty) | IMP-01 | Tạm tính và tổng có cập nhật theo qty mới? | CO-56 |
| IX-05 | Trạng thái tick, vị trí | AC09 (có hàng trở lại) | AC10 (thứ tự), AC04 | SP có hàng lại quay về vị trí nào; có tự tick làm nút Enable không? | CO-30; CO-57 |
| IX-06 | Số lượng | AC07 (khách đổi qty) | AC01 (SP bỏ tick) | Đổi qty của SP đang bỏ tick có kiểm tra Saleable Qty / tự tick không? | Pending - Q-13 |
| IX-07 | Trạng thái tick | AC01 (khách bỏ tick) | AC08 (phạm vi revalidate) | SP bỏ tick đổi tồn kho có làm chặn checkout không? | CO-47 |
| IX-08 | Số lượng | AC06 (qty đã tự điều chỉnh khi tải lại) | AC08 (revalidate) | Bấm Mua hàng sau khi đã điều chỉnh thì qua revalidate? | CO-17 |
| IX-09 | Thứ tự, trạng thái tick | AC10 (sắp xếp lại khi có SP chuyển OOS) | AC01 (trạng thái tick của từng SP) | Khi dòng đầu chuyển OOS và các dòng khác dịch lên, trạng thái tick có đi theo đúng SP (không theo vị trí)? | CO-58 |
| IX-10 | Danh sách SP | AC02 (SP OOS ở lại Cart) | IMP-03 (Mini-cart) | Mini-cart hiển thị / đếm SP OOS thế nào khi Cart hỗn hợp? | CO-46 |
| IX-11 | Danh sách SP | AC01 (chỉ SP được tick vào đơn) | IMP-02 (SP còn lại sau đặt hàng) | SP không chọn có ở lại Cart sau khi đặt hàng? | CO-36 |
| IX-12 | Danh sách SP | AC03 (SP được tick sang Checkout) | AC02 (OOS không vào Checkout) | Bỏ qua bước Mua hàng (URL trực tiếp) có lọt SP bỏ tick / OOS? | CO-51 |
| IX-13 | Thứ tự, trạng thái tick | AC08 (revalidate làm SP được tick thành OOS → AC10 đẩy xuống cuối) | AC01, AC08-c6 (giữ lựa chọn của SP khác) | Sau revalidate, tick có đi theo đúng SP khi các dòng dịch vị trí? | CO-66 |
| IX-14 | Trạng thái tick | Xoá dòng (E6) | AC04 / BR-01, AC05 | Xoá SP còn hàng được tick duy nhất → Cart chỉ còn SP OOS → nút Disable? | CO-67 |
| IX-15 | Vị trí | AC06 (SP thiếu số lượng, vẫn còn hàng) | AC10 (chỉ SP hết hàng xuống cuối) | SP thiếu số lượng có bị đẩy xuống cuối nhầm? | CO-68 |
| IX-16 | Số lượng | AC09 (có hàng trở lại) | BR-03 | Hàng về ít hơn qty trong Cart thì qty / thông báo / tick ra sao? | Pending - Q-21 |

## 9b. Sự kiện kích hoạt & kênh

| EV_ID | Hành vi | Sự kiện kích hoạt / kênh | Kết luận |
|---|---|---|---|
| EV-01 | Phát hiện OOS / thiếu số lượng | Lần đầu vào / mở lại trang Giỏ hàng | CO-04; CO-62; CO-63 |
| EV-02 | Phát hiện OOS / thiếu số lượng | Tải lại trang (F5) khi tồn kho đã đổi | CO-07; CO-16 |
| EV-03 | Phát hiện OOS / thiếu số lượng | Tồn kho đổi khi đang mở Cart, không tải lại, chưa bấm gì (realtime?) | Pending - Q-04 |
| EV-04 | Phát hiện OOS / thiếu số lượng | Bấm "Mua hàng" | CO-25; CO-26 |
| EV-05 | Hiển thị SP OOS | Kênh thứ hai: mini-cart / badge header | CO-37; CO-46 |
| EV-06 | Chỉ SP được chọn sang Checkout | Truy cập thẳng URL Checkout (bỏ qua Mua hàng) | CO-15; CO-51 |
| EV-07 | Trạng thái tick | Back từ trang Checkout về Giỏ hàng | Pending - Q-09 |
| EV-08 | Trạng thái tick | Tab / thiết bị thứ hai cùng tài khoản | Pending - Q-17 |
| EV-09 | SP OOS được giữ | Đăng xuất – đăng nhập lại | CO-29 |
| EV-10 | Bấm Mua hàng | Double-click / bấm liên tiếp | CO-39 |
| EV-11 | Toàn bộ tính năng | Khách vãng lai (chưa đăng nhập) | Pending - Q-09 |
| EV-12 | Revalidate | Tồn kho đổi sau khi đã sang trang Checkout, trước khi đặt hàng | N/A - trang Checkout ngoài phạm vi (§2); ghi vào rủi ro §15 |
| EV-13 | Banner / thông báo | Website chạy tiếng Anh | Pending - Q-10 |
| EV-14 | Chỉ SP được chọn sang Checkout, revalidate | Lối vào Checkout / sửa qty khác nút "Mua hàng" (mini-cart, "Mua ngay"…) — DEV-3653 | Pending - Q-23 |

## 11. Tích hợp & phụ thuộc

- Tồn kho theo **Saleable Qty** của Magento. Dữ liệu test cần quyền admin để đổi tồn kho (SETUP-02, SETUP-03).
- Mini-cart (DEV-3653), quote mới cho SP còn lại (DEV-3654), Gift-popup/Amasty (DEV-3649), Bundle (DEV-3730).

## 12. Quan sát UI (ảnh image-20260812-035015.png — hiện trạng trước tính năng)

| Màn hình | Thành phần | Ghi chú / chênh lệch so với văn bản |
|---|---|---|
| Giỏ hàng | Checkbox "Tất cả sản phẩm" ở đầu danh sách | AC không mô tả → Q-03 |
| Giỏ hàng | Dòng OOS (BOSS) nằm **đầu** danh sách | Trái AC10 — đây là hiện trạng cũ |
| Giỏ hàng | Thông báo OOS: hộp nền đỏ nhạt, icon cảnh báo, "Số lượng sản phẩm không có sẵn" | Khác AC02 → Q-01; thiết kế mới có giữ kiểu hộp này không → Q-19 |
| Giỏ hàng | Ô Số lượng là ô nhập số, không thấy nút +/- | Case nhập qty bằng ô số |
| Giỏ hàng | Icon yêu thích / sửa / xoá trên mỗi dòng | Khách vẫn có thể tự xoá SP OOS |
| Giỏ hàng | KENZO, HUGO áo thun: Giá ≠ Tạm tính (giảm 40%) | Fixture phải mô tả giá bán (SETUP-01) |
| Tóm tắt đơn hàng | "TỔNG (8 SẢN PHẨM)" 55.870.000 ₫ với 4 dòng hiển thị | Không cộng ra từ các dòng → không dùng làm oracle; Q-07 |

## 13. Câu hỏi làm rõ

| ID | Câu hỏi | Liên quan | Mức độ | Trả lời |
|---|---|---|---|---|
| Q-01 | Thông báo dưới SP OOS dùng câu nào: "Sản phẩm hiện đang hết hàng" (AC02, AC08, DEV-3656) hay "Số lượng sản phẩm không có sẵn." (AC05, ảnh hiện trạng)? Bug DEV-3766 cho thấy đang hiện cả hai. | AC02, AC05, IMP-04 | Major | (chờ) |
| Q-02 | Khi vào Cart, SP còn hàng được tick sẵn mặc định hay không? (ảnh hiện trạng đang tick sẵn) | AC01, AC04 | Major | (chờ) |
| Q-03 | Checkbox "Tất cả sản phẩm": tick tất cả có bỏ qua SP OOS không? Khi có SP OOS / tất cả OOS thì hiển thị trạng thái gì? | AC01, AC05 | Major | (chờ) |
| Q-04 | Hệ thống phát hiện tồn kho thay đổi lúc nào: chỉ khi tải lại Cart / bấm Mua hàng, hay realtime khi khách đang mở Cart? | AC06, AC10 | Major | (chờ) |
| Q-05 | Số lượng tối thiểu là bao nhiêu? Nhập 0, số âm, chữ vào ô Số lượng thì xử lý thế nào? | AC07 | Minor | (chờ) |
| Q-06 | SP có hàng trở lại: checkbox Enable nhưng tự tick lại hay để bỏ tick? Quay về vị trí cũ hay vẫn ở cuối? | AC09, AC10 | Major | (chờ) |
| Q-07 | "TỔNG (N SẢN PHẨM)" đếm theo số dòng hay tổng qty? Có tính quà tặng (DEV-3745) không? Không tick SP nào thì hiển thị gì (DEV-3746, DEV-3770)? | IMP-01 | Major | (chờ) |
| Q-08 | Cần đặc tả cho Gift-popup/Amasty (DEV-3649, DEV-3363), Bundle/Set (DEV-3730) và Mini-cart (DEV-3653): badge đếm SP nào, hiển thị SP OOS thế nào? | IMP-03 | Major | (chờ) |
| Q-09 | Tính năng áp dụng cho khách vãng lai (guest) không? Trạng thái tick có được lưu khi reload, Back từ Checkout, đăng nhập lại, sau khi đặt hàng không? | AC01 | Minor | (chờ) |
| Q-10 | Banner "Sản phẩm vừa được cập nhật lại." hiển thị ở đâu, tự ẩn không? Nội dung khi website chạy tiếng Anh? (DEV-3747) | AC08 | Minor | (chờ) |
| Q-11 | AC10: khi SP còn hàng chuyển sang OOS, nó đứng **cuối cùng** danh sách hay chen vào nhóm OOS theo thứ tự ban đầu? | AC10 | Minor | (chờ) |
| Q-12 | Truy cập thẳng URL trang Checkout (bỏ qua nút Mua hàng) thì xử lý thế nào: chuyển về Cart, hay Checkout chỉ với SP được tick? | AC03, AC05 | Major | (chờ) |
| Q-13 | AC07 chỉ nêu SP đang được tick: đổi qty của SP **đang bỏ tick** có kiểm tra Saleable Qty không, có tự tick lại không? | AC07 | Major | (chờ) |
| Q-14 | "Hết hàng" xác định thế nào: chỉ Saleable Qty = 0, hay cả Stock Status = Out of Stock khi qty > 0, backorder, Out-of-Stock Threshold, SP bị disable/xoá? | AC02, BR-02 | Major | (chờ) |
| Q-15 | "Thứ tự trước khi hệ thống sắp xếp" (AC10) là thứ tự hiển thị khi tất cả SP còn hàng (theo thứ tự thêm vào Cart, cũ → mới hay mới → cũ)? | AC10 | Major | (chờ) |
| Q-16 | AC08: SP **không được tick** thay đổi tồn kho lúc bấm Mua hàng thì vẫn sang Checkout ngay hay reload Cart + banner? | AC08 | Major | (chờ) |
| Q-17 | Cart mở ở 2 tab/thiết bị với trạng thái tick khác nhau: bấm Mua hàng ở tab nào thì lấy lựa chọn nào? | AC01 | Minor | (chờ) |
| Q-18 | Ô số lượng của SP hết hàng có sửa được không? Nếu sửa thì xử lý thế nào? | AC02, AC07 | Minor | (chờ) |
| Q-19 | Thông báo OOS có thiết kế UI mới không, hay giữ kiểu hộp nền đỏ nhạt + icon cảnh báo của giao diện hiện tại? | AC02 | Minor | (chờ) |
| Q-20 | Trạng thái tick của SP còn hàng có được giữ khi khách tải lại (F5) / rời rồi mở lại Cart không? Nếu SP được tick sẵn mặc định (Q-02), mỗi lần tải trang hệ thống có tick lại các SP khách đã bỏ tick không? (tách từ Q-09) | AC01, AC04 | Major | (chờ) |
| Q-21 | SP hết hàng có hàng trở lại nhưng Saleable Qty < qty trong Cart (vd. qty 3, hàng về 1): qty có tự điều chỉnh, có hiện "Sản phẩm này chỉ còn số lượng là..." không, checkbox tick hay bỏ tick? | AC09, BR-03 | Minor | (chờ) |
| Q-22 | SP **đang bỏ tick** có tồn kho giảm xuống 0 < Saleable Qty < qty: khi tải trang có tự điều chỉnh qty kèm thông báo như AC06 không? Khi khách tick lại SP này thì có kiểm tra tồn kho ngay không? | AC06, AC07 | Minor | (chờ) |
| Q-23 | Ngoài nút "Mua hàng" ở Giỏ hàng, còn lối nào vào Checkout hoặc sửa qty (nút thanh toán / sửa qty trong mini-cart, "Mua ngay" ở trang sản phẩm…)? Các lối đó có chỉ đưa SP được tick sang Checkout và có revalidate không? (DEV-3653) | AC01, AC02, AC08 | Major | (chờ) |
| Q-24 | Sau khi qty tự điều chỉnh, thông báo "Sản phẩm này chỉ còn số lượng là N" hiển thị đến khi nào (tải lại, khách giảm qty)? Khi có hàng trở lại, qty có được khôi phục về số khách chọn ban đầu không? | AC06, AC07 | Minor | (chờ) |

## 14. Giả định

| ID | Giả định | Câu hỏi liên quan | Case bị ảnh hưởng | Trạng thái xác nhận |
|---|---|---|---|---|
| AS-01 | Dùng "Sản phẩm hiện đang hết hàng" làm thông báo OOS (theo AC02/AC08, DEV-3656) | Q-01 | TC-CART-004, TC-CART-007, TC-CART-024, TC-CART-029, TC-CART-037, TC-CART-040 | Chưa xác nhận |
| AS-02 | SP còn hàng được tick sẵn khi vào Cart (theo ảnh hiện trạng) | Q-02 | TC-CART-001 | Chưa xác nhận |
| AS-03 | Thay đổi tồn kho được phát hiện khi tải lại Cart hoặc bấm "Mua hàng" | Q-04 | – (v2.1: không còn case dùng — kỳ vọng sau một lần tải trang đúng với mọi câu trả lời của Q-04; các case revalidate có bước xác minh trạng thái cũ thay cho giả định) | Chưa xác nhận |
| AS-04 | SP có hàng trở lại: checkbox Enable ở trạng thái bỏ tick | Q-06 | TC-CART-029 | Chưa xác nhận |
| AS-05 | "TỔNG (N SẢN PHẨM)" đếm tổng qty của SP được tick | Q-07 | TC-CART-033, TC-CART-045, TC-CART-046 | Chưa xác nhận |
| AS-06 | "Thứ tự trước khi sắp xếp" = thứ tự hiển thị quan sát được khi tất cả SP còn hàng | Q-15 | TC-CART-031, TC-CART-047 | Chưa xác nhận |
| AS-07 | Trạng thái tick của SP còn hàng được giữ nguyên qua tải lại / mở lại Cart (nếu Q-02 = "tick sẵn mỗi lần tải" thì CO-50 chỉ kiểm tra được qua nhánh revalidate — TC-CART-041) | Q-20 | TC-CART-007, TC-CART-043, TC-CART-045, TC-CART-047 | Chưa xác nhận |

## 15. Đánh giá rủi ro

| Khu vực | Khả năng (1–3) | Ảnh hưởng (1–3) | Điểm | Priority đề xuất |
|---|---|---|---|---|
| SP OOS / SP không chọn lọt vào Checkout / đặt hàng | 2 | 3 | 6 | P1 |
| Revalidate tồn kho khi bấm Mua hàng (đã có bug DEV-3747) | 3 | 3 | 9 | P1 |
| Khách không checkout được sau khi Cart tự điều chỉnh / revalidate → chặn bán hàng | 2 | 3 | 6 | P1 |
| Nút "Mua hàng" Enable khi có SP được tick | 2 | 3 | 6 | P1 |
| Nút "Mua hàng" vẫn Enable khi tập SP được tick thành rỗng (revalidate chặn được) | 2 | 2 | 4 | P2 |
| Điều chỉnh qty Insufficient Stock khi khách tự đổi qty | 2 | 2 | 4 | P2 |
| Tóm tắt đơn hàng tính sai (đã có bug DEV-3745/3746) | 3 | 2 | 6 | P2 |
| Trạng thái tick gắn theo vị trí thay vì theo SP khi Cart sắp xếp lại | 2 | 3 | 6 | P2 (revalidate không phát hiện được vì SP vẫn còn hàng) |
| Sắp xếp OOS xuống cuối | 2 | 1 | 2 | P3 |
| Tồn kho đổi giữa trang Checkout và đặt hàng (EV-12, ngoài phạm vi) | 2 | 3 | 6 | Ghi nhận — cần bộ test Checkout |

## 16. Điều kiện kiểm thử

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-01 | AC01 | Tick ↔ untick SP còn hàng | ST | TC-CART-001 | |
| CO-02 | AC01 | Chỉ SP được tick sang Checkout (Cart toàn SP còn hàng) | UC | TC-CART-002 | |
| CO-03 | AC01; BR-01 | Checkout với toàn bộ SP còn hàng được tick | UC | TC-CART-023 | v2.0: case cũ số 003 (Obsolete) gộp vào case này |
| CO-04 | AC02; BR-02 | SP OOS khi vào Cart: bỏ tick, Disable, thông báo, vẫn giữ | ST | TC-CART-004 | |
| CO-05 | AC02; AC03; AC04 | Chuyển đổi không hợp lệ OOS → Tick bị chặn (DT1-R4) | ST | TC-CART-005 | |
| CO-06 | AC02; AC09 | SP OOS không vào Checkout | UC | TC-CART-006 | |
| CO-07 | AC02; BR-02 | Còn hàng – Tick → OOS sau khi tải lại | ST | TC-CART-007 | |
| CO-08 | AC03; AC10 | Kịch bản A–B–C: trạng thái từng SP, B ở cuối | UC | TC-CART-008 | |
| CO-09 | AC03 | Checkout không cần xoá SP OOS | UC | TC-CART-009 | |
| CO-10 | AC04; BR-01 | DT1-R1: ≥1 SP còn hàng được tick → Enable | DT | TC-CART-010 | |
| CO-11 | AC04; AC01; BR-01 | DT1-R2: không SP còn hàng nào được tick → Disable | DT | TC-CART-011 | |
| CO-12 | AC04; BR-01 | Biên số SP được tick 1 ↔ 0 | BVA | TC-CART-012 | |
| CO-13 | AC04; AC05; BR-01 | DT1-R3: tất cả OOS → Disable | DT | TC-CART-013 | |
| CO-14 | AC05 | Hiển thị Cart khi tất cả OOS | UC | TC-CART-014 | |
| CO-15 | AC05 | Vào thẳng URL Checkout khi tất cả OOS | EG | TC-CART-015 | Hành vi chuyển hướng chờ Q-12 |
| CO-16 | AC06; BR-03 | Tồn kho 2 → 1 khi qty = 2 | ST | TC-CART-016 | |
| CO-17 | AC06 | Checkout sau khi qty đã tự điều chỉnh | UC | TC-CART-017 | |
| CO-18 | AC06; BR-03 | Cố tăng qty sau khi đã bị điều chỉnh | ST | TC-CART-018 | |
| CO-19 | AC07 | qty = 4 (max−1) | BVA | TC-CART-019 | |
| CO-20 | AC07 | qty = 5 (max) | BVA | TC-CART-020 | |
| CO-21 | AC07; BR-03 | qty = 6 (max+1) | BVA | TC-CART-021 | |
| CO-22 | AC07; BR-03 | qty rất lớn (đại diện invalid xa: 999) | EP | TC-CART-022 | |
| CO-23 | AC07 | qty < 1, số âm, chữ | EP | | Pending - Q-05 |
| CO-24 | AC08 | DT2-R1: đủ tồn kho → sang Checkout | DT | TC-CART-023 | |
| CO-25 | AC08; BR-02 | DT2-R2: SP được tick hết hàng lúc bấm Mua hàng | DT | TC-CART-024 | |
| CO-26 | AC08; BR-03 | DT2-R3: tồn kho < qty lúc bấm Mua hàng | DT | TC-CART-025 | |
| CO-27 | AC08 | SP hợp lệ khác giữ nguyên lựa chọn sau revalidate | DT | TC-CART-026 | |
| CO-28 | AC08 | Bấm Mua hàng lần 2 sau khi Cart cập nhật | UC | TC-CART-027 | |
| CO-29 | AC09 | SP OOS còn trong Cart qua reload, điều hướng, đăng nhập lại | ST | TC-CART-028 | |
| CO-30 | AC09 | OOS → Còn hàng: checkbox Enable lại | ST | TC-CART-029 | Trạng thái tick sau khi Enable chờ Q-06 |
| CO-31 | AC09; AC03 | Khách tự xoá SP OOS | CRUD | TC-CART-030 | |
| CO-32 | AC10 | Thứ tự hiển thị 2 nhóm khi Cart có SP chuyển OOS | ST | TC-CART-031 | |
| CO-33 | AC10 | Còn hàng → OOS chuyển xuống nhóm cuối | ST | TC-CART-032 | Vị trí trong nhóm chờ Q-11 |
| CO-34 | IMP-01; AC02 | Tóm tắt chỉ tính SP còn hàng được tick | EG | TC-CART-033 | |
| CO-35 | IMP-01 | Tóm tắt khi bỏ tick toàn bộ | EG | TC-CART-034 | |
| CO-36 | IMP-02; AC09 | SP không được chọn còn lại trong Cart sau đặt hàng | UC | TC-CART-035 | |
| CO-37 | IMP-03; AC05 | Mini-cart khi tất cả OOS | EG | TC-CART-036 | |
| CO-38 | IMP-04; AC02 | Không lặp thông báo sau nhiều lần reload | EG | TC-CART-037 | |
| CO-39 | IMP-05 | Double-click "Mua hàng" | EG | TC-CART-038 | |
| CO-40 | AC02 | Vị trí/hiển thị thông báo OOS | CL | TC-CART-039 | Thiết kế chờ Q-19 |
| CO-41 | AC01; AC05 | Checkbox "Tất cả sản phẩm" khi có SP OOS / tất cả OOS | DT | | Pending - Q-03 |
| CO-42 | AC01 | Khách vãng lai (guest) dùng selective checkout | UC | | Pending - Q-09 |
| CO-43 | AC08 | Banner revalidate khi website chạy tiếng Anh | EG | | Pending - Q-10 |
| CO-44 | AC09 | Gift-popup / Amasty khi Cart có SP OOS | UC | | Pending - Q-08 (chưa đọc DEV-3363) |
| CO-45 | AC01; AC03 | Bundle / Set có component hết hàng | DT | | Pending - Q-08 |
| CO-46 | IMP-03 | Badge / danh sách mini-cart khi Cart hỗn hợp | EG | | Pending - Q-08 |
| CO-47 | AC08 | DT2-R5: SP **không được tick** thay đổi tồn kho lúc bấm Mua hàng (IX-07) | DT | TC-CART-042 | |
| CO-48 | AC08; BR-02; BR-03 | DT2-R4: một SP hết hàng + một SP thiếu số lượng cùng lúc | DT | TC-CART-040 | |
| CO-49 | AC04; AC08 | SP được tick duy nhất hết hàng lúc Mua hàng → nút Disable sau revalidate (IX-02) | DT | TC-CART-041 | |
| CO-50 | AC02; AC04 | SP được tick duy nhất chuyển OOS khi tải lại → nút Disable (IX-01) | ST | TC-CART-043 | |
| CO-51 | AC03 | Vào thẳng URL Checkout khi Cart có SP bỏ tick / OOS (IX-12, EV-06) | EG | TC-CART-044 | |
| CO-52 | AC07 | Đổi qty của SP đang bỏ tick (IX-06) | EP | | Pending - Q-13 |
| CO-53 | AC02; BR-02 | Phân vùng "hết hàng" khác Saleable Qty = 0 | EP | | Pending - Q-14 |
| CO-54 | AC01 | Cart ở 2 tab/thiết bị (EV-08) | EG | | Pending - Q-17 |
| CO-55 | IMP-01; AC02 | Tóm tắt loại SP vừa chuyển OOS (IX-03) | EG | TC-CART-045 | |
| CO-56 | IMP-01; AC08 | Tóm tắt cập nhật theo qty đã tự điều chỉnh (IX-04) | EG | TC-CART-046 | |
| CO-57 | AC09; AC10 | Vị trí / trạng thái tick của SP có hàng trở lại (IX-05) | ST | | Pending - Q-06 |
| CO-58 | AC10; AC01 | Trạng thái tick đi theo SP khi Cart sắp xếp lại (IX-09) | ST | TC-CART-047 | |
| CO-59 | AC02; AC07 | Sửa qty của SP hết hàng (ma trận trạng thái OOS × E2) | EP | | Pending - Q-18 |
| CO-60 | AC06; AC02 | Tồn kho đổi khi đang mở Cart, không tải lại (EV-03) | EG | | Pending - Q-04 |
| CO-61 | AC01 | Trạng thái tick sau Back từ Checkout / đăng nhập lại (EV-07) | EG | | Pending - Q-09 |
| CO-62 | AC06; BR-03 | Tồn kho giảm xuống 0 < Saleable Qty < qty trước khi khách mở lại Cart (EV-01) | ST | TC-CART-048 | v2.1 phản biện F-03 |
| CO-63 | AC02; AC06; AC10; BR-02; BR-03 | 1 dòng OOS + 1 dòng thiếu số lượng cùng lúc khi mở / tải lại Cart | DT | TC-CART-049 | v2.1 F-04 |
| CO-64 | AC08 | DT2-R1b: tồn kho giảm nhưng Saleable Qty = qty lúc bấm Mua hàng | BVA | TC-CART-050 | v2.1 F-05 |
| CO-65 | AC08; AC06; BR-03 | Bấm Mua hàng lần 2 sau khi revalidate tự điều chỉnh qty | UC | TC-CART-051 | v2.1 F-06 |
| CO-66 | AC08; AC10; AC01 | Sau revalidate, SP vừa OOS xuống cuối và tick đi theo SP (IX-13) | ST | TC-CART-052 | v2.1 F-07 |
| CO-67 | AC04; BR-01; AC05 | Xoá SP còn hàng duy nhất được tick → nút Disable (IX-14) | DT | TC-CART-053 | v2.1 F-08 |
| CO-68 | AC10; AC06 | SP thiếu số lượng không bị đẩy xuống cuối (IX-15) | ST | TC-CART-054 | v2.1 F-13 |
| CO-69 | AC09; BR-03 | OOS có hàng trở lại với 0 < Saleable Qty < qty (IX-16) | ST | | Pending - Q-21 |
| CO-70 | AC06; AC07 | Tồn kho giảm dưới qty của SP đang bỏ tick; tick lại SP đó | ST | | Pending - Q-22 |
| CO-71 | AC01; AC08; AC02 | Lối vào Checkout / sửa qty khác nút "Mua hàng" (EV-14) | EG | | Pending - Q-23 |
| CO-72 | AC06; AC07 | Trạng thái "đã điều chỉnh" × có hàng lại / tải lại / giảm qty | ST | | Pending - Q-24 |

## 17. Dữ liệu test & setup

| Setup_ID | Dữ liệu / trạng thái | Cách tạo (điều khiển) | Cách xác minh (quan sát) | Cách reset | Nguồn dữ liệu | Trạng thái |
|---|---|---|---|---|---|---|
| SETUP-01 | Khách hàng customer01@test.com đã đăng nhập. 5 SP (map sang SKU thật cùng loại): **SP-A** HUGO Áo khoác racer da trơn slim fit — giá bán 15.780.000 ₫ · **SP-B** BOSS Áo khoác BOSS BY BECKHAM bằng da nappa — 36.280.000 ₫ · **SP-C** KENZO Áo thun cotton KENZO Cartoon Unisex — giá gốc 5.530.000 ₫, giá bán 3.318.000 ₫ (special price) · **SP-D** HUGO Áo thun cotton jersey in logo thêu nghệ thuật — giá gốc 2.640.000 ₫, giá bán 1.584.000 ₫ · **SP-E** SP còn hàng giá cố định. Tồn kho ban đầu (Saleable Qty): A 10, B 10, C 10, D 10, E 5. Không cart rule / quà tặng / phí ship ảnh hưởng tổng | Tạo tài khoản; admin chọn SKU, đặt giá bán (special price) và tồn kho ban đầu; thêm SP vào Cart theo Preconditions của từng case (SP chỉ thêm được khi còn hàng) | Cột Salable Quantity trong lưới sản phẩm admin; giá hiển thị trên trang chi tiết SP | Xoá toàn bộ Cart; admin trả giá và tồn kho về giá trị trong bảng này | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-02 | Tồn kho của SP theo yêu cầu từng case **trước lần tải trang Giỏ hàng tiếp theo** (lần mở đầu tiên, mở lại, hoặc F5 — vd. SP-B = 0 sau khi đã thêm vào Cart) | Thêm SP vào Cart khi còn hàng → admin sửa **Quantity** sao cho Salable Quantity = giá trị case (**không** đổi Stock Status — trường hợp đó thuộc CO-53 / Q-14) → chờ đến khi storefront phản ánh rồi mới tải trang Giỏ hàng | Trang chi tiết SP trên storefront hiển thị hết hàng (với Saleable Qty = 0) hoặc cột Salable Quantity trong admin đúng giá trị case — xác minh **trước** khi tải trang Giỏ hàng | Như SETUP-01 | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-03 | Đổi tồn kho **trong lúc tab khách đang mở Giỏ hàng và không tải lại**, để lần bấm "Mua hàng" tiếp theo (revalidate) thấy giá trị mới | Admin sửa Quantity (như SETUP-02) ở trình duyệt khác trong lúc tab khách đang mở | Trước khi bấm: trên tab khách, dòng bị đổi **vẫn hiển thị trạng thái cũ** (nếu Cart đã tự cập nhật thì dừng, ghi Blocked — Q-04); storefront (tab ẩn danh) đã phản ánh giá trị mới. **Chưa xác định**: giá trị mới có hiệu lực ngay với revalidate của phiên giỏ hàng đang mở không (indexer, cache) — cần dev xác nhận | Như SETUP-01 | Cần dev / QA lead cung cấp | Chưa rõ cách làm |
| SETUP-04 | Đặt hàng COD: tài khoản customer01@test.com có địa chỉ giao hàng mặc định; phương thức COD bật trên môi trường test | Thêm địa chỉ trong tài khoản; admin bật COD | Trang Checkout hiển thị COD | Huỷ đơn test trong admin | Cần chuẩn bị | Cần chuẩn bị |
