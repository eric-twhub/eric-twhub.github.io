# 大阪櫻川 Splash（i スプラッシュ）頁的插圖與提醒卡（2026-11-21）。
# 參考官網（apollo-1bld.com/isplash-bf/official.html）的文字畫成可愛版：舞台秀、不限時間、
# 入場附 1 杯酒＋果汁喝到飽、營業日曆。只畫一般舞台與 Q 版表演女孩，不畫任何真實成員或 logo。
# 函式照抄 sp_sapporo-jolijo.py（那支在 import 時就會輸出檔案，不能直接 import）。
# 輸出 illust/sp/osaka-splash/*.svg。說明文字放在 illust/spots/osaka-splash.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'osaka-splash')
W, H = 240, 180
F = {}
SPACE = '#2a1f3d'
STAGE = '#3a2c56'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sp-' + name, W, H, label, inner, bg=bg)


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





# 1. 舞台秀
card('stage', '手繪舞台，彩色燈光與彩帶簾幕前面三個可愛女孩在跳舞',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + ''.join(f'<path d="M{20+i*10},12 L{20+i*10},120" stroke="{c}" stroke-width="3" opacity=".7"/>'
               for i, c in enumerate(['#8ff0ff', '#ff8fc8', GOLD] * 7))
     + spot(30, 90, 8, 136, '#5b4a86') + spot(150, 210, 8, 136, '#5b4a86')
     + f'<path d="M3,132 L237,132 {BOT}" fill="#4a3a70"/>'
     + f'<ellipse cx="120" cy="136" rx="96" ry="9" fill="#c9a6ff"/>'
     + girl(64, 78, INK, '#8ff0ff', .85, 'up') + girl(120, 70, '#e8c35a', PINK, .95, 'up', True)
     + girl(176, 78, DBROWN, '#b6f5c8', .85, 'wave')
     + stars_bg([(16, 20, WHITE), (224, 24, GOLD), (120, 16, '#8ff0ff')]), bg=SPACE)

# 2. 不限時間
card('time', '手繪時鐘，指針旁邊寫著無限的符號',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f3ecff"/>'
     + f'<path d="M3,140 L237,140 {BOT}" fill="#e2d6fa"/>'
     + f'<circle cx="120" cy="86" r="52" fill="{WHITE}" stroke-width="4"/>'
     + ''.join(f'<path d="M{120+44*math.sin(a*math.pi/6):.1f},{86-44*math.cos(a*math.pi/6):.1f} '
               f'L{120+38*math.sin(a*math.pi/6):.1f},{86-38*math.cos(a*math.pi/6):.1f}" stroke-width="2.4"/>'
               for a in range(12))
     + f'<path d="M120,86 L120,52 M120,86 L144,98" stroke-width="4"/>'
     + f'<circle cx="120" cy="86" r="4" fill="{INK}"/>'
     + f'<text x="200" y="50" text-anchor="middle" font-size="30" font-weight="700" fill="{PINK}" stroke="none">∞</text>'
     + f'<path d="M78,30 L70,20 M162,30 L170,20" stroke-width="3"/>'
     + star(34, 40, 6) + star(40, 120, 5, PINK), bg='#f3ecff')

# 3. 一杯酒＋果汁喝到飽
card('drink', '手繪一杯啤酒旁邊標著 1，果汁壺旁邊寫著無限',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fff6e3"/>'
     + f'<path d="M3,140 L237,140 {BOT}" fill="#fde7bd"/>'
     + f'<path d="M48,66 L52,136 L88,136 L92,66 Z" fill="{GOLD}"/>'
     + f'<path d="M46,66 Q52,52 64,58 Q72,48 82,56 Q94,52 94,66 Z" fill="{WHITE}"/>'
     + f'<path d="M92,80 q16,0 16,18 q0,18 -16,18" fill="none" stroke-width="3"/>'
     + f'<circle cx="70" cy="34" r="15" fill="{RED}"/>'
     + f'<text x="70" y="41" text-anchor="middle" font-size="19" font-weight="700" fill="{WHITE}" stroke="none">1</text>'
     + f'<path d="M146,72 L140,136 L196,136 L190,72 Z" fill="#ffb36b"/>'
     + f'<path d="M140,72 L196,72 L192,60 L144,60 Z" fill="{WHITE}"/>'
     + f'<path d="M190,82 q18,4 14,28 q-3,12 -12,14" fill="none" stroke-width="3"/>'
     + f'<circle cx="160" cy="104" r="7" fill="#ffd86b" stroke-width="1.4"/>'
     + f'<circle cx="176" cy="116" r="6" fill="#ffd86b" stroke-width="1.4"/>'
     + f'<text x="168" y="44" text-anchor="middle" font-size="28" font-weight="700" fill="{INK}" stroke="none">∞</text>'
     + star(212, 30, 5, PINK), bg='#fff6e3')

# 4. 營業日曆
card('cal', '手繪月曆，有開的日子畫圈、沒開的日子打叉',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<rect x="40" y="26" width="160" height="132" rx="10" fill="{WHITE}"/>'
     + f'<rect x="40" y="26" width="160" height="24" rx="10" fill="{PINK}"/>'
     + f'<path d="M70,18 L70,34 M170,18 L170,34" stroke-width="4"/>'
     + ''.join(
         (f'<circle cx="{56+c*21.5}" cy="{66+r*22}" r="7" fill="#bfe6ff" stroke-width="1.4"/>'
          if (r * 7 + c) % 7 not in (1, 4) or (r * 7 + c) == 4 else
          f'<path d="M{51+c*21.5},{61+r*22} l10,10 M{61+c*21.5},{61+r*22} l-10,10" stroke="{RED}" stroke-width="2.4"/>')
         for r in range(4) for c in range(7))
     + stars_bg([(18, 22, WHITE), (222, 26, GOLD), (220, 150, '#8ff0ff')]), bg=SPACE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('sp-' + name, 120, 120, label, inner, bg='#fff3c4')


# 不能拍照
rem('r-cam', '手繪提醒：相機上面畫一個大叉',
    f'<rect x="18" y="38" width="84" height="58" rx="10" fill="{WHITE}"/>'
    f'<rect x="44" y="28" width="30" height="14" rx="4" fill="{WHITE}"/>'
    f'<circle cx="60" cy="67" r="17" fill="#cfd8ff"/>'
    f'<circle cx="60" cy="67" r="8" fill="{INK}"/>'
    f'<path d="M16,18 L104,108 M104,18 L16,108" stroke="{RED}" stroke-width="6"/>')

# 日曆不是固定公休
rem('r-cal', '手繪提醒：日曆上不規則的幾格打叉',
    f'<rect x="14" y="20" width="92" height="84" rx="8" fill="{WHITE}"/>'
    f'<rect x="14" y="20" width="92" height="20" rx="8" fill="{PINK}"/>'
    + ''.join(f'<rect x="{20+c*12}" y="{48+r*16}" width="9" height="11" rx="2" '
              f'fill="{RED if (r, c) in ((0, 0), (1, 3), (2, 0), (1, 6)) else "#bfe6ff"}" stroke-width="1"/>'
              for r in range(3) for c in range(7))
    + f'<path d="M36,12 L36,28 M84,12 L84,28" stroke-width="3"/>')

print(save(F, OUT), 'files')
