# Brief template for chapter-writing agents

Spawn one background agent per chapter (2–3 lessons each), all in the same turn, after
`src/shell.html`, `build.py`, `course.json` and `AUTHORING.md` exist. Fill every `<…>`. The parts
that matter most: exact page ranges, the list of image-only pages, the course conventions, the
homework policy, and the figure requirements. A vague brief produces a generic lesson.

```text
You are writing <N> HTML lesson fragments for a student's exam-prep site (<course>, <institution>).
Course folder: <abs path>. Lesson site folder: <abs path>/lessons.

FIRST read <abs path>/lessons/AUTHORING.md completely and follow it exactly (fragment format,
teaching rules, course conventions, Viz toolkit, checks). Skim lessons/src/shell.html for the CSS
classes and the Viz API. Do not edit shell.html, build.py or course.json.

Your lessons (write exactly these files):
1. lessons/src/<id>.html — section id "<id>", data-ch="<ch>", data-short="<short>",
   data-title="<title>", data-date="<day>", data-minutes="<min>". Source: <deck> p<a>–<b>:
   <one line per slide group: what each page range covers>.
2. …

Sources: <abs path to deck(s)>. Pages <list> have no text layer, and others keep equations in
images: render every page you use with `python3 <skill>/scripts/render_slides.py grid <deck>
--pages <a-b> --out <scratch dir>` and read the PNGs. Base every formula on the slides.

Exam context: <format>. Instructor focus: <topics>. For this chapter that means: <the 2–4 things
an exam would most likely ask, e.g. "derive X", "count Y", "compare A vs B">.

Related coursework: <homework files, which problems, due/graded or already submitted, past exams>.
Policy: <graded and not yet due → method + hints only; submitted or past exam → may be fully worked>.

Required interactive figures (at least these; more welcome):
- <id>: (a) <concept → interaction, e.g. "step through back substitution one unknown at a time
  with a running count of operations matching the formula">. (b) <…>.
- <id>: (a) <…>. (b) <…>.

Write for <background>. Every lesson needs: eyebrow with "Slides: <deck> p…", h1, one-sentence
idea, roadmap, glossary with <native language> column, sections in slide order (intuition →
statement → "In words" → worked example), Hard-point boxes where reasoning is hard, at least one
Exam-angle box, 5–8 .check questions with data-qid "<id>-q1"… and specific data-topic labels, and
a final cheat-sheet key box.

When done: run `python3 <skill>/scripts/check_site.py <abs path>/lessons`, run
`python3 build.py --only <ids>`, re-check every formula against the slide images, and reply with:
file paths, each figure and what it shows, what you labelled background, and any slide content you
were unsure about (quote page numbers). Do not publish anything and do not edit other files.
```

Why each part is there:

- **Exact page ranges and image-only pages**: agents skip what they cannot see. Naming the pages
  that need rendering is what stops invented formulas.
- **Conventions in AUTHORING.md, not in each brief**: one source of truth prevents two lessons
  defining the same symbol differently.
- **Named figures**: "add two figures" yields decoration; "step through X showing Y" yields
  teaching.
- **The hand-back report**: "unsure slide content" is where the agent tells you about typos,
  ambiguous handwriting and things it had to interpret. Read that list first when reviewing.
