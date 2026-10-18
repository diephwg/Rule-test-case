# Review bộ test case — DEV-3648 Giỏ hàng có sản phẩm hết hàng

| Thông tin | Giá trị |
|---|---|
| Đối tượng review | `output/DEV-3648/testcases.csv` **v2.0** (47 dòng: 46 active, 1 Obsolete) và `output/DEV-3648/analysis.md` **v2.0** |
| Nguồn đối chiếu | `_extracted/jira-DEV-3648.md`, `_extracted/jira-DEV-3648-attachments.md`, 2 ảnh trong `_extracted/attachments/` (đã xem trực tiếp) |
| Người review | AI agent (Claude) — phản biện độc lập, không chung ngữ cảnh với người sinh; đọc nguồn và tự tách mệnh đề **trước** khi đọc analysis |
| Ngày | 2026-10-16 |
| Không tham khảo | các review / report / bản v1.x trước đó (theo yêu cầu, để tránh kế thừa kết luận cũ) |

## 1. Tóm tắt

| Mục | Kết quả |
|---|---|
| Tổng case | 46 active · 1 Obsolete (TC-CART-003) |
| Validator (bộ gốc) | 0 ERROR · 0 WARNING |
| Chỉ số 1 — Req_ID có case | 18/18 (validator) |
| Chỉ số 2 — Mệnh đề nguồn có case · có case Ready | 60/60 · 34/60 (validator). **Mẫu số bị đếm thiếu**: 4 mệnh đề gộp nhiều khẳng định độc lập (F-15) — sau khi tách, mẫu số tăng, tỷ lệ Ready giảm |
| Chỉ số 3 — CO có case | 47/47, Pending 14 (validator). Review phát hiện **11 điều kiện còn thiếu** (CO-62…CO-72): 7 thiết kế được ngay (TC-CART-048…054), 4 phải để Pending (Q-21…Q-24) |
| Chỉ số 4 — IX / EV | IX 12 dòng (11 CO, 1 Pending) · EV 13 dòng (7 CO, 1 N/A, 5 Pending). Thiếu IX-13…IX-16 và EV-14; EV-01 kết luận chưa đủ (F-03) |
| Mức sẵn sàng (validator) | Ready 17 · Needs Clarification 12 · Blocked 17. **Mức thực tế khác**: ~9 case bị tính Blocked/NC thừa (F-02), còn 5 case lẽ ra phải NC vì phụ thuộc chưa đánh dấu (F-01) |
| Phát hiện | **Critical 1 · Major 9 · Minor 11 · Suggestion 2** |
| Case đề xuất bổ sung | 7 (`testcases-additional.csv`, TC-CART-048…054): Ready 2 · Needs Clarification 2 · Blocked 3 |
| Câu hỏi mới | Q-20 … Q-24 |

**Kết luận:** analysis v2.0 có nền tốt (đủ mệnh đề, DT2 đã có R4/R5, đã có tập phần tử, ma trận trạng thái không còn ô trống). Có ba vấn đề chính. (1) Một giả định ngầm, *trạng thái tick được giữ khi tải lại / mở lại Cart*, đang được viết như sự thật trong các case tương tác quan trọng nhất (TC-CART-043, 047). (2) Mức sẵn sàng bị lệch vì `SETUP-03`/`AS-03` gắn vào các case chỉ cần một lần tải trang. (3) Còn thiếu điều kiện ở chỗ giao nhau giữa trigger và luồng: thiếu hàng khi mở trang, ≥2 rule cùng lúc khi tải trang, biên "vừa đủ" lúc revalidate, bấm Mua hàng lần 2 ở nhánh thiếu hàng, AC08 × AC10, xoá dòng × AC04, và các lối vào Checkout ngoài nút "Mua hàng".

## 2. Bảng phát hiện

| ID | TC_ID / CO / Req_ID | Mức | Vấn đề | Căn cứ | Đề xuất sửa |
|---|---|---|---|---|---|
| F-01 | TC-CART-043, TC-CART-047, TC-CART-045, TC-CART-007, TC-CART-033 · CO-50, CO-58, CO-55 · Q-02, Q-09, AS-02 | **Critical** | Expected khẳng định trạng thái tick của các dòng **không bị rule nào tác động** sau F5 / mở lại Cart, nhưng không có marker: 043 "SP-C … vẫn bỏ tick; nút Disable"; 047 "Y … vẫn bỏ tick; Z … vẫn được tick; nút Enable"; 045 "TỔNG (1 SẢN PHẨM)" (cần SP-A còn tick sau F5); 007 "SP-A vẫn được tick; nút vẫn Enable"; 033 bước 1 (Precondition "được tick" rồi Step "Truy cập Giỏ hàng"). Việc tick có được giữ qua các lần tải trang hay không là câu hỏi mở (Q-09, đang để mức *Minor*). **AS-02** (SP còn hàng được tick sẵn khi vào Cart) còn **mâu thuẫn trực tiếp** với 043 và 047: nếu hệ thống tick lại mọi SP còn hàng mỗi lần tải trang, SP-C/Y sẽ được tick sau F5, tập "còn hàng + tick" không rỗng, và mục tiêu IX-01 của TC-CART-043 không còn kiểm tra được. Các case này hiện là NC chỉ nhờ AS-03. Khi Q-04 được trả lời và AS-03 được bỏ, chúng sẽ thành Ready mà vẫn mang giả định ẩn. | Nguồn chỉ nói giữ lựa chọn cho nhánh revalidate (AC08 "Các SP khác vẫn hợp lệ giữ nguyên trạng thái lựa chọn") và cho dòng bị điều chỉnh (AC06 "Keep tick box"). Không mệnh đề nào nói giữ tick cho các dòng khác khi tải lại trang. Q-09 trong analysis hỏi đúng điều này | Tách khỏi Q-09 thành **Q-20 (Major)**. Thêm AS-07 "Trạng thái tick của SP còn hàng được giữ nguyên qua tải lại / mở lại Cart" với Case bị ảnh hưởng: TC-CART-007, TC-CART-033, TC-CART-043, TC-CART-045, TC-CART-047. Gắn `[Cần xác nhận Q-20] [Giả định AS-07]` vào 5 case. TC-033: đổi thành "1. Truy cập Giỏ hàng 2. Tick SP-A, SP-C nếu chưa tick" để bỏ phụ thuộc. Ghi vào AS-02 rằng nếu Q-02 = "tick sẵn mỗi lần tải" thì CO-50 chỉ kiểm tra được qua nhánh revalidate (TC-CART-041) |
| F-02 | TC-CART-007, 016, 017, 029, 031, 032, 043, 045, 047 · SETUP-03 · AS-03 | Major | 9 case có trigger là **một lần tải trang (F5)** nhưng tham chiếu SETUP-03 (*Chưa rõ cách làm*), nên bị tính Blocked, gồm 2 case P1 của AC06 (016, 017). Điều chưa rõ của SETUP-03 là "giá trị mới có hiệu lực ngay với phiên giỏ hàng đang mở". Điều đó chỉ ảnh hưởng tới nhánh bấm "Mua hàng" mà **không tải lại**. Với F5, một lần tải trang mới cũng giống lần mở trang của SETUP-02, và SETUP-02 đã có cách xác minh (cột Salable Quantity / trang chi tiết SP). Tương tự, **AS-03 thừa** trên các case F5: một lần tải trang phản ánh tồn kho hiện tại với **mọi** câu trả lời của Q-04 (kể cả realtime). Chính TC-CART-004 (OOS khi vào trang) cũng không gắn AS-03 | analysis §17 SETUP-02/03; AS-03; TC-CART-004 | Sửa SETUP-02 thành "trước **lần tải trang Giỏ hàng tiếp theo**". Chuyển 9 case sang SETUP-02 và bỏ `[Giả định AS-03]` trên các case này. Chỉ giữ SETUP-03 cho các case không tải lại (024–027, 040–042, 046). Ước tính: Blocked 17 → 8; TC-016/017 → Ready |
| F-03 | EV-01 · AC06-c1…c4 · CO-16, CO-17 | Major | EV-01 (lần đầu vào Cart) chỉ có kết luận CO-04 (OOS). Tổ hợp *thiếu số lượng khi khách mở lại Cart* (tồn kho giảm trong lúc khách rời trang) chưa có điều kiện. Đây là đường xảy ra thường nhất ngoài thực tế. Hệ quả: mọi case của AC06 (P1) đều đi qua F5 + SETUP-03 nên đều Blocked | AC06 Given/When không giới hạn thời điểm phát hiện; EV-01 = CO-04 | Thêm **CO-62** và gắn vào EV-01. Case đề xuất **TC-CART-048** (P1, chỉ cần SETUP-02 → Ready) |
| F-04 | Tập phần tử · CO-48 · AC02, AC06, AC10 | Major | Mục "≥ 2 phần tử thuộc các rule khác nhau cùng lúc" chỉ được phủ ở trigger bấm "Mua hàng" (DT2-R4). Ở trigger vào trang / F5, hai xử lý chạy cùng lúc: OOS tự bỏ tick và **đẩy xuống cuối (làm các dòng dịch vị trí)**, dòng khác bị điều chỉnh qty kèm thông báo. Lỗi có thể xảy ra: thông báo gắn nhầm dòng sau khi sắp xếp, hiện cả hai loại thông báo (như bug DEV-3766), qty điều chỉnh nhầm dòng | rules/02 §Tập phần tử; DEV-3766 | Thêm **CO-63**. Case **TC-CART-049** (P2; NC vì Q-01) |
| F-05 | DT2-R1 · CO-24 · AC08-c2 | Major | DT2-R1 = "không có thay đổi tồn kho". Bảng thiếu phân vùng *tồn kho giảm nhưng vẫn ≥ qty*. Biên "Saleable Qty = qty" lúc revalidate chưa có case (TC-CART-025 chỉ phủ qty − 1). Lỗi điển hình: reload Cart + banner khi chỉ cần **có thay đổi**, thay vì khi **không đủ**. Analysis §7.1 chọn 3-value BVA cho tồn kho, nhưng mới áp dụng cho việc khách tự đổi qty | AC08: "Nếu tất cả SP được chọn vẫn đủ stock → tiếp tục Checkout" | Tách DT2-R1 thành R1a (không đổi) / R1b (giảm, vẫn đủ). Thêm **CO-64**. Case **TC-CART-050** (BVA, P2; Blocked vì SETUP-03) |
| F-06 | CO-28 · AC08-c7 · AC06-c5 | Major | "Bấm Mua hàng để revalidate và Checkout lại" chỉ được phủ ở nhánh hết hàng (TC-CART-027). Nhánh thiếu số lượng chưa có case. Rủi ro: lần bấm thứ hai mang lại qty khách đã chọn ban đầu (3) thay vì qty đã điều chỉnh (2), hoặc revalidate lặp mãi, chặn bán hàng (rủi ro P1 ở §15) | AC08-c7; AC06 "không keep theo số lượng KH chọn" | Thêm **CO-65**. Case **TC-CART-051** (P1; Blocked) |
| F-07 | Ma trận tương tác · AC08 × AC10 × AC01 · TC-CART-024, 026, 027, 040, 041 | Major | Revalidate làm SP đang tick chuyển sang OOS. Theo AC10-c5, SP đó phải xuống cuối Cart, nên các dòng còn lại dịch vị trí. Rủi ro "tick đi theo vị trí" (IX-09) mới được phủ ở F5 (TC-CART-047). Ở nhánh revalidate, lần bấm thứ hai sẽ đưa nhầm SP vào Checkout, và revalidate không bắt được vì SP đó vẫn còn hàng. Không case revalidate nào kiểm tra vị trí | AC10-c5 "sau khi trạng thái tồn kho được cập nhật"; AC08-c6 | Thêm **IX-13 → CO-66**. Case **TC-CART-052** (P2; Blocked) |
| F-08 | Ma trận trạng thái ô *Còn hàng – Tick × E6 xoá dòng* · AC04, AC05, BR-01 | Major | Ô E6 ghi "chức năng hiện có, ngoài phạm vi AC". Thao tác xoá thì đúng là có sẵn, nhưng **hệ quả lên nút "Mua hàng"** thuộc phạm vi: BR-01 là quy tắc theo trạng thái ("Disable khi không có SP nào đồng thời Còn hàng + Được tick"). Xoá SP còn hàng duy nhất được tick → Cart chỉ còn SP OOS (trạng thái AC05). Đây là trường hợp *phần tử duy nhất rời tập* do một sự kiện khác ngoài untick, chưa có IX hay case | AC04 Business Rule; AC05 | Thêm **IX-14 → CO-67**, ô E6 dẫn tới CO-67. Case **TC-CART-053** (P2; Ready) |
| F-09 | Ma trận trạng thái ô *OOS × E5* · AC09-c4 × BR-03 | Minor | Ô "có hàng trở lại" không tách theo lượng hàng về. Nếu 0 < Saleable Qty < qty của dòng (vd. qty 3, hàng về 1): có điều chỉnh qty kèm thông báo không, tick ra sao? Nguồn không nêu. Hậu quả bị giới hạn vì revalidate vẫn bắt được khi bấm Mua hàng | AC09-c4 "theo logic kiểm tra tồn kho" | **Q-21**; thêm IX-16 → **CO-69** `Pending - Q-21` |
| F-10 | Ô *Còn hàng – Untick × E4* · CO-52 · Q-13 | Minor | Ô này dẫn tới Q-13 / CO-52, nhưng Q-13 và CO-52 chỉ hỏi về việc **khách tự đổi qty** của SP bỏ tick. Sự kiện E4 là **tồn kho giảm** (hệ thống tác động), nên ô đang trỏ tới câu hỏi không hỏi điều cần hỏi. Chưa rõ: dòng bỏ tick có tự điều chỉnh qty kèm thông báo khi tải trang không (AC06 Given chỉ nói SP "đang được chọn"), và khi khách tick lại dòng có qty > Saleable Qty thì có kiểm tra ngay không | AC06 tiêu đề "Sản phẩm đang được chọn…"; Q-13 | **Q-22**; ô E4 → **CO-70** `Pending - Q-22` |
| F-11 | Bảng EV · EV-05, EV-06 · DEV-3653 | Major | EV-05 chỉ xét **hiển thị** SP OOS ở mini-cart. Chưa có dòng EV cho **hành động** đi từ kênh thứ hai: nút thanh toán / sửa qty trong mini-cart (nếu có). DEV-3653 có tiêu đề "Minicart đồng bộ trạng thái selective-checkout", nên mini-cart nhiều khả năng có lối vào Checkout. Lối này có thể bỏ qua cả việc lọc SP được tick lẫn revalidate, tức đúng rủi ro P1 "SP hết hàng lọt vào đơn" | rules/04 §B kênh thứ hai; child DEV-3653 | Thêm **EV-14 → CO-71** `Pending - Q-23` (P1 khi có đặc tả) |
| F-12 | TC-CART-024, 025, 026, 027, 040, 041, 042, 046 · Q-04 · SETUP-03 | Major | Các case revalidate (không tải lại) giả định Cart **chưa** hiển thị thay đổi tồn kho lúc khách bấm "Mua hàng". Nếu Q-04 = realtime, Cart đã tự cập nhật trước đó, lúc bấm không còn SP nào thiếu, và việc không có banner là đúng. Khi đó case fail sai, hoặc pass mà không đi qua revalidate. Các case không gắn Q-04, không có bước xác minh precondition. Cột "Cách xác minh" của SETUP-03 vẫn để "Chưa xác định" | AC08; Q-04; AS-03 (chỉ liệt kê case F5) | Thêm bước trước khi bấm: "Trên tab khách, xác nhận dòng X vẫn hiển thị qty / tick cũ, không có thông báo". Không đạt thì case = Blocked, không phải Fail. Bước này chính là phần "Cách xác minh" của SETUP-03 (đã áp dụng trong TC-CART-050…052) |
| F-13 | AC06 × AC10 · AC06-c6 | Minor | Chưa có IX cho câu hỏi: SP **thiếu số lượng** (vẫn còn hàng) có bị đẩy xuống cuối như SP OOS không? Ảnh hiện trạng dùng chung câu "Số lượng sản phẩm không có sẵn" cho lỗi tồn kho, nên khả năng hai trường hợp bị xử lý nhầm là thực tế. TC-CART-016 kiểm tra dòng vẫn được tick, nhưng không kiểm tra vị trí | AC06 "Lưu ý: … khác với trường hợp sản phẩm hoàn toàn hết hàng"; AC10 chỉ áp dụng cho SP hết hàng | Thêm **IX-15 → CO-68**. Case **TC-CART-054** (P3; NC vì Q-15) |
| F-14 | Ma trận trạng thái §8.1 | Minor | Thiếu trạng thái *Còn hàng – Tick, đã điều chỉnh (đang hiện "Sản phẩm này chỉ còn số lượng là N")*. Các ô chưa có kết luận: tải lại lần nữa (thông báo còn hiện không?), khách giảm qty (thông báo có ẩn không?), có hàng trở lại (có khôi phục qty ban đầu không? AC06 nói "không keep theo số lượng KH chọn") | AC06, AC07 | Thêm dòng trạng thái; ô chưa biết → **Q-24**, **CO-72** `Pending - Q-24` |
| F-15 | §4a AC07-c3, AC08-c3, AC08-c4, AC08-c5 | Minor | Mỗi mệnh đề gộp 2–3 khẳng định có thể đúng/sai độc lập (điều chỉnh qty / thông báo / giữ tick; reload Cart / banner chung; uncheck / Disable / thông báo). Trong khi đó AC06 đã tách đúng các khẳng định cùng loại thành c1–c3, nên mẫu số của chỉ số 2 không nhất quán. Không mất coverage vì các case assert đủ | rules/01 Bước 2 | Tách các mệnh đề này thành c3a/c3b/… theo cách đã làm với AC06 |
| F-16 | TC-CART-018 · CO-18 · AC06-c5 | Minor | Title ghi "khi cố tăng qty **sau khi đã bị điều chỉnh**", nhưng Precondition chỉ là qty 1 / tồn kho 1, không tạo ra trạng thái đã tự điều chỉnh. Case này thực chất trùng phân vùng với TC-CART-021 (qty > Saleable). Rủi ro riêng của AC06-c5 (hệ thống còn nhớ qty khách chọn ban đầu) không được kiểm tra | AC06-c5 | Precondition: qty 2 → SETUP-02 đặt tồn kho 1 → mở Cart (đã tự về 1, có thông báo) → nhập 3 → kỳ vọng về 1 |
| F-17 | TC-CART-033, 034, 045, 046 | Minor | Các chuỗi trong ngoặc kép "TỔNG (3 SẢN PHẨM)", "TỔNG (2 SẢN PHẨM)", "TỔNG (1 SẢN PHẨM)", "TỔNG (0 SẢN PHẨM)" không phải nguyên văn: nguồn chỉ có "TỔNG (8 SẢN PHẨM)" (ảnh hiện trạng). Validator vẫn cho qua | rules/03 §Văn phong | Viết: dòng nhãn TỔNG (N SẢN PHẨM) với N = 3 (không ngoặc kép), giữ marker AS-05 |
| F-18 | TC-CART-005, 006, 009, 010, 011, 029, 030 | Minor | Thứ tự Preconditions bị ngược: "3. Đang ở trang Giỏ hàng" đứng trước "4. Theo SETUP-02 … trước khi mở Giỏ hàng". TC-005 còn lặp "(Saleable Qty = 0)" ở mục 2 và mục 4 | rules/03 §Tái tạo được | Đưa bước SETUP-02 lên trước "Đang ở trang Giỏ hàng" |
| F-19 | SETUP-02 · Q-14 · CO-53 | Minor | SETUP-02 cho phép "admin sửa số lượng / Stock Status". "Stock Status = Out of Stock khi qty > 0" là một phân vùng khác (CO-53, `Pending - Q-14`), nên tester có thể vô tình chạy case Ready trên phân vùng chưa xác nhận | Q-14 | SETUP-02 chỉ dùng cách đặt Quantity sao cho Salable Quantity = giá trị case; ghi rõ "không đổi Stock Status" |
| F-20 | TC-CART-030 | Minor | Expected "SP-A không bị ảnh hưởng" mơ hồ | rules/05 §Anti-pattern | "SP-A vẫn hiển thị, giữ trạng thái tick như trước khi xoá; nút "Mua hàng" giữ trạng thái Enable" |
| F-21 | TC-CART-039 | Minor | Title ghi "theo mockup", nhưng ảnh dùng làm oracle là **ảnh hiện trạng trước tính năng**. Analysis §0 đã ghi rõ ảnh này "không dùng làm oracle cho hành vi mới" | analysis §0, §12 | Đổi Title thành "so với giao diện thông báo hiện tại"; giữ `[Cần xác nhận Q-19]` |
| F-22 | IMP-01 · CO-34…CO-35 · AC07 | Suggestion | Tóm tắt đơn hàng mới được kiểm tra khi tick, tồn kho, hoặc qty tự điều chỉnh thay đổi. Chưa kiểm tra (a) khách tự đổi qty của dòng **được tick** thì TỔNG cập nhật, (b) đổi qty của dòng **bỏ tick** (phần tử ngoài tập) thì TỔNG không đổi | IMP-01 "cập nhật khi tick / tồn kho / qty thay đổi" | Thêm 1 case EG kèm `[Giả định AS-05]` khi IMP-01 được xác nhận |
| F-23 | TC-CART-018…022 · AC07 × AC08 | Suggestion | Steps "Đổi qty SP-E thành 4" không nói cách xác nhận giá trị (Enter / rời ô / nút cập nhật). Đoán lỗi: đổi qty lên > Saleable Qty rồi bấm "Mua hàng" ngay khi qty chưa cập nhật xong | rules/02 §EG | Ghi rõ thao tác xác nhận vào Steps; thêm 1 case EG cho race "đổi qty + bấm Mua hàng ngay" |

## 3. Điều kiện kiểm thử chưa bao phủ — dòng cần thêm vào `analysis.md`

Validator chạy trên file gộp đang báo 7 WARNING "không gắn với điều kiện kiểm thử nào" cho TC-CART-048…054. Các cảnh báo này hết khi thêm các dòng dưới đây.

**§16 Điều kiện kiểm thử**

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-62 | AC06; BR-03 | Tồn kho giảm xuống 0 < Saleable Qty < qty trước khi khách mở lại Cart (EV-01) | ST | TC-CART-048 | F-03 |
| CO-63 | AC02; AC06; AC10; BR-02; BR-03 | 1 dòng OOS + 1 dòng thiếu số lượng cùng lúc khi mở Cart / tải lại | DT | TC-CART-049 | F-04, tập phần tử |
| CO-64 | AC08 | DT2-R1b: tồn kho giảm nhưng Saleable Qty = qty lúc bấm Mua hàng | BVA | TC-CART-050 | F-05 |
| CO-65 | AC08; AC06; BR-03 | Bấm Mua hàng lần 2 sau khi revalidate tự điều chỉnh qty | UC | TC-CART-051 | F-06 |
| CO-66 | AC08; AC10; AC01 | Sau revalidate, SP vừa OOS xuống cuối và tick đi theo SP (IX-13) | ST | TC-CART-052 | F-07 |
| CO-67 | AC04; BR-01; AC05 | Xoá SP còn hàng duy nhất được tick → nút Disable (IX-14) | DT | TC-CART-053 | F-08 |
| CO-68 | AC10; AC06 | SP thiếu số lượng không bị đẩy xuống cuối (IX-15) | ST | TC-CART-054 | F-13 |
| CO-69 | AC09; BR-03 | OOS có hàng trở lại với 0 < Saleable Qty < qty (IX-16) | ST | | Pending - Q-21 |
| CO-70 | AC06; AC07 | Tồn kho giảm dưới qty của SP đang bỏ tick; tick lại SP đó | ST | | Pending - Q-22 |
| CO-71 | AC01; AC08; AC02 | Lối vào Checkout / sửa qty khác nút "Mua hàng" (mini-cart…) (EV-14) | EG | | Pending - Q-23 |
| CO-72 | AC06; AC07 | Trạng thái "đã điều chỉnh" × tải lại / giảm qty / có hàng lại | ST | | Pending - Q-24 |

**Các bảng khác**

- §4a Mệnh đề nguồn: AC06-c1, c2, c3 thêm CO-62; AC08-c2 thêm CO-64; AC08-c7 thêm CO-65; AC10-c5 thêm CO-66; AC04-c3 và BR-01-c2 thêm CO-67; AC06-c6 và AC10-c2 thêm CO-68; AC09-c4 thêm CO-69. Tách mệnh đề theo F-15.
- §9 DT2: tách R1 thành R1a / R1b (CO-64). Bảng *Tập phần tử*, dòng "≥2 phần tử khác rule": thêm CO-63 (trigger tải trang). Dòng "phần tử duy nhất": thêm CO-67 (sự kiện xoá).
- §9a: thêm IX-13 (AC08 × AC10 × AC01 → CO-66), IX-14 (xoá dòng × AC04/AC05 → CO-67), IX-15 (AC06 × AC10 → CO-68), IX-16 (AC09 × BR-03 → Pending - Q-21).
- §9b: EV-01 kết luận "CO-04; CO-62". Thêm EV-14 "Thanh toán / sửa qty từ mini-cart hoặc lối vào Checkout khác" → Pending - Q-23.
- §8.1: ô *Còn hàng – Tick × E6* → CO-67. Ô *Còn hàng – Untick × E4* → Q-22 · CO-70. Ô *OOS × E5* tách theo lượng hàng về (CO-69). Thêm dòng trạng thái "Còn hàng – Tick, đã điều chỉnh" (Q-24 · CO-72).
- §14: thêm AS-07 (F-01). Rút TC-CART-007, 016, 017, 029, 031, 032, 043, 045, 047 khỏi danh sách case của AS-03 (F-02).
- §17: sửa SETUP-02 (F-02, F-19). Điền "Cách xác minh" cho SETUP-03 bằng bước xác minh trên tab khách (F-12).

## 4. Nhóm trùng lặp (đã xét ngữ nghĩa)

Validator không báo ứng viên trùng. Đã xét thêm các cặp có bước giống nhau:

- TC-CART-024 / 026 / 027: dùng chung setup revalidate OOS nhưng mục tiêu khác nhau (banner và SP OOS · SP khác giữ lựa chọn, kể cả SP bỏ tick · bấm lần 2) → **không trùng**.
- TC-CART-013 / 014: cùng dữ liệu "tất cả OOS". 013 kiểm tra nút và chặn Checkout, 014 kiểm tra hiển thị (có lặp assertion nút Disable) → không gộp; chấp nhận được.
- TC-CART-010 / 012: cùng hành vi 0 → 1 nhưng khác ngữ cảnh (Cart hỗn hợp có OOS / Cart toàn SP còn hàng) → không trùng.
- TC-CART-018 / 021: hiện **cùng phân vùng** qty > Saleable Qty (xem F-16). Sửa Precondition của 018 theo F-16 thay vì gộp.

## 5. Priority & nhãn

Không thấy lệch đáng kể so với §15. Case đề xuất được đặt Priority theo cùng bảng rủi ro: luồng chặn bán hàng / đi vào Checkout là P1 (048, 051), các tương tác còn lại P2, phần sắp xếp P3.

## 6. Câu hỏi phát sinh

| ID | Câu hỏi | Liên quan | Mức độ |
|---|---|---|---|
| Q-20 | Trạng thái tick của SP còn hàng có được giữ khi khách tải lại (F5) / rời rồi mở lại Cart / đăng nhập lại không? Nếu SP được tick sẵn mặc định (Q-02), mỗi lần tải trang hệ thống có tick lại các SP khách đã bỏ tick không? (tách từ Q-09) | AC01, AC04, IX-01, IX-09 | Major |
| Q-21 | SP hết hàng có hàng trở lại nhưng Saleable Qty < qty trong Cart (vd. qty 3, hàng về 1): qty có tự điều chỉnh, có hiện "Sản phẩm này chỉ còn số lượng là..." không, checkbox ở trạng thái tick hay bỏ tick? | AC09, BR-03 | Minor |
| Q-22 | SP **đang bỏ tick** có tồn kho giảm xuống 0 < Saleable Qty < qty: khi tải trang có tự điều chỉnh qty kèm thông báo như AC06 không? Khi khách tick lại SP này thì có kiểm tra tồn kho ngay không? | AC06, AC07 | Minor |
| Q-23 | Ngoài nút "Mua hàng" ở Giỏ hàng, còn lối nào vào Checkout hoặc sửa qty (nút thanh toán / sửa qty trong mini-cart, "Mua ngay" ở trang sản phẩm…)? Các lối đó có chỉ đưa SP được tick sang Checkout và có revalidate tồn kho không? (DEV-3653) | AC01, AC02, AC08 | Major |
| Q-24 | Sau khi qty tự điều chỉnh, thông báo "Sản phẩm này chỉ còn số lượng là N" hiển thị đến khi nào (tải lại, khách giảm qty)? Khi có hàng trở lại, qty có được khôi phục về số khách chọn ban đầu không? | AC06, AC07 | Minor |

## 7. Validator

- Bộ gốc: `python3 scripts/validate_testcases.py output/DEV-3648/testcases.csv --analysis output/DEV-3648/analysis.md` → **0 ERROR · 0 WARNING**.
- Bộ gốc + đề xuất (file gộp tạm: `/tmp/claude-1000/-home-cuongdoan17-Projects-test-case-render/796718ae-eb94-413c-855f-f455b48308dd/scratchpad/testcases-merged.csv`) → **0 ERROR · 7 WARNING**. Cả 7 là "TC-CART-048…054 không gắn với điều kiện kiểm thử nào", và hết khi thêm CO-62…CO-68 (§3). Mức sẵn sàng của file gộp: Ready 19 · NC 14 · Blocked 20. Riêng 7 case đề xuất: Ready 2 (048, 053) · NC 2 (049, 054) · Blocked 3 (050, 051, 052).
- Case đề xuất **không** tham chiếu Q-20…Q-24 (chưa có trong analysis). Riêng TC-CART-049 có ghi chú không assert tick SP-A vì phụ thuộc F-01.

## 8. Ghi chú về ID

TC-CART-048…054 được đánh tiếp sau số lớn nhất trong `testcases.csv` (TC-CART-047). Theo yêu cầu, review này **không đọc** `testcases-additional.v1.0.csv` / `testcases-additional.v1.1.csv`. Người sinh cần đối chiếu lịch sử ID trong hai file đó trước khi gộp. Nếu 048…054 đã từng được dùng thì đánh số lại các case đề xuất (chúng chưa được dùng ở đâu khác).
