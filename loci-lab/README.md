# Loci Lab

Seven adaptive memory drills, in one static page:

- **Flash** — whole-group apprehension in a single fixation, with a 3-down/1-up staircase
  (Levitt 1971) that converges on the exposure you get ~79% right.
- **Span** — serial recall with a climbing load, scored strictly and item-only.
- **Mental Math** — calculation with a three-place "shelf" for intermediates and a refresh beat.
- **Balance** — linear equations animated the way you move them in your head: the operation
  drops in under both sides, pushes up into the terms, they merge, the equation settles.
- **Patterns** — SM-2 spaced repetition over algebraic forms and the Major System pegs.
- **Verbatim** — a passage in fading stages: whole phrase, first letters, gaps, blank.
- **Grid** — Schulte tables and flash matrices for peripheral attention.

Progress, benchmarks, trend charts, a training calendar and a rotatable 3D performance surface
live in the Progress tab.

## Running it

It is one file. Open `index.html`, or serve the folder:

```
npx http-server .
```

## Install to a home screen

- **iOS Safari** — Share → Add to Home Screen
- **Android Chrome** — ⋮ → Install app

It launches standalone (no browser chrome) and works offline.

## Data

Training data is stored in this browser via `localStorage`. It never leaves the device.
Use **Progress → Export** for a backup and **Import** to restore or move it.
