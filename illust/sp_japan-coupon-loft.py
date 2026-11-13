# Loft 頁（/japan-coupon/loft/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依 Loft 官網（loft.co.jp）首頁的文具、美妝、生活用品介紹與免稅店一覽頁（loft.co.jp/pages/taxfreeshops/）畫成可愛版；
# 招牌留白，不畫商標與招牌配色。輸出 illust/sp/japan-coupon-loft/*.svg，說明在 illust/spots/japan-coupon-loft.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-loft')
PFX = 'lf-'

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


def notebook(x, y, s=1.0, col=SKY):
    return (f'<rect x="{x}" y="{y}" width="{30*s}" height="{40*s}" rx="{3*s}" fill="{col}"/>'
            f'<path d="M{x+6*s},{y} L{x+6*s},{y+40*s}" stroke-width="1.4"/>'
            f'<rect x="{x+10*s}" y="{y+8*s}" width="{16*s}" height="{8*s}" rx="1" fill="{WHITE}" stroke-width="1.2"/>')


def pencup(x, y, s=1.0, col=PINK):
    t = ''
    for dx, c, h in [(4, RED, 30), (11, GOLD, 36), (18, NAVY, 28), (25, GREEN, 34)]:
        t += (f'<rect x="{x+dx*s}" y="{y-h*s}" width="{5*s}" height="{h*s}" rx="1" fill="{c}" stroke-width="1.2"/>'
              f'<path d="M{x+dx*s},{y-h*s} l{2.5*s},{-5*s} l{2.5*s},{5*s}" fill="{WHITE}" stroke-width="1.2"/>')
    return t + f'<rect x="{x}" y="{y-6*s}" width="{34*s}" height="{30*s}" rx="{5*s}" fill="{col}"/>' + face(x + 17 * s, y + 8 * s, .5 * s)


def tape(x, y, r=12, col=PINK):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/><circle cx="{x}" cy="{y}" r="{r*.45:.1f}" fill="{CREAM}" stroke-width="1.4"/>'
            + ''.join(f'<circle cx="{x+r*.72*math.cos(a):.1f}" cy="{y+r*.72*math.sin(a):.1f}" r="1.3" fill="{WHITE}" stroke="none"/>' for a in (0, 1.6, 3.2, 4.8)))


def humidifier(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y+40*s} q{-4*s},{-30*s} {18*s},{-40*s} q{22*s},{10*s} {18*s},{40*s} Z" fill="{col}" stroke-width="1.8"/>'
            + face(x + 18 * s, y + 22 * s, .55 * s)
            + ''.join(f'<path d="M{x+(12+i*6)*s},{y-4*s} q{-4*s},{-6*s} 0,{-12*s} q{4*s},{-6*s} 0,{-12*s}" fill="none" stroke-width="1.6" opacity=".55"/>' for i in range(2)))


def candle(x, y, s=1.0, col=LAV):
    return (f'<rect x="{x}" y="{y}" width="{20*s}" height="{24*s}" rx="{3*s}" fill="{col}"/>'
            f'<path d="M{x+10*s},{y} L{x+10*s},{y-5*s}" stroke-width="1.4"/>'
            f'<path d="M{x+10*s},{y-6*s} q{-5*s},{-6*s} 0,{-12*s} q{5*s},{6*s} 0,{12*s} Z" fill="{GOLD}" stroke-width="1.2"/>')


def mug(x, y, s=1.0, col=MINT):
    return (f'<path d="M{x+24*s},{y+6*s} q{10*s},0 {10*s},{9*s} q0,{9*s} {-10*s},{9*s}" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{26*s}" height="{28*s}" rx="{5*s}" fill="{col}"/>' + face(x + 13 * s, y + 14 * s, .5 * s))


# 1. 車站商場裡的雜貨店
card('front', '手繪生活雜貨店門口，櫥窗裡擺著筆記本和馬克杯',
     floor(152, '#e7e4ef')
     + shop(30, 26, 180, 126, '#fbfaf6', SKY, WHITE, PEACH)
     + win(40, 92, 52, 46, '#fdfbf4') + win(148, 92, 52, 46, '#fdfbf4')
     + notebook(46, 100, .7, PINK) + notebook(68, 100, .7, GOLD) + mug(154, 108, .8) + candle(178, 110, .7)
     + person(16, 128, ORANGE, .8) + sparkle(226, 24) + star(14, 30, 6))

# 2. 文具
card('stationery', '手繪文具：筆筒、筆記本和紙膠帶',
     floor(156, '#f3e6d6')
     + shelf(16, 106, 208, 1)
     + pencup(26, 82, 1.0) + notebook(80, 64, 1.0, SKY) + notebook(116, 66, .95, PINK) + notebook(150, 68, .9, GOLD)
     + tape(48, 136, 13, PINK) + tape(84, 138, 12, MINT) + tape(116, 136, 13, GOLD) + tape(148, 138, 11, LAV)
     + f'<rect x="170" y="122" width="44" height="30" rx="4" fill="{WHITE}"/>' + star(184, 134, 6, PINK) + star(202, 140, 5, GOLD)
     + sparkle(200, 36) + star(196, 70, 6))

# 3. 美妝雜貨
card('cosme', '手繪美妝雜貨區：鏡子、口紅、乳霜和化妝刷',
     floor(156, '#f6e9ee')
     + shelf(16, 104, 208, 2, 48)
     + f'<rect x="24" y="44" width="44" height="58" rx="22" fill="{SKY}" stroke-width="2"/>'
     f'<path d="M34,58 l10,-6" stroke="{WHITE}" stroke-width="2.4"/>'
     + lipstick(84, 78, RED, 1.0) + lipstick(104, 78, PINK, 1.0) + jar(130, 74, PEACH, .8)
     + f'<path d="M184,100 L196,52" stroke-width="3"/><path d="M190,58 q2,-12 10,-12 q4,4 -2,14 Z" fill="{PINK}" stroke-width="1.4"/>'
     + jar(30, 124, LAV, .7, False) + tube(70, 136, PINK, .7) + pump(130, 128, MINT, .6) + lipstick(170, 130, ORANGE, .7) + lipstick(190, 130, '#c45a7a', .7)
     + sparkle(220, 30) + star(150, 34, 6))

# 4. 生活小物
card('home', '手繪生活小物：加濕器、香氛蠟燭和馬克杯',
     floor(150, '#eef3e8')
     + f'<rect x="16" y="110" width="208" height="40" rx="6" fill="#e3d2bc"/>'
     + humidifier(40, 70, 1.0) + candle(104, 86, 1.0) + candle(130, 92, .8, PINK) + mug(162, 82, 1.0, GOLD)
     + f'<path d="M200,110 q-4,-30 10,-40" fill="none" stroke="{DGREEN}" stroke-width="2.4"/>'
     + f'<ellipse cx="212" cy="72" rx="8" ry="5" fill="{GREEN}" stroke-width="1.4"/>'
     + sparkle(120, 34) + star(30, 30, 6) + sparkle(210, 30))

# ---- 提醒小圖 ----
# 不是每家都能免稅
rem('r-notall', '手繪提醒：兩家店，一家可以免稅、一家打問號',
    f'<rect x="10" y="40" width="46" height="50" rx="4" fill="{WHITE}"/>' + awning(8, 40, 50, SKY, WHITE, 3, 10)
    + f'<rect x="64" y="40" width="46" height="50" rx="4" fill="{WHITE}"/>' + awning(62, 40, 50, PEACH, WHITE, 3, 10)
    + ok(33, 24, 11)
    + f'<circle cx="87" cy="24" r="12" fill="{WHITE}"/>'
    f'<path d="M82,20 q0,-6 5,-6 q6,0 6,5 q0,4 -6,6 L87,30" fill="none" stroke="{RED}" stroke-width="2.6"/>'
    + passport(20, 64, .45) + passport(74, 64, .45))

# 退稅還會扣匯款手續費
rem('r-wire', '手繪提醒：退回來的錢，路上被扣了兩次',
    f'<circle cx="26" cy="60" r="16" fill="{GOLD}"/><circle cx="26" cy="60" r="8" fill="none" stroke-width="1.6"/>'
    + arrow(46, 60, 96, 60, INK, 2.6)
    + f'<path d="M58,40 L70,40" stroke="{RED}" stroke-width="4"/><path d="M78,40 L90,40" stroke="{RED}" stroke-width="4"/>'
    + creditcard(68, 76, .9) + sparkle(20, 22))

print(save(F, OUT), 'files')
