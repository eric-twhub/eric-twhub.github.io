# 北新地 Burlesque 大阪（バーレスク大阪）頁的插圖與提醒卡（2026-11-21）。
# 參考官網（burlesque-osaka.com）SYSTEM 頁的文字畫成可愛版：一晚三場、前一天訂比較便宜、
# 看兩場送發光棒、應援方案的照片卡。只畫一般舞台與 Q 版表演女孩，不畫任何真實成員或 logo。
# 函式照抄 sp_osaka-splash.py（那支在 import 時就會輸出檔案，不能直接 import）。
# 輸出 illust/sp/osaka-burlesque/*.svg。說明文字放在 illust/spots/osaka-burlesque.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'osaka-burlesque')
W, H = 240, 180
F = {}
SPACE = '#2a1f3d'
STAGE = '#3a2c56'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('bq-' + name, W, H, label, inner, bg=bg)


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






# 1. 舞台：紅色布幕＋兩個女孩
card('stage', '手繪紅色布幕的舞台，兩個可愛女孩在聚光燈下跳舞',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<path d="M3,10 Q60,40 40,132 L3,132 Z" fill="#c0392b"/><path d="M237,10 Q180,40 200,132 L237,132 Z" fill="#c0392b"/>'
     + f'<path d="M3,8 L237,8 L237,24 Q120,40 3,24 Z" fill="#e05a4f"/>'
     + spot(60, 120, 24, 136, '#5b4a86') + spot(120, 180, 24, 136, '#5b4a86')
     + f'<path d="M3,132 L237,132 {BOT}" fill="#4a3a70"/>'
     + f'<ellipse cx="120" cy="136" rx="90" ry="9" fill="#ffd1dc"/>'
     + girl(92, 78, INK, PINK, .9, 'up', True) + girl(150, 78, '#e8c35a', '#ffd86b', .9, 'wave')
     + stars_bg([(120, 50, WHITE), (60, 60, GOLD), (184, 56, '#8ff0ff')]), bg=SPACE)

# 2. 一晚三場
card('shows', '手繪三個小時鐘，分別標著第 1、2、3 場',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + ''.join(
         f'<circle cx="{x}" cy="78" r="30" fill="{WHITE}" stroke-width="3"/>'
         f'<path d="M{x},78 L{x},58 M{x},78 L{x+hx},{78+hy}" stroke-width="3"/>'
         f'<circle cx="{x}" cy="78" r="3" fill="{INK}"/>'
         f'<text x="{x}" y="138" text-anchor="middle" font-size="16" font-weight="700" fill="{WHITE}" stroke="none">第 {i} 場</text>'
         for i, (x, hx, hy) in enumerate([(52, 14, 4), (120, 16, 0), (188, 4, 14)], 1))
     + stars_bg([(20, 22, WHITE), (220, 24, GOLD), (120, 20, '#ff8fc8')]), bg=SPACE)

# 3. 前一天訂比較便宜
card('adv', '手繪月曆上前一天那格畫了勾，旁邊一張票寫著便宜',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fde9f3"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#f7d3e6"/>'
     + f'<rect x="26" y="34" width="110" height="100" rx="10" fill="{WHITE}"/>'
     + f'<rect x="26" y="34" width="110" height="22" rx="10" fill="{PINK}"/>'
     + ''.join(f'<rect x="{34+c*24}" y="{64+r*22}" width="18" height="16" rx="3" '
               f'fill="{"#b6f5c8" if (r, c) == (1, 1) else "#f3ecff"}" stroke-width="1"/>'
               for r in range(3) for c in range(4))
     + f'<path d="M60,94 l5,6 l10,-12" fill="none" stroke="{INK}" stroke-width="3"/>'
     + f'<path d="M150,60 L214,60 L214,78 Q206,84 214,90 L214,108 L150,108 L150,90 Q158,84 150,78 Z" fill="{GOLD}"/>'
     + f'<text x="182" y="90" text-anchor="middle" font-size="20" font-weight="700" fill="{RED}" stroke="none">¥</text>'
     + f'<path d="M168,122 L196,122 M182,114 L182,132" stroke="{RED}" stroke-width="0"/>'
     + f'<path d="M172,124 L182,134 L192,124" fill="none" stroke="{RED}" stroke-width="4"/>'
     + star(212, 30, 5) + star(30, 22, 5, PINK), bg='#fde9f3')

# 4. 發光棒與照片卡
card('glow', '手繪一支發光棒和一張女孩的照片卡',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#4a3a70"/>'
     + f'<rect x="40" y="40" width="22" height="96" rx="11" fill="#ff8fc8" transform="rotate(-14 51 88)"/>'
     + f'<rect x="44" y="110" width="14" height="30" rx="4" fill="{WHITE}" transform="rotate(-14 51 88)"/>'
     + f'<path d="M30,34 l-8,-8 M58,26 l2,-12 M74,36 l10,-6" stroke="#ff8fc8" stroke-width="3"/>'
     + f'<rect x="112" y="36" width="88" height="110" rx="8" fill="{WHITE}" transform="rotate(6 156 91)"/>'
     + f'<rect x="120" y="44" width="72" height="72" rx="4" fill="#ffe0ec" transform="rotate(6 156 91)"/>'
     + girl(158, 70, INK, PINK, .62, 'wave', True)
     + f'<path d="M126,132 L184,138" stroke-width="2"/>'
     + stars_bg([(220, 24, GOLD), (100, 20, WHITE)]), bg=SPACE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('bq-' + name, 120, 120, label, inner, bg='#fff3c4')


# 前一天訂
rem('r-adv', '手繪提醒：日曆撕下一頁，上面寫前一天',
    f'<rect x="20" y="22" width="80" height="80" rx="8" fill="{WHITE}"/>'
    f'<rect x="20" y="22" width="80" height="20" rx="8" fill="{PINK}"/>'
    f'<text x="60" y="80" text-anchor="middle" font-size="30" font-weight="700" fill="{INK}" stroke="none">-1</text>'
    f'<path d="M38,14 L38,30 M82,14 L82,30" stroke-width="3"/>')

# 第 3 場比較貴
rem('r-3rd', '手繪提醒：月亮旁邊一張帳單寫加 15%',
    f'<path d="M30,24 a24,24 0 1,0 30,34 a20,20 0 1,1 -30,-34 Z" fill="{GOLD}"/>'
    f'<rect x="58" y="52" width="48" height="52" rx="4" fill="{WHITE}"/>'
    f'<rect x="62" y="74" width="40" height="18" rx="4" fill="{RED}"/>'
    f'<text x="82" y="87" text-anchor="middle" font-size="12" font-weight="700" fill="{WHITE}" stroke="none">+15%</text>'
    f'<path d="M64,62 L100,62" stroke-width="2"/>')

print(save(F, OUT), 'files')
