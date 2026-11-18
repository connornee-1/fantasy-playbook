"""Download documented Sleeper endpoints; fail without publishing partial data."""
import json
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import time

BASE = 'https://api.sleeper.app/v1/'
def get(path):
    for attempt in range(3):
        try:
            with urlopen(Request(BASE + path, headers={'User-Agent': 'FantasyPlaybook/1.0 (educational project)'}), timeout=60) as response:
                return json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

def note(player):
    if player.get('injury_status'):
        return 'Injury flag: verify latest team report before adding.'
    if player.get('depth_chart_order') == 1:
        return 'Listed first on depth chart. Research role and availability.'
    return 'Watchlist candidate. Confirm opportunity before a claim.'

def build(state, players, adds, drops):
    assert isinstance(players, dict) and players, 'Missing player directory'
    assert isinstance(adds, list) and adds, 'Missing add trends'
    drop_counts = {str(p['player_id']): int(p['count']) for p in drops}
    ranks = {str(p['player_id']): i+1 for i,p in enumerate(adds)}
    counts = {str(p['player_id']): int(p['count']) for p in adds}
    result = []
    for pid, p in players.items():
        if p.get('position') not in ('QB', 'RB', 'WR', 'TE') or not p.get('active'):
            continue
        result.append({'id': str(pid), 'name': p.get('full_name') or (p.get('first_name','')+' '+p.get('last_name','')).strip(), 'position': p['position'], 'team': p.get('team') or '', 'injury': p.get('injury_status') or '', 'adds': counts.get(str(pid),0), 'drops': drop_counts.get(str(pid),0), 'rank': ranks.get(str(pid)), 'note': note(p)})
    assert result, 'No eligible players'
    result.sort(key=lambda p: (p['rank'] is None, p['rank'] or 99999, p['name']))
    return {'updated_at': datetime.now(timezone.utc).isoformat(), 'season': state['season'], 'season_type': state['season_type'], 'week': state.get('display_week') or state['week'], 'source': 'Sleeper API', 'lookback_hours': 24, 'players': result}

if __name__ == '__main__':
    data = build(get('state/nfl'), get('players/nfl'), get('players/nfl/trending/add?lookback_hours=24&limit=100'), get('players/nfl/trending/drop?lookback_hours=24&limit=100'))
    target = Path(__file__).resolve().parents[1] / 'site/data/weekly.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    tmp.replace(target)
    print(f'Refreshed {len(data["players"])} players for week {data["week"]}')
