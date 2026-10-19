# [First Time Buyer Reconnect] Không tạo task cho Store 202 (HCM.PIA.02) khi khách đã có đơn đầu tại Store 58 nhưng chưa có tại Store 202

- **Test case:** TC-FTB-004
- **Liên quan FRD:** §7 E2, AC-FTB-03, BR-FTB-FIRST-ORDER (xét riêng từng Store)
- **Môi trường / build:** [cần điền]
- **Severity / Priority:** [cần điền] (đề xuất High / P1: luồng cốt lõi của Rule)
- **Người báo / ngày:** [cần điền]

## Điều kiện ban đầu
1. Khách KH-A có `store_stats[58].first_transaction_date` đã có giá trị.
2. KH-A có `store_stats[202].first_transaction_date = null`.
3. KH-A có Active PIC tại Store 202: [cần điền].

## Các bước tái hiện
1. Phát sinh sự kiện `POS_PURCHASE_COMPLETED` cho đơn đầu của KH-A tại `store_id` 202.
2. Truy vấn `ts_tasks` của KH-A theo rule `RULE_FIRST_TIME_BUYER_RECONNECT_PIAGET`.
3. Đọc `store_stats[58]` của KH-A.

## Kết quả mong đợi
- Có thêm 1 task mới với `store.store_id` = 202 và assignee = Active PIC của KH-A tại Store 202.
- Task cũ (nếu có) của Store 58 và `store_stats[58]` không bị thay đổi.

## Kết quả thực tế
Không tạo task cho Store 202.

## Bằng chứng
[cần đính kèm: ảnh, log, kết quả query]
