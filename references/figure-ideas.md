# Figure ideas by kind of content

A figure earns its place when the student can *do* something with it that shows the idea: move a
knob and watch a quantity respond, step through a procedure, compare two methods side by side, or
check a theorem numerically. Pick the interaction from what the concept is about.

| Concept type | Interaction that teaches it | Examples that worked |
|---|---|---|
| A tuning knob (λ, h, k, α, learning rate) | Slider over the knob; the fit and a score update; mark the optimum | smoothing λ from interpolation to straight line; bandwidth with bias²/variance/MISE curves |
| An identity or theorem | Compute both sides live and show they match | brute-force leave-one-out vs the shortcut formula, equal to 1e-12; ∫f''² = ∫g''² + ∫h''² with the cross term printed as 0 |
| A step-by-step algorithm | "Next step" button, highlight what each step reads and writes, running operation count vs the closed form | back substitution, Gaussian elimination into L and U, Cholesky entry by entry, AdaBoost round by round, gradient descent |
| A matrix / operator | Heat map of entries; click a row to see its weights | smoother matrix rows as local weights |
| Geometry of a transform | Unit circle/ball → image under the map, with sliders for entries | SVD ellipse, matrix norms as max stretch |
| Randomness / sampling | Seeded "new sample" and "draw 100 more" buttons; show the running average next to the theory curve | bootstrap out-of-bag fraction → 1/e; bagging B trees |
| Finite precision | Short-digit arithmetic or a toy number system you can resize | 3-digit pivoting disaster; toy floating-point line with gap doubling |
| Building blocks of a model | Show the parts and their sum | weighted B-spline bumps summing to the fit; a basis function built from its two parents |
| Choosing a model by validation | Fold-by-fold view plus the CV curve with its minimum | K-fold CV for pruning α |

Non-quantitative subjects use the same principle with HTML and CSS instead of plots:

- **History / social science:** a draggable timeline; toggling actors shows which events they
  caused; "what changed" sliders across periods.
- **Biology / chemistry:** a pathway or mechanism stepper (each click advances one reaction and
  highlights what is consumed and produced); dose–response or Michaelis–Menten curves with sliders.
- **Law / policy:** a decision tree the student walks with a case's facts; side-by-side rule
  comparison that highlights the differing clause.
- **Languages:** sentence builders that recolour by grammatical role; conjugation tables that
  hide one cell at a time for recall.
- **Programming / CS:** code stepper with a variable table; data-structure animations
  (stack, heap, tree rotations) with an operation counter.
- **Economics:** supply/demand or IS–LM curves with shift sliders and the equilibrium readout.

Keep every figure seeded and deterministic, give it a one-to-two sentence caption that says what
to try, and put live numbers in a `.readout` row so the student can copy them into notes.
