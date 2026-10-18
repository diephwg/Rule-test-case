# Review bộ rules sinh test case — gửi Claude

## 1. Mục tiêu và phạm vi

Review chính bộ quy tắc dùng để hướng dẫn AI sinh test case trong repo `test-case-render`.

Tài liệu được đánh giá:

- `AGENTS.md` và hướng dẫn tương ứng cho Claude.
- `rules/01-quy-trinh.md`.
- `rules/02-ky-thuat-thiet-ke.md`.
- `rules/03-dinh-dang-test-case.md`.
- `rules/04-checklist-bao-phu.md`.
- `rules/05-review-quality-gate.md`.

Phạm vi nhận xét là tính đúng đắn, nhất quán, khả năng áp dụng và khả năng kiểm soát chất lượng của rules. Không sử dụng chất lượng một bộ test case cụ thể để kết luận thay cho việc đánh giá rules.

## 2. Đánh giá chung

Bộ rules có nền tảng tốt và có thể dùng làm quy trình nội bộ: phân tích trước khi thiết kế, truy vết yêu cầu, chọn kỹ thuật kiểm thử, ghi nhận câu hỏi/giả định, giữ ID khi cập nhật và review trước khi bàn giao.

Cần cải thiện một số quy định quá cứng, làm rõ cách xử lý yêu cầu chưa được xác nhận và phân biệt kiểm tra định dạng với đánh giá chất lượng nghiệp vụ. Ưu tiên sửa tính nhất quán trước khi bổ sung thêm checklist.

Nên mô tả đây là **quy trình nội bộ vận dụng các kỹ thuật ISTQB**. Các quy ước về số cột, tiền tố Title và tỷ lệ Priority là lựa chọn nội bộ. Chưa có cơ sở để tuyên bố tuân thủ đầy đủ ISO/IEC/IEEE 29119 nếu chưa xác định phiên bản, phạm vi và ánh xạ các yêu cầu của tiêu chuẩn.

## 3. Các điểm cần cải thiện

### R-01 — Không bắt buộc mọi Req_ID có cả Positive và Negative

**Vị trí:** AGENTS mục quy tắc cốt lõi; `rules/01` Gate 4; `rules/05` Definition of Done.

**Vấn đề:** Không phải mọi yêu cầu đều có đầu vào hợp lệ/không hợp lệ độc lập. Yêu cầu UI tĩnh, yêu cầu mô tả hành vi từ chối hoặc một quy tắc chỉ áp dụng trong một trạng thái có thể không phù hợp với việc ép hai loại Scenario. Ngoại lệ chỉ mang tên `Positive-only` cũng không bao quát mọi trường hợp.

**Đề xuất câu thay thế:**

> Với mỗi yêu cầu, xác định các điều kiện kiểm thử có liên quan: luồng được phép, hành vi bị chặn, dữ liệu không hợp lệ, giá trị biên và ngoại lệ. Bao phủ các điều kiện áp dụng; trường hợp không áp dụng phải có lý do. Không tạo thêm test case hoặc đổi nhãn Scenario chỉ để đủ Positive/Negative.

Nên xác định rõ Positive/Negative nói về loại tình huống đầu vào; Boundary/Edge nói về đặc điểm dữ liệu/tình huống. Một case kiểm tra biên có thể đồng thời là Positive hoặc Negative. Nếu giữ một cột Scenario, phải nêu cách chọn nhãn và không dùng riêng nhãn này để chứng minh đầy đủ coverage.

### R-02 — Làm rõ quan hệ giữa “không bịa đặt”, IMP và AS

**Vị trí:** AGENTS; `rules/01` phần yêu cầu ngầm định, câu hỏi và giả định; `rules/04` phần hành vi chưa có trong tài liệu.

**Vấn đề:** IMP và AS giúp tiếp tục công việc khi tài liệu thiếu, nhưng có thể bị diễn giải thành quyền tự đặt hành vi sản phẩm. Ghi một ID IMP/AS chưa đủ để biến expected thành tiêu chí nghiệm thu đã được chấp thuận.

**Đề xuất:**

- Yêu cầu từ tài liệu phải có nguồn xác định được.
- IMP là kỳ vọng đề xuất theo rủi ro/thông lệ; ghi rõ cơ sở và trạng thái xác nhận.
- AS là giả định tạm thời; ghi rõ Q liên quan, các case chịu ảnh hưởng và trạng thái xác nhận.
- Expected dựa trên IMP/AS chưa xác nhận phải được nhận diện là tạm thời.
- Khi thiếu thông điệp nguyên văn, ghi điều đã biết và điều còn chờ xác nhận; không tự tạo chuỗi lỗi rồi trình bày như trích từ tài liệu.

### R-03 — Dùng kỹ thuật thiết kế theo mô hình và rủi ro

**Vị trí:** AGENTS; `rules/02`; `rules/05` phần bao phủ kỹ thuật.

**Vấn đề:** Các dấu hiệu như “≥2 điều kiện → DT”, “có trạng thái → ST” phù hợp để gợi ý, nhưng có thể tạo bảng hình thức nếu áp dụng bắt buộc mà không xét cách các điều kiện tác động tới kết quả.

**Đề xuất:**

> Chọn kỹ thuật theo cấu trúc yêu cầu và rủi ro. Mỗi kỹ thuật được chọn phải chỉ ra các đối tượng cần bao phủ và cách test case kiểm tra chúng. Khi kỹ thuật không phù hợp hoặc không bổ sung giá trị kiểm thử, ghi lý do.

Làm rõ thêm:

- EP: phân vùng dựa trên cách hệ thống xử lý, không chỉ dựa trên hình thức dữ liệu.
- BVA: dùng cho phân vùng có thứ tự; ghi biên, đơn vị bước và mức coverage được chọn. Miền chưa biết phải được ghi nhận là chưa xác nhận.
- DT: xét các tổ hợp khả thi, điều kiện phụ thuộc và điều kiện có thể đồng thời đúng. Một rule có thể cần nhiều case cho các dữ liệu/rủi ro khác nhau; không bắt chính xác một case mỗi rule.
- ST: mô hình hóa sự kiện, guard, hành động và chuyển đổi có căn cứ. Không mặc định mọi trạng thái được gọi là “kết thúc” đều không thể chuyển tiếp nếu nghiệp vụ cho phép mở lại.
- Pairwise: phải xác định tham số, giá trị và ràng buộc; không dùng để thay thế các tổ hợp nghiệp vụ rủi ro cao đã biết.

### R-04 — Thu hẹp quy tắc chống trùng lặp

**Vị trí:** `rules/03` phần tách/gộp; `rules/05` phần chống trùng lặp.

**Vấn đề:** Quy định “giá trị khác nhau nhưng cùng phân vùng → trùng” dễ làm mất case cần thiết khi khác vai trò, trạng thái, kênh thao tác hoặc tương tác nghiệp vụ.

**Đề xuất câu thay thế:**

> Chỉ coi hai test case là trùng khi chúng kiểm tra cùng mục tiêu, cùng ngữ cảnh nghiệp vụ, cùng phân vùng/biên liên quan và cùng kết quả kỳ vọng. Chỉ gộp khi việc gộp không làm mất coverage hoặc khả năng phát hiện lỗi riêng.

So khớp nội dung tự động chỉ nên tạo ứng viên cần review, không tự quyết định trùng về ngữ nghĩa.

### R-05 — Làm rõ “một mục tiêu” và cách gộp UI

**Vị trí:** AGENTS; `rules/03`; `rules/04` phần UI tĩnh; `rules/05` anti-pattern.

**Vấn đề:** Một mục tiêu có thể cần nhiều assertion. Ngược lại, gom toàn bộ nhãn, bố cục, placeholder và thông báo của một màn hình vào một case có thể tạo nhiều mục tiêu độc lập.

**Đề xuất:**

> Một test case kiểm tra một mục tiêu nghiệp vụ hoặc một điều kiện kiểm thử xác định. Cho phép nhiều assertion cùng chứng minh mục tiêu đó. Tách khi các mục tiêu có thể thành công/thất bại độc lập và việc gộp làm khó xác định kết quả, chạy lại hoặc báo lỗi.

Không áp quota cố định “1–2 case UI mỗi màn hình”. Gộp theo thành phần và mục tiêu quan sát được.

### R-06 — Priority dựa trên rủi ro, không dựa trên tỷ lệ mục tiêu

**Vị trí:** `rules/03` phần Priority; `rules/05` phần review độ ưu tiên.

**Vấn đề:** Dù đang được gọi là tham khảo, tỷ lệ P1/P2/P3/P4 có thể khiến AI chỉnh mức ưu tiên để đạt phân bổ thay vì phản ánh rủi ro thực tế.

**Đề xuất:**

> Priority được quyết định từ ảnh hưởng, khả năng xảy ra và mức quan trọng của luồng nghiệp vụ. Phân bổ Priority chỉ là thống kê hỗ trợ review. Không tăng/hạ Priority hoặc thêm case để đạt một tỷ lệ định trước.

Tương tự, không dùng tỷ lệ Positive/Negative để kết luận suite đầy đủ.

### R-07 — Xác định rõ xử lý khi nguồn thiếu và expected chưa xác nhận

**Vị trí:** `rules/01` Gate 1, Gate 2 và bước bàn giao; `rules/05` Definition of Done.

**Vấn đề:** Rule vừa yêu cầu đọc đủ tài liệu trước khi đi tiếp, vừa cho phép giả định khi thiếu thông tin. Chưa có tiêu chí rõ để phân biệt bản nháp có ích với bộ test đã đủ điều kiện thực thi và đánh giá pass/fail.

**Đề xuất:**

- Có danh mục nguồn: tài liệu/phiên bản, đã đọc hay chưa, phần bị ảnh hưởng.
- Thiếu nguồn chỉ chặn các phần phụ thuộc; phần độc lập có thể tiếp tục.
- Nếu thiếu thông tin khiến không xác định được hành vi mong đợi, ghi rõ điều kiện đang pending.
- Phân biệt trạng thái thiết kế như `Draft / Needs Clarification / Ready` với `Status` của lần chạy như `Not Run / Pass / Fail`.
- Chỉ xác nhận mức hoàn thiện phù hợp với bằng chứng đã có.

Không cần bắt buộc thêm cột ngay: có thể quản lý trạng thái thiết kế trong bảng phụ nếu muốn giữ schema hiện tại.

### R-08 — Phân biệt validator pass với chất lượng nghiệp vụ

**Vị trí:** AGENTS; `rules/01` Gate 5; `rules/05` Definition of Done.

**Vấn đề:** “0 ERROR” là điều kiện cần nhưng không chứng minh expected đúng, dữ liệu tái tạo được hoặc kỹ thuật đã áp dụng đầy đủ. Tỷ lệ Req_ID có TC cũng không chứng minh mọi mệnh đề trong yêu cầu đã được kiểm tra.

**Đề xuất câu bổ sung:**

> Validator xác nhận các điều kiện cấu trúc mà công cụ kiểm tra được. Chất lượng nghiệp vụ phải được review riêng: nguồn của expected, điều kiện kiểm thử, coverage kỹ thuật, tính độc lập, dữ liệu setup và khả năng quan sát kết quả.

Báo cáo nên phân biệt:

1. Tỷ lệ Req_ID có case tham chiếu.
2. Tỷ lệ điều kiện kiểm thử có case/assertion.
3. Coverage các phân vùng, biên, decision rule và transition đã chọn.
4. Phần pending vì thiếu nguồn hoặc expected chưa xác nhận.

Chỉ công bố phần trăm khi đã xác định rõ mẫu số và cách tính. Trường hợp chưa đo được phải ghi “chưa đánh giá”.

### R-09 — ID ổn định thay cho yêu cầu liên tục tuyệt đối

**Vị trí:** AGENTS; `rules/01` phần cập nhật; `rules/05` checklist bảo trì.

**Vấn đề:** “ID liên tục” có thể mâu thuẫn với không đánh số lại khi có khoảng trống lịch sử hoặc case Obsolete.

**Đề xuất câu thay thế:**

> TC_ID phải duy nhất và ổn định. Case mới dùng số tiếp theo của module theo lịch sử ID; không tái sử dụng ID và không lấp khoảng trống bằng cách đánh số lại. Case bị loại giữ ID và ghi trạng thái/lý do theo quy định cập nhật.

### R-10 — Cụ thể hóa yêu cầu “tester mới chạy được ngay”

**Vị trí:** AGENTS; `rules/03` phần Preconditions, Test_Data, Steps; `rules/05` phần thực thi được.

**Vấn đề:** Yêu cầu hiện tại đúng hướng nhưng chưa đủ cụ thể để review nhất quán.

**Đề xuất:**

> Mỗi case phải mô tả dữ liệu và trạng thái ban đầu có thể tái tạo, hoặc tham chiếu một procedure setup có nội dung xác định. Nêu cách chuẩn bị/reset dữ liệu khi case làm thay đổi trạng thái dùng chung. Không phụ thuộc vào việc chạy case trước.

Tùy tính năng, cần có tài khoản/vai trò, dữ liệu định danh, cấu hình nghiệp vụ, mốc thời gian, điều kiện môi trường và phương pháp xác minh expected.

Cho phép dùng dữ liệu minh họa do tester chuẩn bị, nhưng phải phân biệt với dữ liệu được xác nhận đang tồn tại trên môi trường. Nhãn UI và quy tắc nghiệp vụ vẫn phải có căn cứ từ nguồn.

## 4. Thứ tự cải thiện đề xuất

1. **R-01, R-02, R-07, R-08:** sửa định nghĩa coverage, giả định và mức sẵn sàng bàn giao.
2. **R-03, R-04, R-05:** chỉnh cách áp dụng kỹ thuật và tách/gộp case.
3. **R-06, R-09, R-10:** hoàn thiện Priority, ID và khả năng thực thi.

Khi áp dụng thay đổi, đối chiếu các nội dung tương ứng trong AGENTS/CLAUDE, skill, template và ví dụ để tránh nhiều cách diễn giải. `rules/` tiếp tục là nguồn chuẩn duy nhất; các bản tóm tắt chỉ dẫn tới quy định gốc.

## 5. Tiêu chí chấp nhận cho bản rules được cải thiện

- Không có quy định buộc tạo case hình thức chỉ để đủ nhãn hoặc tỷ lệ.
- Phân biệt rõ yêu cầu từ nguồn, đề xuất ngầm định và giả định chưa xác nhận.
- Mỗi tuyên bố coverage có đối tượng đo và cơ sở đối chiếu.
- Các quy định tách/gộp giữ được mục tiêu và coverage cần thiết.
- Gate xử lý rõ nguồn thiếu, expected pending và mức sẵn sàng của bộ test.
- Không có mâu thuẫn về ID, trạng thái và điều kiện bàn giao giữa các file.
- Có tiêu chí đủ cụ thể để đánh giá dữ liệu setup và tính độc lập của test case.

## 6. Nguồn tham chiếu

ISTQB CTFL v4.0.1: §4.2 về các kỹ thuật thiết kế; §5.1.5 về ưu tiên test case theo rủi ro, coverage và yêu cầu. Đây là nguồn đối chiếu phương pháp, không phải chứng nhận cho repo. [ISTQB CTFL Syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf).
