"""Assemble lesson fragments (src/<id>.html) into one self-contained page.

Usage (run from the lessons/ folder):
    python3 build.py                      # every fragment listed in course.json "order"
    python3 build.py --only l0,l3-1       # only these (publish reviewed lessons early)
    LESSONS_ONLY=l0,l3-1 python3 build.py # same, via the environment

Reads course.json (see the skill's assets/course.example.json) and src/shell.html.
Shared JavaScript files in src/ can be spliced into fragments with a comment
placeholder such as  /*__INCLUDE:_engine.js__*/  (put it inside a <script>).
"""
import argparse, html, json, os, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "src"

ap = argparse.ArgumentParser()
ap.add_argument("--config", default=str(HERE / "course.json"))
ap.add_argument("--only", default=os.environ.get("LESSONS_ONLY", ""))
args = ap.parse_args()

cfg = json.loads(pathlib.Path(args.config).read_text())
ORDER = cfg["order"]
CHAPTERS = cfg["chapters"]
PLAN = cfg.get("plan", [])
ONLY = [x.strip() for x in args.only.split(",") if x.strip()]


def attrs(frag, path):
    m = re.search(r"<section\b([^>]*)>", frag)
    if not m:
        sys.exit(f"{path}: no <section> tag")
    a = dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
    idm = re.search(r'\bid="([^"]+)"', m.group(1))
    a["id"] = idm.group(1) if idm else None
    for k in ("ch", "short", "title", "date", "minutes"):
        if k not in a:
            sys.exit(f"{path}: <section> is missing data-{k}")
    return a


frags, meta, missing = [], {}, []
for lid in ORDER:
    if ONLY and lid not in ONLY:
        continue
    f = SRC / f"{lid}.html"
    if not f.exists():
        missing.append(lid)
        continue
    t = f.read_text()
    a = attrs(t, f)
    if a["id"] != lid:
        sys.exit(f"{f}: section id is {a['id']!r}, expected {lid!r}")
    frags.append(t)
    meta[lid] = a

# splice shared JS
def include(m):
    p = SRC / m.group(1)
    if not p.exists():
        sys.exit(f"include not found: {p}")
    return p.read_text()

frags = [re.sub(r"/\*__INCLUDE:([\w.\-]+)__\*/", include, f) for f in frags]

# lesson index (rendered twice by the shell: sidebar + phone menu)
nav = ['<nav class="index" aria-label="Lessons">']
cur = None
for lid in ORDER:
    if lid not in meta:
        continue
    a = meta[lid]
    if a["ch"] != cur:
        cur = a["ch"]
        nav.append(f'<div class="ch">{html.escape(CHAPTERS.get(cur, "Chapter " + cur))}</div>')
    nav.append(
        f'<a href="#{lid}" data-id="{lid}"><span class="dot"></span><span>{html.escape(a["short"])} · '
        f'{html.escape(a["title"])}<small>{html.escape(a["date"])} · ~{html.escape(a["minutes"])} min</small></span></a>'
    )
nav.append("</nav>")

rows = []
for p in PLAN:
    links = ", ".join(
        f'<a href="#{i}">{html.escape(meta[i]["short"])} {html.escape(meta[i]["title"])}</a>'
        for i in p.get("lessons", []) if i in meta
    ) or "—"
    rows.append(
        f'<tr data-md="{html.escape(p.get("date", ""))}"><td>{html.escape(p.get("day", p.get("date", "")))}</td>'
        f'<td>{links}</td><td>{html.escape(p.get("practice", ""))}</td></tr>'
    )

shell = (SRC / "shell.html").read_text()
exam = cfg.get("exam", {})
fill = {
    "TITLE": html.escape(cfg["title"]),
    "BRAND": html.escape(cfg.get("brand", cfg["title"])),
    "COURSE": html.escape(cfg.get("course", "")),
    "TERM": html.escape(cfg.get("term", "")),
    "HERO_TITLE": html.escape(cfg.get("hero_title", "Lessons, in study order")),
    "HERO_SUB": cfg.get("hero_sub", ""),            # trusted HTML
    "PLAN_INTRO": cfg.get("plan_intro", ""),        # trusted HTML
    "STUDY_TIP": cfg.get("study_tip", "Writing it yourself is the practice that transfers to an exam."),
    "STORAGE_KEY": re.sub(r"[^\w\-]", "-", cfg.get("storage_key", "lessons-v1")),
    "EXAM_ISO": exam.get("iso", ""),
    "EXAM_LABEL": html.escape(exam.get("label", "")),
    "EXAM_NAME": html.escape(exam.get("name", "the exam")),
}
out = shell
for k, v in fill.items():
    out = out.replace("{{" + k + "}}", v)
out = out.replace("<!--NAV-->", "\n".join(nav)).replace("<!--PLAN-->", "\n".join(rows)).replace("<!--LESSONS-->", "\n".join(frags))

left = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", out)))
if left:
    print("warning: unfilled placeholders:", ", ".join(left))
if missing:
    print("note: not written yet:", ", ".join(missing))

target = HERE / cfg.get("output", "Lessons.html")
target.write_text(out)
print(f"built {len(frags)} lessons -> {target.name}, {len(out) // 1024} KB")
