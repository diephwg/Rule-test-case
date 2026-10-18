# Test Case Render

Bỏ tài liệu yêu cầu vào → AI (Claude Code hoặc Codex) sinh bộ test case có truy vết (yêu cầu → điều kiện kiểm thử → case), kèm mức sẵn sàng, xuất ra CSV + Excel để tester chạy test.

Đây là **quy trình nội bộ vận dụng các kỹ thuật thiết kế test của ISTQB CTFL v4.0** — không phải chứng nhận tuân thủ ISO/IEC/IEEE 29119.

## Dùng nhanh

```bash
# 1. Tạo thư mục cho tính năng và bỏ tài liệu vào
mkdir -p input/ORDER-CHECKOUT
cp ~/Downloads/SRS_Checkout_v1.2.pdf ~/Downloads/mockup-*.png input/ORDER-CHECKOUT/

# 2. Mở agent tại thư mục này
claude      # hoặc: codex
```

Trong agent gõ:

| Việc cần làm | Claude Code | Codex |
|---|---|---|
| Sinh bộ test case đầy đủ | `/tc-generate ORDER-CHECKOUT` | `$tc-generate ORDER-CHECKOUT` |
| Chỉ phân tích yêu cầu + lập câu hỏi cho BA | `/tc-analyze ORDER-CHECKOUT` | `$tc-analyze ORDER-CHECKOUT` |
| Review bộ test case có sẵn | `/tc-review output/ORDER-CHECKOUT/testcases.csv` | `$tc-review output/ORDER-CHECKOUT/testcases.csv` |

Hoặc nói tự nhiên: *"Tạo test case cho tài liệu trong input/ORDER-CHECKOUT, tiếng Anh, chỉ module Thanh toán"* — agent tự chọn skill.

## Kết quả (`output/<FEATURE>/`)

| File | Nội dung |
|---|---|
| `analysis.md` | Danh mục nguồn, yêu cầu có nguồn, bảng EP/BVA, bảng quyết định, trạng thái, **điều kiện kiểm thử (CO-xx)**, dữ liệu & setup, **câu hỏi cho BA/PO**, giả định |
| `testcases.csv` | Bộ test case chuẩn (import được vào TestRail / Jira Xray / Zephyr / Google Sheets) |
| `testcases.xlsx` | Bản Excel: sheet *Test Cases* (cột **Design_Status** Ready / Needs Clarification, cột Actual_Result, Bug_ID, Tester, dropdown Status), *Summary* (tự cập nhật), *RTM* (yêu cầu → case), *Conditions* (điều kiện → case) |
| `report.md` | Mức sẵn sàng, 4 chỉ số bao phủ (có mẫu số), câu hỏi còn mở, giả định, rủi ro |
| `review.md` | (khi chạy tc-review) danh sách phát hiện + `testcases-additional.csv` |

Xem ví dụ hoàn chỉnh ở `examples/LOGIN/`.

## Bộ quy tắc

| File | Nội dung |
|---|---|
| `AGENTS.md` | Quy tắc cốt lõi — Codex tự đọc; Claude đọc qua `CLAUDE.md` |
| `rules/01-quy-trinh.md` | Quy trình 6 bước, mệnh đề nguồn, ma trận tương tác, sự kiện × kênh, cổng kiểm soát, phản biện độc lập, mức sẵn sàng (Ready / Needs Clarification / Blocked), cập nhật |
| `rules/02-ky-thuat-thiet-ke.md` | Chọn kỹ thuật theo mô hình & rủi ro: EP, BVA, Decision Table, State Transition, Use Case, Pairwise, CRUD, phân quyền, Error Guessing |
| `rules/03-dinh-dang-test-case.md` | Cột, nhãn Scenario, Priority theo rủi ro, đánh dấu phụ thuộc, dữ liệu & setup, tách/gộp, ID ổn định |
| `rules/04-checklist-bao-phu.md` | Gợi ý điều kiện kiểm thử theo loại thành phần: input, form, bảng, upload, phân quyền, API, bảo mật… |
| `rules/05-review-quality-gate.md` | Validator vs review nghiệp vụ, tiêu chí bàn giao, chỉ số bao phủ, anti-pattern, trùng lặp |

Muốn đổi chuẩn của team (thêm cột, đổi quy ước ID, đổi ngôn ngữ mặc định) → sửa trong `rules/` + `templates/`, và nếu đổi cột/giá trị thì sửa `REQUIRED_COLUMNS` / `ENUMS` trong `scripts/validate_testcases.py`.

## Script (chạy tay được)

```bash
uv run scripts/extract_doc.py input/<FEATURE> -o output/<FEATURE>/_extracted [--render-pages]
python3 scripts/validate_testcases.py output/<FEATURE>/testcases.csv --analysis output/<FEATURE>/analysis.md \
    [--sources <thư mục nguồn>] [--previous <testcases cũ>.csv]
uv run scripts/export_xlsx.py output/<FEATURE>/testcases.csv --analysis output/<FEATURE>/analysis.md
```

Yêu cầu: Python 3.9+, `uv` (tự cài `openpyxl`), `pdftotext` + `pdftoppm` (poppler-utils), `pandoc`, LibreOffice (cho .doc/.ppt/.pptx/.xls).

## Cấu trúc skill (dùng chung Claude + Codex)

```
.agents/skills/            ← nguồn thật (Codex đọc ở đây)
  tc-generate/SKILL.md
  tc-analyze/SKILL.md
  tc-review/SKILL.md
.claude/skills/            ← symlink tới .agents/skills (Claude đọc ở đây)
```

Thêm skill mới: tạo `.agents/skills/<ten>/SKILL.md`, rồi `ln -s ../../.agents/skills/<ten> .claude/skills/<ten>`.

## Tham khảo

Bộ quy tắc vận dụng [ISTQB CTFL Syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf) (§4.2 kỹ thuật thiết kế, §5.1.5 ưu tiên theo rủi ro), OWASP Testing Guide, WCAG 2.1 làm nguồn đối chiếu phương pháp, và tham khảo cách tổ chức của các bộ skill QA mã nguồn mở:
[saleem-daqa/qa-test-case-generation](https://github.com/saleem-daqa/qa-test-case-generation),
[trihn-2642/demo-qa-skills](https://github.com/trihn-2642/demo-qa-skills),
[sethdford/claude-skills — functional-testing](https://github.com/sethdford/claude-skills/tree/main/qa-engineer/functional-testing),
[softaworks/agent-toolkit — qa-test-planner](https://github.com/softaworks/agent-toolkit/blob/main/skills/qa-test-planner/README.md).
