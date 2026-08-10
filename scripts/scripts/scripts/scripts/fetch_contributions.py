#!/usr/bin/env python3
import json, pathlib, datetime
import requests
from bs4 import BeautifulSoup

USERNAME = "yesiampavan07-loop"
URL = f"https://github.com/users/{USERNAME}/contributions"

print(f"Fetching contributions for {USERNAME}...")
resp = requests.get(URL, headers={"Accept": "text/html", "User-Agent": "Mozilla/5.0"}, timeout=15)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
days = []
for td in soup.select("td.ContributionCalendar-day"):
    date_str = td.get("data-date", "")
    count_text = td.get("data-level", "0")
    count = 0
    try:
        count = int(td.get("data-count", 0))
    except:
        pass
    if date_str:
        days.append({"date": date_str, "count": count, "level": int(count_text or 0)})

days.sort(key=lambda d: d["date"])

total = sum(d["count"] for d in days)
best_day = max(days, key=lambda d: d["count"]) if days else {}

streak = 0
today = datetime.date.today().isoformat()
for d in reversed(days):
    if d["date"] > today:
        continue
    if d["count"] > 0:
        streak += 1
    else:
        break

longest = cur = 0
for d in days:
    if d["count"] > 0:
        cur += 1
        longest = max(longest, cur)
    else:
        cur = 0

out = {
    "username": USERNAME,
    "generated": datetime.datetime.now(datetime.UTC).isoformat(),
    "total_contributions": total,
    "current_streak": streak,
    "longest_streak": longest,
    "best_day": best_day,
    "days": days,
}

pathlib.Path("data").mkdir(exist_ok=True)
with open("data/contributions.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"Done! {len(days)} days | {total} total | streak {streak} | longest {longest}")
