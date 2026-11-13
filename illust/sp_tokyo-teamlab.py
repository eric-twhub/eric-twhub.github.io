# teamLab 頁的「兩館裡面有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網繁中作品介紹（teamlab.art/zh-hant/e/planets/、/e/borderless-azabudai/）畫成簡化的可愛版，
# 只畫作品的概念（水裡的錦鯉、蘭花、發光球、蛋形物、光蝴蝶），不描作品畫面、不畫 logo。
# 輸出 illust/sp/tokyo-teamlab/*.svg，說明文字在 illust/spots/tokyo-teamlab.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'tokyo-teamlab')
W, H = 240, 180
DARK = '#2b2f55'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('tl-' + name, W, H, label, inner, bg=bg)


def kid(x, y, col=RED, s=1.0):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{7*s}" fill="#f9d9c0"/>' + face(x, y + 1 * s, .55 * s))


def koi(x, y, col, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-14,0 Q-4,-8 10,-3 Q14,0 10,3 Q-4,8 -14,0 Z" fill="{col}" stroke-width="1.4"/>'
            f'<path d="M-14,0 L-22,-6 L-20,0 L-22,6 Z" fill="{col}" stroke-width="1.4"/>'
            f'<circle cx="6" cy="-1" r="1.2" fill="{INK}" stroke="none"/></g>')


def flower(x, y, col, r=5):
    t = ''.join(f'<circle cx="{x+r*.9*c:.1f}" cy="{y+r*.9*s:.1f}" r="{r*.55:.1f}" fill="{col}" stroke-width="1.1"/>'
                for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, -.7)][:5])
    return t + f'<circle cx="{x}" cy="{y}" r="{r*.4:.1f}" fill="{GOLD}" stroke-width="1"/>'


# 1. 錦鯉在水面游，碰到人變成花
card('koi', '手繪赤腳站在水裡的人，身邊有發光的錦鯉和散開的花',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{DARK}"/>'
     + f'<path d="M3,96 L237,96 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#3f5a8f"/>'
     + ''.join(f'<path d="M{x},{y} q8,-4 16,0" fill="none" stroke="#8fb6e8" stroke-width="1.4"/>' for x, y in [(20, 110), (60, 150), (180, 116), (200, 160), (110, 168)])
     + koi(50, 124, '#ff9a7a', 1.1, 10) + koi(186, 140, WHITE, 1.0, 190) + koi(140, 162, GOLD, .9, -8) + koi(60, 160, '#ffb3c7', .8, 200)
     + kid(112, 84, PINK, 1.3)
     + f'<path d="M104,112 L104,140 M120,112 L120,140" stroke-width="3"/>'
     + f'<path d="M86,124 Q112,118 138,124 L138,146 L86,146 Z" fill="#3f5a8f" opacity=".75" stroke="none"/>'
     + f'<ellipse cx="112" cy="124" rx="26" ry="5" fill="none" stroke="#8fb6e8" stroke-width="1.6"/>'
     + flower(150, 106, '#ffb3c7', 6) + flower(166, 92, '#fff1a8', 5) + flower(84, 104, '#ffd0e0', 5) + flower(176, 110, '#c9b8f0', 4)
     + sparkle(40, 40, 4) + sparkle(200, 36, 4) + star(150, 30, 5), bg=DARK)

# 2. 漂浮的花園：掛滿真的蘭花，人走到哪花就往上浮
orch = ''
for i, x in enumerate(range(16, 232, 14)):
    for j in range(3):
        y = 30 + j * 22 + (i % 2) * 8
        if 92 < x < 150 and y > 50:
            y -= 26  # 人站的地方花往上浮
        col = ['#f5b8d6', '#d9b8f0', WHITE][(i + j) % 3]
        orch += f'<path d="M{x},10 L{x},{y-6}" stroke="{GREEN}" stroke-width="1"/>' if j == 0 else ''
        orch += flower(x, y, col, 5.5)
card('orchids', '手繪天花板垂下滿滿的蘭花，人站的地方花往上浮讓出空間',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#3a2f55"/>'
     + orch
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#2a2240"/>'
     + kid(120, 116, SKY, 1.3)
     + f'<path d="M100,94 l-6,-6 M140,94 l6,-6" stroke="{WHITE}" stroke-width="1.6"/>'
     + sparkle(28, 130, 4) + sparkle(210, 130, 4), bg='#3a2f55')

# 3. 發光球的房間：撥開會變色、發出聲音
balls = ''
for x, y, r, c in [(30, 40, 16, '#ffb3c7'), (74, 30, 18, '#a9d4f5'), (128, 24, 14, '#fff1a8'), (176, 36, 18, '#c9b8f0'), (214, 64, 14, '#ffb3c7'),
                   (26, 92, 14, '#c9b8f0'), (58, 74, 12, '#fff1a8'), (196, 110, 16, '#a9d4f5'), (40, 138, 16, '#ffb3c7'), (210, 152, 12, '#fff1a8'),
                   (150, 70, 12, '#ffb3c7'), (88, 140, 12, '#a9d4f5')]:
    balls += f'<circle cx="{x}" cy="{y}" r="{r+5}" fill="{c}" opacity=".3" stroke="none"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke-width="1.8"/>'
card('spheres', '手繪擺滿發光球的房間，小孩用手推開一顆球，球在發光',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{DARK}"/>'
     + balls
     + f'<circle cx="152" cy="118" r="20" fill="{GOLD}" opacity=".35" stroke="none"/>'
     + f'<circle cx="152" cy="118" r="15" fill="{GOLD}" stroke-width="1.8"/>'
     + kid(118, 112, GREEN, 1.25)
     + f'<path d="M126,124 L138,118" stroke-width="3"/>'
     + ''.join(f'<path d="M{x},{y} q4,-4 8,0" fill="none" stroke="{WHITE}" stroke-width="1.6"/>' for x, y in [(172, 100), (178, 112), (172, 124)])
     + sparkle(120, 64, 4), bg=DARK)

# 4. 苔蘚庭園：蛋形物白天映出周圍，日落後發光
eggs = ''
for x, y, s, c, r in [(40, 130, 1.0, '#ffd8a8', 0), (84, 120, .8, '#c9f0d8', 0), (130, 134, 1.1, '#ffb3c7', -18), (178, 122, .85, '#c9e0ff', 0), (212, 136, .9, '#fff1a8', 0)]:
    eggs += (f'<g transform="translate({x},{y}) rotate({r})">'
             f'<ellipse cx="0" cy="-16" rx="{20*s+4}" ry="{26*s+4}" fill="{c}" opacity=".3" stroke="none"/>'
             f'<path d="M0,{-38*s} C{16*s},{-38*s} {18*s},{-8*s} {16*s},0 C{12*s},{8*s} {-12*s},{8*s} {-16*s},0 C{-18*s},{-8*s} {-16*s},{-38*s} 0,{-38*s} Z" fill="{c}"/></g>')
card('moss', '手繪傍晚苔蘚地上的一顆顆發光的蛋形物，其中一顆歪向一邊',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#4a4f86"/>'
     + f'<circle cx="196" cy="40" r="12" fill="#fff1b8"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{WHITE}" stroke="none"/>' for x, y in [(30, 28), (80, 40), (130, 22), (160, 56), (60, 70)])
     + f'<path d="M3,120 Q60,108 120,116 T237,112 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#5f9a6a"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{DGREEN}" stroke="none"/>' for x, y in [(20, 150), (64, 160), (110, 156), (156, 166), (200, 158), (226, 150)])
     + eggs
     + f'<path d="M150,108 q6,-4 10,2" fill="none" stroke="{WHITE}" stroke-width="1.6"/>'
     + star(110, 40, 5), bg='#4a4f86')

# 5. 麻布台：作品走出房間，光做的蝴蝶在館內飛
def bfly(x, y, c, s=1.0, r=0):
    return (f'<g transform="translate({x},{y}) rotate({r}) scale({s})">'
            f'<path d="M0,0 C-10,-14 -18,-6 -12,2 C-16,8 -8,12 0,2 Z" fill="{c}" stroke-width="1.2"/>'
            f'<path d="M0,0 C10,-14 18,-6 12,2 C16,8 8,12 0,2 Z" fill="{c}" stroke-width="1.2"/>'
            f'<path d="M0,-4 L0,6" stroke-width="1.6"/></g>')
card('butterflies', '手繪暗暗的走廊，光做的蝴蝶從一個房間門口飛出來，飛向另一邊',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{DARK}"/>'
     + f'<path d="M20,40 L70,40 L70,150 L20,150 Z" fill="#3d4378"/>'
     + f'<path d="M30,50 L60,50 L60,150 L30,150 Z" fill="#5a62a0"/>'
     + f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#20244a"/>'
     + ''.join(bfly(x, y, c, s, r) for x, y, c, s, r in [(52, 96, '#ffb3c7', .9, -10), (84, 80, '#fff1a8', 1.0, 10), (112, 60, '#a9d4f5', 1.1, -6), (140, 72, '#c9b8f0', .9, 14),
                                                          (164, 50, '#ffb3c7', 1.2, -12), (196, 70, '#fff1a8', 1.0, 8), (120, 100, '#c9f0d8', .8, 0), (180, 108, '#a9d4f5', .8, -10)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{GOLD}" stroke="none"/>' for x, y in [(70, 90), (98, 72), (126, 66), (152, 62), (186, 60)])
     + kid(200, 124, PINK, 1.1)
     + f'<path d="M190,110 l-6,-6 M210,110 l6,-6" stroke="{WHITE}" stroke-width="1.6"/>', bg=DARK)


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label, inner):
    F[name] = svg('tl-' + name, 120, 120, label, inner, bg='#fff3c4')


# 豊洲：鞋子和襪子都要脫
rem('r-barefoot', '手繪提醒：脫下的鞋子和襪子，旁邊是光腳丫',
    f'<path d="M14,70 L14,50 Q14,44 22,44 L34,44 L36,62 Q52,64 54,72 L54,78 L14,78 Z" fill="{RED}"/>'
    + f'<path d="M14,78 L54,78" stroke-width="3"/>'
    + f'<path d="M66,30 L80,30 L80,56 Q80,64 94,64 L98,64 Q104,64 104,72 Q104,78 96,78 L80,78 Q66,78 66,64 Z" fill="{WHITE}"/>'
    + f'<path d="M66,36 L80,36" stroke-width="1.6"/>'
    + f'<ellipse cx="44" cy="100" rx="12" ry="8" fill="#f9d9c0"/>'
    + ''.join(f'<circle cx="{x}" cy="90" r="2.6" fill="#f9d9c0" stroke-width="1.2"/>' for x in (36, 42, 48, 54))
    + f'<path d="M70,98 q6,-4 12,0 q6,4 12,0 M70,106 q6,-4 12,0 q6,4 12,0" fill="none" stroke="#5b86c5" stroke-width="2"/>')

# 麻布台：沿地下通道走，不要上地面
rem('r-underground', '手繪提醒：地下通道的箭頭，往上的路打叉',
    f'<path d="M6,40 L114,40" stroke="{GREEN}" stroke-width="4"/>'
    + f'<path d="M26,40 L26,14 M18,22 L26,12 L34,22" stroke="{GRAY}" stroke-width="4" fill="none"/>'
    + f'<path d="M14,10 L40,40 M40,10 L14,40" stroke="{RED}" stroke-width="3.4"/>'
    + f'<rect x="10" y="56" width="100" height="40" rx="6" fill="{GRAY}"/>'
    + f'<path d="M24,76 L92,76 M82,66 L94,76 L82,86" stroke="{RED}" stroke-width="4" fill="none"/>'
    + f'<text x="94" y="112" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">B1</text>')

print(save(F, OUT), 'files')
