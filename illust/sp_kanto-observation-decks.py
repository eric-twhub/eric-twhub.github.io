# 首都圈觀景台懶人包（/kanto/observation-decks/）東京以外展望點的手繪插圖（2026-11-18）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。輸出 illust/sp/kanto-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'kanto-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
SEA = '#9fd0ea'
MTN = '#9cc59a'
F = {}
BOX = '<rect x="3" y="3" width="234" height="174" rx="22" fill="{c}"/>'
FLOOR = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('kn-' + name, W, H, label, inner, bg=bg)


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def fuji(x0, x1, base, peak):
    m = (x0 + x1) / 2
    return (f'<path d="M{x0},{base} L{m-10},{peak} L{m+10},{peak} L{x1},{base} Z" fill="#a9b8d8" stroke-width="1.6"/>'
            f'<path d="M{m-22},{peak+16} L{m-10},{peak} L{m+10},{peak} L{m+22},{peak+16} q-8,5 -14,0 q-8,5 -16,0 q-8,5 -14,0 Z" fill="{WHITE}" stroke-width="1.2"/>')


def sea(y, col=SEA):
    return f'<path d="M3,{y} L237,{y} {FLOOR}" fill="{col}"/>'


def ship(x, y, s=1.0):
    return (f'<path d="M{x},{y} L{x+40*s},{y} L{x+34*s},{y+10*s} L{x+6*s},{y+10*s} Z" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x+14*s}" y="{y-10*s}" width="{14*s}" height="{10*s}" rx="2" fill="{SKY}" stroke-width="1.2"/>')


def bldgs(base, xs, col='#d6dbe6'):
    return ''.join(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{col}" stroke-width="1.4"/>' for x, w, h in xs)


def lighthouse(cx, base, h=80, col=WHITE):
    return (f'<path d="M{cx-14},{base} L{cx-9},{base-h} L{cx+9},{base-h} L{cx+14},{base} Z" fill="{col}" stroke-width="1.8"/>'
            f'<rect x="{cx-12}" y="{base-h-14}" width="24" height="14" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
            f'<path d="M{cx-14},{base-h-14} L{cx},{base-h-26} L{cx+14},{base-h-14} Z" fill="{RED}" stroke-width="1.6"/>')


def gondola(x, y, col=RED):
    return (f'<path d="M{x},{y-14} L{x},{y}" stroke-width="1.4"/>'
            f'<rect x="{x-14}" y="{y}" width="28" height="20" rx="4" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x-10}" y="{y+4}" width="20" height="8" rx="2" fill="{SKY}" stroke-width="1.2"/>')


def ropeway(x0, y0, x1, y1, col=RED):
    return f'<path d="M{x0},{y0} L{x1},{y1}" stroke-width="1.6"/>' + gondola((x0 + x1) / 2, (y0 + y1) / 2 + 14, col)


card('marinetower', '手繪港邊的紅白高塔，塔下有公園和停泊的大船',
     BOX.format(c=SKYB) + cloud(40, 36, .8) + sea(118)
     + f'<path d="M108,140 L114,40 L126,40 L132,140 Z" fill="{RED}" stroke-width="1.8"/>'
     + ''.join(f'<path d="M{110+i*.6},{60+i*20} L{130-i*.6},{60+i*20}" stroke="{WHITE}" stroke-width="3"/>' for i in range(4))
     + f'<rect x="102" y="30" width="36" height="14" rx="4" fill="{WHITE}" stroke-width="1.6"/>' + ship(160, 128) + back(60, 120, GOLD, .8))
card('cosmoclock', '手繪港邊的大摩天輪，中間是一個大時鐘，晚上亮著燈',
     BOX.format(c=NIGHT) + sea(130, '#3e4f86')
     + f'<circle cx="120" cy="80" r="56" fill="none" stroke="{WHITE}" stroke-width="2.4"/>'
     + ''.join(f'<circle cx="{120+56*__import__("math").cos(a/12*6.283)}" cy="{80+56*__import__("math").sin(a/12*6.283)}" r="5" fill="{GOLD}" stroke-width="1"/>' for a in range(12))
     + f'<circle cx="120" cy="80" r="16" fill="{WHITE}" stroke-width="1.6"/><path d="M120,80 L120,70 M120,80 L128,84" stroke-width="2"/>'
     + f'<path d="M104,150 L120,80 L136,150" fill="none" stroke-width="2.4"/>' + bldgs(130, ((10, 18, 60), (32, 14, 40), (196, 16, 50), (214, 14, 36)), '#56628f'), bg=NIGHT)
card('seacandle', '手繪小島上的燈塔型展望台，遠方海上看得到富士山',
     BOX.format(c=SKYB) + fuji(20, 120, 96, 50) + sea(96)
     + f'<path d="M120,177 Q130,120 180,116 Q230,120 237,140 L237,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<path d="M172,118 L176,46 L188,46 L192,118 Z" fill="{WHITE}" stroke-width="1.8"/><rect x="168" y="36" width="28" height="14" rx="5" fill="{SKY}" stroke-width="1.6"/>'
     + back(150, 112, PINK, .7))
card('chibaporttower', '手繪港邊的玻璃高塔，對岸遠方有富士山和城市',
     BOX.format(c=SKYB) + fuji(10, 110, 92, 56) + bldgs(92, ((130, 10, 20), (144, 12, 30), (160, 8, 16))) + sea(92)
     + f'<path d="M150,160 L160,30 L184,40 L190,160 Z" fill="#a9c7e3" stroke-width="1.8"/>'
     + ''.join(f'<path d="M{155+i},{50+i*22} L{186-i*.2},{56+i*22}" stroke="{WHITE}" stroke-width="1.4"/>' for i in range(5))
     + ship(40, 130))
card('nokogiri', '手繪鋸齒狀岩山上的纜車，下面是海和小港口',
     BOX.format(c=SKYB) + sea(120)
     + f'<path d="M100,177 L120,70 L134,82 L150,52 L164,66 L180,40 L196,58 L237,50 L237,177 Z" fill="#b9a68c" stroke-width="1.8"/>'
     + ropeway(30, 120, 180, 44) + ship(20, 140, .8))
card('hodosan', '手繪山上的纜車，山頂開著黃色臘梅，遠方是城市和山',
     BOX.format(c=SKYB) + f'<path d="M3,70 Q60,40 120,62 Q180,36 237,60 L237,177 L3,177 Z" fill="#b8c7d6" stroke-width="1.4"/>'
     + f'<path d="M3,177 L3,140 Q100,120 237,60 L237,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + ropeway(30, 150, 210, 74, GOLD)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{GOLD}" stroke-width="1"/>' for x, y in ((196, 84), (212, 78), (222, 90), (184, 94))))
card('oyamacable', '手繪山坡上的小纜車，旁邊是紅葉和神社的屋頂',
     BOX.format(c=SKYB) + f'<path d="M3,177 L3,150 L237,40 L237,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<path d="M20,150 L220,56" stroke-width="3"/><rect x="110" y="88" width="34" height="20" rx="4" fill="{RED}" stroke-width="1.6" transform="rotate(-25 127 98)"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#e8a05c" stroke-width="1.2"/>' for x, y in ((60, 112), (80, 128), (170, 72), (200, 64)))
     + f'<path d="M180,44 L210,30 L240,44 Z" fill="{BROWN}" stroke-width="1.6"/>')
card('choshiporttower', '手繪漁港邊的雙塔，下面停著漁船，遠方是海',
     BOX.format(c=SKYB) + sea(110)
     + f'<rect x="96" y="40" width="22" height="100" rx="3" fill="#a9c7e3" stroke-width="1.8"/><rect x="124" y="40" width="22" height="100" rx="3" fill="#a9c7e3" stroke-width="1.8"/>'
     + f'<rect x="92" y="34" width="58" height="14" rx="3" fill="{WHITE}" stroke-width="1.6"/>' + ship(30, 130, .8) + ship(170, 134, .8))
card('chikyunooka', '手繪丘上的展望館屋頂，四周是一望無際、邊緣彎彎的海',
     BOX.format(c=SKYB) + f'<path d="M3,96 Q120,70 237,96 L237,177 L3,177 Z" fill="{SEA}" stroke-width="1.6"/>'
     + f'<path d="M30,177 Q120,120 210,177 Z" fill="{MTN}" stroke-width="1.6"/><rect x="88" y="134" width="64" height="20" rx="4" fill="#e8e2d4" stroke-width="1.6"/>'
     + back(110, 112, RED, .7) + back(130, 112, SKY, .7))
card('inubosaki', '手繪海岬上的白色燈塔，下面是拍打岩岸的浪',
     BOX.format(c=SKYB) + sea(120) + f'<path d="M60,177 Q90,120 170,124 Q210,130 237,150 L237,177 Z" fill="#b9a68c" stroke-width="1.6"/>'
     + lighthouse(140, 128, 80) + ''.join(f'<path d="M{x},150 q8,-8 16,0" fill="none" stroke="{WHITE}" stroke-width="2.4"/>' for x in (14, 40)))
card('kannonzaki', '手繪海岬林間的白色燈塔，前面海上有船經過',
     BOX.format(c=SKYB) + sea(110) + ship(30, 120) + ship(150, 140, .7)
     + f'<path d="M120,177 Q150,100 237,96 L237,177 Z" fill="{MTN}" stroke-width="1.6"/>' + lighthouse(190, 110, 60))
card('osanbashi', '手繪伸進港口的木頭甲板屋頂廣場，對岸是高樓群和大摩天輪',
     BOX.format(c=SKYB) + bldgs(80, ((20, 16, 50), (40, 12, 30), (150, 18, 60), (172, 14, 38), (190, 12, 46)))
     + f'<circle cx="100" cy="56" r="22" fill="none" stroke-width="2"/>' + sea(80)
     + f'<path d="M3,140 Q120,116 237,140 L237,177 L3,177 Z" fill="#d9b48f" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},150 Q{x+60},130 {x+120},150" fill="none" stroke-width="1" opacity=".5"/>' for x in (0, 60, 120))
     + back(80, 122, RED, .8) + back(150, 120, GOLD, .8))
card('kawasakicityhall', '手繪高樓頂層的室內展望大廳與戶外平台，窗外是城市和遠方的高樓',
     BOX.format(c=SKYB) + bldgs(110, ((14, 14, 40), (32, 12, 60), (170, 16, 50), (190, 14, 30), (208, 12, 44)))
     + ''.join(f'<path d="M{x},3 L{x},120" stroke-width="3"/>' for x in (80, 160))
     + f'<path d="M3,120 L237,120 {FLOOR}" fill="#e9dcc8"/><path d="M3,120 L237,120" stroke-width="2.4"/>' + back(110, 128, SKY, 1.0))
card('marien', '手繪港邊的展望塔，晚上看工廠的燈和大船',
     BOX.format(c=NIGHT) + sea(110, '#3e4f86')
     + ''.join(f'<rect x="{x}" y="{110-h}" width="12" height="{h}" fill="#56628f" stroke-width="1.2"/><circle cx="{x+6}" cy="{110-h-4}" r="2.4" fill="{GOLD}" stroke="none"/>' for x, h in ((140, 30), (160, 44), (182, 24), (204, 36)))
     + f'<path d="M50,160 L56,40 L76,40 L82,160 Z" fill="#a9c7e3" stroke-width="1.8"/><rect x="46" y="32" width="40" height="14" rx="3" fill="{WHITE}" stroke-width="1.6"/>'
     + ship(110, 120, .8), bg=NIGHT)
card('minatonomieruoka', '手繪山坡上的公園展望台，下面是港口和大橋',
     BOX.format(c=SKYB) + sea(80)
     + f'<path d="M20,90 Q120,40 220,90" fill="none" stroke-width="3"/><path d="M60,70 L60,90 M180,70 L180,90" stroke-width="3"/>'
     + f'<path d="M3,120 Q120,104 237,120 L237,177 L3,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{PINK}" stroke-width="1"/>' for x, y in ((30, 140), (50, 152), (190, 146), (212, 138)))
     + f'<rect x="80" y="124" width="80" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(110, 104, RED, .8) + back(134, 104, GOLD, .8))
card('shonandaira', '手繪山頂的電視塔和展望台，遠方是海、島和富士山',
     BOX.format(c=SKYB) + fuji(130, 230, 92, 50) + sea(92) + f'<ellipse cx="60" cy="104" rx="18" ry="5" fill="{MTN}" stroke-width="1.2"/>'
     + f'<path d="M3,130 Q120,116 237,132 L237,177 L3,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<path d="M100,130 L108,36 L116,130 Z" fill="none" stroke="{RED}" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{101+i*.8},{120-i*16} L{115-i*.8},{120-i*16}" stroke="{RED}" stroke-width="1.6"/>' for i in range(5))
     + back(160, 118, PINK, .7))

# 0. 封面（首都圈頁、橫濱頁共用）：黃昏的港邊，紅白高塔、時鐘摩天輪、大橋與遠方富士山
import math as _m
_wh = f'<circle cx="520" cy="150" r="74" fill="none" stroke-width="2.4"/>'
for _i in range(16):
    _a = _m.pi * 2 * _i / 16
    _x, _y = 520 + 74 * _m.cos(_a), 150 + 74 * _m.sin(_a)
    _wh += f'<path d="M520,150 L{_x:.1f},{_y:.1f}" stroke-width="1"/><rect x="{_x-5:.1f}" y="{_y-4:.1f}" width="10" height="9" rx="2" fill="{PINK if _i % 2 else GOLD}" stroke-width="1"/>'
_wh += f'<circle cx="520" cy="150" r="22" fill="{WHITE}" stroke-width="1.8"/><path d="M520,150 L520,136 M520,150 L531,156" stroke-width="2.2"/>'
_wh += f'<path d="M496,236 L520,150 L544,236" fill="none" stroke-width="2.6"/>'
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="#f7d9b8"/>'
         + cloud(70, 60, 1.3) + cloud(600, 46, 1.0)
         + f'<circle cx="640" cy="110" r="22" fill="{GOLD}" stroke-width="1.8"/>'
         + f'<path d="M300,200 L360,150 L380,150 L440,200 Z" fill="#a9b8d8" stroke-width="1.6"/>'
         + f'<path d="M346,162 L360,150 L380,150 L394,162 q-8,5 -16,0 q-8,5 -16,0 Z" fill="{WHITE}" stroke-width="1.2"/>'
         + f'<path d="M3,200 L717,200 L717,262 L3,262 Z" fill="{SEA}" stroke="none"/><path d="M3,200 L717,200" stroke-width="1.6"/>'
         + f'<path d="M560,196 Q640,150 717,196" fill="none" stroke-width="2.6"/><path d="M600,176 L600,198 M680,176 L680,198" stroke-width="2.6"/><path d="M560,196 L717,196" stroke-width="2"/>'
         + bldgs(200, ((30, 28, 70), (62, 22, 50), (90, 30, 96), (250, 26, 60), (420, 24, 44), (446, 20, 64)))
         + f'<path d="M168,240 L178,64 L198,64 L208,240 Z" fill="{RED}" stroke-width="2"/>'
         + ''.join(f'<path d="M{171+i*1.2},{96+i*36} L{205-i*1.2},{96+i*36}" stroke="{WHITE}" stroke-width="4"/>' for i in range(4))
         + f'<rect x="158" y="48" width="60" height="20" rx="6" fill="{WHITE}" stroke-width="1.8"/>'
         + _wh
         + f'<path d="M300,232 L360,232 L352,246 L308,246 Z" fill="{WHITE}" stroke-width="1.6"/><rect x="320" y="218" width="20" height="14" rx="2" fill="{SKY}" stroke-width="1.4"/>'
         + f'<path d="M3,262 L717,262 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#efe2cf"/>'
         + f'<path d="M3,262 L717,262" stroke-width="2.4"/>'
         + f'<rect x="60" y="270" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(200, 232, RED, 1.6) + back(380, 236, SKY, 1.5) + back(560, 232, GOLD, 1.6))
F['hero'] = svg('kn-hero', 720, 330, '手繪插圖：黃昏的港邊，有紅白高塔、中間是時鐘的大摩天輪、跨海大橋和遠方的富士山，三個人站在欄杆邊看景色', _hero)

print(save(F, OUT), 'files')
