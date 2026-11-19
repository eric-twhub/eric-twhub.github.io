# 靜岡觀景台頁（/shizuoka/observation-decks/）的手繪插圖（2026-11-19）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。輸出 illust/sp/shizuoka-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obs_helpers import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'shizuoka-observation-decks')
C = Cards('sz')
FUJI = '#8fa8c8'
SNOWR = '#f4f7fb'
TEA = '#7fb069'


def fuji(cx, base, w=70, h=50):
    # 富士山：藍色山體＋山頂的雪
    return (f'<path d="M{cx-w},{base} L{cx-w*0.18},{base-h} L{cx+w*0.18},{base-h} L{cx+w},{base} Z" fill="{FUJI}" stroke-width="1.6"/>'
            f'<path d="M{cx-w*0.42},{base-h*0.6} L{cx-w*0.18},{base-h} L{cx+w*0.18},{base-h} L{cx+w*0.42},{base-h*0.6} '
            f'L{cx+w*0.25},{base-h*0.52} L{cx+w*0.1},{base-h*0.62} L{cx-w*0.05},{base-h*0.5} L{cx-w*0.22},{base-h*0.62} Z" fill="{SNOWR}" stroke-width="1.4"/>')


def pine(x, base, s=1.0):
    return (f'<path d="M{x},{base} L{x+4*s},{base-30*s}" stroke="{DBROWN}" stroke-width="{3*s}"/>'
            f'<ellipse cx="{x+4*s}" cy="{base-32*s}" rx="{16*s}" ry="{6*s}" fill="{DGREEN}" stroke-width="1.2"/>'
            f'<ellipse cx="{x+10*s}" cy="{base-22*s}" rx="{12*s}" ry="{5*s}" fill="{DGREEN}" stroke-width="1.2"/>')


# 公家大樓的富士山展望大廳（縣廳等）
C.card('office', '手繪大樓最上層的大窗戶，窗外是城市和遠方的富士山',
       BOX.format(c=SKYB) + fuji(170, 104, 60, 46) + town(130, 9, '#eef0f4')
       + f'<rect x="20" y="40" width="80" height="120" fill="#e8e2d4" stroke-width="1.8"/><rect x="24" y="44" width="72" height="16" fill="{SKY}" stroke-width="1.2"/>'
       + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{WHITE}" stroke-width="1"/>' for x in (30, 54, 78) for y in (72, 96, 120))
       + band(160, '#cfc6b6') + back(50, 24, RED, .5) + back(72, 24, GOLD, .5))
# 山上的木造展望迴廊，看富士山與海（日本平夢テラス等）
C.card('terrace', '手繪山頂上的木造展望迴廊，遠方是富士山，下面是海灣和茶園',
       BOX.format(c=SKYB) + cloud(40, 34, .7) + fuji(160, 90, 64, 48) + band(90, SEA, 1.2)
       + f'<path d="M3,177 L3,128 Q120,110 237,128 L237,155 Q237,177 215,177 Z" fill="{TEA}" stroke-width="1.6"/>'
       + ''.join(f'<path d="M{x},146 q14,-8 28,0" fill="none" stroke="{DGREEN}" stroke-width="2"/>' for x in (14, 60, 160, 200))
       + f'<path d="M70,128 L170,128 L160,108 L80,108 Z" fill="#d6c3a8" stroke-width="1.6"/>'
       + ''.join(f'<path d="M{x},108 L{x},128" stroke="{BROWN}" stroke-width="1.2"/>' for x in range(86, 160, 10))
       + back(110, 88, RED, .55) + back(132, 88, SKY, .55))
# 纜車上山（久能山、舘山寺、十國峠等）
C.card('ropeway', '手繪綠色山坡上的纜車，往山頂開，遠方是海',
       BOX.format(c=SKYB) + cloud(180, 30, .8) + band(90, SEA, 1.2)
       + f'<path d="M3,177 L3,120 L150,40 L237,90 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + ropeway(20, 150, 150, 46, RED, .5) + back(160, 26, GOLD, .5))
# 海邊松林看富士山（三保松原等）
C.card('pinebeach', '手繪海邊的松樹林與沙灘，海的另一邊是富士山',
       BOX.format(c=SKYB) + fuji(140, 92, 70, 52) + band(92, SEA, 1.2)
       + f'<path d="M3,177 L3,140 Q120,128 237,140 L237,155 Q237,177 215,177 Z" fill="#efe2bf" stroke-width="1.6"/>'
       + pine(30, 142) + pine(60, 138, .9) + pine(196, 140, 1.1)
       + ''.join(f'<path d="M{x},{y} q8,-6 16,0" fill="none" stroke="{WHITE}" stroke-width="2"/>' for x, y in ((90, 120), (130, 128)))
       + back(120, 132, RED, .55))
# 高樓展望迴廊（濱松 Act Tower 等）
C.card('highrise', '手繪城市裡特別高的大樓，最上層一圈是展望迴廊，遠方是湖和海',
       BOX.format(c=SKYB) + cloud(50, 36, .8) + band(110, SEA, 1.2) + town(150, 9, '#eef0f4')
       + f'<path d="M100,160 L104,40 Q120,24 136,40 L140,160 Z" fill="#dfe6ee" stroke-width="1.8"/>'
       + ''.join(f'<path d="M{106 + i * 6},50 L{106 + i * 6},156" stroke-width=".8"/>' for i in range(5))
       + f'<rect x="100" y="52" width="40" height="10" fill="{SKY}" stroke-width="1.2"/>' + band(160, '#cfc6b6')
       + back(120, 36, RED, .4))
# 城的天守（濱松城、掛川城、熱海城等）
C.card('castle', '手繪石垣上的白牆天守，前面有松樹，遠方是城市',
       BOX.format(c=SKYB) + cloud(180, 34, .8) + band(150, GREEN) + castle(120, 150, .9)
       + ''.join(f'<circle cx="{x}" cy="142" r="9" fill="{DGREEN}" stroke-width="1.2"/>' for x in (30, 54, 186, 210)))
# 海邊城：熱海城一類，海與溫泉街
C.card('seacastle', '手繪海邊山丘上的城，下面是溫泉街的房子和海灣',
       BOX.format(c=SKYB) + band(100, SEA, 1.2)
       + f'<path d="M3,177 L3,90 L110,70 L237,110 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + castle(90, 84, .7) + town(160, 7, '#f4e7d8', 100, 20)
       + ''.join(f'<path d="M{x},150 q3,-8 0,-14" fill="none" stroke="{WHITE}" stroke-width="1.6"/>' for x in (120, 160, 200)))
# 港口的水門展望塔（沼津港びゅうお等）
C.card('watergate', '手繪港口巨大的水門，上面是展望台，遠方是富士山和漁船',
       BOX.format(c=SKYB) + fuji(60, 96, 56, 42) + band(96, SEA, 1.2)
       + f'<rect x="120" y="30" width="18" height="130" fill="#e8e2d4" stroke-width="1.6"/><rect x="196" y="30" width="18" height="130" fill="#e8e2d4" stroke-width="1.6"/>'
       + f'<rect x="116" y="22" width="102" height="18" rx="3" fill="{SKY}" stroke-width="1.6"/><rect x="138" y="60" width="58" height="50" fill="#c9d4e6" stroke-width="1.4"/>'
       + f'<path d="M20,140 L70,140 L62,152 L28,152 Z" fill="{WHITE}" stroke-width="1.4"/>'
       + back(150, 6, RED, .45) + back(176, 6, GOLD, .45))
# 吊橋（三島 Skywalk 等）
C.card('suspension', '手繪山谷之間長長的白色吊橋，遠方是富士山',
       BOX.format(c=SKYB) + fuji(170, 84, 56, 42)
       + f'<path d="M3,177 L3,90 L40,90 L40,177 Z M200,177 L200,90 L237,90 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<path d="M40,90 Q120,128 200,90" fill="none" stroke-width="2.4"/><path d="M40,70 Q120,120 200,70" fill="none" stroke="{WHITE}" stroke-width="2"/>'
       + f'<path d="M36,70 L36,92 M204,70 L204,92" stroke="{WHITE}" stroke-width="4"/>'
       + ''.join(f'<path d="M{x},{100 + (abs(x - 120) * -0.24 + 9)} L{x},{78 + abs(x - 120) * -0.2 + 22}" stroke-width=".8"/>' for x in range(60, 190, 20))
       + f'<path d="M3,177 L237,177" stroke-width="1"/>' + back(110, 100, RED, .5) + back(130, 102, SKY, .5))
# 圓圓的火山（大室山等），搭吊椅上去
C.card('volcano', '手繪像倒扣的碗一樣圓圓的綠色山，吊椅沿著斜坡往山頂，遠方是海和島',
       BOX.format(c=SKYB) + band(80, SEA, 1.2) + islands(96, ((40, 14), (200, 18)), MTN)
       + f'<path d="M30,177 Q40,70 120,64 Q200,70 210,177 Z" fill="{GREEN}" stroke-width="1.8"/>'
       + f'<path d="M84,70 Q120,58 156,70" fill="none" stroke="{DGREEN}" stroke-width="3"/>'
       + f'<path d="M150,170 L120,66" stroke-width="1.2"/>'
       + ''.join(f'<rect x="{x-5}" y="{y}" width="10" height="7" fill="{RED}" stroke-width="1"/>' for x, y in ((141, 134), (132, 104)))
       + back(100, 46, GOLD, .5) + back(124, 46, SKY, .5))
# 機場觀景台（富士山靜岡機場）
C.card('airport', '手繪機場屋頂的觀景台，飛機在跑道上起飛，遠方是富士山和茶園',
       BOX.format(c=SKYB) + fuji(170, 92, 60, 44) + band(100, TEA) + band(130, '#cfc6b6')
       + f'<path d="M3,146 L237,146" stroke="{WHITE}" stroke-width="3" stroke-dasharray="12 10"/>'
       + f'<g transform="translate(40,50) rotate(-10)"><rect x="0" y="0" width="60" height="11" rx="5" fill="{WHITE}" stroke-width="1.8"/>'
         f'<path d="M22,6 L12,26 L28,26 L38,6 Z" fill="{WHITE}" stroke-width="1.4"/><path d="M4,6 L0,-8 L8,-8 L14,2 Z" fill="{SKY}" stroke-width="1.4"/></g>'
       + f'<rect x="130" y="120" width="90" height="8" rx="2" fill="#e8e2d4" stroke-width="1.4"/>' + back(160, 98, RED, .7) + back(190, 98, GOLD, .7))
# 湖（濱名湖等）
C.card('lake', '手繪山上的展望台往下看，一大片湖，湖上有小船，遠方是海',
       BOX.format(c=SKYB) + cloud(180, 34, .8) + band(70, SEA, 1.2)
       + f'<path d="M3,96 Q120,80 237,96 L237,150 L3,150 Z" fill="#a9d8ea" stroke-width="1.4"/>'
       + f'<path d="M60,120 L90,120 L84,128 L66,128 Z" fill="{WHITE}" stroke-width="1.2"/><path d="M150,110 L176,110 L170,116 L156,116 Z" fill="{WHITE}" stroke-width="1.2"/>'
       + f'<path d="M3,177 L3,148 Q120,136 237,148 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<rect x="80" y="142" width="80" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(106, 124, RED, .6) + back(134, 124, SKY, .6))

# 封面：茶園、海與富士山
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{SKYB}"/>'
         + cloud(80, 64, 1.3) + cloud(600, 50, 1.0)
         + fuji(380, 190, 220, 150)
         + f'<path d="M3,190 L717,190 L717,214 L3,214 Z" fill="{SEA}" stroke="none"/>'
         + f'<path d="M3,236 L3,214 Q360,196 717,214 L717,236 Z" fill="{TEA}" stroke-width="1.6"/>'
         + ''.join(f'<path d="M{x},228 q20,-10 40,0" fill="none" stroke="{DGREEN}" stroke-width="2.4"/>' for x in range(20, 700, 60))
         + pine(60, 214, 1.4) + pine(640, 214, 1.3)
         + f'<path d="M3,236 L717,236 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#efe2cf"/>'
         + f'<path d="M3,236 L717,236" stroke-width="2.4"/><rect x="60" y="250" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(220, 220, RED, 1.6) + back(380, 224, SKY, 1.5) + back(540, 220, GOLD, 1.6))
C.hero('手繪插圖：大大的富士山，前面是海和一排排的茶園，三個人站在欄杆邊看', _hero)

# 港邊的摩天輪（清水 Dream Plaza 等），遠方富士山
C.card('wheel', '手繪港邊的大摩天輪，旁邊是海和船，遠方是富士山',
       BOX.format(c=SKYB) + fuji(60, 100, 56, 42) + band(110, SEA, 1.2)
       + f'<circle cx="160" cy="78" r="52" fill="none" stroke-width="2.2"/><circle cx="160" cy="78" r="6" fill="{WHITE}" stroke-width="1.6"/>'
       + ''.join(f'<path d="M160,78 L{160 + 52 * c:.1f},{78 + 52 * s:.1f}" stroke-width="1"/>'
                 f'<rect x="{160 + 52 * c - 6:.1f}" y="{78 + 52 * s - 5:.1f}" width="12" height="10" rx="2" fill="{col}" stroke-width="1.2"/>'
                 for c, s, col in ((1, 0, RED), (.5, .866, GOLD), (-.5, .866, SKY), (-1, 0, PINK), (-.5, -.866, GREEN), (.5, -.866, RED)))
       + f'<path d="M140,160 L160,90 L180,160" fill="none" stroke-width="2.4"/>'
       + f'<path d="M20,140 L70,140 L62,152 L28,152 Z" fill="{WHITE}" stroke-width="1.4"/>' + band(160, '#cfc6b6')
       + back(100, 150, GOLD, .5) + back(120, 152, SKY, .5))
# 海岬上的白色燈塔（御前埼燈塔、門脇埼燈塔等）
C.card('lighthouse', '手繪海岬上的白色燈塔，下面是岩岸和浪花',
       BOX.format(c=SKYB) + band(96, SEA, 1.2)
       + f'<path d="M3,177 L3,120 Q60,100 120,112 Q180,104 237,128 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<path d="M108,112 L114,40 L134,40 L140,112 Z" fill="{WHITE}" stroke-width="1.8"/>'
       + f'<rect x="110" y="28" width="28" height="14" rx="3" fill="{GOLD}" stroke-width="1.6"/><path d="M106,28 L124,14 L142,28 Z" fill="{RED}" stroke-width="1.6"/>'
       + f'<path d="M104,44 L144,44" stroke-width="2"/>'
       + ''.join(f'<path d="M{x},130 q6,-8 12,0" fill="none" stroke="{WHITE}" stroke-width="1.6"/>' for x in (20, 50, 190, 214))
       + back(70, 100, RED, .5) + back(170, 100, GOLD, .5))
print(save(C.F, OUT), 'files')
