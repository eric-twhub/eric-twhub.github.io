# -*- coding: utf-8 -*-
"""逐月票價概況：往後十二個月，每個月的中位票價。

主掃描（scan_all.py）只抓最近兩個月，用途是列出今天可以訂的便宜票。
月曆那一頁問的是另一件事：「明年七月去日本大概多少錢」。那需要一份
橫跨一整年的資料，但不需要每個航點都抓，所以這裡只取台北出發的
五個主要航點，六十次 API 呼叫，不影響每日更新的時間。

中位數不是平均數：票價分布右偏，少數幾張貴票會把平均拉高。
樣本少於門檻的月份不給數字，寧可寫「還沒有資料」。

用法：python3 scan_months.py
輸出：/tmp/scan_months.json
"""
import json, os, datetime, urllib.request, urllib.parse, time, statistics

MAIN = [('TYO', '東京'), ('OSA', '大阪'), ('CTS', '札幌'),
        ('FUK', '福岡'), ('OKA', '沖繩')]
ORIGIN = 'TPE'
AHEAD = 12          # 往後幾個月
MIN_N = 8           # 一個月至少要這麼多筆才給數字


def _token():
    t = os.environ.get('TRAVELPAYOUTS_TOKEN')
    if t:
        return t.strip()
    try:
        for l in open('.env', encoding='utf-8'):
            if l.startswith('TRAVELPAYOUTS_TOKEN='):
                return l.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    raise SystemExit('找不到 TRAVELPAYOUTS_TOKEN（環境變數或 .env 皆無）')


TOK = _token()
B = 'https://api.travelpayouts.com'


def get(path, **p):
    p['token'] = TOK
    try:
        with urllib.request.urlopen(
                f'{B}{path}?{urllib.parse.urlencode(p)}', timeout=25) as r:
            return json.loads(r.read().decode()).get('data', [])
    except Exception:
        return []


def months(n):
    t = datetime.date.today().replace(day=1)
    out = []
    for _ in range(n):
        out.append(t.strftime('%Y-%m'))
        t = (t.replace(day=28) + datetime.timedelta(days=7)).replace(day=1)
    return out


rows = []
for m in months(AHEAD):
    for code, name in MAIN:
        d = get('/aviasales/v3/prices_for_dates', origin=ORIGIN, destination=code,
                departure_at=m, currency='twd', one_way='false',
                limit=200, sorting='price')
        for x in (d or []):
            p = x.get('price')
            dep = (x.get('departure_at') or '')[:10]
            if p and dep[:7] == m:
                rows.append({'m': m, 'dest': code, 'name': name, 'price': p,
                             'dep': dep})
        time.sleep(0.15)
    got = sum(1 for r in rows if r['m'] == m)
    print(f'{m}  {got:>4} 筆', flush=True)

by = {}
for r in rows:
    by.setdefault(r['m'], []).append(r['price'])
out = {'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
       'origin': ORIGIN, 'dests': [c for c, _ in MAIN],
       'dest_names': [n for _, n in MAIN], 'min_n': MIN_N,
       'months': {m: {'n': len(v), 'median': round(statistics.median(v)),
                      'low': min(v), 'enough': len(v) >= MIN_N}
                  for m, v in sorted(by.items())}}
json.dump(out, open('/tmp/scan_months.json', 'w'), ensure_ascii=False)
_e = sum(1 for v in out['months'].values() if v['enough'])
print(f'\n{_e} 個月樣本夠（門檻 {MIN_N} 筆），'
      f'{len(out["months"]) - _e} 個月樣本不足，共 {len(rows)} 筆。'
      f'\n遠月沒有資料是正常的：航空公司還沒開賣，API 就查不到價格。')
