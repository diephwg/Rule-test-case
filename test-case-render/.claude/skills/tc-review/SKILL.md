---
name: tc-review
description: Review bộ test case có sẵn (CSV, Excel, Markdown, export TestRail/Jira/Xray) — kiểm tra căn cứ của expected, độ bao phủ điều kiện kiểm thử so với tài liệu, áp dụng kỹ thuật ISTQB, trùng lặp, khả năng tái tạo, rồi đề xuất test case bổ sung. Dùng khi tester nói "review test case", "kiểm tra bộ test case", "tìm test case còn thiếu", "audit test suite".
---

# tc-review — Review & bổ sung bộ test case

Tiêu chuẩn đánh giá: `rules/03`, `rules/04`, `rules/05`. Kỹ thuật dùng để tìm lỗ hổng: `rules/02`.

## Đầu vào

- Bộ test case cần review (bắt buộc): `output/<FEATURE>/testcases.csv` hoặc file tester chỉ định (xlsx/csv/md — trích xuất bằng `scripts/extract_doc.py` nếu không phải CSV chuẩn).
- Tài liệu yêu cầu (khuyến nghị): `input/<FEATURE>/` hoặc link. Không có tài liệu → chỉ review định dạng/chất lượng viết, và ghi rõ **căn cứ & bao phủ: chưa đánh giá**.

## Các bước

1. **Chuẩn hoá:** bộ test không theo cột chuẩn → ánh xạ cột (ghi bảng ánh xạ trong báo cáo); không sửa file gốc.
2. **Phân tích:** chưa có `analysis.md` → chạy quy trình skill `tc-analyze` (gồm điều kiện kiểm thử `CO-xx`), rồi điền cột *Test case* theo bộ đang review.
3. **Validator** (cấu trúc & truy vết):
   `python3 scripts/validate_testcases.py <csv> --analysis output/<FEATURE>/analysis.md`
4. **Review nghiệp vụ** theo checklist `rules/05` §Review:
   - **Căn cứ:** expected trỏ về nguồn? Chuỗi trong ngoặc kép là nguyên văn? Case dựa trên giả định có được đánh dấu **theo từng assertion** — kể cả giả định ngầm (mặc định, thứ tự, thời điểm cập nhật, mockup cũ)? Tự tính lại mọi phép tính.
   - **Bao phủ — đọc lại nguồn trước, rồi mới đọc analysis** (tránh kế thừa điểm mù của người sinh):
     - Tự tách mệnh đề nguồn và đối chiếu với bảng *Mệnh đề nguồn*: thiếu mệnh đề, hoặc mệnh đề gộp hai khẳng định độc lập?
     - Ma trận tương tác: cặp yêu cầu nào dùng chung thực thể/trạng thái mà chưa có dòng `IX-xx`? Trường hợp tập thoả điều kiện thành rỗng / 1 phần tử?
     - Tập phần tử: phần tử ngoài tập chọn, phần tử duy nhất, ≥2 phần tử khác rule cùng lúc?
     - Ma trận trạng thái: thiếu trạng thái / sự kiện (kể cả sự kiện từ hệ thống, tác nhân khác)? Ô kết luận sai?
     - Sự kiện kích hoạt & kênh: tải lại, URL trực tiếp bước sau, kênh hiển thị thứ hai, Back, tab/phiên thứ hai, đăng nhập lại?
     - Điều kiện áp dụng nào chưa có case (phân vùng invalid, biên, rule DT khả thi, vai trò, luồng ngoại lệ)? Điều kiện / tổ hợp bị loại có lý do **chứng minh** được?
   - **Thực thi được:** dữ liệu/setup tái tạo được (có cách tạo trạng thái, cách xác minh, cách reset), trạng thái SETUP ghi đúng thực tế, case độc lập, expected xác minh được.
   - **Priority & nhãn:** khớp rủi ro và quy tắc `rules/03` §Scenario — không đánh giá theo tỷ lệ.
5. **Trùng lặp:** theo `rules/05` §Trùng lặp — ứng viên của validator phải được xét về ngữ nghĩa (mục tiêu, ngữ cảnh, phân vùng, kết quả) trước khi kết luận.

## Đầu ra

1. `output/<FEATURE>/review.md`:
   - Tóm tắt: tổng case, các chỉ số bao phủ (`rules/05` §Chỉ số, ghi mẫu số hoặc "chưa đánh giá"), mức sẵn sàng, số phát hiện theo mức `Critical / Major / Minor / Suggestion`
   - Bảng phát hiện: `ID | TC_ID / CO / Req_ID | Mức | Vấn đề | Căn cứ | Đề xuất sửa`
   - Điều kiện kiểm thử chưa được bao phủ; nhóm case trùng lặp (đã xét ngữ nghĩa)
   - Câu hỏi `Q-xx` phát sinh
2. `output/<FEATURE>/testcases-additional.csv`: case **đề xuất bổ sung**, đúng định dạng, ID tiếp nối **số lớn nhất theo lịch sử** của module, `Notes` ghi `[Đề xuất review]`. Chạy validator cho file này.
3. **Không tự sửa bộ test case gốc** trừ khi tester yêu cầu. Khi được yêu cầu: sửa trên `output/<FEATURE>/testcases.csv`, giữ ID, case bị loại → `Obsolete`, chạy validator với `--previous <bản gốc>` và export lại.

## Trả lời tester

Tóm tắt theo mức độ, top 5 vấn đề nghiêm trọng nhất (kèm căn cứ), số case đề xuất bổ sung, đường dẫn file.
