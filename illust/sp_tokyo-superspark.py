# SUPER SPARK TOKYO 頁的「店裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網首頁、SYSTEM 頁與來店注意事項（superspark.tokyo/、/system/）畫成可愛版；
# 不畫表演者本人、不畫 logo，只畫舞台、飲料、座位與拍照規則。
# 輸出 illust/sp/tokyo-superspark/*.svg，說明文字在 illust/spots/tokyo-superspark.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-superspark')
W, H = 240, 180
DARK = '#2b2f55'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sp-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def confetti(pts):
    cols = [RED, GOLD, PINK, '#a9d4f5', '#c9f0d8']
    return ''.join(f'<rect x="{x}" y="{y}" width="5" height="3" rx="1" fill="{cols[i % 5]}" stroke="none" transform="rotate({(i*37)%90} {x} {y})"/>'
                   for i, (x, y) in enumerate(pts))


# 1. 舞台：燈光、彩帶，一晚三場
card('stage', '手繪舞台，上方打下好幾道彩色燈光、彩帶飛舞，台下觀眾在看',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{DARK}"/>'
     + f'<path d="M3,40 Q3,3 25,3 L46,3 Q44,60 30,110 L3,110 Z" fill="{RED}"/>'
     + f'<path d="M194,3 L215,3 Q237,3 237,25 L237,110 L210,110 Q196,60 194,3 Z" fill="{RED}"/>'
     + ''.join(f'<path d="M{x},10 L{x2-18},104 L{x2+18},104 Z" fill="{c}" opacity=".45" stroke="none"/>'
               for x, x2, c in [(70, 96, '#ffb3c7'), (120, 120, '#fff1a8'), (170, 144, '#a9d4f5')])
     + ''.join(f'<circle cx="{x}" cy="12" r="6" fill="{GOLD}" stroke-width="1.6"/>' for x in (70, 120, 170))
     + f'<path d="M30,104 L210,104 L222,124 L18,124 Z" fill="{BROWN}"/>'
     + ''.join(star(x, y, 4, c) for x, y, c in [(100, 80, GOLD), (140, 70, PINK), (120, 92, '#a9d4f5')])
     + confetti([(60, 40), (90, 30), (150, 36), (180, 50), (110, 56), (76, 70), (166, 80), (130, 44), (100, 22), (196, 70)])
     + f'<path d="M3,124 L237,124 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#20244a"/>'
     + back(50, 140, PINK, 1.0) + back(90, 144, GOLD, 1.0) + back(150, 142, SKY, 1.0) + back(190, 140, GREEN, 1.0)
     + f'<path d="M78,132 l-4,-8 M162,130 l4,-8" stroke="{WHITE}" stroke-width="1.6"/>', bg=DARK)

# 2. 兩杯飲料＋小費額度
card('drinks', '手繪兩杯飲料乾杯，旁邊一個小信封',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f3e6f7"/>'
     + f'<path d="M3,130 L237,130 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{BROWN}"/>'
     + f'<g transform="rotate(-10 86 96)"><path d="M66,56 L106,56 L100,128 L72,128 Z" fill="#ffd27a"/>'
     + f'<path d="M68,70 L104,70" stroke="{WHITE}" stroke-width="3"/>' + face(86, 100, .8) + '</g>'
     + f'<g transform="rotate(10 150 96)"><path d="M130,56 L170,56 L164,128 L136,128 Z" fill="#ffb3c7"/>'
     + f'<path d="M132,70 L168,70" stroke="{WHITE}" stroke-width="3"/>' + face(150, 100, .8) + '</g>'
     + f'<path d="M110,44 l-4,-10 M118,40 l0,-12 M126,44 l4,-10" stroke="{GOLD}" stroke-width="2.4"/>'
     + f'<rect x="184" y="108" width="40" height="28" rx="3" fill="{WHITE}"/>'
     + f'<path d="M184,108 L204,124 L224,108" fill="none" stroke-width="1.8"/>'
     + star(204, 128, 5) + sparkle(40, 40, 5) + sparkle(200, 36, 4) + star(36, 100, 5))

# 3. 座位：2 樓席、前排、沙發、自由座（側面剖面）
def chair(x, y, c):
    return (f'<path d="M{x},{y} L{x},{y-20} Q{x},{y-24} {x+4},{y-24} L{x+6},{y-24}" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y-8}" width="16" height="6" rx="2" fill="{c}"/>'
            f'<path d="M{x+2},{y-2} L{x+2},{y+8} M{x+14},{y-2} L{x+14},{y+8}" stroke-width="2"/>')
card('seats', '手繪表演廳的側面：左邊是舞台，前面一排椅子、中間沙發，右上是一層 2 樓席',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#efe6f5"/>'
     + f'<path d="M3,40 Q3,3 25,3 L52,3 L52,120 L3,120 Z" fill="{RED}"/>'
     + f'<path d="M3,120 L64,120 L64,140 L3,140 Z" fill="{BROWN}"/>'
     + ''.join(star(x, y, 4) for x, y in [(20, 30), (36, 60), (22, 90)])
     + f'<path d="M3,156 L237,156 L237,158 Q237,177 215,177 L25,177 Q3,177 3,158 Z" fill="{DBROWN}"/>'
     + chair(74, 148, GOLD) + chair(96, 148, GOLD)
     + kid(84, 112, PINK, .8)
     + f'<path d="M124,128 L124,156 L174,156 L174,128 Q174,120 166,120 L132,120 Q124,120 124,128 Z" fill="#c9b8f0"/>'
     + f'<rect x="130" y="134" width="38" height="14" rx="4" fill="#e3d8fb" stroke-width="1.4"/>'
     + kid(140, 108, SKY, .75) + kid(158, 108, GOLD, .75)
     + f'<path d="M180,80 L237,80 L237,90 L180,90 Z" fill="{GRAY}"/>'
     + f'<path d="M184,80 L184,64 L234,64" fill="none" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},64 L{x},80" stroke-width="1.4"/>' for x in (196, 208, 220))
     + kid(200, 50, GREEN, .7) + kid(222, 50, RED, .7)
     + f'<path d="M186,90 L186,156 M232,90 L232,156" stroke-width="2"/>'
     + kid(206, 128, PINK, .75)
     + ''.join(f'<path d="M{x},20 L{x2},110" stroke="#fff1a8" stroke-width="2" opacity=".8"/>' for x, x2 in [(30, 40), (40, 56)])
     + sparkle(120, 30, 5) + sparkle(160, 60, 4))

# 4. 拍照：可以拍，但不能用閃光燈
card('camera', '手繪拿手機拍舞台的人，旁邊是打叉的閃光燈',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{DARK}"/>'
     + f'<path d="M30,20 L210,20 L210,80 L30,80 Z" fill="#3d4378"/>'
     + ''.join(star(x, y, 5, c) for x, y, c in [(70, 50, GOLD), (120, 40, PINK), (170, 56, '#a9d4f5')])
     + confetti([(50, 30), (90, 64), (146, 30), (190, 40), (106, 26)])
     + f'<path d="M3,120 L237,120 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#20244a"/>'
     + kid(80, 120, PINK, 1.2)
     + f'<rect x="92" y="94" width="26" height="40" rx="5" fill="{GRAY}"/><rect x="96" y="98" width="18" height="28" rx="2" fill="#a9d4f5" stroke-width="1.4"/>'
     + star(105, 112, 4)
     + f'<path d="M88,136 L94,124" stroke-width="3"/>'
     + f'<path d="M168,104 L178,90 L176,102 L188,100 L176,120 L178,108 L166,110 Z" fill="{GOLD}"/>'
     + f'<circle cx="177" cy="105" r="22" fill="none" stroke="{RED}" stroke-width="3.4"/>'
     + f'<path d="M161,89 L193,121" stroke="{RED}" stroke-width="3.4"/>', bg=DARK)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('sp-' + name, 120, 120, label, inner, bg='#fff3c4')


# 自由座：客滿可能站著看、分開坐
rem('r-standing', '手繪提醒：坐滿的椅子旁邊站著的人',
    f'<rect x="10" y="70" width="18" height="18" rx="3" fill="{PINK}"/><rect x="34" y="70" width="18" height="18" rx="3" fill="{PINK}"/><rect x="58" y="70" width="18" height="18" rx="3" fill="{PINK}"/>'
    + back(19, 52, GOLD, .8) + back(43, 52, SKY, .8) + back(67, 52, GREEN, .8)
    + f'<path d="M14,88 L14,100 M24,88 L24,100 M38,88 L38,100 M48,88 L48,100 M62,88 L62,100 M72,88 L72,100" stroke-width="2"/>'
    + kid(96, 54, RED, 1.0)
    + f'<path d="M91,76 L91,100 M101,76 L101,100" stroke-width="3"/>')

# 同一棟有兩家：認清 B1
rem('r-floor', '手繪提醒：大樓剖面圖，地下 1 樓打星號',
    f'<path d="M10,40 L110,40" stroke="{GREEN}" stroke-width="4"/>'
    + f'<rect x="24" y="14" width="72" height="26" fill="{GRAY}"/>'
    + f'<rect x="24" y="44" width="72" height="30" rx="2" fill="{GOLD}"/>'
    + f'<rect x="24" y="78" width="72" height="30" rx="2" fill="{GRAY}"/>'
    + f'<text x="50" y="65" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">B1</text>'
    + f'<text x="50" y="99" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none" opacity=".55">B2</text>'
    + star(80, 59, 8, RED))

print(save(F, OUT), 'files')
