# SHOW MUSEUM JOLIJO（札幌すすきの）頁的插圖與提醒卡（2026-11-21）。
# 參考官網（jolijo-sapporo.com）首頁與 SYSTEM 頁的文字畫成可愛版：地下大空間、大型 LED 螢幕、
# 無限暢飲、照時間計費。只畫一般舞台與 Q 版表演女孩，不畫任何真實成員或 logo。
# 函式照抄 sp_okinawa-churasun6.py（那支在 import 時就會輸出檔案，不能直接 import）。
# 輸出 illust/sp/sapporo-jolijo/*.svg。說明文字放在 illust/spots/sapporo-jolijo.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'sapporo-jolijo')
W, H = 240, 180
F = {}
SPACE = '#2a1f3d'
STAGE = '#3a2c56'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('jl-' + name, W, H, label, inner, bg=bg)


def girl(x, y, hair=DBROWN, dress=PINK, s=1.0, arms='up', bun=False):
    # Q 版表演女孩：大頭、蓬蓬裙、手舉起來；y 是頭的中心
    t = ''
    if arms == 'up':
        t += (f'<path d="M{x-8*s},{y+18*s} L{x-20*s},{y+4*s} M{x+8*s},{y+18*s} L{x+20*s},{y+4*s}" stroke-width="{2.6*s}"/>'
              f'<circle cx="{x-20*s}" cy="{y+4*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>'
              f'<circle cx="{x+20*s}" cy="{y+4*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>')
    elif arms == 'wave':
        t += (f'<path d="M{x-8*s},{y+18*s} L{x-18*s},{y+30*s} M{x+8*s},{y+18*s} L{x+22*s},{y+6*s}" stroke-width="{2.6*s}"/>'
              f'<circle cx="{x+22*s}" cy="{y+6*s}" r="{2.6*s}" fill="#f9d9c0" stroke-width="1.2"/>')
    t += (f'<path d="M{x-4*s},{y+40*s} L{x-5*s},{y+52*s} M{x+4*s},{y+40*s} L{x+5*s},{y+52*s}" stroke-width="{2.4*s}"/>'
          f'<ellipse cx="{x-6*s}" cy="{y+53*s}" rx="{4*s}" ry="{2*s}" fill="{dress}" stroke-width="1.2"/>'
          f'<ellipse cx="{x+6*s}" cy="{y+53*s}" rx="{4*s}" ry="{2*s}" fill="{dress}" stroke-width="1.2"/>'
          f'<path d="M{x-8*s},{y+14*s} L{x+8*s},{y+14*s} L{x+9*s},{y+26*s} L{x+20*s},{y+42*s} Q{x},{y+46*s} {x-20*s},{y+42*s} L{x-9*s},{y+26*s} Z" fill="{dress}"/>'
          f'<path d="M{x-18*s},{y+40*s} q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0 q{4*s},{-3*s} {8*s},0" fill="none" stroke="{WHITE}" stroke-width="1.4"/>')
    # 頭髮（後）＋臉＋瀏海
    t += f'<path d="M{x-14*s},{y+12*s} Q{x-16*s},{y-14*s} {x},{y-15*s} Q{x+16*s},{y-14*s} {x+14*s},{y+12*s} Z" fill="{hair}"/>'
    t += f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="#f9e0cc"/>'
    t += f'<path d="M{x-12*s},{y-2*s} Q{x-10*s},{y-14*s} {x},{y-13*s} Q{x+10*s},{y-14*s} {x+12*s},{y-2*s} Q{x+6*s},{y-8*s} {x},{y-6*s} Q{x-6*s},{y-8*s} {x-12*s},{y-2*s} Z" fill="{hair}"/>'
    if bun:
        t += f'<circle cx="{x-10*s}" cy="{y-13*s}" r="{5*s}" fill="{hair}"/><circle cx="{x+10*s}" cy="{y-13*s}" r="{5*s}" fill="{hair}"/>'
    t += face(x, y + 2 * s, .55 * s)
    t += star(x + 9 * s, y - 11 * s, 3.4 * s)
    return t


def spot(x1, x2, top=8, bottom=150, col='#46518a'):
    return f'<path d="M{(x1+x2)/2-6},{top} L{(x1+x2)/2+6},{top} L{x2},{bottom} L{x1},{bottom} Z" fill="{col}" stroke="none"/>'


def stars_bg(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{c}" stroke="none"/>' for x, y, c in pts)




# 1. 地下的大空間、大型 LED 螢幕
card('stage', '手繪地下表演廳，舞台後面是一整面發光的大螢幕，兩個可愛女孩在跳舞',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<rect x="30" y="16" width="180" height="70" rx="6" fill="#5b3f8f"/>'
     + ''.join(f'<rect x="{38+i*22}" y="24" width="18" height="54" rx="2" fill="{c}" stroke="none" opacity=".85"/>'
               for i, c in enumerate(['#ff8fc8', '#8ff0ff', GOLD, '#b6f5c8', '#ff8fc8', '#8ff0ff', GOLD, '#b6f5c8']))
     + spot(40, 110, 86, 140, '#4a3a70') + spot(130, 200, 86, 140, '#4a3a70')
     + f'<path d="M3,134 L237,134 {BOT}" fill="#4a3a70"/>'
     + f'<ellipse cx="120" cy="138" rx="86" ry="9" fill="#c9a6ff"/>'
     + girl(86, 84, INK, PINK, .9, 'up', True) + girl(154, 84, '#e8c35a', '#8ff0ff', .9, 'wave')
     + f'<path d="M14,20 L14,8 M226,20 L226,8" stroke-width="2"/>', bg=SPACE)

# 2. 飲料無限暢飲
card('drink', '手繪啤酒杯、調酒杯和果汁杯排在一起，旁邊寫著無限',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f3ecff"/>'
     + f'<path d="M3,138 L237,138 {BOT}" fill="#e2d6fa"/>'
     # 啤酒
     + f'<path d="M44,70 L48,136 L84,136 L88,70 Z" fill="{GOLD}"/>'
     + f'<path d="M42,70 Q48,56 60,62 Q68,52 78,60 Q90,56 90,70 Z" fill="{WHITE}"/>'
     + f'<path d="M88,84 q16,0 16,18 q0,18 -16,18" fill="none" stroke-width="3"/>'
     # 調酒
     + f'<path d="M112,70 L160,70 L136,104 Z" fill="#ff8fc8"/>'
     + f'<path d="M136,104 L136,132 M122,134 L150,134" stroke-width="3"/>'
     + f'<circle cx="152" cy="68" r="7" fill="#b6f5c8"/>'
     # 果汁
     + f'<rect x="176" y="80" width="34" height="56" rx="6" fill="#ffb36b"/>'
     + f'<path d="M198,80 L206,56" stroke-width="3"/>'
     + f'<text x="120" y="38" text-anchor="middle" font-size="22" font-weight="700" fill="{INK}" stroke="none">∞</text>'
     + star(40, 40, 6) + star(204, 36, 5, PINK), bg='#f3ecff')

# 3. 女孩的飲料另外算
card('cast', '手繪表演女孩拿著一杯飲料，旁邊有一枚日圓硬幣',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fde9f3"/>'
     + f'<path d="M3,140 L237,140 {BOT}" fill="#f7d3e6"/>'
     + girl(100, 66, '#e8c35a', PINK, 1.05, 'wave')
     + f'<path d="M126,64 L132,96 L150,96 L156,64 Z" fill="#ff8fc8"/>'
     + f'<path d="M150,60 L160,44" stroke-width="2.4"/>'
     + f'<circle cx="190" cy="118" r="20" fill="{GOLD}"/>'
     + f'<text x="190" y="126" text-anchor="middle" font-size="22" font-weight="700" fill="{INK}" stroke="none">¥</text>'
     + f'<path d="M178,72 q8,-10 18,-4" fill="none" stroke-width="1.6"/>'
     + star(40, 40, 6, PINK) + star(212, 40, 5), bg='#fde9f3')

# 4. 照時間計費
card('time', '手繪三個沙漏，分別標著 60、90、120',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + ''.join(
         f'<path d="M{x-18},40 L{x+18},40 L{x+4},84 L{x+18},128 L{x-18},128 L{x-4},84 Z" fill="#e8e0f7"/>'
         f'<path d="M{x-12},{120-h} L{x+12},{120-h} L{x+16},126 L{x-16},126 Z" fill="{GOLD}" stroke="none"/>'
         f'<path d="M{x-22},36 L{x+22},36 M{x-22},132 L{x+22},132" stroke-width="4"/>'
         f'<text x="{x}" y="158" text-anchor="middle" font-size="16" font-weight="700" fill="{WHITE}" stroke="none">{t}</text>'
         for x, h, t in [(56, 10, '60'), (120, 20, '90'), (184, 30, '120')])
     + stars_bg([(20, 20, WHITE), (220, 22, GOLD), (120, 18, '#8ff0ff')]), bg=SPACE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('jl-' + name, 120, 120, label, inner, bg='#fff3c4')


# 價目表另加 20% 服務費
rem('r-sc', '手繪提醒：帳單上多一行加 20%',
    f'<path d="M24,14 L96,14 L96,104 L88,98 L80,104 L72,98 L64,104 L56,98 L48,104 L40,98 L32,104 L24,98 Z" fill="{WHITE}"/>'
    f'<path d="M34,32 L86,32 M34,46 L74,46 M34,60 L80,60" stroke-width="2"/>'
    f'<rect x="30" y="70" width="60" height="18" rx="4" fill="{RED}"/>'
    f'<text x="60" y="84" text-anchor="middle" font-size="13" font-weight="700" fill="{WHITE}" stroke="none">+20%</text>')

# 週日公休
rem('r-sun', '手繪提醒：日曆上星期日那一格打叉',
    f'<rect x="14" y="20" width="92" height="84" rx="8" fill="{WHITE}"/>'
    f'<rect x="14" y="20" width="92" height="20" rx="8" fill="{PINK}"/>'
    + ''.join(f'<rect x="{20+c*12}" y="{48+r*16}" width="9" height="11" rx="2" fill="{RED if c == 0 else "#e8e0f7"}" stroke-width="1"/>'
              for r in range(3) for c in range(7))
    + f'<path d="M18,46 L32,96 M32,46 L18,96" stroke="{RED}" stroke-width="3"/>'
    f'<path d="M36,12 L36,28 M84,12 L84,28" stroke-width="3"/>')

print(save(F, OUT), 'files')
