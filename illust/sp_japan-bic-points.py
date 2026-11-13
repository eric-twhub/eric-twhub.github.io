# Bic 點數頁（/japan-bic-points/）的「結帳台前先選一條路」插圖與提醒卡（2026-11-13）。
# 內容依 bic-points.json 引的點數卡利用規約（第４条、第５条、第７条）畫成可愛版；
# 不畫店家招牌、點數卡卡面或任何商品品牌，卡片一律是無標誌的素色卡。
# 輸出 illust/sp/japan-bic-points/*.svg，說明文字在 illust/spots/japan-bic-points.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-bic-points')
W, H = 240, 180
F = {}
FLOOR = '<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'


def card_(name, label, inner, bg=CREAM):
    F[name] = svg('bic-' + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg('bic-' + name, 120, 120, label, inner, bg='#fff3c4')


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


def pointcard(x, y, w=60, h=38, col=SKY):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{col}"/>'
            + ''.join(star(x + w * (i + 1) / 5, y + h * .42, w * .07, GOLD) for i in range(4))
            + f'<path d="M{x+6},{y+h*.78:.1f} L{x+w*.55:.1f},{y+h*.78:.1f}" stroke-width="1.4"/>')


def tag(x, y, w=70, h=40, col=GOLD):
    return (f'<path d="M{x},{y} L{x+w-16},{y} L{x+w},{y+h/2} L{x+w-16},{y+h} L{x},{y+h} Z" fill="{col}"/>'
            f'<circle cx="{x+w-14}" cy="{y+h/2}" r="3.4" fill="{WHITE}"/>')


def plus(x, y, r=7):
    return f'<path d="M{x-r},{y} L{x+r},{y} M{x},{y-r} L{x},{y+r}" stroke-width="3.2"/>'


# 1. 結帳前選一條路
card_('fork', '手繪岔路路標，一邊是護照和折價券，一邊是集點的星星',
      FLOOR
      + '<rect x="114" y="30" width="12" height="120" rx="3" fill="#9a6440"/>'
      + '<path d="M106,38 L36,38 L18,58 L36,78 L106,78 Z" fill="#6bb38a"/>'
      + passport(42, 44, 20, 28) + ticket(68, 48, 32, 20, PINK)
      + '<path d="M134,70 L204,70 L222,90 L204,110 L134,110 Z" fill="#f4c152"/>'
      + coin(156, 90, 11, 'star') + coin(184, 90, 11, 'star')
      + legs(66, 130, 1.1) + kid(66, 100, RED, 1.15)
      + sparkle(206, 34) + sparkle(30, 118))

# 2. 走免稅：可以搭折價券，沒有點數
card_('taxfree', '手繪護照加上折價券，旁邊的星星硬幣打叉',
      passport(28, 54, 46, 62)
      + plus(96, 86)
      + ticket(114, 64, 64, 42, PINK)
      + '<path d="M128,76 L156,76 M128,86 L150,86 M128,96 L144,96" stroke-width="1.4"/>'
      + coin(204, 84, 16, 'star') + redx(218, 100, 10)
      + sparkle(30, 30) + sparkle(200, 140) + star(60, 146, 6))

# 3. 走含稅：拿點數，不能用折價券
card_('taxed', '手繪星星硬幣掉進集點卡，旁邊的折價券打叉',
      coin(60, 36, 11, 'star') + coin(86, 28, 11, 'star') + coin(112, 38, 11, 'star')
      + arrow(86, 54, 86, 76, RED)
      + pointcard(34, 84, 104, 64, SKY)
      + face(110, 132, .8)
      + ticket(158, 70, 60, 36, PINK) + redx(214, 104, 11)
      + sparkle(206, 34) + sparkle(30, 150))

# 4. 有些商品整個不給點
card_('zero', '手繪商品吊牌上的星星被畫上禁止符號',
      tag(52, 54, 136, 76, GOLD)
      + '<path d="M174,92 Q196,60 214,30" fill="none" stroke-width="1.8"/>'
      + star(112, 92, 22, WHITE)
      + nosign(112, 92, 30)
      + sparkle(30, 36) + sparkle(40, 146) + sparkle(200, 150))

# 5. 兩年沒再用就失效
card_('expire', '手繪集點卡、月曆和沙漏',
      pointcard(24, 66, 84, 54, SKY)
      + calendar(126, 50, 50, 46)
      + calendar(140, 64, 50, 46)
      + hourglass(206, 92, .9)
      + sparkle(30, 36) + star(120, 146, 6) + sparkle(60, 150))

# 6. 談了現金折扣就沒有點數
card_('haggle', '手繪店員和客人握手，旁邊的星星硬幣打叉',
      FLOOR
      + legs(64, 124, 1.4) + kid(64, 78, GREEN, 1.4)
      + legs(146, 124, 1.4) + kid(146, 78, NAVY, 1.4)
      + '<path d="M76,108 L104,104 L134,108" stroke-width="3"/>'
      + '<circle cx="105" cy="104" r="6" fill="#f9d9c0"/>'
      + tag(70, 20, 64, 34, GOLD) + arrow(96, 26, 96, 48, RED)
      + coin(204, 70, 14, 'star') + redx(216, 84, 9)
      + sparkle(30, 34) + sparkle(170, 34))

# ---- 提醒卡的手繪小圖（120×120，黃底）----
rem('r-pay', '手繪提醒：卡片和硬幣中間一顆打問號的星星',
    card(10, 64, 48, 32, PINK)
    + coin(84, 72, 10) + coin(98, 84, 10) + coin(80, 92, 10)
    + star(30, 42, 9, GOLD) + star(90, 42, 9, GOLD) + qmark(60, 38, 1.1, RED))

rem('r-new', '手繪提醒：護照和星星硬幣中間一個問號',
    passport(12, 40, 32, 44)
    + coin(92, 64, 14, 'star')
    + qmark(60, 58, 1.1, RED)
    + sparkle(100, 22, 4))

print(save(F, OUT), 'files')
