import openpyxl, os, shutil, io
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter
from PIL import Image

SRC = r'C:\Users\htndi\Downloads\test-case-render-2026-10-16\test-case-render\output\TestCase_Dashboard_Customer.xlsx'
OUT_DIR = r'C:\Users\htndi\Downloads\test-case-render-2026-10-16\test-case-render\output'
OUT = os.path.join(OUT_DIR, 'TestCase_Dashboard_Customer_retest_2026-10-18.xlsx')
EV = r'C:\Users\htndi\Downloads\test-case-render-2026-10-16\pw-tests\evidence2'
EV_OUT = os.path.join(OUT_DIR, 'evidence_retest_2026-10-18')
TMP = os.path.join(os.environ['TEMP'], 'xl_thumbs'); os.makedirs(TMP, exist_ok=True)

P, F, B, S = 'passed', 'failed', 'blocked', 'skipped'
def f(k): return f'{k}__funnel'
def t(k): return f'{k}__top'
def tt(k): return f'{k}__total'
def pp(k): return f'{k}__period'
E01, E02, E03, E04, E05, E06, E07, E08, E10, E11, E12, E13 = ('E01_thang_nay_all', 'E02_thang_truoc', 'E03_tuan_nay', 'E04_nam_nay', 'E05_custom_thang3_2026', 'E06_custom_den_31_10_tuong_lai', 'E07_custom_1_ngay_30_09', 'E08_ky_rong_2020', 'E10_custom_366_ngay', 'E11_boss_only_oct', 'E12_hermes_only_oct', 'E13_boss_only_sep')

NO_DATA = 'Không test được trên dữ liệu thật: cần '
R = {}
def add(ids, res, note, *imgs):
    for i in ids.split():
        R[i if i.startswith('TC-') else 'TC-CSD-' + i] = (res, note, list(imgs))

# ---- Nhóm 2
add('010-01', P, "Mở dashboard: preset 'Tháng này' active, kỳ 01/10/2026–18/10/2026 (đúng ngày hôm nay 18/10/2026); đổi preset tính lại ngay (Tháng trước = 01/09–30/09). Quan sát ngoài case: 'Tuần này' vào Chủ nhật 18/10/2026 hiển thị 18/10–18/10, theo quy tắc tuần bắt đầu Thứ Hai phải là 12/10–18/10 → đề nghị kiểm tra.", f(E01), f(E03))
add('010-02', P, "Đơn hoàn tất 23:59 ngày 31/10/2026 (UTC+7) của 'Phạm Minh Đức' thuộc kỳ 01–31/10 và không có trong kỳ 01–18/10 → biên ngày theo UTC+7 đúng. (Hệ thống không có đơn 23:50 ngày 30/09 như Given nên dùng đơn biên 31/10.)", t(E06), t(E01))
add('010-03', F, "Chọn 01/03/2025–02/03/2026 (367 ngày): có toast 'Khoảng ngày không được vượt quá 366 ngày' nhưng (1) ô ngày vẫn hiển thị khoảng 367 ngày, không quay về kỳ trước; (2) chỉ lỗi 400 ở các API overview/top/period, bảng 'In selected period' bị rỗng trong khi Funnel/Top 50 giữ số cũ → trạng thái không nhất quán; (3) xuất hiện nhiều toast trùng. Kỳ vọng: không áp dụng, giữ nguyên kỳ trước.", 'T367_a_sau_0_6s', 'T367_c_sau_6s')
add('010-04', P, "Bảng Breakdown by CA – Total giống hệt qua 14 kỳ lọc khác nhau (Tháng này/Tháng trước/Tuần này/Năm nay/Custom): API customer-assignments không đổi, số trên UI không đổi.", tt(E01), tt(E02))
# ---- Nhóm 3
add('002-01', B, NO_DATA + "20 khách mẫu (Phụ lục A). Số thực tế: Tháng này = 6, Tháng trước = 12, Năm nay = 15.", f(E01))
add('002-02', P, "Khách mua nhiều đơn chỉ đếm 1: tháng này tổng # trans trong Top 50 = 16 đơn nhưng Total Customers = 6 khách (TEST AUTO 3 có 6 đơn vẫn tính 1).", f(E01), t(E01))
add('002-03', B, NO_DATA + "khách chỉ có Engagement Log, không có đơn hợp lệ trong kỳ.")
add('002-04', B, NO_DATA + "khách mua ở cả 2 store. Store Hermès Metropole không có đơn nào trong 2026 nên không dựng được tình huống.")
add('002-05', P, "Kỳ 'Tuần này' (18/10/2026) không có đơn: Total Customers hiển thị 0 (không phải —); Kỳ 01–31/01/2020 cũng ra 0.", f(E03), f(E08))
add('002-06', B, "Không đối soát được: tab Business (Month) hiển thị Customers = 0, Avg Spending/Customer = 0 VND trong khi tab Customer tháng này = 6 khách; hai tab dùng API khác nhau và Business chưa có dữ liệu → cần BA/Dev xác nhận phạm vi.", f(E01))
add('003-01', P, "Tháng này: Total 6, New (Store-level) 3 = 3 khách có First transaction date trong kỳ (Nguyễn Thị Bích Ngọc 13/10, Le Thanh Tun 14/10, Hoàng Thị Lan Anh 14/10); 3 khách còn lại có first order 30/09 → Existing.", f(E01), t(E01))
add('003-02', P, "Khách có lần mua đầu tại store trong kỳ được xếp New: 'Nguyễn Thị Bích Ngọc' first = 13/10/2026 (kỳ tháng 10) → nằm trong New Customers = 3.", f(E01), t(E01))
add('003-03', P, "Khách có first order trước kỳ không là New dù mua lại trong kỳ: TEST AUTO 3 / AUYO4 / TEST AUTO ASIGNEE first 30/09/2026, mua lại tháng 10 → thuộc Existing (3).", f(E01), t(E01))
add('003-04', B, NO_DATA + "khách có đơn đầu tiên do nhân viên khác đứng tên bill để xác nhận độc lập với người đứng tên.")
add('003-05 003-08', B, NO_DATA + "khách có lịch sử mua ở 2 store. Store Hermès Metropole chưa có đơn.")
add('003-06', B, NO_DATA + "đơn giữ First Order Date bị huỷ (thao tác tạo/huỷ đơn trên hệ thống thật).")
add('003-07', P, "Kỳ không có khách (Tuần này 18/10/2026 và 01–31/01/2020): New Customers = 0.", f(E03), f(E08))
add('004-01', P, "Chọn riêng Boss 46 (Brand BOSS), tháng trước: New Store-level = 10, New Brand-level = 3, Existing Brand = 9 (3+9 = Total 12) → New(Brand) ⊆ New(Store). (Số thực tế khác số mẫu 6/4 nhưng đúng quy tắc BR-CSD-008.)", f(E13))
add('004-02 004-03', B, NO_DATA + "khách có lịch sử mua ở Brand khác / lần đầu mua tại Brand để đối chiếu trực tiếp; môi trường chỉ có 1 store có đơn.")
add('004-04 004-05', B, NO_DATA + "tài khoản Retail Manager / Store Manager để kiểm tra phạm vi (case phân quyền, theo yêu cầu bỏ qua).")
add('004-06', P, "Chọn Tất cả Store (nhiều Brand): hiện khối 'CẤP BRAND' nhắc chọn store của 1 Brand, không cộng gộp mọi Brand; các khối Store-level vẫn hiển thị bình thường.", f(E01))
add('004-07 004-08', B, "Bộ chọn store của tài khoản này chỉ có 2 store (Boss 46, Hermès), không có chip Brand và không có dữ liệu 20/30/5 khách như Given; không dựng được tình huống.", 'DROPDOWN_stores')
add('005-01', P, "Công thức đúng trên dữ liệu thật: Tháng này Existing = 6−3 = 3, Repeat Rate = 3/6 = 50.0%; Năm nay Existing = 15−13 = 2, Repeat = 13.3%. (Số mẫu 20/6/14/70% không có trên hệ thống.)", f(E01), f(E04))
add('005-02', P, "Brand-level (chọn Boss 46, tháng trước): Total 12, New(Brand) 3 → Existing(Brand) = 9, Repeat Rate (Brand) = 75.0% = 9/12.", f(E13))
add('005-03', P, "Kỳ không có khách: Repeat Rate hiển thị — (không phải 0%), Existing = 0.", f(E03))
add('005-04', P, "Kỳ 30/09/2026: Total 8, New 8 → Existing 0, Repeat Rate = 0.0%.", f(E07))
add('005-05', P, "Làm tròn half-up 1 chữ số: 2/12 = 16.666…% hiển thị 16.7%; 3/7 = 42.857…% hiển thị 42.9%; 2/15 = 13.3%.", f(E02), f(E06))
add('005-06', P, "New + Existing = Total ở mọi kỳ đã xem: 3+3=6, 10+2=12, 13+2=15, 4+3=7, 8+0=8; Brand-level 3+9=12, 0+6=6.", f(E01), f(E02))
# ---- Nhóm 4
add('006-01', F, "Tháng trước, Tất cả Store: Top 50 có 4 khách Sales Value ≥ 100 triệu (718 304 000; 168 000 000; 155 810 000; 140 936 000 — tương ứng 1 VIC + 3 VIC Potential, đúng cấu trúc case mẫu) nhưng VIC Customers = 0 (kỳ vọng 4).", f(E02), t(E02))
add('006-08', F, "Khách có Net Spend ≥ 100 000 000 không được tính vào VIC Customers: Tháng trước 4 khách ≥ 100 triệu, Năm nay 4 khách (có khách 3 704 936 000) nhưng VIC Customers luôn = 0.", f(E04), t(E04))
add('006-10', F, "Custom 01–31/03/2026: Duong Hang có Sales Value 282 420 000 (≥ 100 triệu → VIC Potential) nhưng VIC Customers = 0.", f(E05), t(E05))
add('006-18', P, "Kỳ không có khách (01–31/01/2020): VIC Customers hiển thị 0.", f(E08))
add('006-02 006-03 006-04 006-05 006-06 006-07 006-09 006-11 006-12 006-13 006-14 006-15 006-16 006-17', B, NO_DATA + "khách có Net Spend theo đúng ngưỡng/đơn trả/nhiều store để dựng tình huống (dữ liệu hiện có: 1 store có đơn, không đơn trả, không khách sát ngưỡng). Lưu ý lỗi chung đã ghi ở TC-CSD-006-01.")
# ---- Nhóm 5
add('007-01', B, NO_DATA + "≥ 51 khách trong kỳ (cao nhất hiện có 16 khách). Đã thấy sắp giảm dần theo Sales Value ở các kỳ.", t(E04))
add('007-02', P, "Tháng này có 7 khách: bảng hiện đúng 7 hàng ('7 khách', '1–7 / 7 hàng'), không có hàng trống đệm.", t(E01))
add('007-03 007-04 007-14', B, NO_DATA + "khách có đơn trả hợp lệ trong kỳ (chưa có đơn trả trên môi trường).")
add('007-05', P, "Cùng Sales Value 8 000 000: 'Debug Probe 6' (last 16/10) xếp trên 'TEST AUTO ASIGNEE ĐƠN HÀNG 1' (last 13/10). Tháng trước, nhóm 16 000 000 xếp theo Last transaction mới → cũ.", t(E01), t(E02))
add('007-06', P, "Preset Tháng này: TEST AUTO 3 mua lần cuối 13/10 → hiển thị 'A7 · 5 ngày' (13/10→18/10).", t(E01))
add('007-07', F, "Kỳ hoàn toàn trong quá khứ (01–30/09/2026): cột Recency hiển thị chip 'Inactive' (API recency = null) thay vì '—'; Last transaction date hiển thị đúng.", t(E02))
add('007-08', P, "Cột PIC hiển thị tên CA kèm nhãn: 'Boss 46 Tràng Tiền HN · Nguyễn Phan Tùng · Advisor-Selected' (Bích Ngọc) và 'Auto-assigned' (TEST AUTO 3).", 'E01__wide_top')
add('007-09', P, "Khách chưa có PIC tại store ('Debug Probe 6') hiển thị 'Chưa có PIC'.", 'E01__wide_top')
add('007-10 007-19', B, NO_DATA + "khách có giao dịch ở nhiều store (Store Hermès Metropole chưa có đơn).")
add('007-11', F, "Custom 01–31/03/2026: # trans và Last transaction chỉ tính trong kỳ (Duong Hang: 2 đơn, last 19/03/2026, trong khi cả năm là 53 đơn) nhưng Recency hiển thị 'Inactive'/trống thay vì '—' theo kỳ vọng.", t(E05))
add('007-12', B, NO_DATA + "khách đổi PIC giữa kỳ để xác nhận PIC hiện tại.")
add('007-13', B, "Chưa xác định được kết quả: # trans/Sales/Last transaction không bị ảnh hưởng bởi đơn ngoài kỳ (Duong Hang 03/2026: 2 đơn; năm nay: 53 đơn) nhưng First transaction date hiển thị mốc lifetime (30/10/2025, trước kỳ). Spec không định nghĩa rõ First transaction date → cần BA xác nhận.", t(E05))
add('007-15', P, "Khách không có hạng Loyalty hiển thị '—' (TEST AUTO 3, AUYO4...), khách có hạng hiển thị 'Member'.", t(E01))
add('007-16', P, "Năm nay (01/01–18/10/2026): Duong Hang last 19/09/2026 → 'A30 · 29 ngày'; QA SearchFilter last 15/09 → 'A60 · 33 ngày' (tính tới hôm nay 18/10).", t(E04))
add('007-17', F, "Custom 01–31/10/2026 (kết thúc tương lai): kỳ không bị coi là 'tới hiện tại' — vẫn tính đơn ngày 31/10/2026 23:59 của 'Phạm Minh Đức' (Last transaction 31/10/2026, Recency 'A7 · 0 ngày'), Total tăng từ 6 lên 7, Top 50 thành 8 khách. Kỳ vọng: chỉ tính đến hôm nay (18/10).", t(E06), f(E06))
add('007-18', F, "Kỳ 1 ngày trong quá khứ (30/09/2026): cột Recency hiển thị 'Inactive' thay vì '—'. (Kỳ 17/10/2026 không có đơn nên dùng 30/09 để kiểm tra.)", t(E07))
add('007-20', F, "Tháng này, Tất cả Store: Top 50 có 7 khách ('Debug Probe 6' chưa có PIC) nhưng Total Customers = 6 → có khách trong Top 50 không thuộc customer_in_period. Năm nay: Top 50 = 16 khách vs Total 15.", f(E01), t(E01))
add('007-21', B, NO_DATA + "khách mua rồi trả hết hàng trong kỳ.")
add('007-22', P, "Khách Top 50 khớp hàng PIC hiện tại ở bảng In selected period: Nguyễn Phan Tùng có 4 khách (1 AS, 3 AA) = hàng (4, 1, 3); Nguyễn Ngọc Trinh có 2 khách (2 AS) = hàng (2, 2, 0).", 'E01__wide_top', 'E01__wide_period')
# ---- Nhóm 6
add('008-01', F, "Hàng 'Nguyễn Phan Tùng' (23 khách): AS 11 + AA 7 = 18 ≠ Total 23 (vi phạm AS + AA = Total, BR-CSD-015); hàng 'Chưa gán PIC' Total 208 có AS = AA = 0.", 'E01__wide_total')
add('008-02', F, "Tổng 7 bucket Recency ≠ Total ở hầu hết các hàng: Nguyễn Phan Tùng Total 50 – bucket 10; Chưa gán PIC Total 49 – bucket 17; Nguyễn Thị Thu Huyền Total 22 – bucket 0; chỉ một số hàng khớp (Trinh 7 = 7).", 'E01__wide_total')
add('008-03', P, "Bảng Total không đổi khi đổi kỳ (Tháng này → Tháng trước → Năm nay → Custom): các số giữ nguyên.", tt(E01), tt(E02))
add('008-04', B, NO_DATA + "khách có last_order_date_store cách hôm nay đúng 7 và 8 ngày.")
add('008-05', F, "Cột INACTIVE = 0 ở mọi hàng dù tổng bucket thấp hơn Total (vd Nguyễn Phan Tùng: 50 khách, bucket 10, Inactive 0) → khách chưa có đơn tại store không được xếp vào Inactive.", 'E01__wide_total')
add('008-07', P, "Bảng chỉ có cột '# Advisor-Selected (AS)' và '# Auto-assigned (AA)', không có cột tách theo mức waterfall.", 'E01__wide_total')
add('008-08 008-14 008-10', B, NO_DATA + "thao tác đổi PIC thủ công / hồ sơ khách có last_order_date_store cụ thể / CA không giữ khách (không thao tác được trên production).")
add('008-09 008-15 008-16', S, "Bỏ qua theo yêu cầu (case phân quyền).")
add('008-11', P, "Mặc định 'Tất cả Store': bảng Total hiển thị hàng của cả 2 store (Boss 46 và Hermès) với các CA riêng; chọn riêng Boss 46 chỉ còn hàng Boss 46.", 'E01__wide_total', tt(E11))
add('008-12', P, "Chọn riêng Boss 46: Funnel (Total 6, 1 Store), Top 50 (6 khách) và 2 bảng Breakdown by CA chỉ tính cho Boss 46.", f(E11), tt(E11))
add('008-13', P, "Bảng Total vẫn tính khách không có đơn trong kỳ: Tháng này chỉ 6 khách có đơn nhưng bảng Total có 208/50/49... khách theo PIC (toàn tệp khách, không giới hạn kỳ).", 'E01__wide_total')
# 009
add('009-01', P, "Công thức % Contacted đúng: hàng Nguyễn Ngọc Trinh 2/2 = 100.0%; Custom 01–31/10: Trinh 2/3 = 66.7%.", 'E01__wide_period', pp(E06))
add('009-02 009-03 009-04 009-05 009-09 009-14', B, NO_DATA + "khách + điểm chạm (cuộc gọi NO_ANSWER/CONNECTED, lịch hẹn Completed) và PIC/người đứng tên bill được kiểm soát; không tạo được trên production.")
add('009-06', P, "New + Existing = Total ở mọi hàng đã xem (Tháng này: Trinh 0+2=2, Tùng 1+3=4; Tháng trước: 0+7, 1+0, ...).", pp(E01), 'E02__wide_period')
add('009-07', P, "Bảng In selected period chỉ có khách có đơn trong kỳ (Tháng này: tổng 4+2 = 6) trong khi Total có hàng trăm khách không có đơn.", 'E01__wide_period', 'E01__wide_total')
add('009-08', P, "Hàng không có khách trong kỳ không hiển thị: Hermès Metropole / tháng này → bảng 'Không có dữ liệu', '0 / 0 hàng'.", pp(E12))
add('009-10', F, "Tháng trước: hàng Nguyễn Phan Tùng gồm 2 khách chi ≥ 100 triệu (155 810 000 và 140 936 000, đều Advisor-Selected) nhưng cột VICs = 0.", 'E02__wide_period', t(E02))
add('009-11', P, "Đổi kỳ → mọi cột và danh sách hàng đổi theo (Tháng này 2 hàng; Tháng trước 5 hàng với số khác).", pp(E01), 'E02__wide_period')
add('009-12', P, "Hàng có PIC: AS + AA = Total (Tùng 2+5=7, Trinh 2+0=2, Lê Thanh Tùng 1+0=1). Lưu ý: hàng không PIC ('···') có Total 1 nhưng AS = AA = 0.", 'E02__wide_period')
add('009-13 009-22', B, NO_DATA + "CA có khách/đơn ở 2 store; Store Hermès Metropole chưa có đơn.")
add('009-15', F, "Khách chi ≥ 100 000 000 không được tính vào cột VICs (inclusive không hoạt động): Tháng trước hàng Nguyễn Phan Tùng có 2 khách 155.8M/140.9M, VICs = 0.", 'E02__wide_period')
add('009-16 009-17 009-18 009-19 009-20', B, NO_DATA + "khách có Net Spend sát ngưỡng / chi ở nhiều store / đơn trả. Lưu ý lỗi VICs luôn = 0 đã ghi ở TC-CSD-009-10.")
add('009-21', F, "Tháng trước có hàng không PIC ('···', Total 1, AS = AA = 0, Existing 1) trong bảng In selected period và Total các hàng (12) = Total Customers (12); theo spec khách chưa có PIC không được nằm ở hàng nào và tổng các hàng phải nhỏ hơn Total Customers.", 'E02__wide_period', f(E02))
# ---- Nhóm 7
add('011-01', P, "Total = 0 → Repeat Rate hiển thị — (không phải 0%).", f(E03))
add('011-02', P, "Tỷ lệ 1 chữ số thập phân: Repeat Rate 50.0%, 100.0%, 0.0%; % Contacted 100.0%.", f(E01), 'E01__wide_period')
add('011-03', P, "Tỷ lệ tuần hoàn làm tròn half-up: 16.666…% → 16.7%; 42.857…% → 42.9%; % Contacted 2/3 → 66.7%.", f(E02), pp(E06))
add('011-04', P, "Số tiền phân tách hàng nghìn bằng khoảng trắng: Sales Value 48 800 000, 718 304 000, 3 704 936 000.", t(E01), t(E04))
add('011-05', P, "Số dưới 1000 không tách nhóm: Total customers 208, 50, 49, 45 (bảng Total); # trans 6, 4, 2.", 'E01__wide_total')
add('011-06', P, "Chọn riêng Boss 46: khối Brand-level ghi rõ chip 'BOSS'; New 0 + Existing 6 = 6 = Total Customers chính, không có Total thứ hai.", f(E11))
# ---- Nhóm 8
add('012-01', P, "Customer Funnel chỉ có 1 số cho mỗi chỉ số (Total 6, New 3, Existing 3, Repeat 50.0%), không có bảng tách theo store. (Tài khoản hiện tại không phải CRM nhưng chọn Tất cả Store.)", f(E01))
add('012-02', P, "Một bộ chọn store áp dụng cho mọi khối: chọn riêng Boss 46 → Funnel 1 Store, Top 50 và 2 bảng chỉ còn Boss 46; chọn riêng Hermès → Funnel 0, Top 50 trống, bảng Total chỉ có hàng Hermès.", f(E11), tt(E12))
add('012-03', P, "Danh sách bộ chọn store chỉ có 'Tất cả Store', 'Boss 46 Tràng Tiền HN', 'Hermès Metropole HN Store' (đúng 2 store được cấp theo API physical-stores), không có store khác để chọn.", 'DROPDOWN_stores')
add('012-04', P, "Gõ 'Huyền' → bảng Total còn 3 hàng của CA Nguyễn Thị Thu Huyền (ở cả 2 store); bảng In selected period và các khối khác không đổi.", 'U01_search_CA_Huyen', 'U03b_period_unchanged_khi_tim_total')
add('012-05', P, "Gõ 'Hermès' → bảng Total chỉ còn 5 hàng của store Hermès Metropole HN Store.", 'U02_search_store_Hermes')
add('012-06', F, "Bấm tiêu đề cột A7 (bảng Total): thứ tự hàng đổi theo A7 nhưng cột PIC NAME và STORE hiển thị '···', Total/AS/AA = 0 ở mọi hàng (chỉ còn cột A7…); bấm lần 2 vẫn không hiển thị đủ dữ liệu.", 'U04_sort_A7_lan1', 'U05_sort_A7_lan2')
add('012-07', P, "Sắp xếp bảng 'In selected period' theo # Contacted customers không làm bảng Total thay đổi (Total vẫn giữ trạng thái sắp xếp A7 riêng). Lưu ý: bảng Total đang hiển thị lỗi sau khi sort A7 (xem TC-CSD-012-06).", 'U06_period_sort_contacted', 'U06b_total_van_giu_sort_A7')
add('012-08', P, "Tìm 'zzzzqq' → bảng Total hiển thị rỗng ('0 / 0 hàng'), các khối khác (Funnel, bảng In selected period) không đổi.", 'U03_search_khong_ket_qua', 'U03b_period_unchanged_khi_tim_total')
add('012-09', P, "Mở lần đầu: hiển thị 15 hàng đầu, sắp theo Total customers giảm dần (208, 50, 49, 45...), chân bảng '1–15 / 16 hàng'. (Dữ liệu thật 16 hàng, không phải 312.)", 'U00_total_default')
add('012-10', P, "Các hàng cùng Total xếp theo tên store rồi tên CA tăng dần: Total=3 → Hoàng Bá Bình (Boss), Chưa gán PIC (Hermès), Lê Mạnh Cường (Hermès); Total=1 → Nguyễn Nhật Vy (Boss), Lê Mạnh Cường, Lê Thanh Tùng STS, Nguyễn Thị Thu Huyền (Hermès); thứ tự giống nhau giữa các lần tải.", 'U07_pagesize_30')
add('012-11', P, "Chọn số dòng 15/30/50: 15 → '1–15 / 16 hàng'; 30 và 50 → '1–16 / 16 hàng'. (Dữ liệu thật 16 hàng, không phải 312.)", 'U07_pagesize_30', 'U08_pagesize_50')
add('012-12', P, "Tìm 'Huyền' trả hàng từ cả trang 1 lẫn trang 2 (hàng Hermès ở trang 2 xuất hiện ngay ở trang 1 kết quả); tìm theo toàn bộ dữ liệu, không chỉ trang đang xem.", 'U01_search_CA_Huyen', 'U09_trang_2')

# ---------------- build
wb = openpyxl.load_workbook(SRC)
ws = wb['Test Cases']
os.makedirs(EV_OUT, exist_ok=True)
hdr_src = ws['J1']
thin = Side(style='thin', color='FFBFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
for col, (title, width) in zip(range(14, 18), [('Kết quả re-test 18/10/2026', 17), ('Ghi chú re-test (thực tế quan sát trên https://ca-app.sts.vn/dashboard)', 62), ('Bằng chứng 1', 62), ('Bằng chứng 2', 62)]):
    c = ws.cell(1, col, title)
    c.font = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
    c.fill = PatternFill('solid', fgColor='FF1F4E78')
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    c.border = border
    ws.column_dimensions[get_column_letter(col)].width = width
FILL = {P: 'FFC6EFCE', F: 'FFFFC7CE', B: 'FFFFEB9C', S: 'FFD9D9D9'}
LABEL = {P: 'passed', F: 'failed', B: 'blocked (không test được)', S: 'skipped (phân quyền)'}
used = {}
rows = {ws.cell(r, 3).value: r for r in range(2, ws.max_row + 1)}
missing = [k for k in R if k not in rows]
assert not missing, missing
def thumb(key):
    src = os.path.join(EV, key + '.png')
    assert os.path.exists(src), src
    shutil.copy2(src, os.path.join(EV_OUT, key + '.png'))
    im = Image.open(src).convert('RGB')
    w = 560
    h = int(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    dst = os.path.join(TMP, key + '.jpg'); im.save(dst, 'JPEG', quality=72)
    return dst, w, h
for tid, r in rows.items():
    if tid not in R:
        continue
    res, note, imgs = R[tid]
    c = ws.cell(r, 14, LABEL[res]); c.fill = PatternFill('solid', fgColor=FILL[res])
    c.font = Font(name='Arial', size=10, bold=True); c.alignment = Alignment(wrap_text=True, vertical='top', horizontal='center'); c.border = border
    n = ws.cell(r, 15, note); n.font = Font(name='Arial', size=10); n.alignment = Alignment(wrap_text=True, vertical='top'); n.border = border
    maxh = 0
    for i, key in enumerate(imgs[:2]):
        dst, w, h = thumb(key)
        img = XLImage(dst); img.width, img.height = w * 0.95, h * 0.95
        ws.add_image(img, f'{get_column_letter(16 + i)}{r}')
        maxh = max(maxh, h * 0.95)
    for col in (16, 17):
        ws.cell(r, col).border = border
    if maxh:
        ws.row_dimensions[r].height = max(ws.row_dimensions[r].height or 15, maxh * 0.75 + 8)
    else:
        ws.row_dimensions[r].height = max(ws.row_dimensions[r].height or 15, 60)
# untested rows (group 1): mark
for tid, r in rows.items():
    if tid.startswith('TC-CSD-001'):
        c = ws.cell(r, 14, LABEL[S]); c.fill = PatternFill('solid', fgColor=FILL[S]); c.font = Font(name='Arial', size=10, bold=True)
        c.alignment = Alignment(wrap_text=True, vertical='top', horizontal='center'); c.border = border
        n = ws.cell(r, 15, 'Bỏ qua theo yêu cầu (nhóm phân quyền, FR-CSD-001).'); n.font = Font(name='Arial', size=10); n.alignment = Alignment(wrap_text=True, vertical='top'); n.border = border
ws.auto_filter.ref = f'A1:Q{ws.max_row}'

# summary sheet
sm = wb.create_sheet('Tong hop re-test 18-10-2026', 0)
from collections import Counter
cnt = Counter(v[0] for v in R.values()); cnt[S] += sum(1 for t in rows if t.startswith('TC-CSD-001'))
lines = [
    ('Kết quả re-test dashboard Customer — ngày 18/10/2026', None),
    ('URL', 'https://ca-app.sts.vn/dashboard (tab Customer), tài khoản Nguyễn Thị Thu Huyền, 2 store được cấp: Boss 46 Tràng Tiền HN, Hermès Metropole HN Store'),
    ('Cách test', 'Playwright (Chromium) điều khiển trình duyệt thật + đọc API của dashboard để đối chiếu; ảnh chụp từng khối làm bằng chứng. Thư mục ảnh gốc: evidence_retest_2026-10-18'),
    ('Giới hạn', "Dữ liệu thật rất ít (tháng này chỉ 6 khách, 1 store có đơn, không có đơn trả/huỷ, không khách sát ngưỡng) nên các case phụ thuộc dữ liệu mẫu cụ thể được ghi 'blocked' kèm lý do, không bịa kết quả."),
    ('Cột gốc', "Cột J 'passed/failed' và K 'Ghi chú' của file gốc giữ nguyên; kết quả mới nằm ở cột N–Q."),
    (None, None),
    ('passed', cnt[P]), ('failed', cnt[F]), ('blocked (không test được)', cnt[B]), ('skipped (phân quyền)', cnt[S]),
    (None, None),
    ('Lỗi phát hiện (failed)', None),
]
fails = [(k, v) for k, v in R.items() if v[0] == F]
for k, v in fails:
    lines.append((k, v[1]))
lines += [(None, None), ('Quan sát ngoài case', "'Tuần này' vào Chủ nhật 18/10/2026 hiển thị 18/10–18/10 thay vì 12/10–18/10 (tuần bắt đầu Thứ Hai); tab Business (Month) hiển thị 0 khách trong khi tab Customer tháng này = 6."), ]
for i, (a, b) in enumerate(lines, 1):
    ca = sm.cell(i, 1, a); cb = sm.cell(i, 2, b)
    ca.font = Font(name='Arial', size=10, bold=True); cb.font = Font(name='Arial', size=10)
    ca.alignment = Alignment(wrap_text=True, vertical='top'); cb.alignment = Alignment(wrap_text=True, vertical='top')
sm['A1'].font = Font(name='Arial', size=13, bold=True)
sm.column_dimensions['A'].width = 30; sm.column_dimensions['B'].width = 120
wb.save(OUT)
print('saved', OUT, dict(cnt), 'cases with verdict', len(R))
