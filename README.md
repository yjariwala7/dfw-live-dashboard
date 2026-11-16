# DFW Operations Monitor

A no-paid-API dashboard displaying FAA-reported DFW ground stops, ground delay programs, and arrival/departure advisories. FlightAware links open the live flight pages for cancellations and flight-level status.

## Publish free with GitHub Pages

1. Create a **public** GitHub repository (for example `dfw-operations`). Upload **all files**, including `.github/workflows/update.yml` (preserve folders).
2. In repository **Settings → Actions → General → Workflow permissions**, enable **Read and write permissions** if the default token cannot commit. Save.
3. Open **Actions → Refresh FAA data → Run workflow** once. Confirm it updates `data.json`.
4. Open **Settings → Pages → Build and deployment → Deploy from a branch**, select `main` and `/ (root)`, and save.
5. Your public URL will be `https://YOUR-GITHUB-USERNAME.github.io/dfw-operations/` (replace with your actual username and repository name).

The scheduled job requests the free FAA NAS Status JSON endpoint every 15 minutes and commits the result. GitHub Actions schedules may be delayed, especially near quarter-hour boundaries; a stale-data indicator appears after 30 minutes. The web page checks for a new snapshot every 15 minutes while open. The feed may omit some events; no event is not proof that every flight is on time.

No API keys needed. The dashboard intentionally does not scrape FlightAware or claim access to paid flight-level data. GitHub's free-tier availability and service policies may change.
