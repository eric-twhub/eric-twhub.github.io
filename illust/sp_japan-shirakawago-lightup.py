# 白川鄉點燈頁的「荻町集落有什麼」插圖與提醒卡（2026-11-13）。
# 參考白川郷観光協会官網（shirakawa-go.gr.jp/highlights/、events/441、events/460）的介紹畫成可愛版，不描照片構圖。
# 輸出 illust/sp/japan-shirakawago-lightup/*.svg（240×180）。說明文字放在 illust/spots/japan-shirakawago-lightup.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-shirakawago-lightup')
W, H = 240, 180
SKYW = '#e3eef7'
NIGHT = '#2e3a63'
THATCH = '#d9b36c'
MILK = '#eef2f7'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sg-' + name, W, H, label, inner, bg=bg)


def flake(x, y, r=5, col=WHITE):
    return (f'<path d="M{x},{y-r} L{x},{y+r} M{x-r*.87:.1f},{y-r/2} L{x+r*.87:.1f},{y+r/2} '
            f'M{x-r*.87:.1f},{y+r/2} L{x+r*.87:.1f},{y-r/2}" stroke="{col}" stroke-width="1.6"/>')


def floor(y, col=WHITE):
    return (f'<path d="M3,{y} Q60,{y-10} 120,{y-2} T237,{y-4} L237,155 Q237,177 215,177 '
            f'L25,177 Q3,177 3,155 Z" fill="{col}"/>')


def gassho(x, base, w, h, win=GOLD, roof=THATCH, face_on=False):
    # 合掌造：很陡的三角茅草屋頂（屋頂積雪）＋深色木牆＋亮燈的窗
    top = base - h
    rb = base - h * .36
    t = (f'<rect x="{x - w*.4:.0f}" y="{rb:.0f}" width="{w*.8:.0f}" height="{base-rb:.0f}" fill="{DBROWN}"/>'
         f'<path d="M{x - w/2:.0f},{rb+2:.0f} L{x},{top} L{x + w/2:.0f},{rb+2:.0f} Z" fill="{roof}"/>'
         f'<path d="M{x - w*.32:.0f},{top + (rb-top)*.64:.0f} L{x},{top} L{x + w*.32:.0f},{top + (rb-top)*.64:.0f} '
         f'Q{x + w*.16:.0f},{top + (rb-top)*.52:.0f} {x},{top + (rb-top)*.6:.0f} '
         f'Q{x - w*.16:.0f},{top + (rb-top)*.52:.0f} {x - w*.32:.0f},{top + (rb-top)*.64:.0f} Z" fill="{WHITE}"/>'
         f'<rect x="{x - w*.09:.0f}" y="{top + (rb-top)*.72:.0f}" width="{w*.18:.0f}" height="{w*.11:.0f}" rx="1" fill="{win}" stroke-width="1.3"/>'
         f'<rect x="{x - w*.3:.0f}" y="{rb + (base-rb)*.25:.0f}" width="{w*.16:.0f}" height="{(base-rb)*.4:.0f}" rx="1.5" fill="{win}" stroke-width="1.3"/>'
         f'<rect x="{x + w*.14:.0f}" y="{rb + (base-rb)*.25:.0f}" width="{w*.16:.0f}" height="{(base-rb)*.4:.0f}" rx="1.5" fill="{win}" stroke-width="1.3"/>')
    if face_on:
        t += face(x, rb + (base - rb) * .55, .6)
    return t


def person(x, y, col=RED, s=1.0, hat=None):
    t = (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
         f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')
    if hat:
        t += f'<path d="M{x-6.5*s},{y-1*s} q{6.5*s},{-11*s} {13*s},0 Z" fill="{hat}" stroke-width="1.4"/>'
    return t


# 1. 合掌造：像兩手合掌的陡屋頂，撐得住又多又重的雪
card('gassho', '手繪雪中的合掌造房子，屋頂像兩隻手合起來',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M3,96 Q50,60 100,84 Q150,50 237,80 L237,120 L3,120 Z" fill="#c9d8e6" stroke-width="1.8"/>'
     + gassho(96, 146, 112, 124, face_on=True)
     + gassho(190, 146, 64, 74)
     + floor(146, WHITE)
     + flake(30, 30) + flake(170, 26) + flake(214, 50, 4) + star(40, 60, 5))

# 2. 點燈：從展望台往下看整片集落
card('lightup', '手繪晚上從高處往下看，雪地裡一整片亮著燈的合掌造',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{NIGHT}"/>'
     + f'<path d="M3,70 Q60,40 120,62 Q180,40 237,64 L237,100 L3,100 Z" fill="#3c4a78" stroke-width="1.8"/>'
     + f'<path d="M3,98 L237,98 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#dfe6f3"/>'
     + gassho(46, 132, 50, 52, roof='#c9a560') + gassho(110, 126, 56, 60, roof='#c9a560') + gassho(176, 134, 50, 52, roof='#c9a560')
     + gassho(80, 166, 44, 44, roof='#c9a560') + gassho(150, 168, 48, 46, roof='#c9a560') + gassho(214, 166, 36, 38, roof='#c9a560')
     + ''.join(f'<circle cx="{x}" cy="{y}" r="16" fill="{GOLD}" opacity=".18" stroke="none"/>' for x, y in [(46, 118), (110, 112), (176, 120), (80, 156), (150, 156)])
     + snow([(24, 20), (70, 30), (130, 16), (190, 28), (220, 12), (100, 46)], 2.2, WHITE)
     + f'<path d="M206,22 a10,10 0 1,0 12,14 a8,8 0 1,1 -12,-14 Z" fill="{GOLD}"/>')

# 3. 和田家與往展望台的步道
card('wada', '手繪一棟大合掌造，後面有一條往山上走的步道和指示牌',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<path d="M96,150 Q150,64 237,34 L237,150 Z" fill="#dbe7f1" stroke-width="1.8"/>'
     + f'<path d="M120,150 Q150,120 170,96 Q186,76 206,60 Q218,50 236,44" fill="none" stroke="#e9dcc8" stroke-width="12"/>'
     + gassho(76, 150, 118, 120, face_on=True)
     + floor(150, WHITE)
     + f'<path d="M188,136 L188,92" stroke-width="3"/>'
     + f'<path d="M172,92 L210,92 L218,100 L210,108 L172,108 Z" fill="{GOLD}"/>'
     + f'<path d="M180,100 L202,100" stroke-width="1.6"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="5" fill="{BROWN}" stroke-width="1.1" transform="rotate(40 {x} {y})"/>'
               for x, y in [(150, 132), (160, 124), (166, 112), (176, 106), (196, 76), (206, 66)])
     + flake(30, 30) + flake(150, 24, 4) + star(130, 40, 5))

# 4. 巴士總站旁邊的泡湯設施
card('onsen', '手繪雪中冒著熱氣的溫泉澡堂，旁邊有巴士站牌',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKYW}"/>'
     + f'<rect x="40" y="76" width="112" height="64" rx="3" fill="#f3e2c0"/>'
     + f'<path d="M28,80 L96,44 L164,80 Z" fill="#6c7a8c"/>'
     + f'<path d="M34,78 Q96,68 158,78" stroke="{WHITE}" stroke-width="5" fill="none"/>'
     + f'<rect x="84" y="96" width="24" height="44" rx="2" fill="{SKY}" stroke-width="1.4"/>'
     + f'<rect x="58" y="84" width="76" height="10" rx="2" fill="{RED}" stroke-width="1.4"/>'
     + f'<path d="M80,30 q-6,-8 0,-16 q6,-8 0,-16 M96,30 q-6,-8 0,-16 q6,-8 0,-16 M112,30 q-6,-8 0,-16 q6,-8 0,-16" '
       f'fill="none" stroke-width="1.8" opacity=".55"/>'
     + f'<path d="M86,58 q-4,6 0,10 q4,4 0,8 M96,56 q-4,6 0,10 q4,4 0,8 M106,58 q-4,6 0,10 q4,4 0,8" fill="none" stroke="{RED}" stroke-width="2.2"/>'
     + floor(140, WHITE)
     + f'<path d="M196,150 L196,90" stroke-width="3"/><circle cx="196" cy="86" r="14" fill="{GREEN}"/>'
     + f'<rect x="188" y="82" width="16" height="8" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="5" fill="{BROWN}" stroke-width="1.1" transform="rotate(-80 {x} {y})"/>'
               for x, y in [(180, 156), (166, 152), (152, 156)])
     + flake(30, 30) + flake(210, 30) + star(150, 30, 5))

# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('sg-' + name, 120, 120, label, inner, bg='#fff3c4')


# 入場票是掛脖子的票夾
rem('r-neck', '手繪提醒：掛在脖子上的入場票',
    f'<path d="M30,14 Q60,70 90,14" fill="none" stroke="{RED}" stroke-width="4"/>'
    f'<rect x="38" y="56" width="44" height="54" rx="6" fill="{WHITE}"/>'
    f'<rect x="44" y="64" width="32" height="20" rx="3" fill="{GOLD}" stroke-width="1.4"/>'
    f'<path d="M46,92 L74,92 M46,100 L66,100" stroke-width="2"/>'
    f'<circle cx="60" cy="58" r="3" fill="{GRAY}" stroke-width="1.4"/>')

# 展望台分三批，時間由工作人員指定
rem('r-turns', '手繪提醒：分三批輪流上展望台',
    f'<path d="M10,104 L54,40 L110,104 Z" fill="#c9d8e6"/>'
    f'<rect x="44" y="30" width="20" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" stroke-width="1.8"/><text x="{x}" y="{y+4}" font-size="11" '
              f'text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">{n}</text>'
              for x, y, c, n in [(26, 92, PINK, 1), (60, 92, SKY, 2), (94, 92, '#c8e6c9', 3)]))

# 往展望台的步道 15:45 截止
rem('r-trail', '手繪提醒：步道入口和時鐘',
    f'<path d="M10,104 Q50,90 70,60 Q84,40 110,26" fill="none" stroke="#e9dcc8" stroke-width="12"/>'
    f'<circle cx="40" cy="40" r="24" fill="{WHITE}"/>'
    f'<path d="M40,40 L22,40 M40,40 L51,45" stroke-width="3"/>'
    f'<path d="M86,104 L86,70" stroke-width="3"/><rect x="72" y="62" width="30" height="14" rx="3" fill="{RED}"/>'
    f'<path d="M80,69 L94,69" stroke="{WHITE}" stroke-width="2.4"/>')

print(save(F, OUT), 'files')
