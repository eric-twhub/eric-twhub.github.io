# -*- coding: utf-8 -*-
"""台日機票速報 — 多頁 SEO 網站產生器"""
import json, datetime, html, collections, os, urllib.parse, shutil, re

CFG=json.load(open('partners.json',encoding='utf-8'))
W=CFG.get('widgets',{})
MARKER=CFG['marker']; P=CFG['partners']
SITE=CFG['site']['url'].rstrip('/'); SITENAME=CFG['site']['name']
BASE=CFG['site'].get('base','').rstrip('/')
def U(p): return BASE+p

LCC={'IT':'台灣虎航','MM':'樂桃航空','GK':'捷星日本','TR':'酷航','IJ':'春秋航空日本','7G':'星悅航空',
 'NQ':'Air Japan','AK':'馬來西亞亞航','D7':'全亞洲航空','XJ':'泰亞航X','FD':'泰國亞洲航空',
 'SL':'泰國獅子航空','VZ':'泰越捷航空','BX':'釜山航空','7C':'濟州航空','LJ':'真航空',
 'TW':'德威航空','UO':'香港快運','Y8':'金鵬航空','HB':'大灣區航空','ZE':'易斯達航空','VJ':'越捷航空','5J':'宿霧太平洋航空'}
FSC={'BR':'長榮航空','CI':'中華航空','JX':'星宇航空','JL':'日本航空','NH':'全日空','NU':'日本越洋航空',
 'CX':'國泰航空','KE':'大韓航空','UA':'聯合航空','AE':'華信航空','HX':'香港航空','MF':'廈門航空','OZ':'韓亞航空','FM':'上海航空','B7':'立榮航空','PR':'菲律賓航空'}
ORI={'TPE':'台北桃園','TSA':'台北松山','RMQ':'台中','KHH':'高雄','TNN':'台南'}
ORIGINS=[('taipei','台北',['TPE','TSA']),('taichung','台中',['RMQ']),
         ('kaohsiung','高雄',['KHH']),('tainan','台南',['TNN'])]
ORI_OF={c:o for o in ORIGINS for c in o[2]}
ONAME=dict((o[0],o[1]) for o in ORIGINS)
# 真正大眾運輸完善的都會區才不推租車；北海道、九州、離島、東北自駕比例高
# 訂票通路 → (顯示名稱, 信任分級)  A=台灣可用 B=國際知名 C=台灣陌生
GATES={
 'Trip.com':('Trip.com','A'),'All Nippon Airways':('全日空官網','A'),
 'Japan Airlines':('日本航空官網','A'),'China Airlines':('中華航空官網','A'),
 'EVA Air':('長榮航空官網','A'),'STARLUX':('星宇航空官網','A'),
 'Kiwi.com':('Kiwi.com','B'),'Gotogate':('Gotogate','B'),'Mytrip.com':('Mytrip','B'),
 'Flightnetwork':('Flightnetwork','B'),'Vayama':('Vayama','B'),'Wowtickets':('Wowtickets','B'),
 'Expedia':('Expedia','B'),'Booking.com':('Booking.com','B'),
}
def gate_info(g):
    if g in GATES: return GATES[g]
    if g and any(x in g for x in ('Airlines','Airways','Air ')): return (g,'A')
    return (g or '其他平台','C')

URBAN={'tokyo','osaka','nagoya','fukuoka','kobe','kitakyushu'}
JPY=0.213  # 1 日圓 ≈ 0.213 台幣（概估，實際依匯率）
# 替代方案：目的地 → [(替代城市slug, 路線, 交通方式, 時間, 已查證票價 或 None)]
ALT={
 'kobe':[('osaka','關西機場 → 神戶','高速船／利木津巴士','約 30–70 分',None)],
 'okayama':[('osaka','新大阪 → 岡山','山陽新幹線','約 35–50 分','¥6,460')],
 'hiroshima':[('osaka','新大阪 → 廣島','山陽新幹線','約 1.5 小時','¥10,210'),
              ('fukuoka','博多 → 廣島','山陽新幹線','約 1 小時',None)],
 'yonago':[('osaka','新大阪 → 岡山 → 米子','新幹線＋特急やくも','約 4 小時',None)],
 'takamatsu':[('osaka','大阪 → 高松','高速巴士／JR快速','約 3.5 小時',None)],
 'matsuyama':[('osaka','大阪 → 松山','高速巴士','約 5.5 小時',None)],
 'kochi':[('osaka','大阪 → 高知','高速巴士','約 5 小時',None)],
 'kitakyushu':[('fukuoka','博多 → 小倉','山陽新幹線','約 20 分',None)],
 'saga':[('fukuoka','博多 → 佐賀','JR 特急','約 40 分',None)],
 'nagasaki':[('fukuoka','博多 → 長崎','特急接力海鷗＋西九州新幹線','約 1 小時 20 分','¥5,960')],
 'kumamoto':[('fukuoka','博多 → 熊本','九州新幹線','約 40 分','¥5,310（自由席）')],
 'oita':[('fukuoka','博多 → 別府','特急 Sonic','約 2 小時',None)],
 'miyazaki':[('fukuoka','博多 → 宮崎','高速巴士','約 4 小時',None)],
 'kagoshima':[('fukuoka','博多 → 鹿兒島中央','九州新幹線','約 1 小時 16 分',None)],
 'toyama':[('tokyo','東京 → 富山','北陸新幹線','約 2 小時 10 分',None),
           ('nagoya','名古屋 → 富山','特急 Hida','約 3.5 小時',None)],
 'kanazawa':[('tokyo','東京 → 金澤','北陸新幹線','約 2.5 小時',None),
             ('osaka','大阪 → 金澤','特急雷鳥號','約 2.5 小時',None)],
 'niigata':[('tokyo','東京 → 新潟','上越新幹線','約 2 小時',None)],
 'shizuoka':[('tokyo','東京 → 靜岡','東海道新幹線','約 1 小時',None),
             ('nagoya','名古屋 → 靜岡','東海道新幹線','約 1 小時',None)],
 'aomori':[('sendai','仙台 → 新青森','東北新幹線','約 1.5 小時',None),
           ('tokyo','東京 → 新青森','東北新幹線','約 3 小時',None)],
 'akita':[('tokyo','東京 → 秋田','秋田新幹線','約 4 小時',None)],
 'morioka':[('sendai','仙台 → 盛岡','東北新幹線','約 40 分',None),
            ('tokyo','東京 → 盛岡','東北新幹線','約 2 小時 15 分',None)],
 'fukushima':[('sendai','仙台 → 福島','東北新幹線','約 25 分',None),
              ('tokyo','東京 → 福島','東北新幹線','約 1.5 小時','約 ¥9,000')],
 'hakodate':[('sapporo','札幌 → 函館','特急北斗','約 3.5 小時',None)],
 'wakkanai':[('sapporo','札幌 → 稚內','特急宗谷／高速巴士','約 5–6 小時',None)],
 'ishigaki':[('okinawa','那霸 → 石垣島','日本國內線班機','約 1 小時',None)],
 'miyakojima':[('okinawa','那霸 → 宮古島','日本國內線班機','約 50 分',None)],
 'sendai':[('tokyo','東京 → 仙台','東北新幹線','約 1.5 小時','約 ¥11,400')],
}
ROUTE_MIN=5  # 票價數低於此值不開獨立頁，避免薄內容被判 doorway page
DEST={
 'CTS':('札幌・新千歲','北海道','札幌'),'SPK':('札幌','北海道','札幌'),'HKD':('函館','北海道','函館'),
 'WKJ':('稚內','北海道','稚內'),
 'SDJ':('仙台','宮城','仙台'),'AXT':('秋田','秋田','秋田'),'HNA':('花卷','岩手','盛岡'),
 'AOJ':('青森','青森','青森'),'FKS':('福島','福島','福島'),
 'NRT':('東京・成田','東京','東京'),'HND':('東京・羽田','東京','東京'),'TYO':('東京','東京','東京'),
 'NGO':('名古屋・中部','愛知','名古屋'),'KMQ':('小松','石川','金澤'),'TOY':('富山','富山','富山'),
 'KIJ':('新潟','新潟','新潟'),'FSZ':('靜岡','靜岡','靜岡'),
 'KIX':('大阪・關西','大阪','大阪'),'OSA':('大阪','大阪','大阪'),'UKB':('神戶','兵庫','神戶'),
 'HIJ':('廣島','廣島','廣島'),'OKJ':('岡山','岡山','岡山'),'YGJ':('米子','鳥取','米子'),
 'TAK':('高松','香川','高松'),'MYJ':('松山','愛媛','松山'),'KCZ':('高知','高知','高知'),
 'FUK':('福岡','福岡','福岡'),'KKJ':('北九州','福岡','北九州'),'HSG':('佐賀','佐賀','佐賀'),
 'KMJ':('熊本','熊本','熊本'),'OIT':('大分','大分','別府'),'KMI':('宮崎','宮崎','宮崎'),
 'KOJ':('鹿兒島','鹿兒島','鹿兒島'),'NGS':('長崎','長崎','長崎'),
 'OKA':('沖繩・那霸','沖繩','那霸'),'ISG':('石垣島','沖繩','石垣島'),
 'MMY':('宮古島','沖繩','宮古島'),'SHI':('下地島','沖繩','宮古島')}
# 城市 = SEO 頁面單位（合併機場）。slug, 中文名, [IATA], 地區slug, 訂房城市
CITIES=[
 ('tokyo','東京',['NRT','HND','TYO'],'kanto','東京'),
 ('osaka','大阪',['KIX','OSA'],'kansai','大阪'),
 ('okinawa','沖繩',['OKA'],'okinawa-islands','那霸'),
 ('fukuoka','福岡',['FUK'],'kyushu','福岡'),
 ('nagoya','名古屋',['NGO'],'chubu','名古屋'),
 ('sapporo','札幌',['CTS','SPK'],'hokkaido','札幌'),
 ('sendai','仙台',['SDJ'],'tohoku','仙台'),
 ('hakodate','函館',['HKD'],'hokkaido','函館'),
 ('kobe','神戶',['UKB'],'kansai','神戶'),
 ('kanazawa','金澤・小松',['KMQ'],'chubu','金澤'),
 ('toyama','富山',['TOY'],'chubu','富山'),
 ('niigata','新潟',['KIJ'],'chubu','新潟'),
 ('shizuoka','靜岡',['FSZ'],'chubu','靜岡'),
 ('hiroshima','廣島',['HIJ'],'chugoku','廣島'),
 ('okayama','岡山',['OKJ'],'chugoku','岡山'),
 ('yonago','米子・鳥取',['YGJ'],'chugoku','米子'),
 ('takamatsu','高松',['TAK'],'shikoku','高松'),
 ('matsuyama','松山',['MYJ'],'shikoku','松山'),
 ('kochi','高知',['KCZ'],'shikoku','高知'),
 ('kitakyushu','北九州',['KKJ'],'kyushu','北九州'),
 ('saga','佐賀',['HSG'],'kyushu','佐賀'),
 ('kumamoto','熊本',['KMJ'],'kyushu','熊本'),
 ('oita','大分・別府',['OIT'],'kyushu','別府'),
 ('miyazaki','宮崎',['KMI'],'kyushu','宮崎'),
 ('kagoshima','鹿兒島',['KOJ'],'kyushu','鹿兒島'),
 ('nagasaki','長崎',['NGS'],'kyushu','長崎'),
 ('ishigaki','石垣島',['ISG'],'okinawa-islands','石垣島'),
 ('miyakojima','宮古島',['MMY','SHI'],'okinawa-islands','宮古島'),
 ('akita','秋田',['AXT'],'tohoku','秋田'),
 ('aomori','青森',['AOJ'],'tohoku','青森'),
 ('morioka','盛岡・花卷',['HNA'],'tohoku','盛岡'),
 ('fukushima','福島',['FKS'],'tohoku','福島'),
 ('wakkanai','稚內',['WKJ'],'hokkaido','稚內'),
]
REGIONS=[('okinawa-islands','沖繩・離島'),('kyushu','九州'),('kansai','關西'),('kanto','關東'),
 ('chubu','中部・北陸'),('hokkaido','北海道'),('tohoku','東北'),('chugoku','中國'),('shikoku','四國')]
REGNAME=dict(REGIONS)
CITY_OF={code:c for c in CITIES for code in c[2]}
LCC_CAP,FSC_CAP=6000,8000
try:                                   # 一律以台北時間為準（CI 執行環境是 UTC）
    from zoneinfo import ZoneInfo
    NOW=datetime.datetime.now(ZoneInfo('Asia/Taipei'))
except Exception:
    NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
NOWS=NOW.strftime('%Y-%m-%d %H:%M'); TODAY=NOW.strftime('%Y-%m-%d')

def plink(kind,city='',**kw):
    p=P[kind]; t=p.get('template','')
    u=t if t and not t.startswith('TODO') else p['fallback']
    u=u.replace('{q}',urllib.parse.quote(city))
    for k,v in kw.items(): u=u.replace('{'+k+'}',str(v))
    return u

def flight_url(x):
    """以航班資料組出 Trip.com 搜尋連結（繁中 / TWD）"""
    return plink('flight', o=x['o'].lower(), d=x['d'].lower(),
                 dep=x['dep'], ret=x['ret'] or x['dep'],
                 tt='rt' if x['rt'] else 'ow')

def compare_line(city_name=''):
    alt=[k for k in ('flight2',) if k in P]
    if not alt: return ''
    ls='、'.join(
      f'<a href="{html.escape(plink(k,city_name))}" target="_blank" rel="nofollow noopener sponsored">'
      f'{P[k]["brand"]}</a>' for k in alt)
    return f'<p class="disc">票價僅供參考，建議到 {ls} 再比一次價——台灣 OTA 常有旅行社切位票，是國際比價站看不到的貨源。</p>'

GATE_FILTER = ('<div class="bar gatebar"><b>訂票通路</b>'
  '<button class="chip" id="gfAll" onclick="gf(0)">全部平台</button>'
  '<button class="chip" id="gfTw" onclick="gf(1)">只看台灣可訂 / 國際平台</button>'
  '<p class="disc" style="width:100%;margin-top:6px">'
  '這些紀錄來自不同訂票通路。標示「台灣較陌生」的多為東歐或俄語系網站，'
  '報價常低於台灣常用平台，但介面與客服未必支援中文。'
  '若想看與 Trip.com 同平台、比較容易對得上的紀錄，可切換下方選項。</p></div>'
  '<script>function gf(on){document.getElementById("gfAll").classList.toggle("on",!on);'
  'document.getElementById("gfTw").classList.toggle("on",!!on);'
  'document.querySelectorAll(".card[data-tier]").forEach(function(e){'
  'e.style.display=(on&&e.dataset.tier==="C")?"none":"";});}</script>')

# 城市 slug → Klook city_id（取自 Klook search suggest API，2026-09-10）
# 沒有對應城市的頁面不顯示 widget，避免在福島頁顯示東京的行程
KLOOK_CITY = {
 'tokyo':28, 'osaka':29, 'okinawa':6484, 'fukuoka':5209, 'nagoya':71,
 'sapporo':133938, 'sendai':17384, 'hakodate':119753, 'kobe':135,
 'kanazawa':445, 'toyama':21926, 'niigata':22144, 'shizuoka':6409,
 'hiroshima':5122, 'okayama':13088, 'yonago':11455, 'takamatsu':15969,
 'kochi':10000056, 'kitakyushu':22379, 'saga':14045, 'kumamoto':4351,
 'oita':8601, 'miyazaki':28941, 'kagoshima':21043, 'nagasaki':7057,
 'ishigaki':25166, 'miyakojima':24144, 'akita':11753, 'aomori':14493,
 'wakkanai':32,
}

def faq_block(name, fs, codes):
    """由現有票價資料自動生成常見問題，並輸出 FAQPage 結構化資料。
    每個答案都必須是資料能支撐的事實，且標明樣本來源，不作無根據推論。"""
    if not fs: return ''
    qa = []
    direct = [x for x in fs if x['tr'] == 0]
    lcc = sorted({x['airname'] for x in direct if x['cls'] == 'lcc'})
    fsc = sorted({x['airname'] for x in direct if x['cls'] == 'fsc'})

    # 1 有沒有直飛
    if direct:
        who = '、'.join(lcc + fsc) or '多家航空'
        qa.append((f'台灣有直飛{name}的班機嗎？',
                   f'有。本站近期紀錄中共有 {len(direct)} 筆直飛{name}的票價，'
                   f'執飛的航空公司包括{who}。'))
    else:
        qa.append((f'台灣有直飛{name}的班機嗎？',
                   f'本站近期紀錄中沒有直飛{name}的班機，查到的都是轉機航班。'
                   f'可考慮飛鄰近機場後轉乘日本國內交通。'))

    # 2 飛行時間
    ds = [x['dur_to'] for x in direct if x.get('dur_to')]
    if ds:
        m = min(ds)
        qa.append((f'台灣飛{name}要多久？',
                   f'直飛去程最短約 {m//60} 小時 {m%60} 分。'))

    # 3 價格區間
    rts = sorted(x['price'] for x in fs if x['rt'])
    if len(rts) >= 4:
        q1 = rts[len(rts)//4]          # 用四分位數，不用中位數
        med = rts[len(rts)//2]         # 中位數會被少數極高價拉高，拿來當「便宜門檻」會誤導
        qa.append((f'台灣飛{name}的機票大概多少錢？',
                   f'本站近期紀錄的來回含稅價最低 {money(rts[0])}，中位數約 {money(med)}。'
                   f'約四分之一的紀錄低於 {money(q1)}，'
                   f'因此看到 {money(q1)} 以下就算是相對便宜的價格。'
                   f'（此為歷史紀錄，實際售價請以訂票平台查詢為準）'))

    # 4 有哪些航空
    alla = sorted({x['airname'] for x in fs})
    if len(alla) > 1:
        parts = []
        if lcc: parts.append(f'廉價航空有{"、".join(lcc)}')
        if fsc: parts.append(f'一般航空有{"、".join(fsc)}')
        extra = [a for a in alla if a not in lcc + fsc]
        if extra: parts.append(f'另有經第三地轉機的{"、".join(extra[:4])}')
        qa.append((f'哪些航空公司飛{name}？', '。'.join(parts) + '。'))

    # 5 哪個月份便宜（樣本需夠分散才回答）
    bym = {}
    for x in fs:
        if x['rt']: bym.setdefault(x['dep'][:7], []).append(x['price'])
    if len(bym) >= 2:
        rank = sorted(((k, min(v), len(v)) for k, v in bym.items()), key=lambda t: t[1])
        best = rank[0]
        if best[2] >= 3:
            y, mo = best[0].split('-')
            qa.append((f'{name}機票什麼時候比較便宜？',
                       f'就本站目前涵蓋的期間而言，{y} 年 {int(mo)} 月出發的紀錄最低，'
                       f'來回含稅 {money(best[1])} 起。樣本僅涵蓋未來兩個月，'
                       f'不代表全年最低。'))

    # 6 哪個機場出發便宜
    byo = {}
    for x in fs:
        if x['rt'] and x['o'] in ORI: byo.setdefault(x['o'], []).append(x['price'])
    if len(byo) >= 2:
        rank = sorted(((k, min(v)) for k, v in byo.items()), key=lambda t: t[1])
        txt = '、'.join(f'{ORI[k]} {money(v)}' for k, v in rank)
        qa.append((f'從哪個機場飛{name}最便宜？',
                   f'各出發地的近期最低來回含稅價：{txt}。'))

    if not qa: return ''
    html_qa = ''.join(f'<details class="faq"><summary>{html.escape(q)}</summary>'
                      f'<div>{html.escape(a)}</div></details>' for q, a in qa)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                     "mainEntity": [{"@type": "Question", "name": q,
                                     "acceptedAnswer": {"@type": "Answer", "text": a}}
                                    for q, a in qa]}, ensure_ascii=False)
    return (f'<h2>關於{name}機票的常見問題</h2>{html_qa}'
            f'<script type="application/ld+json">{ld}</script>')


def klook_tours(slug, name):
    """依頁面城市顯示 Klook 行程 widget（繁中／TWD）"""
    cid = KLOOK_CITY.get(slug)
    tpl = (CFG.get('widgets') or {}).get('klook_tours', '')
    if not cid or not tpl: return ''
    return (f'<h2>{name}熱門行程與體驗</h2>'
            f'<p class="lede">由 Klook 提供，繁體中文介面、台幣計價，可直接預訂。</p>'
            f'<div class="widget">{tpl.replace("{city_id}", str(cid))}</div>'
            '<p class="disc">透過此區塊完成預訂時本站可獲得分潤，不影響你的價格。</p>')


def search_form(title, note, def_o='TPE', def_d='TYO'):
    """自製繁中搜尋表單，送往 Trip.com 繁中／TWD 搜尋頁。
    不用第三方 widget：避免英文介面、美金計價與 iframe 拖慢頁面。"""
    oo=''.join(f'<option value="{c}"{" selected" if c==def_o else ""}>{n}</option>'
               for c,n in ORI.items())
    seen=set(); dd=''
    for slug,name,codes,_,_ in CITIES:
        c=codes[0]
        if c in seen: continue
        seen.add(c)
        dd+=f'<option value="{c}"{" selected" if c==def_d else ""}>{name}</option>'
    return f'''<h2>{title}</h2><p class="lede">{note}</p>
<form class="sf" onsubmit="return sfGo(this)">
 <label>出發地<select name="o">{oo}</select></label>
 <label>目的地<select name="d">{dd}</select></label>
 <label>去程<input type="date" name="dep" required></label>
 <label>回程<input type="date" name="ret"></label>
 <button type="submit">搜尋票價</button>
</form>
<p class="disc">將前往 Trip.com 繁體中文頁面查詢即時票價（TWD 計價）。本站可能獲得分潤，不影響你的價格。</p>'''

SF_JS = ('<script>function sfGo(f){var o=f.o.value.toLowerCase(),d=f.d.value.toLowerCase(),'
         'a=f.dep.value,b=f.ret.value,t=b?"rt":"ow",'
         'u="https://tw.trip.com/flights/showfarefirst?dcity="+o+"&acity="+d+"&ddate="+a'
         '+(b?"&rdate="+b:"")+"&triptype="+t+"&class=y&quantity=1&locale=zh-TW&curr=TWD";'
         'window.open(u,"_blank","noopener");return false;}</script>')

def widget_block(kind,title,note,**kw):
    code=(W.get(kind) or '').strip()
    if not code: return ''          # 未設定嵌入碼時整區不顯示，不留空殼
    for k,v in kw.items(): code=code.replace('{'+k+'}',str(v))
    return (f'<h2>{title}</h2><p class="lede">{note}</p>'
            f'<div class="widget">{code}</div>')

def plabel(kind,city_name=''):
    p=P[kind]
    return f"{p['icon']} 到 {p['brand']} {p['label'].replace('{q}',city_name)}"

def load():
    rows=[]
    for f in ('/tmp/scan_all.json','/tmp/scan.json'):
        if os.path.exists(f): rows+=json.load(open(f))
    seen,out=set(),[]
    for r in rows:
        d=r.get('destination','')
        if d not in DEST: continue
        a=r.get('airline','')
        k=(r.get('origin'),d,r.get('departure_at','')[:10],r.get('return_at','')[:10],a,r.get('price'))
        if k in seen: continue
        seen.add(k)
        out.append(dict(o=r.get('origin'),d=d,air=a,airname=LCC.get(a) or FSC.get(a) or a,
            cls='lcc' if a in LCC else 'fsc' if a in FSC else 'other',
            price=r.get('price',0),dep=r.get('departure_at','')[:10],ret=r.get('return_at','')[:10],
            rt=bool(r.get('return_at')),tr=(r.get('transfers',0) or 0)+(r.get('return_transfers',0) or 0),
            dur=r.get('duration',0) or 0, dur_to=r.get('duration_to',0) or 0,
            gate=r.get('gate','') or '',
            url=f"https://www.aviasales.com{r['link']}&marker={MARKER}" if r.get('link') else ''))
    return out

CSS='''*{box-sizing:border-box}
/* 固定淺色主題：color-scheme 讓下拉選單與日期選擇器等原生元件也維持淺色，
   否則使用者系統為深色模式時表單控制項會變黑，與頁面不一致 */
:root{color-scheme:light;
--bg:#f7f7f5;--card:#fff;--fg:#1a1a1a;--dim:#63605c;--line:#e5e3de;--acc:#c2410c;
--hot:#dc2626;--lcc:#0f766e;--fsc:#4f46e5;--soft:#faf9f7}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px 72px}
a{color:var(--acc)}
.crumb{font-size:.8rem;color:var(--dim);padding:16px 0 0}
.crumb a{color:var(--dim);text-decoration:none}.crumb a:hover{color:var(--acc)}
h1{font-size:1.95rem;margin:14px 0 8px;letter-spacing:-.025em;line-height:1.3}
.lede{color:var(--dim);font-size:.95rem;margin:0 0 4px}
.upd{color:var(--dim);font-size:.78rem;margin:6px 0 0}
nav.top{position:sticky;top:0;z-index:20;background:var(--bg);padding:11px 0;margin-top:14px;
border-bottom:1px solid var(--line);display:flex;gap:15px;overflow-x:auto}
nav.top a{color:var(--dim);text-decoration:none;font-size:.86rem;white-space:nowrap;font-weight:500}
nav.top a:hover,nav.top a.cur{color:var(--acc)}
h2{font-size:1.28rem;margin:40px 0 6px;padding-bottom:8px;border-bottom:2px solid var(--acc)}
h3{font-size:1.02rem;margin:26px 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:11px;margin-top:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:13px 14px;
display:flex;flex-direction:column;gap:6px}
.card.hot{border-color:var(--hot)}
.rt{display:flex;align-items:center;gap:6px;font-size:.96rem;flex-wrap:wrap}
.rt i{color:var(--dim);font-style:normal}
.rt em{background:var(--hot);color:#fff;font-size:.66rem;padding:2px 6px;border-radius:4px;font-style:normal;font-weight:700}
.pr{font-size:1.5rem;font-weight:700;letter-spacing:-.02em;line-height:1.15}
.pr span{font-size:.68rem;font-weight:600;margin-left:6px;padding:2px 6px;border-radius:4px}
.pr .rtx{background:color-mix(in srgb,var(--acc) 14%,transparent);color:var(--acc)}
.pr .owx{background:var(--line);color:var(--dim)}
.mt{display:flex;gap:6px;flex-wrap:wrap;font-size:.78rem;color:var(--dim)}
.tg{padding:1px 6px;border-radius:4px;font-size:.69rem;font-weight:600}
.tg.lcc{background:color-mix(in srgb,var(--lcc) 15%,transparent);color:var(--lcc)}
.tg.fsc{background:color-mix(in srgb,var(--fsc) 15%,transparent);color:var(--fsc)}
.tg.other{background:var(--line);color:var(--dim)}
.gate{font-size:.73rem;color:var(--dim);display:flex;align-items:center;gap:6px;flex-wrap:wrap;
padding-top:6px;border-top:1px dashed var(--line)}
.gate b{color:var(--fg);font-weight:600}
.gate span{padding:1px 6px;border-radius:4px;font-size:.66rem;font-weight:600}
.gate.ga span{background:color-mix(in srgb,var(--lcc) 18%,transparent);color:var(--lcc)}
.gate.gb span{background:var(--line);color:var(--dim)}
.gate.gc span{background:color-mix(in srgb,var(--hot) 14%,transparent);color:var(--hot)}
.dt{font-size:.81rem;color:var(--dim);font-variant-numeric:tabular-nums}
.btn{margin-top:auto;display:block;text-align:center;background:var(--acc);color:#fff;
text-decoration:none;padding:7px;border-radius:7px;font-size:.83rem;font-weight:600}
.cities{display:grid;grid-template-columns:repeat(auto-fill,minmax(196px,1fr));gap:9px;margin-top:12px}
.ct{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:12px 13px;text-decoration:none;color:var(--fg)}
.ct:hover{border-color:var(--acc)}
.ct b{display:block;font-size:1rem}
.ct s{display:block;font-size:.74rem;color:var(--dim);text-decoration:none;margin-top:1px}
.ct u{display:block;font-size:.95rem;color:var(--acc);text-decoration:none;font-weight:700;margin-top:6px}
.ct u small{font-weight:400;font-size:.7rem;color:var(--dim)}
.plinks{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}
.plink{flex:1 1 190px;text-align:center;border:1px solid var(--line);background:var(--card);
color:var(--fg);text-decoration:none;padding:11px 13px;border-radius:9px;font-size:.88rem;font-weight:600}
.plink:hover{border-color:var(--acc);color:var(--acc)}
table{width:100%;border-collapse:collapse;margin-top:12px;font-size:.87rem}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}
th{color:var(--dim);font-weight:600;font-size:.79rem}
td b{color:var(--acc)}
.tldr{background:var(--soft);border:1px solid var(--line);border-left:4px solid var(--acc);
border-radius:10px;padding:16px 18px 16px 34px;margin-top:12px}
.tldr ul{margin:0;padding-left:2px}
.tldr li{margin-bottom:9px;font-size:.94rem;line-height:1.75}
.tldr li:last-child{margin-bottom:0}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:12px}
.tw table{min-width:640px;font-size:.84rem}
.tw th,.tw td{white-space:nowrap;padding:9px 11px}
.tw td.win{color:var(--lcc);font-weight:700}
.tw td.lose{color:var(--acc);font-weight:700}
.cta{display:flex;align-items:center;gap:14px;margin-top:14px;padding:15px 18px;
background:var(--card);border:1px solid var(--line);border-radius:12px;
text-decoration:none;color:var(--fg)}
.cta:hover{border-color:var(--acc)}
.cta .ci{font-size:1.5rem;flex:0 0 auto}
.cta .ct{flex:1;display:flex;flex-direction:column;gap:2px}
.cta .ct b{font-size:.98rem;font-weight:700}
.cta .ct s{text-decoration:none;font-size:.82rem;color:var(--dim)}
.cta .ca{color:var(--acc);font-weight:700;font-size:1.1rem;flex:0 0 auto}
details.faq{background:var(--card);border:1px solid var(--line);border-radius:10px;
margin-top:8px;padding:0}
details.faq summary{cursor:pointer;padding:13px 15px;font-weight:600;font-size:.95rem;
list-style:none;display:flex;justify-content:space-between;align-items:center;gap:10px}
details.faq summary::-webkit-details-marker{display:none}
details.faq summary::after{content:"＋";color:var(--acc);font-weight:700;flex:0 0 auto}
details.faq[open] summary::after{content:"－"}
details.faq summary:hover{color:var(--acc)}
details.faq>div{padding:0 15px 14px;font-size:.9rem;color:var(--dim);line-height:1.8}
.sf{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;margin-top:12px;
padding:16px;background:var(--soft);border:1px solid var(--line);border-radius:12px}
.sf label{display:flex;flex-direction:column;gap:5px;font-size:.78rem;color:var(--dim);flex:1 1 150px}
.sf select,.sf input{font:inherit;font-size:.92rem;padding:9px 10px;border-radius:8px;
border:1px solid var(--line);background:var(--card);color:var(--fg);width:100%}
.sf button{font:inherit;font-weight:700;font-size:.92rem;padding:10px 22px;border:0;
border-radius:8px;background:var(--acc);color:#fff;cursor:pointer;flex:0 0 auto}
.sf button:hover{opacity:.9}
@media(max-width:520px){.sf label{flex:1 1 100%}.sf button{width:100%}}
.widget{margin:12px 0 0;min-height:60px}
.widget iframe{max-width:100%;border:0}
.gatebar{margin:16px 0 0;padding:12px 14px;background:var(--soft);border:1px solid var(--line);border-radius:10px}
.disc{font-size:.76rem;color:var(--dim);margin:8px 0 0;line-height:1.6}
.note{margin-top:52px;padding-top:20px;border-top:1px solid var(--line);font-size:.79rem;color:var(--dim);line-height:1.85}
.note a{color:var(--dim)}
@media(max-width:520px){h1{font-size:1.5rem}.grid{grid-template-columns:1fr}}'''

DRIVE_SRC = "https://tpembars.com/NTcyMTY4.js?t=572168"
DRIVE = ('<script nowprocket data-noptimize="1" data-cfasync="false" '
         'data-wpfc-render="false" seraph-accel-crit="1" data-no-defer="1" data-cmp-ab="2">'
         '(function(){var s=document.createElement("script");s.async=1;'
         's.setAttribute("data-cmp-ab","2");s.src=' + repr(DRIVE_SRC).replace('"',"'") + ';'
         'document.head.appendChild(s);})();</script>')

def head(title,desc,path,extra=''):
    can=f'{SITE}{BASE}/{path}' if path else f'{SITE}{BASE}/'
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google-site-verification" content="lL18Diq98hRIL65-BKEiZ-mhQ2DNyf0WYwRpRBiT-Rk">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{can}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{can}">
<style>{CSS}</style>{extra}{DRIVE}</head><body><div class="wrap">'''

def crumbs(items,root='/'):
    parts=[]; ld=[]
    for i,(name,url) in enumerate(items):
        parts.append(f'<a href="{U(url)}">{name}</a>' if url else f'<span>{name}</span>')
        ld.append({"@type":"ListItem","position":i+1,"name":name,
                   "item":(SITE+U(url) if url else None)})
    j=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":ld},
                 ensure_ascii=False)
    return f'<div class="crumb">{" › ".join(parts)}</div>' \
           f'<script type="application/ld+json">{j}</script>'

def topnav(cur=''):
    ls=''.join(f'<a href="{U("/"+s+"/")}"{" class=cur" if s==cur else ""}>{n}</a>' for s,n in REGIONS)
    return (f'<nav class="top"><a href="{U("/")}"{" class=cur" if not cur else ""}>首頁</a>'
            f'<a href="{U("/deals/")}">🔥 機票特價</a>'
            f'<a href="{U("/apple-japan-price/")}">🍎 台日 Apple 價差</a>{ls}</nav>')

def foot():
    return f'''<p class="note">
票價資料來源為 Aviasales 資料庫，價格為單人含稅及手續費，僅供參考，隨時可能變動。<br>
實際訂購由合作平台完成：機票 Trip.com、住宿 Agoda、行程與交通票 KKday、網卡與租車 Klook。<br>
本站連結為聯盟行銷連結，透過連結完成訂購時本站可獲得分潤，不影響你的價格。<br>
最後更新 {NOWS}　·　<a href="{U("/")}">回首頁</a>
</p></div>{SF_JS}</body></html>'''

def fare_card(x,hot=False):
    tag={'lcc':'廉航','fsc':'一般航空'}.get(x['cls'],'其他')
    cn=CITY_OF[x['d']][1]
    stops='直飛' if x['tr']==0 else f"轉機{x['tr']}"
    trip='來回' if x['rt'] else '單程'
    dates=x['dep']+(f" – {x['ret']}" if x['ret'] else '')
    # 措辭需與上方「近期最低紀錄」區隔：紀錄是過去的，按鈕是去查現在的價
    btn=(f'<a class="btn" href="{html.escape(flight_url(x))}" target="_blank" '
         f'rel="nofollow noopener sponsored">✈️ 到 {P["flight"]["brand"]} 查這天目前票價</a>')
    gname,tier=gate_info(x.get('gate',''))
    gcls={'A':'ga','B':'gb','C':'gc'}[tier]
    gtxt={'A':'台灣可訂','B':'國際平台','C':'台灣較陌生'}[tier]
    is_trip = (x.get('gate') == 'Trip.com')
    if is_trip:
        gate_html=('<div class="gate ga">📊 近期最低紀錄　來源 <b>Trip.com</b>'
                   '<span>同平台可查</span></div>')
    else:
        gate_html=(f'<div class="gate {gcls}">📊 近期最低紀錄　來源 '
                   f'<b>{html.escape(gname)}</b><span>{gtxt}</span></div>')
    return f'''<article class="card{' hot' if hot else ''}" data-tier="{tier}">
<div class="rt"><b>{ORI.get(x['o'],x['o'])}</b><i>→</i><b>{cn}</b>{'<em>超值</em>' if hot else ''}</div>
<div class="pr">NT${x['price']:,}<span class="{'rtx' if x['rt'] else 'owx'}">{trip}含稅</span></div>
<div class="mt"><span class="tg {x['cls']}">{tag}</span><span>{html.escape(x['airname'])}</span><span>{stops}</span></div>
<div class="dt">{dates}</div>{gate_html}{btn}</article>'''

def cta(kind, city_name, hotel_city, headline, sub):
    """單一情境式 CTA。
    不再把 4–5 個夥伴連結並排——Travelpayouts 官方明言「一段五個連結會失去信任」，
    競品分析也顯示成效好的頁面是把連結嵌在相關段落，而非集中成一排按鈕。"""
    p = P[kind]
    return (f'<a class="cta" href="{html.escape(plink(kind, hotel_city))}" target="_blank" '
            f'rel="nofollow noopener sponsored">'
            f'<span class="ci">{p["icon"]}</span>'
            f'<span class="ct"><b>{html.escape(headline)}</b><s>{html.escape(sub)}</s></span>'
            f'<span class="ca">→</span></a>')


def partner_links(city_name, hotel_city, slug=None):
    """保留給尚未改為情境式配置的頁面（航線頁、deal 貼文），至多兩個連結。"""
    keys = ['hotel', 'esim']
    ls = ''.join(
        f'<a class="plink" href="{html.escape(plink(k,hotel_city))}" target="_blank" '
        f'rel="nofollow noopener sponsored">{plabel(k,city_name)}</a>' for k in keys)
    return (f'<div class="plinks">{ls}</div>'
            '<p class="disc">以上連結會前往合作訂票平台完成預訂，本站可能獲得分潤，不影響你的價格。</p>')

def alt_calc(slug):
    """回傳 [(替代城市slug, 機票最低, 交通TWD單程 or None, 總計 or None, route, mode, tm, fare)]"""
    out=[]
    for aslug,route,mode,tm,fare in (ALT.get(slug) or []):
        ac=CITY.get(aslug); af=by_city.get(aslug) or []
        if not ac or not af: continue
        b=best(af,True) or best(af,False)
        jpy=None
        if fare:
            m=re.search(r'([\d,]+)',fare)
            if m: jpy=int(m.group(1).replace(',',''))
        twd=int(jpy*JPY) if jpy else None
        out.append((aslug,b,twd,(b['price']+twd*2) if twd else None,route,mode,tm,fare))
    return out

def alt_block(slug,name,hotelcity,own_min=None):
    alts=alt_calc(slug)
    if not alts: return ''
    rows=''
    for aslug,b,twd,total_v,route,mode,tm,fare in alts:
        ac=CITY[aslug]
        save=(own_min-total_v) if (own_min and total_v and own_min>total_v) else 0
        total=(f'<b>約 {money(total_v)}</b>'+(f'<br><small style="color:var(--hot);font-weight:700">省 {money(save)}</small>' if save else '')
               if total_v else '<span style="color:var(--dim)">機票＋交通另計</span>')
        farecell=(f'{fare}<br><small style="color:var(--dim)">約 NT${twd:,} 單程</small>'
                  if twd else '<a href="'+html.escape(plink("transport",ac[4]))+'" target="_blank" rel="nofollow noopener sponsored">到 '+P["transport"]["brand"]+' 查詢</a>')
        rows+=(f'<tr><td><a href="{U(f"/{aslug}/")}">{ac[1]}</a><br>'
               f'<small style="color:var(--dim)">機票 {money(b["price"])} 起</small></td>'
               f'<td>{route}<br><small style="color:var(--dim)">{mode}</small></td>'
               f'<td>{tm}</td><td>{farecell}</td><td>{total}</td></tr>')
    if not rows: return ''
    note=('<p class="lede" style="font-size:.86rem">日圓票價依 1 日圓 ≈ 0.213 台幣概估，'
          '交通費以來回兩趟計算。實際票價請以 JR 官網或購票平台為準。</p>')
    cheaper=[a for a in alts if a[3] and own_min and a[3]<own_min]
    if cheaper:
        bestalt=min(cheaper,key=lambda a:a[3])
        hd=(f'<h2>飛{CITY[bestalt[0]][1]}再轉乘，比直飛便宜 {money(own_min-bestalt[3])}</h2>'
            f'<p class="lede">直飛{name}最低 {money(own_min)}，但飛到{CITY[bestalt[0]][1]}'
            f'（{money(bestalt[1]["price"])}）再搭{bestalt[5]}（{bestalt[6]}），'
            f'總計約 <b>{money(bestalt[3])}</b>。</p>')
    else:
        hd=(f'<h2>飛不到{name}？從鄰近機場轉乘</h2>'
            f'<p class="lede">台灣目前沒有直飛{name}的便宜票，可以飛到下列機場再轉乘日本國內交通。</p>')
    return (hd +
            f'<table><thead><tr><th>替代機場</th><th>轉乘路線</th><th>時間</th>'
            f'<th>單程交通費</th><th>估算總計</th></tr></thead><tbody>{rows}</tbody></table>{note}'
            + '<div class="plinks">'
            + f'<a class="plink" href="{html.escape(plink("transport",hotelcity))}" target="_blank" '
              f'rel="nofollow noopener sponsored">{plabel("transport",name)}</a>'
            + f'<a class="plink" href="{html.escape(plink("car",hotelcity))}" target="_blank" '
              f'rel="nofollow noopener sponsored">{plabel("car",name)}</a>'
            + '</div>'
            + '<p class="disc">以上連結會前往合作訂票平台完成預訂，本站可能獲得分潤，不影響你的價格。</p>')

def write(path,content):
    d=os.path.dirname(path)
    if d: os.makedirs(d,exist_ok=True)
    open(path,'w',encoding='utf-8').write(content)

# ---------- 建構資料 ----------
deals=load()
by_city=collections.defaultdict(list)
for x in deals:
    c=CITY_OF.get(x['d'])
    if c: by_city[c[0]].append(x)
CITY=dict((c[0],c) for c in CITIES)

def best(fs,rt=None):
    p=[x for x in fs if (rt is None or x['rt']==rt)]
    return min(p,key=lambda x:x['price']) if p else None

def money(n): return f'NT${n:,}'

pages=[]  # (url, lastmod, priority)

# ---------- 城市頁 ----------
for slug,name,codes,reg,hotelcity in CITIES:
    fs=by_city.get(slug,[])
    br=best(fs,True); bo=best(fs,False)
    anchor=br or bo
    if anchor:
        pt=('來回' if anchor['rt'] else '單程')
        title=f'{name}機票｜台灣飛{name}最低 {money(anchor["price"])} {pt}含稅（{NOW.year}年更新）'
        desc=(f'台北、台中、高雄飛{name}的便宜機票整理，目前最低 {money(anchor["price"])} {pt}含稅，'
              f'由{anchor["airname"]}提供。共 {len(fs)} 筆票價，含航空公司、日期與轉機資訊，每日更新。')
    else:
        title=f'{name}機票｜台灣沒有直飛？鄰近機場轉乘方案與費用試算'
        a=ALT.get(slug) or []
        via='、'.join(CITY[x[0]][1] for x in a if CITY.get(x[0]))
        desc=(f'台灣目前沒有直飛{name}的便宜機票。'
              + (f'可改飛{via}再轉乘日本國內交通，本頁提供路線、時間與費用試算。' if via
                 else f'本頁提供{name}機票即時查詢與住宿建議。'))
    airs=collections.Counter(x['airname'] for x in fs)
    oris=collections.Counter(x['o'] for x in fs)

    intro=f'<p class="lede">'
    if anchor:
        lccs=[a for a in airs if a in LCC.values()]
        intro+=f'台灣飛{name}目前最低 <b>{money(anchor["price"])}</b>（{pt}含稅，{anchor["airname"]}，{anchor["dep"]} 出發）。'
        if lccs: intro+=f'飛{name}的廉價航空有 {"、".join(lccs[:4])}。'
        if len(oris)>1:
            intro+=f'{"、".join(ORI[o] for o in oris)} 都有航班。'
    else:
        intro+=f'目前快取中沒有台灣飛{name}的票價，可點下方查詢即時價格。'
    intro+='</p>'

    body=''
    if fs:
        rts=sorted([x for x in fs if x['rt']],key=lambda x:x['price'])[:12]
        ows=sorted([x for x in fs if not x['rt']],key=lambda x:x['price'])[:8]
        body+=search_form(f'查台灣飛{name}的即時票價',
              '選好日期即可查詢目前實際可訂的價格。', 'TPE', codes[0])
        body+=(f'<h2 id="ref">近期行情參考</h2><p class="lede">'
               f'以下是 {NOWS} 從各訂票通路蒐集到的<b>近期最低紀錄</b>，用來判斷目前價格算不算便宜。'
               f'紀錄來源平台已標示於每張卡片上；<b>這些價格不代表現在仍可訂購</b>，'
               f'點卡片下方按鈕可到 Trip.com 查該日期目前的實際票價。</p>')
        body+=GATE_FILTER
        if rts:
            body+=(f'<h3>來回機票</h3><div class="grid">'
                   +''.join(fare_card(x) for x in rts)+'</div>'+compare_line(name))
        if ows:
            body+=f'<h3>單程機票</h3><div class="grid">'+''.join(fare_card(x) for x in ows)+'</div>'
        if len(airs)>1:
            rows=''
            for a,n in airs.most_common():
                sub=[x for x in fs if x['airname']==a]
                r=[x['price'] for x in sub if x['rt']]; w=[x['price'] for x in sub if not x['rt']]
                rows+=(f'<tr><td>{html.escape(a)}</td>'
                       f'<td>{"廉航" if a in LCC.values() else "一般航空" if a in FSC.values() else "—"}</td>'
                       f'<td>{"<b>"+money(min(r))+"</b>" if r else "—"}</td>'
                       f'<td>{money(min(w)) if w else "—"}</td><td>{n} 筆</td></tr>')
            body+=(f'<h2>飛{name}的航空公司</h2><table><thead><tr><th>航空公司</th><th>類型</th>'
                   f'<th>來回最低</th><th>單程最低</th><th>票價數</th></tr></thead><tbody>{rows}</tbody></table>')
        if len(oris)>1:
            og=collections.Counter(ORI_OF[x['o']][0] for x in fs if x['o'] in ORI_OF)
            rows=''
            for o,n in og.most_common():
                sub=[x for x in fs if ORI_OF.get(x['o'],('',))[0]==o]
                r=[x['price'] for x in sub if x['rt']]; w=[x['price'] for x in sub if not x['rt']]
                lbl=(f'<a href="{U(f"/{o}/{slug}/")}">{ONAME[o]}飛{name}</a>'
                     if n>=ROUTE_MIN else ONAME[o])
                rows+=(f'<tr><td>{lbl}</td><td>{"<b>"+money(min(r))+"</b>" if r else "—"}</td>'
                       f'<td>{money(min(w)) if w else "—"}</td><td>{n} 筆</td></tr>')
            body+=(f'<h2>各出發地飛{name}比價</h2><table><thead><tr><th>出發地</th>'
                   f'<th>來回最低</th><th>單程最低</th><th>票價數</th></tr></thead><tbody>{rows}</tbody></table>')
    else:
        body+=(f'<h2>查詢台灣飛{name}即時票價</h2>'
               f'<p><a class="plink" style="display:inline-block;flex:none" '
               f'href="{html.escape(plink("flight",o="tpe",d=codes[0].lower(),dep="",ret="",tt="rt"))}" target="_blank" '
               f'rel="nofollow noopener sponsored">✈️ 到 {P["flight"]["brand"]} 查詢{name}機票</a></p>')

    own_min = anchor['price'] if anchor else None
    _alts = alt_calc(slug)
    _cheaper = any(a[3] and own_min and a[3] < own_min for a in _alts)
    if len(fs) < ROUTE_MIN or _cheaper:
        body += alt_block(slug,name,hotelcity,own_min)
    # 看完票價 → 下一步就是找住宿，放在這裡最順
    if fs:
        body+=cta('hotel',name,hotelcity,f'看好機票了？接著找{name}的住宿',
                  f'到 Agoda 查{name}房價，繁體中文、台幣計價')
    body+=faq_block(name,fs,codes)
    body+=klook_tours(slug,name)
    if slug not in URBAN:
        body+=cta('car',name,hotelcity,f'{name}自駕比較方便',
                  '到 Klook 比較租車方案')
    body+=cta('esim',name,hotelcity,'出發前別忘了日本上網',
              '到 Klook 買 eSIM 或網卡，落地就能用')
    body+='<p class="disc">以上連結會前往合作訂票平台完成預訂，本站可能獲得分潤，不影響你的價格。</p>'
    sib=[c for c in CITIES if c[3]==reg and c[0]!=slug]
    if sib:
        body+=(f'<h2>{REGNAME[reg]}其他航點</h2><div class="cities">'+''.join(
            f'<a class="ct" href="{U("/"+s+"/")}"><b>{n}</b><s>{REGNAME[r]}</s>'
            + (f'<u>{money(best(by_city.get(s,[]))["price"])}<small> 起</small></u>' if by_city.get(s) else '<u style="color:var(--dim);font-weight:400;font-size:.8rem">查詢票價</u>')
            + '</a>' for s,n,_,r,_ in sib)+'</div>')

    write(f'{slug}/index.html', head(title,desc,f'{slug}/')
        + crumbs([('首頁','/'),(REGNAME[reg],f'/{reg}/'),(f'{name}機票',None)])
        + topnav(reg) + f'<h1>{name}機票</h1>' + intro
        + f'<p class="upd">更新於 {NOWS}　·　共 {len(fs)} 筆票價</p>' + body + foot())
    pages.append((f'/{slug}/',0.8 if fs else 0.5))

# ---------- 地區頁（導覽用，非 SEO 主力）----------
for reg,rname in REGIONS:
    cs=[c for c in CITIES if c[3]==reg]
    cs.sort(key=lambda c: best(by_city.get(c[0],[]))['price'] if by_city.get(c[0]) else 10**9)
    n=sum(len(by_city.get(c[0],[])) for c in cs)
    b=min([best(by_city.get(c[0],[]))['price'] for c in cs if by_city.get(c[0])] or [0])
    title=f'{rname}機票｜台灣飛{rname}各城市便宜機票一覽'
    desc=f'台灣飛{rname}（{"、".join(c[1] for c in cs[:5])}）的機票比較，' + (f'最低 {money(b)} 起，' if b else '') + f'共 {n} 筆票價，每日更新。'
    cards=''.join(
        f'<a class="ct" href="{U("/"+s+"/")}"><b>{nm}</b><s>{"、".join(DEST[k][1] for k in codes if k in DEST)}</s>'
        + (f'<u>{money(best(by_city[s])["price"])}<small> 起 · {len(by_city[s])} 筆</small></u>'
           if by_city.get(s) else '<u style="color:var(--dim);font-weight:400;font-size:.8rem">查詢票價</u>')
        + '</a>' for s,nm,codes,_,_ in cs)
    write(f'{reg}/index.html', head(title,desc,f'{reg}/')
        + crumbs([('首頁','/'),(f'{rname}機票',None)]) + topnav(reg)
        + f'<h1>{rname}機票</h1><p class="lede">台灣飛{rname}共 {len(cs)} 個航點'
        + (f'，目前最低 <b>{money(b)}</b>。' if b else '。') + '點選城市查看詳細票價。</p>'
        + f'<p class="upd">更新於 {NOWS}</p><div class="cities">{cards}</div>' + foot())
    pages.append((f'/{reg}/',0.6))

# ---------- 出發地頁 & 航線頁 ----------
by_route=collections.defaultdict(list)
by_origin=collections.defaultdict(list)
for x in deals:
    c=CITY_OF.get(x['d']); o=ORI_OF.get(x['o'])
    if not c or not o: continue
    by_route[(o[0],c[0])].append(x)
    by_origin[o[0]].append(x)

route_pages=set()
for (oslug,cslug),fs in by_route.items():
    if len(fs)<ROUTE_MIN: continue
    route_pages.add((oslug,cslug))
    oname=ONAME[oslug]; city=CITY[cslug]; cname=city[1]; reg=city[3]; hotelcity=city[4]
    br=best(fs,True); bo=best(fs,False); anc=br or bo
    pt='來回' if anc['rt'] else '單程'
    title=f'{oname}飛{cname}機票｜最低 {money(anc["price"])} {pt}含稅（{NOW.year}年更新）'
    desc=(f'{oname}出發飛{cname}的便宜機票整理，目前最低 {money(anc["price"])} {pt}含稅，'
          f'由{anc["airname"]}提供，{anc["dep"]} 出發。共 {len(fs)} 筆票價，含航空公司與轉機資訊。')
    airs=collections.Counter(x['airname'] for x in fs)
    dirs=[x for x in fs if x['tr']==0]
    intro=f'<p class="lede">{oname}飛{cname}目前最低 <b>{money(anc["price"])}</b>'
    intro+=f'（{pt}含稅，{anc["airname"]}，{anc["dep"]} 出發）。'
    if dirs:
        md=min(x['dur'] for x in dirs if x['dur'])if any(x['dur'] for x in dirs) else 0
        intro+=f'有 {len(dirs)} 筆直飛航班'+(f'，最短飛行時間約 {md//60} 小時 {md%60} 分。' if md else '。')
    else:
        intro+='目前皆為轉機航班。'
    intro+=f'共 {len(airs)} 家航空公司經營此航線。</p>'
    _o={'taipei':'TPE','taichung':'RMQ','kaohsiung':'KHH','tainan':'TNN'}.get(oslug,'TPE')
    body=search_form(f'查{oname}飛{cname}的即時票價',
          '選好日期即可查詢目前實際可訂的價格。', _o, city[2][0])
    body+=f'<h2 id="ref">近期行情參考</h2><p class="lede">以下為 {NOWS} 查詢到的價格，供了解行情用；實際票價請以上方即時查詢或訂票平台為準。</p>'
    body+=GATE_FILTER
    rts=sorted([x for x in fs if x['rt']],key=lambda x:x['price'])[:12]
    ows=sorted([x for x in fs if not x['rt']],key=lambda x:x['price'])[:8]
    if rts: body+=(f'<h3>來回機票</h3><div class="grid">'
                   +''.join(fare_card(x) for x in rts)+'</div>'+compare_line(cname))
    if ows: body+=f'<h3>單程機票</h3><div class="grid">'+''.join(fare_card(x) for x in ows)+'</div>'
    if len(airs)>1:
        rows=''
        for a,n in airs.most_common():
            sub=[x for x in fs if x['airname']==a]
            r=[x['price'] for x in sub if x['rt']]; w=[x['price'] for x in sub if not x['rt']]
            rows+=(f'<tr><td>{html.escape(a)}</td>'
                   f'<td>{"廉航" if a in LCC.values() else "一般航空" if a in FSC.values() else "—"}</td>'
                   f'<td>{"<b>"+money(min(r))+"</b>" if r else "—"}</td>'
                   f'<td>{money(min(w)) if w else "—"}</td><td>{n} 筆</td></tr>')
        body+=(f'<h2>{oname}飛{cname}的航空公司</h2><table><thead><tr><th>航空公司</th><th>類型</th>'
               f'<th>來回最低</th><th>單程最低</th><th>票價數</th></tr></thead><tbody>{rows}</tbody></table>')
    body+=klook_tours(cslug,cname)
    body+=f'<h2>{cname}住宿・上網・行程</h2>'+partner_links(cname,hotelcity,cslug)
    body+=(f'<h2>其他選擇</h2><div class="cities">'
           f'<a class="ct" href="{U(f"/{cslug}/")}"><b>{cname}機票總覽</b><s>比較所有出發地</s></a>'
           f'<a class="ct" href="{U(f"/{oslug}/")}"><b>{oname}飛日本</b><s>看所有目的地</s></a></div>')
    write(f'{oslug}/{cslug}/index.html', head(title,desc,f'{oslug}/{cslug}/')
        + crumbs([('首頁','/'),(f'{oname}出發',f'/{oslug}/'),(f'{oname}飛{cname}機票',None)])
        + topnav(reg) + f'<h1>{oname}飛{cname}機票</h1>' + intro
        + f'<p class="upd">更新於 {NOWS}　·　共 {len(fs)} 筆票價</p>' + body + foot())
    pages.append((f'/{oslug}/{cslug}/',0.9))

for oslug,oname,codes in ORIGINS:
    fs=by_origin.get(oslug,[])
    if not fs: continue
    b=best(fs,True) or best(fs,False)
    dests=sorted({CITY_OF[x['d']][0] for x in fs},
                 key=lambda c: min(y['price'] for y in fs if CITY_OF[y['d']][0]==c))
    title=f'{oname}飛日本機票｜{len(dests)} 個航點比價，最低 {money(b["price"])}（{NOW.year}年更新）'
    desc=(f'{oname}出發飛日本 {len(dests)} 個城市的機票整理，最低 {money(b["price"])}'
          f'（{"來回" if b["rt"] else "單程"}含稅，{b["airname"]}）。共 {len(fs)} 筆票價，每日更新。')
    cards=''
    for c in dests:
        sub=[x for x in fs if CITY_OF[x['d']][0]==c]
        mp=min(x['price'] for x in sub)
        href=U(f'/{oslug}/{c}/') if (oslug,c) in route_pages else U(f'/{c}/')
        cards+=(f'<a class="ct" href="{href}"><b>{oname} → {CITY[c][1]}</b>'
                f'<s>{REGNAME[CITY[c][3]]}</s><u>{money(mp)}<small> 起 · {len(sub)} 筆</small></u></a>')
    write(f'{oslug}/index.html', head(title,desc,f'{oslug}/')
        + crumbs([('首頁','/'),(f'{oname}飛日本機票',None)]) + topnav()
        + f'<h1>{oname}飛日本機票</h1>'
        + f'<p class="lede">{oname}出發飛日本共 <b>{len(dests)}</b> 個航點，目前最低 <b>{money(b["price"])}</b>。點選目的地查看詳細票價。</p>'
        + f'<p class="upd">更新於 {NOWS}　·　共 {len(fs)} 筆票價</p><div class="cities">{cards}</div>' + foot())
    pages.append((f'/{oslug}/',0.85))

# ---------- 首頁 ----------
hot=sorted([x for x in deals if x['rt'] and
  ((x['cls']=='lcc' and x['price']<LCC_CAP) or (x['cls']=='fsc' and x['price']<FSC_CAP))],
  key=lambda x:x['price'])
allbest=min([x['price'] for x in deals if x['rt']] or [0])
title=f'台日機票速報｜台灣飛日本便宜機票，{NOW.year}年最低 {money(allbest)} 來回含稅'
desc=(f'台北、台中、高雄、台南飛日本 {len(CITIES)} 個城市的便宜機票整理，含稅價格、航空公司、'
      f'日期一次看。目前最低 {money(allbest)} 來回含稅，每日更新。')
sections=''
for reg,rname in REGIONS:
    cs=[c for c in CITIES if c[3]==reg]
    cs.sort(key=lambda c: best(by_city.get(c[0],[]))['price'] if by_city.get(c[0]) else 10**9)
    cards=''.join(
        f'<a class="ct" href="{U("/"+s+"/")}"><b>{nm}</b><s>{REGNAME[reg]}</s>'
        + (f'<u>{money(best(by_city[s])["price"])}<small> 起</small></u>'
           if by_city.get(s) else '<u style="color:var(--dim);font-weight:400;font-size:.8rem">查詢票價</u>')
        + '</a>' for s,nm,_,_,_ in cs)
    sections+=f'<h2 id="{reg}"><a href="{U("/"+reg+"/")}" style="text-decoration:none;color:inherit">{rname}</a></h2><div class="cities">{cards}</div>'

write('index.html', head(title,desc,'')
  + crumbs([('首頁',None)]) + topnav()
  + f'<h1>台日機票速報</h1>'
  + f'<p class="lede">台灣飛日本 <b>{len(CITIES)}</b> 個城市的便宜機票整理，價格含稅含手續費。'
    f'目前最低 <b>{money(allbest)}</b> 來回含稅。</p>'
  + f'<p class="upd">更新於 {NOWS}　·　共 {len(deals)} 筆票價</p>'
  + (f'<h2>🔥 超值票</h2><p class="lede" style="font-size:.85rem">廉航低於 {money(LCC_CAP)}／一般航空低於 {money(FSC_CAP)}</p>'
     + GATE_FILTER + f'<div class="grid">{"".join(fare_card(x,True) for x in hot[:12])}</div>' if hot else '')
  + '<h2>其他實用資訊</h2><div class="cities">'
  + f'<a class="ct" href="{U("/apple-japan-price/")}"><b>🍎 日本買 iPhone 划算嗎</b>'
    f'<s>台日 Apple 價格全表・含退稅試算</s></a>'
  + '</div>'
  + '<h2>依出發地查詢</h2><div class="cities">'
  + ''.join(f'<a class="ct" href="{U("/"+o+"/")}"><b>{n}飛日本機票</b>'
            f'<s>{len({CITY_OF[x["d"]][0] for x in by_origin[o]})} 個航點</s>'
            f'<u>{money(min(x["price"] for x in by_origin[o]))}<small> 起</small></u></a>'
            for o,n,_ in ORIGINS if by_origin.get(o))
  + '</div>' + sections + foot())
pages.append(('/',1.0))

# ---------- Deal 貼文層 ----------
import statistics
DEALDIR='deals'

def pick_deals():
    """挑出值得發文的 deal：絕對門檻 / 相對折扣 / 轉乘更便宜"""
    picked={}
    for (oslug,cslug),fs in by_route.items():
        rts=[x for x in fs if x['rt']]
        if not rts: continue
        b=min(rts,key=lambda x:x['price'])
        med=statistics.median([x['price'] for x in rts])
        reasons=[]
        cap=LCC_CAP if b['cls']=='lcc' else FSC_CAP if b['cls']=='fsc' else None
        if cap and b['price']<cap:
            reasons.append(('threshold',f'{"廉航" if b["cls"]=="lcc" else "一般航空"}低於 {money(cap)}'))
        if len(rts)>=4 and b['price']<med*0.8:
            # 措辭需精確：med 是本站快取樣本的中位數，非市場均價
            # （樣本含大量冷門日期與轉機票，會偏高），不可寫成「市價」
            reasons.append(('discount',
                f'低於本站近期紀錄中位價 {round((1-b["price"]/med)*100)}%'))
        if reasons:
            k=(oslug,cslug)
            if k not in picked or b['price']<picked[k][0]['price']:
                picked[k]=(b,reasons,med,rts)
    return picked

def deal_slug(o,c,d,p):
    """一天一航線一則。slug 不含價格——否則每次執行價格一變就會多出一個
    近乎重複的頁面（一天跑三次就有三份），會被判定為重複內容。"""
    return f'{d}-{o}-{c}'

deals_out=[]
for (oslug,cslug),(b,reasons,med,rts) in sorted(pick_deals().items(),key=lambda kv:kv[1][0]['price']):
    oname=ONAME[oslug]; city=CITY[cslug]; cname=city[1]; reg=city[3]; hotelcity=city[4]
    slug=deal_slug(oslug,cslug,TODAY,b['price'])
    stops='直飛' if b['tr']==0 else f'轉機 {b["tr"]} 次'
    title=f'{oname}飛{cname} {money(b["price"])} 來回含稅｜{b["airname"]} {b["dep"][5:].replace("-","/")} 出發'
    desc=(f'{oname}→{cname}來回含稅 {money(b["price"])}，{b["airname"]}，{stops}，'
          f'{b["dep"]} 去程 / {b["ret"]} 回程。{reasons[0][1]}。')
    why=''.join(f'<li>{r[1]}</li>' for r in reasons)
    others=sorted([x for x in rts if x is not b],key=lambda x:x['price'])[:3]
    ld=json.dumps({"@context":"https://schema.org","@type":"BlogPosting",
        "headline":title,"datePublished":TODAY,"dateModified":TODAY,
        "description":desc,"author":{"@type":"Organization","name":SITENAME}},ensure_ascii=False)
    body=(f'<p class="lede">{oname}飛{cname}，<b>{money(b["price"])}</b> 來回含稅，'
          f'由{b["airname"]}執飛，{stops}。去程 {b["dep"]}，回程 {b["ret"]}。</p>'
          f'<div class="grid" style="max-width:340px">{fare_card(b,True)}</div>'+compare_line(cname)+
          f'<h2>這個價格為什麼值得買</h2><ul>{why}</ul>'
          f'<p class="lede" style="font-size:.86rem">此航線目前共 {len(rts)} 筆來回票價，'
          f'中位價 {money(int(med))}。</p>')
    if others:
        body+=f'<h2>同航線其他選擇</h2><div class="grid">'+''.join(fare_card(x) for x in others)+'</div>'
    body+=klook_tours(cslug,cname)
    body+=f'<h2>{cname}住宿・上網・行程</h2>'+partner_links(cname,hotelcity,cslug)
    rl=f'<a class="ct" href="{U(f"/{cslug}/")}"><b>{cname}機票總覽</b><s>比較所有出發地</s></a>'
    if (oslug,cslug) in route_pages:
        rl+=f'<a class="ct" href="{U(f"/{oslug}/{cslug}/")}"><b>{oname}飛{cname}</b><s>此航線全部票價</s></a>'
    rl+=f'<a class="ct" href="{U(f"/{DEALDIR}/")}"><b>看更多特價</b><s>每日更新</s></a>'
    body+=f'<h2>延伸閱讀</h2><div class="cities">{rl}</div>'
    write(f'{DEALDIR}/{slug}/index.html',
        head(title,desc,f'{DEALDIR}/{slug}/',f'<script type="application/ld+json">{ld}</script>')
        + crumbs([('首頁','/'),('機票特價',f'/{DEALDIR}/'),(f'{oname}飛{cname}',None)])
        + topnav(reg) + f'<h1>{title}</h1>'
        + f'<p class="upd">發布於 {NOWS}　·　票價隨時變動，請以訂購頁面為準</p>' + body + foot())
    pages.append((f'/{DEALDIR}/{slug}/',0.9))
    deals_out.append(dict(slug=slug,title=title,o=oname,c=cname,
        _oiata=b['o'],_diata=b['d'],price=b['price'],air=b['airname'],
        dep=b['dep'],ret=b['ret'],stops=stops,cls=b['cls'],reasons=[r[1] for r in reasons],
        med=int(med),url=b['url'],hotelcity=hotelcity,cslug=cslug))

# 轉乘更划算也發成貼文
for cslug in CITY:
    fs=by_city.get(cslug) or []
    if not fs: continue
    own=(best(fs,True) or best(fs,False))['price']
    for aslug,ab,twd,total_v,route,mode,tm,fare in alt_calc(cslug):
        if not total_v or total_v>=own: continue
        cname=CITY[cslug][1]; aname=CITY[aslug][1]; reg=CITY[cslug][3]
        slug=f'{TODAY}-transfer-{aslug}-{cslug}'
        title=f'飛{aname}轉乘去{cname}，比直飛省 {money(own-total_v)}'
        desc=(f'直飛{cname}最低 {money(own)}，改飛{aname}（{money(ab["price"])}）'
              f'再搭{mode}（{tm}），總計約 {money(total_v)}，省下 {money(own-total_v)}。')
        ld=json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":title,
            "datePublished":TODAY,"dateModified":TODAY,"description":desc,
            "author":{"@type":"Organization","name":SITENAME}},ensure_ascii=False)
        body=(f'<p class="lede">直飛{cname}目前最低 <b>{money(own)}</b>，但飛到{aname}只要 '
              f'<b>{money(ab["price"])}</b>，再搭{mode}（{route}，{tm}，單程約 NT${twd:,}），'
              f'加起來約 <b>{money(total_v)}</b>——<b style="color:var(--hot)">省下 {money(own-total_v)}</b>。</p>'
              + alt_block(cslug,cname,CITY[cslug][4],own)
              + f'<h2>延伸閱讀</h2><div class="cities">'
                f'<a class="ct" href="{U(f"/{cslug}/")}"><b>{cname}機票</b><s>直飛票價</s></a>'
                f'<a class="ct" href="{U(f"/{aslug}/")}"><b>{aname}機票</b><s>轉乘起點</s></a>'
                f'<a class="ct" href="{U(f"/{DEALDIR}/")}"><b>看更多特價</b><s>每日更新</s></a></div>')
        write(f'{DEALDIR}/{slug}/index.html',
            head(title,desc,f'{DEALDIR}/{slug}/',f'<script type="application/ld+json">{ld}</script>')
            + crumbs([('首頁','/'),('機票特價',f'/{DEALDIR}/'),(title,None)])
            + topnav(reg) + f'<h1>{title}</h1>'
            + f'<p class="upd">發布於 {NOWS}</p>' + body + foot())
        pages.append((f'/{DEALDIR}/{slug}/',0.9))
        # o 用「台灣」而非中轉城市，避免被誤讀成「福岡→熊本要價 8,913」
        deals_out.append(dict(slug=slug,title=title,o='台灣',c=cname,via=aname,
            price=total_v,air=f'飛{aname}再轉乘',
            dep=ab['dep'],ret='',stops=mode,cls='transfer',
            reasons=[f'比直飛省 {money(own-total_v)}'],med=own,url=ab['url'],
            hotelcity=CITY[cslug][4],cslug=cslug))
        break

# deals 索引頁
_it=[]
for d in deals_out:
    _u=U('/'+DEALDIR+'/'+d['slug']+'/')
    _lbl='總計' if d['cls']=='transfer' else '來回含稅'
    _sub=d['air']+' · '+d['stops']+' · '+d['dep']
    _it.append(f'<a class="ct" href="{_u}" style="display:block">'
               f'<b>{d["o"]} → {d["c"]}</b><s>{_sub}</s>'
               f'<u>{money(d["price"])}<small> {_lbl}</small></u></a>')
items_today=''.join(_it)

# 往期貼文：掃描 deals/ 既有目錄，讓貼文累積而非每天覆蓋
import glob as _glob
_today_slugs={d['slug'] for d in deals_out}
_past=[]
for p in _glob.glob(f'{DEALDIR}/*/index.html'):
    slug=os.path.basename(os.path.dirname(p))
    if slug in _today_slugs or not re.match(r'^\d{4}-\d{2}-\d{2}-', slug): continue
    try: t=re.search(r'<title>([^<|]+)', open(p,encoding='utf-8').read()).group(1).strip()
    except Exception: continue
    _past.append((slug[:10], slug, t))
_past.sort(reverse=True)
_past=_past[:120]                       # 只保留最近 120 則，避免索引頁無限膨脹
for _d,_s,_ in _past: pages.append((f'/{DEALDIR}/{_s}/',0.6))

_pit=''.join(
  f'<a class="ct" href="{U("/"+DEALDIR+"/"+s+"/")}" style="display:block">'
  f'<b>{html.escape(t[:34])}</b><s>{d}</s></a>' for d,s,t in _past)
past_html=(f'<h2>往期特價</h2><p class="lede">過去的特價紀錄，可用來判斷目前價格是否划算。</p>'
           f'<div class="cities">{_pit}</div>') if _past else ''

write(f'{DEALDIR}/index.html',
  head(f'機票特價｜台灣飛日本便宜機票每日更新（{TODAY}）',
       f'台灣飛日本的機票特價整理，{TODAY} 共 {len(deals_out)} 則，含稅價格、航空公司與出發日期。',
       f'{DEALDIR}/')
  + crumbs([('首頁','/'),('機票特價',None)]) + topnav()
  + f'<h1>機票特價</h1><p class="lede">符合門檻或明顯低於同航線中位價的票，今日共 <b>{len(deals_out)}</b> 則。</p>'
  + f'<p class="upd">更新於 {NOWS}</p><h2>{TODAY} 特價</h2><div class="cities">{items_today}</div>'
  + past_html + foot())
pages.append((f'/{DEALDIR}/',0.95))

# FB / IG 文案（本地檔，不上傳網站）
os.makedirs('posts',exist_ok=True)
json.dump(deals_out, open('posts/deals.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)     # 供 make_cards.py 產生 IG 圖卡
lines=[f'台日機票速報 {TODAY} — 共 {len(deals_out)} 則\n'+'='*52,
       '⚠️ 發文前務必點「查證連結」確認價格仍在，並截圖存證。',
       '   票價變動快，昨日的好票今天常已失效；對不上就不要發。\n'+'='*52+'\n']
for d in deals_out:
    tag={'lcc':'廉航','fsc':'一般航空','transfer':'轉乘方案'}.get(d['cls'],'')
    _lbl='總計' if d['cls']=='transfer' else '來回含稅'
    _url=SITE+U('/'+DEALDIR+'/'+d['slug']+'/')
    _dates=d['dep']+(' – '+d['ret'] if d['ret'] else '')
    # 查證用：直接開該航線該日期的 Trip.com 搜尋頁
    _oc=(d.get('_oiata') or 'TPE').lower()
    _dc=(d.get('_diata') or '').lower()
    _verify=(f"https://tw.trip.com/flights/showfarefirst?dcity={_oc}&acity={_dc}"
             f"&ddate={d['dep']}&rdate={d['ret'] or d['dep']}"
             f"&triptype={'rt' if d['ret'] else 'ow'}&class=y&quantity=1&locale=zh-TW&curr=TWD"
             ) if _dc else '（轉乘方案，請分段查證）'
    lines.append(f"""✈️【{d['o']} → {d['c']}】NT${d['price']:,} {_lbl}

　🛫 {d['air']}｜{d['stops']}
　📅 {_dates}
　💡 {d['reasons'][0]}

　🔗 貼文用連結：{_url}
　🔍 查證連結（開啟後截圖）：{_verify}

#日本機票 #{d['c']}機票 #{d['o']}出發 #便宜機票 #日本自由行
#機票特價 #{tag} #省錢旅遊 #小資旅行 #日本旅遊
{'-'*52}""")
open('posts/%s.txt'%TODAY,'w',encoding='utf-8').write('\n'.join(lines))

print(f'✅ 產生 {len(pages)} 個頁面')
print(f'   Deal 貼文 {len(deals_out)} 則　→ posts/{TODAY}.txt（FB/IG 文案）')
print(f'   城市頁 {len(CITIES)}（{sum(1 for c in CITIES if by_city.get(c[0]))} 個有票價）')
print(f'   地區頁 {len(REGIONS)}　首頁 1　sitemap.xml / robots.txt')
print(f'   票價 {len(deals)} 筆 · 超值票 {len(hot)} 筆 · 全站最低 {money(allbest)}')


# ---------- 台日 Apple 價差比較頁 ----------
if os.path.exists('apple.json'):
    AP=json.load(open('apple.json',encoding='utf-8'))
    RATE=AP['rate']['jpy_twd']; TAXR=1+AP['tax']['jp_consumption']
    ALLOW=AP['tax']['tw_duty_free_allowance']
    SMALL='<br><small style="color:var(--dim)">'

    def _cell(v):
        if v>0: return f'<td class="win">日本省 {money(v)}</td>'
        if v<0: return f'<td class="lose">台灣省 {money(-v)}</td>'
        return '<td>持平</td>'

    def _row(p):
        inc=round(p['jpy']*RATE); ex=round(p['jpy']/TAXR*RATE)
        spec=(SMALL+html.escape(p['spec'])+'</small>') if p['spec'] else ''
        return ('<tr><td><b>'+html.escape(p['name'])+'</b>'+spec+'</td>'
                f'<td>¥{p["jpy"]:,}</td><td>{money(inc)}</td><td><b>{money(ex)}</b></td>'
                f'<td>{money(p["twd"])}</td>'+_cell(p['twd']-inc)+_cell(p['twd']-ex)+'</tr>')

    # 上市時間（僅本次新品；既有機種早已開賣）
    DT=AP.get('dates',{})
    _drows=''.join(
        f'<tr><td><b>{html.escape(n)}</b></td>'
        f'<td>{d["jp_pre"]}</td><td><b>{d["jp_sale"]}</b></td>'
        f'<td>{d["tw_pre"]}</td><td><b>{d["tw_sale"]}</b></td></tr>'
        for n,d in DT.items())
    dtable=('<h2>什麼時候開賣？</h2>'
            '<p class="lede">預購時間為各地當地時間。日本 21:00（JST）與台灣 20:00 其實是同一時刻，'
            '想在日本官網下單不必另外換算。</p>'
            '<div class="tw"><table><thead><tr><th>型號</th>'
            '<th>日本預約</th><th>日本開賣</th><th>台灣預購</th><th>台灣開賣</th>'
            '</tr></thead><tbody>'+_drows+'</tbody></table></div>'
            f'<p class="disc">{html.escape(AP.get("dates_note",""))}</p>') if _drows else ''

    tables=''
    for cat in ('iPhone','Apple Watch','AirPods'):
        ps=[p for p in AP['products'] if p['cat']==cat]
        if not ps: continue
        ps=sorted(ps,key=lambda p:not p.get('new'))   # 新品排前面
        tables+=('<h3>'+cat+'</h3><div class="tw"><table><thead><tr>'
                 '<th>型號</th><th>日本售價'+SMALL+'含稅</small></th>'
                 '<th>換算台幣'+SMALL+'含稅</small></th>'
                 '<th>退稅後'+SMALL+'約當台幣</small></th><th>台灣售價</th>'
                 '<th>含稅比較</th><th>退稅後比較</th></tr></thead><tbody>'
                 +''.join(_row(p) for p in ps)+'</tbody></table></div>')

    NEWP=[p for p in AP['products'] if p.get('new')]
    OLDP=[p for p in AP['products'] if not p.get('new')]
    iph=[p for p in NEWP if p['cat']=='iPhone']
    acc=[p for p in NEWP if p['cat']!='iPhone']
    EV=AP.get('event',{})
    ev_new='、'.join(EV.get('announced',[])) or ''
    ev_old='、'.join(sorted({p['name'] for p in OLDP}))
    cheap_tw=sum(1 for p in iph if p['twd']-round(p['jpy']*RATE)<0)
    cheap_jp=sum(1 for p in iph if p['twd']-round(p['jpy']/TAXR*RATE)>0)
    acc_tw=sum(1 for p in acc if p['twd']-round(p['jpy']/TAXR*RATE)<0)
    top=max(iph,key=lambda p:p['twd']-round(p['jpy']/TAXR*RATE))
    top_save=top['twd']-round(top['jpy']/TAXR*RATE)

    faq=[
     ('日本買 iPhone 真的比較便宜嗎？',
      f'要看能不能退稅。以 Apple 直營店的含稅價換算，{len(iph)} 個 iPhone 組合中有 {cheap_tw} 個是台灣比較便宜；'
      f'若能在家電量販店以免稅價購買，則有 {cheap_jp} 個組合日本較划算，差距約數千元。'),
     ('在 Apple Store 日本直營店可以退稅嗎？',
      '不行。Apple 日本直營店自 2024 年 6 月起已取消對外國旅客的免稅服務，必須支付含消費稅的全額。'
      '想以免稅價購買，需前往 Bic Camera、Yodobashi Camera 等有 Tax-Free 標示的家電量販店，結帳時出示護照。'
      '惟量販店定價未必與 Apple 官網相同，部分店家另收手續費，需現場確認。'),
     ('Apple Watch 和 AirPods 值得在日本買嗎？',
      f'不太值得。本次發表的 {len(acc)} 項配件中，有 {acc_tw} 項即使退稅後仍是台灣便宜，'
      f'其餘價差也不到 NT$1,000，扣掉換匯成本與保固風險並不划算。'),
     ('日本買的 iPhone 快門聲可以關嗎？',
      '可以。自 iOS 15 起，日版 iPhone 的相機快門聲僅在日本境內強制發出，離開日本後即可透過靜音開關關閉。'),
     ('日版 iPhone 在台灣可以保固嗎？',
      'Apple 的 iPhone 保固採區域性政策，日本購買的機器在台灣的 Apple 授權維修中心可能不受理，需寄回日本處理。'
      '若重視售後服務，建議將此風險一併計入價差考量。'),
     ('帶回台灣需要向海關申報嗎？',
      f'台灣入境旅客行李物品免稅額為 {money(ALLOW)}（2024/6/26 起由 NT$20,000 調高）。'
      f'多數 iPhone 單機已超過此金額，應主動申報，超出部分課徵進口稅捐；手機關稅為 0%，主要為 5% 營業稅，'
      f'實際以海關核定為準。'),
     ('匯率會影響結果嗎？',
      f'會，而且影響很大。本頁使用 {AP["rate"]["source"]} {RATE}（{AP["rate"]["quoted_at"]}）換算。'
      f'日圓每變動 1%，一支 iPhone 的價差就會變動數百元；刷卡另有約 1.5% 國外交易手續費，實際成本會更高。'),
    ]
    faq_html=''.join('<details class="faq"><summary>'+html.escape(q)+'</summary><div>'
                     +html.escape(a)+'</div></details>' for q,a in faq)
    faq_ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
        ensure_ascii=False)

    _tk=by_city.get('tokyo') or []
    _b=(best(_tk,True) or best(_tk,False)) if _tk else None

    # 主要購物城市的即時最低票價（東京、大阪有 Apple Store 與大型量販店）
    SHOP=[('tokyo','東京','銀座、表參道 Apple Store；新宿、池袋 Bic Camera'),
          ('osaka','大阪','心齋橋 Apple Store；梅田 Yodobashi'),
          ('fukuoka','福岡','福岡 Apple Store；博多 Bic Camera'),
          ('nagoya','名古屋','名古屋榮 Apple Store；Bic Camera')]
    _srows=''
    for sl,nm,note in SHOP:
        fsx=by_city.get(sl) or []
        if not fsx: continue
        bb=best(fsx,True) or best(fsx,False)
        _srows+=(f'<tr><td><a href="{U("/"+sl+"/")}"><b>{nm}</b></a>{SMALL}{note}</small></td>'
                 f'<td><b>{money(bb["price"])}</b>{SMALL}{bb["airname"]}・{bb["dep"]}</small></td></tr>')
    shoptable=''
    if _srows:
        shoptable=('<h2>哪個城市買得到？順便看機票</h2>'
                   '<p class="lede">Apple 直營店與大型家電量販店集中在這幾個城市，'
                   '以下是台灣飛過去的近期最低來回含稅價。</p>'
                   '<div class="tw"><table><thead><tr><th>城市</th>'
                   '<th>近期最低機票</th></tr></thead><tbody>'+_srows+'</tbody></table></div>')

    title=f'日本買 iPhone 比較便宜嗎？{AP["updated"][:4]} 台日 Apple 價格全表（含退稅試算）'
    desc=(f'iPhone Duo、18 Pro、Air、Apple Watch、AirPods 台日售價全比較，'
          f'依臺灣銀行匯率 {RATE} 換算並試算退稅後價格。'
          f'結論：Apple 直營店含稅價多數台灣較便宜，量販店免稅價才有明顯價差。')

    flights=''
    if _b:
        flights=('<h2>要專程去日本買？先看機票</h2>'
                 f'<p class="lede">台北飛東京目前最低 <b>{money(_b["price"])}</b>'
                 f'（{_b["airname"]}，{_b["dep"]} 出發）。單看機身價差，通常還不夠一張機票——'
                 f'但如果本來就要去日本，那就順便。</p>'
                 + cta('hotel','東京','東京','順便看看東京的住宿','到 Agoda 查房價，繁體中文、台幣計價')
                 + '<div class="cities">'
                 + f'<a class="ct" href="{U("/tokyo/")}"><b>東京機票</b><s>各出發地比價</s></a>'
                 + f'<a class="ct" href="{U("/osaka/")}"><b>大阪機票</b><s>心齋橋、道頓堀</s></a>'
                 + f'<a class="ct" href="{U("/deals/")}"><b>機票特價</b><s>每日更新</s></a></div>')

    write('apple-japan-price/index.html',
      head(title,desc,'apple-japan-price/','<script type="application/ld+json">'+faq_ld+'</script>')
      + crumbs([('首頁','/'),('日本買 iPhone 價差比較',None)]) + topnav()
      + '<h1>日本買 iPhone 比較便宜嗎？</h1>'
      + f'<p class="lede">把 <b>{html.escape(EV.get("name",""))}</b>新品的台日官方定價全部換算比較，'
        f'並試算<b>退稅後</b>的實際價格。</p>'
      + f'<p class="upd">本次新品：{html.escape(ev_new)}<br>'
        f'{html.escape(ev_old)} 本次未改版，一併列出供比較</p>'
      + f'<p class="upd">換算匯率 <b>{RATE}</b>'
        + (f'（中間匯率 {AP["rate"]["jpy_twd_mid"]} 加計約 {round(AP["rate"]["spread"]*100,1)}% 換匯成本）'
           if AP['rate'].get('jpy_twd_mid') else '')
        + f'　·　匯率更新 {AP["rate"]["quoted_at"]}'
        + f'　·　售價取自 Apple 日本／台灣官網　·　資料更新於 {AP["updated"]}</p>'
      + '<h2>先講結論</h2><div class="tldr"><ul>'
      + f'<li><b>在 Apple 直營店買，台灣比較便宜。</b>{len(iph)} 個新機組合中有 {cheap_tw} 個台灣較低，'
        f'差距多在 NT$1,000 上下。</li>'
      + f'<li><b>能退稅才有價差。</b>在家電量販店以免稅價購買時，{cheap_jp} 個組合日本較划算，'
        f'最多可省 {money(top_save)}（{top["name"]} {top["spec"]}）。</li>'
      + '<li><b>但 Apple 直營店已不能退稅</b>（2024/6 起），要免稅得去 Bic Camera、Yodobashi 等量販店。</li>'
      + f'<li><b>配件不值得為它退稅。</b>{len(acc)} 項新配件中有 {acc_tw} 項連退稅後仍是台灣便宜，'
        f'其餘價差也不到 NT$1,000。</li>'
      + '</ul></div>'
      + search_form('順便查一下機票多少錢',
                    '既然在考慮飛一趟，先看看你的日期要多少。', 'TPE', 'TYO')
      + '<h2>台日價格全表</h2>'
      + '<p class="lede">「退稅後」為日本含稅價扣除 10% 消費稅後換算之約當金額，'
        '實際免稅價與手續費依店家而異。</p>' + tables
      + dtable
      + '<h2>買之前要知道的兩件事</h2>'
      + '<h3>1. Apple 直營店已經不能退稅</h3>'
      + '<p class="lede">Apple 日本直營店自 2024 年 6 月起取消對外國旅客的免稅服務。'
        '要拿到免稅價，必須到有 Tax-Free 標示的家電量販店（Bic Camera、Yodobashi Camera 等），'
        '結帳時出示護照。量販店定價未必與 Apple 官網相同，且部分店家收取手續費，請現場確認。</p>'
      + cta('hotel','東京','東京','要去量販店掃貨？先看住宿',
            'Bic Camera 與 Yodobashi 都在新宿、梅田一帶，住附近最方便')
      + '<h3>2. 保固是區域性的</h3>'
      + '<p class="lede">日本購買的 iPhone 在台灣的 Apple 授權維修中心可能不受理，需寄回日本處理。'
        '省下的幾千元，遇到一次維修就可能不划算。至於快門聲，自 iOS 15 起僅在日本境內強制，'
        '離開日本即可關閉，這點不必擔心。</p>'
      + shoptable
      + flights
      + '<h2>常見問題</h2>' + faq_html
      + cta('esim','日本','東京','出發前先把上網搞定',
            '到 Klook 買 eSIM 或網卡，落地就能開導航找店')
      + f'<p class="disc">補充：台灣入境旅客行李物品免稅額為 {money(ALLOW)}，'
        f'多數 iPhone 單機已超過，依規定應主動向海關申報，超出部分課徵進口稅捐。'
        f'手機關稅為 0%，主要為 5% 營業稅，實際以海關核定為準。<br>'
        f'本頁售價取自 Apple 日本與台灣官網，匯率取自臺灣銀行牌告，僅供參考，'
        f'實際價格與稅務規定請以官方公告為準。頁內部分連結為聯盟行銷連結，'
        f'本站可能獲得分潤，不影響你的價格。</p>'
      + foot())
    pages.append(('/apple-japan-price/',0.9))
    print(f'   台日 Apple 價差頁：{len(AP["products"])} 項商品')

# ---------- sitemap / robots ----------
LASTMOD=NOW.strftime('%Y-%m-%dT%H:%M:%S%z')      # 含時區偏移，避免相對 UTC 變成未來日期
LASTMOD=LASTMOD[:-2]+':'+LASTMOD[-2:]            # +0800 → +08:00（W3C Datetime 格式）
urls='\n'.join(f'  <url><loc>{SITE}{U(u)}</loc><lastmod>{LASTMOD}</lastmod>'
             f'<changefreq>daily</changefreq><priority>{p}</priority></url>' for u,p in pages)
write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n'
      f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}{BASE}/sitemap.xml\n')
write('.nojekyll','')

