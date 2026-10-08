# Review, QA and publishing

## 1. Reviewing an agent's fragment (required before it goes live)

Read the whole fragment, not a skim; you are vouching for it. Then:

1. **Start from the hand-back's "unsure" list.** Render those slide pages and decide each case.
2. **Spot-check the formulas** that carry the chapter (the ones an exam would ask) against
   rendered slides: render 6 pages per grid with `scripts/render_slides.py grid` and compare.
3. **Recompute every worked example and check answer** (a few lines of Python is faster than
   mental arithmetic). Agents are usually right; the misses are arithmetic in answers.
4. **Notation across lessons.** Grep all fragments for the key symbols. The same symbol must mean
   the same thing everywhere (a real case: one lesson used ε_m for 2⁻⁵², another for the rounding
   bound 2⁻⁵³; fix by relabelling one, and say so in the glossary).
5. **Policy.** Graded homework that is not yet due gets hints, not finished answers; background
   content is labelled; slide typos are flagged in the text, not silently corrected.
6. Glance at the script for hard-coded colors, global ids or `document.getElementById` on bare ids.

## 2. Automatic checks

```bash
python3 <skill>/scripts/check_site.py <lessons dir>          # structure, qids, TeX '<', script syntax
```

For a shared numerical engine, test it in node before figures depend on it. Stub the DOM the
shell's `Viz` needs and eval the scripts:

```js
// test.js — node test.js viz.js _engine.js
global.window = global; global.document = { documentElement: {} };
global.getComputedStyle = () => ({ getPropertyValue: () => '' });
global.MutationObserver = class { observe() {} }; global.matchMedia = () => ({ addEventListener() {} });
const fs = require('fs'); eval(fs.readFileSync(process.argv[2], 'utf8')); eval(fs.readFileSync(process.argv[3], 'utf8'));
// …assert identities: brute force vs closed form, row sums = 1, limits, etc.
```

Extract `viz.js` from the shell: the `<script>` whose body starts with `/* ===… Viz:`.

## 3. Browser QA

Serve the folder (the browser pane does not run file:// pages properly):

```bash
cd <lessons dir> && python3 -m http.server 8765 --bind 127.0.0.1    # run in the background
```

Open `http://localhost:8765/<output>.html?v=N` (bump `v` to defeat the cache after each build).
Then run in the page:

```js
// every lesson: charts drawn, MathJax clean
const out = [];
for (const id of [...document.querySelectorAll('section.lesson')].map(s => s.id)) {
  location.hash = id; await new Promise(r => setTimeout(r, 800));
  const sec = document.getElementById(id), cv = [...sec.querySelectorAll('canvas')];
  out.push(`${id}: canvases ${cv.length}, zero-width ${cv.filter(c => c.width === 0).length}, ` +
           `mjx-errors ${sec.querySelectorAll('mjx-merror,[data-mjx-error]').length}`);
}
out.join(' | ')
```

Then read console errors. For phone width, emulate 375 px **and inject a viewport meta first**
(the local file has none; the published page gets one from the artifact skeleton), then measure
horizontal overflow per lesson:

```js
const m = document.createElement('meta'); m.name = 'viewport';
m.content = 'width=device-width,initial-scale=1'; document.head.appendChild(m);
await new Promise(r => setTimeout(r, 800));
const o = [];
for (const id of [...document.querySelectorAll('section.lesson')].map(s => s.id)) {
  location.hash = id; await new Promise(r => setTimeout(r, 600));
  o.push(id + ':' + (document.documentElement.scrollWidth - document.documentElement.clientWidth));
}
o.join(' ')     // all zeros is the goal; find offenders with getBoundingClientRect().right > clientWidth
```

Take one or two screenshots of the figures that matter most (desktop and phone), not every page.
Reset the viewport emulation when done and stop the local server.

## 4. Publishing

- Build only reviewed lessons: `python3 build.py --only l0,l3-1,...`. Publish early so the student
  can start; later publishes of the same file path update the same URL.
- First publish: `Artifact` with `file_path` = the built page, `icon: "book"`, a one-sentence
  `description`, and `capabilities: {"db": {}}` (load the artifact-capabilities skill first if it
  is not loaded). Redeploys: same `file_path`, omit `icon` and `capabilities` so they carry over.
- Functional check once after the first publish: `ArtifactData` `list` on collection `checks`
  (empty is fine; it proves the store is reachable).
- Agents may run `build.py` and overwrite the output with unreviewed fragments. Always rebuild
  with `--only` yourself right before a publish.
- Record the artifact URL, the lessons folder, and the data layout in the student's tracker or
  memory, so later sessions can read the marks.

### Self-check data layout

- Collection `checks`, doc id = question id (`l3-4-q3`), fields `mark` (`got` | `shaky` |
  `missed`), `lesson`, `topic`, `at` (ISO time).
- Collection `lessons`, doc id = lesson id, fields `done`, `at`.

When the student logs a study session, `ArtifactData list` both collections and turn `shaky` /
`missed` topics into the weak-point list (re-study, then re-check two sessions later).

## 5. Pitfalls that cost time before

| Symptom | Cause | Fix (already in the shell where noted) |
|---|---|---|
| Chinese or "·" garbled locally | no charset when served by http.server | `<meta charset="utf-8">` at the top of the shell (in shell) |
| Lesson heading hidden under the top bar after a link | native anchor scroll | `scroll-margin-top` on sections (in shell) |
| Blank canvases | figure built while its section was hidden (width 0) | build figures inside `registerLesson` (runs on first open) |
| Every chart blank during QA in a background browser tab | `requestAnimationFrame` is paused in hidden tabs | the router falls back to `setTimeout` when hidden (in shell) |
| Math fonts missing | KaTeX/CHTML fonts blocked by the artifact CSP | MathJax 3 `tex-svg.js` from jsdelivr (in shell) |
| Page scrolls sideways on phones | long inline math | inline `mjx-container` gets `max-width:100%; overflow-x:auto` under 700 px (in shell) |
| `soffice` conversion "fails" silently | `timeout` is not on macOS; profile lock | call soffice directly with `-env:UserInstallation=file://<tmpdir>` (render_slides.py does this) |
| Published page shows unreviewed drafts | an agent rebuilt the output | rebuild with `--only` right before publishing |
| A "12 lessons" text is wrong after an early publish | hard-coded counts | let JS count lessons; no counts in copy |
