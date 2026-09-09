# -*- coding: utf-8 -*-
import json, os, urllib.request, urllib.parse, urllib.error, time, sys

def _token():
    """優先讀環境變數（GitHub Actions），本機則回退到 .env"""
    t = os.environ.get('TRAVELPAYOUTS_TOKEN')
    if t: return t.strip()
    try:
        for l in open('.env', encoding='utf-8'):
            if l.startswith('TRAVELPAYOUTS_TOKEN='):
                return l.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    raise SystemExit('找不到 TRAVELPAYOUTS_TOKEN（環境變數或 .env 皆無）')

TOK=_token()
B='https://api.travelpayouts.com'

# 日本航點：地區 → [(IATA, 中文名, 所屬縣/註記)]
REGIONS = {
 '北海道': [('CTS','札幌・新千歲','北海道'),('HKD','函館','北海道')],
 '東北':   [('SDJ','仙台','宮城'),('AXT','秋田','秋田'),('HNA','花卷','岩手'),
            ('AOJ','青森','青森'),('FKS','福島','福島')],
 '關東':   [('NRT','東京・成田','東京'),('HND','東京・羽田','東京')],
 '中部・北陸':[('NGO','名古屋・中部','愛知'),('KMQ','小松','石川'),('TOY','富山','富山'),
            ('KIJ','新潟','新潟'),('FSZ','靜岡','靜岡')],
 '關西':   [('KIX','大阪・關西','大阪'),('UKB','神戶','兵庫')],
 '中國':   [('HIJ','廣島','廣島'),('OKJ','岡山','岡山'),('YGJ','米子','鳥取')],
 '四國':   [('TAK','高松','香川'),('MYJ','松山','愛媛'),('KCZ','高知','高知')],
 '九州':   [('FUK','福岡','福岡'),('KKJ','北九州','福岡'),('HSG','佐賀','佐賀'),
            ('KMJ','熊本','熊本'),('OIT','大分','大分'),('KMI','宮崎','宮崎'),
            ('KOJ','鹿兒島','鹿兒島'),('NGS','長崎','長崎')],
 '沖繩・離島':[('OKA','沖繩・那霸','沖繩'),('ISG','石垣島','沖繩'),('MMY','宮古島','沖繩'),
            ('SHI','下地島','沖繩')],
}
ORIGINS=['TPE','TSA','RMQ','KHH','TNN']
MONTHS=['2026-09','2026-10']

def get(path,**p):
    p['token']=TOK
    try:
        with urllib.request.urlopen(f"{B}{path}?{urllib.parse.urlencode(p)}",timeout=25) as r:
            return json.loads(r.read().decode()).get('data',[])
    except Exception: return []

out=[]; n=0
alld=[(c,nm,pref,reg) for reg,v in REGIONS.items() for c,nm,pref in v]
for code,nm,pref,reg in alld:
    got=0
    for o in ORIGINS:
        for m in MONTHS:
            d=get('/aviasales/v3/prices_for_dates',origin=o,destination=code,departure_at=m,
                  currency='twd',one_way='false',limit=200,sorting='price')
            for x in (d or []):
                x['_region']=reg; x['_dname']=nm; x['_pref']=pref; x['_rt']=True
            out+=d or []; got+=len(d or []); n+=1
            time.sleep(0.15)
    # 單程補充（grouped_prices 對冷門航點較有資料）
    for o in ORIGINS:
        g=get('/aviasales/v3/grouped_prices',origin=o,destination=code,currency='twd',group_by='departure_at')
        if isinstance(g,dict):
            for k,x in g.items():
                x['_region']=reg; x['_dname']=nm; x['_pref']=pref; x['_rt']=False
                out.append(x); got+=1
        n+=1; time.sleep(0.15)
    print(f'{reg:<8}{nm:<14}{code}  {got:>4} 筆', flush=True)

json.dump(out,open('/tmp/scan_all.json','w'),ensure_ascii=False)
print(f'\n共 {n} 次 API 呼叫，取得 {len(out)} 筆')
