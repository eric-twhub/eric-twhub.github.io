# 箱根周遊券頁的「一張券坐得到什麼」插圖與提醒卡（2026-11-13）。
# 畫周遊券包含的交通工具與沿線代表景點，參考小田急官方（odakyu-global.com）與
# 箱根ナビ（hakonenavi.jp）的介紹畫成可愛版；不描照片構圖，不畫商標。
# 輸出 illust/sp/japan-hakone-freepass/*.svg。說明文字放在 illust/spots/japan-hakone-freepass.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-hakone-freepass')
W, H = 240, 180
F = {}
SKYB = '#dff0fd'
LAKE = '#9fd0ec'
FUJI = '#8fa8d6'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('hk-' + name, W, H, label, inner, bg=bg)


def fuji(x, base, w=120, h=56):
    l, r = x - w / 2, x + w / 2
    return (f'<path d="M{l},{base} L{x-12},{base-h} Q{x},{base-h-4} {x+12},{base-h} L{r},{base} Z" fill="{FUJI}"/>'
            f'<path d="M{x-12},{base-h} Q{x},{base-h-4} {x+12},{base-h} L{x+22},{base-h+18} '
            f'q-7,5 -12,-2 q-5,7 -10,0 q-5,7 -10,0 q-5,7 -12,2 Z" fill="{WHITE}"/>')


def hills(col=GREEN, y=120):
    return f'<path d="M3,{y} Q50,{y-40} 100,{y-14} Q150,{y-44} 200,{y-18} Q220,{y-26} 237,{y-20} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def trees(pts, col=DGREEN):
    return ''.join(f'<path d="M{x},{y} q-8,-4 -6,-14 q2,-10 6,-14 q4,4 6,14 q2,10 -6,14 Z" fill="{col}" stroke-width="1.4"/>' for x, y in pts)


# 1. 登山電車：之字形折返往上爬
ZZ = 'M14,160 L204,130 L50,98 L214,62'
card('train', '手繪紅色小電車在山坡上之字形往上爬',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,150 L120,30 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#a9d8b1"/>'
     + f'<path d="{ZZ}" fill="none" stroke="{DBROWN}" stroke-width="6"/>'
     + f'<path d="{ZZ}" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-dasharray="3 6"/>'
     + ''.join(f'<path d="M{x},{y} a6,6 0 0 1 0,{h}" fill="none" stroke="{RED}" stroke-width="2.2"/>' for x, y, h in [(210, 124, 12), (44, 92, 12)])
     + f'<g transform="translate(128,112) rotate(12)">'
     f'<rect x="-30" y="-24" width="60" height="24" rx="6" fill="{RED}"/>'
     + ''.join(f'<rect x="{x}" y="-20" width="10" height="9" rx="2" fill="{SKY}" stroke-width="1.2"/>' for x in (-24, -10, 4, 18))
     + f'<path d="M-30,-6 L30,-6" stroke="{WHITE}" stroke-width="2"/>'
     f'<circle cx="-18" cy="2" r="3.4" fill="{INK}"/><circle cx="18" cy="2" r="3.4" fill="{INK}"/></g>'
     + face(104, 102, .5)
     + trees([(30, 140), (226, 110), (176, 92), (88, 72)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="{PINK}" stroke-width="1.2"/>' for x, y in [(70, 146), (80, 144), (150, 78), (160, 74)])
     + sparkle(36, 34) + star(200, 30, 7), bg=SKYB)

# 2. 登山纜車：強羅到早雲山的陡坡
card('cablecar', '手繪在陡坡上往上爬的纜車車廂',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,170 L237,46 L237,155 Q237,177 215,177 L25,177 Q3,177 3,170 Z" fill="#a9d8b1"/>'
     + f'<path d="M3,160 L237,36" stroke="{DBROWN}" stroke-width="3"/>'
     + f'<g transform="translate(112,96) rotate(-28)">'
     f'<path d="M-50,8 L50,8 L50,-26 Q50,-34 42,-34 L-42,-34 Q-50,-34 -50,-26 Z" fill="{GOLD}"/>'
     + ''.join(f'<rect x="{x}" y="-28" width="14" height="14" rx="2" fill="{SKY}" stroke-width="1.2"/>' for x in (-42, -24, -6, 12, 30))
     + f'</g>'
     + face(110, 90, .6)
     + trees([(30, 150), (196, 66), (214, 60), (60, 160)])
     + sparkle(40, 40) + star(200, 120, 6), bg=SKYB)

# 3. 空中纜車：吊廂飛過冒煙的山谷
card('ropeway', '手繪空中纜車的吊廂，下面是冒白煙的山谷，遠處有富士山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + fuji(190, 110, 110, 60)
     + f'<path d="M3,150 Q40,96 90,120 Q130,140 170,112 Q200,96 237,118 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#c9a77a"/>'
     + ''.join(f'<path d="M{x},{y} q-8,-10 0,-18 q8,-8 0,-18" fill="none" stroke="{WHITE}" stroke-width="4"/>' for x, y in [(60, 132), (90, 136), (120, 136)])
     + f'<path d="M3,30 L237,58" stroke-width="2"/>'
     + f'<path d="M108,43 L108,58" stroke-width="2"/>'
     + f'<path d="M86,58 L130,58 Q136,58 136,66 L136,88 Q136,96 128,96 L88,96 Q80,96 80,88 L80,66 Q80,58 86,58 Z" fill="{RED}"/>'
     + f'<rect x="86" y="64" width="44" height="18" rx="4" fill="{SKY}"/>'
     + f'<circle cx="98" cy="74" r="4.5" fill="#f9d9c0" stroke-width="1.2"/><circle cx="116" cy="74" r="4.5" fill="#f9d9c0" stroke-width="1.2"/>'
     + face(108, 89, .5, False)
     + sparkle(40, 50) + star(210, 26, 6), bg=SKYB)

# 4. 大涌谷：火山噴氣、硫磺味
card('owakudani', '手繪光禿禿的火山谷，地面一直冒出白煙',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef3f6"/>'
     + f'<path d="M3,96 Q40,60 80,80 Q120,50 160,76 Q200,54 237,80 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#d9b08a"/>'
     + f'<path d="M3,130 Q60,112 120,126 T237,120 {BOT}" fill="#c48a5c"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.7:.1f}" fill="{WHITE}" stroke-width="1.6"/>' for x, y, r in
               [(70, 90, 16), (84, 72, 20), (72, 52, 14), (150, 96, 14), (162, 78, 18), (156, 56, 12), (110, 116, 10), (118, 102, 12)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{GOLD}" stroke-width="1.2"/>' for x, y in [(40, 140), (52, 146), (190, 138), (204, 144), (126, 150)])
     + f'<path d="M24,108 L24,132 M34,108 L34,132 M20,114 L38,114" stroke="{DBROWN}" stroke-width="2"/>'
     + f'<path d="M200,100 L200,124 M210,100 L210,124 M196,106 L214,106" stroke="{DBROWN}" stroke-width="2"/>'
     + face(84, 72, .7)
     + sparkle(30, 34) + star(214, 30, 6), bg='#eef3f6')

# 5. 海賊觀光船：蘆之湖上的海盜船造型遊船
card('ship', '手繪湖上的海盜船造型遊船，遠處有富士山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + fuji(50, 112, 100, 50)
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{LAKE}"/>'
     + f'<path d="M62,120 L204,120 L192,148 Q180,156 160,156 L90,156 Q76,156 70,148 Z" fill="{DBROWN}"/>'
     + f'<path d="M62,120 L50,108 L80,120 M204,120 L214,104 L196,120" fill="{DBROWN}"/>'
     + f'<path d="M68,132 L198,132" stroke="{GOLD}" stroke-width="3"/>'
     + ''.join(f'<circle cx="{x}" cy="142" r="4" fill="{GOLD}" stroke-width="1.2"/>' for x in (96, 120, 144, 168))
     + f'<path d="M110,120 L110,30 M150,120 L150,44" stroke-width="2.6"/>'
     + f'<path d="M110,36 Q134,50 110,70 Z M110,74 Q138,90 110,112 Z" fill="{WHITE}"/>'
     + f'<path d="M150,48 Q170,60 150,76 Z M150,80 Q172,94 150,112 Z" fill="{WHITE}"/>'
     + f'<path d="M110,30 L126,26 L110,22 Z" fill="{RED}" stroke-width="1.4"/>'
     + face(130, 145, .6)
     + ''.join(f'<path d="M{x},{y} q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>' for x, y in [(20, 136), (210, 140), (40, 160), (200, 164)])
     + sparkle(196, 32) + star(214, 60, 6), bg=SKYB)

# 6. 箱根神社：立在湖面上的鳥居
card('torii', '手繪立在湖水裡的紅色鳥居，後面是森林',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,70 Q60,40 120,58 Q180,36 237,62 L237,120 L3,120 Z" fill="{DGREEN}"/>'
     + trees([(30, 100), (60, 92), (180, 96), (210, 100), (150, 90)], GREEN)
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{LAKE}"/>'
     + f'<path d="M84,58 Q120,50 156,58 L158,50 Q120,40 82,50 Z" fill="{RED}"/>'
     + f'<rect x="88" y="66" width="64" height="7" rx="2" fill="{RED}"/>'
     + f'<rect x="96" y="56" width="9" height="74" rx="2" fill="{RED}"/><rect x="135" y="56" width="9" height="74" rx="2" fill="{RED}"/>'
     + f'<rect x="114" y="58" width="12" height="8" fill="{INK}" stroke-width="1"/>'
     + f'<path d="M90,138 Q120,146 150,138" fill="none" stroke="{RED}" stroke-width="2" opacity=".5"/>'
     + ''.join(f'<path d="M{x},{y} q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>' for x, y in [(30, 140), (190, 140), (60, 160), (170, 162)])
     + sparkle(40, 30) + star(204, 26, 7), bg=SKYB)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('hk-' + name, 120, 120, label, inner, bg='#fff3c4')


def bus(x, y, col, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{48*s}" height="{26*s}" rx="{6*s}" fill="{col}"/>'
            f'<rect x="{x+5*s}" y="{y+5*s}" width="{11*s}" height="{8*s}" rx="2" fill="{SKY}" stroke-width="1.2"/>'
            f'<rect x="{x+19*s}" y="{y+5*s}" width="{11*s}" height="{8*s}" rx="2" fill="{SKY}" stroke-width="1.2"/>'
            f'<rect x="{x+33*s}" y="{y+5*s}" width="{11*s}" height="{8*s}" rx="2" fill="{SKY}" stroke-width="1.2"/>'
            f'<circle cx="{x+11*s}" cy="{y+27*s}" r="{4*s}" fill="{INK}"/><circle cx="{x+37*s}" cy="{y+27*s}" r="{4*s}" fill="{INK}"/>')


# 兩家巴士公司，伊豆箱根巴士不能搭
rem('r-bus', '手繪提醒：兩台顏色不同的巴士，一台打圈一台打叉',
    bus(8, 24, GREEN) + bus(64, 24, '#7fa9d6')
    + f'<circle cx="32" cy="80" r="12" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
    f'<path d="M78,70 L98,90 M98,70 L78,90" stroke="{RED}" stroke-width="3.4"/>'
    f'<path d="M6,104 L114,104" stroke-width="2"/>')

# 纜車停駛改搭代駛巴士，會塞車
rem('r-ropeway', '手繪提醒：停著的纜車和塞在路上的巴士',
    f'<path d="M6,16 L114,30" stroke-width="2"/><path d="M60,23 L60,32" stroke-width="2"/>'
    f'<rect x="44" y="32" width="32" height="24" rx="6" fill="{GRAY}"/>'
    f'<rect x="50" y="37" width="20" height="9" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
    f'<path d="M84,34 L104,54 M104,34 L84,54" stroke="{RED}" stroke-width="3"/>'
    + bus(6, 72, GOLD, .7) + bus(42, 72, GREEN, .7) + bus(78, 72, PINK, .7)
    + f'<path d="M6,100 L114,100" stroke-width="2"/>')

# KKday 憑證只能在新宿西口或小田原換，新宿西口 16:00 關
rem('r-counter', '手繪提醒：服務櫃台和指著 4 點的時鐘',
    f'<rect x="10" y="56" width="66" height="44" rx="4" fill="#e9dcc8"/>'
    f'<rect x="6" y="48" width="74" height="10" rx="3" fill="{SKY}"/>'
    f'<circle cx="43" cy="38" r="9" fill="#f9d9c0"/><path d="M33,48 q0,-8 10,-8 q10,0 10,8" fill="{NAVY}"/>'
    f'<circle cx="94" cy="34" r="18" fill="{WHITE}"/>'
    f'<path d="M94,34 L94,20 M94,34 L104,40" stroke-width="2.6"/>'
    f'<rect x="24" y="66" width="38" height="20" rx="3" fill="{PINK}"/>'
    f'<path d="M6,104 L114,104" stroke-width="2"/>')

print(save(F, OUT), 'files')
