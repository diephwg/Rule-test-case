---
name: tc-analyze
description: Phân tích tài liệu yêu cầu trước khi viết test case — lập danh mục nguồn, trích Req_ID có nguồn, quy tắc nghiệp vụ, từ điển dữ liệu, trạng thái, phân quyền, tìm điểm mơ hồ/mâu thuẫn, lập câu hỏi cho BA/PO và điều kiện kiểm thử (requirement analysis, testability review, clarification questions). Dùng khi tester muốn "phân tích yêu cầu", "review spec", "tìm câu hỏi cho BA", hoặc là bước 2–3 của tc-generate.
---

# tc-analyze — Phân tích yêu cầu & điều kiện kiểm thử

Đầu ra duy nhất: `output/<FEATURE>/analysis.md` theo `templates/analysis-template.md` (giữ nguyên tên các mục — validator đọc theo tên mục). Tuân thủ `rules/01` Bước 1–3 và `rules/02`.

## Các bước

1. **Nguồn:** trích xuất nếu chưa có `output/<FEATURE>/_extracted/`:
   `uv run scripts/extract_doc.py input/<FEATURE> -o output/<FEATURE>/_extracted`
   Nguồn từ xa → lưu nội dung đã đọc vào `_extracted/`. Xem trực tiếp mọi ảnh. Điền **Danh mục nguồn** (trạng thái đọc, phần bị ảnh hưởng).

2. **Đọc lần 1 — tổng quan:** mục tiêu, tác nhân, phạm vi, màn hình/API.

3. **Đọc lần 2 — chi tiết:**
   - **Yêu cầu:** mỗi yêu cầu có nguồn → 1 dòng Req_ID (dùng lại ID gốc nếu có). Ghi **nguồn** (file, mục, trang).
   - **Mệnh đề nguồn:** tách mỗi yêu cầu thành các khẳng định kiểm tra được (`<Req_ID>-c<n>`): mỗi gạch đầu dòng `Then`, mỗi dòng bảng điều kiện, mỗi Business Rule, mỗi câu "phải / không được / khi … thì …". Không gộp hai khẳng định độc lập.
   - **Quy tắc nghiệp vụ** `BR-xx`; **từ điển dữ liệu** với thông điệp **nguyên văn kèm nguồn** — không có thì `? (Q-xx)`.
   - **Bảng EP/BVA** (biên, đơn vị bước, mức coverage), **trạng thái** (có nguồn cho từng chuyển đổi) + **ma trận trạng thái** không để ô trống, **Decision Table** (ghi tổ hợp không khả thi; tổ hợp khả thi bị loại phải chứng minh hành vi không đổi) + bảng **tập phần tử** khi điều kiện áp dụng cho từng phần tử, **phân quyền**.
   - **Yêu cầu ngầm định** `IMP-xx`: chỉ khi có rủi ro thực tế; ghi **cơ sở** và trạng thái *Đề xuất*.

4. **Điểm mơ hồ** (danh sách soi trong `rules/01` Bước 2) → `Q-xx`:
   - Câu hỏi đóng, cụ thể, có gợi ý phương án: ✅ "Tên đăng nhập tối đa bao nhiêu ký tự? (20 hay 50?)" — ❌ "Tên đăng nhập có giới hạn gì?"
   - Mức độ: **Blocker** / **Major** / **Minor**; Req_ID liên quan.
   - Cần tiếp tục → `AS-xx` với Q liên quan, case bị ảnh hưởng (điền sau), trạng thái *Chưa xác nhận*.

5. **Đánh giá rủi ro** (Khả năng × Ảnh hưởng) → cơ sở cho Priority.

6. **Điều kiện kiểm thử** `CO-xx` (`rules/01` Bước 3): mỗi mệnh đề → ≥1 CO (luồng được phép, bị chặn, không hợp lệ, biên, ngoại lệ…); mỗi mục bao phủ của kỹ thuật là một dòng. Sau đó lập **Ma trận tương tác** (`IX-xx`) và **Sự kiện kích hoạt & kênh** (`EV-xx`) — mỗi dòng kết luận CO / N/A / Pending. `N/A - lý do` / `Pending - Q-xx` khi cần. Cột *Test case* để trống nếu chỉ phân tích.

7. **Dữ liệu test & setup** `SETUP-xx`: dữ liệu cần chuẩn bị, cách tạo trạng thái, cách xác minh, cách reset, **Trạng thái** (`Sẵn sàng / Cần chuẩn bị / Chưa rõ cách làm`).

## Tự kiểm tra trước khi kết thúc

- Mọi đoạn có nội dung yêu cầu trong nguồn đã ánh xạ tới ≥1 Req_ID và mệnh đề? Mọi Req_ID có nguồn?
- Mọi mệnh đề, dòng IX/EV, ô ma trận trạng thái đã có kết luận?
- Không có giá trị hay thông điệp tự chế mà không đánh dấu `Q`/`AS`/`IMP`?
- Mọi yêu cầu (trừ N/A) có ≥1 `CO-xx`?
- Nếu đã có `testcases.csv`: chạy `python3 scripts/validate_testcases.py output/<FEATURE>/testcases.csv --analysis output/<FEATURE>/analysis.md`.

## Trả lời tester

Tóm tắt: số yêu cầu / mệnh đề / BR / IMP / điều kiện kiểm thử (tách theo nguồn: mệnh đề, IX, EV, ST, DT), nguồn chưa đọc được, SETUP chưa rõ cách làm, rủi ro chính, và **bảng câu hỏi `Q-xx`** (Blocker trước) để chuyển cho BA/PO.
