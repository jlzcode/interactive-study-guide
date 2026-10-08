# Authoring guide for the lesson fragments

Copy this file into the project as `lessons/AUTHORING.md`, fill in the two sections marked
**[fill in]**, and give it to every agent that writes a lesson. It is the contract that keeps a
dozen fragments written by different hands looking and teaching the same way.

All lessons live in one page built by `python3 build.py` from `src/shell.html` plus one fragment
per lesson in `src/<lesson-id>.html`. The shell holds the CSS, the `Viz` chart toolkit, MathJax,
the router and the self-check storage. **Do not edit `src/shell.html`, `build.py` or
`course.json`.** Write only your own fragment files.

## The reader [fill in]

- Who: <name>, taking <course>. Background: <e.g. high-school math only / strong programming,
  weak proofs>. Has <not> read the slides yet.
- Language: lessons in <English>; glossary adds a <中文> column. If English is the reader's second
  language: plain, short, literal sentences, no idioms.
- Exam: <date, length>, <closed/open book>, <cheat sheet?>, <handwritten?>. So the lessons must
  build the ability to <reproduce definitions and derivations by hand / apply methods in code /
  write essays from memory>.
- Instructor's stated focus: <topics>.

## Course conventions and notation [fill in]

List every convention that differs from textbooks, with the slide page that proves it, and every
notation decision made once for the whole site (one symbol, one meaning). Examples of the kind of
thing that belongs here:

- "FLOPs count only × and ÷ (lect2 p8)" — a textbook count differs by 2×.
- "κ for the variance has a leading factor 2 (lect1 p35)".
- "ε_m means the rounding bound ≈ 2⁻⁵³ (lect1 p22); 2⁻⁵² is written ε_max".

## Teaching rules

1. **Intuition first.** Start every idea from a picture, an everyday analogy or a tiny numeric
   example, *then* the formal statement, then read the statement aloud in a `<p class="words">`
   line. Readers who cannot parse notation can still follow the words line.
2. **Define every symbol and term at first use.** Assume nothing beyond the stated background.
   A one-line reminder costs little; an undefined symbol stops the reader cold.
3. **Hard points get a `.hard` box** with an `<ol class="steps">` derivation or argument where
   every step has a `<p class="because">` line saying why the step is allowed. Be generous exactly
   where students get stuck: these boxes are what the reader copies out by hand.
4. **Accuracy beats coverage.** Every formula, definition, date or claim must match the course's
   own materials and notation. Many slides are images with no text layer: render them
   (`scripts/render_slides.py grid ...`) and read them as images. Cite pages inline, e.g.
   "(lect2 p14)". Anything not in the course materials is labelled
   "(background, not on the slides)". Report slide typos instead of silently fixing them, and say
   in the lesson what the correct reading is.
5. **Follow the conventions section above.** If you need a symbol that is not listed, use the
   slides' notation and mention it in your hand-back report.
6. **Tie practice to real course materials** (homework, past exams, problem sets). For graded
   homework that is not yet due, teach the method and give a structured hint, not a finished
   answer the student could submit. Past exams and already-submitted homework may be fully worked.
7. **Glossary** table with the reader's native-language gloss when one is configured
   (Term | 中文 | Plain meaning). Everything else stays in the lesson language.
8. **Copy style:** active voice, short sentences, no em-dash asides, no "not X but Y" framing, no
   filler ("it's worth noting"), no emoji.

## Fragment format

```html
<section class="lesson" id="l2-1" data-ch="2" data-short="2.1" data-title="Short title"
         data-date="Wed 10/7" data-minutes="90">
  <div class="eyebrow"><span><b>Chapter 2</b> · Lesson 2.1</span><span>Wed 10/7</span><span>~90 min</span><span>Slides: lect2 p1–26</span></div>
  <h1>Full title</h1>
  <p class="idea"><span class="lbl">In one sentence</span><span class="m">The lesson in one sentence.</span></p>

  <h2>What you will be able to do</h2>
  <ul class="roadmap"><li><b>Verb</b> concrete outcome.</li> … 3–5 items …</ul>

  <h2>Words you need</h2>
  <div class="tablewrap"><table class="glossary"><thead><tr><th>Term</th><th>中文</th><th>Plain meaning</th></tr></thead><tbody>
    <tr><td>term</td><td>术语</td><td>Plain meaning.</td></tr>
  </tbody></table></div>

  <h2>1. Section title (lect2 p3–5)</h2>
  <p>Intuition first …</p>
  \[ x_n = b_n / u_{nn} \]
  <p class="words">The formula read aloud in plain words.</p>
  <div class="box example"><span class="tag">Worked example</span> … </div>
  <div class="box hard"><span class="tag">Hard point · slow down</span>
    <ol class="steps"><li><p>Step.</p><p class="because">Why the step is allowed.</p></li></ol>
  </div>

  <figure class="viz" id="l2-1-fig1">
    <div class="vtitle">Figure title</div>
    <div class="controls"></div>
    <div class="canvas-host"></div>
    <div class="readout" id="l2-1-fig1-read"></div>
    <figcaption>What to look at and what to try.</figcaption>
  </figure>

  <div class="box exam"><span class="tag">Exam angle</span> … likely question + what a full answer contains … </div>

  <h2>Check yourself</h2>
  <div class="check" data-qid="l2-1-q1" data-topic="Specific topic label">
    <span class="tag">Check yourself</span>
    <p>Question. Answer on paper first.</p>
    <details><summary>Show answer</summary><div> … full answer … </div></details>
  </div>
  … 5–8 checks …

  <h2>Cheat-sheet lines</h2>
  <div class="key"><span class="tag">Copy to your cheat sheet</span> … the 4–8 facts worth carrying … </div>
</section>
<script>
registerLesson('l2-1', function (root) {
  // build the figures here; runs the first time the lesson is opened (the section is visible then)
});
</script>
```

Other pieces: `<div class="box why"><span class="tag">Why this matters</span>…</div>`,
`<div class="key"><span class="tag">Key result</span>…</div>`, `<div class="tablewrap"><table>…</table></div>`,
`<pre><code>…</code></pre>` for short code, `.legend` with `<span style="--sw:var(--c2)">label</span>` items.
For a complete fragment at the expected quality, read the skill's `assets/example-lesson.html`.

- The shell adds the "Mark lesson done" button and prev/next links; do not add your own.
- The shell adds Got it / Shaky / Missed buttons to every `.check[data-qid]`. `data-qid` must be
  unique (`<lessonid>-q<n>`); `data-topic` is the label in the weak-spot list, so make it specific
  ("FLOPs for back substitution", not "Question 3").
- Prefix every element id with the lesson id. Look up elements with `root.querySelector`, never
  `document.getElementById` on a bare id, so lessons cannot collide.
- Do not hard-code counts that change ("twelve lessons").

## Math

MathJax 3 with SVG output is loaded (fonts are inlined as paths, so no font files are needed).
Inline `\( … \)`, display `\[ … \]`. In HTML write `&lt;` or `\lt` instead of a bare `<` inside
TeX, and `&amp;` for `&` in `aligned`/matrix environments. Never put TeX inside text that
JavaScript rewrites later; live numbers go in plain spans.

## Figures: the `Viz` toolkit (global, defined in the shell)

Every lesson needs **at least two interactive figures that teach something from the materials**
(a slider, a step-through, a hover readout, a "new sample" button). Decoration does not count.
Draw only with `Viz` (or plain HTML styled with `var(--token)`), and take every color from the
theme tokens so light and dark mode both work. No hex colors, no other libraries.

```js
const host = root.querySelector('#l2-1-fig1 .canvas-host');
const ctrl = root.querySelector('#l2-1-fig1 .controls');
let n = 5;
Viz.slider(ctrl, { id: 'l2-1-n', label: 'n', min: 2, max: 12, step: 1, value: n,
                   fmt: v => v.toFixed(0), onInput: v => { n = v; fig.render(); } });
Viz.seg(ctrl, ['Option A', 'Option B'], i => { mode = i; fig.render(); }, 0);
const fig = Viz.figure(host, { height: 320,            // or height: w => (w < 560 ? 420 : 300)
  draw(ctx, w, h) {
    const P = Viz.frame(ctx, w, h, { xlim: [0, 1], ylim: [-1, 1], pad: { l: 46 } });
    P.axes({ xlabel: 'x', ylabel: 'y' });            // also xticks, yticks, fmtx, fmty, grid:false
    P.fn(x => Math.sin(6 * x), Viz.color(0), 2);      // Viz.color(0..7) = series colors
    P.points(xs, ys, Viz.color('ink'), 3.5, { alpha: 0.7, hollow: false });
    P.line(xs, ys, Viz.color(1), 2, [5, 4]);          // dashed
    P.area(xs, 0, ys, Viz.color(2), 0.15);
    P.vline(0.5, Viz.color('muted')); P.hline(0, Viz.color('muted'));
    P.rect(x0, y0, x1, y1, Viz.color(3), 0.3); P.segment(xa, ya, xb, yb, col, 2);
    P.text('label', x, y, { col: Viz.color('muted'), align: 'center', size: 12, mono: true });
    P.clip(() => { /* drawing clipped to the plot area */ });
    // P.X(x)/P.Y(y): data → pixels; P.Xinv(px)/P.Yinv(py): pixels → data (pointer events)
  } });
fig.canvas.addEventListener('pointermove', e => { /* use P.Xinv(e.clientX - rect.left) */ });
```

Token names for `Viz.color('<name>')`: `ink`, `muted`, `rule`, `paper`, `sheet`, `accent`, `red`,
`green`, `amber`, `hl`, `accent-soft`, `red-bg`, `green-bg`, `amber-bg`, `code-bg`.

Helpers: `Viz.rng(seed)` → `{unif(), normal()}` (seeded, so figures are reproducible);
`Viz.LA` → `zeros(n,m)`, `T(A)`, `mul(A,B)`, `mulv(A,v)`, `solve(A,B)` (partial pivoting; B vector
or matrix), `inv(A)`; `Viz.bsplineAll(x, T, r)`, `Viz.knotVector(a,b,interior,r)`;
`Viz.niceTicks(lo,hi,n)`. Matrices are arrays of rows.

If several lessons need the same computational engine (a smoother, a simulator, a parser), write
it once as `src/_<name>.js` defining a global, and put `/*__INCLUDE:_<name>.js__*/` at the top of
the first lesson's `<script>`. Test it numerically in node before any figure depends on it.

## Checks before you hand back

1. Run `python3 <skill>/scripts/check_site.py <lessons dir>`; fix every error it reports for your
   fragments.
2. Run `python3 build.py --only <your ids>`. Do not publish anything.
3. Re-read every formula and number against the rendered slide image it came from; recompute
   every worked example.
4. Hand back: file paths, each figure and what it shows, everything you labelled background, and
   any slide content you were unsure about (with page numbers).
