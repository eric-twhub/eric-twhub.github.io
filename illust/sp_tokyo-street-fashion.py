# 東京潮牌選物店頁的「原宿、澀谷、中目黑走起來不一樣」插圖與提醒卡（2026-11-13）。
# 街景畫一般的巷子與建築，不畫任何店家招牌、品牌服飾或真實人物；路人穿一般的帽 T、棒球帽。
# 說明依 tokyo-shops-raw.json 與 gen.py 本頁內文（各店官方頁逐項標在頁面表上），
# 營業時間另對過 nonnative 官網（nonnative.com，2F, 1-16-7 Aobadai，11:00 - 19:00）；
# 免稅那張依 /japan-tax-free-2026/ 引的觀光廳旅客說明。輸出 illust/sp/tokyo-street-fashion/*.svg。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-street-fashion')
W, H = 240, 180
GLASS = '#e6f2fa'
LILAC = '#e7defa'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sf-' + name, W, H, label, inner, bg=bg)


def phone(x, y, w=44, h=80, body=LILAC, scr=SKY, smile=True):
    # 一般的圓角長方形手機：外殼＋螢幕＋上方一條小膠囊，不畫任何品牌細節
    r = w * .2
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r:.1f}" fill="{body}"/>'
         f'<rect x="{x+4}" y="{y+5}" width="{w-8}" height="{h-10}" rx="{r*.7:.1f}" fill="{scr}" stroke-width="1.6"/>'
         f'<rect x="{x+w/2-5:.1f}" y="{y+8}" width="10" height="3" rx="1.5" fill="{INK}" stroke="none"/>')
    if smile:
        t += face(x + w / 2, y + h * .52, .7 * w / 44)
    return t


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-6*s},{y-1*s} q{6*s},{-10*s} {12*s},0 q{-6*s},{-4*s} {-12*s},0 Z" fill="{hair}" stroke-width="1.4"/>')


def passport(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{28*s}" height="{38*s}" rx="{3*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+14*s}" cy="{y+17*s}" r="{6.5*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+8*s},{y+31*s} L{x+20*s},{y+31*s}" stroke="{GOLD}" stroke-width="1.6"/>')


def suitcase(x, y, col=SKY, s=1.0):
    return (f'<path d="M{x+10*s},{y} L{x+10*s},{y-8*s} L{x+22*s},{y-8*s} L{x+22*s},{y}" fill="none" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{32*s}" height="{40*s}" rx="{5*s}" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+4*s} L{x+10*s},{y+36*s} M{x+22*s},{y+4*s} L{x+22*s},{y+36*s}" stroke-width="1.4" opacity=".6"/>'
            f'<circle cx="{x+6*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+26*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>')


def floor(y=150, col='#e9dcc8'):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def check(x, y, s=1.0, col=GREEN):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{col}"/>'
            f'<path d="M{x-5*s},{y} L{x-1*s},{y+4*s} L{x+6*s},{y-5*s}" fill="none" stroke="{WHITE}" stroke-width="3"/>')


def cross(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{RED}"/>'
            f'<path d="M{x-5*s},{y-5*s} L{x+5*s},{y+5*s} M{x+5*s},{y-5*s} L{x-5*s},{y+5*s}" stroke="{WHITE}" stroke-width="3"/>')


def label(x, y, txt, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="bold" '
            f'text-anchor="middle" fill="{col}" stroke="none">{txt}</text>')


def kid(x, y, col=RED, s=1.0, cap=None, hood=False):
    # 正面的小人（有臉），可以戴棒球帽或穿帽 T
    t = (f'<path d="M{x-9*s},{y+28*s} q0,{-18*s} {9*s},{-18*s} q{9*s},0 {9*s},{18*s} Z" fill="{col}"/>')
    if hood:
        t += f'<path d="M{x-9*s},{y+2*s} q{9*s},{-16*s} {18*s},0 l0,{8*s} l{-18*s},0 Z" fill="{col}" stroke-width="1.6"/>'
    t += f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .5 * s, False)
    if cap:
        t += (f'<path d="M{x-7*s},{y-2*s} q{7*s},{-11*s} {14*s},0 Z" fill="{cap}" stroke-width="1.6"/>'
              f'<path d="M{x+5*s},{y-2*s} l{8*s},{1*s}" stroke-width="2.4"/>')
    return t


def shop(x, base, w, h, roof, awn=None):
    t = (f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="3" fill="{roof}"/>'
         f'<rect x="{x+6}" y="{base-h*.45:.0f}" width="{w-12}" height="{h*.45-2:.0f}" rx="2" fill="{GLASS}" stroke-width="1.6"/>')
    if awn:
        t += f'<path d="M{x-2},{base-h*.5:.0f} L{x+w+2},{base-h*.5:.0f} L{x+w-2},{base-h*.5+8:.0f} L{x+2},{base-h*.5+8:.0f} Z" fill="{awn}" stroke-width="1.6"/>'
    return t


def treeball(x, base, r=16, col=GREEN):
    return (f'<path d="M{x},{base} L{x},{base-r-6}" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{base-r-10}" r="{r}" fill="{col}"/>')


# 1. 原宿一帶：窄窄的巷子兩邊是小店，路人戴帽子、穿帽 T
card('harajuku', '手繪原宿一帶的窄巷，兩邊是小小的店面，路人戴棒球帽、穿帽 T',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M96,150 L112,60 L128,60 L144,150 Z" fill="#efe6d8" stroke-width="1.6"/>'
     + shop(14, 150, 40, 90, '#fbe2d6', PINK) + shop(56, 150, 40, 70, '#e6f0dc', GREEN)
     + shop(146, 150, 38, 76, '#e0eefa', SKY) + shop(186, 150, 40, 96, '#f6ecc6', GOLD)
     + kid(112, 112, NAVY, 1.0, cap=RED) + kid(134, 120, PINK, .9, hood=True)
     + sparkle(120, 34) + star(30, 30, 6) + star(212, 28, 6))

# 2. 澀谷：大樓、斑馬線、很多人在過馬路
card('shibuya', '手繪澀谷的大路口，有高樓和斑馬線，很多人在過馬路',
     f'<path d="M3,124 L237,124 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#d9dde6"/>'
     + ''.join(f'<rect x="{x}" y="132" width="12" height="38" rx="2" fill="{WHITE}" stroke-width="1.4"/>' for x in range(30, 210, 22))
     + f'<rect x="16" y="30" width="50" height="94" rx="3" fill="#e0eefa"/>'
     + f'<rect x="72" y="52" width="40" height="72" rx="3" fill="#f3e6d6"/>'
     + f'<rect x="120" y="20" width="44" height="104" rx="3" fill="#ece6f7"/>'
     + f'<rect x="170" y="44" width="52" height="80" rx="3" fill="#e6f0dc"/>'
     + ''.join(f'<path d="M{x+4},{y} L{x+w-4},{y}" stroke-width="1" opacity=".5"/>' for x, w, y0 in [(16, 50, 30), (72, 40, 52), (120, 44, 20), (170, 52, 44)] for y in range(y0 + 10, 120, 10))
     + f'<rect x="124" y="30" width="36" height="22" rx="3" fill="{SKY}" stroke-width="1.6"/>'
     + kid(56, 130, RED, .8, cap=NAVY) + kid(100, 136, GOLD, .8, hood=True) + kid(150, 132, GREEN, .8)
     + kid(190, 138, PINK, .8, cap=GOLD) + sparkle(220, 24, 4))

# 3. 中目黑那幾家：低矮的街屋、路樹，路邊一塊寫著「青葉台」的路牌
card('nakameguro', '手繪安靜的低矮街道和行道樹，路邊有一塊寫著青葉台的町名牌',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + shop(20, 150, 56, 62, '#f3e6d6', None) + shop(84, 150, 50, 50, '#e0eefa', None) + shop(176, 150, 48, 58, '#fbe2d6', None)
     + treeball(150, 150, 18, GREEN)
     + f'<rect x="20" y="24" width="64" height="30" rx="5" fill="{NAVY}"/>'
     + f'<text x="52" y="45" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle" fill="{WHITE}" stroke="none">青葉台</text>'
     + f'<path d="M52,54 L52,88" stroke-width="3"/>'
     + kid(206, 120, SKY, .9, cap=GREEN)
     + sparkle(120, 30) + star(214, 30, 6))

# 4. 百貨裡的櫃位：剖面看得到 2F、2.5F、3F，中間那層特別矮
card('floor', '手繪商場的剖面，樓層牌寫著 2F、2.5F、3F，中間那層特別矮',
     f'<rect x="30" y="18" width="180" height="140" rx="6" fill="#f4efe6"/>'
     + f'<path d="M30,62 L210,62 M30,90 L210,90 M30,124 L210,124" stroke-width="2.4"/>'
     + f'<rect x="38" y="30" width="34" height="20" rx="4" fill="{WHITE}"/>' + label(55, 45, '3F', 12)
     + f'<rect x="38" y="66" width="40" height="20" rx="4" fill="{GOLD}"/>' + label(58, 81, '2.5F', 12)
     + f'<rect x="38" y="98" width="34" height="20" rx="4" fill="{WHITE}"/>' + label(55, 113, '2F', 12)
     + ''.join(f'<rect x="{x}" y="{y}" width="26" height="{h}" rx="2" fill="{c}" stroke-width="1.4"/>'
               for x, y, h, c in [(96, 34, 24, PINK), (134, 34, 24, SKY), (172, 34, 24, GREEN),
                                  (96, 68, 18, LILAC), (134, 68, 18, PINK), (172, 68, 18, SKY),
                                  (96, 98, 22, GOLD), (134, 98, 22, GREEN), (172, 98, 22, PINK)])
     + f'<path d="M30,158 L210,158" stroke-width="2.4"/>'
     + kid(120, 132, NAVY, .8, hood=True)
     + f'<path d="M214,76 L224,76 M218,70 L224,76 L218,82" fill="none" stroke="{RED}" stroke-width="2.6"/>'
     + sparkle(18, 30, 4) + star(222, 28, 6))

# 5. 發售日排隊：一排人手上拿著號碼牌
card('queue', '手繪店門口排隊的人，每個人手上拿著號碼牌',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<rect x="168" y="40" width="60" height="110" rx="4" fill="#f3e6d6"/>'
     + f'<rect x="178" y="80" width="40" height="70" rx="3" fill="{GLASS}"/>'
     + f'<path d="M198,80 L198,150" stroke-width="1.6"/>'
     + ''.join(kid(x, 112, c, 1.0, cap=cp, hood=hd) for x, c, cp, hd in
               [(150, NAVY, None, True), (118, RED, GOLD, False), (86, GREEN, None, True), (54, GOLD, NAVY, False), (24, PINK, None, False)])
     + ''.join(f'<rect x="{x+6}" y="118" width="14" height="18" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
               + label(x + 13, 131, n, 9) for x, n in [(150, '1'), (118, '2'), (86, '3'), (54, '4'), (24, '5')])
     + sparkle(60, 40) + star(120, 36, 7) + sparkle(200, 24, 4))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label_, inner):
    F[name] = svg('sf-' + name, 120, 120, label_, inner, bg='#fff3c4')


# 地圖要搜店名：地圖上一根問號圖釘，旁邊一個打勾的圖釘
rem('r-mapname', '手繪提醒：地圖上一根問號圖釘、一根打勾的圖釘',
    f'<path d="M12,30 L42,20 L78,30 L108,20 L108,96 L78,106 L42,96 L12,106 Z" fill="#e6f0dc"/>'
    + f'<path d="M42,20 L42,96 M78,30 L78,106" stroke-width="1.4"/>'
    + f'<path d="M14,70 Q60,54 106,72" fill="none" stroke="{WHITE}" stroke-width="5"/>'
    + f'<path d="M36,62 q-14,-18 0,-28 q14,10 0,28 Z" fill="{GRAY}"/>' + label(36, 50, '?', 12, INK)
    + f'<path d="M84,80 q-16,-20 0,-32 q16,12 0,32 Z" fill="{RED}"/><circle cx="84" cy="60" r="5" fill="{WHITE}"/>'
    + check(98, 92, .55))

# 有幾家 19:00 就關：時鐘指著 7 點，門上掛著打烊牌
rem('r-close', '手繪提醒：時鐘指著七點，店門掛著打烊的牌子',
    f'<rect x="54" y="30" width="54" height="78" rx="4" fill="{BROWN}"/>'
    + f'<circle cx="98" cy="72" r="3" fill="{GOLD}" stroke-width="1.2"/>'
    + f'<path d="M70,44 L81,36 L92,44" fill="none" stroke-width="1.6"/>'
    + f'<rect x="64" y="44" width="34" height="20" rx="3" fill="{WHITE}"/>'
    + f'<path d="M70,54 L92,54" stroke="{RED}" stroke-width="3"/>'
    + f'<circle cx="32" cy="42" r="22" fill="{WHITE}"/>'
    + ''.join(f'<circle cx="{32 + 17*__import__("math").cos(__import__("math").radians(i*30)):.1f}" cy="{42 + 17*__import__("math").sin(__import__("math").radians(i*30)):.1f}" r="1.4" fill="{INK}" stroke="none"/>' for i in range(12))
    + f'<path d="M32,42 L26,51 M32,42 L32,27" stroke-width="2.6"/>'
    + f'<circle cx="32" cy="42" r="2.4" fill="{RED}" stroke="none"/>'
    + label(32, 84, '19:00', 13, RED))

# 幫朋友代買：護照和兩個購物袋，收據連到護照
rem('r-passport', '手繪提醒：護照旁邊兩個購物袋，收據用線連到護照',
    passport(12, 22, 1.2)
    + f'<path d="M62,58 L98,58 L104,104 L56,104 Z" fill="{PINK}"/><path d="M70,58 q10,-16 20,0" fill="none" stroke-width="2.4"/>'
    + f'<path d="M82,70 L110,70 L114,108 L78,108 Z" fill="{SKY}"/><path d="M88,70 q8,-12 16,0" fill="none" stroke-width="2.4"/>'
    + f'<path d="M14,78 L46,78 L46,110 L42,106 L38,110 L34,106 L30,110 L26,106 L22,110 L18,106 L14,110 Z" fill="{WHITE}"/>'
    + f'<path d="M20,88 L40,88 M20,96 L36,96" stroke-width="1.3"/>'
    + f'<path d="M30,78 L30,70" stroke-width="1.8" stroke-dasharray="3 3"/>')

print(save(F, OUT), 'files')
