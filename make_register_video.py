"""信用卡加碼登錄日曆 短影音（直式 1080×1920、手繪貼紙月曆＋原創 Lo-fi 配樂）。

數字與日期不在這裡寫死：直接讀線上 /japan-card-register/ 的「全部的登錄活動」表（卡片、加碼、開放時間、下一次、名額）
與「逐張怎麼登錄」各檔的「資格」（當月／當季／活動期間一次），挑出下一次落在目標月份的那幾檔。
適用國家不含日本的（名稱有「非日本」）不放進月曆，收尾小字照實寫出沒列。
星期與月曆格子用 Python 的 calendar 排，並和頁上「下一次」括號裡的星期對過，不一致就停下來。
畫面算繪與合成沿用 make_transit_video_v2（Playwright 截圖 → ffmpeg）。
用法：python3 make_register_video.py [輸出資料夾]；環境變數 MONTH=2026-12 指定月份（預設：15 號以後做下個月）
"""
import calendar
import datetime as dt
import html as htm
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else 'cards/threads/短影音-登錄日曆12月'
sys.argv = sys.argv[:1]
import make_transit_video_v2 as V  # noqa: E402

URL = 'https://jptripcard.com/japan-card-register/'
W, H, FPS = V.W, V.H, V.FPS
BPM = 84                      # Lo-fi 的慢速
BEAT = 60 / BPM
NB = 26                       # 全片 26 拍
DUR = NB * BEAT               # 約 18.6 秒
V.DUR = DUR                   # 讓 V.Mix 用同一個長度
T2, T3, T4 = 4 * BEAT, 18 * BEAT, 23 * BEAT   # 換場（月曆、登錄一次就好嗎、收尾）
WK = '一二三四五六日'


def _txt(s):
    return htm.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def fetch():
    s = urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8')
    upd = re.search(r'最後更新 (?:<!--lm-->)?(\d{4})-(\d\d)-(\d\d)', s)
    if not upd:
        sys.exit('頁尾找不到「最後更新」日期')
    today = dt.date(*map(int, upd.groups()))
    if os.environ.get('MONTH'):
        y, m = map(int, os.environ['MONTH'].split('-'))
    else:
        y, m = (today.year, today.month) if today.day < 15 else (
            (today.year + 1, 1) if today.month == 12 else (today.year, today.month + 1))
    i = s.find('全部的登錄活動</h2>')
    tb = s[i:s.find('</table>', i)]
    rows = []
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', tb, re.S):
        td = [_txt(x) for x in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
        if len(td) == 5:
            rows.append(dict(zip(('card', 'item', 'rule', 'next', 'quota'), td)))
    if len(rows) < 6:
        sys.exit('「全部的登錄活動」表的格式和預期不同，請先看頁面')
    # 各檔的資格（「逐張怎麼登錄」那段：<b>加碼名。</b>…資格：當月／當季／活動期間…）
    k = s.find('逐張怎麼登錄</h2>')
    det = s[k:s.find('常見問題</h2>', k)]
    qual = {}
    for h3, body in re.findall(r'<h3>(.*?)</h3>(.*?)(?=<h3>|$)', det, re.S):
        for it, rest in re.findall(r'<li><b>(.*?)。</b>(.*?)</li>', body, re.S):
            q = re.search(r'資格：([^，。]+)', _txt(rest))
            qual[(_txt(h3), _txt(it))] = q.group(1) if q else None
    days, skipped = {}, []
    for r in rows:
        nx = re.match(r'(\d+)/(\d+)（(.)）\s*(\d\d:\d\d)?', r['next'])
        if not nx or int(nx.group(1)) != m:
            continue
        d = int(nx.group(2))
        if WK[calendar.weekday(y, m, d)] != nx.group(3):
            sys.exit(f'{m}/{d} 的星期和頁面寫的（{nx.group(3)}）不一致，請先看頁面')
        if '非日本' in r['item']:
            skipped.append({'day': d, **r})
            continue
        q = qual.get((r['card'], r['item']))
        if not q:
            sys.exit(f'找不到 {r["card"]}「{r["item"]}」的資格，請先看頁面')
        kind = 'month' if q.startswith('當月') else 'once' if (q.startswith('當季') or q.startswith('活動期間')) else None
        if not kind:
            sys.exit(f'{r["card"]}「{r["item"]}」的資格「{q}」不在預期的三種裡')
        note = ''
        wk = re.match(r'每週(.) ', r['rule'])
        if wk:
            note = f'每週{wk.group(1)}都放新名額'
        elif '額滿提前關閉' in r['rule']:
            note = '額滿提前關閉'
        quota = re.sub(r'（每月（每季 [\d,]+））$', '（每月）', r['quota'])
        days.setdefault(d, []).append({'card': r['card'], 'item': r['item'], 'time': nx.group(4) or '',
                                       'quota': quota, 'note': note, 'kind': kind})
    if len(days) < 3:
        sys.exit(f'{m} 月只找到 {len(days)} 天有開放登錄，頁面可能還沒更新到這個月')
    items = [x for d in days.values() for x in d]
    month_cards = [x for x in items if x['kind'] == 'month']
    once_cards = {}
    for x in items:
        if x['kind'] == 'once':
            once_cards[x['card']] = once_cards.get(x['card'], 0) + 1
    if not month_cards or not once_cards:
        sys.exit('「每月重登」或「登過就不用」其中一邊是空的，畫面要改')
    q_start = (m - 1) // 3 * 3 + 1
    prev = [mm for mm in range(q_start, m)]
    return {'year': y, 'month': m, 'today': today.isoformat(),
            'days': [{'day': d, 'wk': WK[calendar.weekday(y, m, d)], 'items': days[d]} for d in sorted(days)],
            'month_items': [{'card': x['card'], 'item': x['item']} for x in month_cards],
            'once_cards': [{'card': c, 'n': n} for c, n in once_cards.items()],
            'prev_months': prev,
            'skipped': [{'day': x['day'], 'card': x['card'], 'item': x['item']} for x in skipped],
            'first_wd': calendar.weekday(y, m, 1), 'ndays': calendar.monthrange(y, m)[1]}


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#fbf3e4}
body{font-family:"PingFang TC","Noto Sans TC",sans-serif;color:#5a3d2b;-webkit-font-smoothing:antialiased}
.hn{font-family:"Huninn","PingFang TC",sans-serif;font-weight:400}
#bg{position:absolute;inset:-120px;background:
 linear-gradient(#efe2cc 2px,transparent 2px) 0 0/60px 60px,
 linear-gradient(90deg,#efe2cc 2px,transparent 2px) 0 0/60px 60px,#fbf3e4}
.sc{position:absolute;inset:0;transform-origin:540px 860px;opacity:0}
.ab{position:absolute;will-change:transform}
.stk svg{width:100%;height:auto;display:block}
.sh{filter:drop-shadow(0 10px 0 rgba(90,61,43,.12))}
.pill{display:inline-block;background:#5a3d2b;color:#fbf3e4;border-radius:999px;padding:16px 42px;font-size:50px}
/* 開場 */
#k1{left:0;width:1080px;top:236px;text-align:center}
#st1{left:340px;top:330px;width:400px}
#st1b{left:700px;top:470px;width:210px}
#h1{left:0;width:1080px;top:760px;text-align:center;font-size:84px}
#num{left:0;width:1080px;top:850px;text-align:center;color:#e8553e;font-size:300px;line-height:1;text-shadow:0 12px 0 #ffd0c4}
#num small{font-size:120px;margin-left:10px;color:#5a3d2b;text-shadow:none}
#sub1{left:0;width:1080px;top:1175px;text-align:center;font-size:52px;font-weight:800;color:#8a6a55}
#q1{left:0;width:1080px;top:1280px;text-align:center}
#q1 span{display:inline-block;background:#ffe48a;border:5px solid #5a3d2b;border-radius:30px;padding:14px 44px;font-size:62px;transform:rotate(-3deg)}
/* 月曆 */
#t2{left:75px;top:215px;font-size:76px}
#t2 small{font-size:40px;color:#8a6a55;margin-left:14px}
#cal{left:75px;top:320px;width:840px;background:#fff;border:5px solid #5a3d2b;border-radius:30px;
 box-shadow:0 12px 0 #ead9c4;padding:14px 0 10px;overflow:visible}
#cal .wh,#cal .wr{display:flex}
#cal .wh div{width:120px;text-align:center;font-size:34px;font-weight:800;color:#8a6a55;height:50px}
#cal .wh div:nth-child(6),#cal .wh div:nth-child(7){color:#e8553e}
.cell{width:120px;height:84px;position:relative;font-size:38px;font-weight:700;text-align:center;line-height:84px;color:#5a3d2b}
.cell.we{color:#e8553e}
.cell .ring{position:absolute;left:19px;top:1px;width:82px;height:82px;border-radius:50%;background:#ffe48a;
 border:5px solid #e8553e;transform:scale(0)}
.cell b{position:relative;font-weight:800}
.cell .dot{position:absolute;left:53px;top:70px;width:14px;height:14px;border-radius:50%;background:#7fb3e0;transform:scale(0)}
.note{left:80px;width:830px;top:905px;border:5px solid #5a3d2b;border-radius:18px;padding:26px 34px 28px;
 box-shadow:0 12px 0 rgba(90,61,43,.15);opacity:0}
.note .tape{position:absolute;left:340px;top:-26px;width:180px;height:48px;background:rgba(255,255,255,.65);
 border:3px dashed rgba(90,61,43,.35);transform:rotate(-4deg)}
.note .dd{font-size:64px;line-height:1.1}
.note .dd small{font-size:42px;margin-left:8px;color:#8a6a55}
.note .it{margin-top:14px;padding-top:14px;border-top:4px dashed rgba(90,61,43,.25)}
.note .it:first-of-type{border-top:0;padding-top:0}
.note .c{font-size:40px;font-weight:800}
.note .c i{font-style:normal;display:inline-block;background:#5a3d2b;color:#fff;border-radius:12px;padding:2px 14px;
 font-size:36px;margin-right:14px;vertical-align:4px}
.note .n{font-size:42px;margin-top:4px;color:#e8553e;font-weight:800;white-space:nowrap}
.note .q{font-size:30px;margin-top:4px;color:#8a6a55;font-weight:700}
.note .stk{position:absolute;right:20px;bottom:-30px;width:170px}
/* 登錄一次就好嗎 */
#stamp{left:0;width:1080px;top:240px;text-align:center}
#stamp span{display:inline-block;background:#e8553e;color:#fff;border:7px solid #5a3d2b;border-radius:28px;
 padding:18px 50px;font-size:88px;box-shadow:0 14px 0 #5a3d2b}
.bx{left:70px;width:860px;background:#fff;border:5px solid #5a3d2b;border-radius:34px;padding:24px 36px 28px;box-shadow:0 10px 0 #ead9c4}
.bx h3{font-family:"Huninn",sans-serif;font-weight:400;font-size:56px}
.bx h3 em{font-style:normal;color:#e8553e}
.bx p{font-size:44px;font-weight:800;margin-top:12px;line-height:1.3}
#leg{left:80px;width:830px;top:838px;font-size:32px;font-weight:700;color:#8a6a55}
#leg i{display:inline-block;width:18px;height:18px;border-radius:50%;background:#7fb3e0;margin-right:12px;vertical-align:2px}
.bx p small{display:block;font-size:34px;color:#8a6a55;font-weight:700}
/* 收尾 */
#st4{left:340px;top:330px;width:400px}
#brand{left:0;width:1080px;top:740px;text-align:center;font-size:84px}
#url{left:0;width:1080px;top:860px;text-align:center}
#url span{display:inline-block;background:#e8553e;color:#fff;border:6px solid #5a3d2b;border-radius:999px;
 padding:20px 60px;font-size:92px;box-shadow:0 12px 0 #5a3d2b}
#srch{left:0;width:1080px;top:1060px;text-align:center;font-size:52px;font-weight:800}
#tiny{left:80px;width:850px;top:1160px;text-align:center;font-size:29px;line-height:1.6;color:#8a6a55;font-weight:600}
"""

JS = r"""
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-cl(x),3);
const eb=x=>{x=cl(x);const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
function tf(el,x,y,s,r,o){el.style.transform=`translate(${x}px,${y}px) scale(${s}) rotate(${r||0}deg)`;if(o!==undefined)el.style.opacity=o}
function scene(id,a,b,t){const el=$(id);const i=eo((t-a)/.3),o=b<99?1-eo((t-b+.05)/.28):1;
 const v=t<a-.01||t>b+.3?0:Math.min(i,o);el.style.opacity=v;
 el.style.transform=`translateY(${(1-i)*50}px) scale(${1-(1-o)*.06})`;}
function fit(){document.querySelectorAll('.note .n').forEach(n=>{let f=42;while(n.scrollWidth>n.clientWidth&&f>28){f-=1;n.style.fontSize=f+'px'}})}
let _fit=0;
function render(t){if(!_fit){fit();_fit=1}
 $('bg').style.transform=`translate(${-(t*6)%60}px,${-(t*4)%60}px)`;
 scene('s1',0,D.T2,t);scene('s2',D.T2,D.T3,t);scene('s3',D.T3,D.T4,t);scene('s4',D.T4,99,t);
 // 開場
 tf($('k1'),0,(1-eb(t/.5))*-60,1,0,cl(t/.3));
 tf($('st1'),0,(1-eb((t-.15)/.6))*120+Math.sin(t*2.4)*8,.6+.4*eb((t-.15)/.6),Math.sin(t*1.7)*3,cl((t-.15)/.2));
 tf($('st1b'),0,Math.sin(t*2+1)*10,eb((t-.45)/.5),8+Math.sin(t*1.3)*4,cl((t-.45)/.2));
 tf($('h1'),0,(1-eo((t-.4)/.4))*40,1,0,cl((t-.4)/.3));
 const L=D.LAND, p=cl((t-.7)/(L-.7));
 $('nv').textContent=Math.round(D.top*eo(p));
 tf($('num'),0,0,t<L?.85+.15*p:1+.18*Math.exp(-(t-L)*7)*Math.cos((t-L)*18),0,cl((t-.6)/.2));
 tf($('sub1'),0,(1-eo((t-L)/.4))*30,1,0,cl((t-L)/.3));
 tf($('q1'),0,0,eb((t-L-.35)/.5),0,cl((t-L-.35)/.2));
 // 月曆
 tf($('leg'),0,0,1,0,cl((t-D.R[0]-.5)/.3));
 tf($('t2'),(1-eo((t-D.T2)/.4))*-80,0,1,0,cl((t-D.T2)/.3));
 tf($('cal'),0,(1-eb((t-D.T2-.1)/.6))*120,1,0,cl((t-D.T2-.1)/.25));
 D.days.forEach((d,i)=>{
  const R=D.R[i], N=i+1<D.R.length?D.R[i+1]:D.T3+.5;
  const c=$('c'+d.day).querySelector('.ring');c.style.transform=`scale(${eb((t-R)/.4)})`;
  const n=$('n'+i);const a=eb((t-R)/.45), x=eo((t-N+.05)/.3);
  n.style.opacity=t<R?0:(t>N+.3?0:1);
  tf(n,-x*1150,(1-a)*90,.85+.15*a,(i%2?2.2:-2.2)*(1-x*.5),undefined);
 });
 D.wdots.forEach(dd=>{const e=$('c'+dd).querySelector('.dot');e.style.transform=`scale(${eb((t-D.R[0]-.5)/.4)})`});
 // 登錄一次就好嗎
 tf($('stamp'),0,0,1+.6*(1-eb((t-D.T3)/.35)),-3,cl((t-D.T3)/.12));
 tf($('b1'),(1-eo((t-D.T3-.35)/.4))*-900,0,1,-1,1);
 tf($('b2'),(1-eo((t-D.T3-.75)/.4))*900,0,1,1,1);
 // 收尾
 tf($('st4'),0,(1-eb((t-D.T4)/.6))*-100+Math.sin(t*2)*8,1,0,cl((t-D.T4)/.2));
 tf($('brand'),0,0,eb((t-D.T4-.15)/.4),0,cl((t-D.T4-.15)/.2));
 tf($('url'),0,0,eb((t-D.T4-.3)/.45),-2,cl((t-D.T4-.3)/.2));
 tf($('srch'),0,(1-eo((t-D.T4-.45)/.4))*30,1,0,cl((t-D.T4-.45)/.3));
 tf($('tiny'),0,0,1,0,cl((t-D.T4-.6)/.3));
}
"""

COLORS = ['#ffe8a3', '#cfe6ff', '#ffd6d0', '#d6f0d8', '#ffdcb5', '#e6dcff']


def stk_for(items):
    s = ' '.join(x['item'] for x in items)
    return 'iccard' if '交通卡' in s else 'plane' if ('航' in s or 'Trip' in s) else 'card'


def build_html(d):
    e = htm.escape
    m = d['month']
    nd = len(d['days'])
    R = [T2 + BEAT * (1 + 2.5 * i) for i in range(nd)]
    land = 1.6
    # 月曆格子（週一開始，和頁上一樣）
    cells, wd = [], d['first_wd']
    lead = [''] * wd
    nums = lead + list(range(1, d['ndays'] + 1))
    nums += [''] * (-len(nums) % 7)
    weekly = [x for dd in d['days'] for x in dd['items'] if x['note'].startswith('每週')]
    wdots = []
    if weekly:
        wk_idx = WK.index(re.match(r'每週(.)', weekly[0]['note']).group(1))
        first = d['days'][0]['day']
        wdots = [n for n in range(first + 7, d['ndays'] + 1, 7) if calendar.weekday(d['year'], m, n) == wk_idx]
    rows = ''
    for r0 in range(0, len(nums), 7):
        rows += '<div class="wr">'
        for k, n in enumerate(nums[r0:r0 + 7]):
            cid = f' id="c{n}"' if n else ''
            rows += (f'<div class="cell{" we" if k >= 5 else ""}"{cid}><div class="ring"></div>'
                     f'<b>{n}</b>{"<div class=dot></div>" if n else ""}</div>')
        rows += '</div>'
    cal = (f'<div id="cal" class="ab"><div class="wh">{"".join(f"<div>{w}</div>" for w in WK)}</div>{rows}</div>')
    notes = ''
    for i, dd in enumerate(d['days']):
        its = ''
        for x in dd['items']:
            tm = f'<i>{e(x["time"])}</i>' if x['time'] else ''
            extra = f'名額 {e(x["quota"])}' + (f'・{e(x["note"])}' if x['note'] else '')
            its += (f'<div class="it"><div class="c">{tm}{e(x["card"])}</div><div class="n">{e(x["item"])}</div>'
                    f'<div class="q">{extra}</div></div>')
        notes += (f'<div id="n{i}" class="ab note" style="background:{COLORS[i % len(COLORS)]}"><div class="tape"></div>'
                  f'<div class="dd hn">{m}/{dd["day"]}<small>（{dd["wk"]}）</small></div>{its}'
                  f'<div class="stk sh">{V._svg(stk_for(dd["items"]))}</div></div>')
    s1 = (f'<div id="s1" class="sc"><div id="k1" class="ab"><span class="pill hn">{m} 月信用卡加碼登錄</span></div>'
          f'<div id="st1" class="ab stk sh">{V._svg("calendar")}</div>'
          f'<div id="st1b" class="ab stk sh">{V._svg("card")}</div>'
          f'<div id="h1" class="ab hn">{m} 月這幾天要搶登錄</div>'
          f'<div id="num" class="ab hn"><span id="nv">0</span><small>天</small></div>'
          f'<div id="sub1" class="ab">登錄時間、名額各家不同</div>'
          f'<div id="q1" class="ab"><span class="hn">沒登錄只剩基本回饋</span></div></div>')
    s2 = (f'<div id="s2" class="sc"><div id="t2" class="ab hn">{m} 月登錄日曆<small>{d["year"]}</small></div>'
          f'{cal}' + (f'<div id="leg" class="ab"><i></i>{e(weekly[0]["card"])}{e(weekly[0]["note"])}</div>' if wdots else '')
          + f'{notes}</div>')
    once = ''.join(f'<p>{e(x["card"])}' + (f' {x["n"]} 檔' if x['n'] > 1 else '') + '</p>' for x in d['once_cards'])
    monthly = ''.join(f'<p>{e(x["card"])}<small>{e(x["item"])}</small></p>' for x in d['month_items'])
    pm = '、'.join(str(x) for x in d['prev_months'])
    once_h = f'{pm} 月登過就<em>不用再登</em>' if pm else '這一季登一次就好'
    s3 = (f'<div id="s3" class="sc"><div id="stamp" class="ab"><span class="hn">登錄一次就好嗎？</span></div>'
          f'<div id="b1" class="ab bx" style="top:470px"><h3>每個月<em>都要重登</em></h3>{monthly}</div>'
          f'<div id="b2" class="ab bx" style="top:{470 + 150 + 112 * len(d["month_items"]) + 40}px"><h3>{once_h}</h3>'
          f'{once}<p><small>當季或活動期間登錄一次即可</small></p></div></div>')
    sk = '、'.join(f'{x["card"]} {m}/{x["day"]}「{x["item"]}」' for x in d['skipped'])
    s4 = (f'<div id="s4" class="sc"><div id="st4" class="ab stk sh">{V._svg("notebook")}</div>'
          f'<div id="brand" class="ab hn">日本旅遊小卡</div>'
          f'<div id="url" class="ab"><span class="hn">jptripcard.com</span></div>'
          f'<div id="srch" class="ab">各卡登錄時間、名額與入口</div>'
          f'<div id="tiny" class="ab">日期照官方公布的規則推算，銀行臨時改期或提前額滿都有可能'
          + (f'<br>{e(sk)}不含日本，沒列' if sk and '非日本' not in sk else f'<br>{e(sk)}沒列' if sk else '')
          + '<br>以各發卡行公告為準</div></div>')
    D = {'T2': T2, 'T3': T3, 'T4': T4, 'LAND': land, 'top': nd, 'R': R,
         'days': [{'day': x['day']} for x in d['days']], 'wdots': wdots}
    page = ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Huninn&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body><div id="bg"></div>{s1}{s2}{s3}{s4}'
            f'<script>window.D={json.dumps(D)};{JS}</script></body></html>')
    return page, R, land


# ─────────────── Lo-fi 配樂 ───────────────
def make_music_lofi(path, R, land):
    """Lo-fi：84 BPM、搖擺的 8 分音符、C 大調 Fmaj9｜Em7｜Dm9｜G13 的下行進行（IV–iii–ii–V）。
    電鋼琴長和弦（兩支略為走音的疊在一起，像錄音帶）、圓滑的正弦貝斯、悶悶的大鼓和帶殘響的小鼓、
    很輕的唱片雜音；開場只有電鋼琴，月曆出來時鼓組進場，每圈一天就響一顆鐘琴；收尾鼓停、留和弦。"""
    SR = V.SR
    rng = np.random.default_rng(11)
    M = V.Mix()
    bar = 4 * BEAT
    sw = .2 * BEAT / 2  # 搖擺

    def at(b, e8):
        return b * bar + e8 * BEAT / 2 + (sw if e8 % 2 else 0)

    prog = [(41, [57, 60, 64, 67]), (40, [55, 59, 62, 67]), (38, [57, 60, 62, 65]), (43, [53, 57, 59, 64])]
    nbar = int(np.ceil(DUR / bar))
    # 電鋼琴：每小節一個長和弦，輕輕撥開，第 3 拍後半再點一次
    for b in range(nbar):
        root, ch = prog[b % 4]
        for j, mm in enumerate(ch):
            for det, pan in ((0, -.3), (-.12, .3)):
                sig = V._ep(mm + det, bar * .95)
                M.st(sig, b * bar + .018 * j, .07, pan=pan, rv=.35)
        if b * bar + 2.5 * BEAT < T4 + BEAT:
            for j, mm in enumerate(ch[1:]):
                M.st(V._ep(mm + 12, BEAT * .9), at(b, 5) + .012 * j, .025, pan=.2, rv=.4)
        # 貝斯：第 1 拍與第 2 拍後半
        for e8, ln, nn in ((0, 3, root), (3, 2, root), (6, 2, root + 7)):
            if b * bar + e8 * BEAT / 2 > T4 + 2 * BEAT:
                continue
            t = V._tt(ln * BEAT / 2)
            sig = np.sin(2 * np.pi * V._hz(nn) * t) * np.minimum(1, t / .01) * np.clip((ln * BEAT / 2 - t) / .05, 0, 1)
            sig += .25 * np.sin(4 * np.pi * V._hz(nn) * t) * np.exp(-t * 6)
            M.st(sig, at(b, e8), .42)
    # 鼓組：月曆出來（T2）才進，收尾（T4）停
    kick = V._hit(110, 45, 30, .35, 9)
    snare = V._sum(V._fft_filter(V._nz(.25, rng, lo=600, hi=5000, d=14), hi=4000) * .9, V._hit(190, 170, 20, .15, 28) * .4)
    hat = V._fft_filter(V._nz(.05, rng, lo=6000, d=70), hi=9000)
    for b in range(nbar):
        for e8 in range(8):
            tt = at(b, e8)
            if tt < T2 - .01 or tt >= T4:
                continue
            if e8 in (0, 5) or (e8 == 3 and b % 2):
                M.st(kick, tt, .75)
            if e8 in (2, 6):
                M.st(snare, tt, .32, rv=.7)
            M.st(hat, tt, .05 if e8 % 2 else .08, pan=.35)
    # 每圈一天：鐘琴兩顆音（和弦內音，往上走）
    mel = [(72, 76), (74, 79), (76, 81), (79, 84), (81, 86), (84, 88)]
    for i, r in enumerate(R):
        a, c = mel[i % len(mel)]
        M.st(V._glock(a, 1.2), r, .14, pan=-.2, rv=.6)
        M.st(V._glock(c, 1.2), r + BEAT / 2, .1, pan=.2, rv=.6)
    # 數字落地、換場：輕輕的鐘琴和弦
    for tt, notes in ((land, (72, 76, 79)), (T3, (77, 81, 84)), (T4, (72, 76, 79, 84))):
        for j, mm in enumerate(notes):
            M.st(V._glock(mm, 1.6), tt + .03 * j, .09, rv=.7)
    # 唱片雜音：稀疏的爆音加很輕的嘶聲
    N = M.N
    crk = np.zeros(N)
    idx = rng.integers(0, N, int(DUR * 9))
    crk[idx] = rng.uniform(-1, 1, len(idx))
    crk = V._fft_filter(crk, lo=1200, hi=7000) * 2.5
    hiss = V._fft_filter(rng.uniform(-1, 1, N), lo=3000, hi=8000) * .006
    M.L += crk * .5 + hiss
    M.R += crk * .5 + hiss
    # Lo-fi 的悶：整體再往下壓一點高頻
    M.L = V._fft_filter(M.L, hi=5200)
    M.R = V._fft_filter(M.R, hi=5200)
    M.write(path, decay=.6, gain=float(os.environ.get('LOFI_GAIN', '.57')))


def main():
    from playwright.sync_api import sync_playwright
    d = fetch()
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src, R, land = build_html(d)
    keep = os.environ.get('KEEP_FRAMES')
    mp4 = os.path.join(OUT, f'register-{d["year"]}-{d["month"]:02d}-lofi.mp4')
    with tempfile.TemporaryDirectory() as tmp:
        hf = os.path.join(tmp, 'v.html')
        open(hf, 'w', encoding='utf-8').write(src)
        wav = os.path.join(tmp, 'm.wav')
        make_music_lofi(wav, R, land)
        ff = subprocess.Popen(
            ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
             '-c:v', 'png', '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4],
            stdin=subprocess.PIPE)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=V.base._chrome())
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
            pg.goto('file://' + hf)
            pg.evaluate('document.fonts.ready')
            if not pg.evaluate('document.fonts.check(\'40px "Huninn"\')'):
                sys.exit('Huninn 字型沒有載入（需要網路連到 Google Fonts）')
            for f in range(int(DUR * FPS)):
                t = f / FPS
                pg.evaluate(f'render({t})')
                png = pg.screenshot(type='png')
                ff.stdin.write(png)
                if keep and any(abs(t - float(x)) < .5 / FPS for x in keep.split(',')):
                    open(os.path.join(V.keep_dir(), f'{t:05.2f}.png'), 'wb').write(png)
            b.close()
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit('ffmpeg 合成失敗')
    print(mp4)
    for x in d['days']:
        print(f'{d["month"]}/{x["day"]}（{x["wk"]}）' + '；'.join(f'{i["time"]} {i["card"]} {i["item"]} {i["quota"]} {i["note"]}' for i in x['items']))
    print('每月重登：', [x['card'] + ' ' + x['item'] for x in d['month_items']], '｜登過就不用：', d['once_cards'],
          '｜沒列：', d['skipped'])


if __name__ == '__main__':
    main()
