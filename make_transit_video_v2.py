"""交通卡儲值短影音 第二版（15 秒、直式 1080×1920、動態字卡＋手繪貼紙＋原創配樂）。

數字不在這裡算：沿用 make_transit_video.fetch() 直接讀線上 /japan-transit-card/
「每儲 ¥10,000 約付」那張表，所以影片和網站永遠是同一份試算。
畫面：一份 HTML，render(t) 依時間決定每個元素的位置與透明度，Playwright 逐格截圖（30fps）。
配樂：numpy 自己合成（破關風／City Pop／和風／日系可愛，立體聲，場景切換對齊拍點），沒有使用任何外部音檔。
用法：python3 make_transit_video_v2.py [輸出資料夾]
需要 Chrome、Playwright（Python）、numpy、ffmpeg。
"""
import html as htm
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

import make_transit_video as base

OUT = sys.argv[1] if len(sys.argv) > 1 else 'cards/threads/短影音-交通卡儲值'
W, H, FPS, DUR = 1080, 1920, 30, 15.0
BPM = 150  # 破關風的速度；換風格時場景切換點會跟著拍子重排
BEAT = 60 / BPM
# 場景切換點（秒），都落在拍點上
T_RANK, T_CAP, T_END = 8 * BEAT, 23 * BEAT, 31 * BEAT
# 開場數字落地的拍點
T_LAND = 4 * BEAT
SR = 44100


def _svg(name):
    s = open(f'illust/st/{name}.svg', encoding='utf-8').read()
    # 拿掉貼紙外框那張圓角底卡，讓插圖直接站在畫面上
    s = re.sub(r'<rect x="3" y="3" width="174" height="144"[^>]*/>', '', s, count=1)
    return s


def scene_data(d):
    cs = d['cards']
    caps = []
    for c in cs:
        m = re.search(r'約儲 ¥([\d,]+)', c['room'])
        if not m:
            continue
        pre = c['room'].split('；')[0] if '；' in c['room'] else ''
        caps.append({'name': c['name'], 'yen': m.group(1),
                     'pre': pre, 'share': '和購物共用' in c['room']})
    return caps[:3]


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#fff8ec}
body{font-family:"PingFang TC","Noto Sans TC",sans-serif;color:#5a3d2b;-webkit-font-smoothing:antialiased}
.hn{font-family:"Huninn","PingFang TC",sans-serif;font-weight:400}
#bg{position:absolute;inset:-200px;background:
 radial-gradient(circle,#f3dcc0 3px,transparent 3.5px) 0 0/54px 54px,#fff8ec}
#burst{position:absolute;left:540px;top:930px;width:2400px;height:2400px;margin:-1200px 0 0 -1200px;
 background:repeating-conic-gradient(#ffe48a 0 9deg,transparent 9deg 18deg);border-radius:50%;
 -webkit-mask:radial-gradient(circle,#000 0,#000 30%,transparent 62%)}
.sc{position:absolute;inset:0;transform-origin:540px 900px}
.ab{position:absolute;will-change:transform}
.pill{display:inline-block;background:#5a3d2b;color:#fff8ec;border-radius:999px;
 padding:16px 40px;font-size:50px;letter-spacing:.02em}
.stk svg{width:100%;height:auto;display:block}
.sh{filter:drop-shadow(0 10px 0 rgba(90,61,43,.12))}
/* 開場 */
#k1{left:0;width:1080px;top:236px;text-align:center}
#st1{left:340px;top:350px;width:400px}
#st1b{left:690px;top:470px;width:230px}
#st1c{left:150px;top:500px;width:210px}
#h1{left:0;width:1080px;top:720px;text-align:center;font-size:104px;line-height:1.15}
#num{left:0;width:1080px;top:860px;text-align:center;color:#e8553e;font-size:300px;line-height:1;
 letter-spacing:-.02em;text-shadow:0 12px 0 #ffd0c4}
#num small{font-size:120px;margin-right:8px}
#sub1{left:0;width:1080px;top:1210px;text-align:center;font-size:52px;font-weight:800;color:#8a6a55}
#q1{left:0;width:1080px;top:1310px;text-align:center}
#q1 span{display:inline-block;background:#ffe48a;border:5px solid #5a3d2b;border-radius:30px;
 padding:14px 44px;font-size:64px;transform:rotate(-3deg)}
/* 排名 */
#t2{left:70px;width:860px;top:228px;font-size:76px;line-height:1.22}
#t2 em{font-style:normal;color:#e8553e}
.rw{left:60px;width:870px;height:150px}
.rk{position:absolute;left:0;top:22px;width:96px;height:96px;border-radius:50%;background:#fff;
 border:5px solid #5a3d2b;text-align:center;line-height:84px;font-size:58px}
.rw.g .rk{background:#ffe48a}
.nm{position:absolute;left:122px;top:6px;font-size:46px;font-weight:800;white-space:nowrap}
.br{position:absolute;left:122px;top:74px;height:58px;border-radius:29px;background:#ffd0c4;
 border:4px solid #5a3d2b;transform-origin:left center}
.rw.g .br{background:#e8553e}
.vl{position:absolute;top:70px;font-size:58px;white-space:nowrap;color:#5a3d2b}
.vl small{font-size:34px;margin-right:4px}
.rw.g .vl{color:#e8553e}
#crown{left:0;top:0;width:96px}
#base{left:60px;width:870px;top:1385px;font-size:40px;font-weight:700;color:#8a6a55;line-height:1.5;
 border-top:4px dashed #ead9c4;padding-top:22px}
#base b{color:#5a3d2b}
/* 上限 */
#stamp{left:0;width:1080px;top:250px;text-align:center}
#stamp span{display:inline-block;background:#e8553e;color:#fff;border:7px solid #5a3d2b;border-radius:28px;
 padding:20px 56px;font-size:110px;box-shadow:0 14px 0 #5a3d2b}
.cp{left:70px;width:860px;background:#fff;border:5px solid #5a3d2b;border-radius:34px;padding:26px 36px;
 box-shadow:0 10px 0 #ead9c4}
.cp b{display:block;font-size:46px;font-weight:800}
.cp .y{font-size:64px;color:#e8553e;margin-top:6px}
.cp .y small{font-size:40px;color:#5a3d2b;margin-left:6px}
.cp s{display:block;text-decoration:none;font-size:36px;font-weight:700;color:#8a6a55;margin-top:6px}
#reg{left:70px;width:860px;top:1290px;display:flex;align-items:center;gap:18px}
#reg .stk{width:180px;flex:0 0 180px}
#reg div.t{font-size:50px;line-height:1.3}
#reg div.t em{font-style:normal;color:#e8553e}
/* 收尾 */
#st4{left:0;top:330px;width:400px}
#brand{left:0;width:1080px;top:720px;text-align:center;font-size:84px}
#url{left:0;width:1080px;top:850px;text-align:center}
#url span{display:inline-block;background:#e8553e;color:#fff;border:6px solid #5a3d2b;border-radius:999px;
 padding:20px 60px;font-size:92px;box-shadow:0 12px 0 #5a3d2b;letter-spacing:.01em}
#srch{left:0;width:1080px;top:1050px;text-align:center;font-size:54px;font-weight:800}
#tiny{left:80px;width:850px;top:1200px;text-align:center;font-size:32px;line-height:1.65;color:#8a6a55;font-weight:600}
/* 轉場 */
#wipe{position:absolute;top:-300px;left:0;width:1500px;height:2520px;background:#ffe48a;
 border-left:16px solid #e8553e;transform-origin:center}
.cf{position:absolute;left:0;top:0;width:26px;height:16px;border-radius:4px}
"""

JS = r"""
const C=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const P=(t,a,b)=>C((t-a)/(b-a));
const oc=x=>1-Math.pow(1-x,3);
const ob=x=>{const c1=2.2,c3=c1+1;return x<=0?0:1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const oe=x=>x<=0?0:x>=1?1:Math.pow(2,-9*x)*Math.sin((x*10-.75)*2.0944)+1;
const $=id=>document.getElementById(id);
function T(el,{x=0,y=0,s=1,r=0,o=1}){el.style.transform=`translate(${x}px,${y}px) rotate(${r}deg) scale(${s})`;el.style.opacity=o}
function shake(t,t0,a=18,d=.35){const k=t-t0;if(k<0||k>d)return[0,0];const e=1-k/d;return[a*e*Math.sin(k*95),a*e*Math.cos(k*71)]}
function pop(t,t0,d=.45){return ob(P(t,t0,t0+d))}
function fmt(n){return Math.round(n).toLocaleString('en-US')}
function confetti(t,t0,group){
  for(const c of group){const k=t-t0;const el=c.el;
    if(k<0||k>1.6){el.style.opacity=0;continue}
    const x=c.x+c.vx*k, y=c.y+c.vy*k+900*k*k;
    el.style.opacity=k>1.2?(1.6-k)/.4:1;
    el.style.transform=`translate(${x}px,${y}px) rotate(${c.r+c.vr*k}deg) scaleY(${Math.cos(k*c.f)})`;}
}
function render(t){
  const D=window.D;
  // 背景：圓點慢慢斜移、放射光芒旋轉
  $('bg').style.transform=`translate(${(t*40)%54}px,${(t*40)%54}px)`;
  const bo = t<D.R ? .55*oc(P(t,.5,1.4)) : (t>=D.C && t<D.E ? 0 : (t>=D.E ? .45*oc(P(t,D.E+.2,D.E+.9)) : 0));
  $('burst').style.opacity=bo; $('burst').style.transform=`rotate(${t*14}deg)`;
  $('burst').style.top = t>=D.E? '820px':'1010px';
  // 每一場的可見度
  const sc=[['s1',0,D.R],['s2',D.R,D.C],['s3',D.C,D.E],['s4',D.E,99]];
  for(const [id,a,b] of sc){$(id).style.display=(t>=a&&t<b)?'block':'none'}
  // 轉場：斜切色塊從右掃到左，中點換場
  const w=$('wipe'); let wv=-1;
  for(const tc of [D.R,D.C,D.E]){if(Math.abs(t-tc)<.2){wv=(t-(tc-.2))/.4}}
  if(wv<0){w.style.display='none'}else{w.style.display='block';
    w.style.transform=`translateX(${1300-wv*2800}px) skewX(-14deg)`}
  // 場景淡出時輕微放大（whip zoom）
  for(const [id,a,b] of sc){const el=$(id);const k=P(t,b-.22,b);const ki=1-P(t,a,a+.25);
    el.style.transform=`scale(${1+.18*k*k - (a>0?.06*ki:0)})`;}

  /* ── 1 開場 ── */
  if(t<D.R){
    T($('k1'),{y:-260*(1-ob(P(t,0,.4))),o:P(t,0,.12)});
    const s1=pop(t,.12,.5); T($('st1'),{s:s1,r:-8*(1-s1)+3*Math.sin(t*5),y:8*Math.sin(t*4)});
    const s1b=pop(t,.28,.45); T($('st1b'),{s:s1b,r:12+4*Math.sin(t*6+1),y:-10*Math.sin(t*4+1),o:C(s1b*3)});
    const s1c=pop(t,.36,.45); T($('st1c'),{s:s1c,r:-12+4*Math.sin(t*5+2),y:10*Math.sin(t*4+2),o:C(s1c*3)});
    T($('h1'),{s:pop(t,.45,.4),o:C(P(t,.45,.55))});
    // 數字跳動：0.55 秒起從 0 數到目標，D.L（拍點）落地衝擊
    const L=D.L; const k=oc(P(t,.55,L)); $('nv').textContent=fmt(D.top*k);
    const land=t>=L?1+.28*(1-oc(P(t,L,L+.35))):(.8+.2*P(t,.55,L));
    const [sx,sy]=shake(t,L,26,.4);
    T($('num'),{s:land,x:sx,y:sy,o:C(P(t,.55,.7))});
    T($('sub1'),{y:40*(1-oc(P(t,L+.15,L+.45))),o:P(t,L+.15,L+.35)});
    const q=pop(t,L+.55,.4); T($('q1'),{s:q,r:2*Math.sin(t*9),o:C(q*3)});
    confetti(t,D.L,D.cf1);
  }
  /* ── 2 排名：從第 6 名往上揭曉，第 1 名最後落地 ── */
  else if(t<D.C){
    T($('t2'),{x:-900*(1-ob(P(t,D.R+.05,D.R+.45)))});
    const n=D.rows.length;
    for(let i=0;i<n;i++){
      const row=D.rows[i]; const el=$('r'+i);
      const t0=D.rowT[i];
      const a=pop(t,t0,.35);
      const [sx,sy]= i===0?shake(t,t0+.45,22,.4):[0,0];
      T(el,{x:sx+(1-a)*120,y:sy,o:C(P(t,t0,t0+.12))});
      const g=oe(P(t,t0+.08,t0+.75));
      el.querySelector('.br').style.transform=`scaleX(${Math.max(.001,g)})`;
      const vl=el.querySelector('.vl');
      vl.style.left=(122+row.w*g+18)+'px';
      vl.querySelector('i').textContent=fmt(row.save*oc(P(t,t0+.08,t0+.6)));
      if(i===0){const p=t>=t0+.45?1+.08*Math.sin((t-t0)*8)*Math.exp(-(t-t0-.45)*1.2):1;
        el.querySelector('.br').style.transform+=` scaleY(${p})`;}
    }
    const cr=$('crown'); const ct=D.rowT[0]+.45;
    const nw=$('r0').querySelector('.nm').offsetWidth;
    T(cr,{x:60+122+nw+14,y:D.rowY0-14-300*(1-ob(P(t,ct,ct+.4))),r:12+4*Math.sin(t*6),o:C(P(t,ct,ct+.1))});
    T($('base'),{y:30*(1-oc(P(t,D.rowT[0]+.9,D.rowT[0]+1.2))),o:P(t,D.rowT[0]+.9,D.rowT[0]+1.1)});
    confetti(t,D.rowT[0]+.45,D.cf2);
  }
  /* ── 3 上限 ── */
  else if(t<D.E){
    const k=P(t,D.C+.05,D.C+.3); const [sx,sy]=shake(t,D.C+.3,24,.35);
    T($('stamp'),{s:k<1?3-2*k*k:1,r:-6,x:sx,y:sy,o:C(k*4)});
    D.caps.forEach((c,i)=>{const t0=D.C+.55+i*.3;const a=ob(P(t,t0,t0+.45));
      T($('cp'+i),{x:(1-a)*1100,r:(1-a)*6});});
    const rg=pop(t,D.C+1.55,.45); T($('reg'),{s:rg,o:C(rg*3)});
    T($('reg').querySelector('.stk'),{r:8*Math.sin(t*7)});
  }
  /* ── 4 收尾 ── */
  else{
    // 電車從左邊開進來停在中間
    const a=oc(P(t,D.E+.05,D.E+.75));
    T($('st4'),{x:-420+(340+420)*a,y:4*Math.sin(t*30)*(1-a)+6*Math.sin(t*4)});
    T($('brand'),{s:pop(t,D.E+.3,.4),o:C(P(t,D.E+.3,D.E+.4))});
    const u=pop(t,D.E+.5,.45); const [ux,uy]=shake(t,D.E+.95,10,.3);
    T($('url'),{s:u*(1+.03*Math.sin((t-D.E)*6)),x:ux,y:uy,o:C(u*3)});
    T($('srch'),{y:30*(1-oc(P(t,D.E+.8,D.E+1.1))),o:P(t,D.E+.8,D.E+1.0)});
    T($('tiny'),{o:P(t,D.E+1.0,D.E+1.25)});
  }
}
"""


def build_html(d, caps):
    e = htm.escape
    cs = d['cards']
    top = cs[0]
    rnd = random.Random(7)
    cols = ['#e8553e', '#ffe48a', '#9fd3c7', '#f6a5ad', '#6bb38a', '#a5c8f0']

    def burst(n, x, y):
        out = []
        for _ in range(n):
            ang = rnd.uniform(-math.pi, 0)
            sp = rnd.uniform(500, 1300)
            out.append({'x': x, 'y': y, 'vx': math.cos(ang) * sp, 'vy': math.sin(ang) * sp - 200,
                        'r': rnd.uniform(0, 360), 'vr': rnd.uniform(-720, 720),
                        'f': rnd.uniform(6, 16), 'c': rnd.choice(cols)})
        return out

    # 排名列的位置：固定版面，從 y=420 開始每列 150px
    y0, rh = 460, 150
    mx = max(c['save'] for c in cs) or 1
    rows = [{'save': c['save'], 'w': max(60, round(c['save'] / mx * 520))} for c in cs]
    n = len(cs)
    # 第 6 名先出，每 0.45 秒一名；第 1 名多停半拍製造懸念，落在拍點上
    rowT = [0] * n
    for k, i in enumerate(range(n - 1, 0, -1)):
        rowT[i] = T_RANK + (1 + k) * BEAT
    # 第 1 名多停一拍，衝擊（rowT+0.45）落在拍點上
    rowT[0] = T_RANK + (n + 1) * BEAT - 0.45
    cf1 = burst(36, 540, 1010)
    cf2 = burst(30, 700, y0 + 100)
    D = {'L': T_LAND, 'R': T_RANK, 'C': T_CAP, 'E': T_END, 'top': top['save'], 'rows': rows, 'rowT': rowT,
         'rowY0': y0, 'caps': caps, 'cf1': cf1, 'cf2': cf2}

    def cfdivs(g, tag):
        return ''.join(f'<div class="cf" id="{tag}{i}" style="background:{c["c"]}"></div>'
                       for i, c in enumerate(g))

    s1 = (f'<div id="s1" class="sc">'
          f'<div id="k1" class="ab"><span class="pill hn">iPhone 錢包儲 Suica ¥10,000</span></div>'
          f'<div id="st1c" class="ab stk sh">{_svg("phone")}</div>'
          f'<div id="st1" class="ab stk sh">{_svg("iccard")}</div>'
          f'<div id="st1b" class="ab stk sh">{_svg("yen")}</div>'
          f'<div id="h1" class="ab hn">刷對卡少付</div>'
          f'<div id="num" class="ab hn"><small>NT$</small><span id="nv">0</span></div>'
          f'<div id="sub1" class="ab">跟換日圓現鈔投現金比</div>'
          f'<div id="q1" class="ab"><span class="hn">是哪一張卡？</span></div>'
          f'{cfdivs(cf1, "a")}</div>')

    rw = ''
    for i, c in enumerate(cs):
        rw += (f'<div id="r{i}" class="ab rw{" g" if i == 0 else ""}" style="top:{y0 + i * rh}px">'
               f'<div class="rk hn">{i + 1}</div><div class="nm">{e(c["name"])}</div>'
               f'<div class="br" style="width:{rows[i]["w"]}px"></div>'
               f'<div class="vl hn"><small>省</small><i>0</i></div></div>')
    crown = ('<svg viewBox="0 0 110 80"><path d="M8 70 L14 22 L36 46 L55 10 L74 46 L96 22 L102 70 Z" '
             'fill="#ffe48a" stroke="#5a3d2b" stroke-width="6" stroke-linejoin="round"/>'
             '<circle cx="55" cy="10" r="7" fill="#e8553e" stroke="#5a3d2b" stroke-width="4"/>'
             '<circle cx="14" cy="22" r="6" fill="#9fd3c7" stroke="#5a3d2b" stroke-width="4"/>'
             '<circle cx="96" cy="22" r="6" fill="#9fd3c7" stroke="#5a3d2b" stroke-width="4"/></svg>')
    s2 = (f'<div id="s2" class="sc">'
          f'<div id="t2" class="ab hn">每儲 ¥10,000<br>比換現鈔<em>少付多少</em></div>{rw}'
          f'<div id="crown" class="ab">{crown}</div>'
          f'<div id="base" class="ab">單位 NT$。換現鈔投現金要付 <b>NT${d["cash"]:,}</b><br>'
          f'已含 {e(d["fee"])}% 國外交易手續費、扣掉回饋</div>'
          f'{cfdivs(cf2, "b")}</div>')

    cp = ''
    for i, c in enumerate(caps):
        extra = []
        if c['pre']:
            extra.append(e(c['pre']))
        if c['share']:
            extra.append('和購物共用額度')
        cp += (f'<div id="cp{i}" class="ab cp" style="top:{500 + i * 250}px"><b>{e(c["name"])}</b>'
               f'<div class="y hn">約儲 ¥{c["yen"]}<small>就用完</small></div>'
               + (f'<s>{"・".join(extra)}</s>' if extra else '') + '</div>')
    s3 = (f'<div id="s3" class="sc"><div id="stamp" class="ab"><span class="hn">加碼有上限！</span></div>{cp}'
          f'<div id="reg" class="ab"><div class="stk sh">{_svg("calendar")}</div>'
          f'<div class="t hn">而且{"每張都" if all(c["reg"] for c in cs) else "多數"}要<br><em>先登錄或設定</em></div></div></div>')

    s4 = (f'<div id="s4" class="sc"><div id="st4" class="ab stk sh">{_svg("subway")}</div>'
          f'<div id="brand" class="ab hn">日本旅遊小卡</div>'
          f'<div id="url" class="ab"><span class="hn">jptripcard.com</span></div>'
          f'<div id="srch" class="ab">搜尋「日本交通卡」看完整試算</div>'
          f'<div id="tiny" class="ab">{e(d["rate_date"])} 日圓中價 {e(d["rate"])} 試算，'
          f'國外交易手續費以 {e(d["fee"])}% 計<br>各行活動隨時調整，以發卡行官網公告為準</div></div>')

    js_cf = ('for(const [g,p] of [["cf1","a"],["cf2","b"]]) D[g].forEach((c,i)=>c.el=document.getElementById(p+i));')
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Huninn&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body><div id="bg"></div><div id="burst"></div>'
            f'{s1}{s2}{s3}{s4}<div id="wipe"></div>'
            f'<script>window.D={json.dumps(D, ensure_ascii=False)};{js_cf}{JS}</script></body></html>')


# ─────────────── 原創配樂 ───────────────

def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)



def _hz(m):
    return 440 * 2 ** ((m - 69) / 12)



def _noise(n, rng):
    return rng.uniform(-1, 1, n)


def _hp(x):
    return np.diff(x, prepend=0)



def _fft_filter(x, lo=None, hi=None):
    """用 FFT 做的高通／低通（沒有 scipy）。"""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    if hi:
        g *= 1 / (1 + (f / hi) ** 2)
    return np.fft.irfft(X * g, n)


def _conv(x, ir):
    n = len(x) + len(ir)
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]


def _saw(f, t, roll=10.0, kdecay=0.0, phase=0.0):
    """疊加合成的鋸齒波；roll 越小越暖，kdecay 讓高次泛音先消失（像濾波器關起來）。"""
    K = max(1, min(30, int(9000 / f)))
    s = np.zeros_like(t)
    for k in range(1, K + 1):
        a = np.exp(-k / roll) / k
        if kdecay:
            a = a * np.exp(-t * kdecay * k)
        s += a * np.sin(2 * np.pi * f * k * t + phase * k)
    return s



def _glock(m, dur=.6):
    """鐘琴：不諧和泛音，配殘響用，聽起來是亮晶晶不是電子遊戲。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = _hz(m)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 5) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 14)
         + .15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 30))
    return s * np.minimum(1, t / .0015)


def _marimba(m, dur=.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = _hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 9) + .3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 40)
    return s * np.minimum(1, t / .002)


def make_music(path, rowT, caps_n):
    """日系可愛風：140 BPM、D 大調，王道進行 IV△7–V7–iii7–vi7（J-pop 最常見的和弦進行）。
    鐘琴＋木琴主旋律、彈跳切分撥奏和弦、八度跳的低音、鈴鼓與沙鈴；換場用上行琶音，結尾停在 D△9。"""
    rng = np.random.default_rng(11)
    N = int(DUR * SR)
    six = BEAT / 4
    bar = 4 * BEAT
    T_FIN = 8 * bar            # 第 9 小節的第一拍：收尾和弦
    end = T_FIN
    tt_all = np.arange(N) / SR
    L = np.zeros(N)
    R = np.zeros(N)
    send = np.zeros(N)

    def st(sig, t0, g=1.0, pan=0.0, rv=0.0):
        i = int(t0 * SR)
        if i >= N or i < 0:
            return
        j = min(N, i + len(sig))
        x = sig[:j - i] * g
        L[i:j] += x * (1 - max(pan, 0))
        R[i:j] += x * (1 + min(pan, 0))
        if rv:
            send[i:j] += x * rv

    # 鼓：輕的大鼓、拍手、沙鈴、鈴鼓
    n = int(.2 * SR)
    t = np.arange(n) / SR
    kick = np.sin(2 * np.pi * np.cumsum(55 + 140 * np.exp(-t * 40)) / SR) * np.exp(-t * 14)
    n = int(.2 * SR)
    t = np.arange(n) / SR
    clap = sum(np.roll(_fft_filter(_noise(n, rng), lo=1200, hi=6000) * np.exp(-t * 28), int(d * SR))
               for d in (0, .008, .016)) * .8
    shk_n = int(.05 * SR)
    shk = _fft_filter(_noise(shk_n, rng), lo=6000) * _env(shk_n, .008, .015)
    tam_n = int(.15 * SR)
    tq = np.arange(tam_n) / SR
    tam = (_fft_filter(_noise(tam_n, rng), lo=7000) * .6
           + sum(np.sin(2 * np.pi * f * tq + rng.uniform(0, 6)) for f in (5300, 6900, 8100, 9700)) * .15
           ) * _env(tam_n, .002, .045)
    for b in range(int(end / BEAT)):
        tb = b * BEAT
        st(kick, tb, .8)
        if b % 2 == 1:
            st(clap, tb, .5, rv=.45)
        st(tam, tb + BEAT / 2, .22, pan=.35, rv=.1)
        for k in (1, 3):
            st(shk, tb + k * six, .12, pan=-.35)
    # 王道進行：IV△7  V7  iii7  vi7（D 大調：G△7 A7 F#m7 Bm7）
    prog = [(43, [66, 69, 71, 74, 78]), (45, [67, 69, 73, 76, 79]),
            (42, [64, 66, 69, 73, 76]), (47, [66, 69, 71, 74, 78])]
    c = 2 ** (10 / 1200)
    chordL = np.zeros(N)
    chordR = np.zeros(N)
    bass = np.zeros(N)
    for bi in range(int(end / bar)):
        root, ch = prog[bi % 4]
        t0 = bi * bar
        # 切分撥奏：16 分音符的 0、3、6、8、11、14 格（3-3-2 彈跳）
        for s16 in (0, 3, 6, 8, 11, 14):
            n = int(.32 * SR)
            t = np.arange(n) / SR
            env = np.exp(-t * 7) * np.minimum(1, t / .004)
            i = int((t0 + s16 * six) * SR)
            j = min(N, i + n)
            for m in ch:
                f = _hz(m)
                chordL[i:j] += ((_saw(f, t, roll=9, kdecay=1.5) + _saw(f / c, t, roll=9, kdecay=1.5, phase=.8))
                                * env)[:j - i]
                chordR[i:j] += ((_saw(f, t, roll=9, kdecay=1.5) + _saw(f * c, t, roll=9, kdecay=1.5, phase=1.6))
                                * env)[:j - i]
        # 低音：八分音符八度跳
        for k in range(8):
            tb = t0 + k * BEAT / 2
            nn = int(.17 * SR)
            tq = np.arange(nn) / SR
            f = _hz(root + (12 if k % 2 else 0))
            sg = (np.sin(2 * np.pi * f * tq) + .3 * np.sin(2 * np.pi * 2 * f * tq)) * _env(nn, .004, .07)
            i = int(tb * SR)
            j = min(N, i + nn)
            bass[i:j] += sg[:j - i]
    ph = (tt_all % BEAT) / BEAT
    pump = 1 - .5 * np.exp(-ph * BEAT / .07)
    chordL *= pump * .03
    chordR *= pump * .03
    bass *= .5
    L += chordL + bass
    R += chordR + bass
    send += (chordL + chordR) * .25
    # 主旋律：鐘琴＋低八度木琴，兩小節一句
    A = {0: 78, 2: 81, 4: 83, 6: 86, 7: 83, 8: 86, 10: 90, 12: 88, 14: 86,
         16: 85, 18: 83, 19: 81, 20: 76, 22: 81, 24: 85, 26: 88, 28: 86, 30: 85}
    Bp = {0: 85, 2: 81, 4: 78, 6: 81, 8: 85, 10: 88, 11: 86, 12: 85, 14: 81,
          16: 83, 18: 86, 19: 83, 20: 81, 22: 78, 24: 83, 26: 86, 28: 90, 30: 88}
    for ph_ in range(0, int(end / bar), 2):
        pat = A if (ph_ // 2) % 2 == 0 else Bp
        for s16, m in pat.items():
            tb = ph_ * bar + s16 * six
            if tb >= end:
                break
            st(_glock(m, .6), tb, .2, pan=.15, rv=.45)
            st(_marimba(m - 12, .35), tb, .22, pan=-.15, rv=.15)
    # 收尾：D△9 長音＋鐘琴上行琶音
    n = int((DUR - T_FIN) * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / .01) * np.exp(-t * 1.2)
    for m in (62, 66, 69, 73, 76):
        f = _hz(m)
        sg = (_saw(f, t, roll=6) + _saw(f * c, t, roll=6, phase=1)) * env * .035
        st(sg, T_FIN, 1, pan=(-.3 if m % 2 else .3), rv=.3)
    st(np.sin(2 * np.pi * _hz(38) * t) * np.exp(-t * 2.5) * .35, T_FIN)
    st(kick, T_FIN, .8)
    st(tam, T_FIN, .3, rv=.3)
    for k, m in enumerate((74, 78, 81, 86, 90, 93, 98)):
        st(_glock(m, 1.0), T_FIN + k * .05, .16, pan=(-.6 + k * .2), rv=.6)

    def kira(t0, base=86, nn=7, gap=.035, g=.14):
        """キラキラ：五聲音階往上滑。"""
        sc = [0, 2, 4, 7, 9]
        for k in range(nn):
            m = base + 12 * (k // 5) + sc[k % 5]
            st(_glock(m, .5), t0 + k * gap, g, pan=(-.5 + k / nn), rv=.6)

    # 音效：數字跳動的「嗶嗶」、落地、長條「啵」、換場琶音、蓋章、網址
    for k in range(int((T_LAND - .55) / .05)):
        nn = int(.02 * SR)
        tq = np.arange(nn) / SR
        st(np.sin(2 * np.pi * (2000 + 90 * k) * tq) * _env(nn, .001, .006), .55 + k * .05, .1)
    for tq_ in (T_LAND, rowT[0] + .45):
        st(kick, tq_, .6)
        st(clap, tq_, .45, rv=.5)
        kira(tq_ + .02, base=86, nn=6, gap=.04, g=.16)
    order = sorted(range(len(rowT)), key=lambda i: rowT[i])
    for k, i in enumerate(order):
        nn = int(.1 * SR)
        tq = np.arange(nn) / SR
        pop = np.sin(2 * np.pi * np.cumsum(_hz(81 + k * 2) * (1 + 1.6 * tq / .1)) / SR) * _env(nn, .002, .035)
        st(pop, rowT[i] + .05, .3, pan=(.3 if k % 2 else -.3), rv=.25)
    for tc in (T_RANK, T_CAP, T_END):
        kira(tc - .3, base=74, nn=8, gap=.035, g=.12)
    st(kick, T_CAP + .3, .7)
    st(clap, T_CAP + .3, .5, rv=.5)
    for i in range(caps_n):
        st(_glock(86 + i * 3, .4), T_CAP + .55 + i * .3, .16, rv=.4)
    # 殘響
    ir_n = int(1.6 * SR)
    ti = np.arange(ir_n) / SR
    for ch_, seed in ((L, 1), (R, 2)):
        ir = _fft_filter(np.random.default_rng(seed).uniform(-1, 1, ir_n), hi=6000) * np.exp(-ti / .42) * .05
        ch_ += _conv(send, ir)
    out = np.stack([_fft_filter(L, lo=35), _fft_filter(R, lo=35)])
    f0 = int((DUR - .3) * SR)
    out[:, f0:] *= np.linspace(1, 0, N - f0)
    out = np.tanh(out * 1.1)
    # 峰值拉到 -1 dBFS 後再降，整體約 -14 LUFS（Reels／Threads 的正規化水準）
    out *= .89 / (np.max(np.abs(out)) or 1) * float(os.environ.get('MUSIC_GAIN', '.6'))
    pcm = (out.T * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return rowT


# ─────────────── 和風、City Pop 共用的混音台 ───────────────

class Mix:
    def __init__(self):
        self.N = int(DUR * SR)
        self.L = np.zeros(self.N)
        self.R = np.zeros(self.N)
        self.send = np.zeros(self.N)

    def st(self, sig, t0, g=1.0, pan=0.0, rv=0.0):
        i = int(t0 * SR)
        if i >= self.N or i < 0:
            return
        j = min(self.N, i + len(sig))
        x = sig[:j - i] * g
        self.L[i:j] += x * (1 - max(pan, 0))
        self.R[i:j] += x * (1 + min(pan, 0))
        if rv:
            self.send[i:j] += x * rv

    def write(self, path, decay=.42, gain=.6):
        ir_n = int(4 * decay * SR)
        ti = np.arange(ir_n) / SR
        for ch, seed in ((self.L, 1), (self.R, 2)):
            ir = _fft_filter(np.random.default_rng(seed).uniform(-1, 1, ir_n), hi=6000) * np.exp(-ti / decay) * .05
            ch += _conv(self.send, ir)
        out = np.stack([_fft_filter(self.L, lo=35), _fft_filter(self.R, lo=35)])
        f0 = int((DUR - .3) * SR)
        out[:, f0:] *= np.linspace(1, 0, self.N - f0)
        out = np.tanh(out * 1.1)
        # 峰值拉到 -1 dBFS 後再降，整體約 -14 LUFS（Reels／Threads 的正規化水準）
        out *= .89 / (np.max(np.abs(out)) or 1) * gain
        with wave.open(path, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((out.T * 32767).astype('<i2').tobytes())


def _tt(dur):
    return np.arange(int(dur * SR)) / SR


def _hit(f0, f1, k, dur, d):
    t = _tt(dur)
    return np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * k)) / SR) * np.exp(-t * d)


def _nz(dur, rng, lo=None, hi=None, d=30, a=.0005):
    t = _tt(dur)
    return _fft_filter(rng.uniform(-1, 1, len(t)), lo=lo, hi=hi) * np.minimum(1, t / a) * np.exp(-t * d)


def _sum(*xs):
    """長度不同的聲音疊在一起（短的補零）。"""
    out = np.zeros(max(len(x) for x in xs))
    for x in xs:
        out[:len(x)] += x
    return out


# ── 和風音色 ──
def _koto(m, dur=.9, bright=1.0):
    t = _tt(dur)
    f = _hz(m)
    ph = 2 * np.pi * np.cumsum(f * (1 + .006 * np.exp(-t * 25))) / SR
    s = sum(k ** -.8 * np.sin(k * ph * (1 + .0006 * k * k)) * np.exp(-t * (2.2 + k * 1.1 / bright))
            for k in range(1, 11))
    return s * np.minimum(1, t / .001)


def _shamisen(m, dur=.35):
    t = _tt(dur)
    f = _hz(m)
    ph = 2 * np.pi * np.cumsum(f * (1 + .01 * np.exp(-t * 40))) / SR
    s = sum(k ** -.45 * np.sin(k * ph) * np.exp(-t * (7 + k * 1.6)) for k in range(1, 14))
    return s * np.minimum(1, t / .0008)


def _fue(m, dur, rng):
    """篠笛：往上滑進音、延遲的抖音、氣音。"""
    t = _tt(dur)
    f = _hz(m) * 2 ** (-70 / 1200 * np.exp(-t * 28))
    f = f * (1 + .006 * np.sin(2 * np.pi * 5.8 * t) * np.clip((t - .12) / .1, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + .18 * np.sin(2 * ph) + .06 * np.sin(3 * ph)
    s += _fft_filter(rng.uniform(-1, 1, len(t)), lo=2500, hi=9000) * .08
    env = np.minimum(1, t / .03) * np.clip((dur - t) / .06, 0, 1)
    return s * env


def _rin(m, dur=2.5):
    t = _tt(dur)
    f = _hz(m)
    return sum(a * (np.sin(2 * np.pi * f * r * t) + np.sin(2 * np.pi * f * r * 1.003 * t)) * np.exp(-t * d)
               for r, a, d in ((1, .5, 1.1), (2.71, .3, 1.8), (5.2, .15, 3), (8.4, .07, 4.5)))


def make_music_wafu(path, rowT, caps_n):
    """和風：140 BPM，陽音階（D E G A B，祭典民謠那種明亮的五聲音階）。
    篠笛主旋律、琴的分散和弦、三味線反拍、大太鼓＋締太鼓＋現代大鼓；換場用琴的上行刮奏＋拍子木，結尾鈴。"""
    rng = np.random.default_rng(5)
    M = Mix()
    six = BEAT / 4
    bar = 4 * BEAT
    T_FIN = 8 * bar
    YO = [0, 2, 5, 7, 9]  # D 陽音階相對音程
    odaiko = _sum(_hit(115, 62, 18, .7, 7), _nz(.15, rng, hi=900, d=30) * .5)
    shime = _sum(_hit(520, 420, 30, .12, 38) * .6, _nz(.06, rng, lo=2000, d=70) * .5)
    kick = _hit(160, 52, 40, .2, 14)
    clap = sum(np.roll(_nz(.2, rng, lo=1200, hi=6000, d=28), int(x * SR)) for x in (0, .008, .016)) * .8
    hyoshigi = _sum(_hit(2300, 2200, 50, .25, 45), .7 * _hit(3400, 3300, 50, .25, 55),
                    _nz(.01, rng, lo=3000, d=300) * .6)

    def gliss(t0, base=74, n=9, gap=.028, g=.13):
        for k in range(n):
            M.st(_koto(base + 12 * (k // 5) + YO[k % 5], .8), t0 + k * gap, g, pan=-.5 + k / n, rv=.4)

    roots = [38, 38, 43, 45]
    for b in range(int(T_FIN / BEAT)):
        tb = b * BEAT
        M.st(kick, tb, .45)
        if b % 2:
            M.st(clap, tb, .32, rv=.35)
        M.st(shime, tb + BEAT / 2, .2, pan=.25, rv=.1)
        if b % 4 == 0:
            M.st(odaiko, tb, .75, rv=.25)
        if b % 4 == 2:
            M.st(odaiko, tb + BEAT / 2, .45, rv=.25)
    for bi in range(int(T_FIN / bar)):
        r = roots[bi % 4]
        t0 = bi * bar
        for k, iv in enumerate((0, 7, 12, 14, 12, 7, 14, 19)):  # 琴：八分音符分散和弦
            M.st(_koto(r + 24 + iv, .7), t0 + k * BEAT / 2, .1, pan=-.35, rv=.25)
        for s16 in (2, 6, 10, 14):  # 三味線：反拍
            for iv in (12, 19):
                M.st(_shamisen(r + iv + 12, .3), t0 + s16 * six, .06, pan=.4, rv=.1)
        for s16 in (0, 6, 8, 14):  # 低音
            t = _tt(.2)
            f = _hz(r)
            M.st((np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * _env(len(t), .004, .08),
                 t0 + s16 * six, .32)
    P1 = [(0, 81, 2), (2, 83, 2), (4, 86, 4), (8, 83, 2), (10, 81, 2), (12, 79, 2), (14, 81, 2),
          (16, 76, 4), (20, 79, 2), (22, 81, 2), (24, 74, 6), (30, 76, 2)]
    P2 = [(0, 86, 2), (2, 88, 2), (4, 86, 2), (6, 83, 2), (8, 81, 4), (12, 83, 2), (14, 86, 2),
          (16, 88, 4), (20, 86, 2), (22, 83, 2), (24, 81, 4), (28, 79, 2), (30, 76, 2)]
    for ph in range(0, int(T_FIN / bar), 2):
        for s16, m, ln in (P1 if (ph // 2) % 2 == 0 else P2):
            M.st(_fue(m, ln * six * .95 + .05, rng), ph * bar + s16 * six, .2, pan=.1, rv=.35)
    # 音效
    for k in range(int((T_LAND - .55) / .05)):
        M.st(_hit(1500 + 60 * k, 1400 + 60 * k, 40, .05, 80), .55 + k * .05, .12)
    for tq in (T_LAND, rowT[0] + .45):
        M.st(odaiko, tq, .9, rv=.3)
        M.st(hyoshigi, tq, .35, rv=.4)
        gliss(tq + .02, base=79, n=7, g=.12)
    order = sorted(range(len(rowT)), key=lambda i: rowT[i])
    for k, i in enumerate(order):
        M.st(_koto(74 + 12 * (k // 5) + YO[k % 5], .8, bright=1.6), rowT[i] + .05, .3, pan=(.3 if k % 2 else -.3), rv=.3)
    for tc in (T_RANK, T_CAP, T_END):
        for k in range(4):  # 太鼓連打
            M.st(odaiko, tc - BEAT + k * six, .25 + .12 * k, rv=.2)
        gliss(tc - .3, base=74, n=10, gap=.026, g=.12)
        M.st(hyoshigi, tc, .3, rv=.4)
    M.st(odaiko, T_CAP + .3, .8, rv=.3)
    M.st(hyoshigi, T_CAP + .3, .4, rv=.4)
    for i in range(caps_n):
        M.st(_koto(86 + YO[(i + 1) % 5], .8, bright=1.6), T_CAP + .55 + i * .3, .2, rv=.3)
    M.st(_rin(93, 1.2), T_END + .95, .06, rv=.4)
    # 收尾：大太鼓、刮奏、長音、鈴
    M.st(odaiko, T_FIN, 1.0, rv=.4)
    gliss(T_FIN, base=62, n=12, gap=.03, g=.13)
    M.st(_fue(86, DUR - T_FIN - .1, rng), T_FIN + .05, .18, rv=.5)
    M.st(_rin(81, DUR - T_FIN), T_FIN + .15, .09, rv=.4)
    t = _tt(DUR - T_FIN)
    M.st(np.sin(2 * np.pi * _hz(38) * t) * np.exp(-t * 2.5), T_FIN, .3)
    M.write(path, decay=.5, gain=float(os.environ.get('MUSIC_GAIN', '.49')))


# ── City Pop 音色 ──
def _ep(m, dur=.6):
    """電鋼琴（FM）：調變指數隨時間變小，加一點高頻音叉聲。"""
    t = _tt(dur)
    f = _hz(m)
    idx = 1.5 * np.exp(-t * 6) + .25
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t * 2.2)
    s += .2 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t * 45)
    return s * np.minimum(1, t / .002) * np.clip((dur - t) / .03, 0, 1)


def _brass(ch, dur=.28):
    t = _tt(dur)
    c = 2 ** (8 / 1200)
    s = sum(_saw(_hz(m), t, roll=12) + _saw(_hz(m) * c, t, roll=12, phase=1) for m in ch)
    return s * np.minimum(1, t / .008) * np.exp(-t * 5) * np.clip((dur - t) / .04, 0, 1)


def _lead(m, dur):
    t = _tt(dur)
    f = _hz(m) * (1 + .005 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - .15) / .1, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.exp(-k / 5) / k * np.sin(k * ph) for k in range(1, 12))
    return s * np.minimum(1, t / .015) * np.clip((dur - t) / .05, 0, 1)


def make_music_citypop(path, rowT, caps_n):
    """City Pop：112 BPM、16 分音符輕微搖擺，丸サ進行（D 大調 G△9｜F#7｜Bm9｜Am9 D9）。
    大鼓「1、2 的後半拍、3」、小鼓 2／4 拍加鬼音、指彈貝斯帶半音經過音、電鋼琴切分並提前半拍換和弦、
    淡淡的弦樂墊底、能哼的四小節主旋律；數字落地與換場用銅管齊奏。"""
    rng = np.random.default_rng(8)
    M = Mix()
    six = BEAT / 4
    bar = 4 * BEAT
    T_FIN = 6 * bar
    SW = .17 * six  # 搖擺：偶數以外的 16 分音符往後拖一點

    def at(t0, s16):
        return t0 + s16 * six + (SW if s16 % 2 else 0)

    kick = _hit(150, 48, 36, .3, 10)
    snare = _sum(_nz(.3, rng, lo=900, hi=9000, d=15) * 1.1, _hit(200, 180, 20, .2, 26) * .5)
    ghost = _nz(.08, rng, lo=1500, hi=7000, d=50)
    hat = _nz(.04, rng, lo=8000, d=110)
    ohat = _nz(.22, rng, lo=7000, d=16)
    crash = _nz(1.4, rng, lo=3500, d=2.6)
    G9, F7, Bm9, Am9, D9 = [59, 62, 66, 69], [58, 61, 64, 68], [62, 66, 69, 73], [60, 64, 67, 71], [60, 64, 66, 69]
    # 每小節兩個半小節：(根音, 和弦)
    prog = [((43, G9), (43, G9)), ((42, F7), (42, F7)), ((47, Bm9), (47, Bm9)), ((45, Am9), (38, D9))]
    nbar = int(T_FIN / bar)
    for bi in range(nbar):
        t0 = bi * bar
        for s16 in (0, 6, 8) + ((11,) if bi % 2 else ()):
            M.st(kick, at(t0, s16), .8)
        for s16 in (4, 12):
            M.st(snare, at(t0, s16), .45, rv=.6)
        for s16 in (7, 15):
            M.st(ghost, at(t0, s16), .12)
        for s16 in range(16):
            if s16 == 14 and bi % 2:
                M.st(ohat, at(t0, s16), .1, pan=.3)
            else:
                M.st(hat, at(t0, s16), (.09 if s16 % 4 == 2 else .06 if s16 % 2 == 0 else .035), pan=.3)
    for bi in range(nbar):
        t0 = bi * bar
        (r1, c1), (r2, c2) = prog[bi % 4]
        nr = prog[(bi + 1) % 4][0][0]
        nc = prog[(bi + 1) % 4][0][1]
        # 電鋼琴：3、6、11 格，14 格提前換成下一個和弦（City Pop 的搶拍）
        hits = [(3, 2, c1), (6, 3, c1 if r1 == r2 else c2), (11, 2, c2)]
        if bi < nbar - 1:
            hits.append((14, 4, nc))
        if bi == 0:
            hits.insert(0, (0, 2, c1))
        for s16, ln, cc in hits:
            for m in cc:
                M.st(_ep(m, ln * six), at(t0, s16), .075, pan=-.25, rv=.25)
        # 弦樂墊底
        t = _tt(bar)
        env = np.minimum(1, t / .25) * np.clip((bar - t) / .15, 0, 1)
        for k, m in enumerate(c1 if r1 == r2 else c1[:2] + c2[2:]):
            M.st(_saw(_hz(m + 12), t, roll=4) * env, t0, .012, pan=(-.5 if k % 2 else .5), rv=.5)
        # 貝斯：跟著大鼓，第 14 格用半音接到下一小節根音
        for s16, rr, ln in ((0, r1, 3), (3, r1, 1), (6, r1, 2), (8, r2, 2), (10, r2 + 12, 1), (11, r2, 2),
                            (14, nr + (1 if nr < r2 else -1), 2)):
            t = _tt(ln * six + .03)
            sg = _saw(_hz(rr), t, roll=4, kdecay=1.2) * np.minimum(1, t / .004) * np.clip((ln * six + .03 - t) / .03, 0, 1)
            M.st(sg, at(t0, s16), .38)
        for s16 in (2, 6, 10, 14):  # 切音吉他
            t = _tt(.06)
            cc = c1 if s16 < 8 else c2
            g = _sum(sum(_saw(_hz(m + 12), t, roll=10) for m in cc) * np.exp(-t * 55), _nz(.06, rng, lo=2000, d=70) * .6)
            M.st(g, at(t0, s16), .045, pan=.45, rv=.1)
    # 主旋律：四小節一句，第二輪結尾改成往上
    mel = [(0, 78, 2), (2, 81, 2), (4, 83, 4), (8, 81, 2), (10, 78, 2), (12, 74, 3), (15, 76, 1),
           (16, 82, 3), (19, 85, 3), (22, 82, 2), (24, 78, 4), (28, 76, 3), (31, 81, 1),
           (32, 83, 3), (35, 86, 3), (38, 88, 2), (40, 86, 4), (44, 83, 2), (46, 81, 2),
           (48, 84, 3), (51, 83, 1), (52, 81, 4), (56, 78, 3), (59, 81, 3), (62, 83, 2)]
    for ph in range(0, nbar, 4):
        for s16, m, ln in mel:
            tq = at(ph * bar, s16)
            if tq >= T_FIN - .05:
                break
            M.st(_lead(m, ln * six * .92 + .02), tq, .12, pan=.1, rv=.35)
            M.st(_ep(m + 12, .35), tq, .03, rv=.3)

    def chord_at(t):
        bi = int(t / bar) % 4
        (r1, c1), (r2, c2) = prog[bi]
        return c2 if (t % bar) >= bar / 2 else c1

    def stab(t0, g=.06):
        cc = [m + 12 for m in chord_at(t0 + six + .01)]
        M.st(_brass(cc, .12), t0, g, rv=.3)
        M.st(_brass(cc, .32), t0 + six, g * 1.2, rv=.4)

    for k in range(int((T_LAND - .55) / .06)):
        M.st(hat, .55 + k * .06, .16)
    for tq in (T_LAND, rowT[0] + .45):
        stab(tq - six, .07)
        M.st(crash, tq + six, .22, pan=-.2)
    order = sorted(range(len(rowT)), key=lambda i: rowT[i])
    for k, i in enumerate(order):
        M.st(_ep((74, 76, 78, 81, 83, 86)[k % 6] + 12, .4), rowT[i] + .05, .22, pan=(.3 if k % 2 else -.3), rv=.3)
    for tc in (T_RANK, T_CAP, T_END):
        for k in range(4):
            M.st(snare, tc - BEAT + k * six, .12 + .07 * k, rv=.4)
        M.st(crash, tc, .2)
    stab(T_CAP + .3 - six, .08)
    for i in range(caps_n):
        M.st(_ep(86 + (0, 4, 7)[i % 3], .4), T_CAP + .55 + i * .3, .2, rv=.3)
    M.st(_ep(93, .6), T_END + .95, .15, rv=.4)
    # 收尾：搶半拍的 D△9 銅管＋電鋼琴長音、鬆開的大鼓與鈸
    fin = [62, 66, 69, 73, 76]
    M.st(_brass([m + 12 for m in fin], .25), T_FIN - 2 * six, .06, rv=.4)
    M.st(_brass([m + 12 for m in fin], 1.4), T_FIN, .07, rv=.5)
    for m in fin:
        M.st(_ep(m, DUR - T_FIN), T_FIN, .08, rv=.4)
    for k, m in enumerate((74, 78, 81, 85, 88, 93)):
        M.st(_ep(m + 12, .9), T_FIN + .5 + k * .07, .07, pan=-.5 + k * .2, rv=.5)
    M.st(kick, T_FIN, .9)
    M.st(crash, T_FIN, .3)
    t = _tt(DUR - T_FIN)
    M.st(np.sin(2 * np.pi * _hz(38) * t) * np.exp(-t * 2), T_FIN, .35)
    M.write(path, decay=.45, gain=float(os.environ.get('MUSIC_GAIN', '.66')))


# ── 破關風音色 ──
def _horn(m, dur, vib=True):
    """銅管：起音時亮度慢慢打開，延遲抖音。"""
    t = _tt(dur)
    f = _hz(m)
    if vib:
        f = f * (1 + .004 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - .2) / .15, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    roll = 2.5 + 7 * np.minimum(1, t / .09)
    s = sum(np.exp(-k / roll) / k * np.sin(k * ph) for k in range(1, 16))
    return s * np.minimum(1, t / .02) * np.clip((dur - t) / .05, 0, 1)


def _str_stac(m, dur=.12):
    t = _tt(dur)
    c = 2 ** (7 / 1200)
    s = _saw(_hz(m), t, roll=6) + _saw(_hz(m) * c, t, roll=6, phase=1.3)
    return s * np.minimum(1, t / .008) * np.exp(-t * 18)


def _timp(m, dur=1.2, rng=None):
    t = _tt(dur)
    f = _hz(m)
    s = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 4)
         + .3 * np.sin(2 * np.pi * f * 1.98 * t) * np.exp(-t * 3)) * np.exp(-t * 2.8)
    return s * np.minimum(1, t / .003)


def _coin(t0, M, g=.12):
    for k, m in enumerate((95, 100)):
        t = _tt(.07 if k == 0 else .22)
        f = _hz(m)
        s = (np.sin(2 * np.pi * f * t) + .3 * np.sin(6 * np.pi * f * t)) * np.exp(-t * (40 if k == 0 else 14))
        M.st(s, t0 + k * .055, g, rv=.15)


def make_music_game(path, rowT, caps_n):
    """破關風：150 BPM、D 大調，管弦配器（銅管英雄主旋律、弦樂八分頑固音型、定音鼓、進行曲小鼓）。
    遊戲音效：數字跳動吃金幣、排名得分音、第一名升級琶音、上限警示；
    網址卡出現時接 ♭VI–♭VII–I（B♭→C→D）過關終止式。旋律原創，不套任何遊戲的現成曲子。"""
    rng = np.random.default_rng(3)
    M = Mix()
    six = BEAT / 4
    bar = 4 * BEAT
    T_CLR = T_END  # 過關號角開始
    kick = _hit(150, 50, 38, .3, 11)
    snare = _sum(_nz(.25, rng, lo=1200, hi=9000, d=20) * 1.1, _hit(220, 190, 20, .15, 30) * .5)
    ride = _nz(.25, rng, lo=6000, d=14)
    crash = _nz(1.6, rng, lo=3500, d=2.4)
    prog = [(38, [62, 66, 69]), (43, [62, 67, 71]), (45, [61, 64, 69]), (38, [62, 66, 69])]
    nb = int(round(T_CLR / BEAT))
    for b in range(nb):
        tb = b * BEAT
        M.st(kick, tb, .55 if b % 2 == 0 else .35)
        if b % 2:
            M.st(snare, tb, .4, rv=.4)
        M.st(ride, tb + BEAT / 2, .06, pan=.35)
        M.st(ride, tb, .04, pan=.35)
        if b % 4 == 3:  # 小節尾的進行曲小鼓碎打
            for k in (1, 2, 3):
                M.st(snare, tb + k * six, .12 + .04 * k, rv=.3)
        if b % 8 == 0:
            M.st(crash, tb, .16, pan=-.3)
    for bi in range(int(math.ceil(T_CLR / bar))):
        r, ch = prog[bi % 4]
        t0 = bi * bar
        M.st(_timp(r + 12), t0, .18, rv=.3)
        for k in range(8):  # 弦樂八分音符：根、五、八、五…
            tq = t0 + k * BEAT / 2
            if tq >= T_CLR:
                break
            M.st(_str_stac(r + 24 + (0, 7, 12, 7, 0, 7, 12, 16)[k]), tq, .05, pan=(-.4 if k % 2 else .4), rv=.25)
            tb2 = _tt(.18)
            M.st((np.sin(2 * np.pi * _hz(r) * tb2) + .4 * np.sin(4 * np.pi * _hz(r) * tb2)) * _env(len(tb2), .004, .08),
                 tq, .22)
        for s16, ln in ((0, 3), (6, 2)):  # 銅管和弦重音
            tq = t0 + s16 * six
            if tq >= T_CLR:
                break
            for m in ch:
                M.st(_horn(m, ln * six, vib=False), tq, .03, pan=-.2, rv=.3)
    # 主旋律：附點進行曲節奏，兩小節一句
    PA = [(0, 74, 3), (3, 76, 1), (4, 78, 4), (8, 81, 4), (12, 79, 2), (14, 78, 2),
          (16, 79, 6), (22, 81, 2), (24, 83, 4), (28, 81, 2), (30, 79, 2)]
    PB = [(0, 81, 3), (3, 83, 1), (4, 85, 4), (8, 88, 4), (12, 85, 2), (14, 81, 2),
          (16, 86, 8), (24, 81, 2), (26, 83, 2), (28, 85, 2), (30, 81, 2)]
    for ph in range(0, int(math.ceil(T_CLR / bar)), 2):
        for s16, m, ln in (PA if (ph // 2) % 2 == 0 else PB):
            tq = ph * bar + s16 * six
            if tq >= T_CLR - BEAT:
                break
            M.st(_horn(m, ln * six * .95 + .03), tq, .17, pan=.1, rv=.35)
            M.st(_str_stac(m + 12, ln * six * .9 + .05) * .5, tq, .03, rv=.3)
    # 遊戲音效
    for k in range(int((T_LAND - .55) / .09)):
        _coin(.55 + k * .09, M, .07)
    for tq in (T_LAND, rowT[0] + .45):
        for k, m in enumerate((74, 78, 81, 86, 90, 93, 98)):  # 升級琶音
            t = _tt(.25)
            M.st((np.sin(2 * np.pi * _hz(m) * t) + .25 * np.sin(4 * np.pi * _hz(m) * t)) * np.exp(-t * 12),
                 tq + k * .035, .1, pan=-.4 + k * .13, rv=.3)
        for m in (62, 66, 69, 74):
            M.st(_horn(m + 12, .5), tq, .05, rv=.4)
        M.st(crash, tq, .25)
        M.st(_timp(50), tq, .5, rv=.3)
    order = sorted(range(len(rowT)), key=lambda i: rowT[i])
    for k, i in enumerate(order):  # 得分音，一名比一名高
        t = _tt(.12)
        f = _hz(81 + k * 2)
        sg = np.sin(2 * np.pi * np.cumsum(f * (1 + .5 * (t < .04))) / SR) * np.exp(-t * 22)
        M.st(sg, rowT[i] + .05, .18, pan=(.3 if k % 2 else -.3), rv=.2)
    for tc in (T_RANK, T_CAP):
        for k in range(4):
            M.st(snare, tc - BEAT + k * six, .12 + .07 * k, rv=.4)
        M.st(crash, tc, .18)
    # 上限：警示的兩聲低銅管＋定音鼓
    for k, m in enumerate((50, 49)):
        M.st(sum(_horn(m + d, .22, vib=False) for d in (0, 12)), T_CAP + .3 + k * .2, .06, rv=.3)
    M.st(_timp(38), T_CAP + .3, .6)
    for i in range(caps_n):
        t = _tt(.15)
        M.st(np.sin(2 * np.pi * _hz(86 + i * 3) * t) * np.exp(-t * 20), T_CAP + .55 + i * .3, .15, rv=.2)
    # 過關號角：前一拍三連音接 B♭ → C → D
    for k, m in enumerate((69, 74, 78)):
        M.st(_horn(m, .13, vib=False), T_CLR - BEAT + k * BEAT / 3, .12, rv=.3)
    for k in range(6):
        M.st(snare, T_CLR - BEAT + k * BEAT / 6, .1 + .03 * k, rv=.3)
    cad = [(T_CLR, 1.5, 34, [58, 62, 65, 70], 86), (T_CLR + 1.5 * BEAT, 1.5, 36, [60, 64, 67, 72], 88),
           (T_CLR + 3 * BEAT, None, 38, [62, 66, 69, 74], 90)]
    for t0, bt, root, ch, top in cad:
        ln = (bt * BEAT if bt else DUR - t0) - .02
        for m in ch:
            M.st(_horn(m, ln), t0, .045, pan=(-.3 if m % 2 else .3), rv=.4)
            M.st(_horn(m + 12, ln) * .5, t0, .03, rv=.4)
        M.st(_horn(top, ln), t0, .14, rv=.45)
        M.st(_timp(root + 12), t0, .4, rv=.3)
        M.st(kick, t0, .6)
        M.st(crash, t0, .25 if bt else .35)
        t = _tt(ln)
        M.st((np.sin(2 * np.pi * _hz(root) * t) + .3 * np.sin(4 * np.pi * _hz(root) * t)) * np.exp(-t * 1.5), t0, .2)
    tf = T_CLR + 3 * BEAT
    for k in range(int((DUR - tf - .4) / .05)):  # 定音鼓滾奏
        M.st(_timp(50, .4), tf + .1 + k * .05, .12 * (1 - k * .03))
    for k, m in enumerate((86, 90, 93, 98, 102, 105)):
        t = _tt(.8)
        M.st((np.sin(2 * np.pi * _hz(m) * t) + .3 * np.sin(2 * np.pi * _hz(m) * 2.76 * t) * np.exp(-t * 10))
             * np.exp(-t * 4), tf + .15 + k * .06, .08, pan=-.5 + k * .2, rv=.6)
    M.write(path, decay=.6, gain=float(os.environ.get('MUSIC_GAIN', '.57')))


STYLES = {'game': make_music_game, 'kawaii': make_music, 'wafu': make_music_wafu, 'citypop': make_music_citypop}


def main():
    from playwright.sync_api import sync_playwright
    d = base.fetch()
    caps = scene_data(d)
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src = build_html(d, caps)
    rowT = json.loads(re.search(r'"rowT": (\[[^\]]*\])', src).group(1))
    # 配樂風格：MUSIC=game（預設；也可 citypop、wafu、kawaii，逗號分隔一次出多支，速度都跟著 BPM），每種一支 transit-topup-15s-<風格>.mp4
    styles = [x for x in os.environ.get('MUSIC', 'game').split(',') if x]
    bad = [x for x in styles if x not in STYLES]
    if bad:
        sys.exit(f'沒有這種配樂：{bad}，可用 {list(STYLES)}')
    keep = os.environ.get('KEEP_FRAMES')  # 給檢查用：存下指定秒數的影格
    outs = []
    with tempfile.TemporaryDirectory() as tmp:
        hf = os.path.join(tmp, 'v.html')
        open(hf, 'w', encoding='utf-8').write(src)
        silent = os.path.join(tmp, 'v.mp4')
        ff = subprocess.Popen(
            ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
             '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
             '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=base._chrome())
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
                    open(os.path.join(keep_dir(), f'{t:05.2f}.png'), 'wb').write(png)
            b.close()
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit('ffmpeg 合成失敗')
        for sty in styles:
            wav = os.path.join(tmp, f'{sty}.wav')
            STYLES[sty](wav, rowT, len(caps))
            mp4 = os.path.join(OUT, f'transit-topup-15s-{sty}.mp4')
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav,
                            '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                            '-shortest', '-movflags', '+faststart', mp4], check=True)
            outs.append(mp4)
    print('\n'.join(outs))
    print(f'{DUR:.0f} 秒；第一名 {d["cards"][0]["name"]} 少付 NT${d["cards"][0]["save"]}；上限列 {len(caps)} 張')


def keep_dir():
    k = os.environ.get('KEEP_DIR', '/tmp')
    os.makedirs(k, exist_ok=True)
    return k


if __name__ == '__main__':
    main()
