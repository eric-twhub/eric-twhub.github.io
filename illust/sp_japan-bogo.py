# 買一送一頁（/japan-bogo/）的「買一送一，送的到底是什麼」插圖與提醒卡（2026-11-13）。
# 內容依 bogo.json（KKday 方案描述，查證於 2026-11-09）的結構畫成可愛版：一組＝兩人份或兩張。
# 不畫平台、電信公司的標誌，不畫任何行程地點的角色；不寫價格。
# 輸出 illust/sp/japan-bogo/*.svg，說明文字在 illust/spots/japan-bogo.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-bogo')
W, H = 240, 180
F = {}
FLOOR = '<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'


def card_(name, label, inner, bg=CREAM):
    F[name] = svg('bg-' + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg('bg-' + name, 120, 120, label, inner, bg='#fff3c4')


# ---- 共用小零件（購物頁這批自己帶一份，不動 kit.py）----
SKIN = '#f9d9c0'
YEL = '#fff3c4'


def kid(x, y, col=RED, s=1.0, hair=DBROWN):
    # 正面的小人：身體、臉、瀏海
    return (f'<path d="M{x-9*s:.1f},{y+30*s:.1f} q0,{-18*s:.1f} {9*s:.1f},{-18*s:.1f} q{9*s:.1f},0 {9*s:.1f},{18*s:.1f} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{10*s:.1f}" fill="{SKIN}"/>'
            f'<path d="M{x-10*s:.1f},{y-1*s:.1f} q{1*s:.1f},{-11*s:.1f} {10*s:.1f},{-11*s:.1f} q{9*s:.1f},0 {10*s:.1f},{11*s:.1f} '
            f'q{-6*s:.1f},{-5*s:.1f} {-10*s:.1f},{-4*s:.1f} q{-5*s:.1f},{-1*s:.1f} {-10*s:.1f},{4*s:.1f} Z" fill="{hair}"/>'
            + face(x, y + 2.5 * s, .55 * s))


def passport(x, y, w=26, h=34, col=NAVY):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
            f'<circle cx="{x+w/2:.1f}" cy="{y+h*.42:.1f}" r="{w*.2:.1f}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
            f'<path d="M{x+w*.28:.1f},{y+h*.78:.1f} L{x+w*.72:.1f},{y+h*.78:.1f}" stroke="{GOLD}" stroke-width="1.6"/>')


def phone(x, y, w=40, h=70, screen=SKY):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{NAVY}"/>'
            f'<rect x="{x+4}" y="{y+8}" width="{w-8}" height="{h-16}" rx="3" fill="{screen}" stroke-width="1.4"/>'
            f'<path d="M{x+w/2-5},{y+4.5} L{x+w/2+5},{y+4.5}" stroke="{GRAY}" stroke-width="1.6"/>')


def qr(x, y, sz=24):
    u = sz / 7
    t = f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{WHITE}" stroke-width="1.2"/>'
    for cx, cy in [(0, 0), (4, 0), (0, 4)]:
        t += (f'<rect x="{x+cx*u+u*.3:.1f}" y="{y+cy*u+u*.3:.1f}" width="{u*2.4:.1f}" height="{u*2.4:.1f}" '
              f'fill="none" stroke-width="1.3"/>'
              f'<rect x="{x+cx*u+u*1.1:.1f}" y="{y+cy*u+u*1.1:.1f}" width="{u*.9:.1f}" height="{u*.9:.1f}" fill="{INK}" stroke="none"/>')
    for cx, cy in [(4, 4), (5.5, 4.2), (4.6, 5.6), (6, 6), (3.2, 5.8), (5.8, 3.0), (3.4, 3.4)]:
        t += f'<rect x="{x+cx*u:.1f}" y="{y+cy*u:.1f}" width="{u*.8:.1f}" height="{u*.8:.1f}" fill="{INK}" stroke="none"/>'
    return t


def suitcase(x, y, w=40, h=50, col=PINK):
    return (f'<path d="M{x+w*.32:.1f},{y} L{x+w*.32:.1f},{y-9} L{x+w*.68:.1f},{y-9} L{x+w*.68:.1f},{y}" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}"/>'
            f'<path d="M{x+w*.3:.1f},{y+5} L{x+w*.3:.1f},{y+h-5} M{x+w*.7:.1f},{y+5} L{x+w*.7:.1f},{y+h-5}" stroke-width="1.4"/>'
            f'<circle cx="{x+w*.2:.1f}" cy="{y+h+3}" r="3" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+w*.8:.1f}" cy="{y+h+3}" r="3" fill="{INK}" stroke="none"/>')


def bag(x, y, w=30, h=32, col=GOLD):
    return (f'<path d="M{x+w*.3:.1f},{y+2} q0,-12 {w*.2:.1f},-12 q{w*.2:.1f},0 {w*.2:.1f},12" fill="none" stroke-width="2"/>'
            f'<path d="M{x},{y} L{x+w},{y} L{x+w-3},{y+h} L{x+3},{y+h} Z" fill="{col}"/>')


def coin(x, y, r=9, mark=''):
    t = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}"/>'
         f'<circle cx="{x}" cy="{y}" r="{r*.65:.1f}" fill="none" stroke-width="1.2" opacity=".7"/>')
    if mark == 'star':
        t += star(x, y, r * .5, WHITE)
    return t


def card(x, y, w=50, h=32, col=SKY):
    # 沒有任何品牌的卡片
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{col}"/>'
            f'<rect x="{x+6}" y="{y+h*.3:.1f}" width="{w*.2:.1f}" height="{h*.26:.1f}" rx="2" fill="{GOLD}" stroke-width="1.2"/>'
            f'<path d="M{x+6},{y+h*.78:.1f} L{x+w*.6:.1f},{y+h*.78:.1f}" stroke-width="1.4"/>')


def receipt(x, y, w=34, h=46, lines=4):
    zz = ''.join(f' L{x+w-(i+1)*w/8:.1f},{y+h+(4 if i % 2 == 0 else 0)}' for i in range(8))
    return (f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h}{zz} Z" fill="{WHITE}"/>'
            + ''.join(f'<path d="M{x+5},{y+8+i*8} L{x+w-(5 if i % 2 else 11)},{y+8+i*8}" stroke-width="1.3"/>' for i in range(lines)))


def ticket(x, y, w=60, h=30, col=GOLD):
    r = h * .18
    return (f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h/2-r:.1f} a{r:.1f},{r:.1f} 0 0 0 0,{2*r:.1f} L{x+w},{y+h} '
            f'L{x},{y+h} L{x},{y+h/2+r:.1f} a{r:.1f},{r:.1f} 0 0 0 0,{-2*r:.1f} Z" fill="{col}"/>'
            f'<path d="M{x+w*.7:.1f},{y+3} L{x+w*.7:.1f},{y+h-3}" stroke-width="1.3" stroke-dasharray="3 3"/>')


def redx(x, y, r=10):
    d = r * .45
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED}"/>'
            f'<path d="M{x-d:.1f},{y-d:.1f} L{x+d:.1f},{y+d:.1f} M{x+d:.1f},{y-d:.1f} L{x-d:.1f},{y+d:.1f}" stroke="{WHITE}" stroke-width="2.6"/>')


def okv(x, y, r=10):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN}"/>'
            f'<path d="M{x-r*.45:.1f},{y} L{x-r*.1:.1f},{y+r*.38:.1f} L{x+r*.5:.1f},{y-r*.35:.1f}" fill="none" stroke="{WHITE}" stroke-width="2.6"/>')


def nosign(x, y, r=20):
    d = r * .7
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{RED}" stroke-width="4"/>'
            f'<path d="M{x-d:.1f},{y-d:.1f} L{x+d:.1f},{y+d:.1f}" stroke="{RED}" stroke-width="4"/>')


def arrow(x1, y1, x2, y2, col=RED, w=3):
    import math as _m
    a = _m.atan2(y2 - y1, x2 - x1)
    l = 8
    p1 = (x2 - l * _m.cos(a - .5), y2 - l * _m.sin(a - .5))
    p2 = (x2 - l * _m.cos(a + .5), y2 - l * _m.sin(a + .5))
    return (f'<path d="M{x1},{y1} L{x2},{y2} M{p1[0]:.1f},{p1[1]:.1f} L{x2},{y2} L{p2[0]:.1f},{p2[1]:.1f}" '
            f'fill="none" stroke="{col}" stroke-width="{w}"/>')


def qmark(x, y, s=1.0, col=INK):
    return (f'<path d="M{x-6*s:.1f},{y-6*s:.1f} q0,{-8*s:.1f} {6*s:.1f},{-8*s:.1f} q{6*s:.1f},0 {6*s:.1f},{6*s:.1f} '
            f'q0,{5*s:.1f} {-6*s:.1f},{7*s:.1f} l0,{4*s:.1f}" fill="none" stroke="{col}" stroke-width="{3*s:.1f}"/>'
            f'<circle cx="{x}" cy="{y+10*s:.1f}" r="{2*s:.1f}" fill="{col}" stroke="none"/>')


def calendar(x, y, w=44, h=40, top=RED):
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{WHITE}"/>'
         f'<path d="M{x},{y+11} L{x},{y+4} q0,-4 4,-4 L{x+w-4},{y} q4,0 4,4 L{x+w},{y+11} Z" fill="{top}"/>'
         f'<path d="M{x+w*.3:.1f},{y-4} L{x+w*.3:.1f},{y+4} M{x+w*.7:.1f},{y-4} L{x+w*.7:.1f},{y+4}" stroke-width="2.4"/>')
    for i in range(3):
        for j in range(4):
            t += f'<circle cx="{x+w*(j+1)/5:.1f}" cy="{y+18+i*(h-22)/3:.1f}" r="1.6" fill="{INK}" stroke="none"/>'
    return t


def hourglass(x, y, s=1.0):
    return (f'<path d="M{x-14*s:.1f},{y-22*s:.1f} L{x+14*s:.1f},{y-22*s:.1f} M{x-14*s:.1f},{y+22*s:.1f} L{x+14*s:.1f},{y+22*s:.1f}" stroke-width="3"/>'
            f'<path d="M{x-11*s:.1f},{y-22*s:.1f} q0,{14*s:.1f} {11*s:.1f},{22*s:.1f} q{-11*s:.1f},{8*s:.1f} {-11*s:.1f},{22*s:.1f} '
            f'L{x+11*s:.1f},{y+22*s:.1f} q0,{-14*s:.1f} {-11*s:.1f},{-22*s:.1f} q{11*s:.1f},{-8*s:.1f} {11*s:.1f},{-22*s:.1f} Z" fill="{SKY}"/>'
            f'<path d="M{x-7*s:.1f},{y-12*s:.1f} q{7*s:.1f},{5*s:.1f} {14*s:.1f},0 q{-3*s:.1f},{8*s:.1f} {-7*s:.1f},{11*s:.1f} q{-4*s:.1f},{-3*s:.1f} {-7*s:.1f},{-11*s:.1f} Z" fill="{GOLD}" stroke-width="1.2"/>'
            f'<path d="M{x-9*s:.1f},{y+21*s:.1f} q{9*s:.1f},{-12*s:.1f} {18*s:.1f},0 Z" fill="{GOLD}" stroke-width="1.2"/>')


def legs(x, y, s=1.0):
    return f'<path d="M{x-4*s:.1f},{y} L{x-4*s:.1f},{y+16*s:.1f} M{x+4*s:.1f},{y} L{x+4*s:.1f},{y+16*s:.1f}" stroke-width="3"/>'


def sim(x, y, w=30, h=40, col=WHITE, rot=0):
    c = w * .28
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<path d="M{x},{y} L{x+w-c:.1f},{y} L{x+w},{y+c:.1f} L{x+w},{y+h} L{x},{y+h} Z" fill="{col}"/>'
            f'<rect x="{x+w*.22:.1f}" y="{y+h*.4:.1f}" width="{w*.56:.1f}" height="{h*.36:.1f}" rx="3" fill="{GOLD}" stroke-width="1.4"/>'
            f'<path d="M{x+w*.5:.1f},{y+h*.4:.1f} L{x+w*.5:.1f},{y+h*.76:.1f} M{x+w*.22:.1f},{y+h*.58:.1f} L{x+w*.78:.1f},{y+h*.58:.1f}" stroke-width="1.1"/>'
            '</g>')


def envelope(x, y, w=60, h=40, col=WHITE):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
            f'<path d="M{x},{y+2} L{x+w/2},{y+h*.55:.1f} L{x+w},{y+2}" fill="none" stroke-width="2"/>')


def bus(x, y, w=110, h=50):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{SKY}"/>'
            + ''.join(f'<rect x="{x+10+i*24}" y="{y+8}" width="18" height="16" rx="3" fill="{WHITE}" stroke-width="1.4"/>' for i in range(int((w-20)//24)))
            + f'<path d="M{x+4},{y+32} L{x+w-4},{y+32}" stroke="{RED}" stroke-width="3"/>'
            + f'<circle cx="{x+24}" cy="{y+h}" r="8" fill="{INK}"/><circle cx="{x+w-24}" cy="{y+h}" r="8" fill="{INK}"/>')


# 1. 行程：一組給兩個人同行
card_('pair', '手繪兩個小人一起拿著一張票，後面停著一台遊覽車',
      FLOOR
      + bus(118, 60, 110, 54)
      + legs(46, 124, 1.3) + kid(46, 80, PINK, 1.4)
      + legs(104, 124, 1.3) + kid(104, 80, GREEN, 1.4, hair=INK)
      + '<path d="M56,108 L64,108 M94,108 L86,108" stroke-width="3"/>'
      + ticket(56, 96, 40, 24, GOLD)
      + star(30, 30, 6) + sparkle(110, 30) + sparkle(216, 34))

# 2. 實體網卡：一組就是兩張，從台灣寄出
card_('sim', '手繪信封裡探出兩張 SIM 卡',
      '<rect x="40" y="70" width="140" height="84" rx="4" fill="#f6a5ad"/>'
      + sim(70, 32, 40, 54, WHITE, -12) + sim(116, 30, 40, 54, SKY, 10)
      + '<path d="M40,74 L110,120 L180,74 L180,154 L40,154 Z" fill="#f6a5ad"/>'
      + '<path d="M40,154 L110,110 L180,154" fill="none" stroke-width="2"/>'
      + face(110, 132, .9)
      + sparkle(30, 36) + sparkle(210, 40) + star(206, 140, 6))

# 3. eSIM：QR Code 用電子郵件寄
card_('esim', '手繪電子郵件信封飛向手機，手機畫面上是一個條碼',
      envelope(26, 50, 70, 46, WHITE)
      + '<path d="M104,74 Q124,58 138,74" fill="none" stroke-width="2" stroke-dasharray="4 4"/>'
      + arrow(128, 70, 140, 78, INK, 2.4)
      + phone(146, 28, 64, 120)
      + qr(158, 58, 40)
      + sparkle(30, 132) + star(80, 130, 6) + sparkle(222, 24))

# 4. 一個人去，第二份用不到
card_('solo', '手繪一個小人拿著兩張票，第二張是淡淡的、旁邊一個問號',
      FLOOR
      + legs(74, 124, 1.4) + kid(74, 78, RED, 1.5)
      + '<path d="M88,104 L108,94" stroke-width="3"/>'
      + ticket(102, 62, 50, 30, GOLD)
      + '<g opacity=".4">' + ticket(152, 80, 50, 30, GOLD) + '</g>'
      + qmark(206, 52, 1.2)
      + sparkle(30, 30) + sparkle(140, 140))

# ---- 提醒卡的手繪小圖（120×120，黃底）----
rem('r-same', '手繪提醒：兩個小人和一張只圈了一天的月曆',
    kid(26, 64, PINK, 1.0) + kid(52, 64, GREEN, 1.0, hair=INK)
    + calendar(68, 30, 42, 40)
    + '<circle cx="85" cy="52" r="6" fill="none" stroke="#e4625a" stroke-width="2.4"/>')

rem('r-eid', '手繪提醒：手機撥號畫面',
    phone(30, 12, 60, 98)
    + '<text x="60" y="40" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="13" '
      'font-weight="bold" fill="#5a3d2b" stroke="none">*#06#</text>'
    + ''.join(f'<circle cx="{46+i*14}" cy="{54+j*12}" r="4" fill="#ffffff" stroke-width="1.2"/>' for i in range(3) for j in range(4)))

rem('r-unit', '手繪提醒：兩張 SIM 卡和乘以二',
    sim(14, 36, 34, 46, WHITE, -8) + sim(44, 40, 34, 46, SKY, 8)
    + '<text x="98" y="72" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="24" '
      'font-weight="bold" fill="#e4625a" stroke="none">×2</text>')

print(save(F, OUT), 'files')
