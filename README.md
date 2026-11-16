# DFW Airport Operations Control Center — V2

Free, static GitHub Pages dashboard powered by the public FAA NAS airport-events feed.

## Upgrade your existing repository
1. Open https://github.com/yjariwala7/dfw-live-dashboard
2. Replace root `index.html`, `update.py`, `data.json`, and `README.md` with the versions in this ZIP.
3. Add new `history.json` to the root.
4. Replace `.github/workflows/update.yml` with the included version. **The `.github` folder may be hidden by your file manager.** On GitHub, create or edit the path `.github/workflows/update.yml` directly.
5. Commit changes to `main`. In **Actions → Refresh FAA data → Run workflow**, run once.
6. Confirm that `data.json` and `history.json` have updated timestamps/entries.
7. Visit https://yjariwala7.github.io/dfw-live-dashboard/ and refresh.

## Data semantics
- Data is attempted every 15 minutes, not guaranteed precisely on schedule.
- Historical charts start when V2 is installed. No fabricated backfill.
- Timeline colors reflect collected FAA feed observations, not individual flights.
- FAA feed is not a source of comprehensive on-time or cancellation totals.
- A successful HTTP response does not prove the upstream feed is complete.
- On failure, data is marked unknown and historical failures are recorded.

## Caveat
The fetch/parser retains the earlier project's assumed `items`/`airportId` FAA schema. If the FAA changes that schema, the dashboard may show no events even when the feed has events. Verify source format and event interpretation before relying on it for operational decisions.
