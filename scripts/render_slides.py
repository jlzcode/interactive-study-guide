#!/usr/bin/env python3
"""Read lecture decks the way a lesson writer needs to.

  render_slides.py scan  <deck> [<deck> ...]
      Page count, the pages with (almost) no text layer -- these MUST be read as images --
      and the first words of every page, for building a page map.

  render_slides.py grid  <deck> --pages 1-6,9,12-14 --out DIR [--dpi 75] [--cols 3] [--per 6]
      Render pages to PNG grids (6 pages per image by default) and print the image paths.
      Read the PNGs with the image viewer; 70-100 dpi is enough for slides, zoom in on dense
      pages with a higher --dpi and --per 1.

  render_slides.py topdf <deck.pptx|.ppt|.docx> --out DIR
      Convert with LibreOffice and print the PDF path.

<deck> may be .pdf, .pptx, .ppt, .docx; non-PDF files are converted first (needs LibreOffice).
Requires PyMuPDF (`pip install pymupdf`) and Pillow.
"""
import argparse, os, pathlib, shutil, subprocess, sys, tempfile

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF is missing: pip install pymupdf")


def find_soffice():
    for c in [shutil.which("soffice"), shutil.which("libreoffice"),
              "/Applications/LibreOffice.app/Contents/MacOS/soffice"]:
        if c and os.path.exists(c):
            return c
    return None


def to_pdf(path, out_dir=None):
    p = pathlib.Path(path).resolve()
    if p.suffix.lower() == ".pdf":
        return p
    out = pathlib.Path(out_dir or tempfile.mkdtemp(prefix="slides_")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = out / (p.stem + ".pdf")
    if target.exists() and target.stat().st_mtime >= p.stat().st_mtime:
        return target
    so = find_soffice()
    if not so:
        sys.exit(f"cannot convert {p.name}: LibreOffice (soffice) not found. Install it or export to PDF.")
    profile = out / "lo_profile"
    # A private profile avoids the lock/first-run problems that make soffice exit silently.
    cmd = [so, "--headless", f"-env:UserInstallation=file://{profile}", "--convert-to", "pdf", "--outdir", str(out), str(p)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
    if not target.exists():
        sys.exit(f"conversion failed for {p}")
    return target


def parse_pages(spec, n):
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return [p for p in pages if 1 <= p <= n]


def cmd_scan(args):
    for deck in args.decks:
        pdf = to_pdf(deck, args.out)
        d = fitz.open(pdf)
        empty = []
        lines = []
        for i, page in enumerate(d):
            t = " ".join(page.get_text().split())
            if len(t) < 40:
                empty.append(i + 1)
            lines.append(f"  p{i + 1}: {t[:100]}")
        print(f"== {deck}  ({d.page_count} pages)")
        print(f"   image-only or near-empty text: {empty if empty else 'none'}")
        print("\n".join(lines))


def cmd_grid(args):
    from PIL import Image
    pdf = to_pdf(args.deck, args.out)
    d = fitz.open(pdf)
    pages = parse_pages(args.pages, d.page_count) if args.pages else list(range(1, d.page_count + 1))
    out = pathlib.Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stem = pathlib.Path(args.deck).stem
    for start in range(0, len(pages), args.per):
        chunk = pages[start:start + args.per]
        ims = []
        for p in chunk:
            pix = d[p - 1].get_pixmap(dpi=args.dpi)
            ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        w = max(i.size[0] for i in ims)
        h = max(i.size[1] for i in ims)
        cols = min(args.cols, len(ims))
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (w * cols, h * rows), "white")
        for k, im in enumerate(ims):
            sheet.paste(im, ((k % cols) * w, (k // cols) * h))
        name = out / f"{stem}_p{chunk[0]}-{chunk[-1]}.png"
        sheet.save(name)
        print(f"{name}  (pages {', '.join(map(str, chunk))}, left to right, top to bottom)")


def cmd_topdf(args):
    print(to_pdf(args.deck, args.out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("decks", nargs="+"); s.add_argument("--out", default=None); s.set_defaults(f=cmd_scan)
    g = sub.add_parser("grid"); g.add_argument("deck"); g.add_argument("--pages", default="")
    g.add_argument("--out", required=True); g.add_argument("--dpi", type=int, default=75)
    g.add_argument("--cols", type=int, default=3); g.add_argument("--per", type=int, default=6); g.set_defaults(f=cmd_grid)
    t = sub.add_parser("topdf"); t.add_argument("deck"); t.add_argument("--out", required=True); t.set_defaults(f=cmd_topdf)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
