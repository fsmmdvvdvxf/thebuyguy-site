# ORDAFORMA — booking page

Public scheduling page for 30-minute software setup calls.
Live at https://fsmmdvvdvxf.github.io/thebuyguy-site/booking/

## How it works

- `index.html` — the page. Reads `slots.json`, renders open times in the
  visitor's own time zone, and POSTs a booking to a form relay that emails
  ordaformaofficial@gmail.com.
- `slots.json` — generated availability. Times are stored as **UTC instants**
  so nothing shifts across the Nov 1 2026 DST change. Regenerated on a schedule
  from the real Google Calendar; a slot that is busy on the calendar never
  appears here.
- `config.js` — the only file to edit to change how bookings are delivered.
  Switch `PROVIDER` between `"web3forms"` and `"formsubmit"`; nothing else changes.
This directory is served by the GitHub Pages site already enabled on this repo.
No workflow is involved: pushing to `main` publishes it. The root of this repo
(`index.html`, `privacy.html`) belongs to TheBuyGuy and is untouched.

## Deliberate choices

- **No booking data is ever written to this repo.** It is public. Names and
  emails live only in Gmail and Google Calendar, both private.
- Slot times are UTC in the file and localised in the browser.
- `slots.json` is fetched with `cache: no-store` plus a cache-buster, because a
  stale CDN copy would widen the window in which two people can book the same slot.
- The glass styling has a `@supports` fallback to opaque white, so browsers
  without `backdrop-filter` get a readable card rather than a transparent one.

## Regenerating slots by hand

    python3 generate_slots.py <calendar-events.json> slots.json

Commit the result; the push redeploys the page.
