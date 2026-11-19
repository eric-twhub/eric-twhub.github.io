# 東京觀景台懶人包（/tokyo/observation-decks/）的手繪插圖（2026-11-18）。
# 晴空塔、東京鐵塔、SHIBUYA SKY 直接沿用各自頁面已經畫好的圖（illust/sp/japan-*/），
# 這裡只畫其他觀景台與封面。照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。
# 輸出 illust/sp/tokyo-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
ORANGE = '#ee7a3c'
TURF = '#9fd08a'
SILVER = '#dfe4ec'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ob-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def tower(cx, base, top, col=ORANGE, band=WHITE, sw=46):
    # 東京鐵塔的剪影（同東京鐵塔頁的畫法，縮放用 sw 控制腳寬）
    h = base - top
    md = base - h * .45
    td = base - h * .72

    def hw(y):
        u = (base - y) / h
        return max(1.0, sw * (1 - u) ** 2.2 + 1.2)
    pts_l = [f'{cx-hw(y):.1f},{y:.1f}' for y in [base - h * k / 20 for k in range(0, 21)]]
    pts_r = [f'{cx+hw(y):.1f},{y:.1f}' for y in [top + h * k / 20 for k in range(0, 21)]]
    arch = f'L{cx+hw(base)-sw*.3:.1f},{base} Q{cx},{base-h*.22:.1f} {cx-hw(base)+sw*.3:.1f},{base} '
    t = f'<path d="M{" L".join(pts_l)} L{" L".join(pts_r)} {arch}Z" fill="{col}" stroke-width="1.8"/>'
    w1 = hw(md) + sw * .17
    t += f'<rect x="{cx-w1:.1f}" y="{md-sw*.15:.1f}" width="{2*w1:.1f}" height="{sw*.3:.1f}" rx="2" fill="{band}" stroke-width="1.6"/>'
    w2 = hw(td) + sw * .1
    t += f'<rect x="{cx-w2:.1f}" y="{td-sw*.1:.1f}" width="{2*w2:.1f}" height="{sw*.2:.1f}" rx="2" fill="{band}" stroke-width="1.4"/>'
    return t


def skytree(cx, base, top, w=16):
    # 晴空塔：細長的塔身、兩個圓盤展望台、頂上天線
    h = base - top
    d1, d2 = base - h * .55, base - h * .72
    t = (f'<path d="M{cx-w},{base} L{cx-w*.25},{top+h*.12} L{cx+w*.25},{top+h*.12} L{cx+w},{base} Z" fill="{WHITE}" stroke-width="1.8"/>'
         + f'<path d="M{cx},{top} L{cx},{top+h*.14}" stroke-width="2.2"/>'
         + f'<ellipse cx="{cx}" cy="{d1}" rx="{w*.75}" ry="{w*.3}" fill="{SKY}" stroke-width="1.6"/>'
         + f'<ellipse cx="{cx}" cy="{d2}" rx="{w*.55}" ry="{w*.22}" fill="{SKY}" stroke-width="1.4"/>')
    return t


def bldg(x, base, w, h, col=GRAY, win=True):
    t = f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{col}" stroke-width="1.6"/>'
    if win and w >= 14:
        for yy in range(int(base - h + 8), int(base - 6), 12):
            t += f'<path d="M{x+4},{yy} L{x+w-4},{yy}" stroke-width="1" opacity=".45"/>'
    return t


# 0. 封面：東京天際線，東京鐵塔、晴空塔、幾棟高樓，前面有人拿著小卡看夜景
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="#f7d9b8"/>'
         + f'<path d="M3,150 Q3,3 25,3 L695,3 Q717,3 717,25 L717,150 Z" fill="#f4c7a0" stroke="none"/>'
         + f'<circle cx="590" cy="96" r="30" fill="{GOLD}"/>'
         + cloud(90, 70, 1.4) + cloud(380, 50, 1.1) + cloud(640, 150, .9)
         + f'<path d="M430,250 L480,196 L520,232 L556,190 L610,250 Z" fill="#c9b8d6" stroke-width="1.8"/>'
         + f'<path d="M546,200 L556,190 L566,200 Q556,206 546,200 Z" fill="{WHITE}" stroke-width="1.4"/>'
         + bldg(40, 262, 38, 96) + bldg(84, 262, 26, 130, '#d9d2e9') + bldg(118, 262, 44, 74)
         + bldg(250, 262, 30, 150, '#d9d2e9') + bldg(286, 262, 42, 100) + bldg(336, 262, 22, 70)
         + bldg(380, 262, 34, 118, '#d9d2e9') + bldg(420, 262, 24, 62)
         + bldg(640, 262, 36, 92) + bldg(682, 262, 26, 120, '#d9d2e9')
         + tower(200, 262, 70, sw=40)
         + skytree(500, 262, 22, 15)
         + f'<path d="M3,262 L717,262 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#e9dcc8"/>'
         + f'<path d="M3,262 L717,262" stroke-width="2.4"/>'
         + f'<rect x="60" y="270" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(250, 230, PINK, 1.6) + back(330, 234, GREEN, 1.5) + back(420, 230, SKY, 1.6)
         + f'<g transform="translate(366,214) rotate(-8)"><rect x="0" y="0" width="34" height="24" rx="4" fill="{CREAM}"/>'
           f'<path d="M6,8 L28,8 M6,15 L22,15" stroke-width="1.6"/></g>'
         + star(130, 40, 8) + sparkle(660, 52, 6) + sparkle(30, 120, 5))
F['hero'] = svg('ob-hero', 720, 330, '手繪插圖：黃昏的東京天際線，有東京鐵塔、晴空塔、高樓和遠方的富士山，三個人站在窗邊看景色', _hero)

# 1. 六本木之丘 東京 City View：52 樓室內一整圈玻璃，窗外正對東京鐵塔
card('roppongi', '手繪六本木之丘 52 樓的室內展望台，一整面玻璃窗，窗外正對著東京鐵塔',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(26, 40, .8) + cloud(170, 30, .9)
     + bldg(14, 128, 18, 34) + bldg(36, 128, 14, 50) + bldg(176, 128, 20, 40) + bldg(200, 128, 16, 56)
     + tower(118, 128, 30, sw=26)
     + ''.join(f'<path d="M{x},3 L{x},140" stroke-width="3"/>' for x in (60, 180))
     + f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M3,140 L237,140" stroke-width="2.4"/>'
     + back(84, 118, PINK, 1.1) + back(150, 120, GOLD, 1.0)
     + sparkle(214, 20, 4))

# 2. 六本木之丘 Sky Deck：屋頂的露天甲板（加價、天氣不好就關）
card('skydeck', '手繪大樓屋頂的露天甲板，四周有欄杆，風把人的頭髮吹起來',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 50, 1.0) + cloud(160, 40, 1.1) + cloud(110, 150, 1.3)
     + f'<path d="M20,120 L220,120 L236,150 L4,150 Z" fill="#b9bfc9"/>'
     + f'<path d="M20,96 L220,96" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{x},96 L{x},120" stroke-width="1.8"/>' for x in range(28, 220, 16))
     + kid(90, 92, RED, 1.15) + f'<path d="M98,84 q12,-6 20,2 M98,90 q10,-2 16,6" fill="none" stroke-width="1.6"/>'
     + kid(150, 94, GREEN, 1.05)
     + ''.join(f'<path d="M{x},{y} q10,-6 20,0" fill="none" stroke-width="1.6" opacity=".6"/>' for x, y in [(30, 80), (180, 70), (190, 90)])
     + sparkle(120, 24, 5))

# 3. 陽光 60 展望台：像公園一樣的草地造景，可以坐下來看
card('sunshine', '手繪高樓裡像公園一樣的展望台，地上是綠色草地，有人坐著看窗外',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 40, .9) + cloud(170, 34, .8)
     + bldg(20, 112, 16, 30) + bldg(40, 112, 12, 46) + bldg(170, 112, 18, 38) + bldg(194, 112, 22, 26)
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}"/>'
     + ''.join(f'<path d="M{x},{y} l2,-6 l2,6" fill="none" stroke="{DGREEN}" stroke-width="1.4"/>'
               for x, y in [(20, 140), (60, 160), (110, 150), (170, 164), (210, 140), (140, 132)])
     + f'<path d="M3,112 L237,112" stroke-width="2.4"/>'
     + back(70, 112, PINK, 1.1) + back(100, 114, SKY, 1.0)
     + f'<rect x="150" y="128" width="54" height="14" rx="5" fill="{WHITE}"/>'
     + kid(176, 104, GOLD, 1.0)
     + star(120, 26, 6))

# 4. 富士電視台 球體展望室：銀色大球
card('hachitama', '手繪台場富士電視台大樓上的銀色大圓球，旁邊是海和彩虹大橋',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .8) + cloud(190, 30, .8)
     + f'<path d="M3,130 L237,130 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ea"/>'
     + f'<path d="M150,118 L232,118" stroke-width="2"/><path d="M168,118 L168,92 M214,118 L214,92" stroke-width="2.4"/>'
     + f'<path d="M150,110 Q168,92 168,92 Q191,112 214,92 Q224,104 232,108" fill="none" stroke-width="1.4"/>'
     + f'<rect x="36" y="60" width="16" height="70" fill="{GRAY}"/><rect x="104" y="60" width="16" height="70" fill="{GRAY}"/>'
     + f'<rect x="30" y="54" width="96" height="10" rx="2" fill="{GRAY}"/>'
     + f'<rect x="52" y="96" width="52" height="8" fill="{GRAY}"/>'
     + f'<circle cx="78" cy="78" r="22" fill="{SILVER}"/>'
     + f'<path d="M64,70 q8,-10 20,-6" fill="none" stroke="{WHITE}" stroke-width="3"/>'
     + face(78, 82, .8)
     + sparkle(140, 40, 5))

# 5. 東京都廳展望室：雙塔、45 樓
card('tocho', '手繪新宿東京都廳的雙塔大樓，兩座塔頂樓都有窗，前面是樹',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 34, .8) + cloud(200, 50, .7)
     + f'<path d="M70,150 L70,46 L84,40 L84,30 L110,30 L110,150 Z" fill="{GRAY}"/>'
     + f'<path d="M130,150 L130,30 L156,30 L156,40 L170,46 L170,150 Z" fill="{GRAY}"/>'
     + ''.join(f'<path d="M{a},{y} L{b},{y}" stroke-width="1" opacity=".45"/>' for a, b in ((74, 108), (132, 166)) for y in range(60, 146, 10))
     + f'<rect x="84" y="36" width="26" height="10" rx="2" fill="{GOLD}"/><rect x="130" y="36" width="26" height="10" rx="2" fill="{GOLD}"/>'
     + f'<rect x="110" y="96" width="20" height="54" fill="{GRAY}"/>'
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + ''.join(f'<circle cx="{x}" cy="146" r="12" fill="{GREEN}" stroke-width="1.6"/>' for x in (28, 50, 196, 218))
     + kid(120, 150, PINK, .9)
     + sparkle(206, 22, 4))

# 6. 淺草文化觀光中心 8 樓：露台，下面是淺草寺的屋頂，遠方是晴空塔
card('asakusa', '手繪淺草的屋頂露台，看得到寺廟的屋頂和遠方的晴空塔',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .8)
     + skytree(186, 120, 16, 10)
     + f'<path d="M30,112 Q80,94 130,112 Z" fill="{RED}"/><path d="M40,112 L120,112 L120,124 L40,124 Z" fill="{RED}"/>'
     + f'<path d="M24,112 Q80,86 136,112" fill="none" stroke-width="2.4"/>'
     + bldg(140, 124, 16, 18) + bldg(212, 124, 18, 22)
     + f'<path d="M3,124 L237,124 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M14,124 L226,124" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{x},124 L{x},140" stroke-width="1.6"/>' for x in range(20, 226, 14))
     + f'<path d="M14,140 L226,140" stroke-width="2"/>'
     + back(90, 126, GOLD, 1.0) + back(130, 128, GREEN, .95)
     + sparkle(120, 30, 4))

# 7. KITTE 屋頂庭園：草地＋木頭，看東京車站的紅磚屋頂
card('kitte', '手繪屋頂花園的草地和木頭步道，前面是紅磚車站與圓頂',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 36, .9) + cloud(180, 30, .8)
     + bldg(10, 100, 22, 60) + bldg(206, 100, 22, 66)
     + f'<rect x="34" y="70" width="172" height="30" fill="{BRICK}"/>'
     + ''.join(f'<rect x="{x}" y="78" width="8" height="12" rx="1" fill="{CREAM}" stroke-width="1.2"/>' for x in range(46, 200, 18))
     + f'<path d="M98,70 Q120,40 142,70 Z" fill="#5f8f86"/>'
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}"/>'
     + f'<path d="M3,100 L237,100 L237,112 L3,112 Z" fill="#d9a877"/>'
     + f'<path d="M3,100 L237,100" stroke-width="2.4"/>'
     + back(80, 106, PINK, 1.0) + kid(160, 112, SKY, 1.0)
     + sparkle(214, 20, 4))

# 8. 文京 Civic Center 25 樓：免費的觀景休息區，窗外有晴空塔和遠山
card('bunkyo', '手繪室內觀景區，窗邊一排椅子，窗外遠遠看得到晴空塔和山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M120,100 L150,74 L172,94 L196,70 L236,100 Z" fill="#c9b8d6" stroke-width="1.6"/>'
     + skytree(60, 108, 24, 10)
     + bldg(90, 108, 14, 26) + bldg(10, 108, 16, 34) + bldg(200, 108, 18, 22)
     + ''.join(f'<path d="M{x},3 L{x},120" stroke-width="3"/>' for x in (80, 160))
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M3,120 L237,120" stroke-width="2.4"/>'
     + ''.join(f'<rect x="{x}" y="132" width="26" height="12" rx="4" fill="{BROWN}"/><path d="M{x+4},144 L{x+4},160 M{x+22},144 L{x+22},160" stroke-width="2"/>' for x in (40, 104, 168))
     + back(117, 112, GOLD, 1.0)
     + sparkle(220, 20, 4))

# 9. 羽田機場展望台：飛機
card('haneda', '手繪機場頂樓的展望台，看飛機在跑道上起飛',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .8) + cloud(170, 30, .9)
     + f'<path d="M3,110 L237,110 L237,140 L3,140 Z" fill="#b9bfc9"/>'
     + f'<path d="M20,126 L220,126" stroke="{WHITE}" stroke-width="2.4" stroke-dasharray="12 10"/>'
     + f'<g transform="translate(150,70) rotate(-14)">'
     + f'<path d="M-30,0 Q-30,-7 -20,-7 L22,-7 Q32,-7 34,0 Q32,7 22,7 L-20,7 Q-30,7 -30,0 Z" fill="{WHITE}"/>'
     + f'<path d="M-6,-7 L6,-24 L13,-24 L9,-7 Z M-6,7 L6,24 L13,24 L9,7 Z M-25,-7 L-30,-17 L-22,-17 L-15,-7 Z" fill="{SKY}"/>'
     + f'<circle cx="20" cy="-1" r="1.8" fill="{INK}" stroke="none"/></g>'
     + f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M3,140 L237,140" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{x},140 L{x},124" stroke-width="1.4"/>' for x in range(14, 236, 12))
     + f'<path d="M3,124 L237,124" stroke-width="1.8"/>'
     + back(60, 120, RED, 1.0) + back(90, 122, GOLD, .9)
     + sparkle(214, 20, 4))


# ---- 2026-11-18 補：不用門票的觀景點 ----
def win_room(inner, people):
    # 室內展望大廳：窗框＋地板＋背影
    return (inner + ''.join(f'<path d="M{x},3 L{x},128" stroke-width="3"/>' for x in (80, 160))
            + f'<path d="M3,128 L237,128 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
            + f'<path d="M3,128 L237,128" stroke-width="2.4"/>' + people)


# 船堀 Tower Hall：高塔上的展望室，遠方晴空塔
card('funabori', '手繪高塔上的室內展望室，窗外遠遠看得到晴空塔和東京鐵塔',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + win_room(bldg(14, 112, 16, 30) + bldg(36, 112, 12, 22) + skytree(60, 112, 40, 8) + tower(196, 112, 70, sw=14)
                + bldg(110, 112, 20, 34, '#d9d2e9') + bldg(140, 112, 14, 20) + f'<path d="M3,112 L237,112" stroke-width="1.6"/>',
                back(104, 120, PINK, 1.0) + back(140, 122, GOLD, .95))
     + sparkle(214, 20, 4))

# 練馬區役所 20 樓：窗外遠方富士山
card('nerima', '手繪區公所高樓層的展望大廳，窗外遠方是富士山和新宿高樓',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f7d9b8"/>'
     + win_room(f'<path d="M20,112 L70,56 L90,72 L120,112 Z" fill="#c9b8d6" stroke-width="1.6"/>'
                f'<path d="M60,66 L70,56 L80,66 Q70,72 60,66 Z" fill="{WHITE}" stroke-width="1.2"/>'
                + bldg(150, 112, 14, 44, '#d9d2e9') + bldg(168, 112, 18, 56) + bldg(190, 112, 12, 36)
                + f'<path d="M3,112 L237,112" stroke-width="1.6"/>',
                back(100, 120, SKY, 1.0) + back(136, 122, RED, .95)))

# 東京 Gate Bridge：恐龍形的橋、步道上的人
card('gatebridge', '手繪海上一座有兩個大三角骨架的長橋，橋邊步道上有人在走',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 34, .8) + cloud(190, 30, .7)
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ea"/>'
     + f'<path d="M3,100 L237,100" stroke-width="3"/>'
     + ''.join(f'<path d="M{a},100 L{a+30},60 L{a+60},60 L{a+90},100" fill="none" stroke="{GRAY}" stroke-width="6"/>'
               f'<path d="M{a},100 L{a+30},60 L{a+60},60 L{a+90},100" fill="none" stroke-width="1.4"/>' for a in (20, 130))
     + ''.join(f'<path d="M{x},100 L{x},150" stroke-width="2.4"/>' for x in (60, 120, 180))
     + kid(110, 80, PINK, .7) + kid(130, 80, GOLD, .7))

# SHIBU NIWA：澀谷站前大樓 17 樓屋頂，看十字路口
card('shibuniwa', '手繪大樓屋頂的露天庭園，往下看得到斑馬線交叉的十字路口',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in [(30, 24, WHITE), (200, 20, GOLD), (220, 50, WHITE)])
     + bldg(20, 110, 24, 60, '#4b5584') + bldg(190, 110, 30, 70, '#4b5584')
     + f'<path d="M3,110 L237,110 L237,130 L3,130 Z" fill="#3f4a78" stroke="none"/>'
     + ''.join(f'<rect x="{x}" y="114" width="6" height="12" fill="{WHITE}" stroke="none" opacity=".8"/>' for x in range(60, 180, 12))
     + f'<path d="M3,134 L237,134 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}"/>'
     + f'<path d="M3,134 L237,134" stroke-width="2.4"/>' + ''.join(f'<path d="M{x},134 L{x},122" stroke-width="1.4"/>' for x in range(14, 236, 14))
     + f'<path d="M3,122 L237,122" stroke-width="1.6"/>'
     + back(96, 126, PINK, 1.0) + back(132, 128, GOLD, .95) + star(120, 30, 5), bg=NIGHT)

# GINZA SIX 屋頂庭園：大片草地與樹，冬天有溜冰場
card('ginzasix', '手繪大樓屋頂的大片庭園，有草地、樹和一塊小小的溜冰場',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 36, .8) + bldg(170, 100, 20, 50) + bldg(196, 100, 26, 66, '#d9d2e9') + bldg(16, 100, 22, 40)
     + f'<path d="M3,100 L237,100 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}"/>'
     + f'<path d="M3,100 L237,100" stroke-width="2.4"/>'
     + f'<ellipse cx="150" cy="140" rx="46" ry="16" fill="#e6f4fb" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="{GREEN}" stroke-width="1.4"/><path d="M{x},{y+9} L{x},{y+16}" stroke-width="1.6"/>' for x, y in ((30, 112), (60, 118), (90, 110)))
     + kid(140, 120, PINK, .8) + kid(166, 124, SKY, .8) + sparkle(214, 24, 4))

# 豐洲市場屋頂綠化廣場：草坪、遠方的海與橋
card('toyosu', '手繪市場屋頂的草坪廣場，遠方是海、橋和高樓',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(180, 34, .8)
     + bldg(20, 96, 14, 36) + bldg(40, 96, 18, 50, '#d9d2e9') + bldg(64, 96, 12, 28) + tower(200, 96, 40, sw=10)
     + f'<path d="M3,96 L237,96 L237,110 L3,110 Z" fill="#9fd0ea" stroke-width="1.2"/>'
     + f'<path d="M90,96 Q130,70 170,96" fill="none" stroke-width="2"/>'
     + f'<path d="M3,110 L237,110 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}"/>'
     + f'<path d="M3,110 L237,110" stroke-width="2.4"/>'
     + back(110, 126, RED, 1.0) + back(140, 128, GOLD, .95))

# 彩虹大橋步道：橋上的步道，看海和台場
card('rainbow', '手繪吊橋旁的步道，從橋上看出去是海和遠方的高樓',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ea"/>'
     + ''.join(f'<rect x="{x}" y="30" width="14" height="110" rx="2" fill="{WHITE}" stroke-width="1.8"/>' for x in (50, 176))
     + f'<path d="M3,46 Q57,40 57,36 Q120,110 183,36 Q183,40 237,46" fill="none" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},{78 - abs(120 - x) * .35:.0f} L{x},100" stroke-width="1" opacity=".6"/>' for x in range(70, 176, 12))
     + f'<path d="M3,100 L237,100 L237,108 L3,108 Z" fill="{GRAY}" stroke-width="1.6"/>'
     + kid(110, 78, PINK, .7) + kid(130, 78, GREEN, .7) + cloud(200, 20, .6))

# Sky Carrot（三軒茶屋）：26 樓窗邊夜景、東京鐵塔
card('carrot', '手繪高樓層的展望大廳，窗外是城市夜景和遠方的東京鐵塔',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + win_room(''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>' for x in range(10, 230, 9) for y in (100, 110) if (x + y) % 3)
                + tower(120, 112, 60, sw=12) + f'<path d="M3,112 L237,112" stroke-width="1.6"/>',
                back(80, 120, PINK, 1.0) + back(170, 122, GOLD, .95)), bg=NIGHT)

# 目黑天空庭園：繞圈的屋頂花園，有松樹
card('meguro', '手繪繞成圓圈往上的屋頂花園，有松樹和步道，遠方是富士山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M150,70 L180,40 L210,70 Z" fill="#c9b8d6" stroke-width="1.6"/><path d="M172,48 L180,40 L188,48 Q180,52 172,48 Z" fill="{WHITE}" stroke-width="1.2"/>'
     + f'<ellipse cx="110" cy="120" rx="100" ry="40" fill="{TURF}" stroke-width="1.8"/>'
     + f'<ellipse cx="110" cy="120" rx="60" ry="22" fill="#e9dcc8" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},{y} l-10,12 l20,0 Z" fill="{DGREEN}" stroke-width="1.4"/><path d="M{x},{y+12} L{x},{y+20}" stroke-width="1.6"/>' for x, y in ((40, 96), (180, 100), (70, 140), (150, 142)))
     + kid(110, 106, PINK, .8))

# 北とぴあ 17 樓：窗外有新幹線經過
card('hokutopia', '手繪展望大廳，窗外是公園的樹和一列白色新幹線經過',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + win_room(''.join(f'<circle cx="{x}" cy="86" r="10" fill="{GREEN}" stroke-width="1.4"/>' for x in (20, 40, 200, 220))
                + f'<path d="M3,104 L237,104" stroke-width="1.4"/>'
                + f'<path d="M30,108 L190,108 Q214,108 222,100 L222,96 L30,96 Z" fill="{WHITE}" stroke-width="1.6"/><path d="M30,102 L214,102" stroke="{SKY}" stroke-width="2.4"/>'
                + skytree(140, 92, 40, 6) + f'<path d="M3,112 L237,112" stroke-width="1.6"/>',
                back(100, 120, GOLD, 1.0) + back(136, 122, SKY, .95)))

# 惠比壽花園廣場塔 38 樓 SKY LOUNGE（2026-11-19 補）：餐廳樓層的展望大廳，窗外東京鐵塔與彩虹大橋夜景
card('ebisu', '手繪高樓餐廳樓層的展望大廳，窗外是夜景裡的東京鐵塔和遠方的吊橋',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + win_room(''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>' for x in range(10, 230, 9) for y in (102, 110) if (x * y) % 4)
                + tower(70, 112, 56, sw=12)
                + ''.join(f'<rect x="{x}" y="84" width="5" height="26" fill="{WHITE}" stroke-width="1"/>' for x in (170, 206))
                + f'<path d="M150,92 Q172,86 172,84 Q190,104 208,84 Q208,86 230,92" fill="none" stroke="{WHITE}" stroke-width="1.4"/>'
                + f'<path d="M3,112 L237,112" stroke-width="1.6"/>',
                back(110, 120, GOLD, 1.0) + back(146, 122, PINK, .95))
     + star(30, 22, 4), bg=NIGHT)

print(save(F, OUT), 'files')
