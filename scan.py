import json, urllib.request, urllib.parse, urllib.error, collections, time

TOK = next(l.split('=',1)[1].strip() for l in open('.env',encoding='utf-8')
           if l.startswith('TRAVELPAYOUTS_TOKEN='))
BASE = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'

LCC = {'IT','MM','GK','TR','IJ','7G','AK','D7','XJ','FD','SL','VZ','BX','7C','LJ','TW','UO','Y8','JW','3K'}
FSC = {'BR','CI','JX','JL','NH','NU','CX','KE','UA','OZ','KE','SQ','TG','PR'}
ORIGINS = ['TPE','TSA','RMQ','KHH','TNN']
MONTHS  = ['2026-09','2026-10']

rows=[]
for o in ORIGINS:
    for m in MONTHS:
        q = urllib.parse.urlencode(dict(origin=o, destination='JP', departure_at=m,
            currency='twd', one_way='false', limit=1000, sorting='price', token=TOK))
        try:
            with urllib.request.urlopen(f'{BASE}?{q}', timeout=40) as r:
                data = json.loads(r.read().decode()).get('data',[])
            print(f'{o} {m}: {len(data)} 筆')
            rows += data
        except urllib.error.HTTPError as e:
            print(f'{o} {m}: HTTP {e.code} {e.read().decode()[:120]}')
        time.sleep(0.4)

json.dump(rows, open('/tmp/scan.json','w'), ensure_ascii=False)
print(f'\n總計 {len(rows)} 筆\n')

air = collections.Counter(r['airline'] for r in rows)
print('航空公司分佈:', dict(air.most_common()))
unknown = {a for a in air if a not in LCC and a not in FSC}
print('未分類代碼:', unknown or '無')

dest = collections.Counter(r['destination'] for r in rows)
print(f'\n涵蓋目的地 {len(dest)} 個:', dict(dest.most_common(25)))
