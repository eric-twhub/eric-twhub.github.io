# 美麗海水族館頁的「館內有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網エリアガイド（churaumi.okinawa/area/）的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/churaumi/*.svg（240×180）。說明文字放在 illust/spots/okinawa-churaumi.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'churaumi')
W, H = 240, 180
SEA = '#bfe3f5'
DEEP = '#2f5d8a'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('cu-' + name, W, H, label, inner, bg=bg)


def whaleshark(x, y, s=1.0):
    # 藍底白點的鯨鯊，朝左
    t = (f'<path d="M{x},{y} q{30*s},{-26*s} {80*s},{-14*s} q{20*s},{4*s} {34*s},{-10*s} '
         f'l{-4*s},{20*s} l{6*s},{18*s} q{-16*s},{-10*s} {-36*s},{-6*s} q{-50*s},{10*s} {-80*s},{-8*s} Z" fill="#7fa9d6"/>'
         f'<path d="M{x+40*s},{y-18*s} l{8*s},{-14*s} l{8*s},{14*s}" fill="#7fa9d6"/>')
    for dx, dy in [(30, -8), (44, -12), (58, -6), (72, -12), (52, -2), (84, -6), (38, 0)]:
        t += f'<circle cx="{x+dx*s:.1f}" cy="{y+dy*s:.1f}" r="{1.8*s:.1f}" fill="{WHITE}" stroke="none"/>'
    t += f'<circle cx="{x+12*s:.1f}" cy="{y-6*s:.1f}" r="{1.8*s:.1f}" fill="{INK}" stroke="none"/>'
    t += f'<path d="M{x+4*s:.1f},{y+1*s:.1f} q{6*s:.1f},{3*s:.1f} {12*s:.1f},0" fill="none" stroke-width="1.6"/>'
    return t


def manta(x, y, s=1.0):
    return (f'<path d="M{x},{y} q{-30*s},{-6*s} {-40*s},{6*s} q{20*s},{0} {40*s},{10*s} q{20*s},{-10*s} {40*s},{-10*s} '
            f'q{-10*s},{-12*s} {-40*s},{-6*s} Z" fill="#5b6f8f"/>'
            f'<path d="M{x},{y+10*s} q{2*s},{12*s} {10*s},{20*s}" fill="none" stroke-width="1.6"/>'
            f'<circle cx="{x-6*s}" cy="{y+3*s}" r="{1.5*s}" fill="{WHITE}" stroke="none"/>'
            f'<circle cx="{x+6*s}" cy="{y+3*s}" r="{1.5*s}" fill="{WHITE}" stroke="none"/>')


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def fishy(x, y, col, s=1.0, left=False):
    d = -1 if left else 1
    return (f'<path d="M{x},{y} q{10*s*d},{-8*s} {20*s*d},0 q{-10*s*d},{8*s} {-20*s*d},0 Z" fill="{col}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} l{-7*s*d},{-6*s} l0,{12*s} Z" fill="{col}" stroke-width="1.4"/>'
            f'<circle cx="{x+14*s*d}" cy="{y-1}" r="1.3" fill="{INK}" stroke="none"/>')


# 1. 入口的鯨鯊雕像（官網推薦拍照點）
card('monument', '手繪美麗海水族館入口的鯨鯊雕像',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     f'<rect x="40" y="120" width="130" height="30" rx="4" fill="#d8cbb6"/>'
     + whaleshark(30, 98, 1.25)
     + person(200, 122, PINK) + person(220, 126, SKY)
     + f'<path d="M193,106 l-6,-8 M226,110 l6,-8" stroke-width="1.6"/>'
     + sparkle(40, 40) + sparkle(200, 36) + star(120, 30, 7))

# 2. 黑潮之海大水槽
card('kuroshio', '手繪黑潮之海大水槽，有鯨鯊、鬼蝠魟和看水槽的人',
     f'<rect x="18" y="18" width="204" height="118" rx="10" fill="{SEA}"/>'
     + whaleshark(60, 60, 1.05) + manta(160, 100, .8) + fishy(40, 110, GOLD, .7) + fishy(196, 46, PINK, .7, True)
     + fishy(110, 120, GOLD, .6, True)
     + f'<path d="M18,136 L222,136" stroke-width="2.4"/>'
     + person(70, 146, RED, .9) + person(96, 150, GREEN, .8) + person(160, 146, GOLD, .9)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke-width="1.3"/>' for x, y in [(200, 80), (206, 66), (30, 40)]), bg=CREAM)

# 3. 珊瑚之海（沒有屋頂，陽光直接照進來）
card('coral', '手繪珊瑚之海水槽，陽光照進來，有珊瑚和熱帯魚',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SEA}"/>'
     f'<circle cx="200" cy="36" r="16" fill="{GOLD}"/>'
     + ''.join(f'<path d="M200,36 L{x},{y}" stroke="{GOLD}" stroke-width="2" opacity=".7"/>' for x, y in [(150, 90), (170, 110), (120, 80)])
     + f'<path d="M3,150 Q60,138 120,148 T237,144 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#f3e2c0"/>'
     + f'<path d="M40,150 q-6,-24 4,-30 q6,10 2,16 q10,-14 16,-4 q-6,10 -10,18 Z" fill="{PINK}"/>'
     + f'<path d="M100,150 q0,-30 8,-34 q4,8 0,14 q8,-8 12,0 q-2,10 -6,20 Z" fill="#f2a46b"/>'
     + f'<path d="M170,150 q-10,-20 0,-28 q10,6 4,14 q12,-6 14,4 q-8,8 -10,10 Z" fill="#c792d6"/>'
     + fishy(60, 90, GOLD, .8) + fishy(140, 70, PINK, .8, True) + fishy(110, 110, '#8fd0b0', .7), bg=SEA)

# 4. 深海區：海的星象儀，會發光的魚
card('deepsea', '手繪深海區，黑暗中會發光的魚像星星一樣',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NAVY}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="none" opacity=".9"/>'
               for x, y, r, c in [(40, 40, 2.4, GOLD), (90, 30, 2, WHITE), (200, 50, 2.4, '#8ff0ff'), (170, 140, 2, GOLD), (30, 130, 2, '#8ff0ff')])
     + fishy(70, 80, '#8ff0ff', 1.1) + fishy(150, 110, GOLD, 1.0, True) + fishy(120, 60, '#b6f5c8', .8)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}" opacity=".35" stroke="none"/>' for x, y, c in [(84, 79, '#8ff0ff'), (136, 109, GOLD)])
     + f'<path d="M3,160 Q80,148 140,158 T237,152 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#283358"/>', bg=NAVY)

# 5. 歐奇劇場的海豚秀（在館外，免費）
card('dolphin', '手繪海豚秀，海豚從水面跳起來',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#dff0fd"/>'
     f'<path d="M3,120 q20,-8 40,0 t40,0 t40,0 t40,0 t40,0 t34,0 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#7fc4e8"/>'
     f'<g transform="translate(128,78) rotate(-24)">'
     f'<path d="M-48,-2 q-14,-18 -26,-16 q8,10 8,17 q-8,6 -16,15 q16,2 36,-10 Z" fill="#8fb0cc"/>'
     f'<path d="M-4,-24 q8,-18 22,-20 q-7,10 -5,21 Z" fill="#8fb0cc"/>'
     f'<path d="M-52,0 q10,-27 52,-27 q34,0 48,14 q9,4 18,6 q-6,7 -20,7 q-20,13 -50,12 q-36,-2 -48,-12 Z" fill="#a9c4dc"/>'
     f'<path d="M-30,6 q30,10 62,2 q-14,10 -34,10 q-18,0 -28,-12 Z" fill="{WHITE}" stroke="none"/>'
     f'<path d="M4,6 q-2,16 -16,20 q4,-10 2,-19 Z" fill="#8fb0cc"/>'
     f'<circle cx="34" cy="-11" r="2.4" fill="{INK}" stroke="none"/>'
     f'<path d="M50,0 q-8,4 -16,2" fill="none" stroke-width="1.5"/>'
     f'<ellipse cx="30" cy="-3" rx="4" ry="2.2" fill="{PINK}" stroke="none" opacity=".8"/>'
     f'</g>'
     f'<circle cx="196" cy="34" r="12" fill="{GOLD}"/><path d="M184,34 q12,6 24,0" fill="none" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{WHITE}" stroke-width="1.2"/>' for x, y in [(64, 118), (78, 106), (92, 116), (54, 104)])
     + sparkle(40, 40) + sparkle(200, 30) + f'<path d="M190,30 L230,30" stroke="{GOLD}" stroke-width="2" opacity=".0"/>', bg='#dff0fd')

# 6. 海龜館
card('turtle', '手繪在水裡游的海龜',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SEA}"/>'
     f'<ellipse cx="120" cy="92" rx="46" ry="32" fill="#8cc49a"/>'
     f'<path d="M96,80 l24,-14 l24,14 l-8,24 l-32,0 Z" fill="#6ba57a" stroke-width="1.6"/>'
     f'<ellipse cx="176" cy="84" rx="18" ry="14" fill="#a9d8b1"/>'
     + face(178, 82, .8)
     + f'<path d="M90,70 q-30,-20 -36,-6 q10,10 30,16 Z" fill="#a9d8b1"/>'
     f'<path d="M92,114 q-30,18 -30,4 q12,-10 30,-12 Z" fill="#a9d8b1"/>'
     f'<path d="M146,66 q22,-24 30,-14 q-8,12 -26,22 Z" fill="#a9d8b1"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke-width="1.3"/>' for x, y in [(200, 50), (206, 36), (40, 140)]), bg=SEA)

# ---- 提醒卡的手繪小圖（110×110 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('cu-' + name, 120, 120, label, inner, bg='#fff3c4')


# 入口：過海人門後搭手扶梯往下，3 樓右手邊
rem('r-entrance', '手繪提醒：搭手扶梯往下，入口在右手邊',
    f'<path d="M20,40 L60,40 L100,84 L100,96 L56,96 L16,52 Z" fill="{GRAY}"/>'
    + ''.join(f'<path d="M{24+8*i},{46+9*i} L{40+8*i},{46+9*i}" stroke-width="1.4"/>' for i in range(5))
    + f'<path d="M30,20 L30,34 M24,28 L30,34 L36,28" stroke="{RED}" stroke-width="3" fill="none"/>'
    + f'<path d="M74,104 L104,104 M96,96 L104,104 L96,112" stroke="{RED}" stroke-width="3" fill="none"/>'
    + f'<rect x="84" y="20" width="24" height="32" rx="3" fill="{SKY}"/><circle cx="102" cy="37" r="1.6" fill="{INK}" stroke="none"/>')

# 水槽上方參觀：1 樓專用電梯，兩個時段
rem('r-elevator', '手繪提醒：專用電梯和時鐘',
    f'<rect x="18" y="22" width="48" height="76" rx="4" fill="{GRAY}"/>'
    f'<path d="M42,22 L42,98" stroke-width="1.6"/>'
    f'<path d="M34,14 L42,6 L50,14" stroke="{RED}" stroke-width="3" fill="none"/>'
    f'<circle cx="88" cy="70" r="20" fill="{WHITE}"/><path d="M88,70 L88,58 M88,70 L97,74" stroke-width="2.4"/>')

# 巴士站走到入口約 10 分鐘
rem('r-bus', '手繪提醒：巴士站牌和走路的腳印',
    f'<path d="M30,100 L30,30" stroke-width="3"/><circle cx="30" cy="26" r="14" fill="{GREEN}"/>'
    f'<rect x="22" y="22" width="16" height="8" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
    + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="6" fill="{BROWN}" stroke-width="1.2" transform="rotate(20 {x} {y})"/>'
              for x, y in [(56, 96), (68, 84), (76, 96), (88, 82), (96, 94), (106, 80)]))

print(save(F, OUT), 'files')
