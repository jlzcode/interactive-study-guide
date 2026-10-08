#!/usr/bin/env python3
"""Static checks for a lesson site built with the interactive-study-guide skill.

  check_site.py <lessons dir> [--config course.json] [--only l0,l1-1]

Errors (exit code 1): missing section attributes, wrong qid prefixes, duplicate qids,
bare '<' inside TeX, registerLesson id mismatch, unfilled {{PLACEHOLDERS}} in the built page,
JavaScript syntax errors in the built page (needs node).
Warnings: fewer than 2 figures or 5 checks, missing teaching boxes, unprefixed element ids,
hard-coded hex colours, document.getElementById on ids from another lesson.
"""
import argparse, json, pathlib, re, shutil, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--config", default=None)
ap.add_argument("--only", default="")
a = ap.parse_args()

root = pathlib.Path(a.dir).resolve()
cfg = json.loads(pathlib.Path(a.config or root / "course.json").read_text())
only = [x for x in a.only.split(",") if x]
errors, warns = [], []
all_qids = {}


def err(m): errors.append(m)
def warn(m): warns.append(m)


for lid in cfg["order"]:
    if only and lid not in only:
        continue
    f = root / "src" / f"{lid}.html"
    if not f.exists():
        continue
    s = f.read_text()
    m = re.search(r"<section\b([^>]*)>", s)
    if not m:
        err(f"{lid}: no <section>"); continue
    attrs = dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
    for k in ("ch", "short", "title", "date", "minutes"):
        if k not in attrs:
            err(f"{lid}: <section> missing data-{k}")
    if f'id="{lid}"' not in m.group(1):
        err(f"{lid}: <section> id must be {lid!r}")

    html_part = s.split("<script>")[0]
    for cls, need, kind in [('class="eyebrow"', 1, warn), ('class="idea"', 1, warn), ('class="roadmap"', 1, warn),
                            ('class="glossary"', 1, warn), ('class="box hard"', 1, warn), ('class="box exam"', 1, warn),
                            ('class="key"', 1, warn)]:
        if html_part.count(cls) < need:
            kind(f"{lid}: no {cls}")
    nfig = html_part.count('class="viz"')
    if nfig < 2:
        warn(f"{lid}: only {nfig} interactive figure(s); aim for at least 2")

    checks = re.findall(r'<div class="check"([^>]*)>', html_part)
    if len(checks) < 5:
        warn(f"{lid}: {len(checks)} self-checks; aim for 5-8")
    for c in checks:
        q = re.search(r'data-qid="([^"]+)"', c)
        if not q:
            err(f"{lid}: a .check has no data-qid"); continue
        qid = q.group(1)
        if not qid.startswith(lid + "-q"):
            err(f"{lid}: qid {qid!r} should start with '{lid}-q'")
        if qid in all_qids:
            err(f"{lid}: duplicate qid {qid!r} (also in {all_qids[qid]})")
        all_qids[qid] = lid
        if 'data-topic="' not in c:
            warn(f"{lid}: {qid} has no data-topic (weak-spot list will show the raw id)")

    for idv in re.findall(r'\sid="([^"]+)"', html_part):
        if idv != lid and not idv.startswith(lid + "-"):
            warn(f"{lid}: element id {idv!r} is not prefixed with '{lid}-'")

    # bare '<' inside TeX breaks the HTML parser when followed by a letter, '/' or '!'
    for tex in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", html_part, re.S):
        body = tex[0] or tex[1]
        if re.search(r"<[A-Za-z/!]", body):
            err(f"{lid}: bare '<' inside TeX: {body.strip()[:60]!r} (write &lt; or \\lt)")

    script = s.split("<script>", 1)[1] if "<script>" in s else ""
    reg = re.findall(r"registerLesson\('([^']+)'", script)
    if script and lid not in reg:
        err(f"{lid}: script does not call registerLesson('{lid}', ...)")
    for hexc in set(re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b(?![\w-])", script + html_part)):
        warn(f"{lid}: hard-coded colour {hexc}; use Viz.color()/var(--token) so dark mode works")
    for gid in re.findall(r"getElementById\('([^']+)'\)", script):
        if not gid.startswith(lid):
            warn(f"{lid}: getElementById('{gid}') reaches outside the lesson; use root.querySelector")

out = root / cfg.get("output", "Lessons.html")
if out.exists():
    page = out.read_text()
    left = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", page)))
    if left:
        err(f"built page has unfilled placeholders: {', '.join(left)} (set them in course.json)")
    node = shutil.which("node")
    if node:
        js = "\n;\n".join(re.findall(r"<script>(.*?)</script>", page, re.S))
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as t:
            t.write(js)
        r = subprocess.run([node, "--check", t.name], capture_output=True, text=True)
        if r.returncode:
            err("JavaScript syntax error in the built page:\n" + r.stderr.strip()[:800])
    else:
        warn("node not found: skipped the JavaScript syntax check")
else:
    warn(f"{out.name} not built yet: run build.py, then re-run this check for the script syntax test")

for w in warns:
    print("warn :", w)
for e in errors:
    print("ERROR:", e)
print(f"\n{len(all_qids)} self-checks across lessons; {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
