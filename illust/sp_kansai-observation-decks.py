# 關西觀景台懶人包（/kansai/observation-decks/）的手繪插圖（2026-11-18）。
# 阿倍野 HARUKAS 借用 illust/sp/osaka-abeno-harukas/ 的圖，這裡只畫其他觀景台與封面。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物（通天閣的比利肯不畫）。
# 輸出 illust/sp/kansai-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'kansai-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
TURF = '#9fd08a'
PORT = '#d9534a'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('kd-' + name, W, H, label, inner, bg=bg)


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


def umeda(cx, base, h, s=1.0):
    # 梅田藍天大廈：兩棟大樓頂上用一圈空中庭園連起來
    w = 22 * s
    g = 18 * s
    top = base - h
    t = (bldg(cx - g - w, base, w, h) + bldg(cx + g, base, w, h)
         + f'<rect x="{cx-g-w}" y="{top-4*s}" width="{2*(g+w)}" height="{12*s}" rx="{3*s}" fill="{SKY}" stroke-width="1.8"/>'
         + f'<circle cx="{cx}" cy="{top+20*s}" r="{9*s}" fill="{WHITE}" stroke-width="1.6"/>'
         + f'<path d="M{cx-g},{base-h*.45} L{cx+g},{base-h*.45}" stroke-width="2"/>')
    return t


def tsutenkaku(cx, base, h, s=1.0):
    # 通天閣：四隻腳的塔、上面方形展望台、頂上圓頂
    top = base - h
    t = (f'<path d="M{cx-18*s},{base} L{cx-6*s},{top+h*.35} L{cx+6*s},{top+h*.35} L{cx+18*s},{base} '
         f'L{cx+10*s},{base} Q{cx},{base-16*s} {cx-10*s},{base} Z" fill="{GRAY}" stroke-width="1.8"/>'
         + f'<rect x="{cx-12*s}" y="{top+h*.12}" width="{24*s}" height="{h*.25}" rx="{2*s}" fill="{WHITE}" stroke-width="1.8"/>'
         + f'<rect x="{cx-12*s}" y="{top+h*.2}" width="{24*s}" height="{5*s}" fill="{GOLD}" stroke-width="1.2"/>'
         + f'<path d="M{cx-9*s},{top+h*.12} Q{cx},{top} {cx+9*s},{top+h*.12} Z" fill="{SKY}" stroke-width="1.6"/>'
         + f'<path d="M{cx},{top} L{cx},{top-8*s}" stroke-width="2"/>')
    return t


def kyototower(cx, base, h, s=1.0):
    # 京都塔：白色細長塔身、圓盤展望室、紅白頂端，下面是大樓
    top = base - h
    t = (bldg(cx - 30 * s, base, 60 * s, h * .28, WHITE)
         + f'<path d="M{cx-8*s},{base-h*.28} Q{cx-5*s},{top+h*.3} {cx-3*s},{top+h*.18} L{cx+3*s},{top+h*.18} Q{cx+5*s},{top+h*.3} {cx+8*s},{base-h*.28} Z" fill="{WHITE}" stroke-width="1.8"/>'
         + f'<ellipse cx="{cx}" cy="{top+h*.16}" rx="{11*s}" ry="{5*s}" fill="{SKY}" stroke-width="1.6"/>'
         + f'<rect x="{cx-2.5*s}" y="{top}" width="{5*s}" height="{h*.12}" fill="{RED}" stroke-width="1.2"/>')
    return t


def porttower(cx, base, h, s=1.0):
    # 神戶港塔：紅色、上下寬中間窄的沙漏形
    top = base - h
    t = (f'<path d="M{cx-16*s},{base} Q{cx-2*s},{base-h*.5} {cx-14*s},{top+h*.1} L{cx+14*s},{top+h*.1} '
         f'Q{cx+2*s},{base-h*.5} {cx+16*s},{base} Z" fill="{PORT}" stroke-width="1.8"/>'
         + ''.join(f'<path d="M{cx-12*s},{y} L{cx+12*s},{y}" stroke="{WHITE}" stroke-width="1" opacity=".8"/>'
                   for y in [base - h * k / 7 for k in range(1, 7)])
         + f'<rect x="{cx-16*s}" y="{top}" width="{32*s}" height="{h*.12}" rx="{2*s}" fill="{WHITE}" stroke-width="1.6"/>')
    return t


# 0. 封面：大阪的天際線（梅田藍天大廈、通天閣、HARUKAS）、京都塔、神戶港塔，前面有人看景
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="#f7d9b8"/>'
         + f'<path d="M3,150 Q3,3 25,3 L695,3 Q717,3 717,25 L717,150 Z" fill="#f4c7a0" stroke="none"/>'
         + f'<circle cx="630" cy="80" r="28" fill="{GOLD}"/>'
         + cloud(80, 70, 1.3) + cloud(330, 46, 1.1) + cloud(560, 140, .9)
         + f'<path d="M3,262 L3,200 Q120,170 230,200 L230,262 Z" fill="#c9b8d6" stroke-width="1.6"/>'
         + kyototower(90, 262, 150, 1.0)
         + umeda(250, 262, 150, 1.1)
         + bldg(330, 262, 30, 90) + bldg(366, 262, 36, 210, '#d9d2e9')
         + tsutenkaku(450, 262, 130, 1.1)
         + bldg(500, 262, 26, 70)
         + porttower(620, 262, 130, 1.1)
         + f'<path d="M560,262 L700,262 L700,250 Q630,240 560,250 Z" fill="#9fd0ea" stroke-width="1.4"/>'
         + f'<path d="M3,262 L717,262 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#e9dcc8"/>'
         + f'<path d="M3,262 L717,262" stroke-width="2.4"/>'
         + f'<rect x="60" y="270" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(180, 232, PINK, 1.6) + back(300, 236, GREEN, 1.5) + back(540, 232, SKY, 1.6)
         + star(170, 40, 8) + sparkle(470, 40, 6) + sparkle(30, 120, 5))
F['hero'] = svg('kd-hero', 720, 330, '手繪插圖：黃昏的關西天際線，有京都塔、梅田藍天大廈、阿倍野 HARUKAS、通天閣和神戶港塔，三個人站在窗邊看景色', _hero)

# 1. 梅田藍天大廈 空中庭園：兩棟大樓頂上連成一圈的露天迴廊
card('umeda', '手繪兩棟大樓頂上用一圈露天迴廊連在一起，人在迴廊上看夜景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in [(30, 30, WHITE), (90, 20, GOLD), (200, 26, WHITE), (220, 60, GOLD)])
     + umeda(120, 170, 120, 1.4)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>' for x, y in [(70, 100), (78, 120), (162, 110), (170, 130), (74, 140), (166, 150)])
     + back(96, 30, PINK, .8) + back(146, 30, GOLD, .8)
     + star(206, 120, 6) + sparkle(30, 90, 5), bg=NIGHT)

# 2. 通天閣
card('tsutenkaku', '手繪通天閣，塔上方形的展望台和圓頂，下面是熱鬧的商店街招牌',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .8) + cloud(180, 30, .8)
     + tsutenkaku(120, 150, 130, 1.4)
     + ''.join(f'<rect x="{x}" y="{y}" width="26" height="16" rx="3" fill="{c}" stroke-width="1.4"/>' for x, y, c in [(20, 116, GOLD), (52, 126, RED), (166, 120, PINK), (198, 128, GOLD)])
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + kid(60, 150, GREEN, .9) + kid(184, 150, PINK, .9)
     + sparkle(206, 70, 4))

# 3. 咲洲宇宙塔：海邊的高樓，看大阪灣
card('cosmo', '手繪海邊的高樓，頂樓玻璃展望台，下面是大阪灣和船',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 36, .9) + cloud(190, 50, .7)
     + f'<path d="M92,150 L92,40 L120,24 L148,40 L148,150 Z" fill="{GRAY}" stroke-width="1.8"/>'
     + ''.join(f'<path d="M96,{y} L144,{y}" stroke-width="1" opacity=".45"/>' for y in range(56, 146, 10))
     + f'<path d="M92,40 L120,24 L148,40 L148,50 L92,50 Z" fill="{SKY}" stroke-width="1.6"/>'
     + f'<path d="M3,138 L237,138 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ea"/>'
     + f'<path d="M170,146 L210,146 L204,156 L176,156 Z" fill="{WHITE}" stroke-width="1.4"/><path d="M190,146 L190,132 L200,142 Z" fill="{RED}" stroke-width="1.2"/>'
     + back(120, 60, GOLD, .7)
     + sparkle(40, 90, 4) + star(210, 26, 5))

# 4. 京都塔
card('kyototower', '手繪京都車站前的白色京都塔，下面是瓦片屋頂的街道',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .8) + cloud(190, 36, .8)
     + kyototower(120, 160, 140, 1.3)
     + ''.join(f'<path d="M{x},150 L{x+16},138 L{x+32},150 Z" fill="#7d8aa8" stroke-width="1.4"/><rect x="{x+4}" y="150" width="24" height="10" fill="{CREAM}" stroke-width="1.2"/>' for x in (10, 44, 162, 196))
     + f'<path d="M3,160 L237,160 L237,155 Q237,177 215,177 L25,177 Q3,177 3,160 Z" fill="#e9dcc8"/>'
     + sparkle(206, 80, 4))

# 5. 神戶港塔：紅色沙漏形的塔、海、船
card('porttower', '手繪港邊紅色的神戶港塔，旁邊是海和小船',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 36, .9) + cloud(186, 40, .8)
     + porttower(100, 150, 120, 1.4)
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ea"/>'
     + f'<path d="M150,140 L210,140 L202,152 L158,152 Z" fill="{WHITE}" stroke-width="1.4"/><rect x="170" y="128" width="20" height="12" rx="2" fill="{SKY}" stroke-width="1.2"/>'
     + kid(200, 112, PINK, .8)
     + sparkle(40, 90, 4))

# 6. 六甲山：山上看神戶夜景
card('rokko', '手繪山頂的展望台，往下看海邊城市一片閃亮的夜景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in [(30, 24, WHITE), (90, 30, GOLD), (180, 20, WHITE), (214, 44, GOLD)])
     + f'<path d="M3,70 Q120,90 237,70 L237,130 L3,130 Z" fill="#3f4a78" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{GOLD}" stroke="none"/>' for x in range(14, 230, 11) for y in (96, 108) if (x * 7 + y) % 3)
     + f'<path d="M3,118 L237,118 L237,130 L3,130 Z" fill="#26305a" stroke="none"/>'
     + f'<path d="M3,130 L80,112 L150,124 L237,108 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{DGREEN}"/>'
     + back(110, 112, PINK, 1.0) + back(140, 114, GOLD, 1.0)
     + star(200, 60, 5), bg=NIGHT)

# 7. 京都車站大樓的大階梯（免費）
card('kyotostation', '手繪車站大樓裡長長的大階梯，一路往上通到屋頂廣場',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + ''.join(f'<path d="M{x},3 L{x+30},60" stroke-width="1.4" opacity=".5"/>' for x in range(20, 230, 30))
     + f'<path d="M20,60 L220,60" stroke-width="2"/>'
     + ''.join(f'<path d="M{30+i*9},{170-i*9} L{230-i*3},{170-i*9}" stroke-width="1.6"/>' for i in range(12))
     + f'<path d="M30,170 L138,62 L226,62 L230,170 Z" fill="#e9dcc8" opacity=".55" stroke="none"/>'
     + kid(90, 120, RED, .9) + kid(150, 84, GREEN, .8) + kid(190, 50, GOLD, .7)
     + sparkle(40, 30, 4))

# 8. 大阪車站的空中庭園（免費）
card('osakastation', '手繪車站頂樓的大屋頂廣場，下面一條條鐵軌和電車',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,40 Q120,8 237,40" fill="none" stroke-width="2.2"/>'
     + ''.join(f'<path d="M{x},{40-abs(120-x)*0 - (1-((x-120)/117)**2)*32:.0f} L{x},60" stroke-width="1.2" opacity=".5"/>' for x in range(20, 230, 20))
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#b9bfc9"/>'
     + ''.join(f'<path d="M3,{y} L237,{y}" stroke-width="1.4"/>' for y in (134, 150, 166))
     + f'<rect x="30" y="138" width="80" height="12" rx="5" fill="{WHITE}" stroke-width="1.4"/><rect x="130" y="154" width="90" height="12" rx="5" fill="{GOLD}" stroke-width="1.4"/>'
     + f'<path d="M3,96 L237,96 L237,112 L3,112 Z" fill="{TURF}"/><path d="M3,96 L237,96" stroke-width="2.2"/>'
     + ''.join(f'<path d="M{x},96 L{x},84" stroke-width="1.4"/>' for x in range(14, 236, 14)) + f'<path d="M3,84 L237,84" stroke-width="1.6"/>'
     + back(80, 76, PINK, .9) + back(150, 76, SKY, .9)
     + sparkle(206, 24, 4))

# 9. 神戶市役所 24 樓（免費）
card('kobecity', '手繪市政府大樓高樓層的觀景大廳，窗外是港口和山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,70 L50,40 L100,62 L160,34 L237,66 L237,90 L3,90 Z" fill="{GREEN}" stroke-width="1.6"/>'
     + bldg(20, 112, 16, 22) + bldg(40, 112, 12, 30) + bldg(170, 112, 18, 26)
     + porttower(120, 112, 40, .5)
     + f'<path d="M3,112 L237,112 L237,124 L3,124 Z" fill="#9fd0ea" stroke-width="1.2"/>'
     + ''.join(f'<path d="M{x},3 L{x},128" stroke-width="3"/>' for x in (80, 160))
     + f'<path d="M3,128 L237,128 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M3,128 L237,128" stroke-width="2.4"/>'
     + back(100, 120, GOLD, 1.0) + back(140, 122, PINK, .95)
     + sparkle(214, 20, 4))

# 10. 摩耶山 掬星台（免費，搭纜車上山）
card('maya', '手繪山上的觀景廣場，旁邊是小小的纜車，下面是城市夜景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in [(30, 24, WHITE), (70, 40, GOLD), (200, 22, WHITE)])
     + f'<path d="M3,112 Q120,130 237,110 L237,150 L3,150 Z" fill="#3f4a78" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{GOLD}" stroke="none"/>' for x in range(14, 230, 10) for y in (130, 140) if (x + y) % 3)
     + f'<path d="M20,20 L220,100" stroke-width="1.4"/>'
     + f'<rect x="150" y="62" width="30" height="22" rx="4" fill="{RED}" stroke-width="1.6"/><path d="M165,62 L165,74" stroke-width="1.2"/>'
     + f'<path d="M3,150 Q60,138 120,146 T237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{DGREEN}"/>'
     + back(70, 140, PINK, .9) + back(100, 142, GOLD, .9)
     + star(120, 30, 6), bg=NIGHT)

# 11. 大阪城天守閣：石牆上的白牆綠瓦天守，8 樓展望台看出去
card('castle', '手繪石牆上的白牆綠屋頂天守閣，最上層有人在看風景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(30, 40, .8) + cloud(196, 34, .7)
     + f'<path d="M60,160 L72,120 L168,120 L180,160 Z" fill="#b9a68c" stroke-width="1.8"/>'
     + ''.join(f'<path d="M{70+i*2},{128+i*8} L{170-i*2},{128+i*8}" stroke-width="1" opacity=".5"/>' for i in range(4))
     + ''.join(f'<rect x="{120-w/2}" y="{y}" width="{w}" height="16" fill="{WHITE}" stroke-width="1.6"/>'
               f'<path d="M{120-w/2-8},{y} Q120,{y-10} {120+w/2+8},{y} Z" fill="#5f9e8a" stroke-width="1.6"/>'
               for w, y in ((76, 104), (60, 86), (46, 68), (32, 50)))
     + f'<rect x="108" y="54" width="24" height="8" fill="{GOLD}" stroke-width="1.2"/>'
     + f'<path d="M3,160 L237,160 L237,155 Q237,177 215,177 L25,177 Q3,177 3,160 Z" fill="{TURF}"/>'
     + back(34, 140, PINK, .9) + back(200, 140, GOLD, .9)
     + sparkle(206, 80, 4))

# 12. 將軍塚青龍殿 大舞台：山上的木造大平台，往下看京都市區
card('shogunzuka', '手繪山上一大片木頭平台，欄杆外面是京都的街道和遠山',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,70 Q60,52 120,66 T237,60 L237,100 L3,100 Z" fill="#b8c9a3" stroke-width="1.4"/>'
     + ''.join(bldg(x, 100, w, h, '#d6d0c4') for x, w, h in ((20, 10, 14), (40, 14, 20), (70, 10, 12), (150, 12, 18), (176, 16, 24), (206, 10, 14)))
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#c9a06b"/>'
     + ''.join(f'<path d="M{x},112 L{x-20},177" stroke-width="1" opacity=".5"/>' for x in range(30, 240, 26))
     + f'<path d="M3,104 L237,104" stroke-width="2.4"/>' + ''.join(f'<path d="M{x},104 L{x},112" stroke-width="1.6"/>' for x in range(14, 236, 18))
     + back(100, 120, RED, 1.0) + back(136, 122, SKY, .95)
     + sparkle(206, 28, 4) + cloud(40, 34, .7))

# 13. 馬賽克大摩天輪：港邊的摩天輪
card('umie', '手繪港邊的摩天輪，車廂一個個亮著，前面是海',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in [(30, 24, WHITE), (200, 30, GOLD), (220, 70, WHITE)])
     + f'<circle cx="110" cy="80" r="56" fill="none" stroke="{WHITE}" stroke-width="2.4"/>'
     + ''.join(f'<path d="M110,80 L{110+56*__import__("math").cos(a/6*3.1416):.1f},{80+56*__import__("math").sin(a/6*3.1416):.1f}" stroke="{WHITE}" stroke-width="1" opacity=".7"/>'
               f'<circle cx="{110+56*__import__("math").cos(a/6*3.1416):.1f}" cy="{80+56*__import__("math").sin(a/6*3.1416):.1f}" r="6" fill="{[GOLD, PINK, SKY][a % 3]}" stroke-width="1.2"/>' for a in range(12))
     + f'<path d="M96,150 L110,80 L124,150" fill="none" stroke="{WHITE}" stroke-width="2"/>'
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#3f6f9a"/>'
     + f'<rect x="170" y="120" width="50" height="30" rx="3" fill="#e9dcc8" stroke-width="1.4"/>'
     + star(200, 100, 5), bg=NIGHT)

# 14. 若草山：草坡小山、山頂看奈良盆地，有鹿
card('wakakusa', '手繪一整片草坡的小山，山頂有人坐著看遠方的平原，旁邊有一隻鹿',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(160, 36, .9)
     + f'<path d="M3,120 Q50,44 120,40 Q190,44 237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{TURF}" stroke-width="1.8"/>'
     + f'<path d="M30,110 Q80,80 120,74" fill="none" stroke-width="1.2" opacity=".5"/>'
     + back(112, 34, PINK, .8) + back(130, 36, GOLD, .75)
     + f'<ellipse cx="180" cy="128" rx="16" ry="8" fill="#c8915a" stroke-width="1.6"/>'
     + f'<circle cx="196" cy="116" r="6" fill="#c8915a" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x},134 L{x},146" stroke-width="2"/>' for x in (170, 176, 186, 192))
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{WHITE}" stroke="none"/>' for x, y in ((174, 126), (182, 124), (186, 130)))
     + sparkle(40, 40, 4))

# 15. 布引香草園纜車：纜車掛在山坡上，下面是花園
card('nunobiki', '手繪一台小纜車掛在山坡上，下面是一層層的花圃',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,150 L237,40" stroke-width="1.6"/>'
     + f'<rect x="96" y="84" width="34" height="26" rx="5" fill="{WHITE}" stroke-width="1.6"/><path d="M113,84 L113,96" stroke-width="1.2"/>'
     + f'<rect x="102" y="90" width="22" height="10" rx="2" fill="{SKY}" stroke-width="1.2"/>'
     + f'<path d="M3,150 Q100,120 237,100 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{DGREEN}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{c}" stroke="none"/>' for x, y, c in ((40, 156, PINK), (60, 150, GOLD), (90, 146, PINK), (130, 140, GOLD), (170, 132, PINK), (200, 128, WHITE), (220, 124, GOLD), (110, 158, WHITE), (160, 154, PINK)))
     + sparkle(40, 40, 4) + cloud(170, 30, .7))

# 16. 難波公園 PARKS GARDEN：一層層往上的屋頂花園
card('nambaparks', '手繪一層層往上的階梯狀屋頂花園，種滿樹，有人在步道上散步',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(40, 34, .8)
     + ''.join(f'<path d="M{20+i*24},{160-i*18} L{220},{160-i*18} L220,{178-i*18} L{20+i*24},{178-i*18} Z" fill="{["#e9dcc8", "#e2d3bd", "#dccbb2", "#d6c3a8", "#cfbb9e", "#c9b394"][i]}" stroke-width="1.4"/>' for i in range(6))
     + ''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="{GREEN}" stroke-width="1.4"/>' for x, y in ((50, 146), (90, 128), (130, 110), (170, 92), (200, 74), (110, 146), (190, 128)))
     + kid(150, 82, PINK, .7) + kid(80, 136, GOLD, .7)
     + sparkle(206, 30, 4))

# 17. 堺市役所 21 樓展望大廳：窗外是鑰匙孔形的古墳
card('sakai', '手繪高樓的觀景大廳，窗外遠方是一座鑰匙孔形狀、長滿樹的古墳',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + f'<path d="M3,74 Q120,60 237,72 L237,120 L3,120 Z" fill="#b8c9a3" stroke-width="1.2"/>'
     + f'<path d="M120,80 L150,96 Q160,108 140,112 L100,112 Q80,108 90,96 Z" fill="#9fb4d8" stroke-width="1.4"/>'
     + f'<circle cx="120" cy="88" r="14" fill="{DGREEN}" stroke-width="1.6"/><path d="M106,92 L96,108 L144,108 L134,92 Z" fill="{DGREEN}" stroke-width="1.6"/>'
     + bldg(20, 120, 14, 20) + bldg(190, 120, 16, 24)
     + ''.join(f'<path d="M{x},3 L{x},128" stroke-width="3"/>' for x in (70, 170))
     + f'<path d="M3,128 L237,128 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<path d="M3,128 L237,128" stroke-width="2.4"/>'
     + back(104, 120, SKY, 1.0) + back(140, 122, RED, .95)
     + sparkle(214, 20, 4))

# 18. 六甲山 天覽台：山頂平台、往下看平原與海
card('tenrandai', '手繪山頂的木頭平台，往下看遠方的平原和海',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f7d9b8"/>'
     + f'<circle cx="190" cy="50" r="18" fill="{GOLD}"/>'
     + f'<path d="M3,96 Q120,84 237,96 L237,120 L3,120 Z" fill="#c9b8d6" stroke-width="1.2"/>'
     + ''.join(bldg(x, 112, 6, h, '#b7a9c9') for x, h in ((30, 10), (44, 16), (60, 8), (150, 14), (170, 10)))
     + f'<path d="M3,112 L237,112 L237,120 L3,120 Z" fill="#9fd0ea" stroke="none"/>'
     + f'<path d="M3,130 L237,126 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#c9a06b"/>'
     + f'<path d="M3,126 L237,122" stroke-width="2.2"/>'
     + back(96, 128, GREEN, 1.0) + back(130, 128, PINK, 1.0)
     + cloud(50, 50, .8))

# 19. 維納斯橋：山腰的螺旋步道橋，看神戶夜景
card('venus', '手繪山腰一座繞成圓圈的步道橋，下面是神戶的夜景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in [(30, 24, WHITE), (90, 18, GOLD), (210, 30, WHITE)])
     + f'<path d="M3,110 Q120,124 237,108 L237,150 L3,150 Z" fill="#3f4a78" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{GOLD}" stroke="none"/>' for x in range(14, 230, 10) for y in (128, 140) if (x + y) % 3)
     + f'<ellipse cx="120" cy="80" rx="60" ry="18" fill="none" stroke="{WHITE}" stroke-width="5"/>'
     + f'<ellipse cx="120" cy="80" rx="60" ry="18" fill="none" stroke="{GOLD}" stroke-width="1.4"/>'
     + ''.join(f'<path d="M{x},{y} L{x},150" stroke="{WHITE}" stroke-width="2"/>' for x, y in ((80, 94), (160, 94)))
     + f'<path d="M3,150 Q60,140 120,146 T237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{DGREEN}"/>'
     + back(110, 64, PINK, .7) + back(130, 64, GOLD, .7)
     + star(200, 70, 5), bg=NIGHT)

print(save(F, OUT), 'files')
