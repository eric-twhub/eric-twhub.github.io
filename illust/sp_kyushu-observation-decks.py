# 九州觀景台懶人包（/kyushu/observation-decks/）的手繪插圖（2026-11-18）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。
# 輸出 illust/sp/kyushu-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'kyushu-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
TURF = '#9fd08a'
SEA = '#9fd0ea'
F = {}
BOX = '<rect x="3" y="3" width="234" height="174" rx="22" fill="{c}"/>'
FLOOR = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ky-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def bldg(x, base, w, h, col=GRAY):
    t = f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{col}" stroke-width="1.6"/>'
    if w >= 14:
        for yy in range(int(base - h + 8), int(base - 6), 12):
            t += f'<path d="M{x+4},{yy} L{x+w-4},{yy}" stroke-width="1" opacity=".45"/>'
    return t


def stars(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in pts)


def citylights(y0, y1, step=10):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{GOLD}" stroke="none"/>'
                   for x in range(14, 230, step) for y in (y0, y1) if (x + y) % 3)


def window(inner_bg, inner, people):
    # 室內展望大廳：窗框、地板、背對的人
    return (BOX.format(c=inner_bg) + inner
            + ''.join(f'<path d="M{x},3 L{x},128" stroke-width="3"/>' for x in (80, 160))
            + f'<path d="M3,128 L237,128 {FLOOR}" fill="#e9dcc8"/><path d="M3,128 L237,128" stroke-width="2.4"/>'
            + people)


def fktower(cx, base, h, s=1.0):
    # 福岡塔：細長三角柱，玻璃帷幕，上面展望室
    top = base - h
    t = (f'<path d="M{cx-9*s},{base} L{cx-5*s},{top+12*s} L{cx+5*s},{top+12*s} L{cx+9*s},{base} Z" fill="#a9c7e3" stroke-width="1.8"/>'
         + ''.join(f'<path d="M{cx-8*s},{y} L{cx+8*s},{y}" stroke="{WHITE}" stroke-width="1" opacity=".8"/>' for y in [base - h * k / 9 for k in range(1, 8)])
         + f'<rect x="{cx-8*s}" y="{top+14*s}" width="{16*s}" height="{8*s}" rx="{2*s}" fill="{WHITE}" stroke-width="1.4"/>'
         + f'<path d="M{cx},{top+12*s} L{cx},{top}" stroke-width="2"/>')
    return t


def castle(cx, base, s=1.0, wall=WHITE, roof='#3d3d4a', stone='#b9a68c'):
    t = (f'<path d="M{cx-60*s},{base} L{cx-48*s},{base-36*s} L{cx+48*s},{base-36*s} L{cx+60*s},{base} Z" fill="{stone}" stroke-width="1.8"/>'
         + ''.join(f'<path d="M{cx-(50-i*2)*s},{base-28*s+i*8*s} L{cx+(50-i*2)*s},{base-28*s+i*8*s}" stroke-width="1" opacity=".5"/>' for i in range(3)))
    for w, y in ((70, 52), (54, 70), (40, 88), (26, 104)):
        t += (f'<rect x="{cx-w*s/2}" y="{base-y*s}" width="{w*s}" height="{16*s}" fill="{wall}" stroke-width="1.6"/>'
              f'<path d="M{cx-w*s/2-8*s},{base-y*s} Q{cx},{base-y*s-10*s} {cx+w*s/2+8*s},{base-y*s} Z" fill="{roof}" stroke-width="1.6"/>')
    return t


def gondola(x, y, col=RED):
    return (f'<path d="M{x},{y-14} L{x},{y}" stroke-width="1.4"/>'
            f'<rect x="{x-14}" y="{y}" width="28" height="20" rx="4" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x-10}" y="{y+4}" width="20" height="8" rx="2" fill="{SKY}" stroke-width="1.2"/>')


def volcano(cx, base, s=1.0, smoke=True):
    t = (f'<path d="M{cx-70*s},{base} Q{cx-30*s},{base-50*s} {cx-12*s},{base-62*s} L{cx+10*s},{base-64*s} '
         f'Q{cx+34*s},{base-48*s} {cx+74*s},{base} Z" fill="#8f8aa8" stroke-width="1.8"/>'
         f'<path d="M{cx-40*s},{base-30*s} Q{cx},{base-44*s} {cx+44*s},{base-28*s}" fill="none" stroke-width="1" opacity=".5"/>')
    if smoke:
        t += cloud(cx - 6 * s, base - 70 * s, .7 * s, '#eeeeee') + cloud(cx + 8 * s, base - 88 * s, .55 * s, '#f5f5f5')
    return t


def sea(y, col=SEA):
    return f'<path d="M3,{y} L237,{y} {FLOOR}" fill="{col}"/>'


def ship(x, y):
    return (f'<path d="M{x},{y} L{x+40},{y} L{x+34},{y+10} L{x+6},{y+10} Z" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x+14}" y="{y-10}" width="14" height="10" rx="2" fill="{SKY}" stroke-width="1.2"/>')


# 0. 封面
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="#f7d9b8"/>'
         + f'<path d="M3,150 Q3,3 25,3 L695,3 Q717,3 717,25 L717,150 Z" fill="#f4c7a0" stroke="none"/>'
         + f'<circle cx="610" cy="76" r="28" fill="{GOLD}"/>'
         + cloud(80, 70, 1.3) + cloud(330, 46, 1.1) + cloud(520, 120, .9)
         + volcano(600, 262, 1.4)
         + f'<path d="M3,262 L3,190 Q90,140 190,200 L190,262 Z" fill="#9fc28d" stroke-width="1.6"/>'
         + f'<path d="M30,150 L170,215" stroke-width="1.4"/>' + gondola(96, 168, RED)
         + castle(300, 262, .9)
         + bldg(380, 262, 28, 70) + bldg(412, 262, 22, 100, '#d9d2e9')
         + fktower(470, 262, 200, 1.4)
         + f'<path d="M500,262 L717,262 L717,250 Q610,236 500,250 Z" fill="{SEA}" stroke-width="1.4"/>'
         + f'<path d="M3,262 L717,262 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#e9dcc8"/>'
         + f'<path d="M3,262 L717,262" stroke-width="2.4"/>'
         + f'<rect x="60" y="270" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(200, 232, PINK, 1.6) + back(380, 236, GREEN, 1.5) + back(560, 232, SKY, 1.6)
         + star(170, 40, 8) + sparkle(440, 40, 6) + sparkle(30, 120, 5))
F['hero'] = svg('ky-hero', 720, 330, '手繪插圖：黃昏的九州，有細長的福岡塔、城堡天守閣、山上的纜車和冒煙的櫻島，三個人站在窗邊看景色', _hero)

# 付費
card('fukuokatower', '手繪海邊細長的玻璃高塔，頂端是展望室，前面是沙灘和海',
     BOX.format(c=SKYB) + cloud(30, 40, .8) + cloud(190, 34, .7)
     + fktower(110, 150, 140, 1.5)
     + f'<path d="M3,138 L237,138 L237,150 L3,150 Z" fill="{SEA}" stroke-width="1.2"/>'
     + f'<path d="M3,150 L237,150 {FLOOR}" fill="#f0dcb0"/>'
     + kid(170, 136, PINK, .9) + kid(196, 138, GREEN, .85) + sparkle(40, 90, 4))
card('sarakura', '手繪山頂的展望台，旁邊有纜車，往下看一大片城市夜景',
     BOX.format(c=NIGHT) + stars([(30, 24, WHITE), (90, 30, GOLD), (200, 20, WHITE)])
     + f'<path d="M3,96 Q120,112 237,94 L237,140 L3,140 Z" fill="#3f4a78" stroke-width="1.4"/>'
     + citylights(112, 124, 9)
     + f'<path d="M20,30 L200,90" stroke-width="1.4"/>' + gondola(120, 58, GOLD)
     + f'<path d="M3,140 Q80,126 150,136 T237,128 {FLOOR}" fill="{DGREEN}"/>'
     + back(60, 128, PINK, .9) + back(90, 130, SKY, .9) + star(210, 60, 5), bg=NIGHT)
card('kokura', '手繪石牆上的城堡天守閣，最上層比下面一層更寬，前面有樹',
     BOX.format(c=SKYB) + cloud(30, 40, .8) + cloud(196, 34, .7)
     + castle(120, 160, 1.0, WHITE, '#4a4a5c')
     + f'<rect x="92" y="48" width="56" height="10" fill="{WHITE}" stroke-width="1.4"/>'
     + f'<path d="M3,160 L237,160 {FLOOR}" fill="{TURF}"/>'
     + ''.join(f'<circle cx="{x}" cy="150" r="10" fill="{GREEN}" stroke-width="1.4"/>' for x in (24, 216))
     + sparkle(206, 80, 4))
card('mojiko', '手繪港邊的高樓，頂樓是玻璃展望室，前面是海峽和小船',
     BOX.format(c=SKYB) + cloud(40, 36, .9) + cloud(190, 46, .7)
     + f'<path d="M3,96 Q120,80 237,92 L237,120 L3,120 Z" fill="#b8c9a3" stroke-width="1.2"/>'
     + bldg(90, 140, 40, 120) + f'<rect x="88" y="20" width="44" height="14" rx="3" fill="{SKY}" stroke-width="1.6"/>'
     + bldg(40, 140, 30, 34, '#e3cfa8') + bldg(150, 140, 26, 26, '#e3cfa8')
     + sea(140) + ship(170, 148)
     + back(104, 34, GOLD, .6) + sparkle(30, 80, 4))
card('kumamotojo', '手繪黑色屋頂的大城堡，高高的石牆，遠方是山',
     BOX.format(c=SKYB)
     + f'<path d="M3,80 Q60,56 120,70 T237,62 L237,110 L3,110 Z" fill="#a8bfa0" stroke-width="1.2"/>'
     + castle(120, 162, 1.1, WHITE, '#2f2f3a', '#a89678')
     + f'<path d="M3,162 L237,162 {FLOOR}" fill="{TURF}"/>'
     + kid(30, 146, RED, .8) + sparkle(210, 30, 4))
card('globaltower', '手繪細長的塔，頂上像一個盒子的展望台，下面溫泉街冒著白色湯煙',
     BOX.format(c=SKYB) + cloud(190, 36, .7)
     + f'<path d="M110,150 Q104,90 114,30 L126,30 Q136,90 130,150 Z" fill="{WHITE}" stroke-width="1.8"/>'
     + f'<rect x="100" y="16" width="40" height="22" rx="3" fill="{SKY}" stroke-width="1.6"/>'
     + ''.join(cloud(x, y, .5, '#f4f4f4') for x, y in ((24, 130), (60, 120), (170, 124), (200, 132)))
     + f'<path d="M3,140 Q60,130 120,140 T237,134 {FLOOR}" fill="#d9c7a8"/>'
     + bldg(20, 160, 18, 20, '#e3cfa8') + bldg(180, 160, 22, 24, '#e3cfa8')
     + back(120, 18, PINK, .55) + sparkle(40, 50, 4))
card('unzen', '手繪纜車往上開到火山頂，山上滿是秋天的紅黃樹，遠方有幾座山',
     BOX.format(c=SKYB) + cloud(40, 34, .8)
     + f'<path d="M3,120 Q50,60 110,40 Q170,56 237,110 {FLOOR}" fill="#c98b5c" stroke-width="1.8"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}" stroke-width="1.2"/>' for x, y, c in ((40, 110, RED), (70, 90, GOLD), (150, 76, RED), (190, 100, GOLD), (100, 120, RED), (170, 130, GOLD)))
     + f'<path d="M20,150 L120,46" stroke-width="1.4"/>' + gondola(70, 96, WHITE)
     + back(120, 40, SKY, .6) + sparkle(210, 30, 4))

# 不用門票
card('acros', '手繪一棟大樓，一側是一層層種滿樹的階梯花園，有人往上爬',
     BOX.format(c=SKYB) + cloud(190, 34, .8)
     + ''.join(f'<path d="M{20+i*16},{170-i*14} L{220},{170-i*14} L220,{184-i*14} L{20+i*16},{184-i*14} Z" fill="#e2d3bd" stroke-width="1.2"/>' for i in range(10))
     + ''.join(f'<circle cx="{28+i*16}" cy="{162-i*14}" r="8" fill="{GREEN}" stroke-width="1.2"/>' for i in range(10))
     + kid(110, 96, PINK, .7) + kid(150, 66, GOLD, .65)
     + sparkle(40, 40, 4))
card('yokamon', '手繪高樓層的休息區，窗外是海灣，桌上有一杯咖啡',
     window(SKYB, f'<path d="M3,80 Q120,66 237,78 L237,104 L3,104 Z" fill="{SEA}" stroke-width="1.2"/>'
            + bldg(20, 120, 14, 18) + bldg(40, 120, 16, 26) + bldg(180, 120, 18, 22) + cloud(40, 40, .7),
            back(110, 120, GOLD, 1.0) + f'<rect x="140" y="132" width="60" height="8" rx="3" fill="{BROWN}" stroke-width="1.4"/>' + mug(170, 120, .8)))
card('hakatacity', '手繪車站大樓的屋頂廣場，欄杆外面看得到一列列電車進站',
     BOX.format(c=SKYB) + cloud(40, 34, .8) + cloud(190, 30, .7)
     + f'<path d="M3,96 L237,96 L237,140 L3,140 Z" fill="#b9bfc9"/>'
     + ''.join(f'<path d="M3,{y} L237,{y}" stroke-width="1.4"/>' for y in (108, 122, 136))
     + f'<rect x="20" y="110" width="90" height="10" rx="5" fill="{WHITE}" stroke-width="1.4"/><rect x="130" y="124" width="90" height="10" rx="5" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<path d="M3,140 L237,140 {FLOOR}" fill="{TURF}"/><path d="M3,140 L237,140" stroke-width="2.2"/>'
     + ''.join(f'<path d="M{x},140 L{x},128" stroke-width="1.4"/>' for x in range(14, 236, 14)) + f'<path d="M3,128 L237,128" stroke-width="1.6"/>'
     + back(80, 120, PINK, .9) + kid(170, 140, SKY, .8))
card('inasa', '手繪山頂的圓形展望台，下面是港口城市一片閃亮的夜景',
     BOX.format(c=NIGHT) + stars([(30, 24, WHITE), (70, 40, GOLD), (210, 22, WHITE)])
     + f'<path d="M3,104 Q120,124 237,100 L237,150 L3,150 Z" fill="#3f4a78" stroke-width="1.4"/>'
     + citylights(124, 138)
     + f'<path d="M100,112 Q120,90 150,108" fill="#3f6f9a" stroke="none"/>'
     + f'<ellipse cx="120" cy="58" rx="40" ry="10" fill="{GRAY}" stroke-width="1.6"/><rect x="104" y="58" width="32" height="22" fill="{WHITE}" stroke-width="1.4"/>'
     + back(110, 34, PINK, .6) + back(130, 36, GOLD, .6)
     + f'<path d="M3,150 Q60,138 120,146 T237,140 {FLOOR}" fill="{DGREEN}"/>' + star(200, 70, 5), bg=NIGHT)
card('nagasakicity', '手繪市政府高樓的展望大廳，窗外是港口和一座白色斜張橋',
     window(SKYB, f'<path d="M3,70 Q60,50 120,60 T237,56 L237,90 L3,90 Z" fill="{GREEN}" stroke-width="1.4"/>'
            + f'<path d="M3,90 L237,90 L237,120 L3,120 Z" fill="{SEA}" stroke-width="1.2"/>'
            + f'<path d="M150,96 L230,96" stroke-width="2"/><path d="M190,96 L190,70 M190,70 L160,96 M190,70 L220,96" stroke-width="1.2"/>'
            + ship(40, 102),
            back(100, 120, SKY, 1.0) + back(140, 122, RED, .95)))
card('nagasakipref', '手繪大樓的戶外展望露台，往下看港口和對岸的山',
     BOX.format(c=SKYB) + cloud(190, 30, .7)
     + f'<path d="M3,70 Q80,40 140,60 T237,58 L237,100 L3,100 Z" fill="{GREEN}" stroke-width="1.4"/>'
     + f'<path d="M3,100 L237,100 L237,126 L3,126 Z" fill="{SEA}" stroke-width="1.2"/>' + ship(150, 106)
     + f'<path d="M3,134 L237,134 {FLOOR}" fill="#e9dcc8"/>'
     + f'<path d="M3,134 L237,134" stroke-width="2.4"/>' + ''.join(f'<path d="M{x},134 L{x},122" stroke-width="1.4"/>' for x in range(14, 236, 16)) + f'<path d="M3,122 L237,122" stroke-width="1.6"/>'
     + back(70, 112, GOLD, .9) + kid(120, 112, PINK, .85))
card('nabekanmuri', '手繪夜晚小山上的展望台，步道邊有一盞盞路燈，下面是港口夜景',
     BOX.format(c=NIGHT) + stars([(30, 24, WHITE), (200, 30, GOLD)])
     + f'<path d="M3,100 Q120,120 237,96 L237,150 L3,150 Z" fill="#3f4a78" stroke-width="1.4"/>' + citylights(120, 134)
     + f'<path d="M3,150 Q100,120 237,140 {FLOOR}" fill="{DGREEN}"/>'
     + ''.join(f'<path d="M{x},{y} L{x},{y-22}" stroke="{WHITE}" stroke-width="1.6"/><circle cx="{x}" cy="{y-24}" r="4" fill="{GOLD}" stroke="none"/>' for x, y in ((40, 148), (90, 136), (150, 138), (200, 146)))
     + back(120, 116, PINK, .8) + star(120, 40, 6), bg=NIGHT)
card('yumihari', '手繪山上的展望台，往下看海上散落著好多綠色小島',
     BOX.format(c=SKYB) + cloud(40, 30, .8)
     + f'<path d="M3,60 L237,60 L237,140 L3,140 Z" fill="{SEA}" stroke="none"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.5}" fill="{GREEN}" stroke-width="1.2"/>' for x, y, r in ((30, 80, 12), (70, 70, 8), (110, 90, 14), (160, 74, 10), (200, 96, 12), (60, 110, 9), (150, 116, 11), (210, 66, 7)))
     + f'<path d="M3,140 Q120,120 237,140 {FLOOR}" fill="#c9a06b"/><path d="M3,140 Q120,120 237,140" fill="none" stroke-width="2.2"/>'
     + back(100, 120, RED, 1.0) + back(136, 120, SKY, .95) + sparkle(210, 30, 4))
card('saga360', '手繪大樓最上層一圈的玻璃展望大廳，外面是一大片平坦的田野和城市',
     window(SKYB, f'<path d="M3,80 L237,80 L237,120 L3,120 Z" fill="#c6dc9a" stroke-width="1.2"/>'
            + ''.join(f'<path d="M3,{y} L237,{y}" stroke-width="1" opacity=".4"/>' for y in (92, 104))
            + bldg(30, 88, 12, 16) + bldg(46, 88, 14, 22) + bldg(190, 88, 14, 14) + cloud(160, 40, .8),
            back(110, 120, PINK, 1.0) + kid(150, 120, GOLD, .9)))
card('kumamotocity', '手繪高樓展望大廳的窗外，看得到樹林中的黑色城堡',
     window(SKYB, f'<path d="M3,96 Q120,80 237,96 L237,128 L3,128 Z" fill="{GREEN}" stroke-width="1.2"/>'
            + castle(120, 112, .55, WHITE, '#2f2f3a', '#a89678') + cloud(40, 36, .7),
            back(70, 120, SKY, 1.0) + back(190, 122, RED, .95)))
card('daikanbo', '手繪草原山脊上的展望點，前面是一大圈連綿的火山口外輪山和平原',
     BOX.format(c=SKYB) + cloud(60, 34, .8) + cloud(190, 40, .7)
     + f'<path d="M3,90 Q40,70 80,80 Q120,60 160,72 Q200,62 237,84 L237,120 L3,120 Z" fill="#8f9cb8" stroke-width="1.4"/>'
     + f'<path d="M3,110 L237,110 L237,128 L3,128 Z" fill="#c6dc9a" stroke-width="1.2"/>'
     + f'<path d="M3,128 Q120,112 237,132 {FLOOR}" fill="#d9c27a"/>'
     + ''.join(f'<path d="M{x},{y} q3,-10 6,0" fill="none" stroke-width="1.2"/>' for x, y in ((30, 150), (60, 140), (170, 150), (200, 142)))
     + back(110, 120, PINK, 1.0) + back(140, 122, GREEN, .95))
card('oitapref', '手繪辦公大樓高樓層的窗邊，外面是城市和遠方的海',
     window(SKYB, f'<path d="M3,74 L237,74 L237,90 L3,90 Z" fill="{SEA}" stroke-width="1.2"/>'
            + ''.join(bldg(x, 120, w, h) for x, w, h in ((14, 16, 26), (36, 12, 18), (56, 18, 30), (170, 16, 22), (192, 20, 28)))
            + cloud(120, 40, .8),
            back(110, 120, GOLD, 1.0)))
card('jumonji', '手繪高原上的展望台，往下看溫泉城市和海灣',
     BOX.format(c=SKYB) + cloud(50, 34, .8)
     + f'<path d="M3,70 L237,70 L237,96 L3,96 Z" fill="{SEA}" stroke-width="1.2"/>'
     + f'<path d="M3,96 Q120,86 237,96 L237,116 L3,116 Z" fill="#d6c3a8" stroke-width="1.2"/>'
     + ''.join(cloud(x, 98, .35, '#f4f4f4') for x in (40, 90, 150, 200))
     + f'<path d="M3,120 Q120,104 237,124 {FLOOR}" fill="{TURF}"/>'
     + f'<rect x="80" y="112" width="80" height="8" fill="{BROWN}" stroke-width="1.4"/>'
     + back(100, 108, SKY, .9) + back(136, 110, PINK, .9) + sparkle(210, 30, 4))
card('kagoshimapref', '手繪高樓展望大廳的窗外，海灣對面是一座冒煙的火山島',
     window(SKYB, f'<path d="M3,100 L237,100 L237,128 L3,128 Z" fill="{SEA}" stroke-width="1.2"/>' + volcano(120, 104, .9),
            back(80, 120, GOLD, 1.0) + back(170, 122, GREEN, .95)))
card('shiroyama', '手繪小山上的展望台，越過城市和海灣看到冒煙的火山',
     BOX.format(c=SKYB)
     + volcano(150, 100, 1.0)
     + f'<path d="M3,96 L237,96 L237,112 L3,112 Z" fill="{SEA}" stroke-width="1.2"/>'
     + ''.join(bldg(x, 128, w, h, '#d6d0c4') for x, w, h in ((14, 12, 14), (30, 14, 20), (60, 12, 12), (150, 14, 18), (190, 16, 22)))
     + f'<path d="M3,132 Q120,118 237,136 {FLOOR}" fill="{DGREEN}"/>'
     + back(90, 122, PINK, .9) + back(120, 124, GOLD, .9))
card('yunohira', '手繪近在眼前的大火山，山頂冒著白煙，下面是展望所的平台',
     BOX.format(c=SKYB)
     + volcano(120, 140, 1.5)
     + f'<path d="M3,140 L237,140 {FLOOR}" fill="#c9b394"/><path d="M3,140 L237,140" stroke-width="2.2"/>'
     + ''.join(f'<path d="M{x},140 L{x},128" stroke-width="1.4"/>' for x in range(14, 236, 16)) + f'<path d="M3,128 L237,128" stroke-width="1.6"/>'
     + back(60, 120, RED, 1.0) + kid(190, 128, SKY, .8))

print(save(F, OUT), 'files')
