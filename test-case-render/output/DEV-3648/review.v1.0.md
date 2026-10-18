# Review bộ rule qua kết quả Claude sinh cho DEV-3648

Ngày review: 2026-10-16. Phạm vi: đánh giá bộ rule và khả năng kiểm soát chất lượng đầu ra; dùng DEV-3648 làm ví dụ thực tế.

## 1. Kết luận

Bộ rule có nền tảng tốt: phân tích trước khi thiết kế, truy vết yêu cầu, chọn kỹ thuật, ghi nhận Q/AS, giữ ID khi cập nhật và xuất bộ tài liệu thống nhất. Có thể dùng làm quy trình nội bộ để tạo bản nháp có cấu trúc.

Các gate hiện chưa đủ để kết luận đầu ra đầy đủ hoặc tester mới chạy được ngay. Cần ưu tiên kiểm soát bằng chứng nguồn, expected chưa được xác nhận, coverage theo điều kiện và khả năng chuẩn bị dữ liệu. Validator hiện kiểm tra được nhiều lỗi cấu trúc nhưng chưa chứng minh được chất lượng nghiệp vụ.

Không kết luận repo tuân thủ đầy đủ ISO/IEC/IEEE 29119: repo chưa có ánh xạ điều khoản/phiên bản tiêu chuẩn và review này không thực hiện đánh giá tuân thủ tiêu chuẩn đó. Các quy ước 15 cột, tiền tố Title, tỷ lệ Priority là quy ước nội bộ, cần ghi rõ như vậy.

## 2. Tài liệu và kiểm tra đã thực hiện

- Đọc `AGENTS.md`, 5 file `rules/`, 3 skill tc, template, validator, exporter và ví dụ LOGIN.
- Đọc toàn bộ 39 dòng test case DEV-3648, `analysis.md`, `report.md` và bản chép nguồn `_extracted/jira-DEV-3648.md`.
- Đối chiếu dữ liệu XML trong XLSX: sheet `Test Cases` có 39 TC; 15 cột gốc khớp CSV ở mọi dòng. Workbook có `Test Cases`, `Summary`, `RTM`. Đây là đối chiếu nội dung, chưa phải kiểm tra hiển thị workbook.
- Chạy validator trên DEV-3648: **39 TC, 18/18 ID được ánh xạ, 0 ERROR, 0 WARNING**.
- Chạy validator trên ví dụ LOGIN: **17 TC, 7/7 ID được ánh xạ, 0 ERROR, 0 WARNING**.
- Kiểm tra 6 biến thể có chủ đích trên bản sao trong `/tmp/dev3648-rule-review/`, dùng cả `--strict`. Không thay đổi bộ gốc.

Giới hạn nguồn: bản chép Jira có nội dung AC01–AC10 và tiêu đề child/bug, nhưng không có nội dung chi tiết các child/bug; ảnh gốc không có trong repo, ảnh ngày 23/09 được ghi là chưa mở được. Truy cập Jira trực tiếp trong lần review này không lấy được nội dung. Các nhận xét nghiệp vụ dưới đây dựa trên bản chép đã lưu, không khẳng định đó là phiên bản Jira mới nhất.

## 3. Tổng hợp phát hiện

| Mức | Số lượng |
|---|---:|
| Critical | 0 |
| Major | 8 |
| Minor | 3 |
| Suggestion | 1 |

Không ghi Critical vì chưa xác nhận được expected sai chắc chắn so với nguồn đầy đủ. Các lỗ hổng AC08 vẫn cần ưu tiên xử lý do liên quan luồng checkout.

| ID | TC_ID / Req_ID / file | Mức | Vấn đề | Đề xuất sửa |
|---|---|---|---|---|
| R-01 | `report.md` §2; validator dòng 176–194; skill tc-generate phần trả lời | Major | 18/18 chỉ chứng minh mỗi ID có TC tham chiếu. Không đo từng mệnh đề AC, rule khả thi, trạng thái, biên hay expected đã xác nhận. BR được suy ra từ AC và IMP cũng nằm trong cùng mẫu số. | Đổi tên thành “tỷ lệ ID có TC”. Báo riêng coverage điều kiện, kỹ thuật, nguồn và mức sẵn sàng. Chỉ gọi đầy đủ khi có danh mục đối chiếu. |
| R-02 | `rules/01` Gate 4; validator dòng 185–188 | Major | Rule yêu cầu Positive + Negative/Boundary, nhưng code chỉ cảnh báo khi tập Scenario đúng bằng `{Positive}`. Negative-only, Edge-only, Boundary-only hoặc Positive+Edge đều lọt. IMP-03 chỉ Negative; IMP-04/05 chỉ Edge; AC10 Positive+Edge không có ngoại lệ được ghi. | Kiểm tra các nhóm được yêu cầu và ngoại lệ có lý do; đồng thời sửa rule để áp theo điều kiện nghiệp vụ, tránh ép mọi ID phải có Positive. |
| R-03 | TC-007, 008, 024, 033, 034, 037; Q-01, Q-07 | Major | Có 14/39 TC ghi `[Cần xác nhận Q-…]`, gồm 5 P1. Một số phụ thuộc chưa được gắn đủ: TC-007/008/024 dùng câu OOS đang tranh luận nhưng không ghi Q-01. TC-033 dùng qty=1 cho mỗi dòng nên không phân biệt được đếm số dòng với tổng qty. | Quản lý trạng thái thiết kế/oracle riêng với trạng thái chạy. Truy vết Q/AS tới từng assertion; không đếm assertion chưa có oracle vào coverage đã xác nhận. Dùng dữ liệu phân biệt các cách hiểu. |
| R-04 | AC08; DT2; TC-024–026 | Major | DT2 chỉ có “đủ hết”, “có OOS và không có insufficient”, “có insufficient và không có OOS”. Trong một Cart, OOS và insufficient có thể xảy ra ở hai dòng khác nhau cùng lúc. Không có case cho tổ hợp này. | Mô hình hóa theo tập sản phẩm: có dòng stock=0 và có dòng 0<stock<qty là hai điều kiện có thể cùng đúng. Thêm rule và case xử lý đồng thời, rồi kiểm tra TC thực sự có assertion cho từng rule. |
| R-05 | TC-017, 018, 027, 031, 033, 035; analysis §16 | Major | Nhiều tiền điều kiện khó tái tạo: “đã xảy ra revalidate”, “đã tự điều chỉnh”; SP-A…SP-E chưa map SKU, SP-E là “sản phẩm bất kỳ”; thứ tự thêm được dùng như thứ tự hiển thị; giá KENZO từ mockup đã có chênh lệch giá/tạm tính nhưng thiếu cấu hình giảm giá; TC-035 không mô tả địa chỉ/bước đặt COD và qty ban đầu. | Có fixture với SKU/variant, qty, giá và promotion/tax, thứ tự quan sát ban đầu, stock scope, tài khoản, cách setup/reset. Luồng đặt hàng dùng procedure dùng chung có tham chiếu cụ thể. |
| R-06 | `rules/01` Gate 1; analysis §12; TC-039 | Major | Biết có ảnh chưa đọc nhưng chưa có trạng thái tổng thể phân biệt “nháp trên nguồn một phần” và “đã đủ nguồn”. TC-039 so UI với mockup hiện trạng cũ trong khi bản cập nhật chưa xem được. | Lập source manifest: nguồn/phiên bản/đã đọc hay chưa/ảnh hưởng. Nguồn thiếu vẫn cho phép làm phần độc lập, nhưng ghi Draft/Partial và không xác nhận UI chưa có bằng chứng. |
| R-07 | TC-034; `report.md` §2; tiêu đề DEV-3746/3770 trong bản chép nguồn | Major | TC-034 ghi regression DEV-3746 và DEV-3770 nhưng không tái hiện điều kiện quà tặng của DEV-3746 hoặc Set/bundle của DEV-3770. DEV-3770 còn có sản phẩm khác được chọn, khác case bỏ chọn hết. | Chỉ ghi coverage bug khi có fixture/trigger/assertion tái hiện đúng bug. Còn lại ghi “liên quan, chưa xác nhận tái hiện”. Đọc nội dung ticket trước khi nhận là regression hoàn chỉnh. |
| R-08 | validator dòng 94–114, 132, 142–148, 189 | Major | CSV thừa field bị bỏ qua, step nhảy số không bị bắt, AS không có trong analysis không bị phát hiện, Technique=DT không cần rule tồn tại. `--strict` vẫn không phát hiện vì không tạo warning. | Kiểm tra số ô/header trùng, thứ tự step, Q và AS tồn tại, DT/ST/EP/BVA mapping hợp lệ. Markdown chỉ để trình bày; dữ liệu coverage nên có schema riêng. |
| R-09 | TC-003/023; TC-021/022; `rules/05` chống trùng | Minor | TC-003 và TC-023 gần cùng setup/hành động/mục tiêu Checkout; TC-023 thêm assertion không có banner. TC-022 dùng 999 khi max=5 nhưng ghi BVA, dù đây là giá trị xa biên. | Rà gộp TC-003/023 và giữ đủ Req/assertion. TC-022 dùng EP/EG nếu có mục tiêu robustness riêng; nếu không có thì gộp với phân vùng vượt tồn kho. Không coi là trùng chắc chắn chỉ bằng so chữ. |
| R-10 | `examples/LOGIN/`; `rules/03` ví dụ | Minor | Ví dụ chuẩn LOGIN thiếu nhiều mục bắt buộc của analysis, chỉ có negative cho một số FR; các case mật khẩu 8/32 không ghi Positive do Scenario chỉ có một chiều. Kiểm tra khóa sau 16 phút chưa chứng minh đúng ngưỡng 15 phút. Ví dụ trong rules/03 còn có step gộp hai đầu vào. | Chỉnh ví dụ thành bộ tham chiếu thật sự tuân thủ rule sau khi sửa schema. Có ví dụ expected chưa xác nhận, fixture độc lập và coverage theo điều kiện. |
| R-11 | AGENTS mục 4; `rules/02`, `rules/03`, `rules/05` | Suggestion | Một số yêu cầu quá cứng hoặc dễ hiểu sai: mọi ID phải có Positive/Negative; mỗi invalid luôn tách; tỷ lệ Priority gợi ý thành chuẩn; mỗi rule đúng 1 TC; ID phải liên tục. | Áp dụng theo rủi ro/mục tiêu. Cho phép nhiều invalid khi kiểm tra tương tác DT; một rule có thể cần nhiều dữ liệu; giữ khoảng trống ID lịch sử; không hạ Priority để đạt tỷ lệ. |
| R-12 | Expected của 31/39 TC, ví dụ TC-024/029/035 | Minor | Expected bắt đầu dạng `1. 2.`, `1. 1.`; có đoạn như `1. 4. Ở mọi bước`, khiến quan hệ step–assertion khó hiểu. | Dùng một quy ước duy nhất: “Sau bước 2: …”, hoặc cặp Step_ID/Expected. Validator bắt số bước tham chiếu không tồn tại và định dạng lặp. |

## 4. Bằng chứng validator chưa thực thi đủ rule

Mỗi thử nghiệm dưới đây bắt đầu từ bản sao CSV gốc và dùng analysis gốc:

| Biến thể | Kết quả thực tế với `--strict` | Điều đang bị bỏ lọt |
|---|---|---|
| Đổi Scenario của cả 39 TC thành Negative | Exit 0; 0 ERROR, 0 WARNING; 18/18 | Không kiểm tra thiếu Positive |
| Đổi step 2 của TC-001 thành step 9, các step sau vẫn 3/4 | Exit 0; 0 ERROR, 0 WARNING; 18/18 | Không kiểm tra thứ tự step |
| Thêm `[Giả định AS-999]` vào Notes TC-001 | Exit 0; 0 ERROR, 0 WARNING; 18/18 | Không kiểm tra AS tồn tại |
| Xóa tất cả tham chiếu `DTn-Rn` khỏi Notes | Exit 0; 0 ERROR, 0 WARNING; 18/18 | Không đo coverage decision rules |
| Xóa TC-019, 021, 024, 025 | Exit 0; 0 ERROR, 0 WARNING; 18/18 | Mất biên 4/6 của AC07 và cả hai case stock thay đổi của AC08 vẫn đạt 100% theo ID |
| Thêm một ô CSV thứ 16 vào dòng TC-001, header vẫn 15 cột | Exit 0; 0 ERROR, 0 WARNING; 18/18 | Ô thừa bị bỏ qua |

Log tại thời điểm review: `/tmp/dev3648-rule-review/results.json`. Đây là bằng chứng giới hạn validator, không phải lỗi của ứng dụng giỏ hàng.

## 5. Coverage và các case nên bổ sung

Không có ID AC01–AC10, BR-01–BR-03, IMP-01–IMP-05 bị thiếu tham chiếu hoàn toàn. Các điều kiện sau còn thiếu hoặc cần làm rõ:

Rule **DT2-R4 đề xuất**: tại thời điểm bấm “Mua hàng”, có ít nhất một dòng được chọn có stock=0 **đồng thời** có ít nhất một dòng được chọn khác có 0<stock<qty. Kết quả: reload Cart + banner chung; dòng stock=0 bỏ tick/Disable; dòng insufficient giảm qty về stock và giữ tick; dòng hợp lệ khác giữ lựa chọn. Rule này áp dụng ở cấp Cart, không phải hai điều kiện cùng đúng trên một sản phẩm.

| Điều kiện | Đánh giá | Hành động |
|---|---|---|
| A hết hàng đồng thời C thiếu số lượng khi bấm Mua hàng | Thiếu trong DT2 và CSV; suy ra trực tiếp từ xử lý từng dòng ở AC08 | Đề xuất TC-CART-040 |
| Mọi dòng được chọn đều thành OOS; vẫn có dòng còn hàng nhưng đang bỏ tick | Thiếu tổ hợp revalidate + điều kiện nút AC04 | Đề xuất TC-CART-041 |
| Đếm số dòng hay tổng qty | TC-033 có qty=1 nên hai cách đếm cho cùng kết quả | Đợi Q-07; dùng A qty=2, C qty=3 để phân biệt 2 dòng/5 đơn vị |
| Checkbox “Tất cả sản phẩm” trong giỏ mixed/all OOS | Đã nêu Q-03, chưa có case quyết định hành vi | Giữ coverage pending, bổ sung khi có oracle |
| Gift/Set/bundle và regression liên quan | Thiếu đặc tả chi tiết/fixture; không được coi đã cover nhờ gắn bug ID | Đọc ticket chi tiết theo Q-08 |
| Biên dưới qty và đầu vào sai kiểu | Q-05 chưa có câu trả lời | Không tự đặt expected 0/âm/chữ/thập phân |
| Dòng đang bỏ tick bị thay đổi tồn kho có làm reload/banner hay không | Chưa có oracle đủ rõ cho phạm vi revalidate | Làm rõ thêm phạm vi của AC08 trước khi viết expected |

Hai TC đề xuất trong `testcases-additional.csv` dùng ID tiếp nối 040–041, không sửa bộ gốc. Chỉ kiểm tra những hành vi suy ra từ AC04/AC08, không tự chọn câu thông báo OOS đang tranh luận. File bổ sung được validate độc lập vì đây là một phần của suite; kết quả không được hiểu là coverage toàn bộ analysis. Bản ghép tạm với 39 TC gốc cũng được kiểm tra bằng analysis đầy đủ.

Kết quả kiểm tra phần bổ sung:

- `python3 scripts/validate_testcases.py output/DEV-3648/testcases-additional.csv --strict`: **0 ERROR, 0 WARNING**; không đo coverage toàn bộ requirements.
- `python3 scripts/validate_testcases.py /tmp/dev3648-rule-review/combined.csv --analysis output/DEV-3648/analysis.md`: **0 ERROR, 1 WARNING**. Cảnh báo P1 chiếm 15/41 ≈ 37%, vượt ngưỡng 35% của script. Giữ hai case bổ sung ở P1 vì kiểm tra revalidate và ngăn chuyển Checkout sai; không hạ Priority chỉ để đạt tỷ lệ. Đây là giải trình cho bản ghép đề xuất, không phải thay đổi report gốc.

Nhóm gần trùng cần xem: TC-003/023. TC-021/022 cùng phân vùng vượt stock, nhưng chỉ gộp nếu không có mục tiêu riêng cho giá trị rất lớn. Những case kết hợp nhiều assertion để mô tả cùng một lần revalidate không cần tách máy móc thành từng checkbox/message.

Không thêm ID Q mới vào analysis gốc trong lần review này. Ưu tiên trả lời Q-01, Q-03, Q-07, Q-08; câu hỏi phạm vi revalidate của dòng bỏ tick ở bảng trên là đề xuất cần xác nhận khi mở rộng suite.

## 6. Thay đổi rule nên làm trước

### Ưu tiên 1: tách các loại bằng chứng

Thêm vào `rules/01`, `rules/05`, template report và phần trả lời của tc-generate:

> Validator pass là điều kiện cần. Báo riêng: tỷ lệ ID có TC, tỷ lệ điều kiện có assertion, coverage kỹ thuật đã chọn và trạng thái expected. Khi nguồn chưa đọc đủ hoặc expected còn pending, bộ test được bàn giao ở trạng thái Draft/Partial; không công bố đã xác nhận đầy đủ.

Với AC có nhiều mệnh đề, giữ nguyên AC gốc và thêm Condition_ID nội bộ, ví dụ `AC08-C01`. Mỗi điều kiện có source anchor, expected/oracle và TC_ID. BR suy ra từ AC ghi quan hệ dẫn xuất, không dùng số lượng BR để làm tăng cảm giác bao phủ.

### Ưu tiên 2: expected, giả định và mức sẵn sàng

> Mỗi expected phải có cơ sở từ nguồn hoặc AS được khai báo. AS ghi rõ chưa xác nhận/đã chấp thuận và người/ngày xác nhận nếu có. TC có thao tác chạy được nhưng chưa có expected quyết định pass/fail phải được nhận diện là chưa sẵn sàng về oracle.

Dùng `Design_Status` hoặc bảng phụ cho Draft/Needs Clarification/Ready. Giữ `Status` hiện tại cho kết quả chạy; chỉ dùng Blocked khi thực tế không chạy/đánh giá được. `Automation=Candidate` không có nghĩa là đã sẵn sàng tự động hóa; còn cần oracle ổn định và cách điều khiển/reset stock.

### Ưu tiên 3: dữ liệu kỹ thuật có cấu trúc

> Với DT/ST/EP/BVA, phải liệt kê các coverage item có ID, mức áp dụng và TC/assertion tương ứng. DT loại tổ hợp bất khả thi, ghi tổ hợp chưa rõ là pending; không dùng dấu “–” cho tổ hợp bất khả thi. Các điều kiện “có ít nhất một sản phẩm” không được coi là loại trừ nhau nếu chúng có thể đúng ở các dòng khác nhau.

Nên bổ sung file JSON theo schema cho requirements/conditions, sources, Q/AS và design coverage; Markdown được sinh từ đó hoặc đối chiếu nhất quán. Không dựa vào regex quét mọi bảng Markdown để quyết định mọi ngoại lệ N/A/Positive-only.

### Ưu tiên 4: sửa validator theo phần có thể kiểm tra tự động

1. Bắt header trùng/thừa field, dòng thiếu dữ liệu và thứ tự step.
2. Kiểm tra Q/AS và coverage item được tham chiếu tồn tại.
3. Kiểm tra nhóm Scenario theo applicability/ngoại lệ đã khai báo; không chỉ so đúng `{Positive}`.
4. Kiểm tra mỗi coverage item yêu cầu có TC active và assertion mapping; giữ phần đánh giá ngữ nghĩa cho review.
5. Xuất diagnostics có mã ổn định; exception/waiver có mã lỗi, lý do, phạm vi và phiên bản. `--strict` chỉ phát huy tác dụng khi đã có diagnostics phù hợp.

### Ưu tiên 5: fixture, ví dụ chuẩn và quy tắc linh hoạt

> TC phải có fixture tái tạo độc lập hoặc tham chiếu procedure setup có phiên bản. Dữ liệu minh họa do tester tự chuẩn bị được phép dùng, nhưng không trình bày như dữ liệu đang tồn tại trên môi trường. Setup phải đủ để người khác tạo/reset mà không chạy TC trước.

Điều chỉnh các điểm sau:

- Positive/Negative là thuộc tính tình huống; Boundary/Edge là khía cạnh khác. Có thể tách hai chiều hoặc cho phép nhiều nhãn, nhưng cần cập nhật đồng bộ CSV, validator, exporter và ví dụ.
- Mục tiêu coverage lấy từ điều kiện và rủi ro; tỷ lệ P1/P2 hay Positive chỉ là số liệu quan sát, không phải quota để sửa Priority/Scenario.
- Mặc định EP invalid tách để cô lập lỗi; cho phép DT/EG kết hợp đầu vào lỗi khi mục tiêu là tương tác hoặc thứ tự ưu tiên thông báo.
- BVA dựa trên phân vùng có thứ tự và đơn vị bước; không gọi giá trị rất xa biên là BVA. Với miền chưa xác nhận, ghi pending và không tuyên bố đã đủ biên.
- ID duy nhất, ổn định; không bắt lấp khoảng trống lịch sử. Rule “liên tục” không được dẫn tới đánh số lại.
- Sửa LOGIN thành bộ tham chiếu hoàn chỉnh và thêm các mẫu cố ý vi phạm để đánh giá validator khi triển khai thay đổi.

## 7. Đối chiếu nguồn ISTQB

CTFL v4.0.1 §4.2.2 gắn BVA với phân vùng có thứ tự; §4.2.3 đo decision-table coverage trên tổ hợp khả thi và cho phép rút gọn/chọn theo rủi ro; §5.1.5 nêu ưu tiên theo rủi ro, coverage hoặc yêu cầu. Các nội dung này hỗ trợ hướng cải thiện ở trên, không chứng nhận bộ rule hiện tại. [ISTQB CTFL Syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf).

## 8. Thay đổi trong lần review

Tạo `review.md` và `testcases-additional.csv`; chỉ tạo các bản sao kiểm tra trong `/tmp`. Không chỉnh sửa input, rule, skill, script hay 39 TC gốc. Chưa chạy kiểm thử ứng dụng và chưa xác nhận nội dung các ticket con ngoài bản chép nguồn.
