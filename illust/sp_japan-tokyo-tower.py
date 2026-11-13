# 東京鐵塔頁的「上面有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網施設案內（tokyotower.co.jp/guidance/、/maindeck/、/plan/open_air_stair/）與
# Top Deck Tour 頁（tdt.tokyotower.co.jp/topdecktour/）的介紹畫成可愛版，不描照片構圖；
# 不畫官方吉祥物。輸出 illust/sp/japan-tokyo-tower/*.svg，說明文字在 illust/spots/japan-tokyo-tower.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-tokyo-tower')
W, H = 240, 180
ORANGE = '#ee7a3c'
SKYB = '#cfe8f7'
NIGHT = '#2f3a63'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('tt-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def back(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="{DBROWN}"/>')


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-12*s} {12*s},{-12*s} q{4*s},{-10*s} {16*s},{-6*s} '
            f'q{12*s},{-4*s} {16*s},{8*s} q{10*s},0 {8*s},{10*s} Z" fill="{col}" stroke-width="1.8"/>')


def tower(cx, base, top, col=ORANGE, band=WHITE, glow=False):
    # 東京鐵塔的剪影：四隻腳往上收窄，兩層展望台，白色橫帶
    h = base - top
    md = base - h * .45   # Main Deck
    td = base - h * .72   # Top Deck
    def hw(y):  # 該高度的半寬
        u = (base - y) / h
        return max(1.2, 46 * (1 - u) ** 2.2 + 1.5)
    pts_l = [f'{cx-hw(y):.1f},{y:.1f}' for y in [base - h * k / 20 for k in range(0, 21)]]
    pts_r = [f'{cx+hw(y):.1f},{y:.1f}' for y in [top + h * k / 20 for k in range(0, 21)]]
    arch = f'L{cx+hw(base)-14:.1f},{base} Q{cx},{base-h*.22:.1f} {cx-hw(base)+14:.1f},{base} '
    t = f'<path d="M{" L".join(pts_l)} L{" L".join(pts_r)} {arch}Z" fill="{col}"/>'
    for y0 in (base - h * .2, td - h * .1, td + h * .06):
        y1 = y0 + 6
        t += (f'<path d="M{cx-hw(y0)+.8:.1f},{y0:.1f} L{cx+hw(y0)-.8:.1f},{y0:.1f} '
              f'L{cx+hw(y1)-.8:.1f},{y1:.1f} L{cx-hw(y1)+.8:.1f},{y1:.1f} Z" fill="{band}" stroke-width="1.4"/>')
    w1 = hw(md) + 8
    t += f'<rect x="{cx-w1:.1f}" y="{md-7:.1f}" width="{2*w1:.1f}" height="14" rx="3" fill="{GOLD if glow else WHITE}"/>'
    w2 = hw(td) + 5
    t += f'<rect x="{cx-w2:.1f}" y="{td-5:.1f}" width="{2*w2:.1f}" height="10" rx="2" fill="{GOLD if glow else WHITE}"/>'
    return t


# 1. Main Deck：兩層的展望台，有咖啡廳和紀念品店
card('maindeck', '手繪東京鐵塔 Main Deck，窗邊有咖啡和紀念品袋，窗外是街景',
     f'<rect x="16" y="16" width="208" height="96" rx="8" fill="{SKYB}"/>'
     + ''.join(f'<rect x="{x}" y="{112-h}" width="{w}" height="{h}" rx="2" fill="{GRAY}" stroke-width="1.6"/>'
               for x, w, h in [(22, 16, 30), (40, 12, 44), (54, 20, 22), (78, 14, 36), (120, 18, 28), (140, 12, 48), (154, 22, 20), (178, 14, 34), (194, 22, 24)])
     + cloud(90, 44, .9) + cloud(170, 38, .7)
     + f'<path d="M120,16 L120,112" stroke-width="3"/>'
     + f'<path d="M3,112 L237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<rect x="24" y="122" width="96" height="8" rx="3" fill="{BROWN}"/><path d="M72,130 L72,170" stroke-width="3"/>'
     + mug(42, 100, .55, GOLD)
     + f'<path d="M150,128 L190,128 L194,168 L146,168 Z" fill="{PINK}"/>'
     + f'<path d="M160,128 q0,-14 10,-14 q10,0 10,14" fill="none" stroke-width="2.4"/>'
     + star(170, 148, 7)
     + kid(212, 132, GREEN, 1.0)
     + sparkle(40, 32, 4))

# 2. Main Deck 1 樓的玻璃地板：直接往下看 150 公尺
card('skywalk', '手繪從東京鐵塔玻璃地板往下看，鐵塔的鐵骨往下延伸，地面很遠',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e9dcc8"/>'
     + f'<rect x="54" y="30" width="132" height="120" rx="6" fill="{SKYB}"/>'
     + f'<rect x="104" y="80" width="32" height="22" rx="2" fill="#d7ecd0" stroke-width="1.6"/>'
     + ''.join(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{ORANGE}" stroke-width="5"/>'
               for x1, y1, x2, y2 in [(58, 34, 104, 80), (182, 34, 136, 80), (58, 146, 104, 102), (182, 146, 136, 102)])
     + ''.join(f'<path d="M{a},{b} L{c},{d}" stroke="{ORANGE}" stroke-width="2"/>'
               for a, b, c, d in [(70, 46, 170, 46), (82, 58, 158, 58), (70, 134, 170, 134), (82, 122, 158, 122)])
     + f'<rect x="54" y="30" width="132" height="120" rx="6" fill="none" stroke-width="2.6"/>'
     + f'<path d="M120,30 L120,150 M54,90 L186,90" stroke="{WHITE}" stroke-width="2" opacity=".8"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{DGREEN}" stroke="none"/>' for x, y in [(110, 86), (128, 94), (116, 97), (131, 85)])
     + ''.join(f'<path d="M{x-7},{170} q0,-22 7,-22 q7,0 7,22 Z" fill="{c}"/>' for x, c in [(104, RED), (122, RED), (146, PINK), (164, PINK)])
     + sparkle(120, 16, 5) + sparkle(30, 150, 4) + sparkle(210, 30, 4))

# 3. Top Deck：幾何形狀的鏡子和 LED 燈
tri = ''
for i in range(7):
    for j in range(3):
        x = 22 + i * 30 + (15 if j % 2 else 0)
        y = 18 + j * 22
        c = ['#c9b8f0', '#a9d4f5', '#f5c6e0'][(i + j) % 3]
        tri += f'<path d="M{x},{y} L{x+15},{y+22} L{x-15},{y+22} Z" fill="{c}" stroke-width="1.4"/>'
card('topdeck', '手繪 250 公尺的 Top Deck，天花板是一片片三角形鏡子和燈光，窗外是夜景',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + tri
     + f'<rect x="16" y="92" width="208" height="50" rx="6" fill="#43507f"/>'
     + ''.join(f'<rect x="{x}" y="{142-h}" width="{w}" height="{h}" rx="1" fill="#5b6894" stroke-width="1.4"/>'
               for x, w, h in [(22, 14, 20), (38, 10, 32), (52, 18, 14), (110, 12, 26), (124, 18, 16), (186, 14, 28), (202, 18, 18)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{GOLD}" stroke="none"/>'
               for x, y in [(28, 128), (42, 118), (58, 134), (114, 124), (130, 132), (190, 122), (208, 130), (44, 134)])
     + f'<path d="M3,142 L237,142 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#5a4a7a"/>'
     + back(84, 132, PINK, 1.1) + back(160, 134, SKY, 1.0)
     + sparkle(60, 86, 4) + sparkle(190, 84, 4), bg=NIGHT)

# 4. 外階梯：約 600 階從 Foot Town 屋頂走到 150 公尺
card('stairs', '手繪東京鐵塔腳下的之字形外階梯，小人正在往上爬',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYB}"/>'
     + cloud(20, 46, .9) + cloud(176, 40, 1.0)
     + tower(120, 150, 6)
     + f'<path d="M30,150 L210,150 L210,155 Q210,177 188,177 L52,177 Q30,177 30,155 Z" fill="{GRAY}"/>'
     + ''.join(f'<rect x="{x}" y="158" width="14" height="8" rx="2" fill="{WHITE}" stroke-width="1.4"/>' for x in (44, 70, 152, 178))
     + f'<path d="M100,148 L140,138 L102,128 L140,118 L104,108 L138,98" fill="none" stroke="{WHITE}" stroke-width="7"/>'
     + f'<path d="M100,148 L140,138 L102,128 L140,118 L104,108 L138,98" fill="none" stroke-width="1.4" stroke-dasharray="3 4"/>'
     + kid(122, 104, RED, .7)
     + f'<path d="M134,110 l7,-4 M134,116 l8,0" stroke-width="1.4"/>'
     + star(30, 22, 6) + sparkle(204, 90, 4) + sparkle(50, 100, 4))

# 5. 晚上的點燈
card('lightup', '手繪晚上點燈的東京鐵塔，旁邊有月亮和星星',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + f'<circle cx="190" cy="40" r="16" fill="#fff1b8"/>'
     + tower(120, 177, 14, '#f39a4a', '#ffd9a8', glow=True)
     + sparkle(84, 110, 5) + sparkle(158, 104, 5) + sparkle(96, 60, 4) + sparkle(146, 50, 4)
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{c}" stroke="none"/>' for x, y, c in [(40, 30, WHITE), (66, 56, GOLD), (30, 100, WHITE), (210, 110, GOLD), (176, 80, WHITE), (56, 140, GOLD)])
     + star(44, 64, 5) + star(200, 136, 5) + sparkle(160, 24, 4), bg=NIGHT)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('tt-' + name, 120, 120, label, inner, bg='#fff3c4')


# Top Deck 要在 150 公尺換電梯
rem('r-transfer', '手繪提醒：兩台電梯，中途要換一次',
    f'<rect x="14" y="58" width="34" height="48" rx="4" fill="{GRAY}"/><path d="M31,58 L31,106" stroke-width="1.6"/>'
    + f'<rect x="72" y="18" width="34" height="48" rx="4" fill="{GRAY}"/><path d="M89,18 L89,66" stroke-width="1.6"/>'
    + f'<path d="M34,50 Q44,26 64,36" fill="none" stroke="{RED}" stroke-width="3.4"/>'
    + f'<path d="M54,30 L64,36 L56,44" fill="none" stroke="{RED}" stroke-width="3.4"/>'
    + f'<rect x="72" y="84" width="34" height="14" rx="3" fill="{GOLD}"/>'
    + f'<text x="89" y="95" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">150m</text>')

# 外階梯：上去就沒有電梯可以換
rem('r-stairs', '手繪提醒：之字形樓梯和打叉的電梯',
    f'<path d="M14,104 L50,92 L18,80 L54,68 L22,56 L58,44" fill="none" stroke-width="3"/>'
    + kid(46, 26, GREEN, .6)
    + f'<rect x="70" y="50" width="36" height="50" rx="4" fill="{GRAY}"/><path d="M88,50 L88,100" stroke-width="1.6"/>'
    + f'<path d="M66,46 L110,104 M110,46 L66,104" stroke="{RED}" stroke-width="4"/>')

print(save(F, OUT), 'files')
