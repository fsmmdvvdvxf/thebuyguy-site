#!/usr/bin/env python3
"""Turn a Google Calendar list_events dump into slots.json for the booking page.

Usage: python3 generate_slots.py <events.json> [out.json]

Times are computed in America/Chicago (DST-aware via zoneinfo) and emitted as
UTC instants, so the page renders correctly across the Nov 1 2026 DST change.
"""
import json, sys
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chicago")
UTC = ZoneInfo("UTC")

SLOT_MINUTES   = 30
LEAD_HOURS     = 24   # no bookings inside this window
HORIZON_DAYS   = 14
BUFFER_MINUTES = 15   # gap required after any preceding event

# weekday (Mon=0) -> list of (start_minute, end_minute) local wall-clock windows
PATTERN = {
    0: [(780, 840), (1035, 1095)],           # Mon 1:00-2:00p, 5:15-6:15p
    1: [(705, 810), (1020, 1080)],           # Tue 11:45a-1:30p, 5:00-6:00p
    2: [(1140, 1230)],                       # Wed 7:00-8:30p
    3: [(1050, 1095), (1140, 1230)],         # Thu 5:30-6:15p, 7:00-8:30p
    4: [(780, 1020)],                        # Fri 1:00-5:00p
    5: [(780, 960)],                         # Sat 1:00-4:00p
}


def parse_busy(events):
    """Timed events only. All-day entries (Due:/pinned assignment markers) are
    deadlines, not occupied time -- treating them as busy would blank whole days."""
    busy = []
    for e in events:
        s, t = e.get("start", {}), e.get("end", {})
        if not s.get("dateTime") or not t.get("dateTime"):
            continue
        busy.append((
            datetime.fromisoformat(s["dateTime"]).astimezone(UTC),
            datetime.fromisoformat(t["dateTime"]).astimezone(UTC),
            e.get("summary", ""),
        ))
    return busy


def main():
    src = json.load(open(sys.argv[1]))
    events = src.get("events", src if isinstance(src, list) else [])
    busy = parse_busy(events)

    now = datetime.now(UTC)
    earliest = now + timedelta(hours=LEAD_HOURS)
    latest = now + timedelta(days=HORIZON_DAYS)

    slots, skipped = [], 0
    day = now.astimezone(TZ).date()
    for _ in range(HORIZON_DAYS + 2):
        for win_start, win_end in PATTERN.get(day.weekday(), []):
            m = win_start
            while m + SLOT_MINUTES <= win_end:
                local = datetime.combine(day, datetime.min.time(), TZ) + timedelta(minutes=m)
                start = local.astimezone(UTC)
                end = start + timedelta(minutes=SLOT_MINUTES)
                m += SLOT_MINUTES

                if start < earliest or start > latest:
                    continue
                # overlap, with a buffer after any preceding event
                clash = any(
                    start < (b_end + timedelta(minutes=BUFFER_MINUTES)) and end > b_start
                    for b_start, b_end, _ in busy
                )
                if clash:
                    skipped += 1
                    continue
                slots.append({
                    "id": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "start_utc": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                })
        day += timedelta(days=1)

    slots.sort(key=lambda s: s["start_utc"])
    out = {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timezone": "America/Chicago",
        "slot_minutes": SLOT_MINUTES,
        "lead_time_hours": LEAD_HOURS,
        "slots": slots,
    }
    dest = sys.argv[2] if len(sys.argv) > 2 else "slots.json"
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    print(f"{len(slots)} slots -> {dest}  ({skipped} dropped for conflicts, {len(busy)} busy events)")


if __name__ == "__main__":
    main()
