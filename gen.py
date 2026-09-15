# -*- coding: utf-8 -*-
"""台日機票速報 — 多頁 SEO 網站產生器"""
import json, datetime, html, collections, os, urllib.parse, shutil, re, statistics

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
    # Trip.com 的飯店列表要數字城市 ID，沒有對應 ID 的城市就退回關鍵字連結，
    # 否則會產生一個指向錯誤城市（或整個掉回首頁）的連結
    if '{cid}' in u:
        cid=(p.get('city_ids') or {}).get(city)
        u=u.replace('{cid}',str(cid)) if cid else p['fallback']
    u=u.replace('{q}',urllib.parse.quote(city))
    kw.setdefault('sub','')          # 沒傳就留空，別讓 {sub} 原樣留在網址裡
    # 沒有日期可帶時，整段拿掉而不是留下空的 checkin=，否則 Trip.com 會掉回首頁
    if '{ci}' in u and not kw.get('ci'):
        u=re.sub(r'&(checkin|checkout|crn|adult)=\{?[^&]*\}?', '', u)
        kw.pop('ci',None); kw.pop('co',None)
    for k,v in kw.items(): u=u.replace('{'+k+'}',str(v))
    return u

# Trip.com 分潤參數集中放這裡，SF_JS 與貼文查證連結共用，不要各自寫死
_AFF = (P.get('flight', {}) or {}).get('affiliate') or {}
AFF_Q = ''.join(f'&{k}={v}' for k, v in _AFF.items() if not k.startswith('_'))

def flight_url(x):
    """以航班資料組出 Trip.com 搜尋連結（繁中 / TWD）"""
    return plink('flight', o=x['o'].lower(), d=x['d'].lower(),
                 dep=x['dep'], ret=x['ret'] or x['dep'],
                 tt='rt' if x['rt'] else 'ow', sub=x['d'].lower())

def fare_cta(slug, headline, sub_prefix='', before=None):
    """帶真實票價的 CTA——右欄直接放金額。

    沒有票價資料時回傳空字串：寧可不放，也不要放一個只寫「去查」、
    沒有任何數字的連結，那種連結使用者沒有理由點。"""
    fs = by_city.get(slug) or []
    if before:   # 例如免稅改制前的行程，只挑該日期之前出發的航班
        _f = [x for x in fs if x['dep'] < before]
        fs = _f or fs
    b = best(fs, True) or best(fs, False)
    if not b: return ''
    nm = CITY[slug][1]
    pt = '來回' if b['rt'] else '單程'
    sub = (f'{sub_prefix}台北飛{nm}・{b["airname"]}・{b["dep"]} 出發・{pt}含稅'
           f'　→ 到 Trip.com 查這天')
    return (f'<a class="cta" href="{html.escape(flight_url(b))}" target="_blank" '
            f'rel="nofollow noopener sponsored">'
            f'<span class="ci">✈️</span>'
            f'<span class="ct"><b>{html.escape(headline)}</b><s>{html.escape(sub)}</s></span>'
            f'<span class="ca pr">{money(b["price"])}<small>近期最低</small></span></a>')


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

def span_of(fs):
    """這批票價實際涵蓋的出發日區間——「近期紀錄」不說期間等於沒說"""
    ds = sorted(x['dep'] for x in fs if x.get('dep'))
    if not ds:
        return ''
    a, b = ds[0], ds[-1]
    return f"{a[5:7].lstrip('0')}/{a[8:10].lstrip('0')}–{b[5:7].lstrip('0')}/{b[8:10].lstrip('0')}"


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
                   f'有。{span_of(fs)} 出發的票價紀錄中，共有 {len(direct)} 筆直飛{name}，'
                   f'執飛的航空公司包括{who}。'))
    else:
        qa.append((f'台灣有直飛{name}的班機嗎？',
                   f'{span_of(fs)} 出發的 {len(fs)} 筆票價紀錄中沒有直飛{name}的班機，'
                   f'查到的都是轉機航班。'
                   f'可考慮飛鄰近機場後轉乘日本國內交通。'))

    # 2 飛行時間
    ds = [x['dur_to'] for x in direct if x.get('dur_to')]
    if ds:
        m = min(ds)
        qa.append((f'台灣飛{name}要多久？',
                   f'直飛去程最短約 {m//60} 小時 {m%60} 分。'))

    # 3 價格區間
    _rt = [x for x in fs if x['rt'] and x.get('dep')]
    if len(_rt) >= 4:
        _by = collections.defaultdict(list)
        for x in _rt:
            _by[x['dep']].append(x['price'])
        daily = sorted(min(v) for v in _by.values())
        # 講「每天最便宜要多少」而非全部票價的中位數：後者混入冷門日期與
        # 轉機貴票會偏高，讀者不會去買那些票，拿來當基準等於灌水
        avg = round(statistics.mean(daily))
        qa.append((f'台灣飛{name}的機票大概多少錢？',
                   f'{span_of(fs)} 出發的日期中，有 {len(daily)} 天留下紀錄。'
                   f'每天最便宜的來回含稅價平均 {money(avg)}，'
                   f'最低曾出現 {money(daily[0])}、最高的一天也要 {money(daily[-1])}。'
                   f'低於 {money(avg)} 就算是這條航線相對便宜的價格。'
                   f'（以上為歷史紀錄，實際售價請以訂票平台查詢為準）'))

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
                       f'目前紀錄涵蓋 {span_of(fs)} 出發的班次，其中 {y} 年 {int(mo)} 月最低，'
                       f'來回含稅 {money(best[1])} 起（該月有 {best[2]} 筆紀錄）。'
                       f'此區間為目前已抓到紀錄的範圍，未涵蓋的日期不代表沒有更低價。'))

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
         '+(b?"&rdate="+b:"")+"&triptype="+t+"&class=y&quantity=1&locale=zh-TW&curr=TWD"'
         '+"' + AFF_Q + '&trip_sub1="+d;'
         'window.open(u,"_blank","noopener");return false;}</script>')

# details 原生不會互斥、也不會因為點別處而收起來；沒有這段，
# 展開兩個分類就會兩片面板疊在一起，而且一直留在畫面上。
NAV_JS = ('<script>(function(){var n=document.querySelector("nav.top");if(!n)return;'
          'var d=[].slice.call(n.querySelectorAll(":scope>details"));'
          'function shut(x){d.forEach(function(o){if(o!==x)o.open=false})}'
          'd.forEach(function(o){o.addEventListener("toggle",function(){if(o.open)shut(o)})});'
          'document.addEventListener("click",function(e){'
          'if(!n.contains(e.target))shut(null);'
          'else if(e.target.closest&&e.target.closest(".dd a"))shut(null)});'
          'document.addEventListener("keydown",function(e){'
          'if(e.key==="Escape")shut(null)});})();</script>')

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
            dept=r.get('departure_at','')[11:16], rett=r.get('return_at','')[11:16],
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
nav.top{position:sticky;top:0;z-index:30;background:var(--bg);padding:9px 0;margin-top:14px;
border-bottom:1px solid var(--line);display:flex;gap:6px;flex-wrap:wrap;align-items:center}
nav.top>a{color:var(--dim);text-decoration:none;font-size:.86rem;white-space:nowrap;
font-weight:500;padding:6px 10px;border-radius:7px}
nav.top>a:hover,nav.top>a.cur{color:var(--acc);background:var(--soft)}
/* 用 details 做下拉：不需 JS，鍵盤可操作，手機上也不會因 hover 失效 */
/* 寬螢幕：面板錨在自己的項目下方，點哪個就在哪個下面展開 */
nav.top details{position:relative}
nav.top summary{list-style:none;cursor:pointer;font-size:.86rem;font-weight:500;color:var(--dim);
padding:6px 10px;border-radius:7px;white-space:nowrap;user-select:none}
nav.top summary::-webkit-details-marker{display:none}
nav.top summary::after{content:"▾";margin-left:5px;font-size:.7rem;opacity:.6}
nav.top summary:hover,nav.top details[open]>summary{color:var(--acc);background:var(--soft)}
nav.top details[open]>summary::after{content:"▴"}
/* 一律絕對定位：若改 static，展開時會把同列其他項目擠開、版面錯位 */
/* 最右邊的分類往左展開，否則視窗接近斷點時面板會凸出畫面右緣 */
nav.top>details.end>.dd{left:auto;right:0}
.dd{position:absolute;top:calc(100% + 6px);left:0;min-width:220px;
max-width:min(340px,calc(100vw - 32px));max-height:70vh;overflow-y:auto;
background:var(--card);border:1px solid var(--line);border-radius:11px;padding:7px;
box-shadow:0 10px 28px rgba(0,0,0,.14);display:flex;flex-direction:column;gap:1px;z-index:40}
.dd a{display:block;padding:8px 11px;border-radius:7px;color:var(--fg);text-decoration:none;
font-size:.87rem;white-space:nowrap}
.dd a:hover{background:var(--soft);color:var(--acc)}
.dd a.cur{color:var(--acc);font-weight:600}
.dd b{display:block;padding:9px 11px 4px;font-size:.72rem;color:var(--dim);font-weight:600;
letter-spacing:.05em}
.dd hr{border:0;border-top:1px solid var(--line);margin:5px 0}
/* 窄螢幕導覽列會換行，面板錨在各自的項目上時很容易被推出畫面左右緣；
   改為錨定導覽列本身（position:sticky 已建立定位脈絡）並撐滿整列 */
@media(max-width:767px){
 nav.top details{position:static}
 .dd{left:0;right:0;max-width:none;top:calc(100% + 4px)}
 .dd a{white-space:normal}
}
/* 漢堡選單：只在窄螢幕出現，同時把四個分類的下拉收起來 */
nav.top>details.burger{display:none}
@media(max-width:767px){
 nav.top>details.burger{display:block}
 nav.top>details:not(.burger){display:none}
}
/* 漢堡面板內的分類標題 */
.dd>details>summary{list-style:none;cursor:pointer;user-select:none;
font-size:.9rem;font-weight:600;color:var(--fg);padding:10px 11px;border-radius:7px;
display:flex;justify-content:space-between;align-items:center}
.dd>details>summary::-webkit-details-marker{display:none}
.dd>details>summary::after{content:"▾";font-size:.7rem;color:var(--dim)}
.dd>details[open]>summary,.dd>details>summary:hover{color:var(--acc);background:var(--soft)}
.dd>details[open]>summary::after{content:"▴"}
/* 就地展開的子清單，沿用 .dd 的排版但不再是浮動面板 */
.sub{display:flex;flex-direction:column;gap:1px;padding:1px 0 8px 12px}
.sub a{display:block;padding:8px 11px;border-radius:7px;color:var(--fg);
text-decoration:none;font-size:.86rem}
.sub a:hover{background:var(--soft);color:var(--acc)}
.sub a.cur{color:var(--acc);font-weight:600}
.sub b{display:block;padding:9px 11px 4px;font-size:.72rem;color:var(--dim);
font-weight:600;letter-spacing:.05em}
.sub hr{border:0;border-top:1px solid var(--line);margin:5px 0}

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
.tg.gt{background:color-mix(in srgb,#b45309 16%,transparent);color:#b45309}
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
.today{background:linear-gradient(180deg,#fff,var(--soft));border:1px solid var(--line);
 border-top:4px solid var(--acc);border-radius:12px;padding:19px 22px;margin-top:14px}
.tday{font-size:.79rem;color:var(--dim);letter-spacing:.04em;font-weight:600}
.tans{font-size:1.3rem;font-weight:800;line-height:1.42;margin-top:8px;letter-spacing:-.02em}
.tsub{font-size:.93rem;color:var(--dim);line-height:1.7;margin-top:10px}
.tbuf{font-size:.93rem;line-height:1.7;margin-top:12px;padding-top:12px;border-top:1px dashed var(--line)}
.tbuf b{color:var(--acc)}
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
.cta .ca.pr{font-size:1.42rem;letter-spacing:-.03em;line-height:1.15;text-align:right}
.cta .ca.pr small{display:block;font-size:.66rem;font-weight:600;color:var(--dim);letter-spacing:0}
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
.calc{margin-top:12px;padding:16px;background:var(--soft);border:1px solid var(--line);border-radius:12px}
.calc .sf{margin-top:0;padding:0;background:none;border:0}
.cres{margin-top:14px;padding:16px 18px;background:var(--card);border:1px solid var(--line);
 border-radius:10px}
.cres .cl{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
 padding:7px 0;font-size:.95rem;border-bottom:1px dashed var(--line)}
.cres .cl:last-of-type{border-bottom:0}
.cres .cl b{font-size:1.16rem;font-variant-numeric:tabular-nums}
.cres .cl .pw{background:var(--acc);color:#fff;font-size:.7rem;padding:1px 7px;border-radius:4px;
 font-weight:700;margin-right:4px}
.cres .cl .pc{font-style:normal;font-size:.72rem;color:var(--hot);margin-left:8px}
.cres .cl .pp{font-style:normal;font-size:.78rem;color:var(--dim);font-weight:600;margin-left:8px}
.cres .cv{margin-top:12px;padding-top:12px;border-top:2px solid var(--line);
 font-size:1.12rem;font-weight:800;line-height:1.5}
.cres .cv.jp{color:var(--lcc)}.cres .cv.tw{color:var(--acc)}
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
    """分類導覽。寬螢幕是一列下拉；767px 以下收成漢堡選單——
    導覽列在 375px 會折成三行、吃掉約 190px 的畫面高度，而它是 sticky 的。
    首頁與機票特價留在外面（最常點），其餘四個分類收進 ☰，一行就放得下。

    手機與桌機各有一份連結。多幾 KB，但換來純 CSS 切換：
    若靠一個 details 同時當漢堡與桌機容器，桌機必須有人把它打開，
    JS 一失效整條導覽列就只剩一個 ☰。"""
    def link(href, text, is_cur=False):
        return f'<a href="{U(href)}"{" class=cur" if is_cur else ""}>{text}</a>'

    regions = ''.join(link(f'/{sl}/', nm, sl == cur) for sl, nm in REGIONS)
    origins = ''.join(link(f'/{sl}/', f'從{nm}出發') for sl, nm, _ in ORIGINS)
    area = ('<b>日本地區</b>' + regions + '<hr><b>台灣出發地</b>' + origins)

    kinds = (link('/japan-flight-good-times/', '☀️ 早去晚回')
             + link('/deals/', '🔥 今日特價')
            + link('/japan-flight-baggage/', '🧳 廉航行李費'))

    shop = (link('/japan-coupon/', '🏷️ 購物折扣總覽')
            + link('/japan-tax-free-2026/', '🧾 11/1 免稅新制')
            + link('/apple-japan-price/', '🍎 台日 Apple 價差')
            + link('/iphone-cost/', '📉 iPhone 持有成本')
            + link('/iphone-card/', '💰 買 iPhone 刷哪張卡'))
    if os.path.exists('coupons.json'):
        _cp = json.load(open('coupons.json', encoding='utf-8'))['stores']
        shop += '<hr><b>各店折扣</b>' + ''.join(
            link(f'/japan-coupon/{st["slug"]}/', st['name']) for st in _cp[:6])

    _cd = json.load(open('cards.json', encoding='utf-8'))['cards'] \
        if os.path.exists('cards.json') else []
    card = (link('/japan-credit-card/', f'💳 {len(_cd) or ""} 張卡比較'.replace('  ', ' '))
            + link('/japan-card-calculator/', '🧮 回饋計算機'))
    if _cd:
        card += '<hr><b>熱門卡片</b>' + ''.join(
            link(f'/japan-credit-card/{c["slug"]}/', c['name'])
            for c in sorted(_cd, key=lambda x: -x['total'])[:6])

    SEC = [('✈️ 航班地區', area), ('🕐 航班類型', kinds),
           ('🛍️ 旅日購物', shop), ('💳 旅日信用卡', card)]

    def menu(label, inner, end=False):
        # name 讓瀏覽器原生互斥，JS 失效時至少不會兩片面板疊在一起
        return (f'<details name="topnav"{" class=end" if end else ""}>'
                f'<summary>{label}</summary>'
                f'<div class="dd">{inner}</div></details>')

    def sub(label, inner):
        # 漢堡面板內的分類：就地展開，不再疊一層浮動面板
        return (f'<details name="burgernav"><summary>{label}</summary>'
                f'<div class="sub">{inner}</div></details>')

    burger = ('<details class="burger"><summary>☰ 選單</summary><div class="dd">'
              + ''.join(sub(l, i) for l, i in SEC) + '</div></details>')

    return ('<nav class="top">'
            + link('/', '首頁', not cur)
            + link('/deals/', '🔥 機票特價')
            + ''.join(menu(l, i, end=(k == len(SEC) - 1))
                      for k, (l, i) in enumerate(SEC))
            + burger
            + '</nav>')


def foot():
    return f'''<p class="note">
票價資料來源為 Aviasales 資料庫，價格為單人含稅及手續費，僅供參考，隨時可能變動。<br>
實際訂購由合作平台完成：機票 Trip.com、住宿 Agoda、行程與交通票 KKday、網卡與租車 Klook。<br>
本站連結為聯盟行銷連結，透過連結完成訂購時本站可獲得分潤，不影響你的價格。<br>
最後更新 {NOWS}　·　<a href="{U("/")}">回首頁</a>
</p></div>{SF_JS}{NAV_JS}</body></html>'''

def _hh(t):
    """'HH:MM' → 小時整數；缺值回 None"""
    return int(t[:2]) if t and len(t) >= 5 and t[:2].isdigit() else None


def arr_min(x):
    """抵達日本的當地時間，以出發日零時起算的分鐘數。

    刻意不取 %24：跨日的過夜轉機若取模會變成「凌晨 1 點抵達」，
    看起來像「中午前到」，實際上第一天早就沒了。"""
    t = x.get('dept')
    if not t or not x.get('dur_to'):
        return None
    return int(t[:2]) * 60 + int(t[3:5]) + x['dur_to'] + 60   # +60 為台日時差


def good_times(x):
    """不浪費假期的班次。三個條件要同時成立：

    · 出發不早於 05:00——再早就是徹夜未眠的紅眼，02:30 起飛雖然
      06:35 就到，但那一天多半在補眠
    · 當日中午前抵達——決定第一天能不能用的是抵達時間，不是出發
      時間。06–10 出發但轉機拖到 16:35 才到，第一天照樣報廢
    · 回程由日本 18–23 起飛——最後一天能玩到傍晚
    """
    if not x.get('rt'):
        return False
    t, rh, a = x.get('dept'), _hh(x.get('rett')), arr_min(x)
    if not t or rh is None or a is None:
        return False
    dm = int(t[:2]) * 60 + int(t[3:5])
    return dm >= 5 * 60 and a <= 12 * 60 and 18 <= rh <= 23


def fare_card(x,hot=False):
    tag={'lcc':'廉航','fsc':'一般航空'}.get(x['cls'],'其他')
    gt = good_times(x)
    cn=CITY_OF[x['d']][1]
    stops='直飛' if x['tr']==0 else f"轉機{x['tr']}"
    trip='來回' if x['rt'] else '單程'
    dates=x['dep']+(f" – {x['ret']}" if x['ret'] else '')
    if x.get('dept'):
        dates += f"　{x['dept']}"+(f" → {x['rett']}" if x.get('rett') else '')
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
<div class="mt"><span class="tg {x['cls']}">{tag}</span><span>{html.escape(x['airname'])}</span><span>{stops}</span>{'<span class="tg gt">☀️ 早去晚回</span>' if gt else ''}</div>
<div class="dt">{dates}</div>{gate_html}{btn}</article>'''

def cta(kind, city_name, hotel_city, headline, sub, track='', ci='', co=''):
    """單一情境式 CTA。
    不再把 4–5 個夥伴連結並排——Travelpayouts 官方明言「一段五個連結會失去信任」，
    競品分析也顯示成效好的頁面是把連結嵌在相關段落，而非集中成一排按鈕。

    track 會填進 trip_sub1，用來在聯盟後台分辨是哪個頁面帶來的成交。"""
    p = P[kind]
    return (f'<a class="cta" href="'
            f'{html.escape(plink(kind, hotel_city, sub=track, ci=ci, co=co))}" '
            f'target="_blank" '
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

def sort_key(fs):
    """排序用：有來回票的排前面，再依價格。

    單程與來回不可比——米子單程 4,440 排在沖繩來回 5,070 前面，
    看起來比較便宜，其實是兩種東西。"""
    b, lbl = best_labeled(fs)
    if not b:
        return (2, 10 ** 9)
    return (0 if lbl == '來回' else 1, b['price'])


def best_labeled(fs):
    """取最低價，優先來回；沒有來回票才退回單程。

    回傳 (票價紀錄, 標籤)。卡片一定要標單程或來回——單程最低往往
    只有來回的一半（台北→沖繩 2,459 vs 5,070），混在一起取最小值
    又不標示，讀者會以為那個數字就能來回。"""
    r = best(fs, True)
    if r:
        return r, '來回'
    o = best(fs, False)
    return (o, '單程') if o else (None, '')


def best(fs,rt=None):
    p=[x for x in fs if (rt is None or x['rt']==rt)]
    return min(p,key=lambda x:x['price']) if p else None

def money(n): return f'NT${n:,}'

# 行李費用（城市頁的比價要用，完整說明另有專頁）
BAG = json.load(open('baggage.json', encoding='utf-8')) if os.path.exists('baggage.json') else None
BAG_RT = (BAG['ref']['per_leg'] * 2) if BAG else 0

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

    # 全站最低常常來自台灣讀者沒聽過的平台（Farera 等），點進 Trip.com 會對不到。
    # 兩個數字都給：最低是多少、只用 Trip.com 又是多少，讓讀者自己決定要不要用陌生平台。
    _tc = [x for x in fs if x.get('gate') == 'Trip.com']
    _tc_best = (best(_tc, True) or best(_tc, False)) if _tc else None

    intro=f'<p class="lede">'
    if anchor:
        lccs=[a for a in airs if a in LCC.values()]
        intro+=f'台灣飛{name}目前最低 <b>{money(anchor["price"])}</b>（{pt}含稅，{anchor["airname"]}，{anchor["dep"]} 出發）。'
        if _tc_best and _tc_best['price'] > anchor['price']:
            _gn = gate_info(anchor.get('gate',''))[0]
            _tp = '來回' if _tc_best['rt'] else '單程'
            intro+=(f'這筆紀錄來自 {html.escape(_gn)}，台灣讀者較陌生；'
                    f'<b>若只看 Trip.com，最低是 {money(_tc_best["price"])}</b>'
                    f'（{_tp}含稅，{_tc_best["airname"]}，{_tc_best["dep"]} 出發）。')
        if lccs: intro+=f'飛{name}的廉價航空有 {"、".join(lccs[:4])}。'
        if len(oris)>1:
            intro+=f'{"、".join(ORI[o] for o in oris)} 都有航班。'
    else:
        intro+=f'目前快取中沒有台灣飛{name}的票價，可點下方查詢即時價格。'
    intro+='</p>'

    # 卡片是按價格排序只取前 12 張，廉航一定洗版，全服務航空一張都擠不進來。
    # 但資料裡有三分之一是全服務航空，想帶行李、想要好時段的人看不到自己要的數字。
    _lcc_rt = sorted([x for x in fs if x['rt'] and x['cls'] == 'lcc'], key=lambda x: x['price'])
    _fsc_rt = sorted([x for x in fs if x['rt'] and x['cls'] == 'fsc'], key=lambda x: x['price'])
    # 樣本太少時不做這個比較：福岡只有 2 筆一般航空來回，
    # 拿它當「最低價」會算出 NT$12,796 的假價差
    FSC_MIN = 5
    cmp_block = ''
    if _lcc_rt and len(_fsc_rt) >= FSC_MIN:
        _l, _f = _lcc_rt[0], _fsc_rt[0]
        _gap = _f['price'] - _l['price']

        def _slot(x):
            return (f'{x["dept"]} → {x["rett"]}'
                    if x.get('dept') and x.get('rett') else '—')

        _bagrow, _bagnote = '', ''
        if BAG:
            _wb = _l['price'] + BAG_RT
            _left = _f['price'] - _wb
            _verdict = (f'一般航空仍貴 {money(_left)}' if _left > 0
                        else f'反而比一般航空貴 {money(-_left)}')
            _bagrow = (f'<tr><td><b>廉航 ＋ 來回託運 {BAG["ref"]["kg"]}kg</b></td>'
                       f'<td><b>{money(_wb)}</b></td>'
                       f'<td colspan="3" style="text-align:left">'
                       f'以{html.escape(BAG["ref"]["airline"])}公告費率估，{_verdict}</td></tr>')
            _bagnote = (f'<p class="lede">票價差 <b>{money(_gap)}</b>，但廉航的最低票價'
                        f'<b>不含託運行李</b>——那是只能帶手提行李的價格。'
                        f'加購來回 {BAG["ref"]["kg"]}kg 要 {money(BAG_RT)}，'
                        f'價差就縮到 {money(_left)}。'
                        f'<a href="{U("/japan-flight-baggage/")}">各家行李費怎麼算</a>。</p>')
        else:
            _bagnote = (f'<p class="lede">差 <b>{money(_gap)}</b>。'
                        f'一般航空的票價通常已含託運行李，廉航多半要另外加購。</p>')

        cmp_block = (
          f'<h2>廉航和一般航空，差多少？</h2>'
          f'<p class="lede">下面的卡片按價格排序，廉航幾乎一定排在前面。'
          f'如果你想要含託運行李或比較好的時段，這裡先把兩邊的最低價並排：</p>'
          '<div class="tw"><table><thead><tr><th>類型</th><th>來回最低</th>'
          '<th>航空公司</th><th>出發日</th><th>去程起飛 → 回程起飛</th>'
          '</tr></thead><tbody>'
          f'<tr><td><b>廉航</b></td><td class="win"><b>{money(_l["price"])}</b></td>'
          f'<td>{html.escape(_l["airname"])}</td><td>{_l["dep"]}</td>'
          f'<td>{_slot(_l)}</td></tr>'
          f'<tr><td><b>一般航空</b></td><td><b>{money(_f["price"])}</b></td>'
          f'<td>{html.escape(_f["airname"])}</td><td>{_f["dep"]}</td>'
          f'<td>{_slot(_f)}</td></tr>'
          + _bagrow
          + '</tbody></table></div>'
          + _bagnote
          + f'<p class="disc">兩邊都是<b>本站紀錄中</b>的最低價，不是市場最低。'
            f'全服務航空的促銷票常常不在快取裡，看到別處有更低的價格是正常的。'
            f'共 {len(_lcc_rt)} 筆廉航來回、{len(_fsc_rt)} 筆一般航空來回。</p>')

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
        _shown = {id(x) for x in rts}
        _fsc_show = [x for x in _fsc_rt if id(x) not in _shown][:4]
        if _fsc_show:
            body += (f'<h3>一般航空的來回選擇</h3>'
                     f'<p class="lede">上面的排序被廉航佔滿時，這裡單獨列出票價最低的'
                     f'幾筆一般航空紀錄。</p><div class="grid">'
                     + ''.join(fare_card(x) for x in _fsc_show) + '</div>')
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
        # 沒有城市 ID 的城市會退回 Agoda，文案就不能寫 Trip.com
        _has_cid = hotelcity in ((P['hotel'].get('city_ids') or {}))
        _hb = P['hotel']['brand'] if _has_cid else 'Agoda'
        # 沒有房價資料可放（Hotellook API 已下線），但可以把日期帶過去：
        # 落地就是他正在看的那幾晚，比一個靜態的「最低房價」更貼近實際要訂的東西
        _hr = br or bo
        _ci = _hr['dep'] if _hr else ''
        _co = (_hr['ret'] if _hr and _hr['ret'] else '')
        if _has_cid and _ci and _co:
            _hsub = f'直接查 {_ci[5:].replace("-","/")}–{_co[5:].replace("-","/")} 這幾晚的{hotelcity}房價'
        else:
            _hsub = f'到 {_hb} 查{hotelcity}房價，繁體中文、台幣計價'
        body+=cta('hotel',name,hotelcity,f'看好機票了？接著找{name}的住宿',
                  _hsub, track=slug, ci=_ci, co=_co)
    body+=faq_block(name,fs,codes)
    body+=klook_tours(slug,name)
    # 當地玩樂的分潤是機票的八倍（4% vs 0.5%），而且看完機票住宿的下一個問題
    # 本來就是「要玩什麼」，放在這裡最順
    body+=cta('activity',name,name,f'機票住宿都有了，{name}要玩什麼',
              f'到 {P["activity"]["brand"]} 看{name}的門票與一日遊，繁體中文、台幣計價',
              track=slug)
    if slug not in URBAN:
        body+=cta('car',name,hotelcity,f'{name}自駕比較方便',
                  f'到 {P["car"]["brand"]} 比較租車方案', track=slug)
    body+=cta('esim',name,hotelcity,'出發前別忘了日本上網',
              '到 Klook 買 eSIM 或網卡，落地就能用')
    body+='<p class="disc">以上連結會前往合作訂票平台完成預訂，本站可能獲得分潤，不影響你的價格。</p>'
    sib=[c for c in CITIES if c[3]==reg and c[0]!=slug]
    if sib:
        body+=(f'<h2>{REGNAME[reg]}其他航點</h2><div class="cities">'+''.join(
            f'<a class="ct" href="{U("/"+s+"/")}"><b>{n}</b><s>{REGNAME[r]}</s>'
            + (f'<u>{money(best_labeled(by_city[s])[0]["price"])}'
               f'<small> 起 · {best_labeled(by_city[s])[1]}</small></u>' if by_city.get(s)
               else '<u style="color:var(--dim);font-weight:400;font-size:.8rem">查詢票價</u>')
            + '</a>' for s,n,_,r,_ in sib)+'</div>')

    write(f'{slug}/index.html', head(title,desc,f'{slug}/')
        + crumbs([('首頁','/'),(REGNAME[reg],f'/{reg}/'),(f'{name}機票',None)])
        + topnav(reg) + f'<h1>{name}機票</h1>' + intro
        + f'<p class="upd">更新於 {NOWS}　·　共 {len(fs)} 筆票價</p>'
        + cmp_block + body + foot())
    pages.append((f'/{slug}/',0.8 if fs else 0.5))


# ---------- 廉航行李費 ----------
# 城市頁的比價只到「票價」為止，但廉航最低票價是不含託運的。
# 加購行李之後價差會縮水多少？這一頁把它算出來。
if os.path.exists('baggage.json'):
    BG = json.load(open('baggage.json', encoding='utf-8'))
    _REF = BG['ref']
    _TG = BG['tigerair']
    _SM = '<br><small style="color:var(--dim)">'   # SMALL 在後面才定義，這裡自己來
    _rt_fee = _REF['per_leg'] * 2

    _cells = lambda r: ''.join(
        (f'<td>{money(v)}</td>' if v else '<td class="dim">—</td>') for v in r[1:])
    _tgrows = ''.join(f'<tr><td><b>{html.escape(r[0])}</b></td>{_cells(r)}</tr>'
                      for r in _TG['rows'])

    _farerows = ''.join(
        f'<tr><td><b>{html.escape(f["airline"])}</b></td>'
        f'<td>{"廉航" if f["cls"] == "lcc" else "一般航空"}</td>'
        f'<td>{html.escape(f["note"])}</td>'
        f'<td><a href="{f["src"]}" rel="nofollow" target="_blank">'
        f'{html.escape(f["src_name"])}</a></td></tr>' for f in BG['fares'])

    # 三個有 FSC 樣本的城市，加上行李之後的實際比較
    _bcity = ''
    for _s, _n, _c, _r, _h in CITIES:
        _f = by_city.get(_s, [])
        _l = sorted([x for x in _f if x['rt'] and x['cls'] == 'lcc'], key=lambda x: x['price'])
        _g = sorted([x for x in _f if x['rt'] and x['cls'] == 'fsc'], key=lambda x: x['price'])
        if not _l or len(_g) < 5:
            continue
        _lp, _gp = _l[0]['price'], _g[0]['price']
        _with = _lp + _rt_fee
        _shrink = (_gp - _lp) - (_gp - _with)
        _bcity += (f'<tr><td><a href="{U("/"+_s+"/")}"><b>{_n}</b></a></td>'
                   f'<td>{money(_lp)}{_SM}{html.escape(_l[0]["airname"])}</small></td>'
                   f'<td><b>{money(_with)}</b></td>'
                   f'<td>{money(_gp)}{_SM}{html.escape(_g[0]["airname"])}</small></td>'
                   + (f'<td class="win">廉航仍便宜 {money(_gp - _with)}</td>'
                      if _gp > _with else
                      f'<td class="lose">一般航空便宜 {money(_with - _gp)}</td>')
                   + '</tr>')

    _bjs = ("""
<script>
(function(){
 var $=function(i){return document.getElementById(i)};
 function nt(n){return 'NT$'+Math.round(n).toLocaleString('en-US')}
 function calc(){
  var l=+$('bl').value||0, f=+$('bf').value||0, b=+$('bb').value||0, n=+$('bn').value||0;
  var w=l+b*2*n;
  $('q1').textContent=nt(w);
  $('q2').textContent=nt(f);
  var d=f-w, e=$('qv');
  e.className='cv '+(d>0?'jp':'tw');
  e.textContent = Math.abs(d)<100 ? '兩邊幾乎一樣，那就看時段和服務'
   : (d>0 ? ('廉航加完行李仍便宜 '+nt(d)) : ('一般航空反而便宜 '+nt(-d)));
 }
 ['bl','bf','bb','bn'].forEach(function(i){
   var el=$(i); if(el){el.addEventListener('input',calc)}
 });
 calc();
})();
</script>""")

    _bdemo = None
    for _s, _n, _c, _r, _h in CITIES:
        _f = by_city.get(_s, [])
        _l = sorted([x for x in _f if x['rt'] and x['cls'] == 'lcc'], key=lambda x: x['price'])
        _g = sorted([x for x in _f if x['rt'] and x['cls'] == 'fsc'], key=lambda x: x['price'])
        if _l and len(_g) >= 5:
            _bdemo = (_n, _l[0]['price'], _g[0]['price'])
            break
    _dl = _bdemo[1] if _bdemo else 5000
    _df = _bdemo[2] if _bdemo else 9000

    bg_title = '廉航加了行李，還比較便宜嗎？台日航線託運行李費用實算'
    bg_desc = (f'台灣虎航官方行李價目表、樂桃票種含不含託運，'
               f'以及加購來回 {_REF["kg"]}kg 託運（約 {money(_rt_fee)}）之後，'
               f'廉航與一般航空的價差會縮水多少。附試算。')

    bg_faq = [
     ('廉航的票價為什麼不含行李？',
      '因為那是它的商業模式：把行李、選位、餐食拆開來賣，讓帳面票價看起來最低。'
      f'以台灣虎航為例，基本票種 tigerlight 只含 10 公斤手提行李，'
      f'要託運行李箱就得加購——來回 {_REF["kg"]}kg 是 {money(_rt_fee)}。'),
     ('行李費什麼時候買最便宜？',
      f'訂機票的當下。以虎航台灣出發的公告費率，{_REF["kg"]}kg 在訂票時加購是 '
      f'{money(_REF["per_leg"])}，事後到行程管理加購變 {money(_TG["rows"][1][2])}，'
      f'打客服專線是 {money(_TG["rows"][1][3])}。到機場才買只能買 15 公斤，而且要 '
      f'{money(_TG["rows"][6][4])}——比訂票時買 15 公斤貴了將近一倍。'),
     ('超重怎麼算？',
      f'超過已購買的重量，依啟程站費率按每公斤收。虎航機場櫃檯的超重費是每公斤 '
      f'{money(_TG["over_kg"])}，買個伴手禮就可能超過。'
      '與其在機場被收超重，不如訂票時就把重量買足。'),
     ('一般航空一定含兩件 23 公斤嗎？',
      '不一定。中華航空的官網寫明，經濟艙的免費託運件數依航線與「訂位艙等」而定，'
      '最便宜的促銷艙等和一般經濟艙可能不一樣。'
      '買全服務航空的特價票之前，一樣要確認那個艙等實際含多少行李。'),
     ('為什麼本站只列了三家航空的行李規則？',
      f'因為只有這三家的條件我逐項對過官方頁面。其餘 {len(BG["unverified"])} 家還沒查證，'
      '與其抄別人的整理，不如先空著並說明。本站寧可資料少但每個數字都有出處。'),
    ]
    bg_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                      + html.escape(a) + '</div></details>' for q, a in bg_faq)
    bg_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in bg_faq]}, ensure_ascii=False)

    write('japan-flight-baggage/index.html',
      head(bg_title, bg_desc, 'japan-flight-baggage/',
           '<script type="application/ld+json">' + bg_ld + '</script>')
      + crumbs([('首頁', '/'), ('廉航行李費', None)]) + topnav()
      + '<h1>廉航加了行李，還比較便宜嗎？</h1>'
      + '<p class="lede">比票價的時候，廉航幾乎一定贏。但廉航的最低票價<b>不含託運行李</b>——'
        '那是「只能帶手提行李」的價格。把行李費加回去，價差會縮水多少？</p>'
      + f'<div class="today"><div class="tday">行李費率查證於 {BG["checked"]}'
        f'　·　票價更新於 {NOWS}</div>'
        f'<div class="tans">加購來回 {_REF["kg"]}kg 託運行李是 {money(_rt_fee)}'
        f'（{_REF["airline"]}公告費率）</div>'
        f'<div class="tsub">這筆錢會吃掉廉航與一般航空價差的一大塊。'
        f'下面用本站的即時票價實際算給你看。</div></div>'
      + (('<h2>加上行李之後，還差多少？</h2>'
          '<p class="lede">只列出本站有足夠一般航空紀錄（5 筆以上來回）的航點。</p>'
          '<div class="tw"><table><thead><tr><th>航點</th><th>廉航最低</th>'
          f'<th>＋來回 {_REF["kg"]}kg 行李</th><th>一般航空最低</th><th>結果</th>'
          '</tr></thead><tbody>' + _bcity + '</tbody></table></div>'
          f'<p class="disc">行李費以{_REF["airline"]}公告的 {_REF["kg"]}kg 訂票時加購價'
          f'（單程 {money(_REF["per_leg"])}）估算，實際費率各航空不同。'
          f'一般航空的票價是否含行李，同樣要看訂位艙等。'
          f'兩邊都是本站紀錄中的最低價，不是市場最低。</p>') if _bcity else '')
      + '<h2>自己算</h2>'
      + '<p class="lede">填入你查到的票價與行李費，看加完行李之後誰便宜。</p>'
      + '<div class="calc"><div class="sf">'
        f'<label>廉航票價<input id="bl" type="number" value="{_dl}" min="0" step="100"></label>'
        f'<label>一般航空票價<input id="bf" type="number" value="{_df}" min="0" step="100"></label>'
        f'<label>單程行李費<input id="bb" type="number" value="{_REF["per_leg"]}" '
        'min="0" step="50"></label>'
        '<label>幾個人<input id="bn" type="number" value="1" min="1" max="9" step="1"></label>'
        '</div><div class="cres">'
        '<div class="cl"><span>廉航＋行李</span><b id="q1">—</b></div>'
        '<div class="cl"><span>一般航空</span><b id="q2">—</b></div>'
        '<div class="cv" id="qv">—</div></div></div>'
      + '<p class="disc">行李費以「單程 × 2 × 人數」計算。'
        '若你本來就只帶手提行李，這一項填 0 即可。</p>' + _bjs
      + f'<h2>{html.escape(_REF["airline"])}的行李價目表</h2>'
      + f'<p class="lede">同樣的重量，<b>越晚買越貴</b>。這是少數航空公司會完整公告的費率表，'
        f'可以拿來當台日廉航的參考值。</p>'
      + '<div class="tw"><table><thead><tr><th>項目</th>'
      + ''.join(f'<th>{html.escape(c)}</th>' for c in _TG['cols'])
      + '</tr></thead><tbody>' + _tgrows + '</tbody></table></div>'
      + f'<p class="disc">{html.escape(_TG["period"])}　·　'
        f'資料來源：<a href="{_TG["src"]}" rel="nofollow" target="_blank">'
        f'{html.escape(_TG["src_name"])}</a>，查證於 {BG["checked"]}。'
        f'超重另按每公斤 {money(_TG["over_kg"])} 收取（機場櫃檯費率）。</p>'
      + '<div class="tldr"><ul>'
        f'<li><b>訂票時就買最便宜。</b>{_REF["kg"]}kg 訂票時 {money(_TG["rows"][1][1])}，'
        f'事後線上 {money(_TG["rows"][1][2])}，打客服 {money(_TG["rows"][1][3])}。</li>'
        f'<li><b>機場才買最貴，而且只能買 15 公斤。</b>要 {money(_TG["rows"][6][4])}，'
        f'比訂票時買同樣 15 公斤（{money(_TG["rows"][0][1])}）貴了將近一倍。</li>'
        f'<li><b>超重比加購貴得多。</b>每公斤 {money(_TG["over_kg"])}，'
        f'超個 3 公斤就超過一張 20kg 行李的價格。</li>'
        '</ul></div>'
      + '<h2>哪些票種含託運？</h2>'
      + '<p class="lede">只列出本站逐項對過官方頁面的航空公司。</p>'
      + '<div class="tw"><table><thead><tr><th>航空公司</th><th>類型</th>'
        '<th>託運行李</th><th>來源</th></tr></thead><tbody>' + _farerows + '</tbody></table></div>'
      + f'<p class="disc">其餘 {len(BG["unverified"])} 家飛台日的航空'
        f'（{html.escape("、".join(BG["unverified"][:6]))} 等）本站尚未查證，'
        f'所以不列。與其抄第三方整理，不如先空著。</p>'
      + '<h2>順便看看</h2><div class="cities">'
      + f'<a class="ct" href="{U("/japan-flight-good-times/")}"><b>☀️ 早去晚回</b>'
        f'<s>便宜票常常時段很爛，這裡只留好時段</s></a>'
      + f'<a class="ct" href="{U("/deals/")}"><b>🔥 機票特價</b><s>每日更新</s></a>'
      + f'<a class="ct" href="{U("/okinawa/")}"><b>沖繩機票</b><s>廉航與一般航空並列</s></a></div>'
      + '<h2>常見問題</h2>' + bg_html
      + '<p class="disc">行李費率與票種內容由各航空公司隨時調整，'
        '本頁數字查證於 ' + BG['checked'] + '，購票前請以航空公司官網為準。</p>'
      + foot())
    pages.append(('/japan-flight-baggage/', 0.7))

# ---------- 地區頁（導覽用，非 SEO 主力）----------
for reg,rname in REGIONS:
    cs=[c for c in CITIES if c[3]==reg]
    cs.sort(key=lambda c: sort_key(by_city.get(c[0], [])))
    n=sum(len(by_city.get(c[0],[])) for c in cs)
    b=min([best_labeled(by_city[c[0]])[0]['price'] for c in cs if by_city.get(c[0])] or [0])
    title=f'{rname}機票｜台灣飛{rname}各城市便宜機票一覽'
    desc=f'台灣飛{rname}（{"、".join(c[1] for c in cs[:5])}）的機票比較，' + (f'最低 {money(b)} 起，' if b else '') + f'共 {n} 筆票價，每日更新。'
    cards=''.join(
        f'<a class="ct" href="{U("/"+s+"/")}"><b>{nm}</b><s>{"、".join(DEST[k][1] for k in codes if k in DEST)}</s>'
        + (f'<u>{money(best_labeled(by_city[s])[0]["price"])}'
           f'<small> 起 · {best_labeled(by_city[s])[1]}含稅 · {len(by_city[s])} 筆</small></u>'
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
                 key=lambda c: sort_key([y for y in fs if CITY_OF[y['d']][0]==c]))
    title=f'{oname}飛日本機票｜{len(dests)} 個航點比價，最低 {money(b["price"])}（{NOW.year}年更新）'
    desc=(f'{oname}出發飛日本 {len(dests)} 個城市的機票整理，最低 {money(b["price"])}'
          f'（{"來回" if b["rt"] else "單程"}含稅，{b["airname"]}）。共 {len(fs)} 筆票價，每日更新。')
    cards=''
    for c in dests:
        sub=[x for x in fs if CITY_OF[x['d']][0]==c]
        bb,lbl=best_labeled(sub)
        if not bb: continue
        href=U(f'/{oslug}/{c}/') if (oslug,c) in route_pages else U(f'/{c}/')
        cards+=(f'<a class="ct" href="{href}"><b>{oname} → {CITY[c][1]}</b>'
                f'<s>{REGNAME[CITY[c][3]]}</s>'
                f'<u>{money(bb["price"])}<small> 起 · {lbl}含稅 · {len(sub)} 筆</small></u></a>')
    write(f'{oslug}/index.html', head(title,desc,f'{oslug}/')
        + crumbs([('首頁','/'),(f'{oname}飛日本機票',None)]) + topnav()
        + f'<h1>{oname}飛日本機票</h1>'
        + f'<p class="lede">{oname}出發飛日本共 <b>{len(dests)}</b> 個航點，'
          f'目前最低 <b>{money(b["price"])}</b>（{"來回" if b["rt"] else "單程"}含稅）。'
          f'下方各航點價格以來回為準，僅有單程紀錄者另行標示。</p>'
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
    cs.sort(key=lambda c: sort_key(by_city.get(c[0], [])))
    cards=''.join(
        f'<a class="ct" href="{U("/"+s+"/")}"><b>{nm}</b><s>{REGNAME[reg]}</s>'
        + (f'<u>{money(best_labeled(by_city[s])[0]["price"])}'
           f'<small> 起 · {best_labeled(by_city[s])[1]}</small></u>'
           if by_city.get(s) else '<u style="color:var(--dim);font-weight:400;font-size:.8rem">查詢票價</u>')
        + '</a>' for s,nm,_,_,_ in cs)
    sections+=f'<h2 id="{reg}"><a href="{U("/"+reg+"/")}" style="text-decoration:none;color:inherit">{rname}</a></h2><div class="cities">{cards}</div>'

_ALLTC = min((x['price'] for x in deals
              if x.get('gate') == 'Trip.com' and x['rt']), default=None)
write('index.html', head(title,desc,'')
  + crumbs([('首頁',None)]) + topnav()
  + f'<h1>台日機票速報</h1>'
  + f'<p class="lede">台灣飛日本 <b>{len(CITIES)}</b> 個城市的便宜機票整理，價格含稅含手續費。'
    f'目前最低 <b>{money(allbest)}</b> 來回含稅'
    + (f'；<b>只看 Trip.com 是 {money(_ALLTC)}</b>（跨平台的低價常來自台灣較陌生的訂票網站）'
       if _ALLTC and _ALLTC > allbest else '')
    + '。</p>'
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
            f'<u>{money(best_labeled(by_origin[o])[0]["price"])}'
            f'<small> 起 · {best_labeled(by_origin[o])[1]}</small></u></a>'
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
        mb = month_base(rts, b['dep'][:7])
        ur = usual_range(rts)
        if mb and b['price'] < mb[0] * 0.9:
            avg, nd = mb
            y, mo = b['dep'][:7].split('-')
            reasons.append(('discount',
                f'{int(mo)} 月出發的票，每天最便宜的平均要 {money(avg)}'
                f'（{nd} 天有紀錄），這張低 {round((1-b["price"]/avg)*100)}%'))
        elif ur and b['price'] < ur[0]:
            lo, hi, ndays = ur
            reasons.append(('discount',
                f'這條航線平常最低落在 {money(lo)}–{money(hi)}，'
                f'這張是近期 {len(rts)} 筆紀錄中第 {rank_among(b["price"], rts)} 低'))
        if reasons:
            k=(oslug,cslug)
            if k not in picked or b['price']<picked[k][0]['price']:
                picked[k]=(b,reasons,med,rts)
    return picked

def month_base(rts, month):
    """該月「每天最便宜的票」平均多少——讀者規劃行程是以月為單位。

    刻意不用全部票價的平均或中位數：樣本含冷門日期與轉機貴票，
    東京 10 月全部平均 13,307、每日最低平均 10,010，用前者會把
    折扣說成 52%，但沒有人會去買那些貴票，等於灌水。"""
    by = collections.defaultdict(list)
    for x in rts:
        if x.get('dep', '')[:7] == month:
            by[x['dep']].append(x['price'])
    if len(by) < 5:
        return None
    daily = [min(v) for v in by.values()]
    return round(statistics.mean(daily)), len(daily)


def usual_range(rts):
    """這條航線「平常最低要多少」。

    取每個出發日的最低價，再去掉頭尾各 10%，得到一個讀者認得出來的區間。
    不用全部票價的中位數——樣本含大量冷門日期與轉機票，中位數會被拉高，
    講「低於中位價 53%」聽起來很漂亮，但讀者沒有那個基準，等於沒說。"""
    by = collections.defaultdict(list)
    for x in rts:
        if x.get('dep'):
            by[x['dep']].append(x['price'])
    daily = sorted(min(v) for v in by.values())
    if len(daily) < 6:
        return None
    k = max(1, len(daily) // 10)
    return daily[k], daily[-k - 1], len(daily)


def rank_among(price, rts):
    """在本站近期紀錄中排第幾低（1 為最低）"""
    return sum(1 for x in rts if x['price'] < price) + 1


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
          + (lambda ur, mb: (f'<p class="lede" style="font-size:.86rem">此航線目前共 {len(rts)} 筆來回票價。'
                    + (f'{b["dep"][5:7].lstrip("0")} 月有 {mb[1]} 天留下紀錄，'
                       f'每天最便宜的票平均 {money(mb[0])}。' if mb else '')
                    + (f'整體而言每日最低價多落在 {money(ur[0])}–{money(ur[1])}。' if ur else '')
                    + '</p>')
             )(usual_range(rts), month_base(rts, b['dep'][:7])))
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
        med=int(med),url=b['url'],hotelcity=hotelcity,cslug=cslug,
        usual=(lambda ur: {'lo':ur[0],'hi':ur[1],'days':ur[2]} if ur else None)(usual_range(rts)),
        mbase=(lambda m: {'avg':m[0],'days':m[1],'month':int(b['dep'][5:7])} if m else None)(
            month_base(rts, b['dep'][:7])),
        rank=rank_among(b['price'],rts), n=len(rts)))

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
  + f'<h1>機票特價</h1><p class="lede">低於門檻、或明顯低於該航線平常最低價的票，今日共 <b>{len(deals_out)}</b> 則。</p>'
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
             f"{AFF_Q}&trip_sub1={_dc}"
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
    # 臨界匯率：日圓漲到這個價位時，日本免稅價與台灣售價打平
    def be(p): return p['twd']*TAXR/p['jpy']
    def gap_ex(p): return p['twd']-round(p['jpy']/TAXR*RATE)
    _win=[p for p in iph if gap_ex(p)>0]
    _tight=min(_win,key=be) if _win else None      # 最先失去價差的機種
    _buf=(be(_tight)/RATE-1)*100 if _tight else 0
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
     ('可以先在日本 Apple 官網預購，到日本再取貨嗎？',
      '很難。Apple 日本線上商店明確載明「僅在日本國內銷售及配送，不進行日本國外的配送」，'
      '且銷售條款規定線上購買的產品不得出口。到店取貨在制度上可行，但取貨人姓名必須與購買人相同，'
      '並須出示政府機關核發的有效附照片證件。付款與帳單地址也需為日本，海外發行的信用卡常無法通過。'),
     ('直接飛過去到 Apple Store 店頭買得到嗎？',
      '不一定，要看機種。Apple 自 2026 年 2 月 6 日起，針對 iPhone 17、17 Pro、17 Pro Max 停止直營店的'
      '現貨臨櫃販售，即使店內有貨也須先在官網或 Apple Store App 下單，再指定當日到店取貨，'
      '這是針對轉售的管制；同期的 iPhone Air 與 16 系列則不受此限。'
      '這項作法是否沿用到 iPhone 18 Pro 與 iPhone Duo，Apple 尚未說明，也有報導指出發售日店內有貨時'
      '仍可能直接購買。無論如何，新機上市初期供給吃緊，想當天空手走進去帶一支回來並不容易。'
      '若要免稅，仍須到 Bic Camera、Yodobashi 等有 Tax-Free 標示的量販店。'),
     ('2026 年 11 月起日本的免稅方式會改變嗎？',
      '會，而且改得很徹底。自 2026 年 11 月 1 日起日本改採「退款方式」（リファンド方式）：'
      '購買當下一律先支付含稅全額，出境時經海關確認後，再由店家退還消費稅。'
      '同時取消一般物品與消耗品的區分，以及消耗品 50 萬日圓的上限。'
      '換句話說，11 月起在店裡不再直接拿到免稅價，須先墊付稅金並在離境時完成手續才拿得回來，'
      '本頁「退稅後」欄位仍可視為最終實際負擔，但付款當下的金額會是含稅價。'),
     ('日本買的 iPhone 快門聲可以關嗎？',
      '別把這點當成買日版的理由。快門聲限制綁在機器的銷售地版本（日本為 J/A，韓國與中國大陸機種亦同），'
      '而非綁在使用地；日本媒體普遍說明日版無法關閉快門聲。至於帶到國外是否就會靜音，'
      '各方實測說法不一致，Apple 未公布判定規則，也未承諾任何行為。'
      '若你在意拍照有聲音，最保險的做法是不要買日版。'),
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


    _berows=''.join(
        f'<tr><td><b>{html.escape(p["name"])}</b>{SMALL}{html.escape(p["spec"])}</small></td>'
        f'<td class="win">{money(gap_ex(p))}</td>'
        f'<td><b>{be(p):.4f}</b></td><td>{(be(p)/RATE-1)*100:.1f}%</td></tr>'
        for p in sorted(iph,key=be))
    betable=('<h2>匯率要變多少，結論才會翻盤？</h2>'
             '<p class="lede">日圓升值時，日本售價換算成台幣就會變貴，價差隨之縮小。'
             '下表是各機種「日本免稅價與台灣售價打平」的臨界匯率——'
             f'目前匯率 {RATE}，離臨界值越近的機種越禁不起日圓走強。</p>'
             '<div class="tw"><table><thead><tr><th>型號</th>'
             '<th>免稅買現在省</th><th>臨界匯率</th><th>日圓還需升值</th>'
             '</tr></thead><tbody>'+_berows+'</tbody></table></div>'
             '<p class="disc">臨界匯率＝台灣售價 × 1.1 ÷ 日圓售價。'
             '未計入刷卡國外交易手續費與量販店手續費，實際緩衝會更小。</p>')

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
                 + fare_cta('tokyo','為了省幾千元專程飛一趟？先看這個數字')
                 + cta('hotel','東京','東京','機票看好了，住宿呢',
                       f'到 {P["hotel"]["brand"]} 查房價，繁體中文、台幣計價',
                       track='apple-tokyo')
                 + '<div class="cities">'
                 + f'<a class="ct" href="{U("/tokyo/")}"><b>東京機票</b><s>各出發地比價</s></a>'
                 + f'<a class="ct" href="{U("/osaka/")}"><b>大阪機票</b><s>心齋橋、道頓堀</s></a>'
                 + f'<a class="ct" href="{U("/deals/")}"><b>機票特價</b><s>每日更新</s></a></div>')

    # ── 信用卡試算：回饋往往比台日價差還大 ────────────────
    _MID = AP['rate'].get('jpy_twd_mid') or RATE
    _SPREAD = AP['rate'].get('spread', 0.016)
    # 海外回饋 3%、手續費 1.5% 的前提下，台灣回饋要多高才會抵銷日本價差
    def _flip(p): return 1 - (p['jpy']/TAXR*_MID*1.015*0.97)/p['twd']
    _fl = sorted((_flip(p), p) for p in NEWP if p['cat'] == 'iPhone')
    _flo, _fhi = _fl[0], _fl[-1]
    _opts = ''.join(
        f'<option value="{p["jpy"]}|{p["twd"]}">{html.escape(p["name"])} {html.escape(p["spec"])}</option>'
        for p in NEWP if p['cat'] == 'iPhone')
    _cjs = ("""
<script>
(function(){
 var MID=%MID%, FEE0=1.5, SPREAD=%SPREAD%;
 var $=function(i){return document.getElementById(i)};
 function nt(n){return 'NT$'+Math.round(n).toLocaleString('en-US')}
 function calc(){
  var v=$('cm').value.split('|'), jpy=+v[0], twd=+v[1];
  var ov=(+$('co').value||0)/100, dm=(+$('cd').value||0)/100, fee=(+$('cf').value||0)/100;
  var base=($('cw').value==='ex')? jpy/1.1 : jpy;          // 量販店免稅價／直營店含稅價
  var jp=($('cp').value==='card')? base*MID*(1+fee)*(1-ov) // 刷卡：手續費後再扣回饋
                                 : base*MID*(1+SPREAD);    // 付現：換匯成本，無回饋
  var tw=twd*(1-dm);
  var d=tw-jp;
  $('r1').textContent=nt(tw); $('r2').textContent=nt(jp);
  var e=$('rv');
  e.className='cv '+(d>0?'jp':'tw');
  e.textContent=(Math.abs(d)<100)?('兩邊幾乎一樣（相差 '+nt(Math.abs(d))+'），不值得為此特地安排')
   :(d>0?('日本便宜 '+nt(d)):('台灣便宜 '+nt(-d)+'，回饋已經吃掉價差'));
 }
 ['cm','co','cd','cf','cw','cp'].forEach(function(i){
   var el=$(i); if(el){el.addEventListener('input',calc);el.addEventListener('change',calc);}
 });
 calc();
})();
</script>""").replace('%MID%', f'{_MID}').replace('%SPREAD%', f'{_SPREAD}')

    calcblock = (
      '<h2>加上信用卡回饋，結論會變嗎？</h2>'
      '<p class="lede">會，而且可能整個翻過來。台灣的刷卡回饋同樣算數——'
      f'假設海外刷卡回饋 3%、手續費 1.5%，國內回饋只要達到 '
      f'<b>{_flo[0]*100:.1f}%</b>（{_flo[1]["name"]} {_flo[1]["spec"]}）到 '
      f'<b>{_fhi[0]*100:.1f}%</b>（{_fhi[1]["name"]} {_fhi[1]["spec"]}），'
      f'日本的免稅價差就被完全抵銷。新機上市期間國內通路的加碼活動'
      f'確實出現過這個量級，所以別只看機身標價。'
      '海外刷卡則要先加上國外交易手續費（多數發卡行約 1.5%：國際組織 1% ＋ 發卡行 0.5%，'
      '金管會規定發卡行加收不得逾 0.5%；美國運通約 2%）。填入你自己那張卡的條件試算：</p>'
      '<div class="calc"><div class="sf">'
      f'<label>機型<select id="cm">{_opts}</select></label>'
      '<label>日本買法<select id="cw">'
      '<option value="ex">量販店免稅價</option>'
      '<option value="inc">Apple 直營店含稅價</option></select></label>'
      '<label>日本付款<select id="cp">'
      '<option value="card">刷卡</option><option value="cash">付現</option></select></label>'
      '<label>海外回饋 %<input id="co" type="number" value="3" min="0" max="30" step="0.1"></label>'
      '<label>國內回饋 %<input id="cd" type="number" value="3" min="0" max="30" step="0.1"></label>'
      '<label>國外手續費 %<input id="cf" type="number" value="1.5" min="0" max="5" step="0.1"></label>'
      '</div>'
      '<div class="cres">'
      '<div class="cl"><span>台灣實付</span><b id="r1">—</b></div>'
      '<div class="cl"><span>日本實付</span><b id="r2">—</b></div>'
      '<div class="cv" id="rv">—</div></div></div>'
      f'<p class="disc">以中間匯率 {_MID} 為基準：刷卡加計手續費後再扣回饋；'
      f'付現以中間匯率加 {round(_SPREAD*100,1)}% 換匯成本計算，且沒有刷卡回饋。'
      '各卡網實際結匯匯率與入帳日匯率會有差異，回饋多有上限與登錄條件，'
      '結果僅供比較用，請以你的發卡行公告為準。</p>' + _cjs)
    _APPLE_CALC = calcblock

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
      + '<h2>今天的答案</h2>'
      + (f'<div class="today"><div class="tday">{AP["updated"]} · 換算匯率 {RATE}'
         f'（每 1 日圓 ≈ NT${RATE}）· 每日自動更新</div>'
         f'<div class="tans">在日本量販店以免稅價買，{len(_win)}／{len(iph)} 款新機比台灣便宜</div>'
         f'<div class="tsub">最多省 {money(top_save)}（{top["name"]} {top["spec"]}）。'
         f'但在 Apple 直營店買含稅價，{cheap_tw} 款反而是台灣較低——直營店自 2024/6 起已不能退稅。</div>'
         + (f'<div class="tbuf">還有多少緩衝？日圓只要再升值 <b>{_buf:.1f}%</b>'
            f'（匯率升到 <b>{be(_tight):.4f}</b>），{_tight["name"]} {_tight["spec"]} 就會失去價差，'
            f'成為第一個不划算的機種。</div>' if _tight else '')
         + '</div>')
      + '<h3>細節</h3><div class="tldr"><ul>'
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
      + betable
      + _APPLE_CALC
      + '<h2>先別急著比標價</h2>'
      + '<p class="lede">台日價差多半是幾千元，但同一支機器兩三年後的<b>回收價</b>差距'
        '往往比這個大。用台灣實際的二手回收行情把機身價攤成每月成本，'
        '常常會得到和比標價不一樣的結論。</p>'
      + '<div class="cities">'
      + f'<a class="ct" href="{U("/iphone-cost/")}"><b>📉 iPhone 持有成本試算</b>'
        f'<s>用實際回收行情算每月多少</s></a></div>'
      + '<h2>買之前要知道的兩件事</h2>'
      + '<h3>1. Apple 直營店已經不能退稅</h3>'
      + '<p class="lede">Apple 日本直營店自 2024 年 6 月起取消對外國旅客的免稅服務。'
        '要拿到免稅價，必須到有 Tax-Free 標示的家電量販店（Bic Camera、Yodobashi Camera 等），'
        '結帳時出示護照。量販店定價未必與 Apple 官網相同，且部分店家收取手續費，請現場確認。</p>'
      + fare_cta('tokyo','要去量販店掃貨？機票現在多少')
      + '<h3>2. 保固是區域性的</h3>'
      + '<p class="lede">日本購買的 iPhone 在台灣的 Apple 授權維修中心可能不受理，需寄回日本處理。'
        '省下的幾千元，遇到一次維修就可能不划算。快門聲也一樣要先想清楚：'
        '限制綁在銷售地版本（日本為 J/A），帶出國是否就會靜音各方實測說法不一，'
        'Apple 未公布判定規則，在意的話不要買日版。</p>'
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

    # ── iPhone 持有成本：用台灣實際二手回收行情攤提 ──────────────
    # 網路上談「持有成本」多半自己假設一個殘值，數字沒有來源。
    # 這裡改成反過來做：拿收購商今天公開的回收報價，除以該機種當年的
    # 官方售價，得到「實際上掉了多少」，再用這條曲線去攤新機。
    if os.path.exists('resale.json'):
        RS = json.load(open('resale.json', encoding='utf-8'))

        def _yrs(launch):
            d = datetime.date(*map(int, launch.split('-')))
            return max(1, round((NOW.date() - d).days / 365.25))

        # 殘值率一律以「參考容量」計算，優先取 256GB。
        # 若改成逐容量比對，同一個機型在不同年份會落在不同基準上
        #（例如滿一年的 Pro Max 只有 256GB 報價、滿兩年的有 512GB），
        # 算出來的每月成本會出現「用兩年比用一年還貴」這種假訊號。
        REFCAP = ('256GB', '128GB', '512GB', '1TB')
        RES = {}                      # tier → 年 → {rate, spec, name, list, resale}
        for r in RS['rows']:
            caps = {c[0]: c for c in r['caps']}
            spec = next(c for c in REFCAP if c in caps)
            _, lst, res = caps[spec]
            RES.setdefault(r['tier'], {})[_yrs(r['launch'])] = {
                'rate': res / lst, 'spec': spec, 'name': r['name'],
                'launch': r['launch'], 'list': lst, 'resale': res}

        def rate_of(tier, y, spec=None):
            s = RES.get(tier, {}).get(y)
            return s['rate'] if s else None

        def tier_of(n):
            if n.endswith('Pro Max'): return 'Pro Max'
            if n.endswith('Pro'): return 'Pro'
            if n.endswith('Air'): return 'Air'
            if n.replace('iPhone ', '').isdigit(): return '標準'
            return None                      # iPhone Duo 等新形態，沒有可比的回收行情

        def mcost(twd, tier, y, spec):
            rt = rate_of(tier, y, spec)
            if rt is None: return None
            keep = round(twd * rt)
            return {'keep': keep, 'cost': twd - keep, 'm': round((twd - keep) / (y * 12))}

        _YRS = sorted({_yrs(r['launch']) for r in RS['rows']})
        _SRC = f'<a href="{RS["src"]}" rel="nofollow" target="_blank">{html.escape(RS["src_name"])}</a>'
        TIERS_ALL = [t for t in ('Pro Max', 'Pro', '標準', 'Air') if t in RES]

        # 1. 實際折舊表（各機種基本容量）
        _drows2 = ''
        for t in TIERS_ALL:
            for y in sorted(RES.get(t, {})):
                d = RES[t][y]
                _drows2 += (f'<tr><td><b>{html.escape(d["name"])}</b>{SMALL}{d["spec"]}</small></td>'
                            f'<td>{d["launch"].replace("-", "/")}</td><td>{y} 年</td>'
                            f'<td>{money(d["list"])}</td><td><b>{money(d["resale"])}</b></td>'
                            f'<td class="win">{d["rate"] * 100:.0f}%</td>'
                            f'<td class="lose">−{money(d["list"] - d["resale"])}</td></tr>')

        # 2. 殘值率速查（等級 × 年數）
        _mrows = ''
        for t in TIERS_ALL:
            cells = ''.join(
                (f'<td><b>{rate_of(t, y) * 100:.0f}%</b></td>' if rate_of(t, y) else '<td>—</td>')
                for y in _YRS)
            _mrows += f'<tr><td><b>{t}</b></td>{cells}</tr>'

        # 3. 容量加價的殘值（同一支機器，最小容量 → 最大容量）
        _crows = ''
        for r in RS['rows']:
            if len(r['caps']) < 2: continue
            s0, l0, v0 = r['caps'][0]
            s1, l1, v1 = r['caps'][-1]
            up, back = l1 - l0, v1 - v0
            _crows += (f'<tr><td><b>{html.escape(r["name"])}</b>{SMALL}{s0} → {s1}</small></td>'
                       f'<td>{_yrs(r["launch"])} 年</td>'
                       f'<td>＋{money(up)}</td><td>＋{money(back)}</td>'
                       f'<td class="lose">{back / up * 100:.0f}%</td>'
                       f'<td class="win">{v0 / l0 * 100:.0f}%</td></tr>')

        # 4. 在售新機的每月成本
        _NEWI = [p for p in AP['products'] if p['cat'] == 'iPhone']
        _nrows = ''
        for p in _NEWI:
            t = tier_of(p['name'])
            cells = ''
            for y in _YRS:
                m = mcost(p['twd'], t, y, p['spec']) if t else None
                cells += f'<td><b>NT${m["m"]:,}</b></td>' if m else '<td>—</td>'
            _nrows += (f'<tr><td><b>{html.escape(p["name"])}</b>{SMALL}{p["spec"]}</small></td>'
                       f'<td>{money(p["twd"])}</td>{cells}</tr>')
        _nodata = sorted({p['name'] for p in _NEWI if not tier_of(p['name'])})

        # 5. 標題數字：Pro 與 Pro Max 攤到每月差多少
        def _pick(tier, spec='256GB'):
            return next((p for p in _NEWI
                         if p.get('new') and tier_of(p['name']) == tier and p['spec'] == spec), None)
        _P, _PM = _pick('Pro'), _pick('Pro Max')
        _hl = ''
        if _P and _PM:
            _a2, _b2 = mcost(_P['twd'], 'Pro', 2, '256GB'), mcost(_PM['twd'], 'Pro Max', 2, '256GB')
            _a1, _b1 = mcost(_P['twd'], 'Pro', 1, '256GB'), mcost(_PM['twd'], 'Pro Max', 1, '256GB')
            _gap = _PM['twd'] - _P['twd']
            _d2 = _b2['m'] - _a2['m']
            _d1 = _b1['m'] - _a1['m']
            _hl = (f'<div class="today">'
                   f'<div class="tday">{RS["updated"]} · 殘值取自{RS["src_name"]}當日公開報價</div>'
                   f'<div class="tans">{_P["name"]} 每月 NT${_a2["m"]:,}，'
                   f'{_PM["name"]} 每月 NT${_b2["m"]:,}——用兩年，每月只差 '
                   f'NT${abs(_d2):,}</div>'
                   f'<div class="tsub">標價差 {money(_gap)} 看起來很多，但 Pro Max 兩年後的回收價'
                   f'（{money(_b2["keep"])}）比 Pro（{money(_a2["keep"])}）高 '
                   f'{money(_b2["keep"] - _a2["keep"])}，把差價吃掉了大半。</div>'
                   f'<div class="tbuf">一年就換的人更極端：Pro 每月 <b>NT${_a1["m"]:,}</b>、'
                   f'Pro Max 每月 <b>NT${_b1["m"]:,}</b>，'
                   + (f'<b>Pro Max 反而便宜 NT${-_d1:,}</b>——高階機種掉價慢，持有期越短越吃香。'
                      if _d1 < 0 else f'差距 NT${_d1:,}。') +
                   f'</div></div>')

        # 6. 去日本買，攤到每月剩多少
        _jt = by_city.get('tokyo') or []
        _jb = (best(_jt, True) or best(_jt, False)) if _jt else None
        FARE = _jb['price'] if _jb else 6000
        _jp_blk = ''
        if _P:
            _jex = round(_P['jpy'] / TAXR * RATE)
            _sv = _P['twd'] - _jex
            _sv_m = round(_sv / 24)
            _fa_m = round(FARE / 24)
            _jp_blk = (
              '<h2>去日本買，攤到每月省多少？</h2>'
              f'<p class="lede">以 {_P["name"]} {_P["spec"]} 為例：在日本量販店以免稅價買約 '
              f'{money(_jex)}，比台灣的 {money(_P["twd"])} 少 <b>{money(_sv)}</b>。'
              f'聽起來不錯，但攤到兩年只有<b>每月 NT${_sv_m:,}</b>——'
              f'而台北飛東京目前最低 {money(FARE)}，同樣攤兩年是<b>每月 NT${_fa_m:,}</b>。'
              + (f'機票比省下來的多 {money(FARE - _sv)}，'
                 '專程為了買手機飛一趟，怎麼算都是虧的；本來就要去日本才順便買。'
                 if FARE > _sv else
                 f'這種票價下確實還有得賺，但價差只要縮小 {money(FARE - _sv + 1)} 就翻盤。')
              + '</p>'
              + fare_cta('tokyo', '本來就要去？看今天飛東京多少')
              + f'<p class="disc">日本免稅價為日本含稅價扣除 10% 消費稅後以匯率 {RATE} 換算；'
                '刷卡另有約 1.5% 國外交易手續費未計入。另外，日版（J/A）機在台灣二手市場'
                '通常被收購商另行折價，本頁無法取得公開的折價幅度，'
                '但方向是讓日本的價差再縮小一些。</p>')

        # 7. 舊機漲價
        HK = RS.get('hike') or {}
        _hrows = ''.join(
            f'<tr><td><b>{html.escape(n)}</b></td><td>{money(o)}</td><td><b>{money(w)}</b></td>'
            f'<td class="lose">＋{money(w - o)}</td></tr>' for n, o, w in HK.get('items', []))
        _hike_blk = (
          '<h2>提醒：舊機今年不但沒降，還漲了</h2>'
          f'<p class="lede">「等半年買舊款比較便宜」這個假設，{HK.get("date", "")} 起在台灣失效了——'
          f'Apple 同日調高了仍在架上的舊機售價。這會直接墊高你的持有成本，'
          f'也代表二手行情不會像過去那樣一路走低。</p>'
          '<div class="tw"><table><thead><tr><th>機型</th><th>原價</th><th>現價</th><th>漲幅</th>'
          '</tr></thead><tbody>' + _hrows + '</tbody></table></div>'
          f'<p class="disc">現價為 Apple 台灣官網目前定價。'
          f'注意 iPhone 16 等更早的機種在 iPhone 17 上市時曾調降，本次是調回，不列入本表。</p>'
          ) if _hrows else ''

        # 8. 計算機
        _RJS = json.dumps({f'{t}|{y}': round(d['rate'], 4)
                           for t, ys in RES.items() for y, d in ys.items()}, ensure_ascii=False)
        _PJS = json.dumps([{'n': p['name'], 's': p['spec'], 't': tier_of(p['name']) or '',
                            'tw': p['twd'], 'jp': round(p['jpy'] / TAXR * RATE)}
                           for p in _NEWI], ensure_ascii=False)
        _kdef = next((i for i, p in enumerate(_NEWI)
                      if _P and p['name'] == _P['name'] and p['spec'] == _P['spec']),
                     next((i for i, p in enumerate(_NEWI) if tier_of(p['name'])), 0))
        _kopts = ''.join(
            f'<option value="{i}"{" selected" if i == _kdef else ""}>'
            f'{html.escape(p["name"])} {html.escape(p["spec"])}</option>'
            for i, p in enumerate(_NEWI))
        _kyrs = ''.join(f'<option value="{y}"{" selected" if y == 2 else ""}>{y} 年</option>'
                        for y in _YRS)
        _kjs = ("""
<script>
(function(){
 var R=%R%, P=%P%;
 var $=function(i){return document.getElementById(i)};
 function nt(n){return 'NT$'+Math.round(n).toLocaleString('en-US')}
 function rate(t,y){var v=R[t+'|'+y]; return v||null;}
 function fill(){
  var p=P[+$('km').value], y=+$('ky').value, a=rate(p.t,y);
  $('kr').value = a ? (a*100).toFixed(1) : '';
  $('kn').textContent = a ? ('同級機種滿 '+y+' 年的實際行情') : '這個機型還沒有可比的回收行情，請自行填入';
  calc();
 }
 function calc(){
  var p=P[+$('km').value], y=+$('ky').value, raw=$('kr').value;
  if(raw===''){
    ['rk','rc','r1','r2','r3'].forEach(function(i){$(i).textContent='—'});
    $('rv').className='cv'; $('rv').textContent='這個機型沒有可比的回收行情，填入你自己的預期殘值才算得出來';
    return;
  }
  var rt=(+raw||0)/100, fare=+$('kf').value||0, mo=y*12;
  var kT=p.tw*rt, kJ=p.jp*rt;
  var mT=(p.tw-kT)/mo, mJ=(p.jp-kJ)/mo, mJF=(p.jp-kJ+fare)/mo;
  $('rk').textContent=nt(kT);
  $('rc').textContent=nt(p.tw-kT);
  $('r1').textContent=nt(mT);
  $('r2').textContent=nt(mJ);
  $('r3').textContent=nt(mJF);
  var d=mT-mJF, e=$('rv');
  e.className='cv '+(d>0?'jp':'tw');
  e.textContent = (Math.abs(d)<10) ? '算上機票，兩邊每月幾乎一樣'
   : (d>0 ? ('連機票都算進去，日本每月仍省 '+nt(d))
          : ('把機票攤進去，日本每月反而多 '+nt(-d)+'——本來就要去才划算'));
 }
 ['km','ky'].forEach(function(i){$(i).addEventListener('change',fill)});
 ['kr','kf'].forEach(function(i){$(i).addEventListener('input',calc)});
 fill();
})();
</script>""").replace('%R%', _RJS).replace('%P%', _PJS)

        _kcalc = (
          '<h2>算你自己的</h2>'
          '<p class="lede">殘值率會依機型與年數自動帶入上表的實際行情，你也可以改成自己的預期。'
          '機票預設帶入台北飛東京目前的最低來回含稅價。'
          '殘值率在這裡只取到小數點一位，算出來的每月成本可能與上表差個位數。</p>'
          '<div class="calc"><div class="sf">'
          f'<label>機型<select id="km">{_kopts}</select></label>'
          f'<label>打算用幾年<select id="ky">{_kyrs}</select></label>'
          '<label>屆時殘值 %<input id="kr" type="number" value="50" min="0" max="100" step="0.1"></label>'
          f'<label>來回機票<input id="kf" type="number" value="{FARE}" min="0" step="100"></label>'
          '</div>'
          '<p class="disc" id="kn">—</p>'
          '<div class="cres">'
          '<div class="cl"><span>屆時估計回收價</span><b id="rk">—</b></div>'
          '<div class="cl"><span>總持有成本</span><b id="rc">—</b></div>'
          '<div class="cl"><span>台灣買，每月</span><b id="r1">—</b></div>'
          '<div class="cl"><span>日本免稅買，每月</span><b id="r2">—</b></div>'
          '<div class="cl"><span>日本買＋機票，每月</span><b id="r3">—</b></div>'
          '<div class="cv" id="rv">—</div></div></div>' + _kjs)

        _kfaq = [
         ('殘值率是怎麼算出來的？',
          f'用收購商今天公開的回收報價，除以那支機器當年在 Apple 台灣官網的建議售價。'
          f'例如 iPhone 16 Pro Max 256GB 當年賣 NT$44,900，{RS["src_name"]}今天收 NT$24,820，'
          f'滿兩年的殘值率就是 55%。這不是假設值，是可以自己去對的公開報價；'
          f'回收價查詢日期為 {RS["updated"]}。'),
         ('為什麼 Pro 和 Pro Max 每月成本差不多？',
          '因為 Pro Max 掉價比較慢。標價雖然貴幾千元，但兩年後的回收價也高幾千元，'
          '一來一往之後，真正花掉的錢相差有限。反過來說，如果你買 Pro 的理由是「比較便宜」，'
          '這個理由其實不太成立；買 Pro 合理的理由是機身比較輕、比較好單手操作。'),
         ('一年就換新機，是不是很浪費？',
          '比想像中溫和，但仍然最貴。上市滿一年的機種殘值還有六到七成，所以一年換一次的'
          '每月成本大約比用兩年高兩三成；用越久越便宜的方向沒有變，只是差距沒有直覺上那麼大。'
          '另一個常被忽略的點是，持有期越短，高階機種越有利，因為它掉價慢。'),
         ('升級容量划算嗎？',
          '從殘值的角度看是最不划算的一筆。整支機器兩年後大約還有五成價值，'
          '但「容量加價」的部分通常只剩三成上下，滿三年更低。'
          '如果你不確定要不要多花錢升級容量，可以把它想成一筆折舊特別快的支出。'),
         ('二手回收價和自己賣差多少？',
          '收購商報價是你最快、最確定拿得到的數字，不用議價、不用面交、不用處理糾紛，'
          '代價是比自售低。自己在拍賣平台通常能賣得更高，但要花時間、承擔詐騙與售後爭議風險。'
          '本頁一律採用收購價，算出來的持有成本會偏保守。'),
         ('日本買的 iPhone，殘值一樣嗎？',
          '通常比較低。日版機（型號 J/A）在台灣二手市場常被收購商另行折價，'
          '原因包括快門聲無法關閉與保固屬區域性。'
          '各家折價幅度沒有公開，本頁無法量化，但方向明確：'
          '會讓台日價差再縮小一點，計算時請自行保守一些。'),
         ('這個數字有算保護殼、AppleCare+ 嗎？',
          '沒有，只算機身。若加購 AppleCare+，等於每月再多一筆固定支出，'
          '但相對地，有保固的機器在回收時比較不會因為外觀或功能瑕疵被大幅殺價。'
          '電信資費與配件也都不在本頁範圍內。'),
         ('回收價會變嗎？',
          '會，而且變得不慢。收購商會依市場狀況調整報價，新機發表、記憶體漲價、'
          '甚至某個容量在二手市場缺貨，都會讓報價在幾週內移動數千元。'
          f'本頁的回收價查詢於 {RS["updated"]}，決定買賣前請再確認一次當日報價。'),
        ]
        _kfaq_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                             + html.escape(a) + '</div></details>' for q, a in _kfaq)
        _kfaq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in _kfaq]}, ensure_ascii=False)

        _ktitle = 'iPhone 持有成本試算：一個月其實花你多少？（台灣實際二手回收行情）'
        _kdesc = ('用傑昇通信公開的二手回收報價，除以各代 iPhone 當年台灣官方售價，'
                  '算出真實殘值率，再把新機價格攤成每月成本。'
                  'Pro 與 Pro Max 用兩年，每月成本相差不到 NT$100。')

        write('iphone-cost/index.html',
          head(_ktitle, _kdesc, 'iphone-cost/',
               '<script type="application/ld+json">' + _kfaq_ld + '</script>')
          + crumbs([('首頁', '/'), ('iPhone 持有成本試算', None)]) + topnav()
          + '<h1>iPhone 一個月其實花你多少？</h1>'
          + '<p class="lede">手機不是消耗品，買價不等於花掉的錢——'
            '真正的成本是<b>買價減掉你之後賣掉的價錢</b>。'
            '這頁不假設殘值，而是直接拿收購商今天的公開報價，'
            '除以那支機器當年的官方售價，算出各代 iPhone <b>實際</b>掉了多少，'
            '再用這條曲線把新機攤成每月成本。</p>'
          + f'<p class="upd">回收價來源：{_SRC}（查詢於 {RS["updated"]}）'
            f'　·　當年售價：{html.escape(RS["list_src"])}'
            f'　·　共 {len(RS["rows"])} 款機型、{sum(len(r["caps"]) for r in RS["rows"])} 個容量組合</p>'
          + '<h2>今天的答案</h2>' + _hl
          + '<h3>細節</h3><div class="tldr"><ul>'
          + '<li><b>掉價最快的不是最便宜的機型，是 iPhone Air。</b>'
            f'上市滿一年殘值只剩 {rate_of("Air", 1) * 100:.0f}%，'
            f'同期的 Pro Max 還有 {rate_of("Pro Max", 1) * 100:.0f}%。</li>'
          + '<li><b>容量升級是折舊最快的一筆錢。</b>整機兩年後還有五成上下，'
            '但多付的容量費用通常只剩三成。</li>'
          + f'<li><b>舊機今年反而漲價。</b>{HK.get("date", "").replace("-", "/")} Apple 調高在售舊機售價，'
            f'最多一款漲 {money(max((w - o) for _, o, w in HK.get("items", [(0, 0, 0)])))}，'
            '「等一等比較便宜」今年不成立。</li>'
          + '<li><b>為了台日價差專程飛一趟，攤下來是虧的。</b>'
            '價差攤到每月只有幾十到一百多元，機票攤下來比它多。</li>'
          + '</ul></div>'
          + '<h2>各代 iPhone 實際掉了多少</h2>'
          + '<p class="lede">同一天查到的回收報價，對照各機種當年的官方售價。'
            '每一列都是實際發生過的折舊，不是推估。</p>'
          + '<div class="tw"><table><thead><tr><th>機型</th><th>上市</th><th>已滿</th>'
            '<th>當年售價</th><th>今日回收價</th><th>殘值率</th><th>掉了</th>'
            '</tr></thead><tbody>' + _drows2 + '</tbody></table></div>'
          + f'<p class="disc">{html.escape(RS["src_note"])}'
            f'　回收價來源：{_SRC}，查詢於 {RS["updated"]}。'
            '每個世代取同一個參考容量（優先 256GB）以利對照，'
            '其他容量的殘值率見下方「升級容量」一節。</p>'
          + '<h2>殘值率速查</h2>'
          + '<p class="lede">把上表依等級與年數整理。可以清楚看到兩件事：'
            '等級越高掉價越慢，而且第一年掉最多。</p>'
          + '<div class="tw"><table><thead><tr><th>等級</th>'
            + ''.join(f'<th>滿 {y} 年</th>' for y in _YRS)
            + '</tr></thead><tbody>' + _mrows + '</tbody></table></div>'
          + '<p class="disc">每格都取該世代的參考容量（優先 256GB，該世代沒有 256GB 時取 128GB），'
            '避免不同年份落在不同容量上而失去可比性。'
            '「—」表示目前沒有滿該年數的同級機種可以對照，'
            '例如 iPhone Air 2025 年才推出，還沒有滿兩年的實際行情。</p>'
          + '<h2>升級容量，是最不保值的一筆</h2>'
          + '<p class="lede">同一支機器，從最小容量升到最大容量要多付一筆錢；'
            '幾年後回收時，這筆錢還剩多少？除了才剛滿一年的 iPhone 17 之外，'
            '答案都比整機的殘值率低，而且放越久差距越大。</p>'
          + '<div class="tw"><table><thead><tr><th>機型</th><th>已滿</th>'
            '<th>當年多付</th><th>回收多拿</th><th>加價殘值率</th><th>整機殘值率</th>'
            '</tr></thead><tbody>' + _crows + '</tbody></table></div>'
          + '<h2>在售新機的每月成本</h2>'
          + '<p class="lede">用上面的實際殘值率，把目前在架上的 iPhone 攤成每月成本。'
            '數字是「買價減掉估計回收價，再除以月數」。同一機型的各容量套用同一個殘值率，'
            '但由上一節可知大容量實際上掉得更兇，所以大容量那幾列是偏樂觀的估計。</p>'
          + '<div class="tw"><table><thead><tr><th>機型</th><th>台灣售價</th>'
            + ''.join(f'<th>用 {y} 年</th>' for y in _YRS)
            + '</tr></thead><tbody>' + _nrows + '</tbody></table></div>'
          + ('<p class="disc">'
             + '、'.join(html.escape(n) for n in _nodata)
             + ' 是全新形態的機種，市場上沒有可比的回收行情，無法推估殘值，故不列出數字。</p>'
             if _nodata else '')
          + _kcalc
          + _hike_blk
          + _jp_blk
          + '<h2>常見問題</h2>' + _kfaq_html
          + '<div class="cities">'
          + f'<a class="ct" href="{U("/apple-japan-price/")}"><b>🍎 台日 Apple 價差</b>'
            f'<s>每日更新的台日售價全表</s></a>'
          + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 旅日信用卡</b>'
            f'<s>海外回饋可能比價差還大</s></a>'
          + f'<a class="ct" href="{U("/deals/")}"><b>🔥 機票特價</b><s>每日更新</s></a></div>'
          + '<p class="disc">本頁的每月成本只計機身，不含 AppleCare+、配件、電信資費。'
            '殘值率取自收購商公開報價，會隨市場調整；估計回收價假設機況良好、配件齊全，'
            '實際以驗機結果為準。所有數字僅供比較用，不構成購買建議。'
            '頁內部分連結為聯盟行銷連結，本站可能獲得分潤，不影響你的價格。</p>'
          + foot())
        pages.append(('/iphone-cost/', 0.8))

    # ── 買 iPhone 刷哪張卡：三個沒人講清楚的地方 ──────────────
    # 攻略都在比回饋率，但真正讓人拿不到回饋的是「哪天扣款」與
    # 「這個通路算不算」。分期 0 利率 vs 回饋也沒人算過。
    _ICP = [p for p in AP['products'] if p['cat'] == 'iPhone']
    if _ICP:
        _SRC_PAY = ('<a href="https://www.apple.com/tw/shop/help/payments" rel="nofollow" '
                    'target="_blank">Apple 台灣購物協助・付款與安全性</a>')
        _SRC_CUBE = ('<a href="https://www.cathaybk.com.tw/cathaybk/promo/event/credit-card/'
                     'product/CUBE_rights/index.html" rel="nofollow" target="_blank">'
                     '國泰世華 CUBE 卡權益分級</a>')

        def _even(c, n):
            """分期 0 利率要打平 c% 回饋，手上的錢得有多少年化報酬"""
            return 24 * c / (n + 1)

        # 示範用主流機種：優先 Pro 256GB，和持有成本頁的標題機種一致
        _demo = (next((p for p in _ICP if p.get('new') and p['spec'] == '256GB'
                       and p['name'].endswith('Pro')), None)
                 or next((p for p in _ICP if p.get('new') and p['spec'] == '256GB'), _ICP[0]))
        _DEMO_C, _DEMO_R = 3.3, 1.6          # 示範用的回饋率與無風險利率
        _terms = (3, 6, 12, 24)
        _erows = ''.join(
            f'<tr><td><b>{n} 期</b></td>'
            f'<td>{money(round(_demo["twd"] * _DEMO_R / 100 * (n + 1) / 24))}</td>'
            f'<td>{money(round(_demo["twd"] * _DEMO_C / 100))}</td>'
            f'<td class="win">{_even(_DEMO_C, n):.1f}%</td></tr>' for n in _terms)

        # 預設選在上表示範的那支，免得表格與計算機的機型對不起來
        _iopts = ''.join(
            f'<option value="{p["twd"]}"'
            f'{" selected" if p is _demo else ""}>{html.escape(p["name"])} '
            f'{html.escape(p["spec"])}（{money(p["twd"])}）</option>' for p in _ICP)
        _ijs = ("""
<script>
(function(){
 var $=function(i){return document.getElementById(i)};
 function nt(n){return 'NT$'+Math.round(n).toLocaleString('en-US')}
 function calc(){
  var p=+$('im').value, n=+$('in').value;
  var c=(+$('ic').value||0)/100, r=(+$('ir').value||0)/100;
  var inst=p*r*(n+1)/24;          // 分期期間留在手上的錢能生的利息
  var back=p*c;
  $('o1').textContent=nt(back);
  $('o2').textContent=nt(inst);
  $('o3').textContent=(24*c/(n+1)*100).toFixed(2)+'%';
  var d=back-inst, e=$('ov');
  e.className='cv '+(d>0?'tw':'jp');
  e.textContent = Math.abs(d)<50 ? '兩邊差不多，看你比較需要現金還是回饋'
   : (d>0 ? ('一次付清拿回饋多 '+nt(d)+'——除非你本來就缺現金')
          : ('分期 0 利率多 '+nt(-d)+'——你的資金報酬率夠高，分期划算'));
 }
 ['im','in','ic','ir'].forEach(function(i){
   var el=$(i); if(el){el.addEventListener('input',calc);el.addEventListener('change',calc);}
 });
 calc();
})();
</script>""")

        _icalc = (
          '<h2>分期 0 利率和回饋，哪個划算？</h2>'
          '<p class="lede">多數卡是二選一，但沒人告訴你該選哪個。其實算得出來——'
          '<b>0 利率分期的價值，就是你留在手上那筆錢能生的利息</b>。'
          '等額攤還 N 期時，平均未償餘額約為本金的 (N+1)／2N，'
          f'所以分期的價值 ≈ 本金 × 年化報酬率 × (N+1) ÷ 24。</p>'
          f'<p class="lede">以 {html.escape(_demo["name"])} {html.escape(_demo["spec"])}'
          f'（{money(_demo["twd"])}）、回饋 {_DEMO_C}%、資金年化報酬 {_DEMO_R}% 為例：</p>'
          '<div class="tw"><table><thead><tr><th>期數</th><th>分期 0 利率的價值</th>'
          f'<th>{_DEMO_C}% 回饋</th><th>要多少報酬率才打平</th>'
          '</tr></thead><tbody>' + _erows + '</tbody></table></div>'
          '<p class="disc">「要多少報酬率才打平」＝ 24 × 回饋率 ÷ (期數＋1)。'
          '台灣一年期定存目前約 1.5% 上下，要穩定拿到表中那個數字並不容易。</p>'
          '<div class="calc"><div class="sf">'
          f'<label>機型<select id="im">{_iopts}</select></label>'
          '<label>期數<select id="in">'
          + ''.join(f'<option value="{n}"{" selected" if n == 24 else ""}>{n} 期</option>'
                    for n in _terms) +
          '</select></label>'
          f'<label>一次付清的回饋 %<input id="ic" type="number" value="{_DEMO_C}" '
          'min="0" max="30" step="0.1"></label>'
          f'<label>你的資金年報酬 %<input id="ir" type="number" value="{_DEMO_R}" '
          'min="0" max="20" step="0.1"></label>'
          '</div><div class="cres">'
          '<div class="cl"><span>一次付清，拿到回饋</span><b id="o1">—</b></div>'
          '<div class="cl"><span>分期 0 利率的價值</span><b id="o2">—</b></div>'
          '<div class="cl"><span>打平所需年報酬率</span><b id="o3">—</b></div>'
          '<div class="cv" id="ov">—</div></div></div>'
          '<p class="disc">未計入分期手續費（0 利率通常免收，但部分通路會加收）、'
          '提前清償限制，以及分期期間額度被占用的機會成本。'
          '若你打算把那筆錢拿去投資，報酬率請填你有把握的數字，不是期望值。</p>'
          + _ijs)

        _ifaq = [
         ('在 Apple 官網下單，什麼時候扣款？',
          'Apple 台灣的購物說明寫明：確認訂單時只取得「預先授權」，'
          '「當您的訂貨交付運送人時，Apple Store 得向信用卡公司請求帳款」。'
          '也就是出貨才真正請款。很多人下單後只看到一筆 1 元的授權，那是在驗證卡片可用，'
          '不是實際消費。'),
         ('我下單當天切了權益，為什麼沒拿到加碼？',
          '因為回饋是依請款日認列，而 Apple 官網是出貨才請款。'
          '像台新、國泰這類「當日切換權益」的卡，必須在<b>扣款當天</b>處於正確方案，'
          '下單那天切了沒有用。收到刷卡通知才是關鍵時點。'),
         ('活動 9 月底到期，但我的機器 10 月才出貨，還算數嗎？',
          '通常不算。回饋活動多以請款日判定，出貨日落在活動期間之外就吃不到。'
          '這次 iPhone Duo 要到 10 月中才開放預購，出貨可能更晚，'
          '打算靠短期活動衝回饋的人要特別注意。'),
         ('國泰世華 CUBE 卡在 Apple 官網有 3.3% 嗎？',
          '沒有。CUBE 卡「玩數位」方案的認列範圍是 Apple 媒體服務'
          '（App Store、Apple Music、iCloud、Apple TV+、Apple Arcade、Apple One、iTunes 等），'
          '國泰官方權益說明明確寫「不含 Apple Store 之交易」。'
          '在 Apple 官網或直營店買機器不屬於這個通路。'),
         ('分期 0 利率和刷卡回饋可以同時拿嗎？',
          '多數卡不行，要二選一，少數卡分期仍給部分回饋。'
          '要判斷哪個划算，可以用本頁的試算：0 利率分期的價值就是你留在手上那筆錢的利息，'
          '把它跟一次付清的回饋比大小即可。以 24 期、3.3% 回饋來說，'
          '你的資金要有超過 3% 的年化報酬，分期才划算。'),
         ('為什麼這頁不直接排名哪張卡最好？',
          '因為那需要一份逐張查證的國內回饋資料，而各行的活動期間短、條件變動快，'
          '排出來的名次很快就過期。本站寧可先把三個會讓你「照著做卻拿不到」的機制講清楚——'
          '這些不會隨檔期改變。日本消費的部分，本站另有逐張查證的旅日信用卡比較。'),
        ]
        _ifaq_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                             + a.replace('<b>', '<b>').replace('</b>', '</b>')
                             + '</div></details>' for q, a in _ifaq)
        _ifaq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}
            for q, a in _ifaq]}, ensure_ascii=False)

        _ititle = '買 iPhone 刷哪張卡？三個讓你拿不到回饋的機制（Apple 官網扣款日、通路認定、分期）'
        _idesc = ('Apple 官網是出貨才請款，切換型權益要在扣款日才有效；CUBE 卡「玩數位」'
                  '官方載明不含 Apple Store。另附分期 0 利率與回饋的打平試算。')

        write('iphone-card/index.html',
          head(_ititle, _idesc, 'iphone-card/',
               '<script type="application/ld+json">' + _ifaq_ld + '</script>')
          + crumbs([('首頁', '/'), ('買 iPhone 刷哪張卡', None)]) + topnav()
          + '<h1>買 iPhone 刷哪張卡？</h1>'
          + '<p class="lede">網路上的攻略都在比回饋率。但真正讓人「照著做卻拿不到」的，'
            '不是選錯卡，是<b>三個沒人講清楚的機制</b>——哪天扣款、這個通路算不算、'
            '分期跟回饋該選哪個。</p>'
          + '<div class="today">'
            '<div class="tday">資料查證於 ' + NOW.date().isoformat() + '　·　附官方條款出處</div>'
            '<div class="tans">Apple 官網是<b>出貨才請款</b>，'
            '所以「當日切換權益」的卡要在扣款那天切對，不是下單那天</div>'
            '<div class="tsub">下單時你只會看到一筆小額預先授權（常見 1 元），'
            '那是在驗證卡片，不是消費。回饋依請款日認列。</div>'
            '<div class="tbuf">連帶的後果：<b>9 月底到期的活動，10 月才出貨就吃不到</b>。'
            'iPhone Duo 要到 10 月中才開放預購。</div></div>'
          + '<h3>三個機制</h3><div class="tldr"><ul>'
            '<li><b>扣款日 ≠ 下單日。</b>Apple 確認訂單時只做預先授權，'
            '出貨交付運送人時才請款。切換型權益、短期活動都以請款日為準。</li>'
            '<li><b>Apple Store 不算「數位」通路。</b>國泰 CUBE 卡「玩數位」的認列範圍是'
            ' Apple 媒體服務，官方明載不含 Apple Store 的交易。看到「官網有 3.3%」要先確認。</li>'
            '<li><b>分期 0 利率通常比不上回饋。</b>24 期、3.3% 回饋的情況下，'
            '你的資金要有超過 3% 的年化報酬，分期才划算。</li>'
            '</ul></div>'
          + '<h2>1. 扣款日不是下單日</h2>'
          + f'<p class="lede">{_SRC_PAY}寫明：確認訂單時 Apple Store 只取得'
            '該筆金額的<b>預先授權</b>，「當您的訂貨交付運送人時，Apple Store 得向信用卡公司'
            '請求帳款」。實體商品出貨才請款。</p>'
          + '<div class="tw"><table><thead><tr><th>時點</th><th>發生什麼</th>'
            '<th>對回饋的影響</th></tr></thead><tbody>'
            '<tr><td><b>下單／預購</b></td><td>取得預先授權，常見是一筆 1 元</td>'
            '<td>不是消費，不認列回饋</td></tr>'
            '<tr><td><b>出貨</b></td><td>正式請款，金額入帳</td>'
            '<td class="lose">以這天判定權益方案與活動期間</td></tr>'
            '<tr><td><b>結帳日</b></td><td>列入當期帳單</td>'
            '<td>回饋依發卡行週期入帳</td></tr>'
            '</tbody></table></div>'
          + '<div class="tldr"><ul>'
            '<li><b>「當日切換」的卡最危險。</b>台新、國泰這類要在 App 切換權益方案的卡，'
            '必須在收到刷卡通知（＝請款）那天處於正確方案。下單日切了、出貨前切回去，等於白做。</li>'
            '<li><b>短期活動要看得到出貨日再說。</b>活動寫「9/30 前」，'
            '指的通常是請款日落在期間內。</li>'
            '<li><b>預購熱門機種尤其容易踩到。</b>出貨往往排到下個月，跨過活動結束日。</li>'
            '</ul></div>'
          + '<h2>2. Apple Store 不算「數位」通路</h2>'
          + f'<p class="lede">以國泰世華 CUBE 卡為例，「玩數位」方案的認列範圍寫得很細：'
            'App Store、Apple Music、iCloud、Apple TV+、Apple Arcade、Apple One、iTunes 等'
            'Apple 媒體服務的訂閱與購買，<b>「不含 Apple Store 之交易」</b>。'
            f'（{_SRC_CUBE}）</p>'
          + '<p class="lede">也就是說，在 Apple 官網或直營店買一支手機，'
            '不會被歸到這個方案。看到攻略寫「官網刷某卡有 3.3%」，'
            '先去該行的權益說明確認 Apple Store 在不在認列範圍內——'
            '這種細節通常寫在條款的括號裡。</p>'
          + _icalc
          + '<h2>那到底該刷哪張？</h2>'
          + '<p class="lede">本站不排名「哪張卡最好」，原因很實際：那需要一份逐張查證的'
            '國內回饋資料，而各行活動期間短、條件變動快，排出來的名次很快就過期。'
            '與其給你一個會過期的名次，不如給你三個不會變的判斷原則：</p>'
          + '<div class="tldr"><ul>'
            '<li><b>先確認你的卡在「Apple Store」這個通路有沒有加碼</b>，'
            '不是看它在「網購」或「數位」有多少。</li>'
            '<li><b>再確認出貨日落在活動期間內</b>，以及那天你的權益方案是對的。</li>'
            '<li><b>最後才比回饋率。</b>前兩關沒過，回饋率再高都是 0。</li>'
            '</ul></div>'
          + '<h2>常見問題</h2>' + _ifaq_html
          + '<h2>順便看看</h2><div class="cities">'
          + f'<a class="ct" href="{U("/iphone-cost/")}"><b>📉 iPhone 持有成本</b>'
            f'<s>用實際回收行情算每月多少</s></a>'
          + f'<a class="ct" href="{U("/apple-japan-price/")}"><b>🍎 台日 Apple 價差</b>'
            f'<s>日本買划算嗎，每日更新</s></a>'
          + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 旅日信用卡</b>'
            f'<s>逐張查證的日本消費回饋</s></a></div>'
          + '<p class="disc">本頁為公開資訊整理，非理財或投資建議。'
            '各發卡行的權益方案、指定通路與活動期間隨時可能調整，'
            '刷卡前請以發卡行與 Apple 官方公告為準。'
            '試算僅供比較用，未計入分期手續費、提前清償限制與額度占用的機會成本。</p>'
          + foot())
        pages.append(('/iphone-card/', 0.8))

    # ── 2026/11/1 日本免稅改制（リファンド方式） ──────────────
    TF_D = datetime.date(2026, 11, 1)
    _left = (TF_D - NOW.date()).days
    _cd = (f'還有 <b>{_left}</b> 天' if _left > 0 else
           '<b>已經上路</b>' if _left == 0 else f'已實施 <b>{-_left}</b> 天')

    def _tax(pre): return round(pre * 0.1)

    _lv = [5000, 30000, 100000, 300000]
    _rows = ''.join(f'<tr><td>¥{v:,}</td><td>¥{_tax(v):,}</td>'
                    f'<td><b>{money(round(_tax(v)*RATE))}</b></td></tr>' for v in _lv)
    _duo = next((p for p in AP['products'] if p['name'] == 'iPhone Duo' and p['spec'] == '2TB'), None)
    if _duo:
        _pre = round(_duo['jpy'] / TAXR)
        _rows += (f'<tr><td>¥{_pre:,}{SMALL}iPhone Duo 2TB</small></td>'
                  f'<td>¥{_tax(_pre):,}</td>'
                  f'<td><b>{money(round(_tax(_pre)*RATE))}</b></td></tr>')

    tf_faq = [
     ('日本要取消免稅了嗎？',
      '不是。免稅本身繼續存在，改的是拿到退稅的時間點。2026 年 11 月 1 日起改採「退款方式」'
      '（リファンド方式）：購買當下先支付含稅全額，出境時經海關確認商品確實帶出日本後，'
      '再由店家退還消費稅相當額。省下的錢一樣是 10%，只是變成事後拿到。'),
     ('11 月之後買東西要先多付多少？',
      f'先多付商品稅前金額的 10%。以目前匯率 {RATE} 換算，消費 10 萬日圓要先墊 ¥10,000'
      f'（約 {money(round(10000*RATE))}）；買一支 iPhone Duo 2TB 則要先墊約 '
      f'{money(round(_tax(round(_duo["jpy"]/TAXR))*RATE)) if _duo else "NT$1 萬以上"}。'
      '這筆錢在出境並完成海關確認後才會退還，等於旅途中要多帶一筆週轉金。'),
     ('退款什麼時候、用什麼方式拿到？',
      '出境時經海關確認後，由店家或其委託的退稅服務商退還，不需要再回到原店。'
      '退款方式依店家與服務商而定——退稅系統業者列出的可指定方式包含信用卡、'
      'QR 行動支付、銀行帳戶與現金，官方並未統一規定只能用哪一種。'
      '實際到帳時間同樣依業者而異。若你在意刷卡回饋被回沖，退回信用卡以外的方式比較單純。'),
     ('有期限嗎？',
      '有，而且很容易忽略。購買日起 90 天內必須完成出境海關確認，逾期就不算免稅、拿不到退款。'
      '例如 11 月 1 日購買，確認期限是隔年 1 月 30 日。短期旅遊通常不受影響，'
      '但如果你買完之後還要在日本待很久，或把東西先寄放，要特別注意。'),
     ('哪些東西可以免稅？門檻有變嗎？',
      '依業者與公會說明，新制取消「一般物品」與「消耗品」的區分，消耗品的專用包裝也不再需要，'
      '購買上限 50 萬日圓廢止，稅前 5,000 日圓以上即為免稅對象，不再分類別計算。'
      '此部分細則以國稅廳與觀光廳公告為準。'),
     ('買了之後不小心用掉或沒帶出境會怎樣？',
      '整筆交易都拿不到退款。官方說明採每筆購買紀錄判定——同一筆交易中只要有一項商品'
      '未通過海關確認，該筆交易就失去免稅資格，不是只扣掉那一項。'
      '另外「別送」（把商品寄回國）制度已於 2025 年 3 月 31 日廢止，商品必須自己帶出境。'),
     ('10 月底之前買還是舊制嗎？',
      f'是。10 月 31 日之前購買仍適用現行的購買時免稅，結帳當下就是免稅價。'
      f'制度以購買日為準，{_cd.replace("<b>","").replace("</b>","")}。'),
    ]
    tf_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                      + html.escape(a) + '</div></details>' for q, a in tf_faq)
    tf_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in tf_faq]}, ensure_ascii=False)

    tf_title = '2026/11/1 日本免稅新制：先付全額、出境後才退稅（懶人包）'
    tf_desc = ('日本免稅 2026 年 11 月 1 日改採退款方式：購買時先付含稅全額，出境經海關確認後'
               '才退還消費稅。整理新舊制對照、要先墊多少錢、90 天確認期限與常見問題。')

    _NCARD = (len(json.load(open('cards.json', encoding='utf-8'))['cards'])
              if os.path.exists('cards.json') else 0)
    write('japan-tax-free-2026/index.html',
      head(tf_title, tf_desc, 'japan-tax-free-2026/',
           '<script type="application/ld+json">' + tf_ld + '</script>')
      + crumbs([('首頁', '/'), ('日本免稅新制', None)]) + topnav()
      + '<h1>2026/11/1 起，日本免稅改成「出境後才退錢」</h1>'
      + '<p class="lede">很多人看到消息以為日本要取消免稅。不是——免稅還在，'
        '改的是你什麼時候拿到那 10%。</p>'
      + f'<div class="today"><div class="tday">距離 11/1 上路 {_cd}'
        f'　·　換算匯率 {RATE}，每日自動更新</div>'
        f'<div class="tans">購買當下先付含稅全額，出境經海關確認後，由店家退還消費稅</div>'
        f'<div class="tsub">省下的比例一樣是 10%，但付款當下要多掏這筆錢，'
        f'等出境並完成確認才拿得回來。對行李重、消費高的旅客，影響的是現金流。</div>'
        f'<div class="tbuf">最容易忽略的一條：<b>購買日起 90 天內</b>必須完成出境海關確認，'
        f'逾期就不算免稅。</div></div>'
      + '<h2>新舊制對照</h2>'
      + '<div class="tw"><table><thead><tr><th>　</th>'
        '<th>10/31 前（現行）</th><th>11/1 起（新制）</th></tr></thead><tbody>'
        '<tr><td><b>結帳金額</b></td><td>直接扣掉 10%，當場就是免稅價</td>'
        '<td class="lose">先付含稅全額</td></tr>'
        '<tr><td><b>拿到退稅</b></td><td>結帳當下</td>'
        '<td class="lose">出境經海關確認後，由店家退還</td></tr>'
        '<tr><td><b>領取方式</b></td><td>不適用</td>'
        '<td>依店家與退稅服務商而定：信用卡、行動支付、銀行帳戶或現金</td></tr>'
        '<tr><td><b>期限</b></td><td>無</td>'
        '<td class="lose">購買日起 90 天內須完成海關確認</td></tr>'
        '<tr><td><b>物品分類</b></td><td>分一般物品與消耗品，消耗品須專用包裝</td>'
        '<td class="win">取消區分，不需專用包裝</td></tr>'
        '<tr><td><b>金額門檻</b></td><td>稅前 5,000 日圓以上，消耗品上限 50 萬日圓</td>'
        '<td class="win">稅前 5,000 日圓以上，上限廢止</td></tr>'
        '</tbody></table></div>'
      + '<h2>要先墊多少錢？</h2>'
      + '<p class="lede">先墊的是商品稅前金額的 10%。以目前匯率 '
        f'{RATE} 換算：</p>'
      + '<div class="tw"><table><thead><tr><th>購物金額（稅前）</th>'
        '<th>先墊的消費稅</th><th>約合台幣</th></tr></thead><tbody>'
        + _rows + '</tbody></table></div>'
      + '<p class="disc">刷卡另有約 1.5% 國外交易手續費；退款金額依店家與退款服務商可能再扣手續費，'
        '實際入帳以店家說明為準。</p>'
      + fare_cta('tokyo', '趕在改制前去？先看機票多少', before='2026-11-01')
      + '<h2>什麼時候去，適用哪個制度？</h2>'
      + '<p class="lede">制度以<b>購買日</b>為準，不是出境日。10 月 31 日當天買仍是舊制，'
        '11 月 1 日起買就是新制。如果你的行程橫跨兩邊，大筆採購排在 10 月底結帳，'
        '結帳當下就能拿到免稅價，不必墊錢也不用擔心 90 天期限。</p>'
      + fare_cta('osaka', '大阪也有便宜票', '')
      + search_form('查你自己的日期',
                    '上面是近期最低紀錄，選好日期可查目前實際可訂的價格。', 'TPE', 'TYO')
      + '<h2>三個容易踩到的地雷</h2>'
      + '<div class="tldr"><ul>'
        '<li><b>整筆交易連坐。</b>官方說明採每筆購買紀錄判定，'
        '同一筆交易只要有一項商品沒通過海關確認，整筆都失去免稅資格，不是只扣掉那一項。</li>'
        '<li><b>商品必須自己帶出境。</b>「別送」（把免稅品寄回國）制度已於 2025/3/31 廢止，'
        '只能購買自己帶得走的數量。</li>'
        '<li><b>90 天期限。</b>購買日起 90 天內要完成出境海關確認。'
        '短期旅遊不受影響，但長住、留學或先寄放行李的情況要留意。</li>'
        '</ul></div>'
      + '<h2>常見問題</h2>' + tf_html
      + cta('esim', '日本', '東京', '出發前先把上網搞定',
            '到 Klook 買 eSIM 或網卡，落地就能開導航找免稅店')
      + '<h2>順便看看</h2><div class="cities">'
      + f'<a class="ct" href="{U("/apple-japan-price/")}"><b>🍎 日本買 iPhone 划算嗎</b>'
        f'<s>台日價格全表，每日更新匯率</s></a>'
      + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 新制之後回饋會變多嗎</b>'
        f'<s>刷含稅價，{_NCARD} 張卡的實際差額</s></a>'
      + f'<a class="ct" href="{U("/deals/")}"><b>🔥 機票特價</b><s>台灣飛日本，每日更新</s></a>'
      + f'<a class="ct" href="{U("/tokyo/")}"><b>東京機票</b><s>各出發地比價</s></a></div>'
      + '<p class="disc">本頁依日本觀光廳「消費稅免稅店」網站、全國免稅店協會「リファンド方式」'
        '特設網站及免稅系統業者公開說明整理。制度細則以日本國稅廳與觀光廳公告為準，'
        '各店家實際作業方式可能不同，請於現場確認。'
        '頁內部分連結為聯盟行銷連結，本站可能獲得分潤，不影響你的價格。</p>'
      + foot())
    pages.append(('/japan-tax-free-2026/', 0.9))

# ---------- 早去晚回 ----------
_GT = [x for x in deals if good_times(x)]
if _GT:
    def _arr(x):
        a = arr_min(x)
        return None if a is None else f'{a//60:02d}:{a%60:02d}'

    _rtall = [x for x in deals if x.get('rt') and x.get('dept') and x.get('rett')]
    _red = [x for x in _rtall if (_hh(x['dept']) or 99) < 5]
    _gt_sorted = sorted(_GT, key=lambda x: x['price'])

    # 各城市：最便宜 vs 早去晚回最便宜
    _cmp = ''
    _skip = []
    for slug, name, codes, reg, hc in CITIES:
        fs = by_city.get(slug) or []
        g = [x for x in fs if good_times(x)]
        if not g: continue
        cheap = best([x for x in fs if x['rt']], True)
        bg = min(g, key=lambda x: x['price'])
        if not cheap: continue
        diff = bg['price'] - cheap['price']
        # 價差超過一倍的多半是唯一一筆高價紀錄，列出來只會讓對照失真
        if bg['price'] > cheap['price'] * 2:
            _skip.append(name); continue
        _cmp += (f'<tr><td><a href="{U("/"+slug+"/")}"><b>{name}</b></a></td>'
                 f'<td>{money(cheap["price"])}{SMALL}去 {cheap["dept"]}　回 {cheap["rett"]}</small></td>'
                 f'<td class="win"><b>{money(bg["price"])}</b>{SMALL}去 {bg["dept"]}　回 {bg["rett"]}</small></td>'
                 f'<td>{"＋"+money(diff) if diff > 0 else "同價或更低"}</td></tr>')

    _rows = ''
    for x in _gt_sorted[:24]:
        cn = CITY_OF[x['d']][1]
        a = _arr(x)
        _rows += (f'<tr><td><a href="{U("/"+CITY_OF[x["d"]][0]+"/")}">{ORI.get(x["o"],x["o"])}→{cn}</a>'
                  f'{SMALL}{html.escape(x["airname"])}・'
                  f'{"直飛" if x["tr"]==0 else f"轉機{x[chr(39)+chr(39)]}" if False else ("直飛" if x["tr"]==0 else "轉機"+str(x["tr"]))}</small></td>'
                  f'<td><b>{money(x["price"])}</b></td>'
                  f'<td>{x["dep"]}{SMALL}{x["dept"]} 起飛'
                  + (f"，約 {a} 抵達" if a else '') + '</small></td>'
                  f'<td>{x["ret"]}{SMALL}{x["rett"]} 起飛</small></td>'
                  f'<td><a class="btn" href="{html.escape(flight_url(x))}" target="_blank" '
                  f'rel="nofollow noopener sponsored">查這天</a></td></tr>')

    gt_faq = [
     ('為什麼便宜的機票時間都很差？',
      '因為航空公司把最不想飛的時段拿來降價。熱門時段（早上出發、傍晚回程）需求高、不必打折；'
      '凌晨起飛與傍晚出發的班次不好賣，價格才會壓低。'
      f'本站目前 {len(_rtall)} 組有完整時間的來回票中，只有 {len(_GT)} 組符合早去晚回，'
      f'比例約 {len(_GT)/len(_rtall)*100:.0f}%。'),
     ('凌晨出發的紅眼班機不是更早到嗎？',
      '名義上更早，實際上更糟。凌晨 02:30 起飛的班次 06:35 就抵達，看起來很理想，'
      '但那代表你半夜就要到機場、前一晚幾乎沒睡，抵達當天多半在補眠；'
      '而且那個時間沒有機場捷運與國道客運，前往機場的交通得自行處理。'
      f'本站目前有 {len(_red)} 組是凌晨 00–05 出發，本頁一律排除。'),
     ('「早去晚回」的定義是什麼？',
      '三個條件同時成立：去程當日中午前抵達日本、出發不早於 05:00、'
      '回程由日本 18:00 至 23:00 起飛。關鍵是抵達時間而非出發時間——'
      '早上 10:40 起飛但經第三地轉機、下午 16:35 才落地的班次，'
      '第一天同樣用不到，本頁不列入。'),
     ('多付的錢值得嗎？',
      '看你的假期長度。三天兩夜的行程，多出兩個半天等於多了三分之一的時間，'
      '通常比省下一兩千元更划算；十天以上的行程，比例就低很多，'
      '這時候把預算放在住宿或交通票券上可能更有效。'),
    ]
    gt_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                      + html.escape(a) + '</div></details>' for q, a in gt_faq)
    gt_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in gt_faq]}, ensure_ascii=False)

    _lo = _gt_sorted[0]
    write('japan-flight-good-times/index.html',
      head(f'早去晚回的日本機票｜不浪費假期的班次，目前 {len(_GT)} 組',
           f'便宜機票的時段通常很差。本頁只收去程台灣 06–10 點起飛、'
           f'回程日本 18–23 點起飛的來回票，目前 {len(_GT)} 組，'
           f'最低 {money(_lo["price"])}。含與最便宜班次的價差對照，每日更新。',
           'japan-flight-good-times/',
           '<script type="application/ld+json">' + gt_ld + '</script>')
      + crumbs([('首頁', '/'), ('早去晚回', None)]) + topnav()
      + '<h1>不浪費假期的日本機票</h1>'
      + '<p class="lede">最便宜的票，時段幾乎都很差。這頁只留下'
        '<b>去程早上出發、回程晚上才走</b>的班次。</p>'
      + f'<div class="today"><div class="tday">{NOWS} 更新　·　'
        f'共 {len(_rtall)} 組來回票，符合條件的只有 {len(_GT)} 組</div>'
        f'<div class="tans">符合早去晚回的只佔 {len(_GT)/len(_rtall)*100:.0f}%，'
        f'目前最低 {money(_lo["price"])}</div>'
        f'<div class="tsub">定義：去程<b>當日中午前抵達日本</b>、出發不早於 05:00，'
        f'回程由日本 18:00–23:00 起飛。決定第一天能不能用的是抵達時間——'
        f'06:00 出發但轉機到下午才落地，第一天照樣報廢。</div>'
        + (f'<div class="tbuf">另有 <b>{len(_red)}</b> 組是 05:00 前起飛的紅眼班機——'
           f'02:30 起飛雖然 06:35 就到，但那一天多半在補眠，本頁一律排除。</div>' if _red else '')
        + '</div>'
      + (('<h2>多付多少，換到好時段？</h2>'
          '<p class="lede">同一個目的地，最便宜的班次與最便宜的早去晚回班次對照。</p>'
          '<div class="tw"><table><thead><tr><th>目的地</th><th>最便宜</th>'
          '<th>最便宜的早去晚回</th><th>價差</th></tr></thead><tbody>'
          + _cmp + '</tbody></table></div>'
          + (f'<p class="disc">{"、".join(_skip)} 的早去晚回班次價格超過最便宜班次的兩倍，'
             f'多為單筆高價紀錄，未列入對照。</p>' if _skip else '')) if _cmp else '')
      + f'<h2>目前的早去晚回班次</h2>'
      + '<p class="lede">依價格排序。時間為當地時間，抵達時間為飛行時間加時差的估算。</p>'
      + '<div class="tw"><table><thead><tr><th>航線</th><th>價格</th>'
        '<th>去程</th><th>回程</th><th>　</th></tr></thead><tbody>'
      + _rows + '</tbody></table></div>'
      + '<p class="disc">價格為單人來回含稅，取自近期快取紀錄，實際票價請點擊查詢。</p>'
      + search_form('查你自己的日期', '選好日期就能看到當天實際可訂的班次與時間。', 'TPE', 'TYO')
      + '<h2>為什麼值得多付這筆</h2><div class="tldr"><ul>'
        '<li><b>第一天不再報廢。</b>傍晚 17:15 出發的班次，落地已近午夜，'
        '第一天實際只剩下從機場到飯店。早上出發則是中午前就能進市區。</li>'
        '<li><b>最後一天能玩到傍晚。</b>回程 21:00 以後起飛，當天還有完整的白天，'
        '中午前退房寄放行李即可。</li>'
        '<li><b>紅眼班機不是解方。</b>凌晨 02:00 起飛看似最早到，但前一晚幾乎無法睡，'
        '抵達後的第一天多半在補眠，而且深夜前往機場的交通也是成本。</li>'
        '</ul></div>'
      + cta('hotel', '東京', '東京', '時間抓好了，住宿呢',
            f'到 {P["hotel"]["brand"]} 查房價，繁體中文、台幣計價',
            track='good-times')
      + '<h2>常見問題</h2>' + gt_html
      + '<h2>順便看看</h2><div class="cities">'
      + f'<a class="ct" href="{U("/deals/")}"><b>🔥 機票特價</b><s>每日更新</s></a>'
      + f'<a class="ct" href="{U("/japan-coupon/")}"><b>🏷️ 購物折扣</b>'
        f'<s>折價券×免稅×刷卡回饋</s></a>'
      + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 旅日信用卡</b>'
        f'<s>哪張卡回饋最高</s></a></div>'
      + foot())
    pages.append(('/japan-flight-good-times/', 0.9))
    print(f'   早去晚回頁：{len(_GT)} 組（來回票 {len(_rtall)} 組，紅眼 {len(_red)} 組）')

# ---------- 旅日信用卡 ----------
if os.path.exists('cards.json'):
    CD = json.load(open('cards.json', encoding='utf-8'))
    _fx = CD['fx_fee']
    _ap = json.load(open('apple.json', encoding='utf-8')) if os.path.exists('apple.json') else {}
    _MIDC = (_ap.get('rate', {}).get('jpy_twd_mid')
             or _ap.get('rate', {}).get('jpy_twd') or 0.205)
    _RDATE = _ap.get('rate', {}).get('quoted_at', '')
    MODES = [('shop', '符合加碼條件的實體消費'), ('base', '一般日本消費'),
             ('transit', '交通卡儲值')]
    SCOPE_NAME = {'shop': '實體消費', 'transit': '交通卡儲值', 'any': '實體與交通卡'}

    def _bill(jpy):
        """日幣消費換算台幣帳單（含國外交易手續費）"""
        return jpy * _MIDC * (1 + _fx['typical'] / 100)

    def _tiers(c, scope):
        return [t for t in c['tiers'] if t['scope'] in (scope, 'any')]

    def _has(c, mode):
        return mode == 'base' or bool(_tiers(c, mode))

    def _back(c, jpy, mode='shop'):
        """回饋金額。base 模式只算基本回饋，其餘加上該類型的各層加碼（各自受上限）。"""
        b = _bill(jpy)
        v = c['base'] / 100 * b
        capped = False
        if mode != 'base':
            for t in _tiers(c, mode):
                x = t['rate'] / 100 * b
                if t['cap'] and x > t['cap']:
                    x = t['cap']; capped = True
                v += x
        return v, capped

    def _maxrate(c, mode):
        return c['base'] + (0 if mode == 'base' else sum(t['rate'] for t in _tiers(c, mode)))

    def _hit(c, mode):
        """加碼達上限所需的台幣帳單金額（取最先觸頂的那層）"""
        ts = [t for t in _tiers(c, mode) if t['cap']]
        return round(min(t['cap'] / (t['rate'] / 100) for t in ts)) if ts else 0

    _CJS = ('<script>window.JCARD={mid:%s,fee:%s,cards:%s};'
            'window.jfmt=function(n){return Math.round(n).toLocaleString("en-US")};'
            'window.jbill=function(y){return y*JCARD.mid*(1+JCARD.fee/100)};'
            'window.jback=function(c,y,mode){var b=jbill(y),v=c.base/100*b,cap=false;'
            'if(mode!=="base"){c.tiers.filter(function(t){return t.scope===mode||t.scope==="any";})'
            '.forEach(function(t){var x=t.rate/100*b;'
            'if(t.cap&&x>t.cap){x=t.cap;cap=true;}v+=x;});}'
            'return {v:v,cap:cap,bill:b};};'
            'window.jhas=function(c,mode){return mode==="base"||'
            'c.tiers.some(function(t){return t.scope===mode||t.scope==="any";});};</script>') % (
        _MIDC, _fx['typical'],
        json.dumps([{'n': c['name'], 's': c['slug'], 'base': c['base'],
                     'tiers': c['tiers'], 'race': c.get('reg_race', False)}
                    for c in CD['cards']], ensure_ascii=False))

    _mopts = ''.join(f'<option value="{k}">{v}</option>' for k, v in MODES)

    # ── 比較表 ──
    _crows = ''
    for c in sorted(CD['cards'], key=lambda x: -x['total']):
        hit = _hit(c, 'shop')
        tr = _maxrate(c, 'transit') if _tiers(c, 'transit') else 0
        _crows += (f'<tr><td><a href="{U("/japan-credit-card/"+c["slug"]+"/")}">'
                   f'<b>{html.escape(c["name"])}</b></a>{SMALL}{html.escape(c["plan"])}'
                   + ('　⚠ 需搶限量登錄' if c.get('reg_race') else '') + '</small></td>'
                   f'<td><b>{c["total"]}%</b>{SMALL}基本 {c["base"]}%'
                   + (f' ＋ {len(_tiers(c,"shop"))} 層加碼' if _tiers(c, 'shop') else '')
                   + '</small></td>'
                   f'<td>{(money(hit) + SMALL + "超過只剩 " + str(c["base"]) + "%</small>") if hit else "無加碼上限"}</td>'
                   f'<td>{(str(tr) + "%") if tr else "—"}</td>'
                   f'<td>{html.escape(c["period"])}</td></tr>')

    # ── 選卡介面（日幣輸入）──
    _pjs = _CJS + ("""
<script>
(function(){
 var $=function(i){return document.getElementById(i)};
 function run(){
  var y=+$('pa').value||0, mode=$('ps').value;
  var r=JCARD.cards.filter(function(c){return jhas(c,mode)})
   .map(function(c){var o=jback(c,y,mode);
     return {n:c.n,s:c.s,v:o.v,cap:o.cap,bill:o.bill,race:c.race};})
   .sort(function(a,b){return b.v-a.v});
  if(!r.length){$('pr').innerHTML='<div class="cv">這個類型目前沒有卡片有加碼</div>';return;}
  var bill=r[0].bill;
  $('pb').textContent=y?('≈ NT$'+jfmt(bill)+'（已含 '+JCARD.fee+'% 國外交易手續費）'):'';
  $('pr').innerHTML=r.map(function(x,i){
    return '<div class="cl"><span>'+(i===0?'<b class="pw">最佳</b> ':'')+
      '<a href="'+%HUB%+'/'+x.s+'/">'+x.n+'</a>'+
      (x.cap?'<i class="pc">加碼已達上限</i>':'')+
      (x.race?'<i class="pc">需搶登錄</i>':'')+'</span><b>NT$'+jfmt(x.v)+
      '<i class="pp">≈ ¥'+jfmt(x.v/JCARD.mid)+'</i></b></div>';
  }).join('')+(y?('<div class="cv jp">最佳卡實際負擔 NT$'+jfmt(bill-r[0].v)+
    '　·　有效回饋率 '+(r[0].v/bill*100).toFixed(2)+'%</div>'):'<div class="cv">請輸入金額</div>');
 }
 ['pa','ps'].forEach(function(i){var e=$(i);if(e){e.addEventListener('input',run);e.addEventListener('change',run);}});
 run();
})();
</script>""").replace('%HUB%', json.dumps(U('/japan-credit-card')))

    _picker = (
      '<h2>你要刷多少？答案不一樣</h2>'
      '<p class="lede">加碼幾乎都有上限，所以「哪張最好」取決於金額與消費類型。'
      '輸入日幣金額看實際排序：</p>'
      '<div class="calc"><div class="sf">'
      '<label>日本刷卡金額 ¥<input id="pa" type="number" value="200000" min="0" step="10000"></label>'
      f'<label>消費類型<select id="ps">{_mopts}</select></label>'
      '</div><p class="upd" id="pb"></p><div class="cres" id="pr"></div></div>'
      f'<p class="disc">以中間匯率 {_MIDC} 換算並加計 {_fx["typical"]}% 國外交易手續費；'
      f'回饋依台幣帳單金額計算。各層加碼需同時符合其條件才疊得上去，'
      f'試算採全部符合的最高情境。點數型回饋以 1 點約 1 元估算。</p>' + _pjs)

    cc_faq = [
     ('海外刷卡的手續費是多少？',
      f'多數發卡行約 {_fx["typical"]}%，由國際組織 1% 與發卡行 0.5% 組成；'
      f'金管會規定發卡行加收不得逾 0.5%。美國運通約 {_fx["amex"]}%。'
      '算實際成本時要先加上去再扣回饋。'),
     ('結帳時店員問要刷日圓還是台幣，選哪個？',
      '一定選日圓。選台幣是動態貨幣轉換（DCC），由店家端決定匯率，通常比卡片組織匯率差 3% 到 5%，'
      '而且多數銀行的海外加碼要求以外幣結帳，選台幣可能連回饋都拿不到。'),
     ('為什麼看到的最高回饋，我實際拿不到？',
      '因為那是所有加碼同時成立的數字。以聯邦吉鶴卡的 11% 為例，是基本 2.5% 加上行動支付、'
      '前月帳單滿額、指定通路、新戶四層加碼疊出來的，每層各有條件與上限，'
      '一般人不會全部同時符合。看本站每張卡頁的逐金額試算會比較準。'),
     ('限量登錄是什麼意思？',
      '部分銀行的加碼採每月限量登錄，額滿為止。聯邦吉鶴卡每月 15 日 10:00 開放、限量 10,000 名；'
      '台北富邦 J 卡的日韓泰加碼每月 20 日 16:00、交通卡加碼每月 18 日 16:00 開放。'
      '沒搶到就只有基本回饋。出國前要先確認自己這個月登錄了沒。'),
     ('回饋上限怎麼看？',
      '看「刷到多少就到頂」。加碼 6% 上限 500 元，代表台幣帳單刷到約 8,333 元加碼就滿了。'
      '買 iPhone 這種單價高的東西，加碼通常第一筆就用完，後面只剩基本回饋。'),
     ('看到「JCB MyJapan+ 日本刷滿 10 萬回 1 萬日圓」，還能參加嗎？',
      '不行，那個活動已經結束。JCB 的 MyJapan+ App 現金回饋活動登錄期間為 2026 年 7 月 1 日至 9 月 30 日，'
      '限量 88,888 名，官方活動頁目前顯示「活動已結束」。'
      '它不是一張卡，而是疊在台灣發行的 JCB 卡之上的加碼，回饋預計 2026 年 10 月下旬起由各發卡行入帳。'
      '如果你是看到別站的整理才知道這個活動，要注意那類限量活動很容易在文章更新之前就額滿。'),
     ('那買 iPhone 到底要在台灣刷還是日本刷？',
      '兩邊都有回饋，要一起算。台灣通路在新機上市期間的加碼可能更高，足以抵銷日本的免稅價差；'
      '日本則要多付國外交易手續費。本站的台日 Apple 價差頁有試算工具可以比較。'),
    ]
    cc_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                      + html.escape(a) + '</div></details>' for q, a in cc_faq)
    cc_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in cc_faq]}, ensure_ascii=False)

    # ── 行動支付：免手續費到底省多少 ──────────────────────
    # 「台灣電支在日本免 1.5% 國外交易手續費」是攻略常見說法，
    # 但電支的換匯用的是各行牌告賣出價，本身就含價差。把兩邊都
    # 換算成「相對即期中價的成本」才比得出來——省下的遠比想像中少。
    MP = CD.get('mpay') or {}
    _MP_BLOCK = ''
    if MP:
        _b = MP['bot']
        _mid = (_b['spot_buy'] + _b['spot_sell']) / 2
        _c_spot = (_b['spot_sell'] / _mid - 1) * 100
        _c_cash = (_b['cash_sell'] / _mid - 1) * 100
        _c_card = _fx['typical']                       # 卡組織匯率假設約等於中價
        _save_spot = _c_card - _c_spot
        _save_cash = _c_card - _c_cash
        _mp_rows = ''.join(
            f'<tr><td><b>{html.escape(a["name"])}</b></td>'
            f'<td>{"可綁指定信用卡" if a["card"] else "不能綁信用卡"}'
            f'{SMALL}{html.escape(a["card_note"])}</small></td>'
            f'<td>{html.escape(a["fx"])}</td>'
            f'<td>{html.escape(a["src_name"])}</td></tr>' for a in MP['apps'])
        _MP_BLOCK = (
          '<h2>在日本，該刷卡還是用台灣的行動支付？</h2>'
          '<p class="lede">台灣有幾個電子支付可以在日本的 PayPay 特約店掃碼付款，'
          f'主打<b>免 {_fx["typical"]}% 國外交易手續費</b>。但這通常不是「疊加」——'
          '多數電支在境外不收信用卡，你是在二選一。而且免掉的手續費，也沒有省下那麼多。</p>'
          '<h3>先看匯率：免手續費實際省多少</h3>'
          '<p class="lede">電支的換匯是以銀行牌告<b>賣出價</b>計算，本身就含價差；'
          '信用卡則是以卡片組織匯率結算後再加手續費。'
          f'把兩邊都換算成「相對即期中價的成本」才比得出來——'
          f'以 {_b["date"]} 臺灣銀行牌告為例（即期中價 {_mid:.4f}）：</p>'
          '<div class="tw"><table><thead><tr><th>付款方式</th><th>換匯依據</th>'
          '<th>今日匯率</th><th>相對中價的成本</th></tr></thead><tbody>'
          f'<tr><td><b>電支（用即期賣出價）</b></td><td>即期賣出</td>'
          f'<td>{_b["spot_sell"]}</td><td class="win">＋{_c_spot:.2f}%</td></tr>'
          f'<tr><td><b>信用卡</b></td><td>卡組織匯率 ＋ {_c_card}% 手續費</td>'
          f'<td>—</td><td>＋{_c_card:.2f}%</td></tr>'
          f'<tr><td><b>電支（用現金賣出價）</b></td><td>現金賣出</td>'
          f'<td>{_b["cash_sell"]}</td><td class="lose">＋{_c_cash:.2f}%</td></tr>'
          '</tbody></table></div>'
          f'<p class="disc">卡組織匯率無法事先查詢，此處假設約等於即期中價；'
          f'若實際結算匯率高於中價，信用卡那列會再往上一點。'
          f'匯率取自 <a href="{_b["src"]}" rel="nofollow" target="_blank">'
          f'{html.escape(_b["src_name"])}</a>，{_b["date"]} 查詢。</p>'
          '<div class="tldr"><ul>'
          f'<li><b>「免 {_fx["typical"]}% 手續費」實際只省下約 {_save_spot:.1f} 個百分點。</b>'
          f'因為電支用的即期賣出價本身就比中價高 {_c_spot:.2f}%。</li>'
          + (f'<li><b>用現金賣出價的那幾家，等於沒省到。</b>成本 ＋{_c_cash:.2f}%，'
             f'比信用卡的 ＋{_c_card:.2f}% 還高 {abs(_save_cash):.2f} 個百分點。</li>'
             if _save_cash < 0 else
             f'<li>用現金賣出價的那幾家只省 {_save_cash:.2f} 個百分點，幾乎沒有差別。</li>')
          + '<li><b>真正的差距在回饋，不在手續費。</b>旅日信用卡的海外加碼是 '
            f'{min(c["total"] for c in CD["cards"]):.1f}%～{max(c["total"] for c in CD["cards"]):.1f}%，'
            f'比上面那零點幾個百分點大一個量級。走電支就拿不到這些加碼。</li>'
          '</ul></div>'
          '<h3>能不能綁信用卡？</h3>'
          '<p class="lede">這決定了你是「疊加」還是「二選一」。'
          '多數電支在境外只收銀行帳戶或儲值餘額，少數可綁自家或指定的卡。</p>'
          '<div class="tw"><table><thead><tr><th>電子支付</th><th>境外可用的付款來源</th>'
          '<th>換匯依據</th><th>資料來源</th></tr></thead><tbody>'
          + _mp_rows + '</tbody></table></div>'
          f'<p class="disc">查證於 {MP["checked"]}。'
          '標示「第三方整理」者本站尚未逐項比對發卡行或電支業者的官方公告，'
          '各家可綁的付款來源與檔期回饋變動很快，出發前請以業者當期公告為準。</p>'
          '<h3>所以怎麼選</h3>'
          '<div class="tldr"><ul>'
          '<li><b>大額消費用信用卡。</b>買相機、電器、精品這種一筆好幾萬的，'
          '海外加碼即使碰到上限也遠比電支的檔期回饋多，而且電支的檔期回饋'
          '上限多半只有每月一兩百元。</li>'
          '<li><b>小額、零散消費才輪到電支。</b>電支的檔期回饋率有時很高，'
          '但上限低，剛好適合吃飯、便利商店這種金額。</li>'
          '<li><b>別為了免手續費而放棄海外加碼。</b>省的是零點幾個百分點，'
          '放棄的是好幾個百分點。</li>'
          '<li><b>電支不是到處能用。</b>只在 PayPay 特約店有效，'
          '且不保證每台自助機台都支援，結帳前先問店員。</li>'
          '</ul></div>')

    # ── 11/1 免稅新制對回饋的影響 ────────────────────────
    # 直覺是「刷含稅價，回饋基數變大 10%」，但多數卡的加碼有上限，
    # 多刷的那 10% 其實拿不到回饋，反而讓上限更快滿。用實際卡片條件算給讀者看。
    _TFY = 100000                       # 稅前 10 萬日圓的商品
    _TFY2 = round(_TFY * TAXR)          # 含稅後實際要刷的金額
    _tf_rows, _tf_zero, _tf_d = '', 0, []
    for c in sorted(CD['cards'], key=lambda x: -x['total'])[:6]:
        o, _ = _back(c, _TFY, 'shop')
        n, _ = _back(c, _TFY2, 'shop')
        d = round(n) - round(o)
        _tf_d.append(d)
        if d <= 0:
            _tf_zero += 1
        _tf_rows += (f'<tr><td><b>{html.escape(c["name"])}</b></td>'
                     f'<td>{money(round(o))}</td><td>{money(round(n))}</td>'
                     + (f'<td class="win">＋{money(d)}</td>' if d > 0
                        else '<td class="lose">沒有增加</td>')
                     + '</tr>')
    _TF_BLOCK = (
      '<h2>11/1 免稅新制之後，回饋會變多嗎？</h2>'
      '<p class="lede">11 月 1 日起在店裡要先付含稅全額，出境經海關確認後才退稅。'
      f'同一件稅前 ¥{_TFY:,} 的商品，你刷的金額從 ¥{_TFY:,} 變成 ¥{_TFY2:,}，'
      '回饋基數多了 10%——直覺上應該多拿一點回饋。實際算下來沒那麼好：</p>'
      '<div class="tw"><table><thead><tr><th>卡片</th>'
      f'<th>10/31 前<br>刷 ¥{_TFY:,}</th><th>11/1 起<br>刷 ¥{_TFY2:,}</th>'
      '<th>差額</th></tr></thead><tbody>' + _tf_rows + '</tbody></table></div>'
      f'<p class="disc">以稅前 ¥{_TFY:,} 的實體消費、各層加碼全部成立試算，'
      f'匯率 {_MIDC} 並加計 {_fx["typical"]}% 國外交易手續費。'
      f'差額落在 {money(min(_tf_d))}～{money(max(_tf_d))}，'
      f'相當於帳單金額的 {min(_tf_d)/_bill(_TFY2)*100:.1f}%～{max(_tf_d)/_bill(_TFY2)*100:.1f}%——'
      f'而你為此先墊了 {money(round(_bill(_TFY2) - _bill(_TFY)))} 的稅金。</p>'
      '<div class="tldr"><ul>'
      + (f'<li><b>回饋最高的 6 張卡裡，有 {_tf_zero} 張一毛都沒多拿。</b>'
         '因為加碼早就到上限了，多刷的 10% 只能拿基本回饋，甚至完全不變。</li>'
         if _tf_zero else
         '<li><b>多拿到的金額很有限</b>，因為加碼大多有上限，多刷的 10% 只算得到基本回饋。</li>')
      + '<li><b>上限反而更快滿。</b>加碼上限換算出來的「刷到多少到頂」是台幣金額，不會變；'
        '但同樣的商品現在要多刷 10%，等於這個額度只夠買到原本約 <b>91%</b> 的東西。</li>'
      '<li><b>退稅若退回原卡，回饋可能被回沖。</b>多數發卡行的條款都寫明退款時可扣回已給的回饋，'
        '例如合作金庫：「持卡人如因任何理由退還刷卡買受之商品、服務或因簽帳爭議及其他原因而'
        '退還刷卡消費款項時，持卡人原先已取得之本活動回饋金額、本行得逕行調整扣回。」'
        '退稅能選退到信用卡、電子錢包、銀行帳戶或現金，'
        '在意這點的話，退款方式選現金或電子錢包最單純。</li>'
      '<li><b>還要先墊 10% 的現金。</b>加上 90 天內必須完成海關確認、退款服務商可能另收手續費，'
        '這些成本都比那點回饋差額大。</li>'
      '</ul></div>'
      '<p class="lede">結論：<b>別為了「回饋基數變大」改變你的刷卡計畫。</b>'
      '真正會被新制影響的是現金流與加碼額度的分配——'
      '想把加碼留給貴的東西，記得換算的是含稅金額。</p>'
      + '<div class="cities">'
      + f'<a class="ct" href="{U("/japan-tax-free-2026/")}"><b>🧾 11/1 免稅新制全解</b>'
        f'<s>要先墊多少、90 天期限、怎麼退</s></a></div>')

    _best = max(CD['cards'], key=lambda c: c['total'])
    _race = [c['name'] for c in CD['cards'] if c.get('reg_race')]
    cc_title = f'旅日信用卡怎麼挑？{CD["checked"][:4]} 下半年 {len(CD["cards"])} 張卡回饋與上限整理'
    cc_desc = (f'{len(CD["cards"])} 張旅日信用卡比較：回饋率、加碼上限換算成刷多少到頂、'
               f'限量登錄時間、國外交易手續費與 DCC 陷阱。輸入日幣金額即可試算。')

    write('japan-credit-card/index.html',
      head(cc_title, cc_desc, 'japan-credit-card/',
           '<script type="application/ld+json">' + cc_ld + '</script>')
      + crumbs([('首頁', '/'), ('旅日信用卡', None)]) + topnav()
      + '<h1>旅日信用卡怎麼挑？</h1>'
      + '<p class="lede">帳面最高回饋幾乎都是多層加碼疊出來的，而且各有上限。'
        '比較數字之前，先看「刷到多少就到頂」和「要不要搶登錄」。</p>'
      + f'<div class="today"><div class="tday">條件查證於 {CD["checked"]}'
        f'　·　{len(CD["cards"])} 張卡，各附發卡行官方來源　·　匯率 {_MIDC} 每日更新</div>'
        f'<div class="tans">帳面最高是 {html.escape(_best["name"])} 的 {_best["total"]}%，'
        f'但那是 {len(_tiers(_best,"shop"))} 層加碼全部同時成立的數字</div>'
        f'<div class="tsub">每層各有條件與上限，一般人不會全部符合。'
        f'實際能拿多少，要看你刷多少、刷在哪裡。</div>'
        + (f'<div class="tbuf">另外有 {len(_race)} 張卡的加碼需要<b>搶限量登錄</b>'
           f'（{html.escape("、".join(_race))}），沒登錄到就只有基本回饋。</div>' if _race else '')
        + '</div>'
      + f'<h2>{len(CD["cards"])} 張卡的條件比較</h2>'
      + '<div class="tw"><table><thead><tr><th>卡片</th><th>實體消費最高</th>'
        '<th>加碼刷到多少到頂</th><th>交通卡儲值</th><th>活動期間</th>'
        '</tr></thead><tbody>' + _crows + '</tbody></table></div>'
      + '<p class="disc">「實體消費最高」為該卡所有實體消費加碼同時成立時的合計值。'
        '實際回饋依權益等級、通路與交易方式而異。</p>'
      + _picker
      + fare_cta('tokyo', '卡選好了，機票呢')
      + '<h2>怎麼確實拿到這些回饋</h2>'
      + '<div class="tldr"><ul>'
        '<li><b>先確認這個月登錄了沒。</b>聯邦吉鶴卡每月 15 日 10:00、台北富邦 J 卡每月 18 日與 '
        '20 日 16:00 開放登錄，都有名額上限，額滿為止。</li>'
        '<li><b>該切換的要切換。</b>台新與國泰是在 App 切換權益方案，而且是<b>消費當日</b>'
        '要在切換狀態，事後補切沒有用。</li>'
        '<li><b>結帳一律選日圓。</b>選台幣是 DCC，匯率通常差 3–5%，而且多數銀行的海外加碼'
        '要求以外幣結帳。</li>'
        '<li><b>要面對面刷。</b>多數海外加碼限定當地實體商店的面對面交易，'
        '海外訂房平台、網購、訂閱服務常被排除。</li>'
        '<li><b>把加碼額度留給貴的東西。</b>加碼上限換算下來通常是一萬多元。</li>'
        '</ul></div>'
      + _MP_BLOCK
      + _TF_BLOCK
      + '<h2>每張卡的細節</h2><div class="cities">'
      + ''.join(f'<a class="ct" href="{U("/japan-credit-card/"+c["slug"]+"/")}">'
                f'<b>{html.escape(c["name"])}</b><s>{html.escape(c["plan"])}</s>'
                f'<u>最高 {c["total"]}%</u></a>' for c in sorted(CD['cards'], key=lambda x: -x['total']))
      + '</div>'
      + '<h2>順便看看</h2><div class="cities">'
      + f'<a class="ct" href="{U("/japan-card-calculator/")}"><b>🧮 回饋計算機</b>'
        f'<s>輸入日幣金額，換算回饋</s></a>'
      + f'<a class="ct" href="{U("/apple-japan-price/")}"><b>🍎 買 iPhone 台灣還日本划算</b>'
        f'<s>可填入你的回饋率試算</s></a>'
      + f'<a class="ct" href="{U("/japan-tax-free-2026/")}"><b>🧾 11/1 免稅新制</b>'
        f'<s>改成出境後才退稅</s></a></div>'
      + '<h2>常見問題</h2>' + cc_html
      + f'<p class="disc">本頁為公開資訊整理，非理財或投資建議。'
        f'各卡條件、指定通路、回饋上限與登錄規則由發卡行隨時調整，'
        f'表中內容查證於 {CD["checked"]}，申辦或消費前請以發卡行公告為準。'
        f'本站與上述發卡行無合作關係，頁內卡片連結非聯盟連結。</p>'
      + foot())
    pages.append(('/japan-credit-card/', 0.8))

    # ── 每張卡的獨立介紹頁 ──
    _YEN = [10000, 30000, 50000, 100000, 200000, 500000]
    for c in CD['cards']:
        hit = _hit(c, 'shop')
        rows = ''
        for y in _YEN:
            b = _bill(y); v, cap = _back(c, y, 'shop')
            rows += (f'<tr><td>¥{y:,}</td><td>{money(round(b))}</td>'
                     f'<td class="win"><b>{money(round(v))}</b></td>'
                     f'<td>{v/b*100:.1f}%{SMALL}{"加碼已滿" if cap else "加碼未滿"}</small></td>'
                     f'<td>{money(round(b-v))}</td></tr>')

        trows = ''.join(
            f'<tr><td><b>{html.escape(t["label"])}</b>{SMALL}{html.escape(t["cond"])}</small></td>'
            f'<td>+{t["rate"]}%</td>'
            f'<td>{(t["cap_unit"] + " " + money(t["cap"])) if t["cap"] else "未標示"}</td>'
            f'<td>{SCOPE_NAME[t["scope"]]}</td></tr>'
            for t in c['tiers'])

        others = ''.join(
            f'<tr><td><a href="{U("/japan-credit-card/"+o["slug"]+"/")}">{html.escape(o["name"])}</a></td>'
            f'<td>{o["total"]}%</td>'
            f'<td>{money(round(_back(o, 100000, "shop")[0]))}</td></tr>'
            for o in sorted(CD['cards'], key=lambda x: -x['total']) if o['slug'] != c['slug'])

        cf = [
         (f'{c["name"]}在日本刷卡回饋多少？',
          f'{c["base_note"]}。'
          + (''.join(f'另有{t["label"]} {t["rate"]}%（{t["cond"]}）。' for t in c['tiers']))
          + (f'實體消費全部加碼同時成立時合計最高 {c["total"]}%，'
             f'但台幣帳單刷到約 {money(hit)} 加碼就到頂，超過的部分只剩 {c["base"]}%。'
             if hit else f'合計最高 {c["total"]}%。')),
         (f'{c["name"]}要登錄嗎？', c['reg'] + '。'),
         (f'什麼情況拿不到{c["name"]}的加碼？',
          '；'.join(c['exclude']) + '。另外結帳時若選台幣（DCC），'
          '不只匯率差 3–5%，多數銀行的海外加碼也要求以外幣結帳。'),
         (f'{c["name"]}適合什麼人？', f'適合：{c["good"]} 不適合：{c["bad"]}'),
        ]
        cf_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                          + html.escape(a) + '</div></details>' for q, a in cf)
        cf_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in cf]}, ensure_ascii=False)

        t_ = f'{c["name"]}日本回饋怎麼算？最高 {c["total"]}% 的上限與登錄方式'
        de = (f'{c["name"]}（{c["plan"]}）日本消費最高 {c["total"]}%，'
              + (f'加碼刷到約 {money(hit)} 到頂。' if hit else '無加碼上限。')
              + '含各金額實拿試算、加碼層級、登錄時間與不適用情況。')

        write(f'japan-credit-card/{c["slug"]}/index.html',
          head(t_, de, f'japan-credit-card/{c["slug"]}/',
               '<script type="application/ld+json">' + cf_ld + '</script>')
          + crumbs([('首頁', '/'), ('旅日信用卡', '/japan-credit-card/'), (c['name'], None)])
          + topnav()
          + f'<h1>{html.escape(c["name"])}　日本回饋怎麼算？</h1>'
          + f'<p class="lede">{html.escape(c["plan"])}　·　活動期間 {html.escape(c["period"])}</p>'
          + f'<div class="today"><div class="tday">條件查證於 {CD["checked"]}'
            f'　·　匯率 {_MIDC} 每日更新</div>'
            f'<div class="tans">實體消費最高 {c["total"]}%'
            + (f'，加碼刷到 {money(hit)} 就到頂' if hit else '，無加碼上限') + '</div>'
            f'<div class="tsub">{html.escape(c["base_note"])}。'
            + (f'另有 {len(c["tiers"])} 層加碼，各有條件與上限，需同時符合才疊得上去。'
               if c['tiers'] else '') + '</div>'
            + (f'<div class="tbuf">⚠ 加碼需<b>搶限量登錄</b>：{html.escape(c["reg"])}</div>'
               if c.get('reg_race') else
               (f'<div class="tbuf">超過之後只剩 <b>{c["base"]}%</b>。</div>' if hit else ''))
            + '</div>'
          + (('<h2>回饋是怎麼疊出來的</h2>'
              f'<p class="lede">基本 {c["base"]}%（{html.escape(c["base_note"])}），'
              f'再加上以下各層。每層各自受上限限制，也各自要符合條件。</p>'
              '<div class="tw"><table><thead><tr><th>加碼項目</th><th>加碼</th>'
              '<th>上限</th><th>適用</th></tr></thead><tbody>' + trows + '</tbody></table></div>')
             if c['tiers'] else '')
          + '<h2>刷多少、實拿多少</h2>'
          + f'<p class="lede">以中間匯率 {_MIDC} 換算並加計 {_fx["typical"]}% 國外交易手續費，'
            f'假設實體消費的各層加碼條件都符合。</p>'
          + '<div class="tw"><table><thead><tr><th>日幣消費</th><th>台幣帳單</th>'
            '<th>實拿回饋</th><th>有效回饋率</th><th>實際負擔</th>'
            '</tr></thead><tbody>' + rows + '</tbody></table></div>'
          + '<p class="disc">回饋以台幣帳單金額計算；點數型回饋以 1 點約 1 元估算。</p>'
          + fare_cta('tokyo', '算完回饋，順便看機票')
          + '<h2>怎麼啟用</h2><div class="tldr"><ul>'
          + ''.join(f'<li>{html.escape(x)}</li>' for x in c['steps'])
          + '</ul></div>'
          + '<h2>什麼情況拿不到</h2><div class="tldr"><ul>'
          + ''.join(f'<li>{html.escape(x)}</li>' for x in c['exclude'])
          + '<li>結帳選台幣（DCC）——匯率差 3–5%，且多數銀行的海外加碼要求以外幣結帳。</li>'
          + '</ul></div>'
          + '<h2>適合誰</h2>'
          + f'<p class="lede"><b>適合</b>：{html.escape(c["good"])}</p>'
          + f'<p class="lede"><b>不適合</b>：{html.escape(c["bad"])}</p>'
          + '<h2>跟其他卡比（日幣 10 萬為例）</h2>'
          + '<div class="tw"><table><thead><tr><th>卡片</th><th>實體消費最高</th>'
            '<th>¥100,000 實拿</th></tr></thead><tbody>'
          + f'<tr><td><b>{html.escape(c["name"])}</b>（本頁）</td><td>{c["total"]}%</td>'
            f'<td class="win"><b>{money(round(_back(c, 100000, "shop")[0]))}</b></td></tr>'
          + others + '</tbody></table></div>'
          + '<div class="cities">'
          + f'<a class="ct" href="{U("/japan-card-calculator/")}"><b>🧮 回饋計算機</b>'
            f'<s>輸入日幣金額，換算回饋</s></a>'
          + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 {len(CD["cards"])} 張卡比較</b>'
            f'<s>上限、登錄與適用範圍</s></a>'
          + f'<a class="ct" href="{U("/japan-tax-free-2026/")}"><b>🧾 11/1 免稅新制</b>'
            f'<s>改成出境後才退稅</s></a></div>'
          + '<h2>常見問題</h2>' + cf_html
          + f'<p class="disc">本頁為公開資訊整理，非理財建議。條件查證於 {CD["checked"]}，'
            f'來源：<a href="{html.escape(c["src"])}" target="_blank" rel="noopener nofollow">'
            f'{html.escape(c["src_name"])}</a>。'
            f'發卡行可隨時調整條件、指定通路與上限，請以發卡行公告為準。'
            f'本站與發卡行無合作關係，頁內卡片連結非聯盟連結。</p>'
          + foot())
        pages.append((f'/japan-credit-card/{c["slug"]}/', 0.7))

    # ── 日幣回饋計算機 ──
    _calc_js = _CJS + ("""
<script>
(function(){
 var $=function(i){return document.getElementById(i)};
 function run(){
  var i=+$('kc').value, y=+$('ky').value||0, mode=$('ks').value;
  var c=JCARD.cards[i];
  if(!jhas(c,mode)){$('kv').className='cv tw';
    $('kv').textContent='這張卡在此消費類型沒有加碼，只有基本回饋';mode='base';}
  var o=jback(c,y,mode), net=o.bill-o.v;
  $('k1').textContent='¥'+jfmt(y);
  $('k2').textContent='NT$'+jfmt(o.bill);
  $('k3').innerHTML='NT$'+jfmt(o.v)+'<i class="pp">≈ ¥'+jfmt(o.v/JCARD.mid)+'</i>';
  $('k4').innerHTML='NT$'+jfmt(net)+'<i class="pp">≈ ¥'+jfmt(net/JCARD.mid)+'</i>';
  if(y>0&&jhas(c,$('ks').value)){$('kv').className='cv '+(o.cap?'tw':'jp');
   $('kv').textContent='有效回饋率 '+(o.v/o.bill*100).toFixed(2)+'%'+
    (o.cap?'　·　加碼已達上限，再刷下去只剩 '+c.base+'%':'')+
    (c.race?'　·　此卡加碼需搶限量登錄':'');}
  $('kr').innerHTML=JCARD.cards.map(function(x){var r=jback(x,y,jhas(x,$('ks').value)?$('ks').value:'base');
    return '<div class="cl"><span><a href="'+%HUB%+'/'+x.s+'/">'+x.n+'</a>'+
     (jhas(x,$('ks').value)?'':'<i class="pc">此類型無加碼</i>')+'</span><b>NT$'+
     jfmt(r.v)+'</b></div>';}).join('');
 }
 ['kc','ky','ks'].forEach(function(i){var e=$(i);if(e){e.addEventListener('input',run);e.addEventListener('change',run);}});
 run();
})();
</script>""").replace('%HUB%', json.dumps(U('/japan-credit-card')))

    _kopts = ''.join(f'<option value="{i}">{html.escape(c["name"])}（{html.escape(c["plan"])}）</option>'
                     for i, c in enumerate(CD['cards']))
    kc_faq = [
     ('回饋是用日幣還是台幣計算？',
      '台幣。海外刷卡會先由卡片組織換算成台幣入帳，再加上國外交易手續費，'
      '銀行的回饋依這筆台幣金額計算。本頁把回饋同時折算回日幣顯示，'
      '是為了讓你在店裡看標價時好抓，實際入帳與回饋都是台幣。'),
     ('為什麼帳單金額比我用匯率算的高？',
      f'因為多了國外交易手續費，多數發卡行約 {_fx["typical"]}%（國際組織 1% ＋ 發卡行 0.5%），'
      f'美國運通約 {_fx["amex"]}%。本頁的台幣帳單已經加進去了。'),
     ('算出來的金額準嗎？',
      '當成比較用的估算。實際入帳取決於卡片組織當日匯率與請款日；'
      '回饋也受權益等級、排除通路與登錄狀態影響。本頁採各卡公告的最高情境計算，'
      '也就是各層加碼條件都符合時的數字。'),
     ('為什麼有些卡在某個消費類型沒有數字？',
      '因為那張卡在該類型沒有加碼。例如交通卡儲值加碼目前只有部分卡片提供，'
      '其餘卡片在該情境下只有基本回饋。'),
    ]
    kc_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                      + html.escape(a) + '</div></details>' for q, a in kc_faq)
    kc_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in kc_faq]}, ensure_ascii=False)

    write('japan-card-calculator/index.html',
      head('日本刷卡回饋計算機｜輸入日幣金額，換算實拿回饋與台幣帳單',
           f'選擇信用卡、輸入日幣消費金額，立即算出台幣帳單（含 {_fx["typical"]}% 國外交易手續費）、'
           f'實拿回饋與實際負擔，回饋同時顯示日幣與台幣。收錄 {len(CD["cards"])} 張旅日信用卡，'
           f'匯率每日更新。', 'japan-card-calculator/',
           '<script type="application/ld+json">' + kc_ld + '</script>')
      + crumbs([('首頁', '/'), ('旅日信用卡', '/japan-credit-card/'), ('回饋計算機', None)])
      + topnav()
      + '<h1>日本刷卡回饋計算機</h1>'
      + '<p class="lede">在店裡看到日圓標價，想知道刷下去實際負擔多少、回饋拿得到多少。'
        f'選卡、輸入金額就好，目前收錄 {len(CD["cards"])} 張卡。</p>'
      + f'<p class="upd">換算匯率 {_MIDC}（中間匯率）　·　'
        f'國外交易手續費 {_fx["typical"]}%　·　匯率每日自動更新'
        + (f'　·　{_RDATE}' if _RDATE else '') + '</p>'
      + '<div class="calc"><div class="sf">'
      + f'<label>信用卡<select id="kc">{_kopts}</select></label>'
      + '<label>日幣金額 ¥<input id="ky" type="number" value="100000" min="0" step="1000"></label>'
      + f'<label>消費類型<select id="ks">{_mopts}</select></label>'
      + '</div><div class="cres">'
        '<div class="cl"><span>日幣消費</span><b id="k1">—</b></div>'
        '<div class="cl"><span>台幣帳單（含手續費）</span><b id="k2">—</b></div>'
        '<div class="cl"><span>實拿回饋</span><b id="k3">—</b></div>'
        '<div class="cl"><span>實際負擔</span><b id="k4">—</b></div>'
        '<div class="cv" id="kv">—</div></div></div>'
      + '<h3>同金額下其他卡拿多少</h3><div class="cres" id="kr"></div>'
      + f'<p class="disc">回饋依台幣帳單金額計算，點數型回饋以 1 點約 1 元估算。'
        f'試算採各層加碼條件都符合的最高情境，實際以發卡行為準。條件查證於 {CD["checked"]}。</p>'
      + fare_cta('tokyo', '算完回饋，順便看機票')
      + '<h2>常見問題</h2>' + kc_html
      + '<h2>相關頁面</h2><div class="cities">'
      + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 {len(CD["cards"])} 張卡完整比較</b>'
        f'<s>上限、登錄方式與適用範圍</s></a>'
      + f'<a class="ct" href="{U("/apple-japan-price/")}"><b>🍎 買 iPhone 台灣還日本划算</b>'
        f'<s>含刷卡回饋試算</s></a>'
      + f'<a class="ct" href="{U("/japan-tax-free-2026/")}"><b>🧾 11/1 免稅新制</b>'
        f'<s>改成出境後才退稅</s></a></div>'
      + '<p class="disc">本頁為公開資訊整理，非理財建議。本站與各發卡行無合作關係，'
        '頁內卡片連結非聯盟連結。</p>'
      + _calc_js + foot())
    pages.append(('/japan-card-calculator/', 0.8))

    # ── 日本購物折扣：折價券 × 免稅 × 刷卡回饋 ──────────
    if os.path.exists('coupons.json'):
        CP = json.load(open('coupons.json', encoding='utf-8'))
        _srows = ''.join(
            f'<tr><td><a href="{U("/japan-coupon/"+st["slug"]+"/")}">'
            f'<b>{html.escape(st["name"])}</b></a>{SMALL}{html.escape(st["jp"])}</small></td>'
            f'<td>{html.escape(st["cat"])}</td>'
            f'<td class="win"><b>{html.escape(st["rate"])}</b></td>'
            f'<td>{html.escape(st["tiers"])}</td>'
            f'<td>{html.escape(st["tax_min"])}</td></tr>'
            for st in sorted(CP['stores'], key=lambda x: (x['cat'], -x['max'])))

        _cpjs = _CJS + ("""
<script>
(function(){
 var $=function(i){return document.getElementById(i)};
 function run(){
  var p=+$('sp').value||0, cr=(+$('sc').value||0)/100,
      c=JCARD.cards[+$('sk').value], mode=$('sm').value;
  var free=p/1.1, after=free*(1-cr);
  var o=jback(c,after,jhas(c,mode)?mode:'base');
  var net=o.bill-o.v, orig=p*JCARD.mid;
  $('s1').textContent='¥'+jfmt(p);
  $('s2').textContent='¥'+jfmt(free);
  $('s3').textContent='¥'+jfmt(after);
  $('s4').textContent='NT$'+jfmt(o.bill);
  $('s5').innerHTML='－NT$'+jfmt(o.v)+'<i class="pp">'+
    ((c.tiers.length&&!jhas(c,mode))?'此類型無加碼，僅基本回饋':'')+'</i>';
  $('s6').innerHTML='NT$'+jfmt(net)+'<i class="pp">≈ ¥'+jfmt(net/JCARD.mid)+'</i>';
  $('sv').className='cv '+(net<orig?'jp':'tw');
  $('sv').textContent=p?('相當於原價的 '+(net/orig*10).toFixed(1)+' 折　·　'+
    '共省下 NT$'+jfmt(orig-net)):'請輸入定價';
 }
 ['sp','sc','sk','sm'].forEach(function(i){var e=$(i);if(e){e.addEventListener('input',run);e.addEventListener('change',run);}});
 run();
})();
</script>""").replace('%HUB%', json.dumps(U('/japan-credit-card')))

        _sopts = ''.join(f'<option value="{i}">{html.escape(c["name"])}</option>'
                         for i, c in enumerate(CD['cards']))
        _copts = ('<option value="0">不使用折價券</option>'
                  + ''.join(f'<option value="{r}"{" selected" if r==7 else ""}>折 {r}%</option>'
                            for r in (3, 5, 7, 10, 12)))

        cp_faq = [
         ('折價券和免稅可以一起用嗎？',
          '多數店家可以，而且順序是先扣免稅、券再以免稅後金額計算，所以不是單純把兩個百分比相加。'
          '以 ¥10,000 含稅商品為例，免稅後約 ¥9,091，再折 7% 是 ¥8,455，'
          '合計約省 15.4%，不是 17%。少數店家的券不可與免稅併用，結帳前要問清楚。'),
         ('券要什麼時候出示？',
          '結帳前。多數店家是把手機上的券畫面給店員掃描，一旦開始結帳或已經完成免稅手續才拿出來，'
          '通常就不能補折。人多的時候先把券頁面開好。'),
         ('2026/11/1 免稅改制後，這個算法會變嗎？',
          '會變的是拿到退稅的時間點，不是折扣本身。11/1 起日本改採退款方式，'
          '購買當下要先付含稅全額（券的折扣仍當場扣），出境經海關確認後才退還消費稅。'
          '所以最終負擔差不多，但結帳當下要多掏一筆消費稅，且要記得完成出境手續。'),
         ('哪裡拿得到這些券？',
          '多數由店家的官方觀光頁面或合作的旅遊媒體發放，也有店家在機場、飯店、'
          '觀光案內所放實體券。券的版本與期限經常更換，出發前一週再找一次最準，'
          '本頁只整理常見折扣幅度，不提供券本身。'),
         ('刷卡回饋是算在折扣後的金額嗎？',
          '是。銀行是依實際入帳的台幣金額計算回饋，而入帳金額是折扣後的金額再換算台幣、'
          '加上國外交易手續費。所以折扣越多，回饋的絕對金額會越少，但你總共付出的錢還是更少。'),
        ]
        cp_html = ''.join('<details class="faq"><summary>' + html.escape(q) + '</summary><div>'
                          + html.escape(a) + '</div></details>' for q, a in cp_faq)
        cp_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in cp_faq]}, ensure_ascii=False)

        write('japan-coupon/index.html',
          head('日本購物折扣怎麼疊？折價券 × 免稅 × 刷卡回饋實付價計算機',
               f'日本藥妝、電器行折價券常見折扣幅度整理，並提供實付價試算：'
               f'先扣免稅、再折券、最後扣刷卡回饋，直接算出相當於原價幾折。'
               f'收錄 {len(CP["stores"])} 家店與 {len(CD["cards"])} 張信用卡。',
               'japan-coupon/',
               '<script type="application/ld+json">' + cp_ld + '</script>')
          + crumbs([('首頁', '/'), ('日本購物折扣', None)]) + topnav()
          + '<h1>日本購物折扣怎麼疊才對？</h1>'
          + '<p class="lede">折價券、免稅、刷卡回饋是三件事，而且不是把百分比相加。'
            '順序錯了，算出來的實付價會差很多。</p>'
          + f'<div class="today"><div class="tday">折扣幅度查證於 {CP["checked"]}'
            f'　·　匯率 {_MIDC} 每日更新</div>'
            f'<div class="tans">{html.escape(CP["order"])}</div>'
            f'<div class="tsub">以 ¥10,000 含稅商品為例：免稅後約 ¥9,091，再折 7% 是 ¥8,455，'
            f'合計省約 15.4%——不是 10% ＋ 7% ＝ 17%。</div>'
            f'<div class="tbuf">再疊上刷卡回饋，最高可以壓到原價的 <b>七折出頭</b>。'
            f'下面可以用自己的金額和卡片試算。</div></div>'
          + '<h2>實付價計算機</h2>'
          + '<div class="calc"><div class="sf">'
            '<label>商品定價（含稅）¥<input id="sp" type="number" value="50000" min="0" step="1000"></label>'
            f'<label>折價券<select id="sc">{_copts}</select></label>'
            f'<label>信用卡<select id="sk">{_sopts}</select></label>'
            f'<label>消費類型<select id="sm">{_mopts}</select></label>'
            '</div><div class="cres">'
            '<div class="cl"><span>日幣定價（含稅）</span><b id="s1">—</b></div>'
            '<div class="cl"><span>扣免稅 10% 後</span><b id="s2">—</b></div>'
            '<div class="cl"><span>再折價券後</span><b id="s3">—</b></div>'
            '<div class="cl"><span>台幣帳單（含手續費）</span><b id="s4">—</b></div>'
            '<div class="cl"><span>刷卡回饋</span><b id="s5">—</b></div>'
            '<div class="cl"><span>實際負擔</span><b id="s6">—</b></div>'
            '<div class="cv" id="sv">—</div></div></div>'
          + f'<p class="disc">以中間匯率 {_MIDC} 換算並加計 {_fx["typical"]}% 國外交易手續費。'
            f'刷卡回饋依折扣後的台幣帳單計算，採各卡最高情境。'
            f'折扣幅度為常見級距，實際以店家當期公告為準。</p>'
          + fare_cta('tokyo', '算完省多少，機票呢')
          + f'<h2>{len(CP["stores"])} 家常見店家的折扣幅度</h2>'
          + '<p class="lede">以下是各店常見的券折扣級距。券的版本與期限經常更換，'
            '出發前一週再確認一次最準——本頁整理的是幅度，不提供券本身。</p>'
          + '<div class="tw"><table><thead><tr><th>店家</th><th>類別</th><th>常見折扣</th>'
            '<th>級距與條件</th><th>免稅／用券門檻</th></tr></thead><tbody>'
            + _srows + '</tbody></table></div>'
          + '<div class="cities">'
          + ''.join(f'<a class="ct" href="{U("/japan-coupon/"+st["slug"]+"/")}">'
                    f'<b>{html.escape(st["name"])}</b><s>{html.escape(st["cat"])}・'
                    f'{html.escape(st["jp"])}</s><u>{html.escape(st["rate"])}</u></a>'
                    for st in sorted(CP['stores'], key=lambda x: -x['max']))
          + '</div>'
          + '<h2>三個常犯的錯</h2><div class="tldr"><ul>'
            '<li><b>把百分比直接相加。</b>免稅 10% 加券 7% 不等於 17%。'
            '券是以免稅後的金額計算，實際約 15.4%。</li>'
            '<li><b>結帳到一半才拿出券。</b>多數店家要在結帳前出示，'
            '已經開始免稅手續才拿出來通常不能補折。</li>'
            '<li><b>以為每家都能併用。</b>少數店家的券與免稅二擇一，'
            '百貨或車站內的櫃位也常有另外的規則。</li>'
            '</ul></div>'
          + '<h2>11/1 之後會不一樣</h2>'
          + '<p class="lede">2026 年 11 月 1 日起日本免稅改採退款方式：券的折扣仍是當場扣，'
            '但消費稅要先付、出境經海關確認後才退還。最終負擔差不多，'
            '但結帳當下要多掏一筆，而且要記得完成出境手續，'
            f'還有<b>購買日起 90 天</b>的確認期限。</p>'
          + cta('esim', '日本', '東京', '出發前先把上網搞定',
                '到 Klook 買 eSIM 或網卡，落地就能開導航找店')
          + '<h2>常見問題</h2>' + cp_html
          + '<h2>相關頁面</h2><div class="cities">'
          + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 {len(CD["cards"])} 張旅日信用卡</b>'
            f'<s>回饋、上限與登錄時間</s></a>'
          + f'<a class="ct" href="{U("/japan-tax-free-2026/")}"><b>🧾 11/1 免稅新制</b>'
            f'<s>改成出境後才退稅</s></a>'
          + f'<a class="ct" href="{U("/japan-card-calculator/")}"><b>🧮 回饋計算機</b>'
            f'<s>輸入日幣金額，換算回饋</s></a></div>'
          + f'<p class="disc">本頁為公開資訊整理，折扣幅度查證於 {CP["checked"]}，'
            f'券的取得管道、幅度與期限由各店家隨時調整，請以店家當期公告為準。'
            f'本站不提供折價券本身，與文中店家亦無合作關係。'
            f'頁內部分連結為聯盟行銷連結，本站可能獲得分潤，不影響你的價格。</p>'
          + _cpjs + foot())
        pages.append(('/japan-coupon/', 0.8))

        # ── 每家店的獨立頁 ──
        for st in CP['stores']:
            _ex = '<div class="tw"><table><thead><tr><th>日幣定價（含稅）</th>'\
                  '<th>免稅後（未稅）</th><th>適用折扣</th><th>折券後</th>'\
                  '<th>合計省下</th></tr></thead><tbody>'
            def _rate_at(st, free):
                """依未稅金額取得適用折扣；有級距時按級距，否則用單一費率"""
                if not st['steps']:
                    return st['max']
                r = 0
                for thr, rt in st['steps']:
                    if free >= thr: r = rt
                return r
            for y in (10000, 30000, 50000, 100000):
                free = y / 1.1
                rt = _rate_at(st, free)
                after = free * (1 - rt / 100)
                _ex += (f'<tr><td>¥{y:,}</td><td>¥{round(free):,}</td>'
                        f'<td>{(str(rt) + "%") if rt else "未達用券門檻"}</td>'
                        f'<td class="win"><b>¥{round(after):,}</b></td>'
                        f'<td>{(1-after/y)*100:.1f}%</td></tr>')
            _ex += '</tbody></table></div>'

            _oth = ''.join(
                f'<tr><td><a href="{U("/japan-coupon/"+o["slug"]+"/")}">{html.escape(o["name"])}</a></td>'
                f'<td>{html.escape(o["cat"])}</td><td>{html.escape(o["rate"])}</td></tr>'
                for o in sorted(CP['stores'], key=lambda x: -x['max'])
                if o['slug'] != st['slug'] and o['cat'] == st['cat'])

            sf = [
             (f'{st["name"]}的折價券可以折多少？',
              f'{st["tiers"]}。券以免稅後的金額計算，不是直接和免稅相加——'
              f'以 ¥10,000 含稅商品為例，免稅後約 ¥9,091，再折 {st["max"]}% 之後，'
              f'合計約省 {(1-(10000/1.1*(1-st["max"]/100))/10000)*100:.1f}%。'),
             (f'{st["name"]}的券可以和免稅一起用嗎？', f'{st["combo"]}。{st["tax_min"]}。'),
             (f'{st["name"]}的券去哪裡拿？什麼時候出示？', f'{st["how"]}。{st["when"]}。'),
             (f'在{st["name"]}買東西要注意什麼？',
              '；'.join(st['watch']) + '。' if st['watch'] else
              '沒有特別限制，但折扣幅度與適用商品仍以店家當期公告為準。'),
            ]
            sf_html = ''.join('<details class="faq"><summary>' + html.escape(q)
                              + '</summary><div>' + html.escape(a) + '</div></details>'
                              for q, a in sf)
            sf_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in sf]}, ensure_ascii=False)

            write(f'japan-coupon/{st["slug"]}/index.html',
              head(f'{st["name"]}優惠券怎麼用？折扣幅度、免稅併用與實付價試算',
                   f'{st["name"]}（{st["jp"]}）常見折扣 {st["rate"]}，{st["combo"]}。'
                   f'含級距條件、券的取得與出示時機、免稅門檻，'
                   f'以及折價券加免稅加刷卡回饋的實付價試算。',
                   f'japan-coupon/{st["slug"]}/',
                   '<script type="application/ld+json">' + sf_ld + '</script>')
              + crumbs([('首頁', '/'), ('日本購物折扣', '/japan-coupon/'), (st['name'], None)])
              + topnav()
              + f'<h1>{html.escape(st["name"])}優惠券怎麼用？</h1>'
              + f'<p class="lede">{html.escape(st["jp"])}　·　{html.escape(st["cat"])}　·　'
                f'折扣幅度查證於 {CP["checked"]}</p>'
              + f'<div class="today"><div class="tday">常見折扣 {html.escape(st["rate"])}'
                f'　·　{html.escape(st["combo"])}　·　{html.escape(st["tax_min"])}</div>'
                f'<div class="tans">{html.escape(st["tiers"])}</div>'
                f'<div class="tsub">券以<b>免稅後</b>的金額計算，不是和免稅相加。'
                f'以 ¥10,000 含稅商品為例，免稅後約 ¥9,091，再折 {st["max"]}%，'
                f'合計約省 {(1-(10000/1.1*(1-st["max"]/100))/10000)*100:.1f}%。</div>'
                f'<div class="tbuf">{html.escape(st["when"])}</div></div>'
              + '<h2>不同金額省多少</h2>'
              + f'<p class="lede">先扣免稅，券再以未稅金額計算。'
                + ('該店有滿額級距，未稅金額決定適用哪一檔。' if st['steps'] else
                   f'該店為單一費率 {st["max"]}%。') + '</p>'
              + _ex
              + f'<p class="disc">實際折扣依商品類別與當期券別而異，以店家公告為準。'
                f'想連刷卡回饋一起算，可用<a href="{U("/japan-coupon/")}">實付價計算機</a>。</p>'
              + fare_cta('tokyo', '算完省多少，機票呢')
              + '<h2>券怎麼拿、什麼時候出示</h2><div class="tldr"><ul>'
              + f'<li><b>取得</b>：{html.escape(st["how"])}</li>'
                f'<li><b>出示時機</b>：{html.escape(st["when"])}</li>'
                f'<li><b>免稅門檻</b>：{html.escape(st["tax_min"])}</li>'
                f'<li><b>與免稅併用</b>：{html.escape(st["combo"])}</li>'
              + '</ul></div>'
              + (('<h2>要注意的地方</h2><div class="tldr"><ul>'
                  + ''.join(f'<li>{html.escape(x)}</li>' for x in st['watch'])
                  + '</ul></div>') if st['watch'] else '')
              + '<h2>適合誰</h2>'
              + f'<p class="lede"><b>好處</b>：{html.escape(st["good"])}</p>'
              + f'<p class="lede"><b>限制</b>：{html.escape(st["bad"])}</p>'
              + (('<h2>同類型的其他店</h2><div class="tw"><table><thead><tr>'
                  '<th>店家</th><th>類別</th><th>常見折扣</th></tr></thead><tbody>'
                  + _oth + '</tbody></table></div>') if _oth else '')
              + '<h2>相關頁面</h2><div class="cities">'
              + f'<a class="ct" href="{U("/japan-coupon/")}"><b>🏷️ 實付價計算機</b>'
                f'<s>折價券×免稅×刷卡回饋一起算</s></a>'
              + f'<a class="ct" href="{U("/japan-credit-card/")}"><b>💳 旅日信用卡</b>'
                f'<s>哪張卡回饋最高</s></a>'
              + f'<a class="ct" href="{U("/japan-tax-free-2026/")}"><b>🧾 11/1 免稅新制</b>'
                f'<s>改成出境後才退稅</s></a></div>'
              + '<h2>常見問題</h2>' + sf_html
              + f'<p class="disc">本頁為公開資訊整理。折扣幅度與券的取得管道查證於 {CP["checked"]}，'
                f'由店家隨時調整，請以店家當期公告為準。本站不提供折價券本身，'
                f'與文中店家無合作關係。{html.escape(CP["tax_note"])}</p>'
              + foot())
            pages.append((f'/japan-coupon/{st["slug"]}/', 0.7))
        print(f'   店家頁 {len(CP["stores"])} 頁')

        print(f'   日本購物折扣頁：{len(CP["stores"])} 家店')

    print(f'   旅日信用卡：{len(CD["cards"])} 張卡頁 ＋ 比較頁 ＋ 計算機（查證 {CD["checked"]}）')

# ---------- sitemap / robots ----------
LASTMOD=NOW.strftime('%Y-%m-%dT%H:%M:%S%z')      # 含時區偏移，避免相對 UTC 變成未來日期
LASTMOD=LASTMOD[:-2]+':'+LASTMOD[-2:]            # +0800 → +08:00（W3C Datetime 格式）
urls='\n'.join(f'  <url><loc>{SITE}{U(u)}</loc><lastmod>{LASTMOD}</lastmod>'
             f'<changefreq>daily</changefreq><priority>{p}</priority></url>' for u,p in pages)
write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n'
      f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}{BASE}/sitemap.xml\n')
write('.nojekyll','')

