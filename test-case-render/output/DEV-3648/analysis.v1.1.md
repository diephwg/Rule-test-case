# Phân tích yêu cầu — DEV-3648 Giỏ hàng có sản phẩm hết hàng

| Thông tin | Giá trị |
|---|---|
| Người phân tích | AI agent (Claude) |
| Ngày | 2026-10-16 |
| Phiên bản phân tích | v1.1 (chuyển sang bộ rules đã sửa theo RULES-REVIEW) |

## 0. Danh mục nguồn

| Nguồn | Phiên bản / ngày | Trạng thái | Bản trích xuất | Phần bị ảnh hưởng nếu chưa đọc đủ |
|---|---|---|---|---|
| Jira [DEV-3648](https://sts-technical.atlassian.net/browse/DEV-3648) — Description AC01–AC10 | Updated 2026-10-16 | Đã đọc | `_extracted/jira-DEV-3648.md` | – |
| Ảnh `image-20260812-035015.png` (mockup Giỏ hàng) | 2026-09-23 | Đã xem | Mô tả trong `_extracted/jira-DEV-3648.md` | – |
| Ảnh `image-20260923-104852.png` | 2026-09-23 | **Chưa đọc được** | – | Bố cục UI, có thể ảnh hưởng AC02/AC10 và TC-CART-039 |
| Child tickets DEV-3649…3770 | – | Đọc một phần (chỉ tiêu đề; DEV-3656 đọc được mô tả) | `_extracted/jira-DEV-3648.md` | IMP-01…IMP-03, phần Gift-popup / Bundle / Mini-cart |
| Testcase tham chiếu DEV-3363 (SharePoint) | – | **Chưa đọc được** | – | Gift-popup / Amasty (CO-44) |

## 1. Tóm tắt tính năng

Hiện tại, khi Cart có ≥1 sản phẩm hết hàng (OOS), hệ thống báo lỗi và ẩn nút "Mua hàng", nên khách phải tự xoá sản phẩm OOS mới checkout được. Tính năng mới cho phép **checkout chọn lọc**: khách tick sản phẩm còn hàng để mua. Sản phẩm OOS tự bỏ tick, bị khoá checkbox, vẫn nằm lại trong Cart và bị đẩy xuống cuối. Hệ thống tự điều chỉnh số lượng khi tồn kho không đủ (Insufficient Stock) và kiểm tra lại tồn kho khi bấm "Mua hàng".

## 2. Phạm vi

**In-scope:** trang Giỏ hàng — tick/untick, trạng thái OOS, nút "Mua hàng", điều chỉnh qty theo Saleable Qty, revalidate trước Checkout, sắp xếp OOS xuống cuối, khung Tóm tắt đơn hàng, sản phẩm còn lại sau khi đặt hàng.

**Out-of-scope / chờ đặc tả:** Gift-popup / Amasty (DEV-3649), Bundle / Set (DEV-3730, DEV-3769, DEV-3770), trang Checkout & thanh toán (chỉ kiểm tra danh sách sản phẩm được chuyển sang), khách vãng lai (Q-09). Các phần này có điều kiện kiểm thử ở trạng thái *Pending*.

## 3. Tác nhân & phân quyền

| Vai trò | Mô tả | Quyền chính |
|---|---|---|
| Khách hàng (đã đăng nhập) | Mua hàng trên Front-row | Xem Cart, tick/untick, đổi qty, xoá SP, Mua hàng |
| Admin Magento | Chuẩn bị dữ liệu | Thay đổi tồn kho để đạt Saleable Qty cần test |

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

## 5. Quy tắc nghiệp vụ

| Req_ID | Điều kiện | Kết quả | Nguồn |
|---|---|---|---|
| BR-01 | Tồn tại ≥1 SP đồng thời *Còn hàng* + *Được tick* | Nút "Mua hàng" Enable; ngược lại Disable | AC04 Business Rule |
| BR-02 | Saleable Qty = 0 | OOS: uncheck, Disable, thông báo hết hàng, đẩy xuống cuối | AC02, AC08, AC10 |
| BR-03 | 0 < Saleable Qty < qty khách chọn | Insufficient Stock: qty = Saleable Qty, giữ tick, thông báo "Sản phẩm này chỉ còn số lượng là N" | AC06, AC07, AC08 |

## 6. Yêu cầu ngầm định

| Req_ID | Mô tả | Cơ sở | Trạng thái xác nhận |
|---|---|---|---|
| IMP-01 | Khung "Tóm tắt đơn hàng" (TỔNG (N SẢN PHẨM), tạm tính) chỉ tính SP còn hàng được tick | Mockup + bug DEV-3745, DEV-3746 | Đề xuất |
| IMP-02 | Sau khi đặt hàng, SP không được chọn (OOS hoặc bị untick) vẫn nằm lại trong Cart | Tiêu đề child DEV-3654 "giữ SP leftover sang quote mới khi checkout" | Đề xuất |
| IMP-03 | Mini-cart vẫn hiển thị SP khi tất cả SP trong Cart hết hàng | Child DEV-3653 + bug DEV-3768 | Đề xuất |
| IMP-04 | Mỗi SP OOS chỉ hiển thị **một** thông báo, không lặp sau reload | Bug DEV-3766 | Đề xuất |
| IMP-05 | Bấm "Mua hàng" 2 lần liên tiếp không gây lỗi / không nhân đôi sản phẩm | Error guessing | Đề xuất |

## 7. Từ điển dữ liệu

| Trường | Kiểu | Bắt buộc | Giới hạn / Miền giá trị | Mặc định | Thông điệp (nguyên văn, kèm nguồn) |
|---|---|---|---|---|---|
| Checkbox sản phẩm | Checkbox | – | Còn hàng: Enable · OOS: Disable + bỏ tick | ? (Q-02) | – |
| Checkbox "Tất cả sản phẩm" | Checkbox | – | ? (Q-03) | ? | – (chỉ có trong mockup) |
| Số lượng (qty) | Số nguyên | Có | 1 ≤ qty ≤ Saleable Qty (min chưa nêu — Q-05) | qty đã thêm | "Sản phẩm này chỉ còn số lượng là 1" (AC06), "Sản phẩm này chỉ còn số lượng là..." (AC07, AC08) |
| Trạng thái tồn kho | – | – | Saleable Qty = 0 → OOS | – | "Sản phẩm hiện đang hết hàng" (AC02, AC08) · "số lượng sản phẩm không có sẵn" (AC05) · "Số lượng sản phẩm không có sẵn" (mockup) — Q-01 |
| Banner revalidate | – | – | Hiện khi Mua hàng phát hiện SP không đủ tồn kho | – | "Sản phẩm vừa được cập nhật lại." (AC08) |

### 7.1 Phân vùng tương đương & giá trị biên

| Trường | Phân vùng hợp lệ | Phân vùng không hợp lệ | Biên · đơn vị bước · mức coverage |
|---|---|---|---|
| qty so với Saleable Qty (= 5) | 1 ≤ qty ≤ 5 | qty > 5; qty < 1 (chưa xác nhận — Q-05) | 4/5/6 · ±1 · 3-value phía max (rủi ro tồn kho); đại diện invalid xa: 999 |
| Saleable Qty | > 0 (còn hàng) | = 0 (OOS) | 0/1 — biên 1 nằm trong AC06 (2 → 1) |
| Số SP còn hàng được tick | ≥ 1 | 0 | 0/1 · ±1 · 2-value |

## 8. Trạng thái & chuyển đổi — một dòng sản phẩm trong Cart

| Trạng thái hiện tại | Sự kiện | Guard | Trạng thái kế tiếp | Nguồn |
|---|---|---|---|---|
| Còn hàng – Tick | Khách untick | | Còn hàng – Untick | AC01 |
| Còn hàng – Untick | Khách tick | | Còn hàng – Tick | AC01 |
| Còn hàng – Tick | Tồn kho về 0, Cart tải lại / bấm Mua hàng | | OOS (untick, disable, xuống cuối) | AC02, AC08, AC10 |
| Còn hàng – Tick | Tồn kho giảm < qty | Saleable Qty > 0 | Insufficient → qty = Saleable Qty, vẫn Tick | AC06, AC08 |
| Còn hàng – Tick | Khách tăng qty > Saleable Qty | | qty = Saleable Qty, vẫn Tick | AC06, AC07 |
| OOS | Có hàng trở lại | Saleable Qty > 0 | Còn hàng (checkbox Enable; tick hay không — Q-06) | AC09 |

Chuyển đổi **không hợp lệ** chọn để kiểm tra: OOS → Tick (checkbox bị khoá) — rủi ro SP hết hàng lọt vào đơn.

## 9. Bảng quyết định

**DT1 — Nút "Mua hàng" (AC04 / BR-01)**

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| C1: Cart có ≥1 SP còn hàng | Y | Y | N | – |
| C2: Có ≥1 SP còn hàng được tick | Y | N | – | – |
| C3: Chỉ SP OOS được tick | – | – | – | Y |
| **Nút "Mua hàng"** | Enable | Disable | Disable | Không khả thi (checkbox OOS bị Disable) — kiểm tra việc không tick được |

**DT2 — Kết quả khi bấm "Mua hàng" (AC08)**

| | R1 | R2 | R3 |
|---|---|---|---|
| Mọi SP được tick vẫn đủ tồn kho | Y | N | N |
| SP không đủ: Saleable Qty = 0 | – | Y | N |
| SP không đủ: 0 < Saleable Qty < qty | – | N | Y |
| **Kết quả** | Sang Checkout | Reload Cart + banner; SP uncheck, Disable, thông báo hết hàng | Reload Cart + banner; qty = Saleable Qty, giữ tick, thông báo số lượng |

Tổ hợp R2 + R3 cùng lúc (2 SP, mỗi SP một kiểu thiếu) khả thi nhưng không thêm điều kiện riêng — AC08 mô tả xử lý độc lập từng SP; CO-26 kiểm tra SP khác giữ nguyên trạng thái.

## 11. Tích hợp & phụ thuộc

- Tồn kho theo **Saleable Qty** của Magento. Dữ liệu test cần quyền admin để đổi tồn kho trong lúc khách đang mở Cart (SETUP-02).
- Mini-cart (DEV-3653), quote mới cho SP còn lại (DEV-3654), Gift-popup/Amasty (DEV-3649), Bundle (DEV-3730).

## 12. Quan sát UI (mockup image-20260812-035015.png)

| Màn hình | Thành phần | Ghi chú / chênh lệch so với văn bản |
|---|---|---|
| Giỏ hàng | Checkbox "Tất cả sản phẩm" ở đầu danh sách | AC không mô tả → Q-03 |
| Giỏ hàng | Dòng OOS (BOSS) nằm **đầu** danh sách | Mâu thuẫn với AC10 — có thể là mockup hiện trạng cũ |
| Giỏ hàng | Thông báo OOS trong mockup: "Số lượng sản phẩm không có sẵn" | Khác AC02 → Q-01 |
| Giỏ hàng | Icon yêu thích / sửa / xoá trên mỗi dòng | Khách vẫn có thể tự xoá SP OOS |
| Tóm tắt đơn hàng | "TỔNG (8 SẢN PHẨM)" trong khi chỉ thấy 4 dòng | Không rõ N đếm theo dòng hay tổng qty → Q-07 |

## 13. Câu hỏi làm rõ

| ID | Câu hỏi | Liên quan | Mức độ | Trả lời |
|---|---|---|---|---|
| Q-01 | Thông báo dưới SP OOS dùng câu nào: "Sản phẩm hiện đang hết hàng" (AC02, AC08) hay "Số lượng sản phẩm không có sẵn." (AC05, mockup)? Bug DEV-3766 cho thấy đang hiện cả hai. | AC02, AC05, IMP-04 | Major | (chờ) |
| Q-02 | Khi vào Cart, SP còn hàng được tick sẵn mặc định hay không? (mockup đang tick sẵn) | AC01, AC04 | Major | (chờ) |
| Q-03 | Checkbox "Tất cả sản phẩm": tick tất cả có bỏ qua SP OOS không? Khi có SP OOS / tất cả OOS thì hiển thị trạng thái gì? | AC01, AC05 | Major | (chờ) |
| Q-04 | Hệ thống phát hiện tồn kho thay đổi (AC06) lúc nào: chỉ khi tải lại Cart / bấm Mua hàng, hay realtime khi khách đang mở Cart? | AC06, AC10 | Major | (chờ) |
| Q-05 | Số lượng tối thiểu là bao nhiêu? Nhập 0, số âm, chữ vào ô Số lượng thì xử lý thế nào? | AC07 | Minor | (chờ) |
| Q-06 | SP có hàng trở lại: checkbox Enable nhưng tự tick lại hay để bỏ tick? Quay về vị trí cũ hay vẫn ở cuối? | AC09, AC10 | Major | (chờ) |
| Q-07 | "TỔNG (N SẢN PHẨM)" đếm theo số dòng hay tổng qty? Có tính quà tặng (DEV-3745) không? Không tick SP nào thì hiển thị gì (DEV-3746, DEV-3770)? | IMP-01 | Major | (chờ) |
| Q-08 | Cần đặc tả cho Gift-popup/Amasty (DEV-3649, DEV-3363), Bundle/Set (DEV-3730) và Mini-cart (DEV-3653): badge đếm SP nào, hiển thị SP OOS thế nào? | IMP-03 | Major | (chờ) |
| Q-09 | Tính năng áp dụng cho khách vãng lai (guest) không? Trạng thái tick có được lưu khi reload / đăng nhập thiết bị khác không? | AC01 | Minor | (chờ) |
| Q-10 | Banner "Sản phẩm vừa được cập nhật lại." hiển thị ở đâu, tự ẩn không? Nội dung khi website chạy tiếng Anh? (DEV-3747) | AC08 | Minor | (chờ) |
| Q-11 | AC10: khi SP còn hàng chuyển sang OOS, nó đứng **cuối cùng** danh sách hay chen vào nhóm OOS theo thứ tự ban đầu? | AC10 | Minor | (chờ) |
| Q-12 | AC05: tất cả SP OOS mà khách truy cập thẳng URL trang Checkout thì chuyển về đâu, hiển thị gì? | AC05 | Minor | (chờ) |

## 14. Giả định

| ID | Giả định | Câu hỏi liên quan | Case bị ảnh hưởng | Trạng thái xác nhận |
|---|---|---|---|---|
| AS-01 | Dùng "Sản phẩm hiện đang hết hàng" làm thông báo OOS (theo AC02/AC08) | Q-01 | TC-CART-004, 007, 008, 024, 029, 037 | Chưa xác nhận |
| AS-02 | SP còn hàng được tick sẵn khi vào Cart (theo mockup) | Q-02 | TC-CART-001 | Chưa xác nhận |
| AS-03 | Thay đổi tồn kho được phát hiện khi tải lại Cart hoặc bấm "Mua hàng" — case dùng F5 | Q-04 | TC-CART-007, 016, 017 | Chưa xác nhận |
| AS-04 | SP có hàng trở lại: checkbox Enable ở trạng thái bỏ tick | Q-06 | TC-CART-029 | Chưa xác nhận |
| AS-05 | "TỔNG (N SẢN PHẨM)" đếm tổng qty của SP được tick | Q-07 | TC-CART-033 | Chưa xác nhận |

## 15. Đánh giá rủi ro

| Khu vực | Khả năng (1–3) | Ảnh hưởng (1–3) | Điểm | Priority đề xuất |
|---|---|---|---|---|
| SP OOS lọt vào Checkout / đặt hàng | 2 | 3 | 6 | P1 |
| Revalidate tồn kho khi bấm Mua hàng (đã có bug DEV-3747) | 3 | 3 | 9 | P1 |
| Khách không checkout được sau khi Cart tự điều chỉnh / revalidate → chặn bán hàng | 2 | 3 | 6 | P1 |
| Nút "Mua hàng" Enable khi có SP được tick | 2 | 3 | 6 | P1 |
| Nút "Mua hàng" Disable khi không có SP được tick (lỗi chỉ gây lỗi dẫn sang Checkout rỗng, revalidate chặn được) | 2 | 2 | 4 | P2 |
| Điều chỉnh qty Insufficient Stock khi khách tự đổi qty | 2 | 2 | 4 | P2 |
| Tóm tắt đơn hàng tính sai (đã có bug DEV-3745/3746) | 3 | 2 | 6 | P2 |
| Sắp xếp OOS xuống cuối | 2 | 1 | 2 | P3 |

## 16. Điều kiện kiểm thử

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-01 | AC01 | Tick ↔ untick SP còn hàng | ST | TC-CART-001 | |
| CO-02 | AC01 | Chỉ SP được tick sang Checkout (Cart toàn SP còn hàng) | UC | TC-CART-002 | |
| CO-03 | AC01; BR-01 | Checkout với toàn bộ SP còn hàng được tick | UC | TC-CART-003 | |
| CO-04 | AC02; BR-02 | SP OOS khi vào Cart: bỏ tick, Disable, thông báo, vẫn giữ | ST | TC-CART-004 | |
| CO-05 | AC02; AC03; AC04 | Chuyển đổi không hợp lệ OOS → Tick bị chặn (DT1-R4) | ST | TC-CART-005 | |
| CO-06 | AC02; AC09 | SP OOS không vào Checkout | UC | TC-CART-006 | |
| CO-07 | AC02; BR-02 | Còn hàng – Tick → OOS sau khi tải lại | ST | TC-CART-007 | |
| CO-08 | AC03; AC10 | Kịch bản A–B–C: trạng thái từng SP và thứ tự | UC | TC-CART-008 | |
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
| CO-32 | AC10 | Thứ tự hiển thị 2 nhóm khi vào Cart | ST | TC-CART-031 | |
| CO-33 | AC10 | Còn hàng → OOS chuyển xuống nhóm cuối | ST | TC-CART-032 | Vị trí trong nhóm chờ Q-11 |
| CO-34 | IMP-01; AC02 | Tóm tắt chỉ tính SP còn hàng được tick | EG | TC-CART-033 | |
| CO-35 | IMP-01 | Tóm tắt khi bỏ tick toàn bộ | EG | TC-CART-034 | |
| CO-36 | IMP-02; AC09 | SP không được chọn còn lại trong Cart sau đặt hàng | UC | TC-CART-035 | |
| CO-37 | IMP-03; AC05 | Mini-cart khi tất cả OOS | EG | TC-CART-036 | |
| CO-38 | IMP-04; AC02 | Không lặp thông báo sau nhiều lần reload | EG | TC-CART-037 | |
| CO-39 | IMP-05 | Double-click "Mua hàng" | EG | TC-CART-038 | |
| CO-40 | AC02 | Vị trí/hiển thị thông báo OOS theo mockup | CL | TC-CART-039 | Cần đối chiếu ảnh image-20260923-104852.png |
| CO-41 | AC01; AC05 | Checkbox "Tất cả sản phẩm" khi có SP OOS / tất cả OOS | DT | | Pending - Q-03 |
| CO-42 | AC01 | Khách vãng lai (guest) dùng selective checkout | UC | | Pending - Q-09 |
| CO-43 | AC08 | Banner revalidate khi website chạy tiếng Anh | EG | | Pending - Q-10 |
| CO-44 | AC09 | Gift-popup / Amasty khi Cart có SP OOS | UC | | Pending - Q-08 (chưa đọc DEV-3363) |
| CO-45 | AC01; AC03 | Bundle / Set có component hết hàng | DT | | Pending - Q-08 |
| CO-46 | IMP-03 | Badge mini-cart đếm những SP nào | EG | | Pending - Q-08 |

## 17. Dữ liệu test & setup

| Setup_ID | Dữ liệu / trạng thái | Cách chuẩn bị | Cách reset | Nguồn dữ liệu |
|---|---|---|---|---|
| SETUP-01 | Khách hàng customer01@test.com đã đăng nhập. Sản phẩm (map sang SKU thật; giá theo mockup): **SP-A** HUGO Áo khoác racer da trơn slim fit — 15.780.000 ₫, Saleable Qty 10 · **SP-B** BOSS Áo khoác BOSS BY BECKHAM bằng da nappa — 36.280.000 ₫, Saleable Qty 0 · **SP-C** KENZO Áo thun cotton KENZO Cornate Unisex — tạm tính 3.318.000 ₫, Saleable Qty 10 · **SP-D** HUGO Áo thun cotton jersey in logo thêu nghệ thuật — tạm tính 1.584.000 ₫, Saleable Qty 0 · **SP-E** một SP còn hàng giá cố định, Saleable Qty 5 | Tạo tài khoản; chọn SKU tương ứng; admin đặt tồn kho; thêm SP vào Cart theo Preconditions của từng case | Xoá toàn bộ Cart; admin trả tồn kho về giá trị ban đầu trong bảng này | Cần chuẩn bị |
| SETUP-02 | Quyền admin Magento thay đổi tồn kho sao cho Saleable Qty đạt giá trị case yêu cầu, trong khi khách vẫn mở Cart ở tab/trình duyệt khác | Cấp tài khoản admin môi trường test; cách đổi tồn kho cụ thể cần dev/QA lead xác nhận (MSI: Quantity per Source, reservation) | Trả tồn kho về giá trị SETUP-01 sau mỗi case | Cần chuẩn bị |
