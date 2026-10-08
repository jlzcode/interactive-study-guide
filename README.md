# interactive-study-guide

An agent skill that turns a folder of course materials (lecture slides, notes, homework, past exams)
into an **interactive study guide**: plain-language review lessons on one web page, ordered by what
the exam rewards, with interactive figures, step-by-step derivations, self-check questions and a
day-by-day study plan.

Built for students who need to learn a course fast, including those whose background is weaker
than the course assumes. Works for any subject: the first version was used for a graduate
statistics midterm (12 lessons, 85 self-checks, about 40 interactive figures).

## What you get

- **Lessons in study order.** The plan follows the exam's emphasis and your deadlines, not the
  chapter numbers. An optional Lesson 0 covers missing prerequisites.
- **Plain language first.** Every idea starts from intuition or a small example, then the formal
  statement, then the statement read aloud in words. Every symbol is defined at first use.
- **Hard points slowed down.** The steps students get stuck on are broken into numbered steps,
  each with a line saying why the step is allowed.
- **Interactive figures.** Sliders, step-through buttons and live readouts that show the idea, such
  as a smoothing parameter moving from overfitting to a straight line, or an algorithm solving one
  unknown at a time.
- **Checked against the source.** Each lesson cites the slide pages it covers; anything beyond the
  slides is labelled as background.
- **Self-checks that track weak spots.** Each question is marked Got it / Shaky / Missed. Shaky and
  Missed topics collect on the home page as the review list.
- **Exam angle and cheat-sheet lines** at the end of every lesson.
- Light and dark mode, phone-friendly, optional native-language glossary column.

## Requirements

- [Claude Code](https://claude.com/claude-code) or another agent that supports Agent Skills
  (`SKILL.md` format).
- Python 3 with [PyMuPDF](https://pymupdf.readthedocs.io/) and Pillow for reading slides:
  `pip install pymupdf pillow`
- [LibreOffice](https://www.libreoffice.org/) if your slides are `.pptx` / `.ppt` (converted to PDF).
- Node.js (optional) for the JavaScript syntax check.
- Publishing as a shareable page uses Claude's Artifacts. Without it, open the built `.html` file in
  a browser: everything works, and self-check marks are kept in that browser's local storage.

## Install

Clone into your skills folder:

```bash
git clone https://github.com/jlzcode/interactive-study-guide.git ~/.claude/skills/interactive-study-guide
```

Or download `interactive-study-guide.skill` from the Releases page and install it in Claude.

## Use

Point the agent at your course folder and say what you need, for example:

- "Make interactive study lessons from the slides in this folder. Midterm is Oct 14, closed book."
- "I haven't read any slides and my math background is weak. Teach me chapters 2–4 for the final."
- "把这门课做成 HTML 复习材料，用简单详细的语言教我。"

The skill then gathers the brief, reads the slides (including image-only pages), plans the lessons,
writes the first ones itself, delegates the remaining chapters to helper agents in parallel, reviews
every lesson against the slides, runs checks, and publishes. It publishes early so you can start
studying the same day.

## How it is organized

| Path | Purpose |
|---|---|
| `SKILL.md` | The workflow the agent follows (10 steps, with the reasoning behind each) |
| `assets/shell.html` | Page template: design, chart toolkit, math rendering, navigation, self-check storage |
| `assets/build.py` | Assembles lesson fragments into one page (`--only` for partial builds) |
| `assets/course.example.json` | Example configuration with every field filled in |
| `assets/example-lesson.html` | A complete example lesson at the expected quality |
| `references/authoring-guide.md` | Teaching rules and lesson format given to every lesson writer |
| `references/agent-brief.md` | Prompt template for chapter-writing helper agents |
| `references/figure-ideas.md` | Interactive figure ideas by concept type and by subject |
| `references/qa-and-publish.md` | Review checklist, QA snippets, publishing steps, known pitfalls |
| `scripts/render_slides.py` | Scan decks for image-only pages; render pages to image grids; convert PPTX |
| `scripts/check_site.py` | Static checks on lessons and a syntax check of the built page |

A generated project looks like this:

```
your-course/lessons/
  course.json      titles, exam date, lesson order, study plan
  AUTHORING.md     the rules every lesson writer follows
  build.py
  src/shell.html
  src/l0.html, src/l3-1.html, ...
  Lessons.html     the built page
```

## Course materials and copyright

The skill reads your course files locally and cites page numbers; it does not copy slides into the
lessons. Do not commit your instructors' slides, homework or exams to a public repository.

## License

[MIT](LICENSE)
