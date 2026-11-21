# 淺草ロック座頁的插圖與提醒卡（2026-11-21）。
# 參考官網與台東區觀光網的文字畫成可愛版：圓形舞台、一景一景換主演、窗口現金買票、場內不能拿出手機。
# 只畫一般舞台、穿和服拿扇子的 Q 版舞者與物件，不畫任何真實表演者、不畫裸露。函式照抄 sp_osaka-burlesque.py。
# 輸出 illust/sp/tokyo-rockza/*.svg。說明文字放在 illust/spots/tokyo-rockza.json。
# 輸出 illust/sp/osaka-burlesque/*.svg。說明文字放在 illust/spots/osaka-burlesque.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-rockza')
W, H = 240, 180
F = {}
SPACE = '#2a1f3d'
STAGE = '#3a2c56'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('rz-' + name, W, H, label, inner, bg=bg)


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






# 1. 圓形舞台：伸出去的花道加圓台，舞者拿扇子
card('stage', '手繪劇場：紅色布幕前伸出一條花道，盡頭是圓形舞台，穿和服的女孩拿著扇子',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<path d="M3,8 L237,8 L237,22 Q120,36 3,22 Z" fill="#e05a4f"/>'
     + f'<path d="M3,10 Q40,30 30,90 L3,90 Z" fill="#c0392b"/><path d="M237,10 Q200,30 210,90 L237,90 Z" fill="#c0392b"/>'
     + f'<rect x="30" y="80" width="180" height="16" fill="#6b4f2a"/>'
     + f'<path d="M108,96 L132,96 L136,128 L104,128 Z" fill="#8a6a3c"/>'
     + f'<ellipse cx="120" cy="142" rx="44" ry="16" fill="#b8925a"/><ellipse cx="120" cy="138" rx="44" ry="14" fill="#d9b57a"/>'
     + spot(96, 144, 10, 140, '#5b4a86')
     + girl(120, 92, INK, '#e05a4f', .72, 'wave')
     + f'<path d="M134,96 L146,80 Q152,90 146,100 Z" fill="{GOLD}"/>'
     + stars_bg([(60, 50, GOLD), (184, 52, WHITE), (120, 30, '#ff8fc8')]), bg=SPACE)

# 2. 一景一景：七個小布幕
card('scenes', '手繪七個並排的小布幕，上面寫 1 到 7，代表七景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{CREAM}"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#f3e3c4"/>'
     + ''.join(f'<rect x="{12+i*31}" y="{50 + (i % 2) * 14}" width="26" height="60" rx="5" '
               f'fill="{["#e05a4f", "#8f6bd8", GOLD, PINK, "#5fc9e0", "#e05a4f", "#8f6bd8"][i]}"/>'
               f'<text x="{25+i*31}" y="{88 + (i % 2) * 14}" text-anchor="middle" font-size="16" font-weight="700" fill="{WHITE}" stroke="none">{i+1}</text>'
               for i in range(7))
     + f'<path d="M20,34 Q120,14 220,34" fill="none" stroke="{INK}" stroke-width="2"/>'
     + star(30, 140, 5, PINK) + star(210, 140, 5), bg=CREAM)

# 3. 窗口現金買票
card('ticket', '手繪一個售票窗口，前面有一張日圓紙鈔和一張票',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fde9f3"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#f7d3e6"/>'
     + f'<rect x="40" y="26" width="160" height="96" rx="10" fill="#c98a4b"/>'
     + f'<rect x="64" y="44" width="112" height="56" rx="28" fill="#fff3c4"/>'
     + f'<path d="M64,72 L176,72" stroke-width="2"/>'
     + f'<rect x="58" y="112" width="70" height="36" rx="4" fill="#b6f5c8"/>'
     + f'<text x="93" y="136" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}" stroke="none">¥</text>'
     + f'<path d="M140,112 L196,112 L196,124 Q190,130 196,136 L196,148 L140,148 L140,136 Q146,130 140,124 Z" fill="{GOLD}"/>'
     + star(28, 26, 5, PINK) + star(214, 24, 5), bg='#fde9f3')

# 4. 場內不能拿出手機
card('nophone', '手繪一支手機被畫上禁止符號，旁邊一台相機也被寄放在籃子裡',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<rect x="54" y="44" width="52" height="90" rx="10" fill="{WHITE}"/>'
     + f'<rect x="60" y="54" width="40" height="64" rx="4" fill="#cfe8ff"/>'
     + f'<circle cx="80" cy="88" r="46" fill="none" stroke="{RED}" stroke-width="7"/>'
     + f'<path d="M48,56 L112,120" stroke="{RED}" stroke-width="7"/>'
     + f'<path d="M140,104 L212,104 L204,148 L148,148 Z" fill="#c98a4b"/>'
     + f'<rect x="152" y="76" width="48" height="32" rx="6" fill="{INK}"/><circle cx="176" cy="92" r="10" fill="#8ff0ff"/>'
     + stars_bg([(30, 30, GOLD), (210, 30, WHITE)]), bg=SPACE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('rz-' + name, 120, 120, label, inner, bg='#fff3c4')


rem('r-cash', '手繪提醒：一張日圓紙鈔',
    f'<rect x="16" y="36" width="88" height="48" rx="6" fill="#b6f5c8"/>'
    f'<circle cx="60" cy="60" r="14" fill="{WHITE}"/>'
    f'<text x="60" y="66" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}" stroke="none">¥</text>')

rem('r-early', '手繪提醒：一個時鐘指著開演前半小時',
    f'<circle cx="60" cy="60" r="38" fill="{WHITE}" stroke-width="3"/>'
    f'<path d="M60,60 L60,30 M60,60 L60,90" stroke-width="3"/><circle cx="60" cy="60" r="3" fill="{INK}"/>'
    f'<text x="60" y="112" text-anchor="middle" font-size="12" font-weight="700" fill="{RED}" stroke="none">-30 分</text>')

print(save(F, OUT), 'files')
