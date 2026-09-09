import json, hashlib, urllib.request, urllib.error, time

TOK = next(l.split('=',1)[1].strip() for l in open('.env',encoding='utf-8') if l.startswith('TRAVELPAYOUTS_TOKEN='))
MARKER='775639'

def sign(p):
    def flat(v):
        if isinstance(v,dict):  return [x for k in sorted(v) for x in flat(v[k])]
        if isinstance(v,list):  return [x for i in v for x in flat(i)]
        return [str(v)]
    vals=[x for k in sorted(p) for x in flat(p[k])]
    return hashlib.md5((TOK+':'+':'.join(vals)).encode()).hexdigest()

def search(origin,dest,date,ret=None):
    segs=[{"origin":origin,"destination":dest,"date":date}]
    if ret: segs.append({"origin":dest,"destination":origin,"date":ret})
    body={"marker":MARKER,"host":"flights.example.com","user_ip":"127.0.0.1","locale":"en",
          "trip_class":"Y","passengers":{"adults":1,"children":0,"infants":0},"segments":segs}
    body["signature"]=sign(body)
    req=urllib.request.Request("https://api.travelpayouts.com/v1/flight_search",
        data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=40) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_err":e.code,"_body":e.read().decode()[:300]}

print('=== 測試即時搜尋 TPE→YGJ 米子 2026-10-16 ===')
r=search('TPE','YGJ','2026-10-16','2026-10-19')
print(json.dumps(r,ensure_ascii=False)[:600])
