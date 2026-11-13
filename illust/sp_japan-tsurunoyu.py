# 鶴之湯頁的「鶴之湯有什麼」插圖與提醒卡（2026-11-13）。
# 參考鶴之湯官網（tsurunoyu.com/FONDMENT/t-annai、t-onsen、t-shoku、t-ko-tu）的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/japan-tsurunoyu/*.svg（240×180）。說明文字放在 illust/spots/japan-tsurunoyu.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-tsurunoyu')
W, H = 240, 180
SKYW = '#e3eef7'
THATCH = '#d9b36c'
MILK = '#e8eef4'
MILKB = '#cdd9e4'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('tn-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def steam(xs, y, h=16):
    return ''.join(f'<path d="M{x},{y} q-5,-{h/2} 0,-{h} q5,-{h/2} 0,-{h*2}" fill="none" stroke-width="1.8" opacity=".5"/>' for x in xs)


def head(x, y, s=1.0, hair=INK):
    return (f'<circle cx="{x}" cy="{y}" r="{8*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-8*s},{y-1*s} q{8*s},{-12*s} {16*s},0 Z" fill="{hair}" stroke-width="1.2"/>'
            + face(x, y + 2 * s, .45 * s))


# 1. 名字的由來：鶴在溫泉裡療傷
card('crane', '手繪一隻鶴站在冒熱氣的乳白色溫泉裡',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + floor(118, WHITE)
     + f'<ellipse cx="120" cy="138" rx="96" ry="26" fill="{MILKB}"/>'
     + f'<ellipse cx="120" cy="136" rx="84" ry="18" fill="{MILK}"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="6" fill="#b9c3cf" stroke-width="1.6"/>' for x, y in [(30, 132), (40, 150), (200, 150), (212, 132)])
     + steam([70, 172], 112)
     # 鶴：白色身體、黑色尾羽、紅色頭頂
     + f'<path d="M120,138 L116,152 M132,138 L136,152" stroke-width="2.4"/>'
     + f'<path d="M92,112 Q100,92 132,96 Q150,100 146,120 Q132,134 108,128 Q96,124 92,112 Z" fill="{WHITE}"/>'
     + f'<path d="M92,112 Q80,118 78,130 Q90,126 100,124 Z" fill="{INK}"/>'
     + f'<path d="M140,104 Q150,80 148,56" fill="none" stroke-width="7" stroke="{INK}"/>'
     + f'<path d="M140,104 Q150,80 148,56" fill="none" stroke-width="4" stroke="{WHITE}"/>'
     + f'<circle cx="150" cy="50" r="10" fill="{WHITE}"/>'
     + f'<path d="M144,42 Q150,36 156,42 Q150,44 144,42 Z" fill="{RED}" stroke-width="1.2"/>'
     + f'<path d="M158,50 L176,54 L158,55 Z" fill="{GOLD}" stroke-width="1.3"/>'
     + f'<circle cx="152" cy="50" r="1.8" fill="{INK}" stroke="none"/>'
     + f'<ellipse cx="146" cy="55" rx="3" ry="1.8" fill="{PINK}" stroke="none" opacity=".85"/>'
     + f'<path d="M108,112 q10,6 22,2" fill="none" stroke-width="1.4"/>'
     + flake(30, 30) + flake(206, 28) + star(60, 50, 5))

# 2. 本陣：茅草屋頂的長屋
card('honjin', '手繪雪中一長排茅草屋頂的木造長屋',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<rect x="22" y="96" width="196" height="46" fill="{DBROWN}"/>'
     + ''.join(f'<rect x="{x}" y="106" width="26" height="24" rx="2" fill="{GOLD}" stroke-width="1.4"/>' for x in (34, 74, 114, 154, 190 - 2))
     + ''.join(f'<path d="M{x+13},106 L{x+13},130 M{x},118 L{x+26},118" stroke-width="1.1"/>' for x in (34, 74, 114, 154, 188))
     + f'<path d="M8,100 Q20,52 60,44 L180,44 Q220,52 232,100 Z" fill="{THATCH}"/>'
     + ''.join(f'<path d="M{x},{y} l6,8" stroke-width="1.1" opacity=".55"/>' for x, y in [(40, 70), (70, 60), (110, 56), (150, 60), (190, 66), (60, 84), (130, 80), (200, 86)])
     + f'<path d="M20,70 Q40,48 66,44 L174,44 Q200,48 220,70 Q170,58 120,60 Q70,58 20,70 Z" fill="{WHITE}" stroke-width="1.8"/>'
     + face(126, 136, .6)
     + floor(142, WHITE)
     + flake(30, 26) + flake(210, 24) + star(120, 22, 5))

# 3. 混浴露天風呂（源泉是白湯）
card('rotenburo', '手繪雪中的乳白色露天溫泉，旁邊有茅草小屋頂',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M40,50 L40,100 M118,50 L118,100" stroke-width="3.4"/>'
     + f'<path d="M22,54 L79,22 L136,54 Q79,46 22,54 Z" fill="{THATCH}"/>'
     + f'<path d="M30,50 Q79,40 128,50 L79,26 Z" fill="{WHITE}" stroke-width="1.6"/>'
     + floor(100, WHITE)
     + f'<ellipse cx="124" cy="136" rx="104" ry="32" fill="{MILKB}"/>'
     + f'<ellipse cx="124" cy="134" rx="92" ry="24" fill="{MILK}"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="7" fill="#b9c3cf" stroke-width="1.6"/>' for x, y in [(26, 128), (34, 150), (214, 150), (224, 128), (120, 166)])
     + head(96, 128, 1.0) + head(140, 126, 1.0, DBROWN) + head(176, 132, .9)
     + steam([70, 120, 200], 108)
     + flake(200, 30) + flake(170, 60, 4) + star(214, 80, 5))

# 4. 四個源泉：白湯、黑湯、中之湯、瀧之湯
tubs = ''
for i, (x, lab, extra) in enumerate([(40, '白', ''), (94, '黑', ''), (148, '中', ''), (202, '瀧', 'fall')]):
    tubs += (f'<ellipse cx="{x}" cy="126" rx="24" ry="12" fill="{BROWN}"/>'
             f'<ellipse cx="{x}" cy="124" rx="19" ry="8" fill="{MILK if i != 1 else "#c8ccd4"}"/>'
             + steam([x], 112, 10)
             + f'<rect x="{x-13}" y="142" width="26" height="22" rx="5" fill="{WHITE}" stroke-width="1.6"/>'
             f'<text x="{x}" y="159" font-size="15" text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">{lab}</text>')
card('springs', '手繪四個小浴池，分別寫著白、黑、中、瀧',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + floor(112, WHITE)
     + f'<path d="M202,60 L202,116" stroke="{MILKB}" stroke-width="6"/>'
     + f'<path d="M190,60 L214,60 L214,52 L190,52 Z" fill="{BROWN}"/>'
     + tubs
     + f'<circle cx="120" cy="56" r="34" fill="none" stroke-width="1.6" stroke-dasharray="4 5"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}" stroke-width="1.4"/>' for x, y, c in [(104, 46, MILK), (130, 40, '#c8ccd4'), (114, 68, MILK), (138, 62, MILK)])
     + flake(30, 30) + flake(60, 70, 4) + star(214, 30, 5))

# 5. 地爐旁的晚餐＋鹽烤岩魚；下雪天戴斗笠送餐
card('irori', '手繪地爐邊插著烤的魚和小鍋子，旁邊有戴斗笠的人端著餐盤',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f3e2c0"/>'
     + f'<rect x="20" y="104" width="130" height="56" rx="6" fill="{DBROWN}"/>'
     + f'<rect x="32" y="114" width="106" height="36" rx="4" fill="#d9d2c4"/>'
     + ''.join(f'<path d="M{x},{y} q4,-6 8,0 q4,6 8,0" fill="{RED}" stroke-width="1.4"/>' for x, y in [(58, 136), (80, 138), (100, 136)])
     + f'<path d="M84,30 L84,92" stroke-width="2.4"/>'
     + f'<path d="M68,92 Q84,80 100,92 L96,110 Q84,116 72,110 Z" fill="{INK}"/>'
     + ''.join(f'<g transform="rotate({r} {x} 132)"><path d="M{x},150 L{x},96" stroke="{BROWN}" stroke-width="2.4"/>'
               f'<path d="M{x},100 q8,8 0,22 q-8,-14 0,-22 Z" fill="#9fb4cf" stroke-width="1.4"/>'
               f'<circle cx="{x+1}" cy="104" r="1.4" fill="{INK}" stroke="none"/></g>'
               for x, r in [(46, -14), (122, 14)])
     + steam([80, 90], 76, 10)
     # 戴斗笠送餐的人（外面在下雪）
     + f'<rect x="160" y="18" width="66" height="148" rx="8" fill="{SKYW}"/>'
     + snow([(170, 30), (196, 26), (216, 44), (178, 60), (206, 70)], 2.2, WHITE)
     + f'<circle cx="192" cy="96" r="9" fill="#f9d9c0"/>' + face(192, 98, .45)
     + f'<path d="M172,92 L192,76 L212,92 Z" fill="{THATCH}"/>'
     + f'<path d="M180,128 q0,-22 12,-22 q12,0 12,22 Z" fill="{GREEN}"/>'
     + f'<rect x="172" y="114" width="40" height="8" rx="2" fill="{RED}"/>'
     + f'<circle cx="182" cy="110" r="4" fill="{WHITE}" stroke-width="1.2"/><circle cx="200" cy="110" r="4" fill="{GOLD}" stroke-width="1.2"/>'
     + f'<path d="M160,166 L226,166" stroke-width="2"/>')

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('tn-' + name, 120, 120, label, inner, bg='#fff3c4')


# 浴場在木橋對面
rem('r-bridge', '手繪提醒：走過木橋，對面才是溫泉',
    f'<path d="M4,78 L116,78 L116,96 L4,96 Z" fill="#9fc3dc" stroke="none"/>'
    f'<path d="M30,74 Q60,60 90,74 L90,80 Q60,66 30,80 Z" fill="{BROWN}"/>'
    f'<path d="M36,70 L36,60 M60,64 L60,54 M84,70 L84,60 M34,60 Q60,48 86,60" fill="none" stroke-width="2"/>'
    f'<rect x="90" y="38" width="26" height="30" rx="3" fill="{BROWN}"/>'
    f'<path d="M86,40 L103,26 L120,40 Z" fill="{THATCH}"/>'
    + steam([98, 108], 36, 6)
    + f'<path d="M14,52 L40,52 M32,44 L40,52 L32,60" stroke="{RED}" stroke-width="3" fill="none"/>'
    f'<rect x="6" y="56" width="22" height="22" rx="2" fill="{GRAY}"/>')

# 到田澤湖站先打電話報巴士班次
rem('r-phone', '手繪提醒：打電話和巴士時刻',
    f'<rect x="16" y="20" width="40" height="70" rx="7" fill="{NAVY}"/>'
    f'<rect x="21" y="28" width="30" height="48" rx="3" fill="{SKY}"/>'
    f'<path d="M30,44 q6,-6 12,0 M27,40 q9,-10 18,0" fill="none" stroke-width="1.6"/>'
    f'<circle cx="84" cy="48" r="24" fill="{WHITE}"/>'
    f'<path d="M84,48 L84,32 M84,48 L96,52" stroke-width="3"/>'
    f'<rect x="56" y="88" width="56" height="20" rx="6" fill="{GREEN}"/>'
    f'<circle cx="68" cy="108" r="4" fill="{INK}"/><circle cx="100" cy="108" r="4" fill="{INK}"/>')

# 開車：找鶴之湯的木頭招牌，林道約 3 公里
rem('r-sign', '手繪提醒：路口的木頭招牌和林道',
    f'<clipPath id="tn-rclip"><rect x="4.5" y="4.5" width="111" height="111" rx="20.5"/></clipPath>'
    f'<path d="M0,104 L60,104 Q80,104 90,80 Q100,56 120,42" fill="none" stroke="#e9dcc8" stroke-width="14" clip-path="url(#tn-rclip)"/>'
    f'<path d="M40,96 L40,40" stroke-width="3"/><path d="M60,96 L60,40" stroke-width="3"/>'
    f'<rect x="28" y="28" width="44" height="40" rx="3" fill="{BROWN}"/>'
    f'<path d="M36,38 L64,38 M36,48 L58,48 M36,58 L62,58" stroke-width="2"/>'
    + ''.join(f'<path d="M{x},{y} l-8,16 l16,0 Z" fill="{DGREEN}" stroke-width="1.4"/>' for x, y in [(92, 30), (108, 64), (14, 60)])
    + f'<path d="M78,90 L96,74 M88,74 L96,74 L96,82" stroke="{RED}" stroke-width="3" fill="none"/>')

print(save(F, OUT), 'files')
