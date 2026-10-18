# Review bộ rules sinh test case — vòng 2: tăng độ bao phủ và chất lượng

| Thông tin | Giá trị |
|---|---|
| Ngày | 2026-10-16 |
| Phạm vi | `rules/01`–`05`, `templates/`, `.agents/skills/tc-*`, `scripts/validate_testcases.py` (đã áp dụng R-01…R-10 của `review.md` vòng 1) |
| Bằng chứng | Bộ test DEV-3648 v1.1 được sinh **theo đúng bộ rules hiện tại**: 0 ERROR · 0 WARNING, tự báo cáo "39/39 điều kiện có case". Review độc lập (`output/DEV-3648/review.md`) vẫn tìm được 1 Critical + 8 Major. Mỗi phát hiện dưới đây đều trỏ về lỗi thật của bộ test đó |

## 1. Kết luận

Vòng 1 đã sửa xong phần **tính nhất quán và tính trung thực**: không còn ép tỷ lệ, có phân biệt IMP/AS/Q, có mức sẵn sàng, ID ổn định. Bộ rules hiện tại đảm bảo được hai điều: case **viết đúng chuẩn** và **có truy vết**. Điều nó chưa đảm bảo là AI **tìm ra đủ điều kiện cần kiểm thử**.

Các lỗ hổng của DEV-3648 đều không nằm trong một AC riêng lẻ. Chúng nằm ở bốn chỗ:
- **giữa các AC**: AC02 × AC04, AC07 × AC08;
- **giữa các phần tử** của một danh sách: SP được tick và SP không được tick;
- **giữa các kênh / thời điểm kích hoạt**: tải lại, bấm Mua hàng, vào thẳng URL, mini-cart;
- **trong các giả định ngầm** không được ghi ra: thứ tự hiển thị, tick mặc định.

Rules hiện tại chỉ yêu cầu phân tích **từng yêu cầu** rồi chọn kỹ thuật cho yêu cầu đó (`rules/01` Bước 3.1). Mẫu số bao phủ lại do chính AI tự lập. Vì vậy validator báo 100% trong khi bảng quyết định còn thiếu rule.

Để có độ bao phủ cao nhất, cần thêm 3 lớp:
1. **Mở rộng mẫu số một cách có hệ thống** — Nhóm A: mệnh đề, tương tác, tập phần tử, bảng trạng thái đầy đủ, sự kiện × kênh.
2. **Kiểm soát chất lượng oracle và khả năng thực thi** — Nhóm B.
3. **Vòng phản biện độc lập trước khi bàn giao** — Nhóm C.

> "Bao phủ cao nhất" ở đây là bao phủ **điều kiện và rủi ro**, không phải số lượng case. Mọi bổ sung dưới đây làm tăng số `CO-xx` được xét, kể cả các CO kết luận `N/A - lý do`. Nguyên tắc "không tạo case hình thức" vẫn giữ nguyên.

## 2. Tổng hợp đề xuất

| ID | Nhóm | Ưu tiên | Đề xuất | Lỗi DEV-3648 mà rule này bắt được |
|---|---|---|---|---|
| A1 | Mẫu số | **Bắt buộc** | Tách yêu cầu thành **mệnh đề nguồn** (`AC08-c3`), truy vết Mệnh đề → CO | "39/39" không phản ánh các mệnh đề chỉ có oracle tạm |
| A2 | Mẫu số | **Bắt buộc** | **Ma trận tương tác yêu cầu**: các cặp yêu cầu cùng tác động lên một thực thể/trạng thái | AC02×AC04 (SP được tick duy nhất hết hàng), AC06×AC08 |
| A3 | Mẫu số | **Bắt buộc** | Bảng quyết định trên **tập phần tử**: phần tử không được chọn, phần tử duy nhất, nhiều phần tử khác rule | DT2 thiếu 3 rule (TC-040/041/042) |
| A4 | Mẫu số | **Bắt buộc** | Bảng trạng thái **đầy đủ** State × Event, mỗi ô phải có kết luận | Thiếu: SP bỏ tick đổi qty, Insufficient → OOS, OOS + xoá |
| A5 | Mẫu số | **Bắt buộc** | **Ma trận sự kiện kích hoạt × kênh** cho mỗi hành vi | Thời điểm phát hiện (Q-04), URL checkout trực tiếp, 2 tab, mini-cart |
| A6 | Mẫu số | Nên có | Heuristic **phủ định từng mệnh đề** và **bất biến** (cái không được thay đổi) | SP khác giữ nguyên lựa chọn; SP không chọn không lọt vào đơn |
| A7 | Mẫu số | Nên có | Đọc **nội dung** ticket con / bug liên kết, mỗi bug là một CO regression có điều kiện tái hiện | DEV-3746/3770 chỉ đọc tiêu đề |
| A8 | Mẫu số | Nên có | Checklist **theo miền nghiệp vụ** (`rules/04-domain/`) | Định nghĩa "hết hàng" trong Magento (Q-14), giá khuyến mãi |
| A9 | Mẫu số | Nên có | Định nghĩa **mức độ chi tiết** `smoke / standard / full` | Hiện chỉ có `smoke`, chưa định nghĩa mức đầy đủ |
| B1 | Oracle | **Bắt buộc** | Cấm phụ thuộc ghi bằng chữ tự do. Validator đối chiếu AS ↔ case hai chiều | TC-031 báo Ready sai; TC-008 thiếu AS-02 |
| B2 | Oracle | Nên có | Phân loại ảnh / mockup trước khi dùng làm oracle | TC-039 dùng mockup hiện trạng cũ |
| B3 | Oracle | Nên có | Expected có số liệu thì fixture phải đủ tham số tính toán | Giá khuyến mãi 40% không có trong SETUP; TC-033 |
| B4 | Thực thi | **Bắt buộc** | Phân tích **khả năng điều khiển & quan sát** cho từng CO. SETUP có trạng thái sẵn sàng | 32/39 case cần đổi Saleable Qty nhưng chưa có cách làm |
| C1 | Quy trình | **Bắt buộc** | **Vòng phản biện độc lập** (agent mới, không chung ngữ cảnh) trước khi bàn giao | Chính vòng review này tìm ra F-01…F-09 |
| C2 | Quy trình | Nên có | Khi sinh lại phải xử lý đề xuất review cũ. Review ghi phiên bản bộ test được review | TC-040/041 bị bỏ quên qua 1 vòng |
| C3 | Quy trình | Nên có | Vòng học từ **lỗi lọt** (escaped defect) → bổ sung checklist miền | – |
| C4 | Quy trình | Nên có | Hướng dẫn cho **tester** khi nhận bộ test | – |
| D1 | Định dạng | Nên có | Định nghĩa `Test_Type`; Preconditions chỉ tham chiếu SETUP thật sự cần | TC-015 "Security"; SETUP-02 lặp ở 39 case |

## 3. Chi tiết — Nhóm A: mở rộng mẫu số bao phủ

### A1 — Mệnh đề nguồn là đơn vị truy vết nhỏ nhất (Bắt buộc)

**Vấn đề.** `rules/02` §UC đã viết "mỗi mệnh đề Then là một assertion cần được kiểm tra bởi ít nhất một case", nhưng template không có chỗ ghi mệnh đề, validator cũng không đếm mệnh đề. Truy vết hiện tại dừng ở mức `Req_ID` (thô) và `CO-xx` (do AI tự đặt). Kết quả là không ai kiểm tra được các CO đã phủ hết nguồn hay chưa.

**Đề xuất rule** (`rules/01` Bước 2, `rules/02` §UC, template §4a):
> Mỗi yêu cầu được tách thành **mệnh đề nguồn**: mỗi gạch đầu dòng `Then`, mỗi dòng bảng điều kiện, mỗi Business Rule, mỗi câu "phải / không được / khi … thì". ID có dạng `<Req_ID>-c<n>` (vd. `AC08-c3`) và ghi nguyên văn ngắn gọn. Mỗi mệnh đề phải gắn với ≥1 `CO-xx`, hoặc ghi `N/A - lý do` / `Pending - Q-xx`.

Template thêm mục **"4a. Mệnh đề nguồn"**: `| Clause_ID | Req_ID | Mệnh đề (nguyên văn rút gọn) | CO |`.

**Validator:** ERROR khi mệnh đề chưa gắn CO. Chỉ số mới *"Mệnh đề có case với oracle đã xác nhận"*: mệnh đề chỉ được phủ bởi case Needs Clarification thì tính là ⚠.

### A2 — Ma trận tương tác yêu cầu (Bắt buộc)

**Vấn đề.** Phân tích theo từng yêu cầu sẽ bỏ sót trường hợp hai yêu cầu cùng tác động lên một trạng thái. DEV-3648: AC02 (OOS tự bỏ tick) và AC04 (nút Disable khi không còn SP được tick). Không case nào cho SP được tick **duy nhất** chuyển sang OOS. Đây là đúng loại lỗi dễ lọt ra production.

**Đề xuất rule** (`rules/01` Bước 3, mục mới trong template §9a):
> Sau khi lập CO cho từng yêu cầu, lập **ma trận tương tác**. Liệt kê các *thực thể/trạng thái dùng chung* (vd. trạng thái tick, qty, tồn kho, nút Mua hàng, tổng tiền). Với mỗi cặp yêu cầu cùng **đọc hoặc ghi** một thực thể: một yêu cầu thay đổi thực thể, yêu cầu kia có còn đúng không? Mỗi cặp có rủi ro tạo một `CO-xx` (kỹ thuật `DT` hoặc `ST`). Cặp không cần kiểm tra thì ghi lý do.

| Thực thể | Yêu cầu ghi | Yêu cầu đọc | Cặp cần xét |
|---|---|---|---|
| Trạng thái tick | AC02, AC06, AC08 | AC04, IMP-01 | AC02→AC04, AC08→AC04, AC02→IMP-01 |

### A3 — Bảng quyết định trên tập phần tử (Bắt buộc)

**Vấn đề.** `rules/02` §DT coi điều kiện là thuộc tính của một đối tượng. Giỏ hàng, danh sách và đơn hàng nhiều dòng là **tập**, mỗi phần tử có thể rơi vào một rule khác nhau. DT2 của DEV-3648 chỉ xét các SP *được tick*. Nó bỏ sót SP không được tick, SP được tick duy nhất, và trường hợp hai SP thuộc hai rule khác nhau cùng lúc. Analysis còn loại tổ hợp R2+R3 với lý do không đúng.

**Đề xuất bổ sung `rules/02` §DT:**
> 5. **Khi điều kiện áp dụng cho từng phần tử của một tập** (dòng giỏ hàng, item đơn hàng, bản ghi được chọn), ngoài các rule cho từng phần tử, phải xét:
>    - phần tử **nằm ngoài** tập được chọn/áp dụng (không được tick, bị lọc);
>    - phần tử **duy nhất** thoả điều kiện chuyển sang không thoả (tập rỗng sau thay đổi);
>    - **≥ 2 phần tử thuộc các rule khác nhau cùng lúc** (hành động tổng hợp có đúng không: thông báo chung, trạng thái nút);
>    - tập rỗng, tập 1 phần tử, tập tất cả phần tử cùng rule.
> 6. Loại một tổ hợp **khả thi** phải ghi lý do *chứng minh hành vi không đổi* (vd. "xử lý độc lập từng dòng, đã có CO-xx kiểm tra hai dòng khác loại"), không được chỉ ghi "không thêm giá trị".

### A4 — Bảng trạng thái đầy đủ (Bắt buộc)

**Vấn đề.** `rules/02` §ST yêu cầu "lập bảng State × Event", nhưng template chỉ có danh sách chuyển đổi đã biết. AI chỉ liệt kê các chuyển đổi có trong tài liệu, nên các ô *không có trong tài liệu* (thường là chỗ có lỗi) không bao giờ được xét. DEV-3648 không xét: SP OOS + khách đổi qty / xoá; Insufficient → OOS; SP bỏ tick + tồn kho giảm.

**Đề xuất:** template §8 thêm **bảng ma trận** (hàng = trạng thái, cột = sự kiện). **Mỗi ô** điền một trong bốn giá trị: `→ <trạng thái> (nguồn)` / `Bị chặn (nguồn)` / `Không khả thi (lý do)` / `Q-xx`. Ô trống không được phép. Validator kiểm tra không có ô trống.

### A5 — Ma trận sự kiện kích hoạt × kênh (Bắt buộc)

**Vấn đề.** Một hành vi ("SP hết hàng thì tự bỏ tick") có thể được kích hoạt ở nhiều **thời điểm** (vào trang, tải lại, bấm hành động, realtime) và quan sát được ở nhiều **kênh** (trang Cart, mini-cart, URL Checkout trực tiếp, API, tab thứ 2, app). AC thường chỉ mô tả một kênh. DEV-3648: thời điểm phát hiện là câu hỏi mở (Q-04); mini-cart và URL trực tiếp chỉ được thêm theo cảm tính; 2 tab hoàn toàn không được xét.

**Đề xuất rule** (`rules/01` Bước 3, `rules/04` §B mục mới):
> Với mỗi hành vi chính, liệt kê các **sự kiện kích hoạt** và **kênh truy cập / quan sát** cùng một dữ liệu. Mỗi ô có rủi ro → `CO-xx`. Ô không áp dụng → lý do. Ô chưa rõ → `Q-xx`. Tối thiểu phải xét: tải lại trang, quay lại (Back), điều hướng trực tiếp bằng URL, kênh hiển thị thứ hai của cùng dữ liệu, phiên / tab thứ hai, đăng nhập lại.

### A6 — Phủ định và bất biến (Nên có)

**Đề xuất `rules/02` §UC + `rules/03` §Expected:**
> - **Phủ định:** với mỗi mệnh đề "khi X thì Y", xét "khi không X thì không Y" có rủi ro không (vd. "chỉ khi tồn kho thiếu mới hiện banner" → đủ tồn kho thì *không* hiện banner).
> - **Bất biến:** Expected của case làm thay đổi một phần dữ liệu phải có ≥1 assertion về phần **không được thay đổi** khi có rủi ro: dòng khác, SP không chọn, tổng của phần còn lại, dữ liệu người khác.

### A7 — Bug và ticket liên kết là nguồn điều kiện (Nên có)

**Đề xuất `rules/01` Bước 1:**
> Đọc **nội dung** (không chỉ tiêu đề) của ticket con, bug và ticket "relates to". Mỗi bug còn liên quan → một `CO-xx` (kỹ thuật `EG`, `Notes: Regression <key>`), với **điều kiện tái hiện** lấy từ bug (dữ liệu, bước, môi trường). Chỉ đọc được tiêu đề → ghi *Đọc một phần* và không ghi case là "regression" khi case chưa tái hiện đúng điều kiện của bug.

### A8 — Checklist theo miền nghiệp vụ (Nên có)

`rules/04` hiện chỉ có checklist theo thành phần UI chung. Thêm thư mục `rules/04-domain/` để chọn theo tính năng. Bắt đầu với `ecommerce-cart-stock.md`:
- **Định nghĩa hết hàng:** Saleable Qty = 0, Stock Status thủ công, backorder, ngưỡng OOS, reservation, SP bị disable/xoá, SP cấu hình (biến thể), bundle/set dùng chung component.
- **Giá:** giá gốc / giá khuyến mãi / catalog rule / cart rule / quà tặng; làm tròn; đổi giá khi đang ở Cart.
- **Kênh:** trang Cart, mini-cart, Checkout, URL trực tiếp, app, đăng nhập/khách vãng lai, gộp giỏ khi đăng nhập.
- **Đồng thời:** 2 khách mua món cuối; tồn kho đổi giữa Cart → Checkout → Đặt hàng.
- **Sau đặt hàng:** SP còn lại trong giỏ, quote mới, hoàn tồn kho khi huỷ.

Template analysis thêm dòng "Checklist miền đã dùng". Agent khai báo checklist nào đã áp dụng; mục không dùng ghi `N/A`.

### A9 — Mức độ chi tiết (Nên có)

`tc-generate` có tham số `smoke` nhưng rules chưa định nghĩa. Đề xuất `rules/01`:

| Mức | Phạm vi |
|---|---|
| `smoke` | CO có rủi ro P1, luồng chính của từng yêu cầu |
| `standard` (mặc định) | Toàn bộ A1–A5; BVA 2-value; ST 0-switch |
| `full` | `standard` + BVA 3-value cho miền rủi ro cao; ST 1-switch cho luồng cốt lõi; mọi cặp trong ma trận tương tác; pairwise cho cấu hình/thiết bị |

Report ghi rõ mức đã dùng. Khi không ở mức `full`, không được ghi "bao phủ tối đa".

## 4. Chi tiết — Nhóm B: oracle và khả năng thực thi

### B1 — Phụ thuộc phải có ID (Bắt buộc)

**Đề xuất rule** (`rules/03` §Notes):
> Mọi phụ thuộc vào thông tin chưa xác nhận phải được ghi bằng `[Cần xác nhận Q-xx]` / `[Giả định AS-xx]`, không ghi bằng chữ tự do ("cần xác nhận…", "chưa rõ…"). Khi viết expected, rà từng assertion: *assertion này có đúng bất kể câu trả lời của Q nào đang mở không?* Nếu không → gắn marker.

Validator:
- (a) WARNING khi Notes / Expected chứa `cần xác nhận | giả định | chưa rõ | TBD | ?` mà không có `Q-`/`AS-`.
- (b) WARNING hai chiều: case nằm trong cột "Case bị ảnh hưởng" của AS nhưng không có marker, hoặc ngược lại.

### B2 — Phân loại nguồn hình ảnh (Nên có)

Danh mục nguồn thêm cột **Loại**: `Thiết kế mới / Hiện trạng / Ảnh bug / Ảnh chụp tài liệu`. Ảnh *Hiện trạng* / *Ảnh bug* không dùng làm oracle cho hành vi mới. Văn bản và ảnh mâu thuẫn nhau → `Q-xx`.

Trước khi ghi "Chưa đọc được" một attachment Jira, phải thử tải qua connector (`downloadJiraIssueAttachment` của Atlassian MCP). Ghi bổ sung vào `CLAUDE.md`.

### B3 — Fixture đủ tham số cho expected có số liệu (Nên có)

`rules/03` §Tái tạo được:
> Expected chứa số tiền / số lượng tính toán → SETUP phải ghi đủ tham số: giá gốc, giá bán, khuyến mãi, thuế, phí, quy tắc làm tròn. Expected ghi **công thức + kết quả**. Dữ liệu còn "cần map sang SKU thật" thì expected tham chiếu biến của fixture (`giá bán SP-A × 2`), không hard-code số lấy từ mockup.

### B4 — Khả năng điều khiển & quan sát; SETUP có trạng thái (Bắt buộc)

**Vấn đề.** Mức sẵn sàng hiện chỉ đo **oracle**. DEV-3648 có 32/39 case cần đặt Saleable Qty nhưng chưa ai biết cách đặt, vậy mà report vẫn ghi "chạy được toàn bộ".

**Đề xuất:**
- `rules/01` Bước 3: mỗi CO cần trạng thái đặc biệt phải ghi **cách gây ra** (điều khiển: admin, API, DB, feature flag, giả lập thời gian, 2 phiên) và **cách xác minh** (quan sát: UI, API, DB, log).
- Bảng SETUP thêm cột **Trạng thái**: `Sẵn sàng / Cần chuẩn bị / Chưa rõ cách làm`.
- Mức sẵn sàng thêm `Blocked - SETUP-xx` cho case phụ thuộc SETUP *Chưa rõ cách làm*. Validator tính mức này, Excel hiển thị.
- DoD (`rules/05`): report liệt kê SETUP *Chưa rõ cách làm* và người cần cung cấp.

## 5. Chi tiết — Nhóm C: quy trình

### C1 — Vòng phản biện độc lập (Bắt buộc)

**Vấn đề.** Agent tự review chính sản phẩm của mình sẽ có cùng điểm mù như lúc sinh. DEV-3648: tự review của agent (report §6) chỉ sửa Priority/nhãn, không phát hiện lỗ hổng điều kiện nào; review độc lập phát hiện 1 Critical + 8 Major.

**Đề xuất `rules/01` Bước 5 + `tc-generate`:**
> 5b. Sau tự review, chạy **review độc lập**: một subagent mới, không chung ngữ cảnh, chỉ nhận tài liệu nguồn + `analysis.md` + `testcases.csv`, chạy `tc-review` với nhiệm vụ **tìm điều kiện còn thiếu** (A1–A5) và **giả định chưa đánh dấu** (B1). Agent chính xử lý từng phát hiện (nhận / từ chối kèm lý do) trước khi xuất. Report có mục *Kết quả phản biện*.

Nếu môi trường không có subagent: agent chạy lại `tc-review` trong một lượt riêng, bắt đầu từ việc đọc lại nguồn, không dựa vào analysis.

### C2 — Đề xuất review không bị thất lạc (Nên có)

- `tc-review`: `review.md` ghi **phiên bản và thời điểm** của bộ test được review.
- `tc-generate` (chế độ cập nhật): đọc `review.md` + `testcases-additional.csv`. Mỗi đề xuất → *Đã nhận (ID)* / *Từ chối (lý do)* trong report. Review cũ chuyển thành `review.vX.md`.

### C3 — Học từ lỗi lọt (Nên có)

Mục mới trong `rules/05`: lỗi tester / production tìm ra mà bộ test không phủ → ghi vào `rules/04-domain/<miền>.md` (mục *Bài học*), kèm key bug. Lần sinh sau checklist sẽ có sẵn mục này.

### C4 — Hướng dẫn tester (Nên có)

`docs/huong-dan-tester.md` (1 trang) và sheet *Hướng dẫn* trong xlsx, gồm:
- ý nghĩa Ready / Needs Clarification / Blocked;
- case Needs Clarification bị Fail thì ghi câu hỏi cho BA trước khi log bug;
- cập nhật `Status`;
- cách báo case sai / thiếu để vòng sau sửa (C3).

## 6. Nhóm D: định dạng (Nên có)

- **D1.** `rules/03` thêm bảng định nghĩa `Test_Type`: Security = có vector tấn công / phân quyền / lộ dữ liệu; Integration = qua ranh giới module hoặc hệ thống; Validation = ràng buộc dữ liệu nhập; v.v. Preconditions chỉ tham chiếu SETUP mà case thật sự cần.

## 7. Thay đổi validator / template / skill tương ứng

| Hạng mục | Thay đổi |
|---|---|
| `templates/analysis-template.md` | Thêm §4a Mệnh đề nguồn, §8 bảng ma trận State × Event, §9a Ma trận tương tác, §9b Sự kiện × kênh, cột *Loại* ở Danh mục nguồn, cột *Trạng thái* ở SETUP, dòng "Checklist miền đã dùng", "Mức độ chi tiết" |
| `scripts/validate_testcases.py` | Mệnh đề chưa gắn CO (ERROR); ô trống ở ma trận ST (WARNING); phụ thuộc ghi bằng chữ tự do (WARNING); đối chiếu AS ↔ case (WARNING); mức `Blocked - SETUP-xx`; chỉ số "mệnh đề có oracle đã xác nhận" |
| `scripts/export_xlsx.py` | Sheet *Clauses* (Mệnh đề → CO → TC), sheet *Hướng dẫn* |
| `templates/report-template.md` | Chỉ số mệnh đề; mức độ chi tiết; kết quả phản biện; đề xuất review đã nhận / từ chối; SETUP chưa sẵn sàng |
| `tc-generate` / `tc-analyze` / `tc-review` | Bước A1–A5 trong phân tích; bước 5b phản biện độc lập; đọc review cũ khi cập nhật |
| `examples/LOGIN` | Cập nhật theo template mới để làm mẫu |

## 8. Thứ tự triển khai đề xuất

1. **A1 + B1 + validator** — tạo mẫu số khách quan và chặn giả định ẩn. Tác động lớn nhất, ít tranh cãi.
2. **A2, A3, A4, A5** — mở rộng điều kiện. Cập nhật template và `examples/LOGIN`.
3. **B4 + C1** — sẵn sàng thực thi và phản biện độc lập.
4. Các mục *Nên có* còn lại.

**Đo hiệu quả:** sinh lại DEV-3648 từ đầu bằng bộ rules mới. Kỳ vọng bộ test mới tự tìm được F-01…F-09 của `output/DEV-3648/review.md` mà không cần review thủ công. Mục nào còn sót cho thấy rule tương ứng chưa đủ cụ thể.
