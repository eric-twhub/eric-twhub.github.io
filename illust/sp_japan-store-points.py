# 店家集點頁（/japan-store-points/）的插圖與提醒卡（2026-11-13）。
# 內容依 shoppoints.json（各店規約、官方問答，查證於 2026-10-17）畫成可愛版；
# 不畫任何店家招牌、點數卡卡面、電子錢包的品牌圖案，卡片一律是無標誌的素色卡。
# 輸出 illust/sp/japan-store-points/*.svg，說明文字在 illust/spots/japan-store-points.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-store-points')
W, H = 240, 180
F = {}
FLOOR = '<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'


def card_(name, label, inner, bg=CREAM):
    F[name] = svg('spt-' + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg('spt-' + name, 120, 120, label, inner, bg='#fff3c4')


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


def padlock(x, y, s=1.0):
    return (f'<path d="M{x-9*s:.1f},{y} L{x-9*s:.1f},{y-8*s:.1f} q0,{-11*s:.1f} {9*s:.1f},{-11*s:.1f} q{9*s:.1f},0 {9*s:.1f},{11*s:.1f} L{x+9*s:.1f},{y}" fill="none" stroke-width="3.2"/>'
            f'<rect x="{x-14*s:.1f}" y="{y}" width="{28*s:.1f}" height="{22*s:.1f}" rx="{4*s:.1f}" fill="{GOLD}"/>'
            f'<circle cx="{x}" cy="{y+9*s:.1f}" r="{3*s:.1f}" fill="{INK}" stroke="none"/>'
            f'<path d="M{x},{y+10*s:.1f} L{x},{y+16*s:.1f}" stroke-width="2.4"/>')


def heart(cx, cy, s=1.0, col=PINK):
    return (f'<path d="M{cx},{cy+8*s:.1f} C{cx-14*s:.1f},{cy-2*s:.1f} {cx-8*s:.1f},{cy-14*s:.1f} {cx},{cy-6*s:.1f} '
            f'C{cx+8*s:.1f},{cy-14*s:.1f} {cx+14*s:.1f},{cy-2*s:.1f} {cx},{cy+8*s:.1f} Z" fill="{col}"/>')


def tag(x, y, w=70, h=40, col=GOLD):
    return (f'<path d="M{x},{y} L{x+w-16},{y} L{x+w},{y+h/2} L{x+w-16},{y+h} L{x},{y+h} Z" fill="{col}"/>'
            f'<circle cx="{x+w-14}" cy="{y+h/2}" r="3.4" fill="{WHITE}"/>')


def pointcard(x, y, w=60, h=38, col=SKY):
    # 無標誌的集點卡：上面幾顆星星
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{col}"/>'
            + ''.join(star(x + w * (i + 1) / 5, y + h * .42, w * .07, GOLD) for i in range(4))
            + f'<path d="M{x+6},{y+h*.78:.1f} L{x+w*.55:.1f},{y+h*.78:.1f}" stroke-width="1.4"/>')


# 1. 入境走自動閘門的話，當場請職員蓋章
card_('gate', '手繪入境審查台，旅客遞出護照，對話框裡是一個紅色印章',
      FLOOR
      + '<rect x="12" y="80" width="12" height="70" rx="3" fill="#cfd8e6"/>'
      + '<rect x="44" y="80" width="12" height="70" rx="3" fill="#cfd8e6"/>'
      + '<rect x="24" y="104" width="10" height="16" rx="2" fill="#dfeefa" stroke-width="1.4"/>'
      + '<rect x="34" y="104" width="10" height="16" rx="2" fill="#dfeefa" stroke-width="1.4"/>'
      + '<rect x="132" y="104" width="100" height="46" rx="3" fill="#c48a5c"/>'
      + kid(196, 84, NAVY, 1.2)
      + '<path d="M182,78 q14,-17 28,0 Z" fill="#34416e"/><path d="M180,78 L212,78" stroke-width="2.4"/>'
      + '<rect x="128" y="98" width="108" height="8" rx="3" fill="#9a6440"/>'
      + legs(92, 124, 1.4) + kid(92, 80, GREEN, 1.4)
      + '<path d="M104,106 L132,94" stroke-width="3"/>'
      + '<rect x="128" y="84" width="22" height="14" rx="2" fill="#34416e" transform="rotate(-10 139 91)"/>'
      + '<path d="M96,22 L150,22 Q160,22 160,32 L160,50 Q160,60 150,60 L118,60 L108,70 L110,60 L96,60 Q86,60 86,50 L86,32 Q86,22 96,22 Z" fill="#ffffff"/>'
      + '<circle cx="123" cy="41" r="11" fill="none" stroke="#e4625a" stroke-width="2.6"/>'
      + '<circle cx="123" cy="41" r="5" fill="none" stroke="#e4625a" stroke-width="1.6"/>'
      + sparkle(206, 36) + sparkle(30, 40))

# 2. 辦會員常卡在日本門號與日本地址
card_('signup', '手繪手機上的簡訊對話框和一張要填住址的表單，旁邊一個問號',
      phone(28, 34, 58, 104)
      + '<path d="M38,56 L74,56 Q78,56 78,60 L78,74 Q78,78 74,78 L48,78 L42,84 L43,78 L38,78 Q34,78 34,74 L34,60 Q34,56 38,56 Z" fill="#ffffff" stroke-width="1.6"/>'
      + ''.join(f'<circle cx="{46+i*9}" cy="67" r="2" fill="#5a3d2b" stroke="none"/>' for i in range(3))
      + '<rect x="40" y="94" width="34" height="10" rx="3" fill="#f6a5ad" stroke-width="1.4"/>'
      + '<rect x="108" y="30" width="88" height="118" rx="4" fill="#ffffff"/>'
      + ''.join(f'<path d="M116,{48+i*22} L132,{48+i*22}" stroke-width="1.6"/>'
                f'<rect x="138" y="{40+i*22}" width="50" height="14" rx="2" fill="#fff6e6" stroke-width="1.4"/>' for i in range(4))
      + '<path d="M150,124 q0,-10 8,-10 q8,0 8,10 q0,6 -8,14 q-8,-8 -8,-14 Z" fill="#e4625a" stroke-width="1.6"/>'
      + '<circle cx="158" cy="124" r="3" fill="#ffffff" stroke-width="1"/>'
      + qmark(214, 50, 1.4, RED)
      + sparkle(20, 24) + sparkle(220, 150))

# 3. 結帳時是兩條路：免稅，或店家的點數與會員價
card_('choose', '手繪岔路路標，一邊是護照，一邊是集點的星星，小人站在中間想',
      FLOOR
      + '<rect x="114" y="34" width="12" height="116" rx="3" fill="#9a6440"/>'
      + '<path d="M106,42 L40,42 L24,56 L40,70 L106,70 Z" fill="#6bb38a"/>'
      + passport(56, 44, 18, 24)
      + '<path d="M134,74 L200,74 L216,88 L200,102 L134,102 Z" fill="#f4c152"/>'
      + star(160, 88, 9, WHITE) + star(184, 88, 7, WHITE)
      + legs(78, 128, 1.2) + kid(78, 92, PINK, 1.3)
      + qmark(104, 96, .9)
      + sparkle(206, 36) + sparkle(30, 110))

# 4. 電子錢包的餘額帶不走
card_('wallet', '手繪硬幣掉進一張素色卡片，旁邊掛著一個鎖',
      coin(92, 34, 10) + coin(116, 26, 10) + coin(138, 38, 10)
      + arrow(116, 52, 116, 76, RED)
      + '<rect x="60" y="82" width="112" height="70" rx="8" fill="#f6a5ad"/>'
      + '<rect x="72" y="100" width="22" height="16" rx="3" fill="#f4c152" stroke-width="1.4"/>'
      + '<path d="M72,134 L140,134" stroke-width="1.6"/>'
      + face(142, 112, 1.1)
      + padlock(200, 104, 1.2)
      + '<path d="M172,110 L186,110" stroke-width="2" stroke-dasharray="3 3"/>'
      + sparkle(30, 40) + sparkle(210, 40))

# ---- 提醒卡的手繪小圖（120×120，黃底）----
rem('r-member', '手繪提醒：會員價的標籤，旁邊的護照打叉',
    tag(10, 30, 76, 44, GOLD)
    + heart(40, 54, 1.0)
    + passport(70, 64, 24, 32)
    + redx(96, 92, 11))

rem('r-expire', '手繪提醒：集點卡和沙漏',
    pointcard(10, 44, 62, 40, SKY)
    + hourglass(92, 62, .95))

rem('r-new', '手繪提醒：收據和集點的星星中間一個問號',
    receipt(14, 24, 40, 60, 5)
    + coin(88, 84, 14, 'star')
    + qmark(88, 42, 1.2, RED))

print(save(F, OUT), 'files')
