#!/usr/bin/env python3
"""Build assets/data/kols-climatology.json from Iowa Environmental Mesonet hourly ASOS.

Source (no key): https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py
  station=OLS  (KOLS / Nogales International)
  report_type=3  (routine hourly METAR only)
  tz=America/Phoenix

Usage:
  curl -sS -L -o /tmp/ols-asos.csv 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=OLS&data=vsby&data=skyc1&data=skyl1&data=skyc2&data=skyl2&data=skyc3&data=skyl3&data=skyc4&data=skyl4&data=metar&year1=2020&month1=1&day1=1&year2=2025&month2=12&day2=31&tz=America%2FPhoenix&format=onlycomma&latlon=no&elev=no&missing=empty&trace=T&direct=yes&report_type=3'
  python3 tools/kols_climatology.py /tmp/ols-asos.csv
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "data", "kols-climatology.json")

# FAA AIM flight categories. Ceiling is the lowest BKN/OVC/VV base.
# Boundaries: 3,000 ft / 5 SM are MVFR (not VFR); 1,000 ft / 3 SM are MVFR; 500 ft / 1 SM are IFR.
RANK = {"VFR": 0, "MVFR": 1, "IFR": 2, "LIFR": 3}
CLEAR_AMT = {"CLR", "SKC", "FEW", "NSC", "NCD"}
CLOUDY_AMT = {"SCT", "BKN", "OVC", "VV"}
CEILING_AMT = {"BKN", "OVC", "VV"}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def num(v):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def layers(row):
    out = []
    for i in range(1, 5):
        amt = (row.get(f"skyc{i}") or "").strip().upper()
        if not amt:
            continue
        if amt.endswith(" "):
            amt = amt.strip()
        base = num(row.get(f"skyl{i}"))
        out.append((amt, base))
    return out


def ceiling_ft(lyrs):
    c = None
    for amt, base in lyrs:
        if amt in CEILING_AMT:
            # VV without a height is treated as a zero-foot ceiling (very low).
            h = 0.0 if base is None and amt == "VV" else base
            if h is None:
                continue
            if c is None or h < c:
                c = h
    return c


def category(vis, ceil):
    if vis is None and ceil is None:
        return None
    # Missing element is treated as non-restrictive only when the other is present.
    # Visibility is required (a clear sky with no vis is not classified).
    if vis is None:
        return None
    cv = ceil if ceil is not None else float("inf")
    if cv < 500 or vis < 1:
        return "LIFR"
    if cv < 1000 or vis < 3:
        return "IFR"
    if cv <= 3000 or vis <= 5:
        return "MVFR"
    return "VFR"


def sky_kind(lyrs):
    if not lyrs:
        return None
    amts = {a for a, _ in lyrs}
    if amts & CLOUDY_AMT:
        return "cloudy"
    if amts <= CLEAR_AMT:
        return "clear"
    return None


def avg(vals):
    if not vals:
        return 0.0
    return round(sum(vals) / len(vals), 1)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ols-asos-2020-2025.csv"
    # day -> list of (hour, cat, sky)
    days = defaultdict(list)
    years_seen = set()
    n_obs = 0
    n_daytime = 0
    with open(src, newline="") as f:
        for row in csv.DictReader(f):
            valid = (row.get("valid") or "").strip()
            try:
                t = datetime.strptime(valid, "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            years_seen.add(t.year)
            n_obs += 1
            if not (7 <= t.hour < 19):
                continue
            n_daytime += 1
            vis = num(row.get("vsby"))
            lyrs = layers(row)
            cat = category(vis, ceiling_ft(lyrs))
            sky = sky_kind(lyrs)
            if cat is None and sky is None:
                continue
            days[t.date()].append((t.hour, cat, sky))

    # Per-day rollup
    day_rows = []
    for d, obs in days.items():
        cats = [c for _, c, _ in obs if c]
        skys = [s for _, _, s in obs if s]
        if not cats and not skys:
            continue
        worst = None
        if cats:
            worst = max(cats, key=lambda c: RANK[c])
        clear = cloudy = None
        if skys:
            n_clear = sum(1 for s in skys if s == "clear")
            # Clear/sunny day: more than half of daytime obs are CLR/SKC/FEW.
            clear = n_clear > (len(skys) / 2)
            cloudy = not clear
        day_rows.append((d, worst, clear, cloudy, len(cats)))

    years = sorted(years_seen)
    by_year = {}
    for y in years:
        rows = [r for r in day_rows if r[0].year == y]
        cal = 366 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 365
        rec = {
            "VFR": sum(1 for r in rows if r[1] == "VFR"),
            "MVFR": sum(1 for r in rows if r[1] == "MVFR"),
            "IFR": sum(1 for r in rows if r[1] == "IFR"),
            "LIFR": sum(1 for r in rows if r[1] == "LIFR"),
            "clear": sum(1 for r in rows if r[2] is True),
            "cloudy": sum(1 for r in rows if r[3] is True),
            "classified": sum(1 for r in rows if r[1]),
            "calendarDays": cal,
        }
        rec["missingDays"] = cal - rec["classified"]
        by_year[str(y)] = rec

    def series(key):
        return avg([by_year[str(y)][key] for y in years])

    monthly = []
    for m in range(1, 13):
        # Average observed days in this calendar month across the years.
        rec = {"month": m, "name": MONTHS[m - 1]}
        for key in ("VFR", "MVFR", "IFR", "LIFR", "clear", "cloudy", "classified"):
            vals = []
            for y in years:
                rows = [r for r in day_rows if r[0].year == y and r[0].month == m]
                if key == "classified":
                    vals.append(sum(1 for r in rows if r[1]))
                elif key in ("clear", "cloudy"):
                    want = True if key == "clear" else True
                    vals.append(sum(1 for r in rows if (r[2] if key == "clear" else r[3]) is True))
                else:
                    vals.append(sum(1 for r in rows if r[1] == key))
            rec[key] = avg(vals)
        monthly.append(rec)

    method = (
        "A day's flight category is the most restrictive FAA category among routine hourly "
        "ASOS observations from 7:00 a.m. to 7:00 p.m. Arizona time (America/Phoenix; "
        "LIFR > IFR > MVFR > VFR). FAA categories: VFR is ceiling above 3,000 ft and "
        "visibility above 5 SM; MVFR is ceiling 1,000–3,000 ft or visibility 3–5 SM; "
        "IFR is ceiling 500 to below 1,000 ft or visibility 1 to below 3 SM; LIFR is "
        "ceiling below 500 ft or visibility below 1 SM. Days without a usable daytime "
        "visibility observation are omitted, so yearly totals sum to a little under 365. "
        "A day is counted as clear or sunny if more than half of those daytime observations "
        "are CLR, SKC, or FEW; otherwise it is counted as cloudy (SCT, BKN, OVC, or VV)."
    )

    out = {
        "station": "KOLS",
        "iemStation": "OLS",
        "source": "Iowa Environmental Mesonet / NWS ASOS",
        "sourceUrl": "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py",
        "years": years,
        "yearLabel": f"{years[0]}–{years[-1]}",
        "timezone": "America/Phoenix",
        "daytime": "07:00–19:00",
        "method": method,
        "observations": n_obs,
        "daytimeObservations": n_daytime,
        "averageDaysPerYear": {
            "VFR": series("VFR"),
            "MVFR": series("MVFR"),
            "IFR": series("IFR"),
            "LIFR": series("LIFR"),
            "classified": series("classified"),
            "clear": series("clear"),
            "cloudy": series("cloudy"),
        },
        "monthly": monthly,
        "byYear": by_year,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")

    a = out["averageDaysPerYear"]
    print(f"wrote {OUT}")
    print(f"years {out['yearLabel']}  hourly obs {n_obs}  daytime used {n_daytime}")
    print(f"avg days/year  VFR {a['VFR']}  MVFR {a['MVFR']}  IFR {a['IFR']}  LIFR {a['LIFR']}  classified {a['classified']}")
    print(f"avg days/year  clear {a['clear']}  cloudy {a['cloudy']}")
    for y, rec in by_year.items():
        print(f"  {y}: {rec}")


if __name__ == "__main__":
    main()
