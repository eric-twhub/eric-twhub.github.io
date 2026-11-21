# 名古屋栄 burlesque 秀場頁（NAGOYA de SHOW! 與 BARLESQUE NAGOYA）的插圖與提醒卡（2026-11-21）。
# 參考兩家官網的文字畫成可愛版：兩家店、空中方塊特技、現場樂團、選日期看場次、表演時禁止拍照。
# 只畫一般舞台與 Q 版表演者，不畫任何真實成員或 logo。函式照抄 sp_osaka-burlesque.py。
# 輸出 illust/sp/nagoya-burlesque/*.svg。說明文字放在 illust/spots/nagoya-burlesque.json。
# 輸出 illust/sp/osaka-burlesque/*.svg。說明文字放在 illust/spots/osaka-burlesque.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'nagoya-burlesque')
W, H = 240, 180
F = {}
SPACE = '#2a1f3d'
STAGE = '#3a2c56'
BOT = 'L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z'


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ng-' + name, W, H, label, inner, bg=bg)


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






# 1. 兩家店：兩個小舞台並排
card('two', '手繪兩個並排的小舞台，左邊女孩拿麥克風，右邊女孩跳舞',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<path d="M3,132 L237,132 {BOT}" fill="#4a3a70"/>'
     + f'<rect x="14" y="26" width="100" height="106" rx="10" fill="{STAGE}"/>'
     + f'<rect x="126" y="26" width="100" height="106" rx="10" fill="{STAGE}"/>'
     + f'<path d="M14,26 L114,26 L114,40 Q64,52 14,40 Z" fill="#e05a4f"/><path d="M126,26 L226,26 L226,40 Q176,52 126,40 Z" fill="#8f6bd8"/>'
     + spot(40, 88, 40, 128, '#5b4a86') + spot(152, 200, 40, 128, '#5b4a86')
     + girl(64, 74, INK, '#ffd86b', .8, 'wave') + f'<circle cx="82" cy="78" r="4" fill="{WHITE}"/><path d="M82,82 L80,92" stroke-width="2"/>'
     + girl(176, 74, '#e8c35a', PINK, .8, 'up', True)
     + stars_bg([(120, 16, GOLD), (30, 150, WHITE), (210, 152, '#8ff0ff')]), bg=SPACE)

# 2. 空中方塊
card('cube', '手繪一個懸在半空的發光方框，女孩坐在方框裡',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + f'<path d="M120,8 L120,40" stroke="{WHITE}" stroke-width="2"/>'
     + f'<path d="M84,40 L156,40 L156,112 L84,112 Z" fill="none" stroke="#8ff0ff" stroke-width="5"/>'
     + f'<path d="M84,40 L100,28 L172,28 L156,40 M172,28 L172,100 L156,112" fill="none" stroke="#5fc9e0" stroke-width="4"/>'
     + girl(120, 70, INK, PINK, .7, 'up')
     + f'<path d="M3,150 L237,150 {BOT}" fill="#4a3a70"/>'
     + ''.join(f'<circle cx="{x}" cy="150" r="9" fill="#2a1f3d" stroke-width="1.5"/>' for x in (40, 70, 170, 200))
     + stars_bg([(30, 30, GOLD), (210, 40, WHITE), (60, 80, '#ff8fc8'), (196, 90, GOLD)]), bg=SPACE)

# 3. 現場樂團
card('band', '手繪一組爵士鼓和一把吉他，旁邊有音符',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fde9f3"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#f7d3e6"/>'
     + f'<ellipse cx="80" cy="118" rx="36" ry="22" fill="{RED}"/><ellipse cx="80" cy="110" rx="36" ry="10" fill="{WHITE}"/>'
     + f'<ellipse cx="40" cy="84" rx="18" ry="6" fill="{GOLD}"/><path d="M40,90 L40,140" stroke-width="2.5"/>'
     + f'<ellipse cx="124" cy="96" rx="16" ry="9" fill="{WHITE}"/><path d="M124,105 L124,140" stroke-width="2.5"/>'
     + f'<path d="M58,70 L92,100 M104,70 L80,98" stroke-width="3"/>'
     + f'<path d="M170,130 Q150,120 160,100 Q170,88 186,98 Q200,108 190,126 Q182,140 170,130 Z" fill="#c98a4b"/>'
     + f'<path d="M184,100 L212,40" stroke-width="5"/><rect x="206" y="28" width="12" height="16" rx="3" fill="{INK}"/>'
     + f'<circle cx="174" cy="114" r="5" fill="{INK}"/>'
     + f'<path d="M150,40 L150,62 M150,40 L162,36 L162,58" stroke-width="2.5"/><circle cx="146" cy="62" r="4" fill="{INK}"/><circle cx="158" cy="58" r="4" fill="{INK}"/>'
     + star(30, 30, 5, PINK) + star(120, 26, 5), bg='#fde9f3')

# 4. 選日期看場次
card('cal', '手繪一張月曆，有幾格打了叉表示休息，旁邊一個時鐘',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{CREAM}"/>'
     + f'<path d="M3,144 L237,144 {BOT}" fill="#f3e3c4"/>'
     + f'<rect x="22" y="30" width="124" height="108" rx="10" fill="{WHITE}"/>'
     + f'<rect x="22" y="30" width="124" height="22" rx="10" fill="#8f6bd8"/>'
     + ''.join(f'<rect x="{30+c*28}" y="{60+r*24}" width="22" height="18" rx="3" '
               f'fill="{"#ffd1dc" if (r, c) in ((0, 0), (2, 1)) else "#f3ecff"}" stroke-width="1"/>'
               for r in range(3) for c in range(4))
     + f'<path d="M34,63 L48,75 M48,63 L34,75 M62,111 L76,123 M76,111 L62,123" stroke="{RED}" stroke-width="2.5"/>'
     + f'<circle cx="186" cy="84" r="34" fill="{WHITE}" stroke-width="3"/>'
     + f'<path d="M186,84 L186,60 M186,84 L204,84" stroke-width="3"/><circle cx="186" cy="84" r="3" fill="{INK}"/>'
     + star(212, 30, 5, PINK) + star(160, 140, 4), bg=CREAM)

# 5. 表演時禁止拍照
card('nophoto', '手繪一支手機被畫上禁止符號，背景是舞台燈',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SPACE}"/>'
     + spot(30, 110, 8, 150, '#46518a') + spot(130, 210, 8, 150, '#46518a')
     + f'<rect x="92" y="44" width="56" height="96" rx="10" fill="{WHITE}"/>'
     + f'<rect x="98" y="54" width="44" height="70" rx="4" fill="#cfe8ff"/>'
     + f'<circle cx="120" cy="132" r="4" fill="{INK}"/>'
     + f'<circle cx="120" cy="92" r="54" fill="none" stroke="{RED}" stroke-width="8"/>'
     + f'<path d="M82,54 L158,130" stroke="{RED}" stroke-width="8"/>'
     + stars_bg([(30, 30, GOLD), (214, 150, WHITE)]), bg=SPACE)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ng-' + name, 120, 120, label, inner, bg='#fff3c4')


rem('r-week', '手繪提醒：日曆上寫著提早一週',
    f'<rect x="20" y="22" width="80" height="80" rx="8" fill="{WHITE}"/>'
    f'<rect x="20" y="22" width="80" height="20" rx="8" fill="#8f6bd8"/>'
    f'<text x="60" y="82" text-anchor="middle" font-size="30" font-weight="700" fill="{INK}" stroke="none">-7</text>'
    f'<path d="M38,14 L38,30 M82,14 L82,30" stroke-width="3"/>')

rem('r-sc', '手繪提醒：一張帳單寫加 20%',
    f'<rect x="30" y="18" width="60" height="84" rx="4" fill="{WHITE}"/>'
    f'<path d="M38,32 L82,32 M38,44 L82,44 M38,56 L70,56" stroke-width="2"/>'
    f'<rect x="36" y="70" width="48" height="20" rx="4" fill="{RED}"/>'
    f'<text x="60" y="85" text-anchor="middle" font-size="13" font-weight="700" fill="{WHITE}" stroke="none">+20%</text>')

print(save(F, OUT), 'files')
