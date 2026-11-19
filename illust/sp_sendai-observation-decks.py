# 仙台觀景台頁（/sendai/observation-decks/）的手繪插圖（2026-11-19）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物、不畫銅像。輸出 illust/sp/sendai-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obs_helpers import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'sendai-observation-decks')
C = Cards('sd')

# 車站旁高樓的室內展望樓層，窗外是行道樹的大街
C.card('tower', '手繪車站旁高樓最上層的大玻璃窗，窗外是綠色行道樹的大街和遠方的山',
       BOX.format(c=SKYB) + f'<path d="M3,80 Q80,56 160,74 Q200,64 237,72" fill="none" stroke="{MTN}" stroke-width="7"/>'
       + town(120, 9, '#eef0f4')
       + ''.join(f'<circle cx="{x}" cy="130" r="8" fill="{GREEN}" stroke-width="1.2"/>' for x in range(20, 230, 26))
       + band(140, '#cfc6b6')
       + ''.join(f'<path d="M{x},18 L{x},150" stroke="{GRAY}" stroke-width="5"/>' for x in (70, 170))
       + back(110, 128, RED, .7) + back(140, 128, SKY, .7))
# 縣廳、市役所的展望樓層：方正大樓
C.card('office', '手繪方正的公家大樓，最上層一排窗是展望大廳，前面有公園樹木',
       BOX.format(c=SKYB) + cloud(170, 34, .8)
       + f'<rect x="70" y="36" width="100" height="120" fill="#e8e2d4" stroke-width="1.8"/><rect x="74" y="40" width="92" height="14" fill="{SKY}" stroke-width="1.2"/>'
       + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{WHITE}" stroke-width="1"/>' for x in (82, 106, 130, 152) for y in (68, 94, 120))
       + band(150, GREEN) + ''.join(f'<circle cx="{x}" cy="150" r="10" fill="{DGREEN}" stroke-width="1.2"/>' for x in (24, 48, 196, 220))
       + back(120, 18, GOLD, .5))
# 城跡：石垣上看城市
C.card('castlesite', '手繪山上的石垣城跡，旁邊有松樹，下面是河流和整片城市',
       BOX.format(c=SKYB) + town(96, 9, '#eef0f4')
       + f'<path d="M3,104 Q120,96 237,108" fill="none" stroke="{SEA}" stroke-width="8"/>'
       + f'<path d="M3,130 L140,130 L160,177 L3,177 Z" fill="#c9c2b4" stroke-width="1.6"/>'
       + ''.join(f'<path d="M{x},{y} l20,0" stroke-width="1"/>' for x in (12, 40, 70, 100) for y in (142, 156))
       + f'<path d="M180,177 L184,120" stroke="{DBROWN}" stroke-width="5"/><circle cx="184" cy="114" r="18" fill="{DGREEN}" stroke-width="1.4"/>'
       + back(70, 106, RED, .7))
# 山丘上的電視塔／公園展望
C.card('hillpark', '手繪小山丘上的公園展望台，旁邊有細長的電波塔，遠方是城市夜景',
       BOX.format(c=NIGHT) + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{GOLD}" stroke="none"/>' for x, y in ((20, 110), (40, 104), (66, 112), (90, 106), (120, 112), (150, 104), (180, 110), (210, 106)))
       + f'<path d="M3,130 Q120,96 237,130 {GROUND}" fill="#2b3560" stroke-width="1.4"/>'
       + f'<path d="M170,104 L176,24 L182,104 Z" fill="{RED}" stroke-width="1.4"/><path d="M172,60 L180,60 M171,80 L181,80" stroke="{WHITE}" stroke-width="2"/>'
       + f'<rect x="80" y="110" width="60" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(100, 88, GOLD, .7))
# 遊樂園摩天輪
C.card('wheel', '手繪山丘上的遊樂園摩天輪，遠方看得到城市和海',
       BOX.format(c=SKYB) + f'<path d="M3,96 L237,96 L237,104 L3,104 Z" fill="{SEA}" stroke="none"/>' + town(96, 9, '#eef0f4')
       + band(140, MTN) + wheel(120, 82, 54, 14) + f'<path d="M100,140 L120,82 L140,140" fill="none" stroke-width="2.6"/>'
       + back(200, 118, PINK, .7))
# 松島：海上許多小島
C.card('matsushima', '手繪從山上往下看海灣裡一顆顆長著松樹的小島，小船在島間穿梭',
       BOX.format(c=SKYB) + cloud(180, 30, .8)
       + band(70, SEA, 1.2) + islands(110, ((40, 22), (96, 16), (150, 26), (206, 18))) + islands(150, ((70, 18), (180, 22)))
       + f'<path d="M120,132 L148,132 L144,138 L124,138 Z" fill="{WHITE}" stroke-width="1.2"/>'
       + f'<path d="M3,40 L60,72 L3,72 Z" fill="{DGREEN}" stroke-width="1.4"/>' + back(30, 46, RED, .5))
# 山寺：岩壁上的小堂
C.card('yamadera', '手繪陡峭岩山上突出的小木堂，人站在木頭欄杆邊往下看山谷的村落',
       BOX.format(c=SKYB) + cloud(40, 34, .8)
       + f'<path d="M110,177 L130,40 L170,30 L210,60 L237,50 L237,155 Q237,177 215,177 Z" fill="#b9b2a3" stroke-width="1.6"/>'
       + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="#e8a05c" stroke-width="1.2"/>' for x, y in ((140, 90), (190, 110), (220, 90)))
       + f'<rect x="120" y="66" width="44" height="22" fill="{BROWN}" stroke-width="1.6"/><path d="M114,66 L170,66 L160,56 L124,56 Z" fill="#7d7f8f" stroke-width="1.4"/>'
       + f'<path d="M110,88 L172,88" stroke-width="2"/>' + back(130, 46, GOLD, .5)
       + town(170, 4, '#eef0f4', 10, 22))
# 樹冰：雪山與纜車
C.card('juhyo', '手繪白雪覆蓋的山頂上一個個圓滾滾的樹冰，纜車從山下往上開',
       BOX.format(c='#dde8f3') + band(120, WHITE)
       + f'<path d="M3,120 L90,50 L170,96 L237,70 L237,120 Z" fill="{WHITE}" stroke-width="1.6"/>'
       + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="18" fill="{SNOWB}" stroke-width="1.4"/>' for x, y in ((40, 146), (80, 136), (170, 140), (210, 150)))
       + ropeway(20, 160, 200, 60, RED, .55) + back(120, 128, SKY, .7))
# 港邊山丘公園
C.card('harborhill', '手繪山丘公園上的展望處，往下看得到港口、河口和海',
       BOX.format(c=SKYB) + cloud(60, 34, .8) + band(80, SEA, 1.2)
       + f'<path d="M3,120 Q60,98 120,110 Q180,96 237,116" fill="none" stroke="{SEA}" stroke-width="10"/>'
       + town(116, 9, '#eef0f4')
       + f'<path d="M3,177 L3,140 Q120,120 237,140 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + ''.join(f'<circle cx="{x}" cy="138" r="7" fill="{PINK}" stroke-width="1"/>' for x in (30, 200))
       + back(120, 118, RED, .7))
# 白色大觀音像（胎內最上層有展望窗）
C.card('kannon', '手繪住宅區上方高高站著的白色觀音像，胸口一排小窗，遠方是城市和海',
       BOX.format(c=SKYB) + cloud(50, 40, .8) + cloud(190, 56, .6) + band(118, SEA, 1.2) + town(140, 9, '#eef0f4')
       + f'<path d="M3,177 L3,150 Q120,138 237,150 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<path d="M104,160 L110,52 L130,52 L136,160 Z" fill="{WHITE}" stroke-width="1.8"/>'
       + f'<path d="M110,70 Q120,80 130,70" fill="none" stroke-width="1.2"/><path d="M106,120 L134,120" stroke-width="1"/>'
       + ''.join(f'<rect x="{x}" y="84" width="5" height="7" rx="1" fill="{SKY}" stroke-width="1"/>' for x in (112, 118, 124))
       + f'<circle cx="120" cy="40" r="11" fill="{WHITE}" stroke-width="1.8"/><path d="M112,32 Q120,22 128,32" fill="{WHITE}" stroke-width="1.4"/>'
       + f'<path d="M134,74 L148,96" stroke-width="2"/><circle cx="149" cy="98" r="3" fill="{GOLD}" stroke-width="1"/>'
       + back(190, 140, RED, .7))
# 機場觀景台
C.card('airport', '手繪機場屋頂的觀景台，飛機在跑道上起飛，遠方是海',
       BOX.format(c=SKYB) + cloud(40, 40, .8) + band(100, SEA, 1.2) + band(130, '#cfc6b6')
       + f'<path d="M3,146 L237,146" stroke="{WHITE}" stroke-width="3" stroke-dasharray="12 10"/>'
       + f'<g transform="translate(140,60) rotate(-12)"><rect x="0" y="0" width="60" height="11" rx="5" fill="{WHITE}" stroke-width="1.8"/>'
         f'<path d="M22,6 L12,26 L28,26 L38,6 Z" fill="{WHITE}" stroke-width="1.4"/><path d="M4,6 L0,-8 L8,-8 L14,2 Z" fill="{SKY}" stroke-width="1.4"/></g>'
       + f'<rect x="20" y="120" width="90" height="8" rx="2" fill="#e8e2d4" stroke-width="1.4"/>' + back(50, 98, RED, .7) + back(80, 98, GOLD, .7))
# 封面：仙台街景（行道樹大街、車站高樓、山上電波塔、遠方松島小島）
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{DUSK}"/>'
         + cloud(80, 64, 1.3) + cloud(560, 50, 1.0) + f'<circle cx="650" cy="96" r="22" fill="{GOLD}" stroke-width="1.8"/>'
         + f'<path d="M420,180 Q520,120 640,150 Q690,140 717,150 L717,236 L420,236 Z" fill="{MTN}" stroke-width="1.6"/>'
         + f'<path d="M600,150 L606,60 L612,150 Z" fill="{RED}" stroke-width="1.6"/><path d="M602,100 L610,100 M601,124 L611,124" stroke="{WHITE}" stroke-width="2.4"/>'
         + ''.join(f'<rect x="{x}" y="{236-h}" width="{w}" height="{h}" fill="#e7d6c6" stroke-width="1.4"/>'
                   for x, w, h in ((30, 34, 70), (70, 26, 100), (230, 30, 60), (264, 24, 90), (380, 30, 76)))
         + f'<path d="M120,236 L126,60 L176,60 L182,236 Z" fill="#c9d4e6" stroke-width="2"/><rect x="128" y="64" width="46" height="18" fill="{SKY}" stroke-width="1.4"/>'
         + ''.join(f'<path d="M{130},{100+i*26} L{178},{100+i*26}" stroke-width="1"/>' for i in range(5))
         + ''.join(f'<circle cx="{x}" cy="226" r="16" fill="{GREEN}" stroke-width="1.4"/><path d="M{x},236 L{x},242" stroke-width="2"/>' for x in range(30, 420, 46))
         + f'<path d="M3,236 L717,236 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#efe2cf"/>'
         + f'<path d="M3,236 L717,236" stroke-width="2.4"/><rect x="60" y="250" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(220, 220, RED, 1.6) + back(380, 224, SKY, 1.5) + back(540, 220, GOLD, 1.6))
C.hero('手繪插圖：黃昏的仙台街景，有綠色行道樹的大街、車站旁的高樓、山上的紅白電波塔，三個人站在欄杆邊看', _hero)

print(save(C.F, OUT), 'files')
