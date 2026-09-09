import json, os, urllib.request, urllib.parse, urllib.error

tok = None
for line in open('.env', encoding='utf-8'):
    if line.startswith('TRAVELPAYOUTS_TOKEN='):
        tok = line.split('=', 1)[1].strip()
if not tok or tok == 'PASTE_YOUR_TOKEN_HERE':
    raise SystemExit('token 未設定')
print(f'token 已載入（長度 {len(tok)}，前 4 碼 {tok[:4]}…）\n')

def call(name, url, params):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(f'{url}?{q}', headers={'X-Access-Token': tok})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode())
        d = body.get('data', body)
        n = len(d) if isinstance(d, (list, dict)) else 0
        print(f'[{r.status}] {name}: success={body.get("success")}, 筆數={n}')
        return body
    except urllib.error.HTTPError as e:
        print(f'[{e.code}] {name}: {e.read().decode()[:200]}')
    except Exception as e:
        print(f'[ERR] {name}: {e}')
    return None

BASE = 'https://api.travelpayouts.com'
r1 = call('v3 prices_for_dates TPE→OKA 10月', f'{BASE}/aviasales/v3/prices_for_dates',
          dict(origin='TPE', destination='OKA', departure_at='2026-10', currency='twd',
               one_way='false', limit=30, sorting='price'))
r2 = call('v2 prices/latest TPE→JP', f'{BASE}/v2/prices/latest',
          dict(origin='TPE', destination='JP', currency='twd', limit=30, show_to_affiliates='true'))
r3 = call('v3 grouped_prices TPE→JP', f'{BASE}/aviasales/v3/grouped_prices',
          dict(origin='TPE', destination='JP', currency='twd', group_by='departure_at'))

with open('/tmp/tp_raw.json','w') as f:
    json.dump({'prices_for_dates': r1, 'latest': r2, 'grouped': r3}, f, ensure_ascii=False)
print('\n原始回應已存 /tmp/tp_raw.json')
