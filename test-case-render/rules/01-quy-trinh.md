# 01 — Quy trình sinh test case (6 bước)

Quy trình vận dụng ISTQB Test Process: *Test Analysis → Test Design → Test Implementation*. Mỗi bước có **đầu ra** và **cổng kiểm soát (gate)**.

```
[1] Tiếp nhận nguồn → [2] Phân tích yêu cầu + tách mệnh đề → [3] Điều kiện kiểm thử (+ ma trận mở rộng)
      → [4] Thiết kế test case → [5] Validate + review nghiệp vụ + phản biện độc lập → [6] Xuất & báo cáo
```

Thuật ngữ dùng xuyên suốt:

| Ký hiệu | Nghĩa | Có phải tiêu chí nghiệm thu? |
|---|---|---|
| `Req_ID` (vd. `AC01`, `FR-02`, `REQ-LOGIN-01`), `BR-xx` | Yêu cầu / quy tắc nghiệp vụ **có nguồn** trong tài liệu | Có |
| `<Req_ID>-c<n>` (vd. `AC08-c3`) | **Mệnh đề nguồn** — một khẳng định kiểm tra được trong yêu cầu; đơn vị truy vết nhỏ nhất | Có (thuộc yêu cầu) |
| `IMP-xx` | Kỳ vọng **đề xuất** theo rủi ro/thông lệ, tài liệu không ghi | Chỉ khi trạng thái = *Đã xác nhận* |
| `Q-xx` | Câu hỏi làm rõ (mơ hồ, mâu thuẫn, thiếu) | – |
| `AS-xx` | Giả định **tạm thời** để tiếp tục khi `Q-xx` chưa có trả lời | Không — chỉ để thiết kế nháp |
| `CO-xx` | Điều kiện kiểm thử — "cái cần kiểm tra", đơn vị đo bao phủ | – |
| `IX-xx` | Cặp **tương tác** giữa hai yêu cầu cùng tác động lên một thực thể/trạng thái | – |
| `EV-xx` | Một tổ hợp **hành vi × sự kiện kích hoạt / kênh** | – |
| `SETUP-xx` | Quy trình chuẩn bị/reset dữ liệu & trạng thái dùng chung, có trạng thái sẵn sàng | – |

Truy vết: `Req_ID` → `Mệnh đề` → `CO-xx` → `TC`. `IX-xx`, `EV-xx` và các bảng kỹ thuật (DT, ST) là **nguồn sinh thêm** `CO-xx` ngoài các mệnh đề.

---

## Bước 1 — Tiếp nhận & lập danh mục nguồn

1. Xác định `<FEATURE>` (hỏi tester nếu không rõ; mặc định lấy tên thư mục trong `input/`).
2. Trích xuất sang text:
   `uv run scripts/extract_doc.py input/<FEATURE> -o output/<FEATURE>/_extracted`
3. Ảnh (mockup, screenshot, ảnh nhúng): **mở và xem trực tiếp**, không đoán qua tên file.
   PDF/PPTX có bảng, sơ đồ, hoặc text bị lỗi dấu tiếng Việt (vd. "bằ ng") → chạy lại với `--render-pages` và xem ảnh trang.
4. Nguồn từ xa (Jira, Confluence, Figma…): đọc qua connector/browser nếu có, **lưu nội dung đọc được** vào `output/<FEATURE>/_extracted/<nguồn>.md` (đây là bản đối chiếu nguyên văn cho validator). Attachment Jira: thử tải qua connector trước khi ghi *Chưa đọc được*.
5. Ghi **Danh mục nguồn** trong `analysis.md`: mỗi nguồn có phiên bản/ngày, trạng thái (*Đã đọc / Đọc một phần / Chưa đọc được*), và phần yêu cầu bị ảnh hưởng nếu chưa đọc được.
6. Có `output/<FEATURE>/testcases.csv` cũ → đây là **cập nhật** (xem cuối file). Sao lưu bản cũ để chạy `--previous`.

**Gate 1:** Mọi nguồn đều có trong danh mục với trạng thái rõ ràng. Nguồn không đọc được **chỉ chặn phần phụ thuộc vào nó** — phần độc lập tiếp tục; báo tester nguồn nào thiếu và ảnh hưởng gì.

---

## Bước 2 — Phân tích yêu cầu → `output/<FEATURE>/analysis.md`

Dùng mẫu `templates/analysis-template.md`. Nội dung chính: tóm tắt, phạm vi in/out, tác nhân & phân quyền, danh sách yêu cầu (có nguồn), **mệnh đề nguồn**, quy tắc nghiệp vụ, từ điển dữ liệu, trạng thái, tích hợp, yêu cầu ngầm định, câu hỏi, giả định, rủi ro.

**Quy ước Req_ID:** dùng lại ID trong tài liệu nếu có (`FR-01`, `US-12`, `AC01`). Nếu không có, tự đặt `REQ-<MODULE>-<NN>`. Mỗi ID ghi **nguồn** (file, mục, trang).

**Tách mệnh đề nguồn** (mục *Mệnh đề nguồn*): mỗi yêu cầu tách thành các mệnh đề kiểm tra được — mỗi gạch đầu dòng `Then`, mỗi dòng của bảng điều kiện, mỗi Business Rule, mỗi câu "phải / không được / khi … thì …". ID `<Req_ID>-c<n>` (tách thêm một mệnh đề đã có thì dùng hậu tố chữ: `AC08-c3a`, `AC08-c3b`), ghi nội dung rút gọn bám sát nguyên văn. Mệnh đề **không** được gộp hai khẳng định có thể đúng/sai độc lập. Đây là **mẫu số khách quan** của bao phủ — không phụ thuộc cách AI đặt `CO-xx`.

**Quan hệ giữa nguồn, IMP, Q, AS:**
- Yêu cầu từ tài liệu phải trỏ được tới nguồn. Không có nguồn → không phải yêu cầu, mà là `IMP` hoặc `Q`.
- `IMP-xx` ghi rõ **cơ sở** (thông lệ bảo mật, bug đã biết, ticket con…) và **trạng thái xác nhận**: *Đề xuất* (mặc định) / *Đã xác nhận* / *Bị từ chối*. Chỉ thêm IMP khi có rủi ro thực tế.
- `AS-xx` ghi rõ `Q-xx` liên quan, **các case chịu ảnh hưởng** (ghi đủ từng `TC_ID`, không viết tắt), và trạng thái: *Chưa xác nhận* (mặc định) / *Đã xác nhận* / *Sai — đã sửa case*.
- Thiếu thông điệp nguyên văn → mô tả ý nghĩa thông điệp **không dùng ngoặc kép** (vd. `hiển thị thông báo lỗi về độ dài mật khẩu (nội dung chờ Q-03)`), không tự đặt chuỗi rồi trình bày như trích từ tài liệu.

**Soi điểm mơ hồ:** từ ngữ không đo được ("nhanh", "hợp lệ", "v.v.", "có thể"), giới hạn thiếu, thông điệp không nêu nguyên văn, hành vi khi lỗi mạng/timeout, mâu thuẫn văn bản ↔ mockup, quyền hạn không rõ, đồng thời, huỷ giữa chừng, **khái niệm nghiệp vụ chưa định nghĩa** (vd. "hết hàng" xác định bằng gì, "thứ tự ban đầu" là thứ tự nào), **giá trị mặc định** (đã chọn sẵn hay chưa). Mỗi điểm → `Q-xx` đóng, cụ thể, có mức độ *Blocker / Major / Minor*.

**Gate 2:**
- Mọi yêu cầu (trừ N/A) có ≥1 mệnh đề nguồn.
- `Q-xx` mức *Blocker* (không xác định được hành vi mong đợi của một phần) → **dừng, trình bày câu hỏi cho tester**, hỏi: trả lời ngay hay tiếp tục phần đó với `AS-xx`.
- Không hỏi được (chạy không tương tác) → tiếp tục với giả định; các case liên quan sẽ ở trạng thái *Needs Clarification*.

---

## Bước 3 — Điều kiện kiểm thử (`analysis.md` mục *Điều kiện kiểm thử*)

Điều kiện được sinh từ **năm nguồn**, theo thứ tự. Bước 3.1 bảo đảm phủ tài liệu; các bước 3.2–3.5 tìm lỗi nằm **giữa** các yêu cầu, phần tử, trạng thái và kênh — nơi thường có lỗi nhất nhưng không có câu nào trong tài liệu mô tả trực tiếp.

1. **Từ mệnh đề nguồn:** mỗi mệnh đề → ≥1 `CO-xx` (ghi CO ở cột *CO* của bảng mệnh đề). Với mỗi mệnh đề xét thêm các điều kiện **có liên quan**: luồng được phép, hành vi bị chặn, dữ liệu không hợp lệ, giá trị biên, ngoại lệ, phân quyền, tích hợp (gợi ý ở `rules/04`). Chọn kỹ thuật theo cấu trúc yêu cầu và rủi ro (`rules/02`); mỗi **mục bao phủ** của kỹ thuật (phân vùng, biên, rule DT, chuyển trạng thái…) là một dòng `CO-xx`.
2. **Ma trận tương tác** (mục *Ma trận tương tác*): liệt kê các **thực thể/trạng thái dùng chung** (vd. trạng thái chọn, số lượng, tồn kho, trạng thái nút, tổng tiền, trạng thái tài khoản, bộ đếm). Với mỗi cặp yêu cầu mà một yêu cầu **thay đổi** thực thể và yêu cầu kia **phụ thuộc** vào thực thể đó → một dòng `IX-xx`: *khi yêu cầu A làm thay đổi X, yêu cầu B còn đúng không?* Kết luận mỗi dòng: `CO-xx` / `N/A - lý do` / `Pending - Q-xx`. Đặc biệt xét trường hợp thay đổi làm **tập thoả điều kiện của B trở thành rỗng hoặc chỉ còn một phần tử**.
3. **Tập phần tử:** yêu cầu áp dụng cho từng phần tử của một tập (dòng giỏ hàng, item, bản ghi được chọn) → lập bảng quyết định theo `rules/02` §DT mục *Tập phần tử* (phần tử ngoài tập chọn, phần tử duy nhất, ≥2 phần tử khác rule cùng lúc).
4. **Bảng trạng thái đầy đủ** (khi có hành vi phụ thuộc trạng thái): ma trận *Trạng thái × Sự kiện*, **mỗi ô** có kết luận (`rules/02` §ST). Ô có rủi ro → `CO-xx`; ô chưa biết → `Q-xx`.
5. **Sự kiện kích hoạt × kênh** (mục *Sự kiện kích hoạt & kênh*): với mỗi hành vi chính, liệt kê **khi nào** hệ thống áp dụng nó (vào trang, tải lại, bấm hành động, thay đổi nền/realtime, hết thời gian) và **ở đâu** dữ liệu đó được truy cập/hiển thị (màn hình chính, kênh hiển thị thứ hai như mini-cart/badge/email, URL trực tiếp, API, tab/phiên/thiết bị thứ hai, đăng nhập lại, nút Back). Mỗi tổ hợp → một dòng `EV-xx` với kết luận `CO-xx` / `N/A - lý do` / `Pending - Q-xx`. Danh sách tối thiểu ở `rules/04` §B *Sự kiện kích hoạt & kênh*.
6. Lập bảng phụ trợ khi kỹ thuật cần: phân vùng EP/BVA, bảng quyết định, ma trận phân quyền, ma trận CRUD, bảng pairwise.
7. **Dữ liệu test & setup** (`SETUP-xx`): tài khoản/vai trò, dữ liệu định danh, cấu hình, mốc thời gian, môi trường; **cách tạo trạng thái** (điều khiển: UI, admin, API, DB, cấu hình, giả lập thời gian, phiên thứ hai), **cách xác minh** khi kết quả không nhìn thấy trên UI (quan sát: API, DB, log, màn hình admin), **cách reset**, và **trạng thái**: *Sẵn sàng* (đã có hoặc đã có quy trình chạy được) / *Cần chuẩn bị* (biết cách, tester tự làm) / *Chưa rõ cách làm* (cần dev/QA lead cung cấp). Mỗi `CO-xx` cần trạng thái đặc biệt phải có cách tạo trạng thái đó qua một `SETUP-xx`.
8. Điều kiện **không áp dụng** → `N/A - <lý do>`. Điều kiện **chưa thiết kế được vì thiếu thông tin** → `Pending - Q-xx`.

**Gate 3:** Mọi mệnh đề có ≥1 `CO-xx` (hoặc N/A/Pending); mọi dòng `IX-xx`, `EV-xx` và mọi ô của ma trận trạng thái có kết luận; mọi `CO-xx` có kỹ thuật và trạng thái; mọi `SETUP-xx` có trạng thái.

---

## Bước 4 — Thiết kế test case → `output/<FEATURE>/testcases.csv`

- Định dạng theo `rules/03` (header lấy từ `templates/testcases-template.csv`). Ghi CSV bằng script dùng module `csv` của Python để tránh lỗi escape.
- Thứ tự viết gợi ý: luồng chính → luồng thay thế → hành vi bị chặn / dữ liệu không hợp lệ → biên → tương tác & tập phần tử → kênh / sự kiện → phân quyền → tích hợp → phi chức năng → UI.
- Sau khi viết, điền cột *Test case* của từng `CO-xx`.
- **Rà phụ thuộc theo từng assertion** (`rules/03` §Notes): với mỗi dòng Expected và mỗi Precondition, hỏi *"điều này có còn đúng với mọi câu trả lời của các `Q-xx` đang mở không?"*. Không → gắn `[Cần xác nhận Q-xx]` / `[Giả định AS-xx]` và thêm case vào cột *Case bị ảnh hưởng* của AS. Không ghi phụ thuộc bằng chữ tự do.

**Gate 4:** Mọi `CO-xx` không phải N/A/Pending có ≥1 case; mọi case gắn với ≥1 `CO-xx`; mọi phụ thuộc vào Q/AS có ID.

---

## Bước 5 — Validate + review nghiệp vụ + phản biện độc lập

1. Chạy validator (kiểm tra **cấu trúc & truy vết**):
   `python3 scripts/validate_testcases.py output/<FEATURE>/testcases.csv --analysis output/<FEATURE>/analysis.md`
   Sửa đến **0 ERROR**. Mỗi WARNING là ứng viên cần review: sửa nếu đúng là vấn đề, ngược lại ghi giải trình vào `report.md`. **Không đổi nội dung chỉ để hết cảnh báo.**
2. **Tự review nghiệp vụ** theo checklist `rules/05` — phần validator không kiểm tra được: expected có nguồn và đúng, phép tính đúng, kỹ thuật áp dụng đủ, dữ liệu/setup tái tạo được, case độc lập, kết quả quan sát được.
3. **Phản biện độc lập:** người review **không chung ngữ cảnh** với người sinh chạy quy trình skill `tc-review` trên tài liệu nguồn + `analysis.md` + `testcases.csv`, với nhiệm vụ chính: tìm **điều kiện còn thiếu** (mệnh đề, tương tác, tập phần tử, ô trạng thái, sự kiện × kênh) và **phụ thuộc chưa được đánh dấu**.
   - Có subagent (Claude Code `Agent`, Codex sub-agent) → dùng một subagent **mới**, chỉ truyền đường dẫn file, không truyền kết luận của người sinh.
   - Không có subagent → chạy `tc-review` trong một lượt riêng, bắt đầu bằng việc **đọc lại nguồn** trước khi đọc `analysis.md`.
   - Người sinh xử lý từng phát hiện: *Đã sửa* / *Từ chối — lý do*. Ghi vào `report.md` mục *Phản biện độc lập*. Sửa xong chạy lại validator.

**Gate 5:** 0 ERROR; mọi WARNING đã xử lý hoặc giải trình; đã tự review; mọi phát hiện của phản biện độc lập đã có kết luận.

---

## Bước 6 — Xuất & báo cáo

1. `uv run scripts/export_xlsx.py output/<FEATURE>/testcases.csv --analysis output/<FEATURE>/analysis.md`
2. Viết `output/<FEATURE>/report.md` theo `templates/report-template.md`, gồm các chỉ số **tách biệt** (`rules/05` §Chỉ số bao phủ), **mức sẵn sàng**, SETUP chưa sẵn sàng và kết quả phản biện độc lập.
3. Trả lời tester ngắn gọn: số case theo mức sẵn sàng, đường dẫn file, danh sách `Q-xx` cần BA/PO trả lời, SETUP cần dev/QA lead cung cấp, nguồn chưa đọc được.

### Mức sẵn sàng (Design_Status) — tách biệt với `Status` lần chạy

| Mức | Nghĩa | Cách xác định |
|---|---|---|
| **Ready** | Expected có căn cứ đã xác nhận **và** chạy được ngay | Không phụ thuộc `Q` mở, `AS` hay `IMP` chưa xác nhận; mọi `SETUP-xx` tham chiếu ≠ *Chưa rõ cách làm* |
| **Needs Clarification** | Chạy được nhưng expected là **tạm thời** | Tham chiếu `Q-xx` mở / `AS-xx` / `IMP-xx` chưa xác nhận |
| **Blocked** | Expected có thể đúng nhưng **chưa chạy được** | Tham chiếu `SETUP-xx` ở trạng thái *Chưa rõ cách làm*. Ưu tiên hơn Needs Clarification khi cả hai cùng có |
| **Pending** (ở mức điều kiện) | Chưa viết được case | `CO-xx` ghi `Pending - Q-xx` |

Validator tự tính Design_Status; Excel hiển thị cột `Design_Status`. `Status` (`Not Run / Pass / Fail / Blocked / Skipped / Obsolete`) là kết quả **thực thi**, không dùng để biểu thị mức sẵn sàng thiết kế. Chỉ tuyên bố bộ test "sẵn sàng / chạy được" ở mức tương ứng với bằng chứng đã có.

---

## Cập nhật khi tài liệu / câu trả lời thay đổi

1. Sao lưu `testcases.csv` cũ (vd. `testcases.v1.csv`).
2. So sánh nguồn mới với `analysis.md` → liệt kê yêu cầu và mệnh đề *Thêm / Sửa / Xoá*; cập nhật trạng thái `Q`, `AS`, `IMP`, `SETUP`.
3. Yêu cầu bị xoá / IMP bị từ chối → case liên quan `Status = Obsolete`, `Notes` ghi lý do + phiên bản.
4. Yêu cầu bị sửa / Q được trả lời → cập nhật case, **giữ ID**, bỏ đánh dấu chờ, `Notes` ghi `Updated vX.Y`.
5. Yêu cầu mới → case mới với **số tiếp theo theo lịch sử ID của module** (không lấp khoảng trống, không tái sử dụng ID Obsolete). ID đã dùng trong `testcases-additional.csv` của review cũng tính là lịch sử.
6. Chạy validator với `--previous testcases.v1.csv`.
7. `report.md` có mục *Thay đổi so với phiên bản trước*.
