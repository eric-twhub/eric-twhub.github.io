# 札幌藥妝優惠券頁（/japan-coupon/sapporo-drug/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依 MATCHA 發券頁（matcha-jp.com/tw/coupon/22）的店家介紹與適用店舖一覽畫成可愛版，招牌留白、不畫商標；
# 提醒卡依同一頁的使用條件與札幌藥妝店舖公告（shop.satudora.co.jp/detail/store-factory/news/10261719/）。
# 輸出 illust/sp/japan-coupon-sapporo-drug/*.svg，說明在 illust/spots/japan-coupon-sapporo-drug.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-sapporo-drug')
PFX = 'sp-'

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


def pin(x, y, col=RED, s=1.0):
    return (f'<path d="M{x},{y} q{-8*s},{-10*s} {-8*s},{-16*s} a{8*s},{8*s} 0 1 1 {16*s},0 q0,{6*s} {-8*s},{16*s} Z" fill="{col}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{y-16*s}" r="{3*s}" fill="{WHITE}" stroke-width="1.2"/>')


def cookiebox(x, y, s=1.0, col='#f3c9a0'):
    # 伴手禮餅乾盒：蓋子打開，裡面幾片小餅乾
    return (f'<rect x="{x}" y="{y}" width="{60*s}" height="{30*s}" rx="{4*s}" fill="{col}"/>'
            f'<rect x="{x+4*s}" y="{y+4*s}" width="{52*s}" height="{22*s}" rx="{3*s}" fill="{CREAM}" stroke-width="1.4"/>'
            + ''.join(f'<rect x="{x+(8+i*16)*s:.1f}" y="{y+8*s:.1f}" width="{12*s:.1f}" height="{14*s:.1f}" rx="2" fill="#f1d58f" stroke-width="1.2"/>' for i in range(3))
            + face(x + 30 * s, y + 15 * s, .35 * s, blush=False))


def milk(x, y, s=1.0):
    # 玻璃牛奶瓶
    return (f'<rect x="{x+4*s}" y="{y-6*s}" width="{16*s}" height="{6*s}" rx="2" fill="{SKY}" stroke-width="1.4"/>'
            f'<path d="M{x+5*s},{y} L{x+19*s},{y} q{5*s},{8*s} {5*s},{14*s} L{x+24*s},{y+38*s} q0,{4*s} {-4*s},{4*s} L{x+4*s},{y+42*s} '
            f'q{-4*s},0 {-4*s},{-4*s} L{x},{y+14*s} q0,{-6*s} {5*s},{-14*s} Z" fill="{WHITE}" stroke-width="1.8"/>'
            + face(x + 12 * s, y + 24 * s, .45 * s))


def corn(x, y, s=1.0):
    t = (f'<path d="M{x},{y+40*s} q{-14*s},{-20*s} {-4*s},{-38*s} q{6*s},{14*s} {4*s},{38*s} Z" fill="{GREEN}" stroke-width="1.4"/>'
         f'<path d="M{x},{y+40*s} q{14*s},{-20*s} {4*s},{-38*s} q{-6*s},{14*s} {-4*s},{38*s} Z" fill="{DGREEN}" stroke-width="1.4"/>'
         f'<ellipse cx="{x}" cy="{y+16*s}" rx="{8*s}" ry="{20*s}" fill="{GOLD}" stroke-width="1.6"/>')
    for r in range(5):
        for c in (-1, 0, 1):
            t += f'<circle cx="{x+c*4*s:.1f}" cy="{y+(2+r*6)*s:.1f}" r="{1.4*s:.1f}" fill="#e0a52f" stroke="none"/>'
    return t


def staff(x, y, s=1.0):
    # 穿圍裙的店員
    return (person(x, y, '#9fd3c7', s)
            + f'<rect x="{x-5*s}" y="{y+13*s}" width="{10*s}" height="{12*s}" rx="2" fill="{WHITE}" stroke-width="1.2"/>')


def bubble(x, y, w=48, h=30):
    return (f'<path d="M{x},{y} L{x+w},{y} q6,0 6,6 L{x+w+6},{y+h-6} q0,6 -6,6 L{x+16},{y+h} l-8,10 l0,-10 L{x},{y+h} '
            f'q-6,0 -6,-6 L{x-6},{y+6} q0,-6 6,-6 Z" fill="{WHITE}" stroke-width="1.8"/>')


def heart(x, y, r=5, col=PINK):
    return (f'<path d="M{x},{y+r*1.2} q{-r*2},{-r*1.2} {-r},{-r*2} q{r*.6},{-r*.6} {r},{0} '
            f'q{r*.4},{-r*.6} {r},{0} q{r},{r*.8} {-r},{r*2} Z" fill="{col}" stroke-width="1.4"/>')


# 1. 商店街拱廊裡的藥妝店（札幌狸小路一帶就有好幾家）
card('front', '手繪有拱頂的商店街裡，一家藥妝店和逛街的人',
     floor(150, '#ecdcc4')
     + f'<path d="M8,64 Q120,-6 232,64" fill="#e6f2f8" stroke-width="2.2"/>'
     + ''.join(f'<path d="M{x},{64-(1-((x-120)/112)**2)*35:.1f} L{x},150" stroke-width="2" opacity=".7"/>' for x in (30, 210))
     + ''.join(f'<path d="M{120+d},{29+(d/112)**2*35:.1f} L{120+d*1.04:.1f},{36+(d/112)**2*35:.1f}" stroke-width="1.3" opacity=".5"/>' for d in range(-100, 101, 20))
     + shop(62, 62, 116, 88, '#fdf6ec', GOLD, WHITE, PINK)
     + win(70, 112, 22, 26, '#fff3c4') + win(148, 112, 22, 26, '#fff3c4')
     + person(42, 120, LAV, .9) + person(200, 122, ORANGE, .85, INK)
     + sparkle(120, 20) + star(222, 24, 5))

# 2. 北海道伴手禮與飲料
card('souvenir', '手繪伴手禮貨架：餅乾盒、牛奶瓶、玉米和零食',
     floor(156, '#f3e6d6')
     + shelf(16, 100, 208, 2, 52)
     + cookiebox(24, 70, 1.0) + milk(96, 56, 1.0) + corn(150, 58, 1.0) + snack(176, 48, GOLD, 1.0)
     + cookiebox(30, 122, .8, '#cfe6a8') + milk(92, 110, .8) + snack(130, 102, ORANGE, .9, False) + pump(190, 112, MINT, .8)
     + sparkle(140, 30) + star(30, 30, 6))

# 3. 北海道很多、沖繩也有
card('map', '手繪地圖：北海道插滿紅色圖釘，沖繩也有幾根',
     f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#dff0fd"/>'
     + f'<path d="M58,30 q20,-8 34,6 q16,-12 30,-4 q24,4 36,24 q12,10 26,8 q8,12 -4,22 q-18,6 -30,0 q-14,18 -36,22 '
       f'q-10,16 -28,26 q-14,4 -20,-8 q8,-10 2,-18 q-16,-4 -18,-18 q-10,-14 0,-26 q-4,-20 8,-34 Z" fill="#cde8b9"/>'
     + pin(82, 70) + pin(104, 58) + pin(130, 66) + pin(160, 64) + pin(118, 94) + pin(90, 104) + pin(186, 76) + pin(144, 90)
     + f'<path d="M188,132 q10,-10 18,-2 q6,10 4,22 q-2,14 -12,16 q-8,-2 -8,-14 q-6,-12 -2,-22 Z" fill="#cde8b9"/>'
     + pin(194, 146, ORANGE, .7) + pin(202, 156, ORANGE, .7) + pin(198, 166, ORANGE, .7)
     + f'<path d="M120,158 q30,-4 60,-10" stroke-width="1.6" stroke-dasharray="4 4" fill="none"/>'
     + sparkle(30, 150) + star(30, 30, 6), bg='#dff0fd')

# 4. 部分分店有會說中文的店員
card('staff', '手繪穿圍裙的店員和旅客開心地聊天',
     floor(152)
     + staff(128, 72, 1.4) + register(92, 100, 1.1) + person(60, 96, PINK, 1.3)
     + bubble(150, 26, 52, 30) + heart(170, 36, 5) + heart(186, 38, 4, RED)
     + bubble(20, 34, 44, 26) + sparkle(42, 46, 6)
     + star(220, 100, 6))

# ---- 提醒小圖 ----
# 菸酒等部分商品不折，也不能疊其他券
rem('r-alcohol', '手繪提醒：酒瓶和香菸不在折扣裡',
    f'<rect x="22" y="44" width="14" height="10" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
    f'<path d="M22,54 L36,54 q8,10 8,22 L44,104 L14,104 L14,76 q0,-12 8,-22 Z" fill="#a8d5b5" stroke-width="1.8"/>'
    f'<rect x="18" y="74" width="22" height="18" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
    f'<rect x="54" y="66" width="36" height="38" rx="3" fill="{LAV}" stroke-width="1.8"/>'
    f'<path d="M54,78 L90,78" stroke-width="1.4"/><rect x="62" y="56" width="6" height="12" fill="#f2e3c6" stroke-width="1.2"/>'
    f'<rect x="72" y="58" width="6" height="10" fill="#f2e3c6" stroke-width="1.2"/>'
    + nope(92, 32, 15))

# 護照和券在付款前一起拿出來
rem('r-passport', '手繪提醒：先拿護照和券，再拿錢包',
    passport(12, 30, .9) + phone(52, 20, .85) + arrow(46, 98, 72, 98, RED, 3)
    + f'<rect x="78" y="86" width="30" height="22" rx="4" fill="{BROWN}"/><path d="M78,94 L108,94" stroke-width="1.4"/>'
    + sparkle(100, 30))

print(save(F, OUT), 'files')
