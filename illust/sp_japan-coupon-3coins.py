# 3COINS 頁（/japan-coupon/3coins/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依 3COINS 官方網路商店（palcloset.jp/3coins/）的商品分類畫成可愛版；招牌留白，不畫商標，也不畫硬幣圖案。
# 提醒卡依觀光廳旅客問答與 coupons.json 的免稅門檻說明。
# 輸出 illust/sp/japan-coupon-3coins/*.svg，說明在 illust/spots/japan-coupon-3coins.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-3coins')
PFX = 'tc-'

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


def plate(x, y, r=14, col=WHITE, rim=SKY):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.42:.1f}" fill="{col}" stroke-width="1.8"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r*.62:.1f}" ry="{r*.25:.1f}" fill="none" stroke="{rim}" stroke-width="1.6"/>')


def bowl(x, y, s=1.0, col=PINK):
    return (f'<path d="M{x-18*s},{y} q0,{20*s} {18*s},{20*s} q{18*s},0 {18*s},{-20*s} Z" fill="{col}" stroke-width="1.8"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{18*s}" ry="{4*s}" fill="{WHITE}" stroke-width="1.6"/>'
            + ''.join(f'<circle cx="{x+dx*s}" cy="{y+10*s}" r="{1.8*s}" fill="{WHITE}" stroke="none"/>' for dx in (-8, 0, 8)))


def ladle(x, y, s=1.0, col=MINT):
    return (f'<path d="M{x},{y} L{x},{y+40*s}" stroke-width="3"/>'
            f'<path d="M{x-10*s},{y+40*s} q{10*s},{14*s} {20*s},0 Z" fill="{col}" stroke-width="1.6"/>')


def whisk(x, y, s=1.0):
    return (f'<rect x="{x-3*s}" y="{y}" width="{6*s}" height="{18*s}" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
            f'<path d="M{x-2*s},{y+18*s} q{-10*s},{14*s} {2*s},{24*s} M{x+2*s},{y+18*s} q{10*s},{14*s} {-2*s},{24*s} M{x},{y+18*s} L{x},{y+42*s}" fill="none" stroke-width="1.4"/>')


def slipper(x, y, s=1.0, col=PINK):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{10*s}" ry="{22*s}" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x-10*s},{y-8*s} q{10*s},{-14*s} {20*s},0 L{x+10*s},{y-4*s} q{-10*s},{-10*s} {-20*s},0 Z" fill="{WHITE}" stroke-width="1.6"/>')


def umbrella(x, y, s=1.0, col=SKY):
    return (f'<path d="M{x-24*s},{y} q{24*s},{-30*s} {48*s},0 q{-6*s},{-4*s} {-12*s},0 q{-6*s},{-4*s} {-12*s},0 q{-6*s},{-4*s} {-12*s},0 q{-6*s},{-4*s} {-12*s},0 Z" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x},{y-1*s} L{x},{y+26*s} q0,{6*s} {-6*s},{6*s}" fill="none" stroke-width="2.2"/>')


def bin_(x, y, s=1.0, col=MINT):
    return (f'<path d="M{x},{y} L{x+40*s},{y} L{x+36*s},{y+30*s} L{x+4*s},{y+30*s} Z" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x+4*s},{y+8*s} L{x+36*s},{y+8*s}" stroke-width="1.2" opacity=".6"/>'
            + face(x + 20 * s, y + 18 * s, .45 * s))


def pouch2(x, y, s=1.0, col=LAV):
    # 旅行用的拉鍊收納包
    return (f'<rect x="{x}" y="{y}" width="{44*s}" height="{28*s}" rx="{8*s}" fill="{col}"/>'
            f'<path d="M{x+4*s},{y+6*s} L{x+40*s},{y+6*s}" stroke-width="1.4" stroke-dasharray="2 2"/>'
            f'<circle cx="{x+38*s}" cy="{y+6*s}" r="{2.6*s}" fill="{GOLD}" stroke-width="1.2"/>')


def clip(x, y, col=PINK, s=1.0):
    return (f'<path d="M{x},{y} q{8*s},{-8*s} {16*s},0 q{8*s},{-8*s} {16*s},0 l0,{8*s} q{-8*s},{8*s} {-16*s},0 q{-8*s},{8*s} {-16*s},0 Z" fill="{col}" stroke-width="1.6"/>'
            f'<circle cx="{x+16*s}" cy="{y+4*s}" r="{3*s}" fill="{GOLD}" stroke-width="1.2"/>')


def polish(x, y, col=RED, s=1.0):
    return (f'<rect x="{x+4*s}" y="{y-14*s}" width="{8*s}" height="{14*s}" rx="2" fill="{INK}" stroke="none"/>'
            f'<rect x="{x}" y="{y}" width="{16*s}" height="{20*s}" rx="{5*s}" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+4*s},{y+5*s} l0,{8*s}" stroke="{WHITE}" stroke-width="1.6"/>')


def phonecase(x, y, col=SKY, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{26*s}" height="{46*s}" rx="{6*s}" fill="{col}"/>'
            f'<rect x="{x+3*s}" y="{y+3*s}" width="{10*s}" height="{12*s}" rx="3" fill="{INK}" opacity=".75" stroke="none"/>'
            + star(x + 15 * s, y + 30 * s, 5 * s, GOLD))


def scrunchie(x, y, r=12, col=PEACH):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke-width="1.8"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*.45:.1f}" fill="{CREAM}" stroke-width="1.4"/>'
            + ''.join(f'<path d="M{x+r*.5*math.cos(a):.1f},{y+r*.5*math.sin(a):.1f} L{x+r*.95*math.cos(a):.1f},{y+r*.95*math.sin(a):.1f}" stroke-width="1" opacity=".55"/>' for a in [i * .9 for i in range(7)]))


# 1. 店面：門口一張平台堆著各種小東西
card('front', '手繪小雜貨店門口，平台上堆著碗、拖鞋和收納包',
     floor(152, '#f0e6ee')
     + shop(40, 24, 160, 128, '#fdfbf8', PINK, WHITE, '#d7ecd9')
     + win(50, 88, 40, 44, '#fdfbf4') + win(150, 88, 40, 44, '#fdfbf4')
     + bowl(70, 112, .7, GOLD) + slipper(170, 112, .6, LAV)
     + f'<rect x="8" y="126" width="56" height="26" rx="4" fill="#e3d2bc"/>' + pouch2(14, 108, .6, MINT) + bowl(50, 116, .5, PINK)
     + f'<rect x="176" y="126" width="56" height="26" rx="4" fill="#e3d2bc"/>' + umbrella(204, 104, .7, PEACH)
     + sparkle(20, 30) + star(222, 28, 6))

# 2. 廚房用品與餐具
card('kitchen', '手繪廚房用品：碗盤、湯勺、打蛋器',
     floor(156, '#f3e6d6')
     + f'<rect x="20" y="20" width="200" height="84" rx="6" fill="#f6eee2"/>'
     + ''.join(f'<path d="M{40+i*32},20 L{40+i*32},26" stroke-width="1.6"/>' for i in range(6))
     + ladle(46, 26, 1.0) + whisk(78, 26, 1.0) + ladle(110, 26, .9, PINK) + whisk(142, 26, .9)
     + f'<rect x="166" y="36" width="44" height="54" rx="6" fill="{WHITE}"/><circle cx="188" cy="62" r="12" fill="{SKY}" stroke-width="1.6"/>'
     + shelf(16, 140, 208, 1)
     + plate(46, 134, 20, WHITE, PINK) + plate(46, 126, 20, WHITE, PINK) + bowl(110, 118, 1.0, MINT) + bowl(170, 118, 1.0, GOLD)
     + sparkle(214, 120) + star(214, 22, 5))

# 3. 收納、拖鞋、雨具、旅行用品
card('home', '手繪生活用品：收納籃、室內拖鞋、雨傘和旅行收納包',
     floor(150, '#eaf0e6')
     + bin_(20, 120, 1.0) + bin_(66, 120, 1.0, PEACH)
     + slipper(130, 126, 1.0, PINK) + slipper(156, 126, 1.0, PINK)
     + f'<rect x="184" y="118" width="26" height="32" rx="4" fill="{GRAY}"/>' + umbrella(200, 86, 1.0, SKY) + umbrella(192, 96, .8, PINK)
     + shelf(16, 90, 130, 1) + pouch2(26, 62, 1.0, LAV) + pouch2(80, 68, .8, MINT)
     + sparkle(140, 40) + star(30, 30, 6) + sparkle(110, 70))

# 4. 小飾品：髮飾、指甲油、手機殼
card('acc', '手繪小飾品：髮夾、髮圈、指甲油和手機殼',
     floor(156, '#f6e9ee')
     + f'<rect x="18" y="22" width="110" height="72" rx="6" fill="{WHITE}"/>'
     + ''.join(f'<circle cx="{30+c*20}" cy="{34+r*20}" r="1.6" fill="{INK}" stroke="none" opacity=".4"/>' for c in range(5) for r in range(4))
     + clip(28, 46, PINK) + clip(76, 46, GOLD) + clip(28, 76, MINT) + clip(76, 76, LAV)
     + scrunchie(160, 50, 14, PEACH) + scrunchie(196, 56, 12, SKY)
     + shelf(16, 138, 208, 1)
     + polish(30, 118, RED) + polish(54, 118, PINK) + polish(78, 118, MINT)
     + phonecase(130, 92, SKY) + phonecase(166, 92, PINK) + sparkle(214, 100) + star(150, 22, 5))

# ---- 提醒小圖 ----
# 同一張收據少一件，整張不退
rem('r-receipt', '手繪提醒：同一張收據的小東西少了一個，整張打叉',
    receipt(14, 16, 1.0, 5)
    + clip(60, 30, PINK, .9) + polish(92, 26, MINT, .8) + bowl(74, 62, .6, GOLD)
    + f'<path d="M58,80 L102,80" stroke-width="1.4" stroke-dasharray="3 3"/>'
    + f'<circle cx="82" cy="98" r="9" fill="none" stroke-width="1.8" stroke-dasharray="3 3"/>'
    + cross(31, 98, 10))

# 不同分店的收據不能加起來
rem('r-samestore', '手繪提醒：兩家店的收據不能疊在一起算',
    f'<rect x="8" y="26" width="44" height="32" rx="4" fill="{WHITE}"/>' + awning(6, 26, 48, PINK, WHITE, 3, 9)
    + f'<rect x="68" y="26" width="44" height="32" rx="4" fill="{WHITE}"/>' + awning(66, 26, 48, MINT, WHITE, 3, 9)
    + receipt(14, 66, .7, 3) + receipt(74, 66, .7, 3)
    + f'<path d="M50,80 L70,80" stroke-width="2.4"/><path d="M60,70 L60,90" stroke-width="2.4"/>' + nope(60, 80, 13))

print(save(F, OUT), 'files')
