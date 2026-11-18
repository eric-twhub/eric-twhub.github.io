# 名古屋觀景台頁（/nagoya/observation-decks/）的手繪插圖（2026-11-19）。
# 照各官網的介紹畫成可愛版，不描照片構圖、不畫商標與吉祥物。輸出 illust/sp/nagoya-observation-decks/*.svg，gen.py 直接內嵌。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'nagoya-observation-decks')
W, H = 240, 180
SKYB = '#cfe8f7'
DUSK = '#f7d9b8'
NIGHT = '#3d4a78'
SEA = '#9fd0ea'
MTN = '#9cc59a'
F = {}
BOX = '<rect x="3" y="3" width="234" height="174" rx="22" fill="{c}"/>'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ng-' + name, W, H, label, inner, bg=bg)


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def town(base, n=9, col='#e9e1d3', x0=14, step=24):
    t = ''
    for i in range(n):
        x = x0 + i * step
        h = 10 + (i * 7) % 14
        t += f'<rect x="{x}" y="{base-h}" width="18" height="{h}" fill="{col}" stroke-width="1.2"/>'
    return t


def lattice_tower(cx, top, base, wb, wt, col=RED):
    # 鐵塔：梯形外框加交叉斜撐
    t = f'<path d="M{cx-wb},{base} L{cx-wt},{top} L{cx+wt},{top} L{cx+wb},{base} Z" fill="none" stroke="{col}" stroke-width="3"/>'
    n = 5
    for i in range(n):
        y0 = top + (base - top) * i / n
        y1 = top + (base - top) * (i + 1) / n
        w0 = wt + (wb - wt) * i / n
        w1 = wt + (wb - wt) * (i + 1) / n
        t += f'<path d="M{cx-w0:.1f},{y0:.1f} L{cx+w1:.1f},{y1:.1f} M{cx+w0:.1f},{y0:.1f} L{cx-w1:.1f},{y1:.1f}" stroke="{col}" stroke-width="1.6"/>'
    return t


def wheel(cx, cy, r, n=12, hub=WHITE):
    t = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="2.2"/>'
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        t += (f'<path d="M{cx},{cy} L{x:.1f},{y:.1f}" stroke-width="1"/>'
              f'<rect x="{x-4:.1f}" y="{y-3:.1f}" width="8" height="7" rx="2" fill="{PINK if i % 2 else GOLD}" stroke-width="1"/>')
    return t + f'<circle cx="{cx}" cy="{cy}" r="{r*.18:.1f}" fill="{hub}" stroke-width="1.6"/>'


def castle(cx, base, s=1.0, wall=WHITE, roof='#5d6b7a'):
    # 天守：三層屋頂＋石垣
    t = f'<path d="M{cx-34*s},{base} L{cx-28*s},{base-18*s} L{cx+28*s},{base-18*s} L{cx+34*s},{base} Z" fill="#c9c2b4" stroke-width="1.6"/>'
    y = base - 18 * s
    for i, w in enumerate((26, 20, 14)):
        h = 14 * s
        t += f'<rect x="{cx-w*s}" y="{y-h}" width="{2*w*s}" height="{h}" fill="{wall}" stroke-width="1.4"/>'
        t += f'<path d="M{cx-(w+8)*s},{y-h} L{cx-(w-4)*s},{y-h-8*s} L{cx+(w-4)*s},{y-h-8*s} L{cx+(w+8)*s},{y-h} Z" fill="{roof}" stroke-width="1.4"/>'
        y = y - h - 8 * s
    return t + f'<path d="M{cx-6*s},{y} L{cx+6*s},{y}" stroke="{GOLD}" stroke-width="3"/>'


# 中部電力 MIRAI TOWER：公園中央的鐵塔
card('mirai', '手繪長條公園中間的紅色鐵塔，塔的中段有一圈展望室，兩邊是城市大樓',
     BOX.format(c=SKYB) + cloud(30, 40, .8) + cloud(180, 30, .7)
     + town(150, 3, '#eef0f4', 10, 22) + town(150, 3, '#eef0f4', 168, 22)
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{GREEN}" stroke-width="1.6"/>'
     + lattice_tower(120, 30, 150, 30, 6)
     + f'<rect x="100" y="80" width="40" height="14" rx="4" fill="{WHITE}" stroke-width="1.6"/>'
     + f'<rect x="108" y="44" width="24" height="8" rx="3" fill="{WHITE}" stroke-width="1.4"/><path d="M120,30 L120,14" stroke-width="2"/>'
     + ''.join(f'<circle cx="{x}" cy="158" r="7" fill="{DGREEN}" stroke-width="1.2"/>' for x in (30, 60, 180, 210))
     + back(60, 120, GOLD, .7))
# Midland Square Sky Promenade：高樓頂端的露天迴廊
card('midland', '手繪高樓最上面幾層是露天的展望迴廊，人站在欄杆邊，背景是黃昏的城市',
     BOX.format(c=DUSK) + f'<circle cx="190" cy="50" r="16" fill="{GOLD}" stroke-width="1.6"/>'
     + town(170, 9, '#e7d6c6')
     + f'<path d="M84,177 L92,40 L148,40 L156,177 Z" fill="#c9d4e6" stroke-width="2"/>'
     + ''.join(f'<path d="M{94+i*0.3},{70+i*20} L{146-i*0.3},{70+i*20}" stroke-width="1"/>' for i in range(5))
     + f'<path d="M86,40 L154,40 L150,26 L90,26 Z" fill="{WHITE}" stroke-width="1.8"/>'
     + f'<path d="M90,34 L150,34" stroke-width="1.2"/>' + back(108, 14, RED, .6) + back(132, 14, SKY, .6))
# 東山 Sky Tower：森林山丘上的白塔
card('higashiyama', '手繪綠色山丘森林上的細長白塔，頂端是圓圓的展望室，下面有小動物園的柵欄',
     BOX.format(c=SKYB) + cloud(40, 40, .8)
     + f'<path d="M3,130 Q80,96 160,118 Q200,108 237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{MTN}" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="10" fill="{DGREEN}" stroke-width="1.2"/>' for x, y in ((30, 132), (54, 124), (190, 126), (214, 130), (80, 138)))
     + f'<path d="M126,118 L130,46 L142,46 L146,118 Z" fill="{WHITE}" stroke-width="1.8"/>'
     + f'<ellipse cx="136" cy="44" rx="20" ry="12" fill="{SKY}" stroke-width="1.8"/><path d="M136,32 L136,18" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},150 L{x},164" stroke-width="1.6"/>' for x in range(150, 216, 10)) + '<path d="M146,154 L216,154" stroke-width="1.6"/>'
     + back(100, 140, PINK, .7))
# 名古屋港 Port Building：港邊像帆的白色大樓
card('portbldg', '手繪港口邊像船帆一樣的白色大樓，旁邊停著一艘白色的大船，海面有小波浪',
     BOX.format(c=SKYB) + cloud(170, 34, .8)
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{SEA}" stroke-width="1.4"/>'
     + f'<path d="M60,120 L80,40 Q96,60 100,120 Z" fill="{WHITE}" stroke-width="2"/><rect x="72" y="58" width="20" height="8" rx="2" fill="{SKY}" stroke-width="1.2"/>'
     + f'<path d="M130,118 L210,118 L200,134 L140,134 Z" fill="{WHITE}" stroke-width="1.8"/><rect x="150" y="104" width="40" height="14" rx="3" fill="{WHITE}" stroke-width="1.6"/>'
     + f'<path d="M140,126 L200,126" stroke="{RED}" stroke-width="3"/>'
     + ''.join(f'<path d="M{x},150 q6,-5 12,0" fill="none" stroke-width="1.4"/>' for x in (30, 80, 120, 170))
     + back(84, 98, GOLD, .6))
# Sunshine Sakae Sky-Boat：大樓側面的摩天輪
card('skyboat', '手繪商業大樓側面嵌著一座彩色摩天輪，晚上的城市燈光',
     BOX.format(c=NIGHT) + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>' for x, y in ((30, 30), (70, 22), (200, 28), (150, 18)))
     + f'<rect x="40" y="70" width="110" height="107" fill="#e8e2d4" stroke-width="2"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{GOLD}" stroke-width="1"/>' for x in (54, 80, 106) for y in (90, 120, 150))
     + wheel(150, 92, 52, 14, PINK))
# Oasis 21「水の宇宙船」：橢圓玻璃屋頂上的水
card('oasis21', '手繪公園上方浮著一個橢圓形的玻璃屋頂，屋頂上有一層水，人在上面散步，旁邊是鐵塔',
     BOX.format(c=SKYB) + town(110, 9, '#eef0f4')
     + lattice_tower(200, 26, 110, 14, 3)
     + f'<path d="M100,124 L106,170 M140,124 L134,170" stroke-width="3"/>'
     + f'<ellipse cx="120" cy="110" rx="100" ry="18" fill="#bfe3f2" stroke-width="2"/><ellipse cx="120" cy="106" rx="84" ry="10" fill="{SEA}" stroke-width="1.2"/>'
     + f'<path d="M3,160 L237,160 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{GREEN}" stroke-width="1.4"/>'
     + back(80, 82, RED, .6) + back(150, 82, GOLD, .6))
# 中部國際機場 Sky Deck：伸到海上的長甲板與飛機
card('centrair', '手繪伸向海面的長條木甲板，前面一架飛機正在起飛，人在欄杆邊看',
     BOX.format(c=SKYB) + cloud(40, 40, .8)
     + f'<path d="M3,110 L237,110 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{SEA}" stroke-width="1.4"/>'
     + f'<path d="M3,140 L170,118 L180,124 L3,152 Z" fill="{BROWN}" stroke-width="1.6"/>'
     + f'<g transform="translate(150,60) rotate(-14)"><rect x="0" y="0" width="64" height="12" rx="6" fill="{WHITE}" stroke-width="1.8"/>'
       f'<path d="M24,6 L14,28 L30,28 L40,6 Z" fill="{WHITE}" stroke-width="1.4"/><path d="M4,6 L0,-8 L8,-8 L14,2 Z" fill="{SKY}" stroke-width="1.4"/></g>'
     + back(60, 120, RED, .7) + back(90, 116, SKY, .7))
# 犬山城：河邊山丘上的天守
card('inuyama', '手繪大河邊小山丘上的白色天守，最上層有一圈外廊，河上有小船',
     BOX.format(c=SKYB) + cloud(180, 36, .8)
     + f'<path d="M3,130 L237,130 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{SEA}" stroke-width="1.4"/>'
     + f'<path d="M40,132 Q110,64 200,132 Z" fill="{MTN}" stroke-width="1.6"/>'
     + castle(120, 100, .9)
     + f'<path d="M30,150 L60,150 L56,156 L34,156 Z" fill="{BROWN}" stroke-width="1.2"/>'
     + back(150, 36, PINK, .5))
# 岐阜城＋金華山纜車：山頂城、纜車
card('gifujo', '手繪高高的山頂上有小小的天守，纜車沿著纜線往山頂爬，山下是河和城市',
     BOX.format(c=SKYB)
     + f'<path d="M3,150 Q60,140 110,150" fill="none" stroke="{SEA}" stroke-width="8"/>' + town(150, 4, '#eef0f4')
     + f'<path d="M100,177 L170,40 L237,110 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + castle(170, 44, .55)
     + f'<path d="M60,150 L160,52" stroke-width="1.4"/>'
     + f'<path d="M110,101 L110,108" stroke-width="1.2"/><rect x="100" y="108" width="20" height="14" rx="3" fill="{RED}" stroke-width="1.4"/>')
# Twin Arch 138：雙拱高塔
card('twinarch', '手繪大公園裡兩道細長的白色拱形組成的高塔，頂端有展望室，旁邊是河',
     BOX.format(c=SKYB) + cloud(30, 40, .8)
     + f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{GREEN}" stroke-width="1.6"/>'
     + f'<path d="M3,150 Q120,140 237,156" fill="none" stroke="{SEA}" stroke-width="8"/>'
     + f'<path d="M90,140 Q96,30 120,24 Q144,30 150,140" fill="none" stroke-width="7" stroke="{WHITE}"/><path d="M90,140 Q96,30 120,24 Q144,30 150,140" fill="none" stroke-width="1.6"/>'
     + f'<path d="M102,140 Q108,52 120,48 Q132,52 138,140" fill="none" stroke-width="1.6"/>'
     + f'<rect x="106" y="40" width="28" height="10" rx="3" fill="{SKY}" stroke-width="1.4"/>'
     + back(60, 116, GOLD, .7) + back(180, 116, RED, .7))
# 御在所纜車：高空纜車越過山谷、山頂
card('gozaisho', '手繪纜車從山腳越過深谷往岩石山頂開，山頂有展望台，旁邊是雲',
     BOX.format(c=SKYB)
     + f'<path d="M3,177 L3,150 L60,150 L237,40 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + f'<path d="M150,100 L170,86 L190,92 L210,70" fill="none" stroke="#8a8f99" stroke-width="2.6"/>'
     + f'<path d="M30,150 L210,52" stroke-width="1.4"/>'
     + f'<path d="M110,106 L110,114" stroke-width="1.2"/><rect x="100" y="114" width="20" height="14" rx="3" fill="{GOLD}" stroke-width="1.4"/>'
     + cloud(30, 110, .8, '#f2f2f2') + cloud(150, 140, .8, '#f2f2f2')
     + f'<rect x="200" y="50" width="26" height="8" rx="2" fill="{BROWN}" stroke-width="1.4"/>' + back(212, 30, RED, .55))

# JR Central Towers Sky Street：玻璃走廊看鐵道
card('jrskystreet', '手繪大樓高處一整面玻璃的走廊，窗外下面是好幾條鐵軌和電車，遠方是山',
     BOX.format(c=SKYB) + f'<path d="M3,70 Q60,50 120,66 Q180,48 237,64" fill="none" stroke="{MTN}" stroke-width="6"/>'
     + town(110, 9, '#eef0f4')
     + ''.join(f'<path d="M3,{124+i*12} L237,{116+i*12}" stroke="#8a8f99" stroke-width="1.6"/>' for i in range(3))
     + f'<rect x="40" y="114" width="70" height="10" rx="4" fill="{GOLD}" stroke-width="1.4"/><rect x="130" y="126" width="80" height="10" rx="4" fill="{WHITE}" stroke-width="1.4"/>'
     + ''.join(f'<path d="M{x},20 L{x},160" stroke="{GRAY}" stroke-width="5"/>' for x in (60, 120, 180))
     + f'<path d="M3,160 L237,160 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e8e2d4" stroke-width="1.6"/>'
     + back(90, 140, RED, .7) + back(150, 140, SKY, .7))
# 大名古屋大樓 Sky Garden：屋頂庭園、白色燈樹、高樓
card('dnbskygarden', '手繪大樓之間的空中庭園，晚上有閃亮的白色聖誕樹和小燈，旁邊是高樓',
     BOX.format(c=NIGHT) + f'<path d="M150,177 L156,24 L196,24 L202,177 Z" fill="#7d86a8" stroke-width="1.8"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="8" height="8" fill="{GOLD}" stroke-width=".8"/>' for x in (164, 184) for y in (40, 70, 100))
     + f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#a9d48f" stroke-width="1.6"/>'
     + f'<path d="M70,140 L96,60 L122,140 Z" fill="{WHITE}" stroke-width="1.8"/>' + star(96, 56, 8)
     + ''.join(sparkle(x, y, 3) for x, y in ((30, 60), (40, 110), (130, 90), (220, 60), (82, 120), (110, 104)))
     + back(40, 120, PINK, .7))
# 清洲城：紅色橋、城、燈飾
card('kiyosu', '手繪河邊的白牆天守，前面有一座紅色的橋，晚上庭園有小燈',
     BOX.format(c=DUSK) + castle(150, 120, .9)
     + f'<path d="M3,130 L237,130 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{SEA}" stroke-width="1.4"/>'
     + f'<path d="M20,140 Q70,112 120,140" fill="none" stroke="{RED}" stroke-width="6"/><path d="M28,134 L28,150 M60,124 L60,146 M92,124 L92,146 M114,134 L114,150" stroke="{RED}" stroke-width="3"/>'
     + ''.join(sparkle(x, y, 3) for x, y in ((190, 100), (210, 116), (100, 96)))
     + back(70, 104, SKY, .6))
# 小牧山：山頂天守風建築、森林
card('komakiyama', '手繪綠色圓圓的小山，山頂有白牆的小天守，外面一圈回廊有人在看景',
     BOX.format(c=SKYB) + cloud(180, 34, .8)
     + f'<path d="M3,177 L3,150 Q120,70 237,150 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="{DGREEN}" stroke-width="1.2"/>' for x, y in ((50, 142), (76, 124), (166, 124), (192, 142), (100, 150), (140, 152)))
     + castle(120, 112, .7) + back(146, 50, GOLD, .5))
# 岡崎城：天守與河
card('okazaki', '手繪石垣上的白色天守，前面兩條河匯在一起，岸邊有樹',
     BOX.format(c=SKYB) + cloud(40, 34, .8)
     + f'<path d="M3,138 L237,138 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{SEA}" stroke-width="1.4"/>'
     + f'<path d="M3,138 Q120,118 237,138" fill="{GREEN}" stroke-width="1.4"/>'
     + castle(120, 130, 1.0)
     + ''.join(f'<circle cx="{x}" cy="128" r="9" fill="{DGREEN}" stroke-width="1.2"/>' for x in (30, 54, 186, 210)))
# 刈谷觀覽車：高速公路休息區、透明車廂的摩天輪
card('kariya', '手繪公路休息區旁的大摩天輪，車廂彩色，下面是公園和小房子',
     BOX.format(c=SKYB) + cloud(30, 34, .8)
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{GREEN}" stroke-width="1.6"/>'
     + wheel(130, 82, 56, 16) + f'<path d="M108,150 L130,82 L152,150" fill="none" stroke-width="2.6"/>'
     + f'<rect x="20" y="124" width="56" height="26" fill="#e8e2d4" stroke-width="1.6"/><path d="M14,124 L48,108 L82,124 Z" fill="{RED}" stroke-width="1.4"/>'
     + back(200, 128, PINK, .7))
# 四日市 うみてらす14：港邊大樓、工廠夜景
card('umiterasu', '手繪港邊的高大樓，晚上窗外是亮著燈的工廠和煙囪，海面倒映燈光',
     BOX.format(c=NIGHT) + f'<path d="M30,177 L36,40 L80,40 L86,177 Z" fill="#c9d4e6" stroke-width="1.8"/><rect x="40" y="48" width="36" height="12" fill="{GOLD}" stroke-width="1.2"/>'
     + f'<path d="M86,128 L237,128 L237,155 Q237,177 215,177 L86,177 Z" fill="#2b3560" stroke-width="1.2"/>'
     + ''.join(f'<rect x="{x}" y="{128-h}" width="12" height="{h}" fill="#5c6690" stroke-width="1.2"/>' for x, h in ((110, 50), (140, 34), (170, 60), (200, 40)))
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{GOLD}" stroke="none"/>' for x, y in ((116, 90), (146, 100), (176, 76), (206, 96), (126, 110), (186, 104), (214, 112)))
     + ''.join(f'<path d="M{x},150 l8,0" stroke="{GOLD}" stroke-width="2"/>' for x in (110, 150, 190))
     + back(58, 30, RED, .5))
# 岐阜 City Tower 43：高樓與遠方山上的城
card('gifu43', '手繪車站旁的高樓，頂樓窗邊的人看向遠方山頂上的小城和一條河',
     BOX.format(c=SKYB)
     + f'<path d="M110,177 L160,60 L200,100 L237,90 L237,155 Q237,177 215,177 Z" fill="{MTN}" stroke-width="1.6"/>' + castle(160, 64, .4)
     + f'<path d="M100,170 Q170,150 237,160" fill="none" stroke="{SEA}" stroke-width="7"/>'
     + f'<path d="M30,177 L34,30 L78,30 L82,177 Z" fill="#d6dbe6" stroke-width="1.8"/><rect x="38" y="36" width="36" height="14" fill="{SKY}" stroke-width="1.2"/>'
     + ''.join(f'<path d="M36,{60+i*20} L80,{60+i*20}" stroke-width="1"/>' for i in range(5))
     + back(58, 26, GOLD, .5))
# 豐橋市役所：市役所高樓、路面電車
card('toyohashi', '手繪方正的市府大樓，頂樓是展望大廳，前面街上跑著一輛小小的路面電車',
     BOX.format(c=SKYB) + cloud(180, 34, .8)
     + f'<rect x="60" y="40" width="80" height="110" fill="#e8e2d4" stroke-width="1.8"/><rect x="64" y="44" width="72" height="14" fill="{SKY}" stroke-width="1.2"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="12" height="10" fill="{WHITE}" stroke-width="1"/>' for x in (70, 94, 118) for y in (70, 94, 118))
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#cfc6b6" stroke-width="1.4"/>'
     + f'<path d="M3,164 L237,164" stroke="#8a8f99" stroke-width="1.6"/><path d="M150,140 L150,130 L230,130" fill="none" stroke-width="1.2"/>'
     + f'<rect x="150" y="140" width="64" height="22" rx="6" fill="{GOLD}" stroke-width="1.6"/><rect x="158" y="145" width="12" height="8" fill="{WHITE}" stroke-width="1"/><rect x="176" y="145" width="12" height="8" fill="{WHITE}" stroke-width="1"/><rect x="194" y="145" width="12" height="8" fill="{WHITE}" stroke-width="1"/>'
     + ''.join(f'<circle cx="{x}" cy="150" r="8" fill="{DGREEN}" stroke-width="1.2"/>' for x in (20, 40))
     + back(100, 22, RED, .5))

# 封面：名古屋的街（鐵塔、橢圓水屋頂、高樓、天守、摩天輪）
_hero = (f'<rect x="3" y="3" width="714" height="324" rx="22" fill="{DUSK}"/>'
         + cloud(80, 64, 1.3) + cloud(560, 50, 1.0)
         + f'<circle cx="650" cy="96" r="22" fill="{GOLD}" stroke-width="1.8"/>'
         + ''.join(f'<rect x="{x}" y="{236-h}" width="{w}" height="{h}" fill="#e7d6c6" stroke-width="1.4"/>'
                   for x, w, h in ((20, 30, 60), (54, 26, 90), (420, 24, 70), (448, 30, 110), (482, 22, 64), (660, 34, 80)))
         # 兩棟高樓（車站前）
         + f'<path d="M520,236 L526,70 L566,70 L572,236 Z" fill="#c9d4e6" stroke-width="2"/><path d="M522,70 L570,70 L566,58 L526,58 Z" fill="{WHITE}" stroke-width="1.6"/>'
         + f'<path d="M582,236 L586,104 L616,104 L620,236 Z" fill="#d6dbe6" stroke-width="1.8"/>'
         # 鐵塔
         + lattice_tower(170, 40, 236, 42, 8)
         + f'<rect x="142" y="118" width="56" height="18" rx="5" fill="{WHITE}" stroke-width="1.8"/><path d="M170,40 L170,18" stroke-width="2.2"/>'
         # 橢圓水屋頂
         + f'<path d="M262,214 L268,240 M318,214 L312,240" stroke-width="3"/>'
         + f'<ellipse cx="290" cy="204" rx="78" ry="14" fill="#bfe3f2" stroke-width="2"/><ellipse cx="290" cy="201" rx="64" ry="7" fill="{SEA}" stroke-width="1.2"/>'
         # 天守
         + castle(380, 236, 1.2)
         # 摩天輪
         + wheel(90, 170, 46, 12, PINK)
         + f'<path d="M3,236 L717,236 L717,305 Q717,327 695,327 L25,327 Q3,327 3,305 Z" fill="#efe2cf"/>'
         + f'<path d="M3,236 L717,236" stroke-width="2.4"/>'
         + f'<rect x="60" y="250" width="600" height="10" rx="4" fill="{BROWN}"/>'
         + back(220, 220, RED, 1.6) + back(380, 224, SKY, 1.5) + back(540, 220, GOLD, 1.6))
F['hero'] = svg('ng-hero', 720, 330, '手繪插圖：黃昏的名古屋街景，有紅色鐵塔、浮在空中的橢圓水屋頂、白色天守、摩天輪和車站前的高樓，三個人站在欄杆邊看', _hero)

print(save(F, OUT), 'files')
