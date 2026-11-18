# Fantasy Playbook

Interactive fantasy football dashboard by Connor Nee. Static HTML, CSS and JavaScript, published with GitHub Pages. No account or paid API key is required.

## Features
- Weekly Sleeper player directory, injury status and add/drop trends.
- Position and name filters, watchlist saved on this device.
- Start/sit calculator with adjustable projected statistics and PPR / half-PPR / standard scoring.
- Trade calculator comparing user-entered rest-of-season values. Values are not expert consensus.
- Weekly Tuesday 12:17 UTC refresh and redeployment through GitHub Actions, plus manual refresh.

## Data and methodology
Sleeper's documented, free noncommercial API supplies NFL state, player metadata and 24-hour add/drop counts. Trending order measures add activity, not projected fantasy production. Waiver advice is a rule-based research prompt based on injury status, depth-chart order and add activity; availability in your league is unknown. No fabricated expert rankings or projections are displayed. The comparison calculator converts your stat estimates using 0.04 points per passing yard, 4 per passing TD, -2 per interception, 0.1 per rushing/receiving yard, 6 per rushing/receiving TD, and the selected reception bonus. It does not account for matchups, weather, bye weeks or breaking news. Check team reports before kickoff.

Sources: https://docs.sleeper.com/ and https://github.com/connornee-1/fantasy-playbook .

## Run locally
Run `python3 -m http.server 8000 --directory site` and open http://localhost:8000 . To download a fresh snapshot first, run `python3 scripts/refresh.py`. Requires Python 3.10+. The site also works without a snapshot and clearly reports that data is unavailable.

## Deployment
In repository Settings → Pages, set Source to GitHub Actions. The workflow refreshes data, runs unit tests and publishes `site/`. GitHub may delay scheduled runs, and disables schedules in public repositories after 60 days without repository activity. Data freshness is displayed on the page; a failed refresh fails deployment rather than labeling old data current. Use Actions → Refresh and publish → Run workflow to retry. No secrets are needed.
