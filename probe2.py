import json,urllib.request,urllib.parse,urllib.error,time
TOK=next(l.split('=',1)[1].strip() for l in open('.env',encoding='utf-8') if l.startswith('TRAVELPAYOUTS_TOKEN='))
B='https://api.travelpayouts.com'
def get(path,**p):
    p['token']=TOK
    try:
        with urllib.request.urlopen(f"{B}{path}?{urllib.parse.urlencode(p)}",timeout=30) as r:
            b=json.loads(r.read().decode()); d=b.get('data',b)
            return len(d) if isinstance(d,(list,dict)) else 0, d
    except urllib.error.HTTPError as e: return f'HTTP{e.code}', None
    except Exception as e: return f'ERR', None

tests=[('HSG','佐賀'),('OIT','大分'),('YGJ','米子'),('OKJ','岡山'),('KMJ','熊本'),('KCZ','高知'),('HKD','函館'),('TAK','高松')]
print(f"{'目的地':<10}{'v2/cheap':>12}{'v2/direct':>12}{'month-matrix':>14}{'v3 grouped':>12}")
for code,name in tests:
    a,_=get('/v2/prices/cheap',origin='TPE',destination=code,currency='twd')
    b,_=get('/v2/prices/direct',origin='TPE',destination=code,currency='twd')
    c,_=get('/v2/prices/month-matrix',origin='TPE',destination=code,currency='twd',month='2026-10-01')
    d,dd=get('/aviasales/v3/grouped_prices',origin='TPE',destination=code,currency='twd',group_by='departure_at')
    print(f"{name:<10}{str(a):>12}{str(b):>12}{str(c):>14}{str(d):>12}")
    if isinstance(d,int) and d>0:
        k=list(dd)[0]; print('     樣本:', json.dumps(dd[k],ensure_ascii=False)[:150])
    time.sleep(0.3)
