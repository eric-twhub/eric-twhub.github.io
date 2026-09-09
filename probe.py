import json, urllib.request, urllib.parse, urllib.error, time
TOK = next(l.split('=',1)[1].strip() for l in open('.env',encoding='utf-8') if l.startswith('TRAVELPAYOUTS_TOKEN='))
BASE='https://api.travelpayouts.com/aviasales/v3/prices_for_dates'

def q(o,d,m='2026-10'):
    p=urllib.parse.urlencode(dict(origin=o,destination=d,departure_at=m,currency='twd',
        one_way='false',limit=100,sorting='price',token=TOK))
    try:
        with urllib.request.urlopen(f'{BASE}?{p}',timeout=30) as r:
            return json.loads(r.read().decode()).get('data',[])
    except urllib.error.HTTPError as e:
        return f'HTTP{e.code}'

print('--- 二線機場（指定機場代碼，不用 JP）---')
for d,name in [('HSG','佐賀'),('OIT','大分'),('YGJ','米子'),('OKJ','岡山'),('KMJ','熊本'),
               ('HNA','花卷'),('KIJ','新潟'),('KCZ','高知'),('KKJ','北九州'),('HKD','函館'),('AXT','秋田')]:
    r=q('TPE',d)
    if isinstance(r,str): print(f'  TPE→{d} {name}: {r}')
    else:
        best=min(r,key=lambda x:x['price']) if r else None
        print(f'  TPE→{d} {name}: {len(r):>3} 筆' + (f"  最低 NT${best['price']:,} {best['airline']} {best['departure_at'][:10]} 轉機{best['transfers']}" if best else ''))
    time.sleep(0.3)

print('\n--- 台南 TNN（逐一指定目的地）---')
for d in ['KIX','OKA','KMJ','OSA','TYO']:
    r=q('TNN',d)
    print(f'  TNN→{d}: ' + (r if isinstance(r,str) else f'{len(r)} 筆' + (f"  最低 NT${min(x['price'] for x in r):,}" if r else '')))
    time.sleep(0.3)
