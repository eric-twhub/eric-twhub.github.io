# 沖繩觀景台頁（/okinawa/observation-decks/）的手繪插圖（2026-11-19）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物、不畫風獅爺。輸出 illust/sp/okinawa-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obs_helpers import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'okinawa-observation-decks')
C = Cards('ok')
TEAL = '#6fd0d6'
LAGOON = '#a6e6e3'
SAND = '#f3e3b8'


def sea(y):
    return band(y, TEAL, 1.2) + f'<path d="M3,{y} L237,{y} L237,{y+14} L3,{y+14} Z" fill="{LAGOON}" stroke="none"/>'


def gusuku(x0, x1, base, top):
    # 彎彎曲曲的石牆：上緣與下緣兩條平行曲線，中間是石塊紋
    m = (x0 + x1) / 2
    up = f'M{x0},{base} Q{x0+(m-x0)*0.5},{top-10} {m},{top} Q{m+(x1-m)*0.5},{top+12} {x1},{top-4}'
    lo = f'L{x1},{top+14} Q{m+(x1-m)*0.5},{top+30} {m},{top+18} Q{x0+(m-x0)*0.5},{top+8} {x0},{base+16} Z'
    return (f'<path d="{up} {lo}" fill="#e2d6bd" stroke-width="1.8"/>'
            + ''.join(f'<path d="M{x},{top+4+abs(x-m)*0.08} l10,0" stroke-width="1"/>' for x in range(int(x0) + 14, int(x1) - 14, 18)))


def palm(x, base, h=50):
    return (f'<path d="M{x},{base} Q{x+6},{base-h/2} {x+2},{base-h}" fill="none" stroke="{DBROWN}" stroke-width="4"/>'
            + ''.join(f'<path d="M{x+2},{base-h} q{dx},{dy} {dx*2},{dy*0.4}" fill="none" stroke="{DGREEN}" stroke-width="4"/>' for dx, dy in ((14, -8), (-14, -8), (12, 6), (-12, 6))))


# 城跡（勝連、中城、今歸仁）：弧形石牆與海
C.card('gusuku', '手繪山丘上彎彎曲曲的石牆城跡，人站在城牆上，遠方是藍綠色的海',
       BOX.format(c=SKYB) + cloud(170, 30, .8) + sea(70)
       + f'<path d="M3,177 L3,120 Q120,96 237,120 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + gusuku(40, 200, 140, 96) + back(120, 72, RED, .6))
# 海角公園：草地懸崖與海
C.card('cape', '手繪綠色草地的海角，懸崖下是藍綠色的大海，人坐在邊上的長椅看海',
       BOX.format(c=SKYB) + cloud(60, 34, .8) + sea(80)
       + f'<path d="M3,177 L3,110 L150,110 Q180,112 186,140 L200,177 Z" fill="#a9d48f" stroke-width="1.6"/>'
       + f'<path d="M150,110 Q180,112 186,140 L200,177 L176,177 Z" fill="#b9b2a3" stroke-width="1.4"/>'
       + f'<rect x="60" y="98" width="50" height="6" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(76, 80, GOLD, .6) + back(96, 80, SKY, .6))
# 燈塔
C.card('lighthouse', '手繪海邊岩岸上的白色燈塔，塔頂有人在看海',
       BOX.format(c=SKYB) + cloud(180, 34, .8) + sea(100)
       + f'<path d="M3,177 L3,130 Q80,120 150,134 L180,177 Z" fill="#b9b2a3" stroke-width="1.6"/>'
       + f'<path d="M88,130 L94,40 L114,40 L120,130 Z" fill="{WHITE}" stroke-width="1.8"/><rect x="88" y="28" width="32" height="14" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
       + f'<path d="M84,44 L124,44" stroke-width="2"/>' + back(104, 10, RED, .5))
# 跨海大橋與島
C.card('bridge', '手繪一條長長的橋跨過藍綠色的海通往小島，島上有沙灘',
       BOX.format(c=SKYB) + cloud(40, 30, .8) + sea(70)
       + f'<path d="M150,92 Q200,70 237,84 L237,100 L150,100 Z" fill="{MTN}" stroke-width="1.4"/><path d="M150,100 L237,100 L237,106 L150,106 Z" fill="{SAND}" stroke="none"/>'
       + f'<path d="M3,150 Q90,110 170,98" fill="none" stroke="{WHITE}" stroke-width="7"/><path d="M3,150 Q90,110 170,98" fill="none" stroke-width="1.4"/>'
       + ''.join(f'<path d="M{x},{150-(x-3)*0.3} L{x},{170}" stroke-width="1.6"/>' for x in (30, 70, 110))
       + f'<path d="M3,177 L3,150 L80,177 Z" fill="{MTN}" stroke-width="1.4"/>' + back(30, 128, PINK, .6))
# 海中展望塔：水面下的窗與魚
C.card('undersea', '手繪伸到海裡的圓形展望塔，水面下的窗外有熱帶魚和珊瑚',
       BOX.format(c=SKYB) + band(60, TEAL, 1.2)
       + f'<path d="M3,40 L120,40 L120,48 L3,48 Z" fill="{BROWN}" stroke-width="1.4"/>'
       + f'<rect x="110" y="30" width="40" height="140" rx="16" fill="{WHITE}" stroke-width="1.8"/>'
       + ''.join(f'<circle cx="130" cy="{y}" r="8" fill="{SKY}" stroke-width="1.4"/>' for y in (100, 130))
       + ''.join(f'<path d="M{x},{y} q8,-6 16,0 q-8,6 -16,0 Z M{x+16},{y} l6,-5 l0,10 Z" fill="{c}" stroke-width="1"/>' for x, y, c in ((40, 100, GOLD), (170, 120, PINK), (60, 140, SKY), (190, 88, GOLD)))
       + ''.join(f'<path d="M{x},170 q-6,-16 0,-24 q6,8 0,24" fill="{PINK}" stroke-width="1"/>' for x in (30, 200, 220))
       + back(130, 16, RED, .5))
# 山頂展望（名護城、嘉津宇岳、八重岳）：山上看海灣與城市
C.card('mountain', '手繪山頂的木頭展望台，往下看是海灣旁的城市和遠方的海',
       BOX.format(c=SKYB) + cloud(170, 30, .8) + sea(76) + town(100, 9, '#eef0f4')
       + f'<path d="M3,177 L3,130 Q120,104 237,130 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<rect x="80" y="122" width="80" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/><path d="M86,130 L86,160 M154,130 L154,160" stroke-width="2.4"/>'
       + back(108, 100, RED, .7) + back(134, 100, GOLD, .7))
# 奇岩山（大石林山）
C.card('rocks', '手繪尖尖的灰色岩石山之間的步道與展望台，遠方是海',
       BOX.format(c=SKYB) + sea(80)
       + ''.join(f'<path d="M{x},150 L{x+12},{t} L{x+22},{t+10} L{x+32},150 Z" fill="#a59d8e" stroke-width="1.4"/>' for x, t in ((10, 70), (50, 90), (150, 76), (190, 96)))
       + band(150, MTN) + ''.join(f'<circle cx="{x}" cy="148" r="8" fill="{DGREEN}" stroke-width="1.2"/>' for x in (100, 124, 140))
       + back(112, 120, RED, .6))
# 塔（古宇利 Ocean Tower 等）
C.card('tower', '手繪島上山丘的白色展望塔，下面是長橋和藍綠色的海',
       BOX.format(c=SKYB) + cloud(40, 30, .8) + sea(96)
       + f'<path d="M3,96 Q60,80 110,96" fill="none" stroke="{WHITE}" stroke-width="5"/>'
       + f'<path d="M100,177 L120,110 Q170,90 237,108 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + tower(176, 40, 108, 9) + back(176, 18, GOLD, .5))
# 城市高處公園（那霸）
C.card('citypark', '手繪城市裡小山丘上的公園，紅瓦屋頂和白色大樓，遠方是港口',
       BOX.format(c=SKYB) + cloud(170, 30, .8) + sea(80)
       + ''.join(f'<rect x="{x}" y="{110-h}" width="18" height="{h}" fill="#eef0f4" stroke-width="1.2"/>' for x, h in ((20, 20), (46, 30), (180, 26), (206, 18)))
       + ''.join(f'<rect x="{x}" y="100" width="20" height="12" fill="#e8e2d4" stroke-width="1"/><path d="M{x-2},100 L{x+10},92 L{x+22},100 Z" fill="{BRICK}" stroke-width="1"/>' for x in (80, 110, 140))
       + f'<path d="M3,177 L3,134 Q120,114 237,134 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + palm(40, 140) + palm(200, 140) + back(120, 112, RED, .7))
# 封面：沖繩（藍綠色海、長橋與島、石牆城跡、燈塔、椰子樹）
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{SKYB}"/>'
         + cloud(80, 64, 1.3) + cloud(520, 50, 1.0) + f'<circle cx="650" cy="80" r="22" fill="{GOLD}" stroke-width="1.8"/>'
         + f'<path d="M3,160 L717,160 L717,236 L3,236 Z" fill="{TEAL}" stroke="none"/><path d="M3,160 L717,160 L717,176 L3,176 Z" fill="{LAGOON}" stroke="none"/>'
         + f'<path d="M500,166 Q580,130 680,150 L717,160 L500,166 Z" fill="{MTN}" stroke-width="1.6"/>'
         + f'<path d="M260,220 Q400,170 540,160" fill="none" stroke="{WHITE}" stroke-width="8"/><path d="M260,220 Q400,170 540,160" fill="none" stroke-width="1.6"/>'
         + f'<path d="M3,236 L3,180 Q100,150 240,186 L260,236 Z" fill="{MTN}" stroke-width="1.6"/>'
         + gusuku(30, 210, 214, 170)
         + f'<path d="M620,236 L626,150 L644,150 L650,236 Z" fill="{WHITE}" stroke-width="1.8"/><rect x="618" y="138" width="34" height="14" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
         + palm(300, 236, 70) + palm(560, 236, 60)
         + f'<path d="M3,236 L717,236 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="{SAND}"/>'
         + f'<path d="M3,236 L717,236" stroke-width="2.4"/><rect x="60" y="250" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(220, 220, RED, 1.6) + back(380, 224, SKY, 1.5) + back(540, 220, GOLD, 1.6))
C.hero('手繪插圖：沖繩藍綠色的海，長橋通往小島，山丘上有彎曲的石牆城跡、白色燈塔和椰子樹，三個人站在欄杆邊看海', _hero)

print(save(C.F, OUT), 'files')
