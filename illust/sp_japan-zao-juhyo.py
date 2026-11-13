# 藏王樹冰頁的「山上有什麼」插圖與提醒卡（2026-11-13）。
# 參考藏王纜車官網（zaoropeway.co.jp/winter/juhyo.php、guide.php、juhyo_illusion.php）與すみかわ官網 /tour/ 的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/japan-zao-juhyo/*.svg（240×180）。說明文字放在 illust/spots/japan-zao-juhyo.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-zao-juhyo')
W, H = 240, 180
SKYW = '#e3eef7'
NIGHT = '#2e3a63'
FIR = '#4f8a6a'
SHADE = '#d6e2ee'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('zj-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def monster(x, base, h, w, col=WHITE, smile=True, s=.75):
    # 有臉的樹冰（雪包住的冷杉），兩側露出一點點綠枝
    t = (f'<path d="M{x-w/2},{base} Q{x-w*.66:.0f},{base-h*.45:.0f} {x-w*.32:.0f},{base-h*.62:.0f} '
         f'Q{x-w*.48:.0f},{base-h*.86:.0f} {x-w*.12:.0f},{base-h*.9:.0f} Q{x},{base-h-6} {x+w*.14:.0f},{base-h*.9:.0f} '
         f'Q{x+w*.5:.0f},{base-h*.84:.0f} {x+w*.32:.0f},{base-h*.6:.0f} Q{x+w*.66:.0f},{base-h*.42:.0f} {x+w/2},{base} Z" '
         f'fill="{col}"/>'
         f'<path d="M{x-w*.3:.0f},{base-h*.4:.0f} l-7,-4 M{x+w*.3:.0f},{base-h*.5:.0f} l7,-5" stroke="{DGREEN}" stroke-width="2"/>')
    if smile:
        t += face(x, base - h * .55, s)
    return t


def person(x, y, col=RED, s=1.0, hat=None):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if hat:
        t += f'<path d="M{x-6.5*s},{y-1*s} q{6.5*s},{-11*s} {13*s},0 Z" fill="{hat}" stroke-width="1.4"/>'
    return t


def gondola(x, y, col=RED, s=1.0):
    return (f'<path d="M{x},{y-16*s} L{x},{y}" stroke-width="2"/>'
            f'<rect x="{x-18*s}" y="{y}" width="{36*s}" height="{30*s}" rx="{7*s}" fill="{col}"/>'
            f'<rect x="{x-13*s}" y="{y+5*s}" width="{26*s}" height="{11*s}" rx="3" fill="{SKY}" stroke-width="1.4"/>'
            + face(x, y + 22 * s, .55 * s))


def snowcat(x, y, s=1.0, col=GOLD):
    # 一般的雪上車：方方的車廂＋履帶
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-46" y="-34" width="92" height="34" rx="7" fill="{col}"/>'
            f'<path d="M30,-34 L46,-20 L46,0 L30,0 Z" fill="{col}"/>'
            + ''.join(f'<rect x="{-38+i*16}" y="-27" width="11" height="11" rx="2" fill="{SKY}" stroke-width="1.3"/>' for i in range(4))
            + f'<rect x="34" y="-26" width="8" height="10" rx="2" fill="{SKY}" stroke-width="1.3"/>'
            f'<rect x="-50" y="0" width="100" height="18" rx="9" fill="#6c7a8c"/>'
            + ''.join(f'<circle cx="{cx}" cy="9" r="5" fill="{GRAY}" stroke-width="1.4"/>' for cx in (-36, -12, 12, 36))
            + f'<circle cx="40" cy="-8" r="3" fill="{WHITE}" stroke-width="1.2"/>'
            f'</g>')


# 1. 兩段纜車：樹冰在上面那一段
card('ropeway', '手繪纜車從雪山往上開，山頂一帶有很多樹冰',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,150 L120,70 L237,30 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WHITE}"/>'
     + monster(176, 66, 34, 22, smile=False) + monster(204, 56, 40, 26) + monster(150, 80, 28, 18, smile=False)
     + f'<path d="M3,120 L237,20" stroke-width="1.8"/>'
     + f'<path d="M60,148 L60,94 M50,94 L70,94" stroke-width="3"/>'
     + f'<path d="M150,108 L150,56 M140,56 L160,56" stroke-width="3"/>'
     + gondola(100, 93, RED)
     + monster(40, 168, 30, 22, smile=False)
     + flake(30, 30) + flake(80, 22, 4) + star(120, 26, 5))

# 2. 樹冰的構造：冷杉被冰和雪包住，迎風面長出「蝦尾巴」
card('ebi', '手繪一棵被冰雪包住的冷杉，枝上長出一排排像蝦尾巴的冰',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + floor(150, WHITE)
     + f'<path d="M120,26 L150,80 L136,80 L162,130 L78,130 L104,80 L90,80 Z" fill="{FIR}"/>'
     + f'<g transform="translate(240,0) scale(-1,1)">'
     + f'<path d="M120,26 Q132,40 132,56 L150,80 L140,82 Q146,100 162,130 L150,132 Q140,110 128,96 Z" fill="{WHITE}" stroke-width="1.8"/>'
     + ''.join(f'<path d="M{x},{y} l14,-5 l-3,5 l5,4 Z" fill="{WHITE}" stroke-width="1.4"/>'
               for x, y in [(134, 48), (146, 72), (152, 94), (160, 114), (166, 128)])
     + '</g>'
     + ''.join(f'<path d="M{x},{y} q-10,-4 -18,2" fill="none" stroke="#8fc0e0" stroke-width="2"/>' for x, y in [(70, 50), (60, 70), (66, 92)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#8fc0e0" stroke="none"/>' for x, y in [(80, 46), (84, 64), (76, 86), (88, 100)])
     + f'<path d="M110,130 L110,146 L130,146 L130,130" fill="{DBROWN}" stroke-width="1.6"/>'
     + face(126, 112, .7)
     + flake(200, 30) + flake(36, 140, 4) + star(204, 70, 5))

# 3. 一季的變化：初期→成長→最盛→變細
stages = (monster(40, 132, 30, 22, smile=False) + f'<path d="M40,102 L40,132" stroke="{FIR}" stroke-width="5" opacity=".6"/>'
          + monster(96, 132, 50, 32) + monster(158, 132, 76, 48) + monster(212, 132, 46, 18, smile=False))
card('season', '手繪四棵大小不同的樹冰，從小小一棵長到很大，最後變細',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + floor(132, WHITE) + stages
     + ''.join(f'<text x="{x}" y="160" font-size="13" text-anchor="middle" fill="{INK}" stroke="none" '
               f'font-family="sans-serif">{t}</text>' for x, t in [(40, '11～12月'), (96, '1月'), (158, '2月'), (212, '3月')])
     + f'<path d="M206,106 q4,6 0,12" stroke="#8fc0e0" stroke-width="2" fill="none"/>'
     + flake(30, 30) + flake(120, 24, 4) + star(200, 30, 5))

# 4. 地藏山頂站附近的藏王地藏尊（可愛版的石地藏）
card('jizo', '手繪雪中一尊戴紅色圍兜的石地藏，旁邊有樹冰',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + monster(46, 140, 70, 40, smile=False) + monster(200, 136, 60, 34, smile=False)
     + f'<path d="M86,140 L86,96 Q86,70 120,70 Q154,70 154,96 L154,140 Z" fill="#b9bfc8"/>'
     + f'<circle cx="120" cy="64" r="22" fill="#b9bfc8"/>'
     + face(120, 64, .9)
     + f'<path d="M98,92 L142,92 L136,118 Q120,124 104,118 Z" fill="{RED}"/>'
     + f'<path d="M86,62 Q120,30 154,62 Q120,48 86,62 Z" fill="{WHITE}" stroke-width="1.8"/>'
     + floor(140, WHITE)
     + flake(30, 24) + flake(210, 28) + star(170, 30, 5))

# 5. 點燈＋夜間雪上車
card('night', '手繪晚上打了彩色燈光的樹冰，雪上車從中間開過',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{WHITE}" stroke="none"/>' for x, y in [(30, 24), (80, 18), (150, 30), (210, 20), (190, 50)])
     + monster(40, 128, 70, 40, '#f7c6d0') + monster(110, 120, 80, 44, '#c9e6ff') + monster(196, 126, 72, 42, '#fff1b8')
     + floor(130, '#d9e3f2')
     + snowcat(120, 146, .62, RED)
     + f'<path d="M150,138 L196,128 L196,150 Z" fill="{GOLD}" opacity=".35" stroke="none"/>'
     + star(56, 30, 5))

# 6. 宮城側：雪上車開進樹冰原
card('sumikawa', '手繪雪上車在雪原上往樹冰群開',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,92 Q120,72 237,92 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WHITE}"/>'
     + monster(150, 92, 50, 30, smile=False) + monster(186, 90, 64, 36) + monster(218, 94, 40, 24, smile=False) + monster(124, 94, 30, 20, smile=False)
     + f'<path d="M3,150 Q80,130 140,108" fill="none" stroke="{SHADE}" stroke-width="10"/>'
     + snowcat(70, 136, .8)
     + face(102, 118, .55)
     + flake(30, 30) + flake(80, 22, 4) + star(120, 30, 5))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('zj-' + name, 120, 120, label, inner, bg='#fff3c4')


# 山上多半是暴風雪
rem('r-blizzard', '手繪提醒：山上風雪很大',
    f'<path d="M20,50 Q20,30 42,32 Q50,16 70,22 Q92,18 96,38 Q110,42 104,56 L26,56 Q16,56 20,50 Z" fill="{GRAY}"/>'
    + ''.join(f'<path d="M{x},{y} q14,-4 28,0 q8,2 6,-6" fill="none" stroke="#8fa6c0" stroke-width="2.6"/>' for x, y in [(14, 74), (40, 88), (20, 102)])
    + flake(84, 76, 6, '#8fa6c0') + flake(100, 96, 5, '#8fa6c0') + flake(66, 104, 4, '#8fa6c0'))

# 海報上的 QR code 掃不到，要按頁面下方的按鈕
rem('r-qr', '手繪提醒：模糊的 QR code 和手機',
    f'<rect x="14" y="20" width="56" height="56" rx="4" fill="{WHITE}"/>'
    + ''.join(f'<rect x="{x}" y="{y}" width="10" height="10" fill="#9aa3b0" stroke="none" opacity=".7"/>'
              for x, y in [(20, 26), (54, 26), (20, 60), (36, 40), (46, 50), (36, 60), (56, 46)])
    + f'<path d="M16,22 L68,74" stroke="{RED}" stroke-width="4"/>'
    f'<rect x="66" y="44" width="40" height="66" rx="7" fill="{NAVY}"/>'
    f'<rect x="71" y="52" width="30" height="46" rx="3" fill="{SKY}"/>'
    f'<rect x="75" y="82" width="22" height="9" rx="3" fill="{GREEN}" stroke-width="1.2"/>')

print(save(F, OUT), 'files')
