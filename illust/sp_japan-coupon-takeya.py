# 多慶屋優惠券頁（/japan-coupon/takeya/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依 LIVE JAPAN 官方發券頁（livejapan.com/public/operation/coupon/takeya/zh-tw.html，2026/11/12 更新版）
# 與多慶屋官網（takeya.co.jp）的樓層與商品介紹畫成可愛版；招牌留白、不畫商標。
# 輸出 illust/sp/japan-coupon-takeya/*.svg，說明在 illust/spots/japan-coupon-takeya.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-takeya')
PFX = 'tk-'

W, H = 240, 180
F = {}
LAV = '#c9b8e8'
MINT = '#bfe8d6'
PEACH = '#f9d2b4'
TEAL = '#7cc7c2'
ORANGE = '#f2a46b'
BEIGE = '#e9dcc8'
YEL = '#fff3c4'
SKIN = '#f9d9c0'


def card(name, label, inner, bg=CREAM):
    F[name] = svg(PFX + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg(PFX + name, 120, 120, label, inner, bg=YEL)


def floor(y=150, col=BEIGE):
    # 卡片底部的地面，順著外框的圓角
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def awning(x, y, w, c1, c2, n=6, h=14):
    sw = w / n
    t = ''
    for i in range(n):
        c = c1 if i % 2 == 0 else c2
        t += (f'<path d="M{x+sw*i:.1f},{y} L{x+sw*(i+1):.1f},{y} L{x+sw*(i+1):.1f},{y+h} '
              f'q{-sw/2:.1f},{h*.8:.1f} {-sw:.1f},0 Z" fill="{c}" stroke-width="1.8"/>')
    return t


def shop(x, y, w, h, wall, a1, a2, sign, door=SKY, smile=True, icon=''):
    """空白招牌的可愛店面：招牌只畫臉或商品小圖示，不寫字。"""
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{wall}"/>'
         f'<rect x="{x+10}" y="{y+8}" width="{w-20}" height="24" rx="8" fill="{sign}"/>')
    if smile:
        t += face(x + w / 2, y + 18, .8)
    t += icon
    t += awning(x - 4, y + 38, w + 8, a1, a2, n=max(4, int(w // 26)))
    dw = min(34, w * .26)
    t += (f'<rect x="{x+w/2-dw/2:.1f}" y="{y+h-40}" width="{dw:.1f}" height="40" rx="3" fill="{door}"/>'
          f'<path d="M{x+w/2:.1f},{y+h-40} L{x+w/2:.1f},{y+h}" stroke-width="1.6"/>')
    return t


def win(x, y, w, h, col=SKY):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{col}"/>'


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    # 正面小人（有臉）
    return (f'<path d="M{x-8*s},{y+26*s} q0,{-16*s} {8*s},{-16*s} q{8*s},0 {8*s},{16*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{8*s}" fill="{SKIN}"/>'
            f'<path d="M{x-8*s},{y-1*s} q{1*s},{-9*s} {8*s},{-9*s} q{7*s},0 {8*s},{9*s} q{-8*s},{-4*s} {-16*s},0 Z" fill="{hair}" stroke-width="1.4"/>'
            + face(x, y + 1.5 * s, .5 * s))


def shelf(x, y, w, n=2, gap=34, col=BROWN):
    return ''.join(f'<rect x="{x}" y="{y+gap*i}" width="{w}" height="6" rx="2" fill="{col}"/>' for i in range(n))


def lipstick(x, y, col=RED, s=1.0):
    return (f'<path d="M{x+2*s},{y} L{x+2*s},{y-12*s} L{x+12*s},{y-18*s} L{x+12*s},{y} Z" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{14*s}" height="{8*s}" rx="1" fill="{GOLD}" stroke-width="1.6"/>'
            f'<rect x="{x-1*s}" y="{y+8*s}" width="{16*s}" height="{18*s}" rx="2" fill="{NAVY}" stroke-width="1.6"/>')


def jar(x, y, col=PINK, s=1.0, smile=True):
    return (f'<rect x="{x}" y="{y}" width="{30*s}" height="{10*s}" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
            f'<rect x="{x-2*s}" y="{y+9*s}" width="{34*s}" height="{20*s}" rx="{6*s}" fill="{col}" stroke-width="1.8"/>'
            + (face(x + 15 * s, y + 18 * s, .5 * s) if smile else ''))


def pump(x, y, col=MINT, s=1.0):
    # 按壓瓶（化妝水、洗髮精）
    return (f'<path d="M{x+8*s},{y-12*s} l{12*s},0" stroke-width="2.4"/>'
            f'<rect x="{x+6*s}" y="{y-12*s}" width="{6*s}" height="{14*s}" fill="{WHITE}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{18*s}" height="{40*s}" rx="{5*s}" fill="{col}" stroke-width="1.8"/>'
            f'<rect x="{x+3*s}" y="{y+12*s}" width="{12*s}" height="{14*s}" rx="2" fill="{WHITE}" stroke-width="1.2"/>')


def pillbox(x, y, w=34, h=26, col=WHITE, mark=RED):
    # 藥盒：只畫十字，不畫任何品牌
    return (f'<path d="M{x},{y} l8,-8 l{w},0 l-8,8 Z" fill="{GRAY}" stroke-width="1.6"/>'
            f'<path d="M{x+w},{y} l8,-8 l0,{h} l-8,8 Z" fill="{GRAY}" stroke-width="1.6"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x+w/2},{y+6} L{x+w/2},{y+h-6} M{x+w/2-7},{y+h/2} L{x+w/2+7},{y+h/2}" stroke="{mark}" stroke-width="3.2"/>')


def eyedrop(x, y, col=SKY, s=1.0):
    return (f'<path d="M{x+3*s},{y} L{x+5*s},{y-10*s} L{x+9*s},{y-10*s} L{x+11*s},{y} Z" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x}" y="{y}" width="{14*s}" height="{28*s}" rx="{5*s}" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x+3*s}" y="{y+8*s}" width="{8*s}" height="{10*s}" rx="1" fill="{WHITE}" stroke-width="1"/>')


def tube(x, y, col=MINT, s=1.0):
    return (f'<path d="M{x},{y} L{x+44*s},{y} L{x+50*s},{y+7*s} L{x+44*s},{y+14*s} L{x},{y+14*s} Z" fill="{col}" stroke-width="1.6"/>'
            f'<rect x="{x+50*s}" y="{y+3*s}" width="{8*s}" height="{8*s}" rx="1" fill="{WHITE}" stroke-width="1.4"/>'
            f'<path d="M{x+4*s},{y} L{x+4*s},{y+14*s}" stroke-width="1.2"/>')


def snack(x, y, col=GOLD, s=1.0, smile=True):
    # 零食袋：上下鋸齒封口
    w, h = 40 * s, 50 * s
    zz = ''.join(f'l{w/8:.1f},{(-3 if i % 2 == 0 else 3)*s:.1f} ' for i in range(8))
    zb = ''.join(f'l{-w/8:.1f},{(3 if i % 2 == 0 else -3)*s:.1f} ' for i in range(8))
    return (f'<path d="M{x},{y} {zz} q{4*s},{h/2:.1f} 0,{h:.1f} {zb} q{-4*s},{-h/2:.1f} 0,{-h:.1f} Z" fill="{col}" stroke-width="1.8"/>'
            f'<ellipse cx="{x+w/2:.1f}" cy="{y+h/2+2*s:.1f}" rx="{13*s:.1f}" ry="{11*s:.1f}" fill="{WHITE}" stroke-width="1.4"/>'
            + (face(x + w / 2, y + h / 2 + 1 * s, .55 * s) if smile else ''))


def phone(x, y, s=1.0, col=NAVY, screen=WHITE, coupon=True):
    # 手機畫面上是一張沒有字的券
    t = (f'<rect x="{x}" y="{y}" width="{40*s}" height="{70*s}" rx="{7*s}" fill="{col}"/>'
         f'<rect x="{x+4*s}" y="{y+8*s}" width="{32*s}" height="{54*s}" rx="2" fill="{screen}" stroke-width="1.4"/>')
    if coupon:
        t += ticket(x + 7 * s, y + 18 * s, .45 * s)
        t += ''.join(f'<path d="M{x+9*s:.1f},{y+(40+i*6)*s:.1f} L{x+31*s:.1f},{y+(40+i*6)*s:.1f}" stroke-width="1.4" opacity=".5"/>' for i in range(3))
    return t


def ticket(x, y, s=1.0, col=PINK):
    # 兩側有缺口的券，中間虛線，不寫字
    w, h = 58 * s, 30 * s
    r = 5 * s
    return (f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h/2-r} a{r},{r} 0 0 0 0,{2*r} L{x+w},{y+h} L{x},{y+h} '
            f'L{x},{y+h/2+r} a{r},{r} 0 0 0 0,{-2*r} Z" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+w*.68:.1f},{y+3*s:.1f} L{x+w*.68:.1f},{y+h-3*s:.1f}" stroke-width="1.4" stroke-dasharray="3 3"/>'
            + star(x + w * .34, y + h / 2, 7 * s, GOLD))


def passport(x, y, s=1.0, col='#3b5a8c'):
    # 護照：只畫一個圓，不畫任何國徽
    return (f'<rect x="{x}" y="{y}" width="{34*s}" height="{46*s}" rx="{4*s}" fill="{col}"/>'
            f'<circle cx="{x+17*s}" cy="{y+20*s}" r="{8*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+9*s},{y+36*s} L{x+25*s},{y+36*s}" stroke="{GOLD}" stroke-width="1.8"/>')


def receipt(x, y, s=1.0, n=4):
    w, h = 34 * s, (18 + n * 7) * s
    return (
            f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h} '
            + ''.join(f'L{x+w-w/6*(i+1):.1f},{y+h+(4 if i % 2 == 0 else 0)*s:.1f} ' for i in range(6))
            + f'Z" fill="{WHITE}" stroke-width="1.6"/>'
            + ''.join(f'<path d="M{x+6*s:.1f},{y+(10+i*7)*s:.1f} L{x+w-6*s:.1f},{y+(10+i*7)*s:.1f}" stroke-width="1.4" opacity=".55"/>' for i in range(n)))


def basket(x, y, s=1.0, col=RED):
    return (f'<path d="M{x+6*s},{y} q{24*s},{-26*s} {48*s},0" fill="none" stroke-width="3"/>'
            f'<path d="M{x},{y} L{x+60*s},{y} L{x+54*s},{y+30*s} L{x+6*s},{y+30*s} Z" fill="{col}"/>'
            + ''.join(f'<path d="M{x+(12+i*12)*s},{y+4*s} L{x+(12+i*12)*s},{y+26*s}" stroke-width="1.4" opacity=".6"/>' for i in range(4)))


def suitcase(x, y, s=1.0, col=ORANGE):
    return (f'<rect x="{x+12*s}" y="{y-10*s}" width="{16*s}" height="{12*s}" rx="3" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{40*s}" height="{54*s}" rx="{7*s}" fill="{col}"/>'
            f'<path d="M{x+13*s},{y+6*s} L{x+13*s},{y+48*s} M{x+27*s},{y+6*s} L{x+27*s},{y+48*s}" stroke-width="1.6"/>'
            f'<circle cx="{x+8*s}" cy="{y+58*s}" r="{3.5*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+32*s}" cy="{y+58*s}" r="{3.5*s}" fill="{INK}" stroke="none"/>')


def nope(x, y, r=14):
    # 紅色禁止圈
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{RED}" stroke-width="4"/>'
            f'<path d="M{x-r*.7:.1f},{y+r*.7:.1f} L{x+r*.7:.1f},{y-r*.7:.1f}" stroke="{RED}" stroke-width="4"/>')


def cross(x, y, r=10):
    return f'<path d="M{x-r},{y-r} L{x+r},{y+r} M{x+r},{y-r} L{x-r},{y+r}" stroke="{RED}" stroke-width="4.5"/>'


def ok(x, y, r=12):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN}"/>'
            f'<path d="M{x-r*.45:.1f},{y} L{x-r*.1:.1f},{y+r*.4:.1f} L{x+r*.5:.1f},{y-r*.4:.1f}" stroke="{WHITE}" stroke-width="3" fill="none"/>')


def arrow(x1, y1, x2, y2, col=RED, w=3):
    a = math.atan2(y2 - y1, x2 - x1)
    l = 8
    p1 = (x2 - l * math.cos(a - .5), y2 - l * math.sin(a - .5))
    p2 = (x2 - l * math.cos(a + .5), y2 - l * math.sin(a + .5))
    return (f'<path d="M{x1},{y1} L{x2},{y2} M{p1[0]:.1f},{p1[1]:.1f} L{x2},{y2} L{p2[0]:.1f},{p2[1]:.1f}" '
            f'stroke="{col}" stroke-width="{w}" fill="none"/>')


def register(x, y, s=1.0, col=GRAY):
    return (f'<rect x="{x}" y="{y+20*s}" width="{60*s}" height="{30*s}" rx="4" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+20*s} L{x+16*s},{y} L{x+44*s},{y} L{x+50*s},{y+20*s} Z" fill="{WHITE}"/>'
            f'<rect x="{x+20*s}" y="{y+4*s}" width="{20*s}" height="{8*s}" rx="1" fill="{SKY}" stroke-width="1.2"/>'
            + ''.join(f'<rect x="{x+(8+i*12)*s}" y="{y+28*s}" width="{8*s}" height="{6*s}" rx="1" fill="{WHITE}" stroke-width="1"/>' for i in range(4)))


def creditcard(x, y, s=1.0, col=TEAL):
    # 沒有任何品牌的卡：只有晶片和一條線
    return (f'<rect x="{x}" y="{y}" width="{46*s}" height="{30*s}" rx="{4*s}" fill="{col}"/>'
            f'<rect x="{x+6*s}" y="{y+8*s}" width="{10*s}" height="{8*s}" rx="1.5" fill="{GOLD}" stroke-width="1.2"/>'
            f'<path d="M{x+6*s},{y+23*s} L{x+30*s},{y+23*s}" stroke-width="1.6" opacity=".6"/>')


PURPLE = '#b49ad8'
DPURPLE = '#8e72bd'


def building(x, y, w, h, s=1.0, smile=True):
    # 紫色大樓：一排排窗戶，屋頂上一塊空白招牌
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PURPLE}"/>'
         f'<rect x="{x+w*.2:.1f}" y="{y-16}" width="{w*.6:.1f}" height="16" rx="5" fill="{WHITE}"/>')
    rows = int((h - 50) // 22)
    for r in range(rows):
        for c in range(3):
            t += f'<rect x="{x+10+c*(w-20)/3:.1f}" y="{y+12+r*22}" width="{(w-20)/3-8:.1f}" height="14" rx="2" fill="#e8e0f6" stroke-width="1.4"/>'
    t += (f'<rect x="{x+w/2-18:.1f}" y="{y+h-34}" width="36" height="34" rx="3" fill="{SKY}"/>'
          f'<path d="M{x+w/2:.1f},{y+h-34} L{x+w/2:.1f},{y+h}" stroke-width="1.6"/>')
    t += awning(x - 4, y + h - 46, w + 8, DPURPLE, WHITE, n=6, h=10)
    if smile:
        t += face(x + w / 2, y - 8, .6, blush=False)
    return t


def handbag(x, y, s=1.0, col=BRICK):
    return (f'<path d="M{x+10*s},{y} q{10*s},{-16*s} {20*s},0" fill="none" stroke-width="2.6"/>'
            f'<path d="M{x},{y} L{x+40*s},{y} L{x+44*s},{y+28*s} L{x-4*s},{y+28*s} Z" fill="{col}"/>'
            f'<rect x="{x+16*s}" y="{y+6*s}" width="{8*s}" height="{6*s}" rx="1" fill="{GOLD}" stroke-width="1.2"/>')


def watch(x, y, s=1.0, band=BROWN, dial=WHITE):
    return (f'<rect x="{x-6*s}" y="{y-20*s}" width="{12*s}" height="{40*s}" rx="{4*s}" fill="{band}"/>'
            f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{GOLD}"/>'
            f'<circle cx="{x}" cy="{y}" r="{8*s}" fill="{dial}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} L{x},{y-5*s} M{x},{y} L{x+4*s},{y+2*s}" stroke-width="1.6"/>')


def fan(x, y, s=1.0, col=MINT):
    # 小電風扇
    return (f'<circle cx="{x}" cy="{y}" r="{16*s}" fill="{col}"/>'
            + ''.join(f'<path d="M{x},{y} q{10*s*math.cos(a):.1f},{10*s*math.sin(a):.1f} {13*s*math.cos(a+.6):.1f},{13*s*math.sin(a+.6):.1f}" fill="none" stroke-width="1.6"/>'
                      for a in (0, 2.1, 4.2))
            + f'<circle cx="{x}" cy="{y}" r="{3*s}" fill="{WHITE}" stroke-width="1.2"/>'
            f'<path d="M{x},{y+16*s} L{x},{y+28*s} M{x-10*s},{y+28*s} L{x+10*s},{y+28*s}" stroke-width="3"/>')


def diaperpack(x, y, col=SKY):
    return (f'<rect x="{x}" y="{y}" width="24" height="32" rx="5" fill="{col}"/>'
            f'<circle cx="{x+12}" cy="{y+16}" r="7" fill="{SKIN}" stroke-width="1.2"/>' + face(x + 12, y + 17, .3, blush=False))


def stroller(x, y, s=1.0, col=PINK):
    return (f'<path d="M{x},{y} q{0},{-30*s} {30*s},{-30*s} L{x+30*s},{y} Z" fill="{col}"/>'
            f'<rect x="{x-2*s}" y="{y}" width="{40*s}" height="{12*s}" rx="{5*s}" fill="{col}"/>'
            f'<path d="M{x+38*s},{y} L{x+50*s},{y-24*s} L{x+56*s},{y-24*s}" fill="none" stroke-width="2.6"/>'
            f'<circle cx="{x+4*s}" cy="{y+20*s}" r="{6*s}" fill="{WHITE}" stroke-width="2"/>'
            f'<circle cx="{x+32*s}" cy="{y+20*s}" r="{6*s}" fill="{WHITE}" stroke-width="2"/>')


# 1. 紫色大樓
card('building', '手繪紫色的大樓，門口有紫白條紋遮陽棚，路人走過',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f2fb"/>'
     + floor(152, '#e2dbe9')
     + building(70, 28, 100, 124)
     + f'<rect x="22" y="92" width="36" height="60" rx="3" fill="{GRAY}"/><rect x="182" y="80" width="40" height="72" rx="3" fill="#e9dcc8"/>'
     + person(40, 124, ORANGE, .9) + person(200, 126, GREEN, .85, INK)
     + sparkle(30, 30) + star(214, 30, 6) + sparkle(200, 60), bg='#e6f2fb')

# 2. 剖開的大樓：每層賣的東西不一樣
card('floors', '手繪剖開的大樓，每一層擺著零食、藥妝、手錶包包和小家電',
     f'<rect x="20" y="16" width="200" height="146" rx="6" fill="{PURPLE}"/>'
     + ''.join(f'<rect x="28" y="{24+i*35}" width="184" height="30" rx="3" fill="{CREAM}" stroke-width="1.6"/>' for i in range(4))
     # 頂樓：小家電
     + fan(60, 36, .55) + f'<rect x="88" y="30" width="34" height="20" rx="4" fill="{SKY}"/>' + face(105, 39, .45)
     + f'<rect x="140" y="32" width="40" height="18" rx="6" fill="{PINK}"/>'
     # 手錶、包包
     + watch(60, 74, .6) + watch(86, 74, .6, NAVY) + handbag(118, 66, .7) + handbag(160, 66, .7, NAVY)
     # 藥妝
     + pillbox(44, 102, 22, 16) + lipstick(84, 108, RED, .6) + pump(108, 102, MINT, .4) + jar(132, 104, PINK, .5, False) + pillbox(164, 102, 22, 16, '#e8f4ec', GREEN)
     # 零食
     + snack(44, 132, GOLD, .44) + snack(74, 132, ORANGE, .44, False) + snack(104, 132, PINK, .44)
     + f'<rect x="136" y="142" width="54" height="14" rx="3" fill="#9ccf8e"/>'
     + sparkle(228, 20))

# 3. 通道寬，推嬰兒車也好逛
card('family', '手繪寬敞的走道，家人推著嬰兒車逛貨架',
     floor(150, '#efe6f5')
     + shelf(14, 60, 60, 2, 40, BROWN) + shelf(166, 60, 60, 2, 40, BROWN)
     + snack(18, 26, GOLD, .65) + snack(46, 26, PINK, .65, False) + pillbox(22, 82, 20, 16) + jar(50, 80, MINT, .5, False)
     + diaperpack(170, 22) + diaperpack(198, 22, PINK) + snack(172, 70, ORANGE, .6) + jar(200, 80, SKY, .5, False)
     + stroller(88, 128, 1.0) + person(156, 104, LAV, 1.1)
     + face(105, 112, .4, blush=False)
     + sparkle(120, 30) + star(120, 60, 5))

# ---- 提醒小圖 ----
# 同一棟樓裡還有別家店
rem('r-floor', '手繪提醒：大樓裡有一層是別家店，打了問號',
    f'<rect x="26" y="16" width="56" height="92" rx="4" fill="{PURPLE}"/>'
    + ''.join(f'<rect x="32" y="{22+i*21}" width="44" height="16" rx="2" fill="{CREAM if i else GOLD}" stroke-width="1.4"/>' for i in range(4))
    + f'<rect x="32" y="108" width="44" height="8" rx="2" fill="{GRAY}" stroke-width="1.2"/>'
    + f'<circle cx="100" cy="30" r="13" fill="{WHITE}"/>'
    f'<path d="M95,26 q0,-7 6,-7 q6,0 6,6 q0,4 -6,6 L101,35" fill="none" stroke="{RED}" stroke-width="3"/>'
    f'<circle cx="101" cy="40" r="1.8" fill="{RED}" stroke="none"/>'
    + arrow(98, 46, 82, 30, RED, 2.6))

# 不辦免稅也能用
rem('r-nontax', '手繪提醒：沒有護照的一般結帳，券也能用',
    phone(14, 22, .8) + ok(40, 98, 10)
    + passport(66, 30, .8) + f'<path d="M60,24 L104,74" stroke="{RED}" stroke-width="3.5"/>'
    + register(56, 82, .55) + sparkle(100, 16))

# 機場領現金要另付手續費
rem('r-cash', '手繪提醒：在機場領現金，會少一點',
    f'<rect x="14" y="20" width="48" height="74" rx="6" fill="{GRAY}"/>'
    f'<rect x="20" y="28" width="36" height="22" rx="2" fill="{SKY}" stroke-width="1.4"/>'
    f'<rect x="24" y="62" width="28" height="6" rx="2" fill="{INK}" stroke="none"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="{GOLD}"/><circle cx="{x}" cy="{y}" r="4" fill="none" stroke-width="1.2"/>' for x, y in [(80, 86), (98, 96), (84, 104)])
    + f'<circle cx="86" cy="44" r="8" fill="{GOLD}"/>' + arrow(105, 64, 105, 26, RED, 2.6)
    + f'<path d="M80,26 L92,26" stroke="{RED}" stroke-width="4"/>')

print(save(F, OUT), 'files')
