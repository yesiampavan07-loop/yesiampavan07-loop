#!/usr/bin/env python3
import json, datetime

with open("data/contributions.json") as f:
    data = json.load(f)

days = data["days"]
total = data["total_contributions"]
streak = data["current_streak"]
longest = data["longest_streak"]

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX = 11
GAP = 3
WEEKS = 53
DAYS_PER_WEEK = 7
PAD_L = 28
PAD_T = 20
PAD_B = 50
PAD_R = 10

W = PAD_L + WEEKS * (BOX + GAP) + PAD_R
H = PAD_T + DAYS_PER_WEEK * (BOX + GAP) + PAD_B

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(weeks=53)
date_to_day = {d["date"]: d for d in days}

grid = []
cur = start_date - datetime.timedelta(days=start_date.weekday())
for w in range(WEEKS):
    week = []
    for wd in range(DAYS_PER_WEEK):
        d = cur + datetime.timedelta(days=w * 7 + wd)
        ds = d.isoformat()
        info = date_to_day.get(ds, {"date": ds, "count": 0, "level": 0})
        week.append(info)
    grid.append(week)

month_labels = []
seen = set()
for w, week in enumerate(grid):
    for day in week:
        try:
            d = datetime.date.fromisoformat(day["date"])
            if d.month not in seen and d.day <= 7:
                seen.add(d.month)
                x = PAD_L + w * (BOX + GAP)
                month_labels.append((x, d.strftime("%b")))
        except:
            pass

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
parts.append(f'<rect width="{W}" height="{H}" rx="6" fill="#0d1117"/>')
parts.append('<style>')
parts.append('  .ml{font-family:"Courier New",monospace;font-size:9px;fill:#8b949e}')
parts.append('  @keyframes reveal{from{opacity:0}to{opacity:1}}')
for w in range(WEEKS):
    for wd in range(DAYS_PER_WEEK):
        diag = w + wd
        delay = diag * 0.012
        parts.append(f'  .d{w}_{wd}{{opacity:0;animation:reveal .05s {delay:.3f}s forwards}}')
parts.append('</style>')

for x, label in month_labels:
    parts.append(f'<text class="ml" x="{x}" y="{PAD_T - 5}">{label}</text>')

for wd, label in enumerate(["Mon","","Wed","","Fri","",""]):
    if label:
        y = PAD_T + wd * (BOX + GAP) + BOX - 2
        parts.append(f'<text class="ml" x="2" y="{y}">{label}</text>')

for w, week in enumerate(grid):
    for wd, day in enumerate(week):
        level = min(day.get("level", 0), 5)
        color = PALETTE[level]
        x = PAD_L + w * (BOX + GAP)
        y = PAD_T + wd * (BOX + GAP)
        cls = f"d{w}_{wd}"
        count = day.get("count", 0)
        parts.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" fill="{color}"><title>{day["date"]}: {count} contributions</title></rect>')

leg_x = W - 110
leg_y = H - 18
parts.append(f'<text class="ml" x="{leg_x}" y="{leg_y}">Less</text>')
for i, c in enumerate(PALETTE[1:]):
    parts.append(f'<rect x="{leg_x+32+i*14}" y="{leg_y-8}" width="{BOX}" height="{BOX}" rx="2" fill="{c}"/>')
parts.append(f'<text class="ml" x="{leg_x+32+len(PALETTE)*14-10}" y="{leg_y}">More</text>')

stats_y = H - 32
parts.append(f'<text class="ml" x="{PAD_L}" y="{stats_y}" font-size="10" fill="#c9d1d9">{total} contributions in the last year  ·  🔥 streak {streak}  ·  longest {longest}</text>')

parts.append('</svg>')

with open("contrib-heatmap.svg", "w") as f:
    f.write("\n".join(parts))
print(f"Saved contrib-heatmap.svg ({W}x{H}px)")
