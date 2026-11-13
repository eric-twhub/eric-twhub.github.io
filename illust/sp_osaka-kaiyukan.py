# 海遊館頁的「館內有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網展示紹介頁（kaiyukan.com/about/exhibition/）的介紹畫成可愛版，不描照片構圖；
# 海遊館的吉祥物不畫。
# 輸出 illust/sp/osaka-kaiyukan/*.svg。說明文字放在 illust/spots/osaka-kaiyukan.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'osaka-kaiyukan')
W, H = 240, 180
F = {}
SEA = '#bfe3f5'
DEEP = '#7fb6dc'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ky-' + name, W, H, label, inner, bg=bg)


def fishy(x, y, col, s=1.0, left=False):
    d = -1 if left else 1
    return (f'<path d="M{x},{y} q{10*s*d},{-8*s} {20*s*d},0 q{-10*s*d},{8*s} {-20*s*d},0 Z" fill="{col}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} l{-7*s*d},{-6*s} l0,{12*s} Z" fill="{col}" stroke-width="1.4"/>'
            f'<circle cx="{x+14*s*d}" cy="{y-1}" r="1.3" fill="{INK}" stroke="none"/>')


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def whaleshark(x, y, s=1.0):
    t = (f'<path d="M{x},{y} q{30*s},{-26*s} {80*s},{-14*s} q{20*s},{4*s} {34*s},{-10*s} '
         f'l{-4*s},{20*s} l{6*s},{18*s} q{-16*s},{-10*s} {-36*s},{-6*s} q{-50*s},{10*s} {-80*s},{-8*s} Z" fill="#7fa9d6"/>'
         f'<path d="M{x+40*s},{y-18*s} l{8*s},{-14*s} l{8*s},{14*s}" fill="#7fa9d6"/>')
    for dx, dy in [(30, -8), (44, -12), (58, -6), (72, -12), (52, -2), (84, -6), (38, 0)]:
        t += f'<circle cx="{x+dx*s:.1f}" cy="{y+dy*s:.1f}" r="{1.8*s:.1f}" fill="{WHITE}" stroke="none"/>'
    t += f'<circle cx="{x+12*s:.1f}" cy="{y-6*s:.1f}" r="{1.8*s:.1f}" fill="{INK}" stroke="none"/>'
    t += f'<path d="M{x+4*s:.1f},{y+1*s:.1f} q{6*s:.1f},{3*s:.1f} {12*s:.1f},0" fill="none" stroke-width="1.6"/>'
    return t


def ray(x, y, s=1.0):
    return (f'<path d="M{x},{y} q{-30*s},{-6*s} {-40*s},{6*s} q{20*s},0 {40*s},{10*s} q{20*s},{-10*s} {40*s},{-10*s} '
            f'q{-10*s},{-12*s} {-40*s},{-6*s} Z" fill="#5b6f8f"/>'
            f'<path d="M{x},{y+10*s} q{2*s},{12*s} {10*s},{20*s}" fill="none" stroke-width="1.6"/>'
            f'<circle cx="{x-6*s}" cy="{y+3*s}" r="{1.5*s}" fill="{WHITE}" stroke="none"/>'
            f'<circle cx="{x+6*s}" cy="{y+3*s}" r="{1.5*s}" fill="{WHITE}" stroke="none"/>')


def bubbles(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke-width="1.3"/>' for x, y in pts)


# 1. 入口的水族門：像海底隧道
card('gate', '手繪藍色的海底隧道，頭上有熱帶魚游過',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SEA}"/>'
     f'<path d="M30,160 L30,90 Q30,26 120,26 Q210,26 210,90 L210,160" fill="#9fd0ec"/>'
     f'<path d="M58,160 L58,96 Q58,54 120,54 Q182,54 182,96 L182,160 Z" fill="#e8f5fc"/>'
     + fishy(70, 44, GOLD, .8) + fishy(150, 40, PINK, .8, True) + fishy(196, 80, '#8fd0b0', .7, True) + fishy(42, 100, '#f2a46b', .7)
     + fishy(110, 36, '#c792d6', .6)
     + f'<path d="M3,160 L237,160 {BOT}" fill="#cfe3ef"/>'
     + person(104, 128, RED, 1.0) + person(130, 132, GOLD, .85)
     + f'<path d="M98,124 l-6,-8" stroke-width="1.6"/>'
     + bubbles([(200, 40), (206, 54), (36, 60)]), bg=SEA)

# 2. 日本之森：瀑布、青苔和溪邊的水獺
card('forest', '手繪有瀑布和青苔的森林溪邊，石頭上坐著一隻水獺',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f4dc"/>'
     f'<path d="M3,70 Q40,40 80,56 Q120,30 160,52 Q200,34 237,60 L237,90 L3,90 Z" fill="{GREEN}"/>'
     f'<path d="M150,50 L150,130 L182,130 L182,48 Z" fill="#bfe3f5"/>'
     + ''.join(f'<path d="M{x},56 L{x},126" stroke="{WHITE}" stroke-width="2"/>' for x in (158, 166, 174))
     + f'<path d="M3,120 Q80,110 150,126 L237,124 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9fd0ec"/>'
     + f'<path d="M30,132 q20,-24 52,-4 q8,10 -4,14 L36,142 Q26,140 30,132 Z" fill="#b9b0a0"/>'
     + f'<path d="M36,128 q10,-8 20,-2" fill="none" stroke="{DGREEN}" stroke-width="3"/>'
     # 水獺
     + f'<path d="M52,126 q-6,-40 12,-44 q18,4 12,44 Z" fill="#a8774f"/>'
     + f'<ellipse cx="64" cy="112" rx="8" ry="10" fill="#f0d9b8" stroke="none"/>'
     + f'<ellipse cx="64" cy="84" rx="12" ry="10" fill="#a8774f"/>'
     + f'<circle cx="53" cy="78" r="2.4" fill="#a8774f"/><circle cx="75" cy="78" r="2.4" fill="#a8774f"/>'
     + f'<ellipse cx="64" cy="89" rx="7" ry="5" fill="#f0d9b8" stroke="none"/>'
     + face(64, 83, .7, False)
     + f'<ellipse cx="64" cy="88" rx="2.6" ry="1.8" fill="{INK}" stroke="none"/>'
     + f'<path d="M54,90 l-10,-2 M54,92 l-10,2 M74,90 l10,-2 M74,92 l10,2" stroke-width="1"/>'
     + f'<path d="M78,120 q20,4 26,-8" fill="none" stroke="#a8774f" stroke-width="6"/>'
     + ''.join(f'<path d="M{x},{y} q-8,-16 0,-26 q8,10 0,26" fill="{DGREEN}" stroke-width="1.4"/>' for x, y in [(110, 122), (126, 124), (206, 124)])
     + ''.join(f'<path d="M{x},{y} q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>' for x, y in [(120, 146), (190, 150), (70, 160)]),
     bg='#e6f4dc')

# 3. 太平洋大水槽：鯨鯊、鬼蝠魟、魚群
card('pacific', '手繪大水槽，有鯨鯊、鬼蝠魟和一群小魚',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{DEEP}"/>'
     + whaleshark(56, 70, 1.1) + ray(176, 118, .75)
     + ''.join(fishy(x, y, '#d8e6f2', .45, True) for x, y in [(60, 120), (74, 128), (66, 136), (82, 116), (90, 132), (50, 130)])
     + f'<path d="M3,156 Q60,148 120,156 T237,150 {BOT}" fill="#5f8fb8"/>'
     + ''.join(f'<path d="M{x},3 L{x-20},90" stroke="{WHITE}" stroke-width="6" opacity=".18"/>' for x in (60, 120, 190))
     + bubbles([(206, 40), (212, 26), (30, 40)]), bg=DEEP)

# 4. 南極大陸：企鵝
def penguin(x, y, s=1.0):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{14*s}" ry="{20*s}" fill="{NAVY}"/>'
            f'<ellipse cx="{x}" cy="{y+4*s}" rx="{9*s}" ry="{14*s}" fill="{WHITE}" stroke="none"/>'
            f'<ellipse cx="{x}" cy="{y-7*s}" rx="{8*s}" ry="{6*s}" fill="{WHITE}" stroke="none"/>'
            f'<path d="M{x-2.5*s},{y-4*s} l{2.5*s},{3*s} l{2.5*s},{-3*s} Z" fill="{GOLD}" stroke="none"/>'
            + face(x, y - 9 * s, .5 * s, False)
            + f'<path d="M{x-14*s},{y-2*s} q{-8*s},{8*s} {-4*s},{14*s}" fill="none" stroke-width="2"/>'
            f'<path d="M{x+14*s},{y-2*s} q{8*s},{8*s} {4*s},{14*s}" fill="none" stroke-width="2"/>'
            f'<path d="M{x-8*s},{y+20*s} l{6*s},0 M{x+2*s},{y+20*s} l{6*s},0" stroke="{GOLD}" stroke-width="3"/>')


card('penguin', '手繪冰上的企鵝，旁邊有雪',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e3f1fa"/>'
     f'<path d="M3,120 L60,96 L120,108 L180,90 L237,104 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{WHITE}"/>'
     f'<path d="M150,150 L237,140 L237,155 Q237,177 215,177 L150,177 Z" fill="#9fd0ec"/>'
     + penguin(70, 104, 1.1) + penguin(116, 116, .9) + penguin(176, 86, .8)
     + snow([(30, 30), (60, 50), (100, 24), (150, 40), (200, 26), (214, 60), (130, 60)], 2.6, '#bcd6ea')
     + sparkle(40, 70), bg='#e3f1fa')

# 5. 塔斯曼海：海豚
card('dolphin', '手繪在水裡游的兩隻海豚',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SEA}"/>'
     + ''.join(
         f'<g transform="translate({cx},{cy}) rotate({r}) scale({s})">'
         f'<path d="M-48,-2 q-14,-18 -26,-16 q8,10 8,17 q-8,6 -16,15 q16,2 36,-10 Z" fill="#a9c4dc"/>'
         f'<path d="M-6,-24 q6,-12 16,-14 q-4,8 -2,15 Z" fill="#a9c4dc"/>'
         f'<path d="M-52,0 q10,-27 52,-27 q34,0 48,14 q9,4 18,6 q-6,7 -20,7 q-20,13 -50,12 q-36,-2 -48,-12 Z" fill="#c3d8ea"/>'
         f'<path d="M-30,6 q30,10 62,2 q-14,10 -34,10 q-18,0 -28,-12 Z" fill="{WHITE}" stroke="none"/>'
         f'<circle cx="34" cy="-11" r="2.4" fill="{INK}" stroke="none"/>'
         f'<path d="M58,0 q-10,6 -22,0" fill="none" stroke-width="1.6"/>'
         f'<ellipse cx="30" cy="-3" rx="4" ry="2.2" fill="{PINK}" stroke="none" opacity=".8"/></g>'
         for cx, cy, r, s in [(110, 66, -8, .95), (140, 126, 6, .75)])
     + bubbles([(200, 50), (208, 36), (30, 120), (40, 106)])
     + f'<path d="M3,160 Q60,152 120,160 T237,154 {BOT}" fill="#f3e2c0"/>', bg=SEA)

# 6. 蒙特雷灣：海獅
card('sealion', '手繪岩石上的海獅，旁邊是海浪',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SEA}"/>'
     f'<path d="M3,120 Q60,110 120,118 T237,112 {BOT}" fill="#7fb6dc"/>'
     f'<path d="M40,140 Q50,96 100,92 Q160,90 176,140 Z" fill="#b9b0a0"/>'
     f'<path d="M150,140 Q170,110 210,118 Q226,130 220,146 Z" fill="#a39a88"/>'
     # 海獅
     + f'<path d="M70,104 Q76,60 110,56 Q126,58 124,74 Q118,96 128,104 Z" fill="#a8774f"/>'
     + f'<circle cx="112" cy="54" r="15" fill="#a8774f"/>'
     + f'<ellipse cx="124" cy="58" rx="9" ry="6" fill="#c89a72"/>'
     + face(114, 52, .7)
     + f'<path d="M128,104 q16,-2 22,6 q-12,2 -24,0 Z M72,104 q-14,-6 -22,2 q12,4 24,2 Z" fill="#8a5c3a"/>'
     + f'<path d="M126,60 l10,-2 M126,63 l10,2" stroke-width="1.2"/>'
     + ''.join(f'<path d="M{x},{y} q6,-4 12,0" fill="none" stroke="{WHITE}" stroke-width="1.8"/>' for x, y in [(20, 130), (190, 160), (60, 160)])
     + sparkle(40, 36) + star(200, 34, 7), bg=SEA)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ky-' + name, 120, 120, label, inner, bg='#fff3c4')


# 行李箱不能帶進館，先寄置物櫃
rem('r-luggage', '手繪提醒：行李箱放進置物櫃',
    f'<rect x="58" y="14" width="50" height="86" rx="4" fill="{GRAY}"/>'
    + ''.join(f'<rect x="62" y="{y}" width="42" height="24" rx="2" fill="{WHITE}" stroke-width="1.4"/><circle cx="96" cy="{y+12}" r="2" fill="{INK}" stroke="none"/>' for y in (18, 46, 74))
    + f'<rect x="12" y="52" width="34" height="46" rx="6" fill="{PINK}"/>'
    f'<path d="M22,52 L22,40 L36,40 L36,52" fill="none" stroke-width="2.4"/>'
    f'<circle cx="20" cy="102" r="4" fill="{INK}"/><circle cx="38" cy="102" r="4" fill="{INK}"/>'
    f'<path d="M30,26 L50,26 M44,20 L50,26 L44,32" stroke="{RED}" stroke-width="3" fill="none"/>'
    f'<path d="M8,108 L112,108" stroke-width="2"/>')

# 部分展區整修中
rem('r-closed', '手繪提醒：水槽前面掛著整修中的牌子',
    f'<rect x="14" y="16" width="92" height="64" rx="6" fill="{SEA}"/>'
    f'<path d="M14,80 L106,80" stroke-width="2"/>'
    f'<path d="M24,60 L96,36 M24,36 L96,60" stroke="#f2a46b" stroke-width="0"/>'
    f'<rect x="20" y="40" width="80" height="18" rx="2" fill="{GOLD}"/>'
    + ''.join(f'<path d="M{x},40 L{x+10},58" stroke="{INK}" stroke-width="4"/>' for x in (26, 44, 62, 80))
    + f'<path d="M30,58 L30,100 M90,58 L90,100" stroke-width="3"/>'
    f'<path d="M84,100 L96,100 M24,100 L36,100" stroke-width="3"/>'
    f'<path d="M98,92 L110,108 L86,108 Z" fill="#f2a46b"/>')

# 搭到大阪港站，跟著大摩天輪走
rem('r-wheel', '手繪提醒：地鐵站出口和遠處的大摩天輪',
    f'<circle cx="80" cy="44" r="30" fill="none" stroke-width="2.4"/>'
    + ''.join(f'<path d="M80,44 L{x},{y}" stroke-width="1.3"/>' for x, y in [(110, 44), (50, 44), (80, 14), (80, 74), (101, 23), (59, 65), (59, 23), (101, 65)])
    + ''.join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c}" stroke-width="1.3"/>' for x, y, c in [(110, 44, PINK), (50, 44, GOLD), (80, 14, SKY), (80, 74, GREEN), (101, 23, GOLD), (59, 65, PINK), (59, 23, GREEN), (101, 65, SKY)])
    + f'<path d="M80,44 L70,100 M80,44 L90,100" stroke-width="2.2"/>'
    f'<rect x="10" y="66" width="34" height="34" rx="4" fill="{RED}"/>'
    f'<path d="M18,78 L36,78 M18,86 L36,86" stroke="{WHITE}" stroke-width="2.4"/>'
    f'<path d="M48,94 L62,94 M56,88 L62,94 L56,100" stroke="{RED}" stroke-width="2.6" fill="none"/>'
    f'<path d="M6,104 L114,104" stroke-width="2"/>')

print(save(F, OUT), 'files')
