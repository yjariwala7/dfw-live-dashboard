import json, urllib.request
from datetime import datetime, timezone
from pathlib import Path
URL='https://nasstatus.faa.gov/api/airport-events'
out={'checked_at':datetime.now(timezone.utc).isoformat(),'source':URL,'success':False,'events':[]}
try:
    req=urllib.request.Request(URL,headers={'User-Agent':'DFW-FAA-Status-Dashboard/1.0','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=25) as r: payload=json.load(r)
    items=payload.get('items',[]) if isinstance(payload,dict) else payload
    if not isinstance(items,list): raise ValueError('Unexpected FAA response format')
    for item in items:
        airport=str(item.get('airportId') or '').upper()
        if airport not in ('DFW','KDFW'): continue
        for kind in ('groundStop','groundDelay','arrivalDelay','departureDelay','airportClosure'):
            block=item.get(kind)
            if isinstance(block,dict) and block:
                out['events'].append({'type':kind,'details':block})
    out['success']=True
except Exception as exc:
    out['error']=str(exc)
Path('data.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
