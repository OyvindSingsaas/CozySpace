#!/usr/bin/env python3
"""Poll NASA DSN Now and append one row per dish (and per signal) to a CSV.

Usage:  python3 scripts/log_dsn.py [--interval 60] [--out data/dsn_log.csv]
Stop with Ctrl-C. Stdlib only.
"""
import argparse, csv, os, sys, time, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

URL = "https://eyes.nasa.gov/dsn/data/dsn.xml"
FIELDS = ["fetched_utc", "feed_utc", "station", "dish", "activity", "az", "el", "wind",
          "target", "rtlt", "upleg_km", "downleg_km",
          "dir", "active", "signal_type", "band", "data_rate", "power", "freq", "spacecraft"]

def fetch():
    req = urllib.request.Request(f"{URL}?r={int(time.time())}", headers={"User-Agent": "CozySpace-logger"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return ET.fromstring(r.read())

def rows(root, fetched):
    ts = root.findtext("timestamp")
    feed = datetime.fromtimestamp(int(ts) / 1000, timezone.utc).isoformat() if ts else ""
    station = ""
    for e in root:
        if e.tag == "station":
            station = e.get("friendlyName")
        elif e.tag == "dish":
            t = e.find("target")
            base = dict(fetched_utc=fetched, feed_utc=feed, station=station, dish=e.get("name"),
                        activity=e.get("activity"), az=e.get("azimuthAngle"), el=e.get("elevationAngle"),
                        wind=e.get("windSpeed"),
                        target=t.get("name") if t is not None else "",
                        rtlt=t.get("rtlt") if t is not None else "",
                        upleg_km=t.get("uplegRange") if t is not None else "",
                        downleg_km=t.get("downlegRange") if t is not None else "")
            sigs = [s for s in e if s.tag in ("upSignal", "downSignal")]
            if not sigs:
                yield base
            for s in sigs:
                yield {**base, "dir": "up" if s.tag == "upSignal" else "down", "active": s.get("active"),
                       "signal_type": s.get("signalType"), "band": s.get("band"),
                       "data_rate": s.get("dataRate"), "power": s.get("power"),
                       "freq": s.get("frequency"), "spacecraft": s.get("spacecraft")}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=float, default=60)
    ap.add_argument("--out", default="data/dsn_log.csv")
    a = ap.parse_args()
    new = not os.path.exists(a.out)
    with open(a.out, "a", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if new: w.writeheader()
        n = 0
        while True:
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            try:
                k = 0
                for r in rows(fetch(), now):
                    w.writerow(r); k += 1
                f.flush(); n += 1
                print(f"{now}  snapshot {n}: {k} rows", flush=True)
            except Exception as ex:
                print(f"{now}  error: {ex}", file=sys.stderr, flush=True)
            time.sleep(a.interval)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nstopped")
