@AGENTS.md

## Ghi chú riêng cho Claude Code

- Skill nằm ở `.claude/skills/` (symlink tới `.agents/skills/` — sửa skill thì sửa ở `.agents/skills/`, không sửa qua symlink rồi tạo file mới).
- Ảnh màn hình / mockup trong `input/`: dùng Read để xem trực tiếp ảnh; mô tả các trường, nút, trạng thái nhìn thấy vào `analysis.md` mục *Quan sát UI*.
- Link Jira / Confluence: dùng Atlassian MCP nếu đã kết nối (`getJiraIssue`, `getConfluenceContent`). Attachment Jira: lấy lệnh tải qua `discover` → `downloadJiraIssueAttachment`, lưu vào `output/<FEATURE>/_extracted/attachments/` rồi Read ảnh.
- Phản biện độc lập (`rules/01` Bước 5.3): dùng `Agent` với `subagent_type: general-purpose`, prompt chỉ gồm đường dẫn file + nhiệm vụ chạy `tc-review` (đọc nguồn trước, tìm điều kiện thiếu & phụ thuộc chưa đánh dấu), không kèm kết luận của agent sinh.
- Tài liệu lớn (> ~30 trang hoặc nhiều module): có thể dùng subagent phân tích song song từng module, nhưng **một agent duy nhất** ghép kết quả, đánh ID và chạy validate.
