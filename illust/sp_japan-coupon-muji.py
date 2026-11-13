# 無印良品頁（/japan-coupon/muji/）的「店裡大概長這樣」插圖與提醒卡（2026-11-13）。
# 依 coupons.json 對日本店品項的說明（收納、衣物、食品線）畫成可愛版；招牌留白，不畫商標與店名字樣。
# 提醒卡依觀光廳與國稅廳的新制免稅旅客說明。輸出 illust/sp/japan-coupon-muji/*.svg，說明在 illust/spots/japan-coupon-muji.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-muji')
PFX = 'mj-'

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


WOOD = '#dcc3a0'
LWOOD = '#efe0c8'
KRAFT = '#c9a77c'
OAT = '#f1ebe0'


def drawers(x, y, s=1.0, n=3):
    # 半透明的白色抽屜盒
    t = f'<rect x="{x}" y="{y}" width="{50*s}" height="{n*18*s+6*s}" rx="{3*s}" fill="#f7f7f4"/>'
    for i in range(n):
        t += (f'<rect x="{x+4*s}" y="{y+(4+i*18)*s}" width="{42*s}" height="{14*s}" rx="2" fill="#eceff1" stroke-width="1.4"/>'
              f'<path d="M{x+19*s},{y+(9+i*18)*s} L{x+31*s},{y+(9+i*18)*s}" stroke-width="1.8"/>')
    return t


def basket2(x, y, s=1.0):
    # 藤編籃
    return (f'<rect x="{x}" y="{y}" width="{52*s}" height="{30*s}" rx="{6*s}" fill="{KRAFT}"/>'
            + ''.join(f'<path d="M{x+4*s},{y+(7+i*8)*s} L{x+48*s},{y+(7+i*8)*s}" stroke-width="1.2" opacity=".6"/>' for i in range(3))
            + ''.join(f'<path d="M{x+(9+i*9)*s},{y+3*s} L{x+(9+i*9)*s},{y+27*s}" stroke-width="1" opacity=".4"/>' for i in range(5)))


def folded(x, y, col, s=1.0):
    # 摺好的一件衣服
    return (f'<rect x="{x}" y="{y}" width="{36*s}" height="{12*s}" rx="{3*s}" fill="{col}" stroke-width="1.6"/>'
            f'<path d="M{x+13*s},{y} q{5*s},{5*s} {10*s},0" fill="none" stroke-width="1.2"/>')


def hanger(x, y, col, s=1.0):
    return (f'<path d="M{x},{y-8*s} q0,{-6*s} {4*s},{-6*s}" fill="none" stroke-width="1.6"/>'
            f'<path d="M{x-16*s},{y} L{x},{y-8*s} L{x+16*s},{y}" fill="none" stroke-width="1.6"/>'
            f'<path d="M{x-14*s},{y} L{x-22*s},{y+12*s} L{x-14*s},{y+16*s} L{x-12*s},{y+44*s} L{x+12*s},{y+44*s} L{x+14*s},{y+16*s} '
            f'L{x+22*s},{y+12*s} L{x+14*s},{y} q{-14*s},{8*s} {-28*s},0 Z" fill="{col}" stroke-width="1.6"/>')


def pouch(x, y, s=1.0, col=KRAFT):
    # 牛皮紙色的立袋包裝
    return (f'<path d="M{x},{y} L{x+34*s},{y} L{x+36*s},{y+44*s} L{x-2*s},{y+44*s} Z" fill="{col}" stroke-width="1.8"/>'
            f'<path d="M{x},{y+6*s} L{x+34*s},{y+6*s}" stroke-width="1.2"/>'
            f'<rect x="{x+6*s}" y="{y+16*s}" width="{22*s}" height="{16*s}" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
            + face(x + 17 * s, y + 24 * s, .4 * s, blush=False))


def teabox(x, y, s=1.0, col=OAT):
    return (f'<rect x="{x}" y="{y}" width="{30*s}" height="{36*s}" rx="{2*s}" fill="{col}"/>'
            f'<circle cx="{x+15*s}" cy="{y+16*s}" r="{7*s}" fill="#b9d6a8" stroke-width="1.2"/>'
            f'<path d="M{x+15*s},{y+9*s} L{x+15*s},{y+23*s}" stroke-width="1"/>')


# 1. 木頭色的店面
card('front', '手繪木頭色系的生活用品店，櫥窗裡有收納盒和摺好的衣服',
     floor(152, '#e8e2d6')
     + f'<rect x="30" y="26" width="180" height="126" rx="6" fill="{OAT}"/>'
     + f'<rect x="40" y="34" width="160" height="22" rx="4" fill="{LWOOD}"/>'
     + f'<rect x="30" y="62" width="180" height="8" fill="{WOOD}"/>'
     + win(40, 80, 54, 60, '#fbfaf6') + win(146, 80, 54, 60, '#fbfaf6')
     + drawers(46, 94, .8, 2) + folded(152, 120, '#dfe7ef', .9) + folded(152, 108, WHITE, .9) + folded(152, 96, '#e8d9c4', .9)
     + f'<rect x="104" y="100" width="32" height="52" rx="3" fill="{LWOOD}"/><path d="M120,100 L120,152" stroke-width="1.6"/>'
     + face(120, 44, .6, blush=False)
     + person(222, 126, '#9fb8c8', .8, INK) + sparkle(16, 30) + star(222, 28, 5))

# 2. 收納
card('storage', '手繪收納區：白色抽屜盒和藤編籃排在層架上',
     floor(156, '#ede6da')
     + f'<rect x="20" y="20" width="200" height="136" rx="4" fill="none" stroke-width="2"/>'
     + shelf(20, 92, 200, 1, 0, WOOD)
     + drawers(30, 30, 1.0, 3) + drawers(88, 30, 1.0, 3) + basket2(150, 56, 1.0)
     + basket2(32, 120, 1.0) + basket2(92, 120, 1.0) + drawers(156, 98, .9, 3)
     + face(55, 48, .5) + sparkle(200, 40))

# 3. 衣物
card('clothes', '手繪衣物區：摺好的衣服疊在桌上，旁邊掛著上衣',
     floor(150, '#ede6da')
     + f'<rect x="18" y="104" width="120" height="46" rx="4" fill="{LWOOD}"/>'
     + ''.join(folded(26 + c * 38, 92 - r * 12, col, .95) for c, cols in enumerate([['#dfe7ef', WHITE, '#c9d6e3'], ['#e8d9c4', OAT, '#d8c4a8'], ['#e3e8dc', '#f3efe6', '#c8d4bc']]) for r, col in enumerate(cols))
     + f'<path d="M150,30 L226,30" stroke-width="3"/>'
     + hanger(166, 44, '#c9d6e3', .9) + hanger(206, 44, '#e8d9c4', .9)
     + face(185, 26, 0.01, blush=False)
     + sparkle(40, 30) + star(120, 32, 6))

# 4. 食品
card('food', '手繪食品區：牛皮紙色的零食袋和茶的盒子',
     floor(156, '#ede6da')
     + shelf(16, 104, 208, 2, 48, WOOD)
     + pouch(26, 58, 1.0) + pouch(70, 58, 1.0, '#e6d3b3') + teabox(116, 66, 1.0) + teabox(152, 66, 1.0, '#e9e2f0') + pouch(190, 66, .8, '#d9c9a6')
     + snack(28, 107, '#e8d9c4', .9) + pouch(80, 117, .8) + teabox(120, 123, .8, '#f3e3d3') + snack(160, 107, '#d9c9a6', .9, False)
     + sparkle(120, 30) + star(30, 30, 6))

# ---- 提醒小圖 ----
# 吃掉的就不退：收據以張為單位
rem('r-food', '手繪提醒：同一張收據的零食被吃掉一個，整張打叉',
    receipt(14, 18, 1.0, 4)
    + pouch(62, 22, .7) + snack(88, 22, '#e8d9c4', .55, False)
    + f'<circle cx="80" cy="84" r="16" fill="#e8d9c4" stroke-width="1.8"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{DBROWN}" stroke="none"/>' for x, y in [(74, 80), (82, 90), (86, 78), (72, 90)])
    + f'<circle cx="95" cy="74" r="7" fill="{YEL}" stroke="none"/><circle cx="98" cy="84" r="6" fill="{YEL}" stroke="none"/>'
    + cross(31, 98, 10))

# 收納箱先別託運
rem('r-checkin', '手繪提醒：大箱子先別放上託運輸送帶',
    f'<rect x="10" y="84" width="100" height="14" rx="7" fill="{GRAY}"/>'
    + ''.join(f'<circle cx="{x}" cy="91" r="3" fill="{WHITE}" stroke-width="1"/>' for x in (22, 46, 70, 94))
    + f'<rect x="54" y="42" width="44" height="40" rx="3" fill="{KRAFT}"/><path d="M54,54 L98,54 M76,42 L76,54" stroke-width="1.4"/>'
    + passport(14, 30, .7) + nope(84, 30, 13))

print(save(F, OUT), 'files')
