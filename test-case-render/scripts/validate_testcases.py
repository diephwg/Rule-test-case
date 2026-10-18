#!/usr/bin/env python3
"""Validate a test case CSV against rules/03-dinh-dang-test-case.md and rules/05-review-quality-gate.md.

Usage:
    python3 scripts/validate_testcases.py output/<FEATURE>/testcases.csv \
        [--analysis output/<FEATURE>/analysis.md] [--sources output/<FEATURE>/_extracted] \
        [--previous old-testcases.csv] [--strict]

ERROR   = vi phạm cấu trúc / truy vết mà công cụ kiểm tra được — phải sửa.
WARNING = ứng viên cần người review — sửa hoặc giải trình, KHÔNG sửa chỉ để hết cảnh báo.
Validator pass là điều kiện cần, không chứng minh chất lượng nghiệp vụ (xem rules/05).

Exit code: 0 = không có ERROR (và không có WARNING khi dùng --strict), 1 = ngược lại.
Standard library only.
"""
import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REQUIRED_COLUMNS = [
    "TC_ID", "Module", "Req_ID", "Title", "Test_Type", "Scenario", "Technique", "Priority",
    "Preconditions", "Test_Data", "Steps", "Expected_Result", "Automation", "Status", "Notes",
]
NON_EMPTY = ["TC_ID", "Module", "Req_ID", "Title", "Test_Type", "Scenario", "Technique",
             "Priority", "Steps", "Expected_Result"]
ENUMS = {
    "Test_Type": {"Functional", "UI", "Validation", "Integration", "API", "Security", "Performance",
                  "Accessibility", "Compatibility", "Usability"},
    "Scenario": {"Positive", "Negative", "Boundary", "Edge"},
    "Technique": {"EP", "BVA", "DT", "ST", "UC", "PW", "CRUD", "PERM", "EG", "CL"},
    "Priority": {"P1", "P2", "P3", "P4"},
    "Automation": {"", "Yes", "No", "Candidate"},
    "Status": {"", "Not Run", "Pass", "Fail", "Blocked", "Skipped", "Obsolete"},
}
TC_ID_RE = re.compile(r"^TC-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3,}$")
TC_REF_RE = re.compile(r"\bTC-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3,}\b")
# Accepts REQ-LOGIN-01, FR-01, BR-02, IMP-03 and dash-less IDs such as AC01 / US12
REQ_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-?\d+[A-Za-z]?$")
NON_REQ_PREFIXES = ("Q-", "AS-", "TC-", "CO-", "SETUP-", "IX-", "EV-")
Q_RE = re.compile(r"\bQ-\d+\b")
AS_RE = re.compile(r"\bAS-\d+\b")
SETUP_RE = re.compile(r"\bSETUP-\d+\b")
COND_RE = re.compile(r"^CO-\d+$")
CO_REF_RE = re.compile(r"\bCO-\d+\b")
CLAUSE_RE = re.compile(r"^[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-c\d+[a-z]?$")  # AC08-c3, AC08-c3a
ITEM_RE = {"interactions": re.compile(r"^IX-\d+$"), "triggers": re.compile(r"^EV-\d+$")}
# "TC-CART-004, 007, 008" -> prefix + bare numbers that follow it
TC_LIST_RE = re.compile(r"\b(TC-[A-Z0-9]+(?:-[A-Z0-9]+)*-)(\d{3,})((?:\s*[,;/]\s*\d{3,}\b(?!-))*)")
# Dependency written as free text instead of a Q-xx / AS-xx marker (rules/03 §Notes)
FREE_DEP_RE = re.compile(r"cần xác nhận|chờ xác nhận|chưa xác nhận|giả định|chưa rõ|chưa xác định|\btbd\b|"
                         r"to be confirmed|\bassum", re.I)
SETUP_STATES = {"sẵn sàng": "ready", "cần chuẩn bị": "prep", "chưa rõ cách làm": "unclear"}
QUOTE_RE = re.compile(r'["“”]([^"“”\n]{3,})["“”]')
OPEN_ANSWERS = {"", "-", "?", "(chờ)", "chờ", "pending", "tbd"}
SOURCE_EXT = {".md", ".txt", ".csv", ".feature", ".json", ".yaml", ".yml", ".xml", ".html"}

# Heading keyword in analysis.md -> kind of table below it (first match wins)
SECTION_KEYS = [
    ("mệnh đề nguồn", "clauses"), ("ma trận trạng thái", "statematrix"),
    ("ma trận tương tác", "interactions"), ("sự kiện kích hoạt", "triggers"),
    ("điều kiện kiểm thử", "conditions"), ("chiến lược kiểm thử", "conditions"),
    ("danh sách yêu cầu", "reqs"), ("quy tắc nghiệp vụ", "reqs"), ("yêu cầu ngầm định", "reqs"),
    ("câu hỏi", "questions"), ("giả định", "assumptions"),
    ("setup", "setups"), ("dữ liệu test", "setups"),
]

VAGUE_EXPECTED = [
    "hoạt động bình thường", "hoạt động đúng", "hiển thị đúng", "như mong đợi", "như mong muốn",
    "đúng như yêu cầu", "theo yêu cầu", "không có lỗi", "ok", "works correctly", "as expected",
    "works fine", "works as expected", "correctly displayed", "no error",
]
VAGUE_DATA = ["hợp lệ", "không hợp lệ", "bất kỳ", "ngẫu nhiên", "valid", "invalid", "any ", "random"]
MAX_STEPS = 12
MAX_TITLE = 150


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def norm_src(text):
    """Normalise for verbatim lookup: NFC, lower-case, digits -> '#', collapse spaces."""
    text = unicodedata.normalize("NFC", text or "").lower()
    return re.sub(r"\s+", " ", re.sub(r"\d+", "#", text))


def split_ids(value):
    return [p.strip() for p in re.split(r"[;,\n]", value or "") if p.strip()]


def clean(cell):
    return cell.strip().strip("`*").strip()


def iter_tables(text):
    """Yield (section_kind, header_cells_lower, row_cells) for every markdown table row."""
    section, header = None, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            low = s.lower()
            section = next((kind for kw, kind in SECTION_KEYS if kw in low), None)
            header = None
            continue
        if not s.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        yield section, header, cells


def col(header, cells, *keywords):
    for i, h in enumerate(header):
        if any(k in h for k in keywords) and i < len(cells):
            return cells[i]
    return ""


def col_exact(header, cells, name):
    for i, h in enumerate(header):
        if clean(h) == name and i < len(cells):
            return cells[i]
    return None


def is_na(cells):
    return any(re.match(r"N/?A\b", clean(c), re.I) for c in cells[1:])


def is_pending(cells):
    return any(clean(c).lower().startswith("pending") for c in cells[1:])


def expand_tc_refs(text):
    """All TC IDs in text, expanding shorthand lists such as 'TC-CART-004, 007, 008'."""
    ids = set(TC_REF_RE.findall(text or ""))
    for prefix, first, rest in TC_LIST_RE.findall(text or ""):
        ids.update(prefix + n.zfill(len(first)) for n in re.findall(r"\d{3,}", rest))
    return ids


def parse_analysis(path):
    """Parse analysis.md into requirement, question, assumption, condition and setup registries."""
    a = {"reqs": {}, "req_na": set(), "req_confirmed": set(), "req_rejected": set(), "imp": set(),
         "questions": {}, "assumptions": {}, "conditions": {}, "setups": {},
         "clauses": {}, "interactions": {}, "triggers": {}, "statematrix": [], "sections": set()}
    for section, header, cells in iter_tables(Path(path).read_text(encoding="utf-8")):
        first = clean(cells[0])
        row_low = " ".join(cells).lower()
        if section:
            a["sections"].add(section)
        if section == "statematrix":
            a["statematrix"].append((first, header, cells))
        elif section == "clauses" and CLAUSE_RE.match(first):
            a["clauses"][first] = {
                "req": clean(col(header, cells, "req")),
                "cos": CO_REF_RE.findall(" ".join(cells[1:])),
                "qs": Q_RE.findall(" ".join(cells[1:])),
                "na": is_na(cells), "pending": is_pending(cells),
                "desc": clean(col(header, cells, "mệnh đề", "clause")),
            }
        elif section in ITEM_RE and ITEM_RE[section].match(first):
            a[section][first] = {
                "cos": CO_REF_RE.findall(" ".join(cells[1:])),
                "qs": Q_RE.findall(" ".join(cells[1:])),
                "na": is_na(cells), "pending": is_pending(cells),
                "desc": " · ".join(clean(c) for c in cells[1:3]),
            }
        elif section == "questions" and re.fullmatch(r"Q-\d+", first):
            has_answer_col = any("trả lời" in h for h in header)
            answer = clean(col(header, cells, "trả lời")).lower()
            a["questions"][first] = (not has_answer_col) or answer in OPEN_ANSWERS
        elif section == "assumptions" and re.fullmatch(r"AS-\d+", first):
            a["assumptions"][first] = {"qs": set(Q_RE.findall(" ".join(cells[1:]))),
                                       "tcs": expand_tc_refs(col(header, cells, "case")),
                                       "has_tc_col": any("case" in h for h in header),
                                       "confirmed": "đã xác nhận" in row_low}
        elif section == "setups" and re.fullmatch(r"SETUP-\d+", first):
            raw = col_exact(header, cells, "trạng thái")
            state = None if raw is None else SETUP_STATES.get(clean(raw).lower(), "invalid")
            a["setups"][first] = {"state": state, "raw": clean(raw or "")}
        elif section == "conditions" and COND_RE.match(first):
            a["conditions"][first] = {
                "reqs": split_ids(clean(col(header, cells, "req"))),
                "tcs": TC_REF_RE.findall(" ".join(cells[1:])),
                "tech": clean(col(header, cells, "kỹ thuật", "technique")),
                "na": is_na(cells),
                "pending": is_pending(cells),
                "desc": clean(col(header, cells, "điều kiện", "condition")),
            }
        elif section == "reqs" and REQ_ID_RE.match(first) and not first.startswith(NON_REQ_PREFIXES):
            a["reqs"].setdefault(first, clean(cells[1]) if len(cells) > 1 else "")
            if is_na(cells):
                a["req_na"].add(first)
            if "từ chối" in row_low:
                a["req_rejected"].add(first)
            elif "đã xác nhận" in row_low:
                a["req_confirmed"].add(first)
            if first.startswith("IMP-"):
                a["imp"].add(first)
    return a


def design_status(row, a):
    """Return (status, reasons).

    Blocked             - references a SETUP whose state is 'Chưa rõ cách làm' (cannot be executed yet)
    Needs Clarification - relies on an open Q / unconfirmed AS / unconfirmed IMP (expected is provisional)
    """
    if row.get("Status") == "Obsolete":
        return "Obsolete", []
    if a is None:
        return "", []
    text = " ".join(row.get(k, "") for k in ("Notes", "Expected_Result", "Preconditions", "Test_Data"))
    blocked = [s for s in sorted(set(SETUP_RE.findall(text)))
               if a["setups"].get(s, {}).get("state") == "unclear"]
    reasons = []
    for q in sorted(set(Q_RE.findall(text))):
        if a["questions"].get(q, True):
            reasons.append(q)
    for s in sorted(set(AS_RE.findall(text))):
        asn = a["assumptions"].get(s)
        if not asn or not asn["confirmed"]:
            reasons.append(s)
    for rid in split_ids(row.get("Req_ID")):
        if rid in a["imp"] and rid not in a["req_confirmed"]:
            reasons.append(rid)
    if blocked:
        return "Blocked", blocked + reasons
    return ("Needs Clarification", reasons) if reasons else ("Ready", [])


def load_sources(path):
    p = Path(path)
    files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in SOURCE_EXT]
    return norm_src("\n".join(f.read_text(encoding="utf-8", errors="replace") for f in files)), len(files)


def read_csv(path):
    """Return (header, rows). Cells beyond the header are kept under '__extra__'."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, restkey="__extra__")
        header = [h.strip() for h in (reader.fieldnames or [])]
        rows = []
        for r in reader:
            row = {k.strip(): (v or "").strip() for k, v in r.items() if k and k != "__extra__"}
            row["__extra__"] = [v for v in (r.get("__extra__") or []) if (v or "").strip()]
            rows.append(row)
    return header, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--analysis", help="analysis.md — kiểm tra truy vết yêu cầu, điều kiện kiểm thử, Q/AS/SETUP")
    ap.add_argument("--sources", help="thư mục/file tài liệu nguồn đã trích xuất (mặc định <thư mục csv>/_extracted)")
    ap.add_argument("--previous", help="testcases.csv phiên bản trước — kiểm tra ID ổn định")
    ap.add_argument("--strict", action="store_true", help="coi WARNING là lỗi")
    args = ap.parse_args()

    errors, warnings = [], []

    def err(where, msg):
        errors.append(f"[ERROR] {where}: {msg}")

    def warn(where, msg):
        warnings.append(f"[WARN]  {where}: {msg}")

    header, rows = read_csv(args.csv_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        print(f"[ERROR] header: thiếu cột {missing}. Header chuẩn: templates/testcases-template.csv")
        return 1
    dup = sorted(h for h, n in Counter(header).items() if n > 1)
    if dup:
        print(f"[ERROR] header: cột bị trùng {dup}")
        return 1
    if header[:len(REQUIRED_COLUMNS)] != REQUIRED_COLUMNS:
        warn("header", "thứ tự cột khác templates/testcases-template.csv")

    a = parse_analysis(args.analysis) if args.analysis else None
    src_path = args.sources or (Path(args.csv_path).parent / "_extracted")
    sources, n_src = load_sources(src_path) if Path(src_path).exists() else ("", 0)

    seen_ids, fingerprints = {}, {}
    req_to_tcs = defaultdict(list)
    as_marked = defaultdict(set)
    status_by_tc, active_ids, obsolete_ids = {}, set(), set()
    active = []

    for i, row in enumerate(rows, start=2):
        tc = row["TC_ID"] or f"dòng {i}"
        loc = f"{tc} (dòng {i})"

        if row["__extra__"]:
            err(loc, f"dòng có {len(row['__extra__'])} ô thừa ngoài header — kiểm tra dấu phẩy / ngoặc kép")
        for c in NON_EMPTY:
            if not row[c]:
                err(loc, f"cột {c} đang trống")
        for c, allowed in ENUMS.items():
            if row[c] and row[c] not in allowed:
                err(loc, f"{c}='{row[c]}' không hợp lệ. Cho phép: {sorted(v for v in allowed if v)}")
        if row["TC_ID"]:
            if not TC_ID_RE.match(row["TC_ID"]):
                err(loc, "TC_ID sai quy ước TC-<MODULE>-<NNN> (vd. TC-LOGIN-001)")
            if row["TC_ID"] in seen_ids:
                err(loc, f"TC_ID trùng với dòng {seen_ids[row['TC_ID']]}")
            seen_ids.setdefault(row["TC_ID"], i)

        refs_text = " ".join(row[k] for k in ("Notes", "Expected_Result", "Preconditions", "Test_Data"))
        if a is not None:
            for q in sorted(set(Q_RE.findall(refs_text))):
                if q not in a["questions"]:
                    err(loc, f"tham chiếu {q} nhưng analysis.md không có câu hỏi này")
                elif not a["questions"][q] and row["Status"] != "Obsolete":
                    warn(loc, f"{q} đã có trả lời — cập nhật case theo câu trả lời và bỏ đánh dấu chờ")
            for s in sorted(set(AS_RE.findall(refs_text))):
                if s not in a["assumptions"]:
                    err(loc, f"tham chiếu {s} nhưng analysis.md không có giả định này")
                elif row["Status"] != "Obsolete":
                    as_marked[s].add(row["TC_ID"])
            for s in sorted(set(SETUP_RE.findall(refs_text))):
                if s not in a["setups"]:
                    err(loc, f"tham chiếu {s} nhưng analysis.md không có setup này")

        if row["Status"] == "Obsolete":
            obsolete_ids.add(row["TC_ID"])
            continue
        active.append(row)
        active_ids.add(row["TC_ID"])
        status_by_tc[row["TC_ID"]] = design_status(row, a)

        title = row["Title"]
        if title and not re.match(r"^(Kiểm tra|Verify)\b", title, re.I):
            warn(loc, "Title nên bắt đầu bằng 'Kiểm tra' / 'Verify'")
        if len(title) > MAX_TITLE:
            warn(loc, f"Title dài {len(title)} ký tự (> {MAX_TITLE})")

        step_lines = [ln for ln in row["Steps"].splitlines() if ln.strip()]
        if step_lines and not re.match(r"^\s*1[.)]", step_lines[0]):
            err(loc, "Steps phải đánh số bắt đầu từ '1.'")
        numbered = [int(m.group(1)) for ln in step_lines if (m := re.match(r"^\s*(\d+)[.)]", ln))]
        if numbered and numbered != list(range(1, len(numbered) + 1)):
            err(loc, f"Steps đánh số không liên tiếp {numbered} — phải là 1, 2, 3…")
        exp_refs = [int(m.group(1)) for ln in row["Expected_Result"].splitlines()
                    if (m := re.match(r"^\s*(\d+)[.)]", ln))]
        if numbered and any(n > len(numbered) for n in exp_refs):
            err(loc, f"Expected_Result tham chiếu bước {max(exp_refs)} nhưng Steps chỉ có {len(numbered)} bước")
        if exp_refs != sorted(set(exp_refs)):
            warn(loc, f"Expected_Result đánh số lặp/không tăng dần {exp_refs} — mỗi số là bước mà kết quả được kiểm tra")
        if len(numbered) > MAX_STEPS:
            warn(loc, f"{len(numbered)} bước (> {MAX_STEPS}) — xem có nhiều mục tiêu độc lập không")

        for field in ("Notes", "Expected_Result", "Preconditions"):
            for m in FREE_DEP_RE.finditer(row[field]):
                window = row[field][max(0, m.start() - 30):m.end() + 30]
                if not (Q_RE.search(window) or AS_RE.search(window)):
                    warn(loc, f"{field} ghi phụ thuộc bằng chữ tự do ('{m.group(0)}') không kèm Q-xx/AS-xx — "
                              "tạo câu hỏi/giả định và gắn marker, nếu không case bị tính Ready sai")
                    break

        if not row["Preconditions"]:
            warn(loc, "Preconditions trống — mô tả trạng thái ban đầu tái tạo được hoặc tham chiếu SETUP-xx")

        exp = norm(row["Expected_Result"])
        if len(re.sub(r"^\d+[.)]\s*", "", exp)) < 15:
            warn(loc, "Expected_Result quá ngắn — mô tả kết quả quan sát được cụ thể")
        for phrase in VAGUE_EXPECTED:
            if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", exp):
                warn(loc, f"Expected_Result mơ hồ: chứa '{phrase}'")
                break
        data = norm(row["Test_Data"])
        for phrase in VAGUE_DATA:
            if phrase.strip() in data and not re.search(r"\d|\"|@", data):
                warn(loc, f"Test_Data mơ hồ ('{phrase.strip()}') — ghi giá trị cụ thể")
                break

        if sources:
            not_found = [q for q in QUOTE_RE.findall(row["Expected_Result"]) if norm_src(q) not in sources]
            if not_found:
                shown = "; ".join(f'"{q}"' for q in not_found[:3])
                warn(loc, f"chuỗi trong ngoặc kép ở Expected_Result không thấy trong nguồn: {shown} — "
                          "ngoặc kép chỉ dùng cho văn bản nguyên văn từ nguồn")

        fp = (norm(row["Preconditions"]), norm(row["Steps"]), norm(row["Test_Data"]), exp)
        if fp in fingerprints:
            warn(loc, f"ứng viên trùng lặp với {fingerprints[fp]} — review mục tiêu, ngữ cảnh, phân vùng trước khi gộp")
        fingerprints.setdefault(fp, tc)

        for rid in split_ids(row["Req_ID"]):
            req_to_tcs[rid].append(tc)
            if a is not None and rid in a["req_rejected"]:
                warn(loc, f"{rid} đã bị từ chối trong analysis.md — đặt case Obsolete hoặc sửa Req_ID")

    if args.previous:
        _, prev_rows = read_csv(args.previous)
        for r in prev_rows:
            if r["TC_ID"] and r["TC_ID"] not in seen_ids:
                err(r["TC_ID"], "có trong phiên bản trước nhưng đã biến mất — không xoá/đánh số lại, giữ với Status=Obsolete")

    # ---- Traceability against analysis.md
    metrics = []
    if a is not None:
        reqs = a["reqs"]
        if not reqs:
            err("analysis", "không tìm thấy Req_ID trong các bảng Danh sách yêu cầu / Quy tắc nghiệp vụ / Yêu cầu ngầm định")
        for rid in sorted(set(req_to_tcs) - set(reqs)):
            err(rid, f"Req_ID dùng trong test case ({', '.join(req_to_tcs[rid][:3])}) nhưng không có trong analysis.md")
        must_cover = [r for r in reqs if r not in a["req_na"] and r not in a["req_rejected"]]
        for rid in must_cover:
            if rid not in req_to_tcs:
                err(rid, f"yêu cầu chưa có test case nào ({reqs[rid][:80]})")
        covered = sum(1 for r in must_cover if r in req_to_tcs)
        metrics.append(f"Req_ID có test case tham chiếu : {covered}/{len(must_cover)}"
                       + (f" · N/A: {len(a['req_na'])}" if a["req_na"] else "")
                       + (f" · bị từ chối: {len(a['req_rejected'])}" if a["req_rejected"] else ""))

        conds = a["conditions"]
        if conds:
            linked_tcs = set()
            by_tech = defaultdict(lambda: [0, 0])
            for cid, c in conds.items():
                for rid in c["reqs"]:
                    if rid not in reqs:
                        warn(cid, f"Req_ID '{rid}' của điều kiện không có trong danh sách yêu cầu")
                for t in c["tcs"]:
                    linked_tcs.add(t)
                    if t in obsolete_ids:
                        err(cid, f"tham chiếu {t} đang Obsolete")
                    elif t not in active_ids:
                        err(cid, f"tham chiếu {t} không có trong testcases.csv")
                if c["na"] or c["pending"]:
                    continue
                live = [t for t in c["tcs"] if t in active_ids]
                tech = c["tech"] or "?"
                by_tech[tech][1] += 1
                if live:
                    by_tech[tech][0] += 1
                else:
                    err(cid, f"điều kiện kiểm thử chưa có test case ({c['desc'][:70]}) — thêm case, hoặc ghi N/A/Pending kèm lý do")
            for t in sorted(active_ids - linked_tcs):
                warn(t, "không gắn với điều kiện kiểm thử nào trong analysis.md — review mục tiêu của case")
            reqs_with_cond = {r for c in conds.values() for r in c["reqs"]}
            for rid in must_cover:
                if rid not in reqs_with_cond:
                    warn(rid, "yêu cầu chưa có điều kiện kiểm thử (CO-xx) trong analysis.md")
            n_na = sum(1 for c in conds.values() if c["na"])
            n_pending = sum(1 for c in conds.values() if c["pending"] and not c["na"])
            cov = sum(v[0] for v in by_tech.values())
            tot = sum(v[1] for v in by_tech.values())
            metrics.append(f"Điều kiện kiểm thử có test case: {cov}/{tot} · N/A: {n_na} · Pending: {n_pending}")
            metrics.append("  theo kỹ thuật                 : "
                           + " · ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(by_tech.items())))
        else:
            metrics.append("Điều kiện kiểm thử             : chưa đánh giá (analysis.md không có bảng 'Điều kiện kiểm thử' với CO-xx)")

        # ---- Assumption <-> case markers (both directions)
        for s, asn in sorted(a["assumptions"].items()):
            if not asn["has_tc_col"]:
                continue
            listed = {t for t in asn["tcs"] if t not in obsolete_ids}
            for t in sorted(listed - as_marked[s]):
                warn(s, f"liệt kê {t} ở 'Case bị ảnh hưởng' nhưng case không có marker [Giả định {s}]")
            for t in sorted(as_marked[s] - listed):
                warn(s, f"{t} có marker {s} nhưng chưa có trong cột 'Case bị ảnh hưởng'")

        # ---- Coverage-item tables: source clauses, interactions (IX), triggers/channels (EV)
        def check_items(kind, label):
            items = a[kind]
            for iid, it in items.items():
                for c in it["cos"]:
                    if c not in conds:
                        err(iid, f"tham chiếu {c} nhưng không có trong bảng Điều kiện kiểm thử")
                for q in it["qs"]:
                    if q not in a["questions"]:
                        err(iid, f"tham chiếu {q} nhưng analysis.md không có câu hỏi này")
                if not (it["cos"] or it["na"] or it["pending"]):
                    err(iid, f"{label} chưa có kết luận ({it['desc'][:60]}) — ghi CO-xx, N/A - lý do hoặc Pending - Q-xx")
            return items

        def live_tcs(co_ids):
            return {t for c in co_ids for t in conds.get(c, {}).get("tcs", []) if t in active_ids}

        clauses = check_items("clauses", "mệnh đề")
        if not clauses:
            err("analysis", "thiếu mục 'Mệnh đề nguồn' (rules/01 Bước 2) — không có mẫu số khách quan cho bao phủ")
        else:
            for cid, c in clauses.items():
                if c["req"] and c["req"] not in reqs:
                    warn(cid, f"Req_ID '{c['req']}' của mệnh đề không có trong danh sách yêu cầu")
            with_clause = {c["req"] for c in clauses.values()}
            for rid in must_cover:
                if rid not in with_clause:
                    err(rid, "yêu cầu chưa được tách mệnh đề nguồn (Clause_ID <Req_ID>-c<n>)")
            denom = cov_c = ready_c = pend_c = na_c = 0
            for c in clauses.values():
                if c["na"]:
                    na_c += 1
                    continue
                tcs = live_tcs(c["cos"])
                if c["pending"] or (not tcs and c["cos"] and all(conds.get(x, {}).get("pending") for x in c["cos"])):
                    pend_c += 1
                    continue
                denom += 1
                cov_c += bool(tcs)
                ready_c += any(status_by_tc.get(t, ("",))[0] == "Ready" for t in tcs)
            metrics.insert(1, f"Mệnh đề nguồn có test case      : {cov_c}/{denom} · có case Ready: {ready_c}/{denom}"
                              f" · N/A: {na_c} · Pending: {pend_c}")

        for kind, label, title in (("interactions", "dòng tương tác", "Ma trận tương tác"),
                                   ("triggers", "dòng sự kiện/kênh", "Sự kiện kích hoạt & kênh")):
            items = check_items(kind, label)
            if not items:
                if kind == "triggers" or len(must_cover) > 1:
                    warn("analysis", f"thiếu mục '{title}' (rules/01 Bước 3) — điều kiện giữa các yêu cầu/kênh chưa được xét")
                continue
            n_na = sum(1 for it in items.values() if it["na"])
            n_p = sum(1 for it in items.values() if it["pending"] and not it["na"])
            n_co = len(items) - n_na - n_p
            metrics.append(f"  {title:<29}: {len(items)} dòng · CO {n_co} · N/A {n_na} · Pending {n_p}")

        # ---- Full state matrix (rules/02 §ST)
        uses_st = any("ST" in re.split(r"[^A-Z]+", c["tech"]) for c in conds.values())
        if uses_st and not a["statematrix"]:
            warn("analysis", "có điều kiện kỹ thuật ST nhưng thiếu 'Ma trận trạng thái' (mọi ô Trạng thái × Sự kiện phải có kết luận)")
        for state, header, cells in a["statematrix"]:
            empty = [header[i] for i in range(1, len(header)) if i >= len(cells) or not clean(cells[i])]
            if empty:
                warn(f"Ma trận trạng thái [{state}]", f"ô trống ở sự kiện {empty} — điền kết luận hoặc Q-xx")
            for c in CO_REF_RE.findall(" ".join(cells[1:])):
                if c not in conds:
                    err(f"Ma trận trạng thái [{state}]", f"tham chiếu {c} không có trong bảng Điều kiện kiểm thử")
            for q in Q_RE.findall(" ".join(cells[1:])):
                if q not in a["questions"]:
                    err(f"Ma trận trạng thái [{state}]", f"tham chiếu {q} nhưng analysis.md không có câu hỏi này")

        # ---- SETUP readiness
        for sid, s in sorted(a["setups"].items()):
            if s["state"] is None:
                warn(sid, "thiếu cột 'Trạng thái' (Sẵn sàng / Cần chuẩn bị / Chưa rõ cách làm)")
            elif s["state"] == "invalid":
                warn(sid, f"Trạng thái '{s['raw']}' không hợp lệ — dùng Sẵn sàng / Cần chuẩn bị / Chưa rõ cách làm")
        unclear = sorted(s for s, v in a["setups"].items() if v["state"] == "unclear")

        ready = Counter(s for s, _ in status_by_tc.values())
        metrics.append(f"Mức sẵn sàng thiết kế          : Ready {ready.get('Ready', 0)} · "
                       f"Needs Clarification {ready.get('Needs Clarification', 0)} · Blocked {ready.get('Blocked', 0)}")
        metrics.append("SETUP chưa rõ cách làm         : " + (", ".join(unclear) if unclear else "0"))
        open_q = sum(1 for v in a["questions"].values() if v)
        unconf_as = sum(1 for v in a["assumptions"].values() if not v["confirmed"])
        unconf_imp = len(a["imp"] - a["req_confirmed"] - a["req_rejected"])
        metrics.append(f"Đang chờ xác nhận              : Q mở {open_q} · AS chưa xác nhận {unconf_as} · IMP chưa xác nhận {unconf_imp}")
    else:
        metrics.append("Truy vết / sẵn sàng            : chưa đánh giá (không truyền --analysis)")
    metrics.append("Kiểm tra văn bản nguyên văn    : "
                   + (f"đã đối chiếu {n_src} file nguồn" if sources else "bỏ qua (không có --sources / _extracted)"))

    for line in errors + warnings:
        print(line)

    def fmt(counter):
        return " · ".join(f"{k}: {v}" for k, v in sorted(counter.items())) or "-"

    print("\n=== TÓM TẮT ===")
    print(f"Tổng test case (không tính Obsolete): {len(active)} · Obsolete: {len(obsolete_ids)}")
    print(f"Priority : {fmt(Counter(r['Priority'] for r in active))}")
    print(f"Scenario : {fmt(Counter(r['Scenario'] for r in active))}")
    print(f"Test_Type: {fmt(Counter(r['Test_Type'] for r in active))}")
    print(f"Technique: {fmt(Counter(r['Technique'] for r in active))}")
    print(f"Module   : {fmt(Counter(r['Module'] for r in active))}")
    print("(Phân bổ trên chỉ là thống kê, không phải chỉ tiêu.)")
    for m in metrics:
        print(m)
    print(f"Kết quả  : {len(errors)} ERROR · {len(warnings)} WARNING")
    print("Lưu ý    : 0 ERROR chỉ xác nhận cấu trúc & truy vết; chất lượng nghiệp vụ phải review theo rules/05.")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
