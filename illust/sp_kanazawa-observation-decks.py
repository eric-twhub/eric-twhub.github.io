# 金澤觀景台頁（/kanazawa/observation-decks/）的手繪插圖（2026-11-19）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。輸出 illust/sp/kanazawa-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obs_helpers import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'kanazawa-observation-decks')
C = Cards('kz')
LEAD = '#9fb0b8'   # 金澤城一帶的鉛瓦屋頂
SNOWR = '#f4f7fb'


def yukizuri(x, base, h=60, col=DGREEN):
    # 雪吊：樹頂中間一根柱子，拉出放射狀的繩子
    t = f'<path d="M{x-30},{base} Q{x},{base-h-10} {x+30},{base} Z" fill="{col}" stroke-width="1.6"/>'
    t += f'<path d="M{x},{base} L{x},{base-h-20}" stroke="{BROWN}" stroke-width="2.4"/>'
    t += ''.join(f'<path d="M{x},{base-h-20} L{x+dx},{base-6}" stroke="{GOLD}" stroke-width="1"/>' for dx in (-28, -18, -8, 8, 18, 28))
    return t


def gassho(x, base, s=1.0, snow=False):
    # 合掌造：很陡的三角形茅草屋頂
    roof = SNOWR if snow else '#c9a46a'
    return (f'<rect x="{x-16*s}" y="{base-14*s}" width="{32*s}" height="{14*s}" fill="#d9c7a8" stroke-width="1.4"/>'
            f'<path d="M{x-20*s},{base-14*s} L{x},{base-46*s} L{x+20*s},{base-14*s} Z" fill="{roof}" stroke-width="1.6"/>'
            f'<rect x="{x-4*s}" y="{base-30*s}" width="{8*s}" height="{6*s}" fill="{WHITE}" stroke-width="1"/>')


# 公家大樓最上層的展望大廳（石川縣廳、富山市役所、福井縣廳等）
C.card('office', '手繪高高的公家大樓，最上層一排大窗是展望大廳，遠方是城市和海',
       BOX.format(c=SKYB) + cloud(180, 34, .8) + band(120, SEA, 1.2) + town(140, 9, '#eef0f4')
       + f'<rect x="80" y="30" width="80" height="130" fill="#e8e2d4" stroke-width="1.8"/><rect x="84" y="34" width="72" height="16" fill="{SKY}" stroke-width="1.2"/>'
       + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{WHITE}" stroke-width="1"/>' for x in (90, 114, 138) for y in (62, 86, 110, 134))
       + band(160, '#cfc6b6') + back(110, 14, RED, .5) + back(132, 14, GOLD, .5))
# 山丘公園往下看城市與日本海（卯辰山等）
C.card('hillpark', '手繪山丘公園的展望台，往下看是一整片瓦屋頂的城市，遠方是海',
       BOX.format(c=SKYB) + cloud(50, 34, .8) + band(76, SEA, 1.2)
       + ''.join(f'<path d="M{x},{y} l10,-8 l10,8 Z" fill="{LEAD}" stroke-width="1"/><rect x="{x+2}" y="{y}" width="16" height="7" fill="#efe8da" stroke-width="1"/>'
                 for x in range(10, 230, 22) for y in (100, 118))
       + f'<path d="M3,177 L3,140 Q120,124 237,140 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<rect x="80" y="134" width="80" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>'
       + ''.join(f'<circle cx="{x}" cy="140" r="9" fill="{AUT}" stroke-width="1.2"/>' for x, AUT in ((26, '#e8a05c'), (212, '#d9634a')))
       + back(104, 116, RED, .6) + back(132, 116, SKY, .6))
# 日式庭園的眺望台：雪吊的松樹、池子、兩隻腳的石燈籠
C.card('garden', '手繪日式庭園，松樹用繩子吊成傘狀，池邊有兩隻腳的石燈籠，遠方是山',
       BOX.format(c=SKYB) + f'<path d="M3,80 L70,46 L130,72 L190,40 L237,64 L237,90 L3,90 Z" fill="{MTN}" stroke-width="1.4"/>'
       + band(110, '#bcd99a') + f'<ellipse cx="130" cy="146" rx="80" ry="18" fill="{SEA}" stroke-width="1.6"/>'
       + yukizuri(46, 128, 50) + yukizuri(200, 124, 44)
       + f'<path d="M108,140 L104,160 M122,140 L132,162" stroke="#8a8274" stroke-width="3"/>'
       + f'<rect x="104" y="124" width="22" height="14" fill="#b9b2a3" stroke-width="1.4"/><path d="M98,124 L115,112 L132,124 Z" fill="#a59d8e" stroke-width="1.4"/>'
       + back(170, 96, GOLD, .55))
# 白牆鉛瓦的城（金澤城、丸岡城等）
C.card('castle', '手繪石垣上的白牆城樓，屋頂是淡灰色的瓦，前面有松樹',
       BOX.format(c=SKYB) + cloud(180, 34, .8) + band(150, GREEN) + castle(120, 150, .9, WHITE, LEAD)
       + ''.join(f'<circle cx="{x}" cy="142" r="9" fill="{DGREEN}" stroke-width="1.2"/>' for x in (30, 54, 186, 210)))
# 港口航廈屋頂（金澤港等）
C.card('port', '手繪港邊航廈的屋頂甲板，前面停著大船，遠方是海和夕陽',
       BOX.format(c=DUSK) + f'<circle cx="190" cy="56" r="16" fill="{GOLD}" stroke-width="1.6"/>' + band(90, SEA, 1.2)
       + f'<path d="M110,96 L220,96 L208,116 L118,116 Z" fill="{WHITE}" stroke-width="1.6"/><rect x="140" y="80" width="50" height="16" fill="{WHITE}" stroke-width="1.4"/>'
       + ''.join(f'<rect x="{x}" y="84" width="6" height="6" fill="{SKY}" stroke-width=".8"/>' for x in (146, 158, 170, 182))
       + f'<path d="M3,177 L3,128 L120,128 L120,177 Z" fill="#e8e2d4" stroke-width="1.6"/><path d="M3,128 L130,128" stroke-width="2"/>'
       + ''.join(f'<path d="M{x},120 L{x},128" stroke-width="1.2"/>' for x in range(10, 125, 12)) + f'<path d="M3,120 L124,120" stroke-width="1.4"/>'
       + back(50, 100, RED, .6) + back(80, 100, SKY, .6))
# 機場觀景台
C.card('airport', '手繪機場屋頂的觀景台，飛機在跑道上起飛，遠方是山',
       BOX.format(c=SKYB) + cloud(40, 40, .8) + f'<path d="M3,100 L60,70 L120,92 L180,64 L237,90 L237,104 L3,104 Z" fill="{MTN}" stroke-width="1.4"/>' + band(130, '#cfc6b6')
       + f'<path d="M3,146 L237,146" stroke="{WHITE}" stroke-width="3" stroke-dasharray="12 10"/>'
       + f'<g transform="translate(140,60) rotate(-12)"><rect x="0" y="0" width="60" height="11" rx="5" fill="{WHITE}" stroke-width="1.8"/>'
         f'<path d="M22,6 L12,26 L28,26 L38,6 Z" fill="{WHITE}" stroke-width="1.4"/><path d="M4,6 L0,-8 L8,-8 L14,2 Z" fill="{SKY}" stroke-width="1.4"/></g>'
       + f'<rect x="20" y="120" width="90" height="8" rx="2" fill="#e8e2d4" stroke-width="1.4"/>' + back(50, 98, RED, .7) + back(80, 98, GOLD, .7))
# 大樓上的展望塔，背後是雪山（富山市役所展望塔等）
C.card('tower', '手繪城市大樓頂上的細長展望塔，背後是一整排積雪的高山',
       BOX.format(c=SKYB) + f'<path d="M3,96 L40,50 L70,74 L110,36 L150,70 L190,44 L237,80 L237,104 L3,104 Z" fill="{SNOWR}" stroke-width="1.6"/>'
       + f'<path d="M3,104 L237,104 L237,112 L3,112 Z" fill="{MTN}" stroke="none"/>' + town(150, 9, '#eef0f4')
       + f'<rect x="90" y="96" width="60" height="64" fill="#e8e2d4" stroke-width="1.6"/>' + tower(120, 46, 96, 7, WHITE, SKY)
       + band(160, '#cfc6b6') + back(120, 26, RED, .45))
# 運河上的橋，兩端是展望塔（富岩運河環水公園天門橋等）
C.card('bridge', '手繪運河上的一座橋，橋的兩端各有一座小展望塔，水面映著燈',
       BOX.format(c=DUSK) + band(120, SEA, 1.2)
       + f'<rect x="40" y="60" width="26" height="70" fill="{WHITE}" stroke-width="1.6"/><rect x="174" y="60" width="26" height="70" fill="{WHITE}" stroke-width="1.6"/>'
       + f'<path d="M36,60 L53,46 L70,60 Z M170,60 L187,46 L204,60 Z" fill="{RED}" stroke-width="1.4"/>'
       + f'<path d="M66,80 L174,80" stroke-width="3"/><path d="M66,90 L174,90" stroke-width="1.6"/>'
       + ''.join(f'<path d="M{x},140 l0,10" stroke="{GOLD}" stroke-width="2"/>' for x in range(60, 190, 16))
       + f'<path d="M3,177 L3,160 L237,160 L237,155 Q237,177 215,177 Z" fill="{GREEN}" stroke-width="1.4"/>'
       + back(100, 62, SKY, .5) + back(130, 62, GOLD, .5))
# 海邊柱狀岩斷崖旁的展望塔（東尋坊等）
C.card('cliff', '手繪海邊一根根柱子般的岩石斷崖，旁邊有一座細長的展望塔，海浪拍上來',
       BOX.format(c=SKYB) + cloud(60, 32, .8) + band(100, SEA, 1.2)
       + ''.join(f'<rect x="{x}" y="{y}" width="14" height="{177-y}" fill="#8f8a80" stroke-width="1.2"/>'
                 for x, y in ((3, 116), (17, 108), (31, 112), (45, 104), (59, 110), (73, 118), (87, 124)))
       + ''.join(f'<path d="M{x},{y} q8,-8 16,0" fill="none" stroke="{WHITE}" stroke-width="2.4"/>' for x, y in ((110, 132), (140, 148), (170, 128)))
       + tower(200, 30, 140, 8, WHITE, SKY) + f'<path d="M150,177 L150,140 L237,140 L237,155 Q237,177 215,177 Z" fill="{GREEN}" stroke-width="1.4"/>'
       + back(200, 12, RED, .45))
# 從山上的展望台看合掌村（白川鄉、五箇山）
C.card('village', '手繪從山上的展望台往下看，田地之間散著一棟棟尖屋頂的合掌造房子，屋頂上有雪',
       BOX.format(c=SKYB) + f'<path d="M3,70 L60,30 L120,62 L180,26 L237,60 L237,80 L3,80 Z" fill="{SNOWR}" stroke-width="1.4"/>'
       + band(80, SNOWB, 1.2)
       + ''.join(gassho(x, y, s, True) for x, y, s in ((40, 124, .8), (96, 112, .7), (150, 128, .9), (204, 114, .7), (120, 150, .8)))
       + f'<path d="M3,177 L3,160 Q40,150 80,160 L80,177 Z" fill="{DGREEN}" stroke-width="1.4"/>'
       + f'<rect x="10" y="150" width="60" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(30, 128, RED, .55) + back(54, 128, SKY, .55))
# 冬天封山的高山（立山等）
C.card('snowmtn', '手繪積雪的高山，山腰有纜車，山頂一帶白茫茫一片',
       BOX.format(c='#dde8f3') + f'<path d="M3,140 L70,50 L120,90 L170,40 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{SNOWR}" stroke-width="1.8"/>'
       + f'<path d="M3,177 L3,150 Q120,130 237,150 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.4"/>'
       + ropeway(30, 150, 160, 70, RED, .55) + back(190, 120, SKY, .55))

# 封面：金澤的黃昏（瓦屋頂的城下町、雪吊松樹、遠方的城與日本海）
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{DUSK}"/>'
         + cloud(80, 64, 1.3) + cloud(560, 50, 1.0) + f'<circle cx="640" cy="96" r="22" fill="{GOLD}" stroke-width="1.8"/>'
         + f'<path d="M3,170 L717,170 L717,200 L3,200 Z" fill="{SEA}" stroke="none"/>'
         + castle(470, 200, 1.4, WHITE, LEAD)
         + ''.join(f'<path d="M{x},{y} l14,-12 l14,12 Z" fill="{LEAD}" stroke-width="1.2"/><rect x="{x+3}" y="{y}" width="22" height="10" fill="#efe8da" stroke-width="1.2"/>'
                   for x in range(20, 330, 30) for y in (206, 222))
         + yukizuri(120, 236, 70) + yukizuri(620, 236, 60)
         + f'<path d="M3,236 L717,236 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#efe2cf"/>'
         + f'<path d="M3,236 L717,236" stroke-width="2.4"/><rect x="60" y="250" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(220, 220, RED, 1.6) + back(380, 224, SKY, 1.5) + back(540, 220, GOLD, 1.6))
C.hero('手繪插圖：黃昏的金澤，一排排灰瓦屋頂的老街、繩子吊成傘狀的松樹、遠方白牆的城和海，三個人站在欄杆邊看', _hero)

print(save(C.F, OUT), 'files')
