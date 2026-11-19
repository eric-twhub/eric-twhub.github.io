# 廣島觀景台頁（/hiroshima/observation-decks/）的手繪插圖（2026-11-19）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。輸出 illust/sp/hiroshima-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obs_helpers import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'hiroshima-observation-decks')
C = Cards('hs')
AUT = '#e8a05c'


def crane(x, y, s=1.0, col=PINK):
    # 紙鶴
    return (f'<path d="M{x-14*s},{y} L{x},{y-6*s} L{x+16*s},{y-14*s} L{x+6*s},{y+2*s} L{x+10*s},{y+10*s} L{x-2*s},{y+4*s} Z" fill="{col}" stroke-width="1.2"/>')


# 折鶴塔：木質外牆的屋頂展望台＋紙鶴
C.card('orizuru', '手繪大樓屋頂的木頭甲板展望台，旁邊飄著彩色紙鶴，下面是綠色公園和河',
       BOX.format(c=SKYB) + cloud(180, 30, .8)
       + band(130, GREEN) + f'<path d="M3,150 Q120,140 237,154" fill="none" stroke="{SEA}" stroke-width="8"/>'
       + f'<rect x="60" y="50" width="90" height="110" fill="#d6c3a8" stroke-width="1.8"/>'
       + ''.join(f'<path d="M{60+i*10},50 L{60+i*10},160" stroke="{BROWN}" stroke-width="1.2"/>' for i in range(1, 9))
       + f'<rect x="54" y="42" width="102" height="10" rx="2" fill="{BROWN}" stroke-width="1.6"/>'
       + crane(190, 80) + crane(206, 110, .8, GOLD) + crane(30, 70, .8, SKY)
       + back(90, 22, RED, .6) + back(118, 22, GOLD, .6))
# 宮島纜車與獅子岩：海上的島、纜車
C.card('miyajima', '手繪綠色山上的纜車往山頂開，下面是海和一座座小島，海上有紅色的鳥居',
       BOX.format(c=SKYB) + band(110, SEA, 1.2) + islands(130, ((60, 20), (140, 14)), MTN)
       + f'<path d="M180,130 L180,104 M200,130 L200,104" stroke="{RED}" stroke-width="4"/><path d="M174,104 L206,104" stroke="{RED}" stroke-width="5"/><path d="M176,112 L204,112" stroke="{RED}" stroke-width="3"/>'
       + f'<path d="M3,110 L3,40 L120,18 L150,60 L3,110 Z" fill="{MTN}" stroke-width="1.6"/>'
       + ropeway(20, 96, 130, 30, RED, .5) + back(120, 4, GOLD, .5))
# 彌山山頂：岩石與遠方島
C.card('misen', '手繪山頂的大岩石之間有展望台，遠方是瀨戶內海一座座的小島',
       BOX.format(c=SKYB) + cloud(50, 30, .8) + band(80, SEA, 1.2) + islands(110, ((50, 18), (120, 26), (196, 16)), MTN)
       + f'<path d="M3,177 L3,140 Q40,120 80,132 L110,124 Q160,116 237,140 L237,155 Q237,177 215,177 Z" fill="#b9b2a3" stroke-width="1.6"/>'
       + f'<ellipse cx="40" cy="132" rx="26" ry="18" fill="#a59d8e" stroke-width="1.4"/><ellipse cx="200" cy="134" rx="22" ry="16" fill="#a59d8e" stroke-width="1.4"/>'
       + f'<rect x="96" y="112" width="60" height="12" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(126, 92, RED, .6))
# 城市夜景山丘（黃金山、灰ヶ峰等）
C.card('nightview', '手繪山頂的展望廣場，往下看是一整片亮著燈的城市和港口',
       BOX.format(c=NIGHT) + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{GOLD}" stroke="none"/>'
                                     for x, y in ((20, 100), (36, 108), (58, 96), (80, 110), (102, 100), (128, 108), (150, 96), (176, 106), (198, 98), (220, 108), (50, 120), (120, 122), (190, 122)))
       + f'<path d="M3,84 L237,84" stroke="#2b3560" stroke-width="10"/>'
       + f'<path d="M3,177 L3,140 Q120,120 237,140 L237,155 Q237,177 215,177 Z" fill="#2b3560" stroke-width="1.6"/>'
       + f'<rect x="80" y="134" width="80" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(108, 112, GOLD, .7) + back(134, 112, PINK, .7))
# 山丘公園（比治山等）：樹木與城市
C.card('hillpark', '手繪小山丘上的公園展望台，四周是樹，下面是河流與城市',
       BOX.format(c=SKYB) + cloud(170, 34, .8) + town(96, 9, '#eef0f4')
       + f'<path d="M3,104 Q120,96 237,108" fill="none" stroke="{SEA}" stroke-width="8"/>'
       + f'<path d="M3,177 L3,130 Q120,110 237,130 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + ''.join(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}" stroke-width="1.2"/>' for x, y, c in ((24, 128, DGREEN), (48, 122, PINK), (196, 122, DGREEN), (220, 128, AUT)))
       + f'<rect x="90" y="124" width="60" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(120, 102, RED, .7))
# 尾道千光寺纜車：坡道小鎮、海峽、纜車
C.card('onomichi', '手繪坡道小鎮的屋頂之間，纜車往山頂開，山頂有細長的展望台，下面是窄窄的海峽和橋',
       BOX.format(c=SKYB) + band(130, SEA, 1.2)
       + f'<path d="M100,140 Q170,110 237,124" fill="none" stroke="{WHITE}" stroke-width="5"/><path d="M100,140 Q170,110 237,124" fill="none" stroke-width="1.4"/>'
       + f'<path d="M3,130 L3,40 L100,30 L140,80 L180,130 Z" fill="{MTN}" stroke-width="1.6"/>'
       + ''.join(f'<rect x="{x}" y="{y}" width="14" height="10" fill="#e8e2d4" stroke-width="1"/><path d="M{x-2},{y} L{x+7},{y-6} L{x+16},{y} Z" fill="#7d7f8f" stroke-width="1"/>' for x, y in ((20, 110), (44, 96), (70, 104), (96, 90), (120, 112), (30, 76)))
       + f'<rect x="60" y="32" width="70" height="8" rx="2" fill="{WHITE}" stroke-width="1.6"/><path d="M70,40 L70,52 M120,40 L120,52" stroke-width="2"/>'
       + ropeway(20, 130, 110, 46, GOLD, .45) + back(96, 14, RED, .5))
# 天守（福山城、岩國城）
C.card('castle', '手繪石垣上的白牆黑屋頂天守，前面是車站和樹',
       BOX.format(c=SKYB) + cloud(40, 34, .8) + castle(120, 140, .95, WHITE, '#3f4652')
       + band(140, '#cfc6b6') + ''.join(f'<circle cx="{x}" cy="132" r="9" fill="{DGREEN}" stroke-width="1.2"/>' for x in (30, 54, 186, 210)))
# 山上的城＋纜車＋河上木橋（岩國）
C.card('mountcastle', '手繪山頂的小天守，纜車從山腳往上開，山下河上有一座五個拱的木橋',
       BOX.format(c=SKYB) + f'<path d="M80,177 L150,40 L237,120 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>' + castle(150, 46, .45)
       + band(140, SEA, 1.2)
       + ''.join(f'<path d="M{x},150 Q{x+14},132 {x+28},150" fill="none" stroke="{BROWN}" stroke-width="4"/>' for x in (6, 34, 62, 90, 118))
       + ropeway(110, 120, 170, 60, RED, .5))
# 港邊的展望公園（吳）
C.card('harbor', '手繪港邊的山坡公園，往下看是停著大船的港口和造船的吊臂',
       BOX.format(c=SKYB) + cloud(60, 30, .8) + band(100, SEA, 1.2)
       + f'<path d="M120,96 L220,96 L212,110 L128,110 Z" fill="{GRAY}" stroke-width="1.6"/><rect x="150" y="80" width="40" height="16" fill="{WHITE}" stroke-width="1.4"/>'
       + f'<path d="M40,100 L40,40 L90,40 M40,50 L70,40" fill="none" stroke="{RED}" stroke-width="3"/><path d="M84,40 L84,60" stroke-width="1.2"/>'
       + f'<path d="M3,177 L3,140 Q120,124 237,140 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
       + f'<rect x="80" y="134" width="70" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(114, 112, GOLD, .7))
# 公家大樓展望（市役所、縣廳）
C.card('office', '手繪方正的公家大樓，最上層一排窗是展望樓層，前面有樹和路面電車',
       BOX.format(c=SKYB) + cloud(170, 34, .8)
       + f'<rect x="70" y="36" width="100" height="114" fill="#e8e2d4" stroke-width="1.8"/><rect x="74" y="40" width="92" height="14" fill="{SKY}" stroke-width="1.2"/>'
       + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{WHITE}" stroke-width="1"/>' for x in (82, 106, 130, 152) for y in (68, 94, 120))
       + band(150, '#cfc6b6') + f'<rect x="150" y="144" width="64" height="20" rx="6" fill="{GREEN}" stroke-width="1.6"/>'
       + ''.join(f'<circle cx="{x}" cy="150" r="8" fill="{DGREEN}" stroke-width="1.2"/>' for x in (20, 44))
       + back(120, 18, GOLD, .5))
# 機場觀景台
C.card('airport', '手繪機場屋頂的觀景台，飛機在跑道上起飛，遠方是山',
       BOX.format(c=SKYB) + f'<path d="M3,100 Q80,70 160,92 Q200,80 237,90 L237,110 L3,110 Z" fill="{MTN}" stroke-width="1.4"/>' + band(118, '#cfc6b6')
       + f'<path d="M3,140 L237,140" stroke="{WHITE}" stroke-width="3" stroke-dasharray="12 10"/>'
       + f'<g transform="translate(140,50) rotate(-12)"><rect x="0" y="0" width="60" height="11" rx="5" fill="{WHITE}" stroke-width="1.8"/>'
         f'<path d="M22,6 L12,26 L28,26 L38,6 Z" fill="{WHITE}" stroke-width="1.4"/><path d="M4,6 L0,-8 L8,-8 L14,2 Z" fill="{SKY}" stroke-width="1.4"/></g>'
       + f'<rect x="20" y="110" width="90" height="8" rx="2" fill="#e8e2d4" stroke-width="1.4"/>' + back(50, 88, RED, .7) + back(80, 88, GOLD, .7))

# 封面：廣島（河邊城市、紙鶴、海上鳥居與島、纜車山）
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{DUSK}"/>'
         + cloud(80, 64, 1.3) + cloud(330, 44, 1.0) + f'<circle cx="420" cy="90" r="22" fill="{GOLD}" stroke-width="1.8"/>'
         + f'<path d="M440,236 L560,90 L717,170 L717,236 Z" fill="{MTN}" stroke-width="1.6"/>'
         + f'<path d="M470,200 L600,110" stroke-width="1.6"/><path d="M535,155 L535,165" stroke-width="1.4"/><rect x="523" y="165" width="24" height="16" rx="3" fill="{RED}" stroke-width="1.4"/>'
         + f'<path d="M3,236 L717,236 L717,200 L440,200 Z" fill="{SEA}" stroke="none"/>'
         + f'<path d="M640,236 L640,196 M676,236 L676,196" stroke="{RED}" stroke-width="6"/><path d="M630,196 L686,196" stroke="{RED}" stroke-width="7"/><path d="M634,208 L682,208" stroke="{RED}" stroke-width="4"/>'
         + ''.join(f'<rect x="{x}" y="{236-h}" width="{w}" height="{h}" fill="#e7d6c6" stroke-width="1.4"/>'
                   for x, w, h in ((30, 34, 70), (70, 26, 100), (250, 30, 60), (284, 24, 90), (316, 30, 50)))
         + f'<rect x="130" y="80" width="90" height="156" fill="#d6c3a8" stroke-width="2"/>'
         + ''.join(f'<path d="M{130+i*10},80 L{130+i*10},236" stroke="{BROWN}" stroke-width="1.2"/>' for i in range(1, 9))
         + f'<rect x="124" y="72" width="102" height="10" rx="2" fill="{BROWN}" stroke-width="1.6"/>'
         + crane(260, 120, 1.3) + crane(300, 150, 1.0, GOLD) + crane(100, 110, 1.0, SKY)
         + f'<path d="M3,236 L717,236 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#efe2cf"/>'
         + f'<path d="M3,236 L717,236" stroke-width="2.4"/><rect x="60" y="250" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(220, 220, RED, 1.6) + back(380, 224, SKY, 1.5) + back(540, 220, GOLD, 1.6))
C.hero('手繪插圖：黃昏的廣島，河邊的木質外牆大樓旁飄著紙鶴，海上有紅色鳥居，山上的纜車往山頂開，三個人站在欄杆邊看', _hero)

print(save(C.F, OUT), 'files')
