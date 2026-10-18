# 02 — Kỹ thuật thiết kế test (vận dụng ISTQB CTFL v4.0 §4.2)

## Nguyên tắc chọn kỹ thuật

> Chọn kỹ thuật theo **cấu trúc của yêu cầu và rủi ro**, không theo từ khoá trong tài liệu. Mỗi kỹ thuật được chọn phải chỉ ra **các mục cần bao phủ** (phân vùng, biên, rule, chuyển đổi, cặp giá trị…) — mỗi mục là một điều kiện kiểm thử `CO-xx` trong `analysis.md` — và test case nào kiểm tra chúng. Khi một kỹ thuật có dấu hiệu áp dụng nhưng không phù hợp hoặc không thêm giá trị kiểm thử, ghi lý do ở cột *Ghi chú* của điều kiện.

Mỗi test case ghi kỹ thuật **chính** ở cột `Technique`.

| Mã | Kỹ thuật | Mục bao phủ |
|---|---|---|
| `EP` | Equivalence Partitioning — Phân vùng tương đương | Mỗi phân vùng (hợp lệ và không hợp lệ) |
| `BVA` | Boundary Value Analysis — Giá trị biên | Mỗi giá trị biên đã chọn của phân vùng **có thứ tự** |
| `DT` | Decision Table — Bảng quyết định | Mỗi rule khả thi của bảng |
| `ST` | State Transition — Chuyển trạng thái | Mỗi chuyển đổi hợp lệ (+ chuyển đổi không hợp lệ được chọn theo rủi ro) |
| `UC` | Use Case / Scenario | Luồng chính, mỗi luồng thay thế, mỗi luồng ngoại lệ |
| `PW` | Pairwise / Combinatorial | Mỗi cặp giá trị tham số (sau khi loại tổ hợp không khả thi) |
| `CRUD` | Ma trận CRUD | Mỗi thao tác Tạo/Đọc/Sửa/Xoá áp dụng cho thực thể |
| `PERM` | Ma trận phân quyền | Mỗi ô (vai trò × hành động) có rủi ro |
| `EG` | Error Guessing — Đoán lỗi | Mỗi lỗi giả định cụ thể (có cơ sở: bug cũ, kinh nghiệm) |
| `CL` | Checklist-based | Mỗi mục checklist áp dụng |

---

## EP — Phân vùng tương đương

1. Phân vùng dựa trên **cách hệ thống xử lý** (các giá trị được xử lý giống nhau → cùng phân vùng), không chỉ dựa trên hình thức dữ liệu. Hai giá trị cùng định dạng nhưng đi qua nhánh nghiệp vụ khác nhau (vd. khách VIP và thường) là hai phân vùng.
2. Ghi bảng phân vùng trong `analysis.md`: phân vùng, hợp lệ/không, giá trị đại diện, nguồn.
3. **Phân vùng hợp lệ:** có thể gộp nhiều phân vùng hợp lệ của các trường khác nhau vào cùng 1 case nếu không che lấp lỗi.
4. **Phân vùng không hợp lệ:** mỗi case chứa **đúng 1** giá trị không hợp lệ, các trường còn lại hợp lệ — để biết chính xác lỗi đến từ đâu.
5. Phân vùng không hợp lệ thường gặp: rỗng, chỉ khoảng trắng, sai kiểu, sai định dạng, ngoài miền, ký tự đặc biệt, null.

Ví dụ trường *Tuổi* (18–60, số nguyên):

| Phân vùng | Loại | Giá trị đại diện |
|---|---|---|
| 18 ≤ x ≤ 60 | Hợp lệ | 35 |
| x < 18 | Không hợp lệ | 10 |
| x > 60 | Không hợp lệ | 75 |
| Số thập phân | Không hợp lệ | 20.5 |
| Không phải số | Không hợp lệ | "abc" |
| Rỗng | Không hợp lệ | (để trống) |

## BVA — Giá trị biên

- Chỉ áp dụng cho phân vùng **có thứ tự** (số, độ dài, ngày giờ, số lượng, dung lượng, số lần thử, phân trang).
- Ghi rõ trong `analysis.md`: **biên**, **đơn vị bước** (số nguyên ±1; tiền 2 số thập phân ±0.01; độ dài ±1 ký tự; ngày ±1 ngày) và **mức coverage đã chọn**:
  - *2-value BVA* (mặc định): mỗi biên + giá trị liền kề phía ngoài → `min-1, min, max, max+1`.
  - *3-value BVA* (khi rủi ro cao: tiền, tồn kho, giới hạn bảo mật): thêm giá trị liền kề phía trong → `min-1, min, min+1, max-1, max, max+1`.
- Biên tài liệu không nêu → **không tự chế số**; ghi miền là *chưa xác nhận*, tạo `Q-xx`, điều kiện tương ứng để `Pending - Q-xx` hoặc thiết kế với `AS-xx`.

Ví dụ *Tên đăng nhập 6–20 ký tự*, 2-value: 5 (bị chặn), 6 (chấp nhận), 20 (chấp nhận), 21 (bị chặn).

## DT — Bảng quyết định

1. Liệt kê điều kiện (C1..Cn) và hành động (A1..Am); điều kiện không nhị phân thì liệt kê giá trị.
2. Xét **các tổ hợp khả thi**: loại tổ hợp không thể xảy ra (ghi lý do), lưu ý điều kiện **phụ thuộc nhau** và điều kiện **có thể đồng thời đúng**.
3. Rút gọn: gộp các rule cho cùng hành động mà một điều kiện không ảnh hưởng (ghi `-`) — chỉ khi chắc chắn điều kiện đó không ảnh hưởng.
4. Mỗi rule còn lại là một `CO-xx` và cần **≥ 1** case. Một rule có thể cần nhiều case khi có dữ liệu hoặc rủi ro khác nhau (vd. cùng rule "giảm giá" nhưng khác biên giá trị đơn). Ghi rule ID (`DT1-R3`) ở `Notes`.
5. **Loại một tổ hợp khả thi** phải ghi lý do **chứng minh hành vi không đổi** (vd. "mỗi dòng xử lý độc lập, đã có CO-xx kiểm tra hai dòng khác loại cùng lúc"). Lý do kiểu "không thêm giá trị" / "đã có case tương tự" không được chấp nhận.

### Tập phần tử

Khi điều kiện áp dụng cho **từng phần tử của một tập** (dòng giỏ hàng, item đơn hàng, bản ghi được chọn trong danh sách, file trong lô upload) và có **hành động tổng hợp** trên cả tập (nút được bật/tắt, thông báo chung, tổng tiền, số lượng đếm), ngoài các rule cho một phần tử phải xét:

| Mục | Ví dụ (giỏ hàng) |
|---|---|
| Phần tử **nằm ngoài** tập được chọn/áp dụng chịu cùng sự kiện | SP **không được tick** hết hàng lúc bấm Mua hàng |
| Phần tử **duy nhất** thoả điều kiện chuyển sang không thoả → tập rỗng | SP được tick **duy nhất** hết hàng → nút Mua hàng phải Disable |
| **≥ 2 phần tử thuộc các rule khác nhau cùng lúc** | Dòng A hết hàng + dòng B thiếu số lượng trong cùng một lần kiểm tra |
| Tập rỗng · 1 phần tử · tất cả phần tử cùng rule | Giỏ trống; giỏ 1 SP; tất cả SP hết hàng |

Mỗi mục có rủi ro → `CO-xx` (kỹ thuật `DT`); mục không áp dụng → `N/A - lý do`. Ghi bảng này ngay dưới bảng quyết định liên quan trong `analysis.md`.

## ST — Chuyển trạng thái

1. Mô hình hoá **có căn cứ**: trạng thái, sự kiện, điều kiện chặn (guard), hành động — mỗi chuyển đổi trỏ được về nguồn. Chuyển đổi suy luận ra (không có trong tài liệu) → `Q-xx`.
2. Lập **ma trận trạng thái đầy đủ** (hàng = trạng thái, cột = sự kiện, gồm cả sự kiện từ người dùng, hệ thống và tác nhân khác). **Mỗi ô** điền một trong: `→ <trạng thái kế tiếp> (nguồn)` · `Bị chặn (nguồn)` · `Không đổi (nguồn)` · `Không khả thi - <lý do>` · `Q-xx`. **Không để ô trống** — ô trống là chỗ chưa ai nghĩ tới, thường là nơi có lỗi. Danh sách chuyển đổi (dạng bảng dòng) chỉ là phần trích của ma trận này.
3. Bao phủ tối thiểu: **mọi chuyển đổi hợp lệ** ít nhất 1 lần (0-switch coverage); **chuyển đổi không hợp lệ / ô "Bị chặn"** được chọn theo rủi ro → hệ thống phải chặn; ô `Q-xx` → `CO-xx` `Pending - Q-xx`.
4. Trạng thái "kết thúc" chỉ được coi là không thể chuyển tiếp khi nguồn nói vậy — nhiều nghiệp vụ cho phép mở lại / hoàn tác.
5. Luồng nghiệp vụ cốt lõi, rủi ro cao: cân nhắc 1-switch (chuỗi 2 chuyển đổi liên tiếp).

## UC — Use Case / Scenario

- Luồng chính, mỗi luồng thay thế, mỗi luồng ngoại lệ (lỗi validate, mất kết nối, timeout, huỷ giữa chừng, phiên hết hạn) **có trong nguồn hoặc có rủi ro rõ** → mỗi luồng là một `CO-xx`.
- Acceptance Criteria dạng Gherkin: mỗi scenario → ≥1 `CO-xx`; mỗi mệnh đề `Then` là một **mệnh đề nguồn** (`<Req_ID>-c<n>`, `rules/01` Bước 2) cần được kiểm tra bởi ít nhất một case. `Given` → Preconditions, `When` → Steps, `Then` → Expected_Result.
- `When` chỉ nêu **một** sự kiện kích hoạt / kênh, nhưng hành vi thường áp dụng ở nhiều thời điểm và kênh → xét bảng *Sự kiện kích hoạt & kênh* (`rules/01` Bước 3.5).

## PW — Pairwise

1. Xác định rõ **tham số**, **giá trị** của từng tham số và **ràng buộc** (tổ hợp không khả thi, tổ hợp bắt buộc).
2. Sinh bộ all-pairs (mọi cặp giá trị xuất hiện ít nhất 1 lần) có tôn trọng ràng buộc; ghi bảng tổ hợp vào `analysis.md`.
3. Pairwise **không thay thế** các tổ hợp nghiệp vụ rủi ro cao đã biết — luôn thêm chúng vào riêng.

## CRUD — Ma trận CRUD

Với mỗi thực thể: Create / Read (chi tiết + danh sách) / Update / Delete — chỉ các thao tác nguồn có mô tả. Kiểm tra: dữ liệu lưu đúng, hiển thị lại đúng sau reload, xoá thì không còn xuất hiện (hoặc soft-delete theo nguồn), ràng buộc tham chiếu.

## PERM — Ma trận phân quyền

Bảng `Vai trò × Hành động → Được phép / Không` (có nguồn). Kiểm tra vai trò thực hiện được hành động được phép; **bị chặn** ở hành động không được phép — cả trên UI **và** qua URL/API khi có rủi ro; người chưa đăng nhập.

## EG — Đoán lỗi (gợi ý)

Mỗi lỗi giả định ghi **cơ sở** (bug cũ, sự cố tương tự, kinh nghiệm). Gợi ý:
- Double-click / submit 2 lần; nút Back sau khi submit; refresh (F5) giữa luồng
- Hai tab cùng sửa một bản ghi
- Khoảng trắng đầu/cuối; Unicode, emoji, tiếng Việt có dấu
- Chuỗi rất dài; HTML/script (`<script>alert(1)</script>`); SQL (`' OR '1'='1`)
- Số âm, 0, rất lớn, có dấu phân cách hàng nghìn
- Phiên hết hạn khi đang thao tác; mất mạng, API 500, API chậm
- Múi giờ; dữ liệu rỗng / cực nhiều

---

## Gợi ý dấu hiệu (chỉ để cân nhắc, không bắt buộc)

| Trong tài liệu thấy… | Cân nhắc | Áp dụng khi |
|---|---|---|
| "từ … đến …", "tối đa", "tối thiểu" | BVA + EP | Miền có thứ tự và hệ thống xử lý khác nhau ở hai phía biên |
| "nếu … và … thì …" | DT | Các điều kiện **kết hợp** quyết định kết quả (không độc lập nhau) |
| "trạng thái", "chuyển sang", vòng đời | ST | Hành vi phụ thuộc trạng thái hiện tại |
| User story, use case, luồng màn hình | UC | Có chuỗi bước người dùng với nhánh rẽ |
| Nhiều trình duyệt/thiết bị/cấu hình | PW | Tổ hợp đầy đủ quá lớn và lỗi chủ yếu do tương tác cặp |
| Thêm/sửa/xoá dữ liệu | CRUD | Thực thể có vòng đời dữ liệu |
| Nhiều vai trò | PERM | Quyền khác nhau giữa vai trò |
| Hai yêu cầu cùng nhắc tới một trạng thái/dữ liệu (chọn, số lượng, nút, tổng) | DT / ST qua *Ma trận tương tác* (`rules/01` Bước 3.2) | Một yêu cầu thay đổi dữ liệu mà yêu cầu kia phụ thuộc |
| "mỗi dòng", "các sản phẩm được chọn", "từng bản ghi" | DT — mục *Tập phần tử* | Có hành động tổng hợp trên cả tập |
