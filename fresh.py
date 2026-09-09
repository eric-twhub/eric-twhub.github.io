import json,urllib.request,urllib.parse,datetime,collections,time
TOK=next(l.split('=',1)[1].strip() for l in open('.env',encoding='utf-8') if l.startswith('TRAVELPAYOUTS_TOKEN='))
now=datetime.datetime.now()
ages=[];rows=[]
for o in ['TPE','TSA','RMQ','KHH']:
    q=urllib.parse.urlencode(dict(origin=o,destination='JP',currency='twd',limit=1000,
        show_to_affiliates='true',period_type='month',token=TOK))
    with urllib.request.urlopen(f'https://api.travelpayouts.com/v2/prices/latest?{q}',timeout=40) as r:
        d=json.loads(r.read().decode()).get('data',[])
    for x in d: x['_o']=o
    rows+=d; time.sleep(0.3)

for x in rows:
    try: ages.append((now-datetime.datetime.fromisoformat(x['found_at'])).total_seconds()/3600)
    except: pass
ages.sort()
print(f'樣本 {len(rows)} 筆')
print(f'資料年齡（小時）: 最新 {ages[0]:.1f} / 中位 {ages[len(ages)//2]:.1f} / 最舊 {ages[-1]:.1f}')
b=collections.Counter('<24h' if a<24 else '24-48h' if a<48 else '48-72h' if a<72 else '>72h' for a in ages)
print('分佈:', dict(b))
print('目的地:', dict(collections.Counter(x['destination'] for x in rows).most_common()))
u6=[x for x in rows if x['value']<6000]
print(f'\n低於 NT$6,000 的來回票: {len(u6)} 筆')
for x in sorted(u6,key=lambda y:y['value'])[:12]:
    print(f"  {x['_o']}→{x['destination']}  NT${x['value']:,}  {x['depart_date']}~{x['return_date']}  轉機{x['number_of_changes']}  找到於 {x['found_at'][:16]}")
