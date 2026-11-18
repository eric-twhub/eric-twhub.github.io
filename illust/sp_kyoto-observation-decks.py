# 京都觀景台頁（/kyoto/observation-decks/）新增展望點的手繪插圖（2026-11-18）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。輸出 illust/sp/kyoto-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'kyoto-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
SEA = '#9fd0ea'
MTN = '#9cc59a'
AUT = '#e8a05c'
F = {}
BOX = '<rect x="3" y="3" width="234" height="174" rx="22" fill="{c}"/>'
FLOOR = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('kt-' + name, W, H, label, inner, bg=bg)


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def hills(y, col=MTN):
    return f'<path d="M3,{y} Q50,{y-30} 100,{y-8} Q150,{y-34} 237,{y-6} L237,177 L3,177 Z" fill="{col}" stroke-width="1.6"/>'


def town(base, n=9, col='#e9e1d3'):
    t = ''
    for i in range(n):
        x = 14 + i * 24
        h = 8 + (i * 7) % 12
        t += f'<rect x="{x}" y="{base-h}" width="18" height="{h}" fill="{col}" stroke-width="1.2"/><path d="M{x-2},{base-h} L{x+9},{base-h-6} L{x+20},{base-h} Z" fill="#7d7f8f" stroke-width="1.2"/>'
    return t


def maple(x, y, s=1.0, col=AUT):
    return f'<circle cx="{x}" cy="{y}" r="{10*s}" fill="{col}" stroke-width="1.4"/><path d="M{x},{y+8*s} L{x},{y+20*s}" stroke-width="2"/>'


def sandbar(y):
    # 天橋立：海中細長松樹砂洲
    return (f'<path d="M3,{y} L237,{y} {FLOOR}" fill="{SEA}"/>'
            f'<path d="M30,{y+40} Q120,{y+18} 210,{y+6}" fill="none" stroke="#e9dcb5" stroke-width="9"/>'
            + ''.join(f'<circle cx="{x}" cy="{y+40-(x-30)*.19}" r="4" fill="{DGREEN}" stroke-width="1"/>' for x in range(36, 210, 12)))


def chairlift(x0, y0, x1, y1):
    t = f'<path d="M{x0},{y0} L{x1},{y1}" stroke-width="1.6"/>'
    for k in (0.3, 0.65):
        x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
        t += f'<path d="M{x},{y} L{x},{y+12}" stroke-width="1.4"/><path d="M{x-8},{y+12} L{x+8},{y+12} L{x+8},{y+18}" fill="none" stroke-width="2"/>'
    return t


# Garden Museum 比叡：山上庭園、花、遠方的湖
card('gmhiei', '手繪山頂上的花園，花圃後面有小展望塔，遠方是湖和城市',
     BOX.format(c=SKYB) + cloud(40, 34, .9) + f'<path d="M3,74 L237,74 L237,96 L3,96 Z" fill="{SEA}" stroke-width="1.2"/>'
     + town(96, 9, '#eef0f4')
     + f'<path d="M3,112 Q120,98 237,114 L237,177 L3,177 Z" fill="#a9d48f" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}" stroke-width="1"/>' for x, y, c in ((30, 140, PINK), (50, 150, GOLD), (70, 138, RED), (170, 146, PINK), (196, 136, GOLD), (214, 152, '#b7a3e0')))
     + f'<rect x="120" y="78" width="22" height="46" rx="3" fill="#e8e2d4" stroke-width="1.6"/><path d="M114,78 L148,78 L131,66 Z" fill="{BROWN}" stroke-width="1.6"/>'
     + back(96, 124, RED, .8) + back(150, 128, SKY, .8))
# 天橋立 View Land：彎腰倒看（股のぞき）
card('viewland', '手繪山上的人彎腰從腳下倒看海上細長的松樹砂洲',
     BOX.format(c=SKYB) + cloud(170, 32, .9) + sandbar(70)
     + f'<path d="M3,138 Q120,126 237,140 L237,177 L3,177 Z" fill="#a9d48f" stroke-width="1.6"/>'
     + f'<rect x="94" y="132" width="52" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>'
     + f'<path d="M112,132 L116,112 M128,132 L124,112" stroke-width="3"/><path d="M110,112 Q120,96 130,112 Z" fill="{RED}" stroke-width="1.4"/>'
     + f'<circle cx="120" cy="120" r="6" fill="{DBROWN}"/>')
# 傘松公園：纜車與吊椅上山、Sky Deck
card('kasamatsu', '手繪纜車和吊椅開上山，山上圓形平台往下看海上的松樹砂洲',
     BOX.format(c=SKYB) + sandbar(64)
     + f'<path d="M3,150 L150,150 L237,96 L237,177 L3,177 Z" fill="#a9d48f" stroke-width="1.6"/>'
     + chairlift(40, 150, 200, 100)
     + f'<ellipse cx="200" cy="100" rx="30" ry="7" fill="#e8e2d4" stroke-width="1.6"/>' + back(196, 78, PINK, .8))
# 五老 Sky Tower：山頂塔、谷灣海岸、船
card('goro', '手繪山頂的白色高塔，下面是彎彎曲曲的海灣和小船，旁邊有雲海',
     BOX.format(c=SKYB) + f'<path d="M3,96 Q40,80 70,100 Q110,124 150,96 Q190,72 237,92 L237,177 L3,177 Z" fill="{SEA}" stroke-width="1.4"/>'
     + f'<path d="M3,120 Q60,104 110,130 Q170,150 237,120 L237,177 L3,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + cloud(20, 118, .8, '#f2f2f2') + cloud(190, 128, .8, '#f2f2f2')
     + f'<path d="M108,128 L114,40 L126,40 L132,128 Z" fill="{WHITE}" stroke-width="1.8"/><rect x="104" y="36" width="32" height="16" rx="4" fill="{SKY}" stroke-width="1.6"/>'
     + f'<path d="M150,92 L180,92 L176,99 L154,99 Z" fill="{GRAY}" stroke-width="1.2"/>')
# 嵐山 Monkey Park：山上休息處看城市
card('monkeypark', '手繪山上的木頭休息處，前面坐著小猴子，遠方是城市和小小的塔',
     BOX.format(c=SKYB) + town(92, 9, '#eef0f4')
     + f'<path d="M150,92 L152,62 L158,62 L160,92 Z" fill="{WHITE}" stroke-width="1.4"/><circle cx="155" cy="60" r="5" fill="{RED}" stroke-width="1.2"/>'
     + f'<path d="M3,110 Q120,96 237,112 L237,177 L3,177 Z" fill="{AUT}" stroke-width="1.6"/>'
     + f'<rect x="30" y="118" width="90" height="10" rx="3" fill="{BROWN}" stroke-width="1.4"/>'
     + f'<circle cx="170" cy="134" r="14" fill="#b8835a" stroke-width="1.6"/><circle cx="170" cy="118" r="11" fill="#b8835a" stroke-width="1.6"/>'
     + f'<ellipse cx="170" cy="120" rx="7" ry="6" fill="#f2b8a8" stroke-width="1"/>' + face(170, 120, .5)
     + back(60, 104, GOLD, .8))
# 嵐山公園 龜山地區：紅葉山林、河谷
card('kameyama', '手繪紅葉的山坡上有木頭展望台，下面是流過山谷的河',
     BOX.format(c=SKYB) + f'<path d="M3,40 L80,120 L3,177 Z" fill="{MTN}" stroke-width="1.6"/><path d="M237,30 L150,120 L237,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<path d="M80,177 Q110,120 150,120 L120,177 Z" fill="{SEA}" stroke-width="1.4"/>'
     + maple(30, 90) + maple(50, 120, .8, RED) + maple(200, 80) + maple(214, 118, .8, RED)
     + f'<rect x="60" y="138" width="60" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/><path d="M64,146 L64,170 M116,146 L116,170" stroke-width="2.4"/>'
     + back(90, 116, RED, .8))
# 伏見稻荷 荒神峰：鳥居與城市
card('inari_kojin', '手繪山上一排紅色鳥居，鳥居後方視野打開，看得到遠方的城市',
     BOX.format(c=SKYB) + town(84, 9, '#eef0f4')
     + f'<path d="M3,100 Q120,90 237,104 L237,177 L3,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},{170} L{x},{120-i*4} M{x+30},{170} L{x+30},{120-i*4}" stroke="{RED}" stroke-width="5"/>'
               f'<path d="M{x-6},{118-i*4} L{x+36},{118-i*4}" stroke="{RED}" stroke-width="6"/>' for i, x in enumerate((20, 70, 120)))
     + back(190, 110, PINK, .8))
# 大吉山：山上展望台看宇治的街
card('daikichi', '手繪山頂的木頭展望台，下面是河邊的小鎮和一座橋',
     BOX.format(c=SKYB) + f'<path d="M3,96 L237,96 L237,112 L3,112 Z" fill="{SEA}" stroke-width="1.2"/>'
     + f'<path d="M60,104 L180,104" stroke="{BROWN}" stroke-width="4"/>' + town(96, 9, '#eef0f4')
     + f'<path d="M3,124 Q120,110 237,126 L237,177 L3,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<rect x="80" y="128" width="80" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(110, 108, GOLD, .8) + back(134, 110, SKY, .8))
# 天王山：三條河匯流
card('tennozan', '手繪山腰的展望處，往下看三條河匯合成一條大河，遠方有大樓',
     BOX.format(c=SKYB) + ''.join(f'<rect x="{x}" y="{50-h}" width="10" height="{h+10}" fill="#d6dbe6" stroke-width="1.2"/>' for x, h in ((170, 20), (184, 30), (198, 14)))
     + f'<path d="M3,60 L237,60 L237,130 L3,130 Z" fill="#e6efd9" stroke="none"/>'
     + f'<path d="M20,64 Q80,96 120,104 M40,128 Q90,112 120,104 M200,70 Q160,100 120,104 M120,104 Q150,120 230,128" fill="none" stroke="{SEA}" stroke-width="7"/>'
     + f'<path d="M3,134 Q120,124 237,138 L237,177 L3,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<path d="M60,148 q8,-30 0,-40" stroke="{DBROWN}" stroke-width="3" fill="none"/><circle cx="58" cy="104" r="12" fill="{DGREEN}" stroke-width="1.4"/>'
     + back(110, 130, RED, .8))
# 甘南備山：山頂展望台
card('kannabi', '手繪森林山頂的展望台，遠方是平原上的城市',
     BOX.format(c=SKYB) + cloud(60, 34, .8) + town(88, 9, '#eef0f4')
     + f'<path d="M3,100 L237,100 L237,177 L3,177 Z" fill="#cfe6c0" stroke="none"/>'
     + ''.join(f'<path d="M{x},{150} L{x+12},{118} L{x+24},{150} Z" fill="{DGREEN}" stroke-width="1.4"/>' for x in (6, 30, 186, 210))
     + f'<path d="M70,177 L90,120 L150,120 L170,177 Z" fill="{BROWN}" stroke-width="1.6"/><rect x="84" y="112" width="72" height="10" rx="2" fill="#e8e2d4" stroke-width="1.4"/>'
     + back(108, 92, GOLD, .8) + back(132, 92, PINK, .8))

print(save(F, OUT), 'files')
