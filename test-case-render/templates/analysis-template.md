# Phân tích yêu cầu — <FEATURE>

> Validator đọc các bảng theo **tiêu đề mục** (Danh sách yêu cầu, Mệnh đề nguồn, Quy tắc nghiệp vụ, Yêu cầu ngầm định, Ma trận trạng thái, Ma trận tương tác, Sự kiện kích hoạt & kênh, Câu hỏi, Giả định, Điều kiện kiểm thử, Dữ liệu test & setup) và **cột đầu tiên là ID**. Giữ nguyên tên các mục này.

| Thông tin | Giá trị |
|---|---|
| Người phân tích | <AI agent / tester> |
| Ngày | YYYY-MM-DD |
| Phiên bản phân tích | v1.0 |

## 0. Danh mục nguồn

| Nguồn | Phiên bản / ngày | Trạng thái | Bản trích xuất | Phần bị ảnh hưởng nếu chưa đọc đủ |
|---|---|---|---|---|
| `input/<FEATURE>/<file>` | v1.2 (YYYY-MM-DD) | Đã đọc / Đọc một phần / Chưa đọc được | `_extracted/<file>.md` | – |

## 1. Tóm tắt tính năng

<Tính năng làm gì, cho ai, giá trị nghiệp vụ — 3–5 câu.>

## 2. Phạm vi

**In-scope:**
- ...

**Out-of-scope:**
- ... (lý do)

## 3. Tác nhân & phân quyền

| Vai trò | Mô tả | Quyền chính |
|---|---|---|
| ... | ... | ... |

## 4. Danh sách yêu cầu

> Chỉ yêu cầu **có nguồn**. Không test: ghi `N/A - <lý do>` ở cột *Ghi chú*.

| Req_ID | Mô tả | Nguồn | Rủi ro | Ghi chú |
|---|---|---|---|---|
| REQ-<MODULE>-01 | ... | file.pdf §2.1 tr.3 | High | |

## 4a. Mệnh đề nguồn

> Mỗi khẳng định kiểm tra được của yêu cầu (gạch đầu dòng `Then`, dòng bảng điều kiện, Business Rule, câu "phải / không được / khi … thì …") là **một** dòng. Không gộp hai khẳng định có thể đúng/sai độc lập. Đây là mẫu số khách quan của bao phủ (`rules/01` Bước 2). Cột *CO* điền ở Bước 3; không áp dụng → `N/A - lý do`; chưa thiết kế được → `Pending - Q-xx`.

| Clause_ID | Req_ID | Mệnh đề (bám sát nguyên văn) | CO | Ghi chú |
|---|---|---|---|---|
| REQ-<MODULE>-01-c1 | REQ-<MODULE>-01 | ... | CO-01; CO-02 | |
| REQ-<MODULE>-01-c2 | REQ-<MODULE>-01 | ... | | Pending - Q-02 |

## 5. Quy tắc nghiệp vụ

| Req_ID | Điều kiện | Kết quả | Nguồn |
|---|---|---|---|
| BR-01 | ... | ... | ... |

## 6. Yêu cầu ngầm định

> Kỳ vọng **đề xuất** theo rủi ro/thông lệ, tài liệu không ghi. Chưa phải tiêu chí nghiệm thu cho tới khi *Đã xác nhận*. Trạng thái: `Đề xuất` / `Đã xác nhận` / `Bị từ chối`.

| Req_ID | Mô tả | Cơ sở | Trạng thái xác nhận |
|---|---|---|---|
| IMP-01 | ... | Thông lệ bảo mật / bug DEV-xxx / ticket con ... | Đề xuất |

## 7. Từ điển dữ liệu

| Trường | Kiểu | Bắt buộc | Giới hạn / Miền giá trị | Định dạng | Mặc định | Thông điệp lỗi (nguyên văn, kèm nguồn) |
|---|---|---|---|---|---|---|
| ... | ... | Có | 6–20 ký tự | ... | ... | "..." (§2.1) — hoặc `? (Q-xx)` |

### 7.1 Phân vùng tương đương & giá trị biên

| Trường | Phân vùng hợp lệ | Phân vùng không hợp lệ | Biên · đơn vị bước · mức coverage |
|---|---|---|---|
| ... | ... | ... | 5/6/20/21 · ±1 ký tự · 2-value |

## 8. Trạng thái & chuyển đổi (nếu có)

| Trạng thái hiện tại | Sự kiện | Guard | Trạng thái kế tiếp | Nguồn |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Chuyển đổi **không hợp lệ** chọn để kiểm tra (theo rủi ro): ...

### 8.1 Ma trận trạng thái

> Hàng = trạng thái, cột = sự kiện (người dùng, hệ thống, tác nhân khác). **Mọi ô phải có kết luận**: `→ <trạng thái> (nguồn)` · `Bị chặn (nguồn)` · `Không đổi (nguồn)` · `Không khả thi - lý do` · `Q-xx`. Ô có rủi ro ghi thêm `CO-xx`. Bắt buộc khi có điều kiện kỹ thuật `ST` (`rules/02` §ST).

| Trạng thái \ Sự kiện | <Sự kiện 1> | <Sự kiện 2> | <Sự kiện 3> |
|---|---|---|---|
| <Trạng thái A> | → B (§2.1) · CO-03 | Bị chặn (§2.2) · CO-04 | Q-05 |
| <Trạng thái B> | Không đổi (§2.1) | Không khả thi - <lý do> | → A (§2.3) · CO-05 |

## 9. Bảng quyết định (nếu có)

**DT1 — <tên>**

| | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| C1: ... | Y | Y | N | N |
| C2: ... | Y | N | Y | N |
| **A1: ...** | X | | | |

Tổ hợp không khả thi / bị loại & lý do (tổ hợp **khả thi** bị loại phải chứng minh hành vi không đổi): ...

**Tập phần tử** (khi điều kiện áp dụng cho từng phần tử của một tập và có hành động tổng hợp — `rules/02` §DT *Tập phần tử*):

| Mục | Áp dụng? | CO / lý do |
|---|---|---|
| Phần tử ngoài tập được chọn chịu cùng sự kiện | | |
| Phần tử duy nhất thoả điều kiện chuyển sang không thoả (tập rỗng) | | |
| ≥ 2 phần tử thuộc các rule khác nhau cùng lúc | | |
| Tập rỗng · 1 phần tử · tất cả phần tử cùng rule | | |

## 9a. Ma trận tương tác

> Thực thể/trạng thái dùng chung giữa các yêu cầu (vd. trạng thái chọn, số lượng, trạng thái nút, tổng tiền, bộ đếm). Mỗi cặp *yêu cầu A thay đổi X — yêu cầu B phụ thuộc X* là một dòng (`rules/01` Bước 3.2). Kết luận: `CO-xx` / `N/A - lý do` / `Pending - Q-xx`. Nếu tính năng chỉ có một yêu cầu, ghi một dòng `N/A - lý do`.

| IX_ID | Thực thể / trạng thái | A — yêu cầu thay đổi | B — yêu cầu phụ thuộc | Câu hỏi kiểm thử | Kết luận |
|---|---|---|---|---|---|
| IX-01 | ... | REQ-...-02 | REQ-...-04 | Khi A làm X thay đổi (đặc biệt: tập thoả B thành rỗng / 1 phần tử), B còn đúng không? | CO-10 |

## 9b. Sự kiện kích hoạt & kênh

> Với mỗi hành vi chính: **khi nào** hệ thống áp dụng (vào màn hình, tải lại, bấm hành động chính, dữ liệu đổi ở nền, hết phiên) và **ở đâu** cùng dữ liệu được truy cập (kênh hiển thị thứ hai, URL trực tiếp của bước sau, Back, tab/phiên/thiết bị thứ hai, đăng nhập lại, API). Danh sách tối thiểu: `rules/04` §B. Kết luận: `CO-xx` / `N/A - lý do` / `Pending - Q-xx`.

| EV_ID | Hành vi | Sự kiện kích hoạt / kênh | Kết luận |
|---|---|---|---|
| EV-01 | ... | Tải lại trang | CO-12 |
| EV-02 | ... | Truy cập thẳng URL bước sau | Pending - Q-06 |

## 10. Ma trận phân quyền (nếu có)

| Hành động \ Vai trò | Admin | User | Guest |
|---|---|---|---|
| ... | ✔ | ✔ | ✘ |

## 11. Tích hợp & phụ thuộc

- API / hệ thống ngoài / email / job: ...

## 12. Quan sát UI (từ mockup / screenshot)

| Màn hình | Thành phần | Ghi chú / chênh lệch so với văn bản |
|---|---|---|
| ... | ... | ... |

## 13. Câu hỏi làm rõ

| ID | Câu hỏi | Liên quan | Mức độ | Trả lời |
|---|---|---|---|---|
| Q-01 | ... | REQ-...-01 | Blocker / Major / Minor | (chờ) |

## 14. Giả định

> Giả định **tạm thời** khi Q chưa có trả lời. Trạng thái: `Chưa xác nhận` / `Đã xác nhận` / `Sai — đã sửa case`.

| ID | Giả định | Câu hỏi liên quan | Case bị ảnh hưởng | Trạng thái xác nhận |
|---|---|---|---|---|
| AS-01 | ... | Q-01 | TC-...-003, TC-...-004 | Chưa xác nhận |

## 15. Đánh giá rủi ro

| Khu vực | Khả năng (1–3) | Ảnh hưởng (1–3) | Điểm | Priority đề xuất |
|---|---|---|---|---|
| ... | 3 | 3 | 9 | P1 |

## 16. Điều kiện kiểm thử

> Mỗi dòng là **một mục cần bao phủ** (phân vùng, biên, rule DT, chuyển trạng thái, luồng, mục checklist…). Cột *Test case* điền sau Bước 4. Không áp dụng → `N/A - <lý do>`; chưa thiết kế được → `Pending - Q-xx`.

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-01 | REQ-...-01 | ... | BVA | TC-...-001 | |
| CO-02 | REQ-...-02 | ... | DT | | Pending - Q-01 |

## 17. Dữ liệu test & setup

> Quy trình chuẩn bị/reset dùng chung. Case tham chiếu bằng `Theo SETUP-xx` ở Preconditions — chỉ SETUP mà case thật sự cần. Ghi rõ dữ liệu nào **cần tester chuẩn bị** và dữ liệu nào **đã xác nhận tồn tại** trên môi trường.
> *Trạng thái*: `Sẵn sàng` (đã có / có quy trình chạy được) · `Cần chuẩn bị` (biết cách, tester tự làm theo cột *Cách tạo*) · `Chưa rõ cách làm` (cần dev/QA lead cung cấp — case tham chiếu bị **Blocked**).

| Setup_ID | Dữ liệu / trạng thái | Cách tạo (điều khiển) | Cách xác minh (quan sát) | Cách reset | Nguồn dữ liệu | Trạng thái |
|---|---|---|---|---|---|---|
| SETUP-01 | ... | UI / admin / API / DB / cấu hình … | UI / API / DB / log … | ... | Cần chuẩn bị / Đã có trên môi trường | Cần chuẩn bị |
