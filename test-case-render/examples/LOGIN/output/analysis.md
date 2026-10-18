# Phân tích yêu cầu — LOGIN (ví dụ mẫu)

| Thông tin | Giá trị |
|---|---|
| Ngày | 2026-10-16 |
| Phiên bản phân tích | v1.2 (thêm mệnh đề nguồn, ma trận trạng thái, ma trận tương tác, sự kiện × kênh, trạng thái SETUP) |

## 0. Danh mục nguồn

| Nguồn | Phiên bản / ngày | Trạng thái | Bản trích xuất | Phần bị ảnh hưởng nếu chưa đọc đủ |
|---|---|---|---|---|
| `examples/LOGIN/input/spec.md` | v1.0 | Đã đọc | (chính file này) | – |

## 1. Tóm tắt tính năng

Người dùng đã đăng ký đăng nhập bằng email + mật khẩu để vào Trang chủ. Hệ thống validate đầu vào, báo lỗi khi sai thông tin, khoá tạm tài khoản sau 5 lần sai liên tiếp và chặn tài khoản Inactive.

## 2. Phạm vi

**In-scope:** màn hình Đăng nhập, validate, khoá tài khoản, trạng thái tài khoản.
**Out-of-scope:** Quên mật khẩu, Đăng ký, đăng nhập mạng xã hội (không có trong tài liệu).

## 4. Danh sách yêu cầu

| Req_ID | Mô tả | Nguồn | Rủi ro | Ghi chú |
|---|---|---|---|---|
| FR-01 | Đăng nhập bằng Email + Mật khẩu, thành công → Trang chủ | spec.md §2.1 | High | |
| FR-02 | Email bắt buộc, đúng định dạng | spec.md §2.1 | Medium | |
| FR-03 | Mật khẩu bắt buộc, 8–32 ký tự | spec.md §2.1 | Medium | |
| FR-04 | Sai email/mật khẩu → "Sai email hoặc mật khẩu" | spec.md §2.1 | High | |
| FR-05 | Sai 5 lần liên tiếp → khoá 15 phút | spec.md §2.1 | High | |
| FR-06 | Tài khoản Inactive không được đăng nhập | spec.md §2.1 | High | |

## 4a. Mệnh đề nguồn

| Clause_ID | Req_ID | Mệnh đề (bám sát nguyên văn) | CO | Ghi chú |
|---|---|---|---|---|
| FR-01-c1 | FR-01 | Người dùng đăng nhập bằng Email và Mật khẩu | CO-01 | |
| FR-01-c2 | FR-01 | Đăng nhập thành công chuyển tới "Trang chủ" | CO-01 | |
| FR-02-c1 | FR-02 | Email bắt buộc | CO-02 | |
| FR-02-c2 | FR-02 | Email đúng định dạng email; lỗi "Email không đúng định dạng" | CO-03; CO-04 | |
| FR-03-c1 | FR-03 | Mật khẩu bắt buộc | CO-05 | |
| FR-03-c2 | FR-03 | Mật khẩu 8–32 ký tự; lỗi "Mật khẩu phải từ 8 đến 32 ký tự" | CO-06; CO-07; CO-08; CO-09 | |
| FR-04-c1 | FR-04 | Sai email hoặc mật khẩu hiển thị "Sai email hoặc mật khẩu" | CO-10; CO-11 | |
| FR-05-c1 | FR-05 | Sai 5 lần liên tiếp thì khoá tài khoản | CO-12; CO-13; CO-19 | |
| FR-05-c2 | FR-05 | Thời gian khoá 15 phút | CO-14; CO-15 | |
| FR-05-c3 | FR-05 | Thông báo "Tài khoản bị khoá tạm thời" | CO-13 | |
| FR-06-c1 | FR-06 | Tài khoản Inactive không được đăng nhập | CO-17 | |
| IMP-01-c1 | IMP-01 | Mật khẩu hiển thị dạng ẩn khi nhập | CO-18 | |

## 6. Yêu cầu ngầm định

| Req_ID | Mô tả | Cơ sở | Trạng thái xác nhận |
|---|---|---|---|
| IMP-01 | Mật khẩu hiển thị dạng ẩn khi nhập | Thông lệ bảo mật | Đề xuất |

## 7. Từ điển dữ liệu

| Trường | Kiểu | Bắt buộc | Giới hạn | Thông điệp lỗi (nguyên văn, kèm nguồn) |
|---|---|---|---|---|
| Email | Text | Có | ? (Q-01) | "Email không đúng định dạng" (§2.1) |
| Mật khẩu | Password | Có | 8–32 ký tự | "Mật khẩu phải từ 8 đến 32 ký tự" (§2.1) |

### 7.1 Phân vùng tương đương & giá trị biên

| Trường | Hợp lệ | Không hợp lệ | Biên · đơn vị bước · mức coverage |
|---|---|---|---|
| Mật khẩu (độ dài) | 8–32 ký tự | rỗng, <8, >32 | 7/8/32/33 · ±1 ký tự · 2-value |
| Email | user@domain.tld | rỗng, thiếu @ | Độ dài tối đa chưa xác nhận (Q-01) |
| Số lần sai liên tiếp | 0–4 (chưa khoá) | ≥5 (khoá) | 4/5 · ±1 lần · 2-value |

## 8. Trạng thái tài khoản

| Hiện tại | Sự kiện | Guard | Kế tiếp | Nguồn |
|---|---|---|---|---|
| Active | Đăng nhập sai lần thứ 5 liên tiếp | | Locked (15 phút) | FR-05 |
| Locked | Hết 15 phút | | Active | FR-05 |
| Locked | Đăng nhập đúng mật khẩu | trong 15 phút | Locked (bị chặn) | FR-05 |
| Inactive | Đăng nhập đúng mật khẩu | | Inactive (bị chặn) | FR-06 |

### 8.1 Ma trận trạng thái

| Trạng thái \ Sự kiện | Đăng nhập đúng mật khẩu | Đăng nhập sai mật khẩu | Hết 15 phút kể từ lúc khoá / theo thời gian |
|---|---|---|---|
| Active, bộ đếm sai 0–3 | → Đã đăng nhập (FR-01) · CO-01; bộ đếm reset: Q-02 | → Active, bộ đếm +1 (FR-05) · CO-12 | Q-08 (bộ đếm có tự reset theo thời gian?) · CO-24 |
| Active, bộ đếm sai = 4 | → Đã đăng nhập (FR-01); bộ đếm reset: Q-02 · CO-16 | → Locked (FR-05) · CO-13 | Q-08 · CO-24 |
| Locked | Bị chặn (FR-05) · CO-14 | Bị chặn (FR-05); có kéo dài thời gian khoá không: Q-06 · CO-23 | → Active (FR-05) · CO-15 |
| Inactive | Bị chặn (FR-06) · CO-17 | Q-04 (có tính bộ đếm / khoá không?) · CO-21 | Không đổi (FR-06 không có điều kiện thời gian) |

## 9a. Ma trận tương tác

| IX_ID | Thực thể / trạng thái | A — yêu cầu thay đổi | B — yêu cầu phụ thuộc | Câu hỏi kiểm thử | Kết luận |
|---|---|---|---|---|---|
| IX-01 | Bộ đếm sai | FR-01 (đăng nhập đúng) | FR-05 (5 lần **liên tiếp**) | Đăng nhập đúng xen giữa có reset chuỗi "liên tiếp" không? | CO-16 |
| IX-02 | Bộ đếm sai | FR-02, FR-03 (lỗi validate) | FR-05 | Lần submit bị chặn bởi validate (rỗng, sai định dạng, sai độ dài) có tính là một lần sai không? | Pending - Q-05 |
| IX-03 | Bộ đếm sai | FR-04 (email chưa đăng ký) | FR-05 | Email chưa đăng ký có làm tăng bộ đếm của tài khoản nào không? | N/A - bộ đếm gắn với tài khoản; email chưa đăng ký không có tài khoản |
| IX-04 | Trạng thái tài khoản | FR-06 (Inactive) | FR-05 | Tài khoản Inactive nhập sai mật khẩu có bị tính bộ đếm / khoá không? | Pending - Q-04 |
| IX-05 | Thông điệp | FR-05 (Locked) | FR-04 | Tài khoản đang khoá nhập sai mật khẩu hiển thị thông điệp nào, có kéo dài thời gian khoá không? | Pending - Q-06 |

## 9b. Sự kiện kích hoạt & kênh

| EV_ID | Hành vi | Sự kiện kích hoạt / kênh | Kết luận |
|---|---|---|---|
| EV-01 | Đăng nhập | Submit bằng phím Enter thay cho nút "Đăng nhập" | N/A - tài liệu không nêu; thuộc checklist UI chung, rủi ro thấp đối với tính năng này |
| EV-02 | Khoá tài khoản | Đăng nhập từ trình duyệt / thiết bị khác trong thời gian khoá | CO-19 |
| EV-03 | Đăng nhập thành công | Bấm Back / mở lại màn hình Đăng nhập khi đã đăng nhập | Pending - Q-07 |
| EV-04 | Mở khoá | Sự kiện thời gian: hết 15 phút | CO-15 |
| EV-05 | Bộ đếm sai | Các lần sai trên nhiều trình duyệt khác nhau | N/A - FR-05 khoá theo tài khoản, đã có CO-19 kiểm tra tính nhất quán giữa trình duyệt; cộng dồn thuộc cùng câu hỏi Q-08 về phạm vi bộ đếm |

## 13. Câu hỏi làm rõ

| ID | Câu hỏi | Liên quan | Mức độ | Trả lời |
|---|---|---|---|---|
| Q-01 | Email tối đa bao nhiêu ký tự? (64 hay 254?) | FR-02 | Minor | (chờ) |
| Q-02 | Bộ đếm lần sai có reset sau 1 lần đăng nhập thành công không? | FR-05 | Major | (chờ) |
| Q-03 | Tài khoản Inactive đăng nhập thì hiển thị thông điệp gì? | FR-06 | Major | (chờ) |
| Q-04 | Tài khoản Inactive nhập sai mật khẩu có bị tính vào bộ đếm / bị khoá không? | FR-05, FR-06 | Minor | (chờ) |
| Q-05 | Lần submit bị chặn bởi validate (Email rỗng / sai định dạng, Mật khẩu ngoài 8–32 ký tự) có tính là một lần sai không? | FR-02, FR-03, FR-05 | Major | (chờ) |
| Q-06 | Khi đang khoá, nhập sai mật khẩu có kéo dài thời gian khoá không? Hiển thị thông điệp nào? | FR-04, FR-05 | Minor | (chờ) |
| Q-07 | Đã đăng nhập mà bấm Back / mở lại URL màn hình Đăng nhập thì chuyển về Trang chủ hay hiển thị form? | FR-01 | Minor | (chờ) |
| Q-08 | Bộ đếm sai liên tiếp có tự reset sau một khoảng thời gian không (vd. sai 4 lần hôm qua, hôm nay sai 1 lần có bị khoá)? | FR-05 | Major | (chờ) |

## 14. Giả định

| ID | Giả định | Câu hỏi liên quan | Case bị ảnh hưởng | Trạng thái xác nhận |
|---|---|---|---|---|
| AS-01 | Đăng nhập thành công reset bộ đếm về 0 | Q-02 | TC-LOGIN-015 | Chưa xác nhận |

## 16. Điều kiện kiểm thử

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-01 | FR-01 | Luồng chính: email + mật khẩu đúng → Trang chủ | UC | TC-LOGIN-001; TC-LOGIN-006; TC-LOGIN-007 | |
| CO-02 | FR-02 | Email rỗng | EP | TC-LOGIN-002 | |
| CO-03 | FR-02 | Email sai định dạng (thiếu @) | EP | TC-LOGIN-003 | |
| CO-04 | FR-02 | Email tại biên độ dài tối đa | BVA | | Pending - Q-01 |
| CO-05 | FR-03 | Mật khẩu rỗng | EP | TC-LOGIN-004 | |
| CO-06 | FR-03 | Độ dài 7 (dưới min) | BVA | TC-LOGIN-005 | |
| CO-07 | FR-03 | Độ dài 8 (min) | BVA | TC-LOGIN-006 | |
| CO-08 | FR-03 | Độ dài 32 (max) | BVA | TC-LOGIN-007 | |
| CO-09 | FR-03 | Độ dài 33 (trên max) | BVA | TC-LOGIN-008 | |
| CO-10 | FR-04 | Email chưa đăng ký | EP | TC-LOGIN-009 | |
| CO-11 | FR-04 | Mật khẩu sai với email đã đăng ký | EP | TC-LOGIN-010 | |
| CO-12 | FR-05 | Biên 4 lần sai — chưa khoá | ST | TC-LOGIN-011 | |
| CO-13 | FR-05 | Active → Locked ở lần sai thứ 5 | ST | TC-LOGIN-012 | |
| CO-14 | FR-05 | Locked + mật khẩu đúng → vẫn bị chặn | ST | TC-LOGIN-013 | |
| CO-15 | FR-05 | Locked → Active sau 15 phút | ST | TC-LOGIN-014 | |
| CO-16 | FR-05 | Bộ đếm reset sau đăng nhập thành công | ST | TC-LOGIN-015 | Dựa trên AS-01 |
| CO-17 | FR-06 | Inactive bị chặn đăng nhập | ST | TC-LOGIN-016 | Thông điệp chờ Q-03 |
| CO-18 | IMP-01 | Mật khẩu hiển thị dạng ẩn | CL | TC-LOGIN-017 | Không có điều kiện "bị chặn" — chỉ kiểm tra hiển thị |
| CO-19 | FR-05 | Khoá áp dụng cho tài khoản trên trình duyệt khác (EV-02) | ST | TC-LOGIN-018 | |
| CO-20 | FR-01 | Back / mở lại màn hình Đăng nhập khi đã đăng nhập (EV-03) | UC | | Pending - Q-07 |
| CO-21 | FR-05; FR-06 | Inactive + sai mật khẩu (IX-04) | ST | | Pending - Q-04 |
| CO-22 | FR-05; FR-03 | Lần submit lỗi validate có tính vào bộ đếm (IX-02) | DT | | Pending - Q-05 |
| CO-23 | FR-05; FR-04 | Locked + sai mật khẩu (IX-05) | ST | | Pending - Q-06 |
| CO-24 | FR-05 | Bộ đếm hết hạn theo thời gian | ST | | Pending - Q-08 |

## 17. Dữ liệu test & setup

| Setup_ID | Dữ liệu / trạng thái | Cách tạo (điều khiển) | Cách xác minh (quan sát) | Cách reset | Nguồn dữ liệu | Trạng thái |
|---|---|---|---|---|---|---|
| SETUP-01 | user01@test.com, mật khẩu Abc@1234, Active, bộ đếm sai = 0 | Tạo qua trang Đăng ký hoặc admin | Trạng thái tài khoản xem ở màn hình admin | Admin mở khoá + đặt bộ đếm sai = 0 sau mỗi case có đăng nhập sai | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-02 | user08@test.com (mật khẩu Abc@1234, 8 ký tự); user32@test.com (mật khẩu Abc@1234Abc@1234Abc@1234Abc@1234, 32 ký tự); inactive01@test.com (Abc@1234, Inactive) | Admin tạo và đặt trạng thái | Màn hình admin | Không cần — case không làm đổi trạng thái | Cần chuẩn bị | Cần chuẩn bị |
