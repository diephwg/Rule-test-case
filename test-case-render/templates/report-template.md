# Báo cáo bộ test case — <FEATURE>

| Thông tin | Giá trị |
|---|---|
| Nguồn | ... (xem Danh mục nguồn trong `analysis.md`) |
| Ngày tạo | YYYY-MM-DD |
| File | `testcases.csv`, `testcases.xlsx`, `analysis.md` |

## 1. Mức sẵn sàng

| Mức | Số lượng | Ghi chú |
|---|---|---|
| Ready | ... | Expected có căn cứ đã xác nhận |
| Needs Clarification | ... | Phụ thuộc Q mở / AS / IMP chưa xác nhận — expected tạm thời |
| Blocked | ... | Phụ thuộc SETUP *Chưa rõ cách làm* — chưa chạy được |
| SETUP chưa sẵn sàng | ... | SETUP-xx: cần ai cung cấp gì |
| Điều kiện Pending | ... | Chưa viết được case — chờ Q-xx |
| Nguồn chưa đọc được | ... | Phần bị ảnh hưởng: ... |

Kết luận ngắn: bộ test **sẵn sàng chạy ở mức nào** (vd. "25/39 case chạy và đánh giá được ngay; 10 case cần xác nhận expected sau khi BA trả lời Q-01, Q-04; 4 case Blocked chờ dev cung cấp SETUP-02"). Không ghi "chạy được toàn bộ" khi còn case Blocked.

## 2. Chỉ số bao phủ (dán từ output validator)

| # | Chỉ số | Giá trị | Mẫu số |
|---|---|---|---|
| 1 | Req_ID có case tham chiếu | x/y | Yêu cầu trừ N/A, bị từ chối |
| 2 | Mệnh đề nguồn có case · có case Ready | x/y · z/y | Mệnh đề trừ N/A, Pending |
| 3 | Điều kiện kiểm thử có case | x/y | CO-xx trừ N/A, Pending |
| 4 | Theo kỹ thuật · nguồn mở rộng | BVA x/y · DT x/y · ST x/y … · IX x/y · EV x/y | CO-xx theo kỹ thuật; dòng IX/EV có kết luận |
| 5 | Đang chờ | Pending: · Needs Clarification: · Blocked: · Q mở: · AS/IMP chưa xác nhận: · SETUP chưa rõ cách làm: | – |

Chỉ số chưa đo được ghi "chưa đánh giá". Chỉ số 1 không chứng minh mọi mệnh đề của yêu cầu đã được kiểm tra.

## 3. Thống kê (tham khảo, không phải chỉ tiêu)

| Chỉ số | Giá trị |
|---|---|
| Tổng số test case | ... |
| Theo Priority | P1: · P2: · P3: · P4: |
| Theo Scenario | Positive: · Negative: · Boundary: · Edge: |
| Theo Test_Type | ... |
| Ứng viên tự động hoá | ... |

## 4. Câu hỏi còn mở (cần BA/PO trả lời)

| ID | Câu hỏi | Mức độ | Case / điều kiện bị ảnh hưởng |
|---|---|---|---|
| Q-01 | ... | Blocker | TC-...-003, CO-07 |

## 5. Giả định & yêu cầu ngầm định đang dùng

| ID | Nội dung | Trạng thái | Case bị ảnh hưởng |
|---|---|---|---|
| AS-01 | ... | Chưa xác nhận | ... |
| IMP-01 | ... | Đề xuất | ... |

## 6. Review nghiệp vụ

- Đã review theo `rules/05` §Review: có / chưa
- Phát hiện còn mở: ...

## 6a. Phản biện độc lập

| Cách chạy | Subagent mới / lượt review riêng — ghi rõ |
|---|---|

| Phát hiện | Mức | Kết luận | Thay đổi |
|---|---|---|---|
| ... | Major | Đã sửa / Từ chối — lý do | TC-..., CO-... |

## 7. Cảnh báo validator chưa sửa & giải trình

| Cảnh báo | Lý do giữ nguyên |
|---|---|
| ... | ... |

## 8. Rủi ro & khuyến nghị

- ...

## 9. Thay đổi so với phiên bản trước (khi cập nhật)

| Loại | Test case | Lý do |
|---|---|---|
| Thêm / Sửa / Obsolete | ... | ... |
