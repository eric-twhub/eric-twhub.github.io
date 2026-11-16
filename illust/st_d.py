# 主題貼紙 D 組（2026-11-16）：年末年始用的手繪貼紙。
# 門松給 /japan-new-year-hours/（跨年店家營業），福袋給 /japan-fukubukuro/。
# 共用工具在 kit.py。跑 `python3 illust/st_d.py` 輸出 illust/st/*.svg，
# 再跑 `python3 illust/make_banners.py` 產生標題下的寬版封面。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st')
STRAW = '#e2c27a'
BAMBOO = '#7cc48f'
PINE = '#4f9a6a'

FILES = {}


def add(name, label, inner, bg=CREAM, dots=True):
    FILES[name] = sticker(name, label, inner, bg=bg, dots=dots)


# ---- kadomatsu：門松（三根斜切竹子＋松枝＋草蓆底座）----
def bamboo(x, top, base, w=14):
    # 斜切的竹子：切口是一個斜的橢圓，中間兩道竹節
    t = (f'<path d="M{x-w/2},{base} L{x-w/2},{top+6} L{x+w/2},{top-6} L{x+w/2},{base} Z" fill="{BAMBOO}"/>'
         f'<ellipse cx="{x}" cy="{top}" rx="{w/2+.5}" ry="6.5" transform="rotate(-40 {x} {top})" fill="{CREAM}"/>')
    for k in (.35, .7):
        yy = top + (base - top) * k
        t += f'<path d="M{x-w/2},{yy:.0f} q{w/2},4 {w},0" fill="none" stroke-width="1.6"/>'
    return t


def pine(x, y, s=1.0, flip=1):
    # 一小叢松針
    t = ''
    for a in (-50, -25, 0, 25, 50):
        t += (f'<path d="M{x},{y} l{flip*14*s:.1f},{-6*s + a*.18*s:.1f}" stroke="{PINE}" stroke-width="2.6"/>')
    return t + f'<circle cx="{x}" cy="{y}" r="{3*s}" fill="{PINE}" stroke-width="1.4"/>'


kad = ''
kad += pine(52, 74, 1.2, -1) + pine(128, 70, 1.2, 1) + pine(60, 58, 1.0, -1) + pine(120, 54, 1.0, 1)
kad += bamboo(78, 34, 96) + bamboo(102, 44, 96) + bamboo(90, 22, 96)
# 草蓆底座＋兩道繩
kad += f'<path d="M56,92 L124,92 L118,134 Q90,140 62,134 Z" fill="{STRAW}"/>'
kad += ''.join(f'<path d="M{60+i*8},96 L{63+i*7},132" stroke-width="1" opacity=".45"/>' for i in range(8))
kad += f'<path d="M58,104 Q90,110 122,104" fill="none" stroke="{RED}" stroke-width="3.2"/>'
kad += f'<path d="M60,122 Q90,128 120,122" fill="none" stroke="{RED}" stroke-width="3.2"/>'
kad += face(90, 113, .9)
# 旁邊的紅白梅花與日出
kad += f'<circle cx="146" cy="40" r="13" fill="{RED}" stroke-width="2"/>'
for x, y, c in [(36, 104, PINK), (146, 108, WHITE)]:
    kad += ''.join(f'<circle cx="{x + 5*dx}" cy="{y + 5*dy}" r="3.6" fill="{c}" stroke-width="1.2"/>'
                   for dx, dy in [(0, -1), (.95, -.3), (.6, .8), (-.6, .8), (-.95, -.3)])
    kad += f'<circle cx="{x}" cy="{y}" r="2" fill="{GOLD}" stroke="none"/>'
add('kadomatsu', '門松', kad)


# ---- fukubukuro：福袋（紅色布袋、金色綁繩、福字圓牌）----
fk = ''
fk += f'<path d="M48,62 Q40,128 60,134 L120,134 Q140,128 132,62 Q90,50 48,62 Z" fill="{RED}"/>'
fk += f'<path d="M62,62 Q68,36 76,40 Q84,30 90,40 Q96,30 104,40 Q112,36 118,62 Z" fill="{RED}"/>'
fk += f'<path d="M58,64 Q90,74 122,64" fill="none" stroke="{GOLD}" stroke-width="5"/>'
fk += (f'<path d="M90,68 q-14,6 -18,18 M90,68 q14,6 18,18" fill="none" stroke="{GOLD}" stroke-width="3"/>'
       f'<circle cx="72" cy="88" r="3.4" fill="{GOLD}" stroke-width="1.2"/>'
       f'<circle cx="108" cy="88" r="3.4" fill="{GOLD}" stroke-width="1.2"/>')
fk += f'<circle cx="90" cy="104" r="17" fill="{CREAM}" stroke-width="2"/>'
fk += (f'<text x="90" y="112" text-anchor="middle" font-size="22" font-weight="700" fill="{RED}" stroke="none" '
       f'font-family="Huninn, \'Noto Sans TC\', sans-serif">福</text>')
fk += face(90, 124, .7, blush=False)
fk += (f'<ellipse cx="68" cy="122" rx="4" ry="2.4" fill="{PINK}" stroke="none" opacity=".9"/>'
       f'<ellipse cx="112" cy="122" rx="4" ry="2.4" fill="{PINK}" stroke="none" opacity=".9"/>')
fk += star(38, 46, 8) + star(144, 52, 7) + sparkle(150, 94) + sparkle(30, 96)
add('fukubukuro', '福袋', fk)

# ---- donut：甜甜圈（福袋頁 Mister Donut 段落用，一般甜甜圈，不畫任何品牌角色）----
dn = ''
dn += f'<ellipse cx="90" cy="84" rx="50" ry="42" fill="#e9b27a"/>'
dn += (f'<path d="M44,74 Q50,44 90,42 Q130,44 136,74 Q140,92 124,96 Q112,84 100,96 Q90,88 80,96 '
       f'Q68,84 56,96 Q40,92 44,74 Z" fill="{PINK}"/>')
dn += f'<ellipse cx="90" cy="80" rx="15" ry="11" fill="{CREAM}"/>'
for x, y, c, a in [(62, 60, GOLD, 30), (78, 52, WHITE, -20), (108, 54, GREEN, 40), (120, 70, WHITE, -35), (58, 78, GREEN, 10), (100, 66, GOLD, 60)]:
    dn += f'<rect x="{x}" y="{y}" width="9" height="3.4" rx="1.7" fill="{c}" stroke-width="1" transform="rotate({a} {x+4} {y+2})"/>'
dn += face(90, 108, .9)
dn += star(34, 40, 7) + sparkle(150, 44) + sparkle(146, 118)
add('donut', '甜甜圈', dn)

# ---- seatree：海上的聖誕樹＋煙火＋紅磚倉庫（/hakodate/christmas-fantasy/）----
st = ''
for cx, cy, r, c in [(40, 36, 16, GOLD), (142, 30, 13, PINK), (122, 58, 9, SKY)]:
    st += ''.join(f'<path d="M{cx},{cy} l{r*math.cos(a):.1f},{r*math.sin(a):.1f}" stroke="{c}" stroke-width="2"/>'
                  for a in [i * math.pi / 6 for i in range(12)])
    st += f'<circle cx="{cx}" cy="{cy}" r="2.4" fill="{c}" stroke="none"/>'
# 紅磚倉庫（右後方）
st += f'<path d="M118,104 L118,84 L134,74 L150,84 L150,104 Z" fill="{BRICK}"/>'
st += f'<path d="M150,104 L150,86 L162,78 L172,86 L172,104 Z" fill="#c45a4a"/>'
st += ''.join(f'<rect x="{x}" y="90" width="6" height="8" rx="1" fill="{GOLD}" stroke-width="1"/>' for x in (124, 138, 158))
# 浮台與樹
st += tree(76, 104, 74, 56)
st += f'<rect x="46" y="104" width="60" height="8" rx="3" fill="{DBROWN}"/>'
# 海浪
st += (f'<path d="M6,114 q12,-7 24,0 t24,0 t24,0 t24,0 t24,0 t24,0 t24,0 L174,136 Q174,144 166,144 '
       f'L14,144 Q6,144 6,136 Z" fill="#5b86c4"/>')
st += f'<path d="M30,126 q10,-5 20,0 M96,130 q10,-5 20,0 M140,124 q8,-4 16,0" fill="none" stroke="{SKY}" stroke-width="1.6"/>'
FILES['seatree'] = sticker('seatree', '海上的聖誕樹', st, bg=NAVY, dots=False)

# ---- skgbus：雪地裡往合掌村開的巴士（/japan-takayama-shirakawago-bus/，一般巴士，不畫任何公司的塗裝）----
THATCH = '#b98f55'
def _gh(x, base, w, h):
    top, rb = base - h, base - h * .38
    return (f'<rect x="{x - w*.38:.0f}" y="{rb:.0f}" width="{w*.76:.0f}" height="{base-rb:.0f}" fill="{DBROWN}"/>'
            f'<path d="M{x - w/2:.0f},{rb+2:.0f} L{x},{top} L{x + w/2:.0f},{rb+2:.0f} Z" fill="{THATCH}"/>'
            f'<path d="M{x - w*.28:.0f},{top + (rb-top)*.58:.0f} L{x},{top} L{x + w*.28:.0f},{top + (rb-top)*.58:.0f} '
            f'Q{x},{top + (rb-top)*.48:.0f} {x - w*.28:.0f},{top + (rb-top)*.58:.0f} Z" fill="{WHITE}"/>'
            f'<rect x="{x - w*.1:.0f}" y="{top + (rb-top)*.68:.0f}" width="{w*.2:.0f}" height="{w*.12:.0f}" rx="1" fill="{GOLD}" stroke-width="1.2"/>')
bs = ''
bs += _gh(132, 92, 70, 70) + _gh(40, 84, 40, 44)
# 雪地
bs += f'<path d="M6,96 Q60,88 120,94 T174,92 L174,136 Q174,144 166,144 L14,144 Q6,144 6,136 Z" fill="{WHITE}"/>'
# 巴士車身
bs += f'<rect x="30" y="74" width="112" height="46" rx="10" fill="{SKY}"/>'
bs += f'<path d="M30,104 L142,104" stroke="{GREEN}" stroke-width="6"/>'
bs += ''.join(f'<rect x="{x}" y="82" width="18" height="15" rx="2.5" fill="{WHITE}" stroke-width="1.4"/>' for x in (40, 62, 84, 106))
bs += f'<rect x="126" y="82" width="12" height="28" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
bs += f'<path d="M40,74 Q86,64 132,74" fill="{WHITE}" stroke-width="1.6"/>'
for cx in (52, 118):
    bs += f'<circle cx="{cx}" cy="121" r="9" fill="{INK}"/><circle cx="{cx}" cy="121" r="3.4" fill="{GRAY}" stroke="none"/>'
bs += f'<circle cx="141" cy="112" r="3" fill="{GOLD}" stroke-width="1"/>'
bs += face(73, 112, .7)
bs += snow([(20, 30), (70, 22), (104, 40), (160, 24), (12, 62), (90, 50)])
add('skgbus', '手繪雪地裡開往合掌村的巴士', bs, bg='#e4eefa', dots=False)

print(save(FILES, OUT), 'stickers')
