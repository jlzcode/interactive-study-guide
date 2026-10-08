---
name: interactive-study-guide
description: Build an interactive study guide, a set of plain-language HTML review lessons that teaches a course from its own materials (lecture slides, notes, homework, past exams) for exam prep, published as one private Artifact with interactive figures, step-by-step derivations, self-check questions that record the student's weak spots, and a day-by-day study plan. Use this whenever a student asks to be taught a course or a set of chapters ("teach me this course", "make HTML lessons / study material / review pages from my slides", "I haven't read the slides", "my background is weak, explain it simply", "help me prepare for the midterm/final from these lectures"), or wants a study plan turned into actual lessons, in any subject (statistics, math, CS, physics, biology, economics, law, history, languages). Also use for Chinese requests such as "做成HTML复习材料", "用简单详细的语言教我", "帮我做讲义/课件", "按计划给我写课". Not for a single quick explanation, a one-page cheat sheet, or grading homework.
---

# Interactive study guide

Turn a folder of course materials into review lessons a struggling student can actually learn
from: one web page, one lesson per study session, in the order the exam rewards, each lesson
checked against the instructor's own slides. The page records which self-check questions the
student marks Shaky or Missed, so later coaching works from evidence instead of guesses.

This skill grew out of a statistics midterm (B616): 12 lessons, 85 self-checks, about 40
interactive figures, written in one long session with three helper agents. The bundled shell,
build script and authoring guide are the parts that made that work repeatable.

## What you produce

```
<course folder>/lessons/
  course.json          titles, exam date, lesson order, chapter names, study plan
  AUTHORING.md         the contract every lesson writer follows (from references/authoring-guide.md)
  build.py             assembles the page
  src/shell.html       design, chart toolkit, MathJax, router, self-check storage (from assets/)
  src/l0.html …        one fragment per lesson
  <Output>.html        the built page, published as an Artifact with the `db` capability
```

## Workflow

1. Gather the brief
2. Inventory and read the materials
3. Plan the lessons
4. Set up the project
5. Write the first lessons yourself
6. Delegate the remaining chapters
7. Review every fragment
8. QA
9. Publish early, publish again
10. Hand off and keep coaching

Reply to the user in their language; write the lessons in the language they asked for.

### 1. Gather the brief

Most of it is usually in the conversation, the course folder or memory; ask only for what is
missing, in one message. You need:

- **Materials**: where the slides, notes, homework and past exams are.
- **Exam**: date and time, length, closed or open book, cheat sheet, handwritten or on a computer.
  This decides what every lesson trains: reproducing derivations by hand, applying methods in
  code, or writing arguments from memory. If nothing tells you, ask this one question.
- **Instructor's hints** about scope ("splines, CV, matrix decomposition will be on it").
- **The student**: background (a weak background calls for a Lesson 0), language, and whether a
  native-language gloss column helps.
- **Deadlines inside the plan** (homework due in three days changes the lesson order) and a
  daily time budget (default 2–2.5 h on weekdays, 3 h on weekends).

### 2. Inventory and read the materials

- Run `python3 scripts/render_slides.py scan <deck> …` on every deck. It reports the page count,
  the first words of each page (your page map), and the pages with no text layer. Those pages
  hold equations or diagrams as images and must be read as images, or the lessons will contain
  invented formulas.
- When a deck exists in two versions (e.g. `lect3.pdf` and a newer `lect3_new.pptx`), teach from
  the newer one and note what it adds.
- Read every page you will teach from: `render_slides.py grid <deck> --pages a-b --out <dir>`,
  6 pages per image. Do not rely on an older study guide or a filename to know what a deck says.
- Write down every **course convention** that differs from textbooks, with its page (for example
  "FLOPs count only × and ÷, lect2 p8"), and settle notation once ("ε_m is the rounding bound;
  2⁻⁵² is ε_max"). Check memory for conventions already discovered in earlier sessions.
- Note each homework and past exam and its status: graded and not yet due, or already submitted.

### 3. Plan the lessons

- **Order by what the exam rewards and by deadlines, not by chapter number.** The chapter the
  instructor stressed, and the one a homework due this week depends on, come first. Tell the
  student the reason in one line, since it departs from the syllabus order.
- **Add Lesson 0** when the background is thin: only the prerequisite tools used everywhere in the
  course (for the statistics course: reading Σ and subscripts, slope and bending, minimizing by
  setting a derivative to zero, matrices, expectation, bias and variance).
- **Size**: one lesson is 60–120 minutes, about 10–25 slides, one chain of ideas. Ids are `l0`,
  `l<chapter>-<n>`.
- **Calendar**: one or two lessons a day, each day's practice tied to real coursework, mock exams,
  and two buffer days before the exam; schedule re-reviews of the hinted topics at +1, +3, +7 days.
- Write `course.json`; `assets/course.example.json` shows every field with real values.

### 4. Set up the project

```bash
mkdir -p "<course>/lessons/src"
cp <skill>/assets/shell.html "<course>/lessons/src/shell.html"
cp <skill>/assets/build.py "<course>/lessons/build.py"
cp <skill>/assets/course.example.json "<course>/lessons/course.json"        # then edit
cp <skill>/references/authoring-guide.md "<course>/lessons/AUTHORING.md"    # then fill the two [fill in] sections
```

The shell is a finished design: theme tokens for light and dark mode, the `Viz` canvas toolkit,
MathJax 3 (SVG output, which works under the Artifact CSP), a hash router, lesson-done buttons,
Got it / Shaky / Missed buttons on every check, a weak-spot list and the plan table on the home
page. It already meets the Artifact page contract, so do not redesign it per course; change the
words through `course.json`. Keeping one design across courses also means the student learns the
page once.

Everything is one page built from fragments for three reasons: the Artifact `db` capability is
reliable on the main page, the student gets a single URL, and fragments let several writers work
in parallel without editing the same file.

### 5. Write the first lessons yourself

Write Lesson 0 and the highest-priority chapter yourself. They set the standard the helper agents
will match, and the top chapter is where a mistake costs the student most. Read
`assets/example-lesson.html` (a complete fragment) and follow `AUTHORING.md`.

The parts of a lesson that do the teaching:

- intuition or a tiny numeric example first, then the formal statement, then the statement read
  aloud in plain words;
- every symbol and term defined at first use, at the stated background level;
- **Hard point** boxes for the steps students get stuck on, each step with a "Why" line;
- at least two interactive figures that teach something specific (see
  `references/figure-ideas.md`);
- an Exam-angle box: the likely question and what a full-credit answer contains;
- 5–8 self-checks with specific topic labels, and cheat-sheet lines at the end;
- slide page citations everywhere, and "(background, not on the slides)" on anything extra.

For computational subjects, put shared logic in `src/_<name>.js`, splice it into a lesson with
`/*__INCLUDE:_<name>.js__*/`, and test it numerically in node before a figure depends on it. A
figure that claims to demonstrate a theorem has to satisfy it; in B616 the leave-one-out demo
matched the shortcut formula to 15 digits before it shipped.

### 6. Delegate the remaining chapters

Spawn one background agent per remaining chapter (two or three lessons each), all in the same
turn, with the brief in `references/agent-brief.md`. The brief names exact page ranges, the
image-only pages, the exam focus for that chapter, the homework policy and the figures wanted.
Keep writing your own lessons while they run, and give the user a one-line status.

### 7. Review every fragment before it goes live

Read each agent-written fragment in full before it is published. You are vouching for it, and the
Artifact tool will not publish content you have not read. Follow `references/qa-and-publish.md`
§1: start from the agent's list of slide content it was unsure about, spot-check the key formulas
against rendered slides, recompute worked numbers, and grep for symbols that mean different
things in different lessons. In B616 the review caught a notation clash (ε_m used for two
different quantities) and confirmed a slide typo the agent had flagged.

### 8. QA

- `python3 scripts/check_site.py "<course>/lessons"`: structure, unique question ids, bare `<`
  inside TeX, colour tokens, and a JavaScript syntax check of the built page.
- Browser pass (`references/qa-and-publish.md` §3): serve the folder locally, open every lesson,
  confirm the charts drew and MathJax reported no errors, read the console, and measure sideways
  overflow at 375 px after injecting a viewport tag.

### 9. Publish early, publish again

As soon as the first day's lessons pass review, build only those (`python3 build.py --only l0,l3-1`)
and publish, so the student can start that day. The first publish takes `icon: "book"`, a
one-sentence description and `capabilities: {"db": {}}`. Later publishes of the same file path
update the same URL; omit icon and capabilities on those. Rebuild with `--only` right before
every publish, because an agent may have rebuilt the output with unreviewed drafts. After the
first publish, list the `checks` collection once with `ArtifactData` to confirm the store works.
Details: `references/qa-and-publish.md` §4.

### 10. Hand off and keep coaching

Tell the student, briefly: the link; what is ready and for which day; how to use the lessons (pen
and paper, answer before revealing, mark honestly); and what to report after a session. Record
the artifact URL, the lessons folder, the notation decisions and the data layout in memory or the
student's tracker.

In later sessions, read the `checks` and `lessons` collections before giving advice. Shaky and
Missed topics are the weak points: assign them for re-study, then re-check two sessions later. To
fix or extend a lesson, edit its fragment, rebuild and republish to the same URL.

## Scaling the workflow

- **One chapter or one lesson**: skip delegation; still use the shell and build script so the
  result can grow later.
- **No exam date**: omit `exam.iso`; the countdown disappears and the plan is optional.
- **Non-quantitative subjects**: the shell works unchanged (MathJax costs nothing when unused);
  pick figures from the HTML-based ideas in `references/figure-ideas.md`.
- **Short on time**: publish Lesson 0 and the first day's lessons first and grow the site day by
  day ahead of the plan.

## Files in this skill

| File | Use |
|---|---|
| `assets/shell.html` | Page template with `{{PLACEHOLDERS}}` filled from `course.json` |
| `assets/build.py` | Assembles `src/*.html` into the page; `--only` for partial builds; `/*__INCLUDE:…__*/` splicing |
| `assets/course.example.json` | Every config field with the B616 values |
| `assets/example-lesson.html` | A complete lesson fragment at the expected quality (B616 Lesson 0) |
| `references/authoring-guide.md` | Teaching rules, fragment format, math, `Viz` API; copy into the project as `AUTHORING.md` |
| `references/agent-brief.md` | Prompt template for chapter-writing agents |
| `references/figure-ideas.md` | Interactions that teach, by kind of concept and by subject |
| `references/qa-and-publish.md` | Review checklist, QA snippets, publishing steps, data layout, pitfalls |
| `scripts/render_slides.py` | `scan` decks, render page `grid`s, convert pptx with LibreOffice |
| `scripts/check_site.py` | Static checks plus a JavaScript syntax check of the built page |
