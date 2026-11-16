import json, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

URL = "https://nasstatus.faa.gov/api/airport-events"
now = datetime.now(timezone.utc).isoformat(timespec="seconds")
output = {"checked_at": now, "source": URL, "success": False, "events": []}
history_path = Path("history.json")
try:
    req = urllib.request.Request(URL, headers={"User-Agent":"DFW-Operations-Monitor/2.0","Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=25) as response:
        payload = json.load(response)
    items = payload.get("items", []) if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("Unexpected FAA response shape: items is not a list")
    for item in items:
        if not isinstance(item, dict):
            continue
        airport = str(item.get("airportId") or "").upper()
        if airport not in ("DFW", "KDFW"):
            continue
        for kind in ("groundStop", "groundDelay", "arrivalDelay", "departureDelay", "airportClosure"):
            detail = item.get(kind)
            if isinstance(detail, dict) and detail:
                output["events"].append({"type":kind, "details":detail})
    output["success"] = True
except Exception as exc:
    output["error"] = str(exc)

Path("data.json").write_text(json.dumps(output, indent=2, default=str) + "\n")
try:
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    if not isinstance(history, list):
        history = []
except (ValueError, OSError):
    history = []
counts = {k:sum(e["type"] == k for e in output["events"]) for k in
          ("groundStop", "groundDelay", "arrivalDelay", "departureDelay", "airportClosure")}
history.append({"at":now, "success":output["success"], "counts":counts if output["success"] else None})
cutoff = datetime.now(timezone.utc) - timedelta(days=7)
history = [h for h in history if isinstance(h, dict) and
           datetime.fromisoformat(h["at"].replace("Z","+00:00")) >= cutoff]
history_path.write_text(json.dumps(history[-850:], indent=2) + "\n")
print("FAA fetch success:", output["success"], "DFW events:", len(output["events"]),
      "history samples:", len(history))
