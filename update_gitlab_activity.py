import datetime as dt
import json
import urllib.request
from pathlib import Path

url = "https://gitlab.com/users/spr1te-q/calendar.json"
request = urllib.request.Request(url, headers={"User-Agent": "spr1te-q-profile-calendar"})
with urllib.request.urlopen(request, timeout=30) as response:
    data = json.load(response)

if not isinstance(data, dict):
    raise ValueError("Unexpected GitLab calendar response")

today = dt.datetime.now(dt.timezone.utc).date()
start = today - dt.timedelta(days=364)
first_sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
colors = ("#34313b", "#f8d7e4", "#f4bad1", "#ed96ba", "#e773a5")
values = sorted(int(value) for value in data.values() if int(value) > 0)

def color(count):
    if not count or not values:
        return colors[0]
    return colors[1 + min(3, sum(count > values[min(len(values) - 1, len(values) * q // 4)] for q in (1, 2, 3)))]

cells = []
for offset in range(365):
    day = start + dt.timedelta(days=offset)
    days_from_first = (day - first_sunday).days
    x, y = (days_from_first // 7) * 14, (days_from_first % 7) * 14
    count = int(data.get(day.isoformat(), 0))
    cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{color(count)}"><title>{day}: {count} contributions</title></rect>')
width = ((today - first_sunday).days // 7 + 1) * 14
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 98" role="img" aria-label="GitLab contributions over the last 365 days">' + ''.join(cells) + '</svg>\n'
Path("gitlab-activity.svg").write_text(svg, encoding="utf-8")
