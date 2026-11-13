# 晴空塔頁的「上面有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網フロアガイド（tokyo-skytree.jp/floor/）各樓層的介紹畫成可愛版，不描照片構圖；
# 不畫官方吉祥物。輸出 illust/sp/japan-skytree/*.svg，說明文字在 illust/spots/japan-skytree.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-skytree')
W, H = 240, 180
SKYB = '#cfe8f7'
GLASS = '#e6f4fb'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sk-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    # 背影的小人：頭＋頭髮＋三角身體
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{hair}"/>')


def kid(x, y, col=RED, s=1.0):
    # 正面的小人（有臉）
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def skyline(x0, base, items, col=GRAY):
    # items: (相對 x, 寬, 高)
    t = ''
    for dx, w, h in items:
        t += f'<rect x="{x0+dx}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{col}" stroke-width="1.6"/>'
        for wy in range(int(base - h + 6), int(base - 3), 8):
            t += f'<path d="M{x0+dx+3},{wy} L{x0+dx+w-3},{wy}" stroke-width="1" opacity=".45"/>'
    return t


# 1. 350 公尺天望甲板：整圈落地玻璃，往外看關東平原
city = [(0, 16, 22), (18, 12, 34), (32, 20, 16), (54, 14, 28), (70, 22, 12), (94, 12, 30),
        (108, 18, 20), (128, 14, 36), (144, 22, 14), (168, 14, 26), (184, 18, 18)]
card('deck', '手繪晴空塔 350 公尺天望甲板，大片玻璃窗外是東京街景',
     f'<rect x="16" y="16" width="208" height="120" rx="8" fill="{SKYB}"/>'
     + f'<path d="M16,96 q30,-10 60,-4 q50,8 90,-6 q30,-8 58,0 L224,128 Q224,136 216,136 L24,136 Q16,136 16,128 Z" fill="#d7ecd0" stroke-width="1.8"/>'
     + skyline(22, 132, city)
     + cloud(40, 44, .9) + cloud(150, 36, 1.0)
     + f'<path d="M85,16 L85,136 M155,16 L155,136" stroke-width="3"/>'
     + f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + person(70, 132, PINK, 1.1) + person(98, 136, SKY, .9) + person(176, 132, GOLD, 1.1)
     + sparkle(204, 30) + sparkle(120, 28, 4))

# 2. 340 樓的玻璃地板：腳下看得到鐵骨和街景
card('glassfloor', '手繪站在晴空塔玻璃地板上的人，腳下是鐵骨和很小的街道',
     f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<rect x="60" y="112" width="120" height="62" fill="{GLASS}"/>'
     + ''.join(f'<path d="M{60+i*20},174 L{90+i*10},112" stroke="{GRAY}" stroke-width="3"/>' for i in range(0, 7, 2))
     + f'<path d="M60,140 L180,140" stroke="{GRAY}" stroke-width="3"/>'
     + skyline(70, 172, [(0, 8, 10), (12, 6, 16), (22, 10, 8), (60, 8, 14), (72, 6, 9), (84, 10, 12)], '#f0e6d8')
     + f'<rect x="60" y="112" width="120" height="62" fill="none" stroke-width="2.4"/>'
     + kid(104, 70, RED, 1.3) + kid(140, 74, GREEN, 1.15)
     + f'<path d="M96,100 l-2,12 M112,100 l2,12 M134,102 l-2,10 M146,102 l2,10" stroke-width="2.6"/>'
     + f'<path d="M86,62 l-8,-6 M84,72 l-9,0 M156,62 l8,-6 M158,72 l9,0" stroke-width="1.6"/>'
     + sparkle(40, 40) + sparkle(200, 36) + star(120, 26, 6))

# 3. 天望回廊：玻璃管狀的斜坡從 445 繞到 450
card('galleria', '手繪晴空塔頂端的玻璃迴廊，繞著塔身往上走，旁邊是雲',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(26, 150, 1.2) + cloud(170, 160, 1.3) + cloud(180, 50, .8)
     + f'<path d="M106,8 L134,8 L138,177 L102,177 Z" fill="{WHITE}"/>'
     + ''.join(f'<path d="M{104+y*.02:.0f},{y} L{136-y*.02:.0f},{y+22} M{136-y*.02:.0f},{y} L{104+y*.02:.0f},{y+22}" stroke-width="1.1" opacity=".45"/>' for y in range(10, 170, 22))
     + f'<path d="M58,126 Q120,150 182,120 L182,100 Q120,128 58,104 Z" fill="{GLASS}"/>'
     + f'<path d="M58,92 Q120,114 182,86 L182,70 Q120,96 58,76 Z" fill="{GLASS}"/>'
     + f'<path d="M182,100 Q196,94 182,86 M58,104 Q44,98 58,92" fill="none" stroke-width="2.4"/>'
     + kid(84, 110, PINK, .7) + kid(152, 80, GOLD, .7)
     + f'<path d="M120,8 L120,0" stroke-width="2"/>'
     + sparkle(40, 34) + sparkle(204, 120, 4) + star(80, 28, 6))

# 4. 345 樓的郵筒：寄出去的信會蓋紀念章
card('post', '手繪雲上的紅色郵筒和蓋了紀念章的明信片',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(20, 160, 1.4) + cloud(150, 168, 1.5)
     + f'<rect x="58" y="52" width="58" height="96" rx="10" fill="{RED}"/>'
     + f'<path d="M54,56 Q87,30 120,56 Z" fill="{RED}"/>'
     + f'<rect x="70" y="66" width="34" height="6" rx="3" fill="{INK}"/>'
     + face(87, 96, 1.0)
     + f'<rect x="64" y="148" width="46" height="10" rx="3" fill="{DBROWN}"/>'
     + f'<g transform="rotate(-10 172 92)"><rect x="138" y="66" width="70" height="50" rx="4" fill="{WHITE}"/>'
     + f'<circle cx="190" cy="84" r="11" fill="none" stroke="{RED}" stroke-width="2"/>'
     + f'<path d="M146,80 L172,80 M146,90 L168,90 M146,100 L172,100" stroke-width="1.4" opacity=".6"/></g>'
     + sparkle(200, 30) + star(40, 30, 6) + sparkle(130, 26, 4))

# 5. 咖啡：350 樓站著喝、340 樓有座位
card('cafe', '手繪靠窗的咖啡杯，一邊是站立吧檯、一邊是有椅子的座位',
     f'<rect x="14" y="14" width="212" height="84" rx="8" fill="{SKYB}"/>'
     + skyline(20, 96, [(0, 14, 18), (16, 10, 28), (30, 18, 12), (110, 12, 24), (124, 18, 14), (146, 12, 30), (160, 20, 16), (182, 14, 22)])
     + cloud(70, 40, .8)
     + f'<path d="M120,14 L120,98" stroke-width="3"/>'
     # 左：高腳站立吧檯
     + f'<rect x="24" y="104" width="80" height="8" rx="3" fill="{BROWN}"/>'
     + f'<path d="M64,112 L64,166 M48,166 L80,166" stroke-width="3"/>'
     + mug(46, 84, .55, GOLD)
     # 右：桌子和椅子
     + f'<rect x="140" y="124" width="64" height="8" rx="3" fill="{BROWN}"/>'
     + f'<path d="M172,132 L172,166 M158,166 L186,166" stroke-width="3"/>'
     + f'<path d="M132,112 L132,166 M132,140 L150,140 L150,166 M214,112 L214,166 M214,140 L196,140 L196,166" stroke-width="3" fill="none"/>'
     + mug(160, 104, .55, PINK)
     + sparkle(200, 30, 4))

# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('sk-' + name, 120, 120, label, inner, bg='#fff3c4')


# 入口在 4 樓：一棟樓、往上的箭頭、4F 那層有門
rem('r-4f', '手繪提醒：往上到 4 樓的入口',
    f'<rect x="20" y="20" width="56" height="88" rx="4" fill="{GRAY}"/>'
    + ''.join(f'<path d="M20,{20+i*22} L76,{20+i*22}" stroke-width="1.4"/>' for i in range(1, 4))
    + f'<rect x="24" y="24" width="48" height="18" rx="2" fill="{GOLD}"/>'
    + f'<text x="48" y="38" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">4F</text>'
    + f'<rect x="40" y="90" width="16" height="18" rx="2" fill="{WHITE}"/>'
    + f'<path d="M94,96 L94,34 M84,44 L94,32 L104,44" stroke="{RED}" stroke-width="4" fill="none"/>')

# 回程電梯在 340 樓：樓梯往下＋向下的電梯
rem('r-down', '手繪提醒：往下走兩層再搭電梯',
    f'<path d="M14,34 L36,34 L36,54 L58,54 L58,74 L80,74" fill="none" stroke-width="3"/>'
    + f'<path d="M14,20 Q44,22 60,44" fill="none" stroke="{RED}" stroke-width="3.4"/><path d="M50,42 L60,46 L62,34" fill="none" stroke="{RED}" stroke-width="3.4"/>'
    + f'<rect x="70" y="56" width="38" height="50" rx="4" fill="{GRAY}"/>'
    + f'<path d="M89,56 L89,106" stroke-width="1.6"/>'
    + f'<path d="M80,30 L98,30 L89,44 Z" fill="{RED}" stroke="{RED}"/>')

print(save(F, OUT), 'files')
