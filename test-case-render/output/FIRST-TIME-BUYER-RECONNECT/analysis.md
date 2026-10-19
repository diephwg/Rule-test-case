# Phân tích yêu cầu — FIRST-TIME-BUYER-RECONNECT

| Thông tin | Giá trị |
|---|---|
| Người phân tích | Claude Code |
| Ngày | 2026-10-19 |
| Phiên bản phân tích | v1.0 (bản rút gọn — tester yêu cầu ~10 case, chỉ các luồng rủi ro cao nhất) |

## 0. Danh mục nguồn

| Nguồn | Phiên bản / ngày | Trạng thái | Bản trích xuất | Phần bị ảnh hưởng nếu chưa đọc đủ |
|---|---|---|---|---|
| `test-case-render/docs/Task Nhắc Kết nối lại Khách Mua lần đầu tại Boutique Piaget (First Time Buyer Reconnect).docx` (FRD Confluence V2, 19/10/2026 09:22) | V2 | Đọc một phần: file export chứa tracked changes (chữ xoá + chữ mới dính liền, vd. "7248 giờ" = 72→48, "26 Store" = 2→6) và ảnh/sơ đồ không trích được | Không có file `_extracted` (môi trường chưa có Python) | Giá trị due_date và số Store suy ra từ bản sửa mới nhất — xem AS-01, AS-02 |

## 1. Tóm tắt tính năng

Khi khách có đơn hàng đầu tiên tại một Boutique thuộc danh sách (sự kiện `POS_PURCHASE_COMPLETED`), hệ thống tự tạo 1 Task nhắc CA kết nối lại với khách qua SMS, hạn xử lý = thời điểm hoàn thành đơn + 48 giờ (giữ nguyên giờ). Task gán cho Active PIC của khách tại Store đó; chưa có PIC thì gán Store Manager và đánh dấu cần giao lại.

## 2. Phạm vi

**In-scope:** Rule `RULE_FIRST_TIME_BUYER_RECONNECT_PIAGET`; thuộc tính task sinh ra; điều kiện "đơn đầu tiên tại Store"; gán assignee; idempotency; giới hạn quyền sửa của CA; không phản ứng khi đơn bị huỷ/trả.

**Out-of-scope:** Task thủ công/CSV/Data Cloud; Boutique ngoài danh sách; quà tặng; task mốc +7/+30 ngày (đã bãi bỏ); nội dung Push Notification.

## 3. Tác nhân & phân quyền

| Vai trò | Mô tả | Quyền chính |
|---|---|---|
| System Automation Engine | Sinh task | Tạo task (`assigned_by.user_id = "system"`) |
| CA (Active PIC) | Người thực hiện | Hoàn thành, bình luận, đính kèm; không sửa due_date/priority/purpose/kênh/mô tả |
| Store Manager | Nhận task khi khách chưa có PIC | Điều phối lại người phụ trách |
| CRM / Retail Ops HQ | Cấu hình Rule | Cấu hình Rule |

## 4. Danh sách yêu cầu

| Req_ID | Mô tả | Nguồn | Rủi ro | Ghi chú |
|---|---|---|---|---|
| BR-FTB-TRIGGER | Chỉ xử lý khi store_id thuộc conditions.store_ids | FRD §4, §7 E6 | High | |
| BR-FTB-FIRST-ORDER | Chỉ tạo task khi first_transaction_date tại Store chuyển từ null sang có giá trị; xét riêng từng Store | FRD §4, §7 E1–E2 | High | |
| BR-FTB-DUE | due_date = thời điểm hoàn thành đơn + 48 giờ, giữ giờ của đơn | FRD §4, §7 E5 | High | Xem AS-01 |
| BR-FTB-ASSIGNEE | Gán Active PIC; chưa có PIC → SM + needs_reassignment = true, original_pic = null | FRD §4, §7 E3 | High | |
| BR-FTB-ORDER-VALID | Task không đổi khi đơn gốc bị huỷ/trả | FRD §4, §7 E8 | Medium | |
| BR-FTB-EDIT-SCOPE | CA không sửa trường bị khoá | FRD §4, §7 E10 | Medium | |
| FR-FTB-IDEMP | Event trùng (retry) không sinh task trùng | FRD §3 Bước 1, §7 E4 | High | |
| FR-FTB-TASKDEF | Giá trị task ghi lúc tạo (§2) | FRD §2.1–2.6 | High | |

## 4a. Mệnh đề nguồn

| Clause_ID | Req_ID | Mệnh đề (bám sát nguyên văn) | CO | Ghi chú |
|---|---|---|---|---|
| BR-FTB-TRIGGER-c1 | BR-FTB-TRIGGER | Đơn phát sinh ở Boutique khác: bỏ qua | CO-05 | |
| BR-FTB-TRIGGER-c2 | BR-FTB-TRIGGER | Store trong danh sách 6 store_id (292, 34, 294, 58, 40, 202) kích hoạt Rule | CO-01; CO-02 | Đại diện 2 Store, xem report |
| BR-FTB-FIRST-ORDER-c1 | BR-FTB-FIRST-ORDER | first_transaction_date tại S từ null chuyển có giá trị → tạo task cùng bước xử lý | CO-01 | |
| BR-FTB-FIRST-ORDER-c2 | BR-FTB-FIRST-ORDER | first_transaction_date đã có giá trị → mọi đơn mới tại S không tạo task | CO-03 | |
| BR-FTB-FIRST-ORDER-c3 | BR-FTB-FIRST-ORDER | Xét riêng từng Store | CO-04 | |
| BR-FTB-DUE-c1 | BR-FTB-DUE | due_date = event.timestamp + 48 giờ, giữ nguyên giờ, không ép 09:00 | CO-02; CO-08 | |
| BR-FTB-ASSIGNEE-c1 | BR-FTB-ASSIGNEE | Có PIC → assignee = original_pic = PIC | CO-01 | |
| BR-FTB-ASSIGNEE-c2 | BR-FTB-ASSIGNEE | Chưa có PIC → SM, needs_reassignment = true, original_pic = null | CO-06 | |
| BR-FTB-ORDER-VALID-c1 | BR-FTB-ORDER-VALID | Sau khi tạo, đơn huỷ/trả không làm đổi/xoá/tạo lại task | CO-09 | |
| BR-FTB-EDIT-SCOPE-c1 | BR-FTB-EDIT-SCOPE | CA không sửa due_date, priority, purpose, kênh gợi ý, mô tả; vẫn hoàn thành/bình luận/đính kèm | CO-10 | |
| FR-FTB-IDEMP-c1 | FR-FTB-IDEMP | Idempotency Key (rule + event + customer + source_id) chặn trùng | CO-07 | |
| FR-FTB-TASKDEF-c1 | FR-FTB-TASKDEF | Task ghi đúng title, priority, SMS, purpose, status, metadata… | CO-01 | |

## 5. Quy tắc nghiệp vụ

| Req_ID | Điều kiện | Kết quả | Nguồn |
|---|---|---|---|
| BR-FTB-NO-SUPPRESSION | Rule không bật Cross-Type Suppression | suppression.is_enabled = false | FRD §4 |

## 6. Yêu cầu ngầm định

| Req_ID | Mô tả | Cơ sở | Trạng thái xác nhận |
|---|---|---|---|
| (không có) | | | |

## 9a. Ma trận tương tác

| IX_ID | Thực thể / trạng thái | A — yêu cầu thay đổi | B — yêu cầu phụ thuộc | Câu hỏi kiểm thử | Kết luận |
|---|---|---|---|---|---|
| IX-01 | store_stats[S].first_transaction_date | BR-FTB-FIRST-ORDER | BR-FTB-FIRST-ORDER | Mua đầu ở Store A rồi đầu ở Store B: mỗi Store 1 task | CO-04 |
| IX-02 | Active PIC của khách | BR-FTB-ASSIGNEE | BR-FTB-ORDER-VALID | Đổi PIC/huỷ đơn sau khi tạo: task giữ nguyên | CO-09 |

## 9b. Sự kiện kích hoạt & kênh

| EV_ID | Hành vi | Sự kiện kích hoạt / kênh | Kết luận |
|---|---|---|---|
| EV-01 | Sinh task | Event `POS_PURCHASE_COMPLETED` gửi lại (retry broker) | CO-07 |
| EV-02 | Thông báo cho assignee khi tạo task | Notification | Pending - Q-04 |
| EV-03 | Đơn 0 đồng | Event với đơn 0 đồng | Pending - Q-03 |

## 13. Câu hỏi làm rõ

| ID | Câu hỏi | Liên quan | Mức độ | Trả lời |
|---|---|---|---|---|
| Q-01 | Danh sách Store: §2.3 vẫn ghi "chỉ 1 trong 6 Store: HAN.PIA.01 hoặc HCM.PIA.02" trong khi §1/§5 liệt kê 6 Store (gồm Chaumet, Chopard, JLC). Xác nhận 6 Store đều sinh task? | BR-FTB-TRIGGER | Major | (chờ) |
| Q-02 | Ví dụ due_date trong FRD bị lỗi hiển thị ("187/10/2026"). Xác nhận 15/10/2026 14:30 → 17/10/2026 14:30 (48 giờ)? | BR-FTB-DUE | Major | (chờ) |
| Q-03 | Đơn 0 đồng có tính là giao dịch đầu tiên không (FRD nói theo logic sẵn có của ts_customers)? | BR-FTB-FIRST-ORDER | Minor | (chờ) |
| Q-04 | Nội dung/kênh Notification cho assignee ở Bước 6? | BR-FTB-ASSIGNEE | Minor | (chờ) |
| Q-05 | Tên khách làm title vượt 120 ký tự xử lý thế nào (OQ-FTB-12)? | FR-FTB-TASKDEF | Minor | (chờ) |

## 14. Giả định

| ID | Giả định | Câu hỏi liên quan | Case bị ảnh hưởng | Trạng thái xác nhận |
|---|---|---|---|---|
| AS-01 | Hạn là 48 giờ (bản sửa 2026-10-16), không phải 72 giờ | Q-02 | TC-FTB-002, TC-FTB-008 | Chưa xác nhận |
| AS-02 | Cả 6 Store trong conditions.store_ids đều sinh task | Q-01 | TC-FTB-005 | Chưa xác nhận |

## 15. Đánh giá rủi ro

| Khu vực | Khả năng (1–3) | Ảnh hưởng (1–3) | Điểm | Priority đề xuất |
|---|---|---|---|---|
| Sinh task đúng điều kiện đơn đầu | 3 | 3 | 9 | P1 |
| Assignee / fallback SM | 2 | 3 | 6 | P1–P2 |
| due_date | 2 | 3 | 6 | P1 |
| Idempotency | 2 | 3 | 6 | P1 |
| Quyền sửa, đơn huỷ/trả | 2 | 2 | 4 | P2 |

## 16. Điều kiện kiểm thử

| Cond_ID | Req_ID | Điều kiện kiểm thử | Kỹ thuật | Test case | Ghi chú |
|---|---|---|---|---|---|
| CO-01 | BR-FTB-FIRST-ORDER; BR-FTB-ASSIGNEE; FR-FTB-TASKDEF | Đơn đầu tại Store 58, có PIC → task đúng toàn bộ giá trị | UC | TC-FTB-001 | |
| CO-02 | BR-FTB-DUE; BR-FTB-TRIGGER | due_date = giờ đơn + 48 giờ (ví dụ 14:30) | DT | TC-FTB-002 | AS-01 |
| CO-03 | BR-FTB-FIRST-ORDER | Đã có first_transaction_date → không task | DT | TC-FTB-003 | |
| CO-04 | BR-FTB-FIRST-ORDER | Đơn đầu ở Store 2 sau khi đã có ở Store 1 → 1 task Store 2 | DT | TC-FTB-004 | IX-01 |
| CO-05 | BR-FTB-TRIGGER | Store ngoài danh sách → không task | EP | TC-FTB-006 | |
| CO-06 | BR-FTB-ASSIGNEE | Chưa có PIC → SM + needs_reassignment | DT | TC-FTB-007 | |
| CO-07 | FR-FTB-IDEMP | Event trùng source_id → 1 task | EG | TC-FTB-009 | |
| CO-08 | BR-FTB-DUE | Đơn 23:30 → due_date 23:30 sau 2 ngày | BVA | TC-FTB-008 | AS-01 |
| CO-09 | BR-FTB-ORDER-VALID | Đơn huỷ/trả sau khi tạo → task không đổi | ST | TC-FTB-010 | |
| CO-10 | BR-FTB-EDIT-SCOPE | CA không sửa được trường bị khoá | PERM | TC-FTB-011 | |
| CO-11 | BR-FTB-TRIGGER | Store khác trong danh sách (đại diện Store 202) sinh task | EP | TC-FTB-005 | AS-02 |

## 17. Dữ liệu test & setup

| Setup_ID | Dữ liệu / trạng thái | Cách tạo (điều khiển) | Cách xác minh (quan sát) | Cách reset | Nguồn dữ liệu | Trạng thái |
|---|---|---|---|---|---|---|
| SETUP-01 | Khách KH-A: store_stats[58].first_transaction_date = null, Active PIC tại Store 58 = CA Mai; store_stats[202] = null | Tạo khách mới trên môi trường test (hoặc DB) | Query ts_customers | Xoá khách và task test | Cần chuẩn bị | Cần chuẩn bị |
| SETUP-02 | Khả năng bắn event `POS_PURCHASE_COMPLETED` (payload: customer_id, store_id, source_id, timestamp) | Tạo đơn qua POS test hoặc publish event lên broker | Bảng ts_tasks / màn hình Task của CA | Xoá task + đơn test | Cần chuẩn bị | Cần chuẩn bị |
