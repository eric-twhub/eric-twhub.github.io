# 松本清優惠券頁的店內插圖與提醒卡（2026-11-13）。
# 依據 MATCHA 發券頁（matcha-jp.com/tw/coupon/72）的店家介紹與使用條件畫成可愛版；
# 招牌留白、不畫店家標誌與配色。說明文字放在 illust/spots/japan-coupon-matsukiyo.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-coupon-matsukiyo')
PFX = 'jcm-'

W, H = 240, 180
F = {}
LAV = '#c9b8e8'
MINT = '#bfe8d6'
PEACH = '#f9d2b4'
TEAL = '#7cc7c2'
ORANGE = '#f2a46b'
BEIGE = '#e9dcc8'
YEL = '#fff3c4'


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


def shop(x, y, w, h, wall, a1, a2, sign, door=SKY, smile=True):
    """空白招牌的可愛店面：招牌只畫臉，不寫字。"""
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{wall}"/>'
         f'<rect x="{x+10}" y="{y+8}" width="{w-20}" height="24" rx="8" fill="{sign}"/>')
    if smile:
        t += face(x + w / 2, y + 18, .8)
    t += awning(x - 4, y + 38, w + 8, a1, a2, n=max(4, int(w // 26)))
    dw = min(34, w * .26)
    t += (f'<rect x="{x+w/2-dw/2:.1f}" y="{y+h-40}" width="{dw:.1f}" height="40" rx="3" fill="{door}"/>'
          f'<path d="M{x+w/2:.1f},{y+h-40} L{x+w/2:.1f},{y+h}" stroke-width="1.6"/>')
    return t


def win(x, y, w, h, col=SKY):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{col}"/>'


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def camera(x, y, s=1.0, col=GRAY):
    return (f'<rect x="{x+8*s}" y="{y-6*s}" width="{14*s}" height="8" rx="2" fill="{col}"/>'
            f'<rect x="{x}" y="{y}" width="{48*s}" height="{32*s}" rx="{6*s}" fill="{col}"/>'
            f'<circle cx="{x+26*s}" cy="{y+17*s}" r="{11*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+26*s}" cy="{y+17*s}" r="{5*s}" fill="{SKY}" stroke-width="1.4"/>'
            f'<circle cx="{x+23*s}" cy="{y+14*s}" r="{1.6*s}" fill="{WHITE}" stroke="none"/>'
            f'<rect x="{x+38*s}" y="{y+5*s}" width="{6*s}" height="{4*s}" rx="1" fill="{GOLD}" stroke-width="1.2"/>')


def watch(x, y, s=1.0, band=BROWN, dial=WHITE):
    # x,y 是錶面中心
    return (f'<rect x="{x-7*s}" y="{y-26*s}" width="{14*s}" height="{52*s}" rx="{4*s}" fill="{band}"/>'
            f'<circle cx="{x}" cy="{y}" r="{14*s}" fill="{GOLD}"/>'
            f'<circle cx="{x}" cy="{y}" r="{10.5*s}" fill="{dial}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} L{x},{y-7*s} M{x},{y} L{x+5*s},{y+2*s}" stroke-width="1.8"/>')


def tv(x, y, w=70, h=48, col=NAVY):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{col}"/>'
            f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" rx="3" fill="{SKY}" stroke-width="1.4"/>'
            + face(x + w / 2, y + h / 2 - 2, .8)
            + f'<path d="M{x+w/2-10},{y+h+10} L{x+w/2+10},{y+h+10} M{x+w/2},{y+h} L{x+w/2},{y+h+10}" stroke-width="2.4"/>')


def ricecooker(x, y, s=1.0, col=WHITE):
    return (f'<rect x="{x}" y="{y+10*s}" width="{50*s}" height="{36*s}" rx="{12*s}" fill="{col}"/>'
            f'<path d="M{x+2*s},{y+16*s} q{23*s},{-22*s} {46*s},0 Z" fill="{GRAY}"/>'
            f'<rect x="{x+18*s}" y="{y+2*s}" width="{14*s}" height="{6*s}" rx="2" fill="{GRAY}" stroke-width="1.4"/>'
            f'<rect x="{x+16*s}" y="{y+34*s}" width="{18*s}" height="{6*s}" rx="2" fill="{GOLD}" stroke-width="1.2"/>'
            + face(x + 25 * s, y + 25 * s, .7 * s))


def kettle(x, y, s=1.0, col=MINT):
    return (f'<path d="M{x+36*s},{y+14*s} q{12*s},{0} {12*s},{14*s} q0,{12*s} {-12*s},{12*s}" fill="none" stroke-width="3"/>'
            f'<path d="M{x},{y+44*s} L{x+4*s},{y+8*s} q{16*s},{-8*s} {32*s},0 L{x+40*s},{y+44*s} Z" fill="{col}"/>'
            f'<path d="M{x+2*s},{y+16*s} l{-10*s},{-8*s}" stroke-width="3"/>'
            f'<rect x="{x-4*s}" y="{y+44*s}" width="{48*s}" height="{6*s}" rx="2" fill="{GRAY}"/>'
            + face(x + 20 * s, y + 28 * s, .6 * s))


def dryer(x, y, s=1.0, col=PINK):
    return (f'<rect x="{x+22*s}" y="{y+16*s}" width="{12*s}" height="{34*s}" rx="{5*s}" fill="{col}"/>'
            f'<rect x="{x}" y="{y}" width="{52*s}" height="{24*s}" rx="{12*s}" fill="{col}"/>'
            f'<ellipse cx="{x+50*s}" cy="{y+12*s}" rx="{5*s}" ry="{11*s}" fill="{GRAY}"/>'
            + ''.join(f'<path d="M{x+62*s},{y+(4+i*8)*s} q{6*s},{-3*s} {12*s},0" fill="none" stroke-width="1.6" opacity=".6"/>' for i in range(3))
            + face(x + 22 * s, y + 11 * s, .6 * s))


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
    return (f'<path d="M{x+7*s},{y-14*s} q{-5*s},{8*s} 0,{14*s} q{5*s},{-6*s} 0,{-14*s} Z" fill="{WHITE}" stroke-width="1.4"/>'
            f'<rect x="{x}" y="{y}" width="{14*s}" height="{28*s}" rx="{5*s}" fill="{col}" stroke-width="1.6"/>'
            f'<circle cx="{x+7*s}" cy="{y+40*s}" r="{3*s}" fill="{SKY}" stroke-width="1.2"/>')


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


def candy(x, y, col=PINK, s=1.0):
    return (f'<path d="M{x-14*s},{y-6*s} L{x-8*s},{y} L{x-14*s},{y+6*s} Z" fill="{col}" stroke-width="1.4"/>'
            f'<path d="M{x+14*s},{y-6*s} L{x+8*s},{y} L{x+14*s},{y+6*s} Z" fill="{col}" stroke-width="1.4"/>'
            f'<circle cx="{x}" cy="{y}" r="{8*s}" fill="{col}" stroke-width="1.6"/>')


def sake(x, y, s=1.0, col='#a8d5b5'):
    # 一升瓶：標籤留白
    return (f'<rect x="{x+9*s}" y="{y-6*s}" width="{10*s}" height="{8*s}" rx="1" fill="{GOLD}" stroke-width="1.4"/>'
            f'<path d="M{x+9*s},{y+2*s} L{x+9*s},{y+14*s} q{-9*s},{8*s} {-9*s},{20*s} L{x},{y+70*s} q0,{4*s} {4*s},{4*s} '
            f'L{x+24*s},{y+74*s} q{4*s},0 {4*s},{-4*s} L{x+28*s},{y+34*s} q0,{-12*s} {-9*s},{-20*s} L{x+19*s},{y+2*s} Z" fill="{col}" stroke-width="1.8"/>'
            f'<rect x="{x+4*s}" y="{y+38*s}" width="{20*s}" height="{26*s}" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
            f'<path d="M{x+9*s},{y+44*s} L{x+9*s},{y+58*s} M{x+15*s},{y+44*s} L{x+15*s},{y+54*s}" stroke-width="1.2" opacity=".5"/>')


def robot(x, y, s=1.0, col=SKY):
    return (f'<path d="M{x+14*s},{y-10*s} L{x+14*s},{y}" stroke-width="1.6"/><circle cx="{x+14*s}" cy="{y-12*s}" r="{3*s}" fill="{RED}" stroke-width="1.2"/>'
            f'<rect x="{x}" y="{y}" width="{28*s}" height="{22*s}" rx="{5*s}" fill="{col}"/>'
            + face(x + 14 * s, y + 10 * s, .55 * s)
            + f'<rect x="{x+2*s}" y="{y+24*s}" width="{24*s}" height="{22*s}" rx="{4*s}" fill="{col}"/>'
            f'<rect x="{x+9*s}" y="{y+30*s}" width="{10*s}" height="{8*s}" rx="2" fill="{GOLD}" stroke-width="1.2"/>')


def phone(x, y, s=1.0, col=NAVY, screen=WHITE, bars=True):
    t = (f'<rect x="{x}" y="{y}" width="{40*s}" height="{70*s}" rx="{7*s}" fill="{col}"/>'
         f'<rect x="{x+4*s}" y="{y+8*s}" width="{32*s}" height="{54*s}" rx="2" fill="{screen}" stroke-width="1.4"/>')
    if bars:
        for i, bw in enumerate([1.5, 1, 2.2, 1, 1.4, 2, 1, 1.6, 1, 2.2, 1.2]):
            t += f'<rect x="{x+(8+i*2.3)*s:.1f}" y="{y+30*s:.1f}" width="{bw*s:.1f}" height="{16*s:.1f}" fill="{INK}" stroke="none"/>'
        t += f'<rect x="{x+8*s:.1f}" y="{y+14*s:.1f}" width="{24*s:.1f}" height="{10*s:.1f}" rx="2" fill="{PINK}" stroke-width="1.2"/>'
    return t


def passport(x, y, s=1.0, col='#3b5a8c'):
    # 護照：只畫一個圓，不畫任何國徽
    return (f'<rect x="{x}" y="{y}" width="{34*s}" height="{46*s}" rx="{4*s}" fill="{col}"/>'
            f'<circle cx="{x+17*s}" cy="{y+20*s}" r="{8*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+9*s},{y+36*s} L{x+25*s},{y+36*s}" stroke="{GOLD}" stroke-width="1.8"/>')


def suitcase(x, y, s=1.0, col=ORANGE):
    return (f'<rect x="{x+12*s}" y="{y-10*s}" width="{16*s}" height="{12*s}" rx="3" fill="none" stroke-width="2.4"/>'
            f'<rect x="{x}" y="{y}" width="{40*s}" height="{54*s}" rx="{7*s}" fill="{col}"/>'
            f'<path d="M{x+13*s},{y+6*s} L{x+13*s},{y+48*s} M{x+27*s},{y+6*s} L{x+27*s},{y+48*s}" stroke-width="1.6"/>'
            f'<circle cx="{x+8*s}" cy="{y+58*s}" r="{3.5*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+32*s}" cy="{y+58*s}" r="{3.5*s}" fill="{INK}" stroke="none"/>')


def basket(x, y, s=1.0, col=RED):
    return (f'<path d="M{x+6*s},{y} q{24*s},{-26*s} {48*s},0" fill="none" stroke-width="3"/>'
            f'<path d="M{x},{y} L{x+60*s},{y} L{x+54*s},{y+30*s} L{x+6*s},{y+30*s} Z" fill="{col}"/>'
            + ''.join(f'<path d="M{x+(12+i*12)*s},{y+4*s} L{x+(12+i*12)*s},{y+26*s}" stroke-width="1.4" opacity=".6"/>' for i in range(4)))


def tag(x, y, col=GOLD, s=1.0):
    # 價格標籤：不寫數字
    return (f'<path d="M{x},{y} L{x+30*s},{y} L{x+42*s},{y+12*s} L{x+30*s},{y+24*s} L{x},{y+24*s} Z" fill="{col}" stroke-width="1.8"/>'
            f'<circle cx="{x+31*s}" cy="{y+12*s}" r="{3*s}" fill="{WHITE}" stroke-width="1.4"/>')


def nope(x, y, r=14):
    # 紅色禁止圈
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{RED}" stroke-width="4"/>'
            f'<path d="M{x-r*.7:.1f},{y+r*.7:.1f} L{x+r*.7:.1f},{y-r*.7:.1f}" stroke="{RED}" stroke-width="4"/>')


def ok(x, y, r=12):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREEN}"/>'
            f'<path d="M{x-r*.45:.1f},{y} L{x-r*.1:.1f},{y+r*.4:.1f} L{x+r*.5:.1f},{y-r*.4:.1f}" stroke="{WHITE}" stroke-width="3" fill="none"/>')


def wifi(x, y, s=1.0, col=TEAL):
    return (f'<circle cx="{x}" cy="{y}" r="{3*s}" fill="{col}" stroke="none"/>'
            + ''.join(f'<path d="M{x-r*s:.1f},{y-r*.4*s:.1f} q{r*s:.1f},{-r*1.1*s:.1f} {2*r*s:.1f},0" fill="none" stroke="{col}" stroke-width="3"/>'
                      for r in (9, 16, 23)))


def register(x, y, s=1.0, col=GRAY):
    return (f'<rect x="{x}" y="{y+20*s}" width="{60*s}" height="{30*s}" rx="4" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+20*s} L{x+16*s},{y} L{x+44*s},{y} L{x+50*s},{y+20*s} Z" fill="{WHITE}"/>'
            f'<rect x="{x+20*s}" y="{y+4*s}" width="{20*s}" height="{8*s}" rx="1" fill="{SKY}" stroke-width="1.2"/>'
            + ''.join(f'<rect x="{x+(8+i*12)*s}" y="{y+28*s}" width="{8*s}" height="{6*s}" rx="1" fill="{WHITE}" stroke-width="1"/>' for i in range(4)))


def calendar(x, y, w=70, h=64, marks=(), col=RED):
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{WHITE}"/>'
         f'<path d="M{x},{y+14} L{x+w},{y+14}" stroke-width="1.6"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="6" fill="{col}"/>'
         f'<path d="M{x+14},{y-5} L{x+14},{y+6} M{x+w-14},{y-5} L{x+w-14},{y+6}" stroke-width="2.6"/>')
    cw, ch = w / 7, (h - 18) / 5
    for r in range(5):
        for c in range(7):
            cx, cy = x + cw * c + cw / 2, y + 18 + ch * r + ch / 2
            if (r, c) in marks:
                t += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{min(cw,ch)/2+.5:.1f}" fill="{GOLD}" stroke-width="1.2"/>'
            else:
                t += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.3" fill="{INK}" stroke="none" opacity=".45"/>'
    return t


def arrow(x1, y1, x2, y2, col=RED, w=3):
    import math as _m
    a = _m.atan2(y2 - y1, x2 - x1)
    l = 8
    p1 = (x2 - l * _m.cos(a - .5), y2 - l * _m.sin(a - .5))
    p2 = (x2 - l * _m.cos(a + .5), y2 - l * _m.sin(a + .5))
    return (f'<path d="M{x1},{y1} L{x2},{y2} M{p1[0]:.1f},{p1[1]:.1f} L{x2},{y2} L{p2[0]:.1f},{p2[1]:.1f}" '
            f'stroke="{col}" stroke-width="{w}" fill="none"/>')


def shelf(x, y, w, n=2, gap=34, col=BROWN):
    return ''.join(f'<rect x="{x}" y="{y+gap*i}" width="{w}" height="6" rx="2" fill="{col}"/>' for i in range(n))


# 1. 車站前的藥妝店
card('store', '手繪車站前燈很亮的藥妝店，店外擺著貨架',
     floor(152, '#e9e2ec')
     + shop(30, 24, 180, 128, '#fff8fa', PINK, MINT, '#ffd6dc')
     + f'<rect x="38" y="84" width="58" height="62" rx="3" fill="#fdfbf4"/><rect x="144" y="84" width="58" height="62" rx="3" fill="#fdfbf4"/>'
     + shelf(38, 108, 58, 2, 22) + shelf(144, 108, 58, 2, 22)
     + lipstick(44, 102, RED, .45) + jar(58, 92, PINK, .4, False) + pump(82, 90, MINT, .4)
     + eyedrop(48, 116, SKY, .38) + tube(64, 124, MINT, .35)
     + pillbox(150, 92, 16, 12) + pillbox(172, 94, 14, 10, '#fff4e0', GREEN)
     + candy(158, 122, GOLD, .4) + snack(176, 112, PINK, .3, False)
     + ''.join(f'<path d="M{x},18 L{x},10" stroke="{GOLD}" stroke-width="2"/>' for x in (60, 120, 180))
     + sparkle(18, 40) + star(224, 40, 5))

# 2. 化妝品與保養品
card('cosme', '手繪口紅、乳霜、化妝水和面膜',
     floor(150, '#f8e6ec')
     + pump(24, 76, PINK, 1.15)
     + lipstick(62, 100, RED, 1.2) + lipstick(88, 104, '#e88aa0', 1.0)
     + jar(116, 96, LAV, 1.15)
     + f'<rect x="168" y="70" width="46" height="66" rx="6" fill="{MINT}"/>'
     + f'<ellipse cx="191" cy="98" rx="14" ry="18" fill="{WHITE}" stroke-width="1.6"/>' + face(191, 98, .6)
     + sparkle(40, 40) + star(140, 44, 7) + sparkle(220, 48))

# 3. 藥品
card('medicine', '手繪藥盒、眼藥水和溫度計',
     floor(150, '#e4f1ec')
     + pillbox(22, 100, 46, 40, WHITE, RED) + pillbox(78, 108, 34, 30, '#fff4e0', GREEN)
     + eyedrop(126, 88, SKY, 1.3) + eyedrop(150, 96, PINK, 1.1)
     + f'<rect x="180" y="72" width="14" height="60" rx="7" fill="{WHITE}"/><circle cx="187" cy="136" r="9" fill="{RED}"/><path d="M187,84 L187,128" stroke="{RED}" stroke-width="3"/>'
     + sparkle(36, 44) + star(110, 48, 7) + sparkle(214, 50))

# ---- 提醒卡 ----
rem('r-baby', '手繪提醒：尿布和嬰兒食品不打折',
    f'<path d="M14,44 L58,44 L54,64 q-18,20 -36,0 Z" fill="{WHITE}"/>'
    + f'<path d="M14,44 L58,44" stroke-width="2.4"/>' + face(36, 54, .5)
    + f'<rect x="66" y="40" width="30" height="40" rx="6" fill="{PEACH}"/><rect x="64" y="34" width="34" height="10" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
    + nope(60, 60, 50))

rem('r-pharmacist', '手繪提醒：藥師不在的時候，有些藥買不到',
    f'<rect x="12" y="62" width="96" height="40" rx="4" fill="{BROWN}"/>'
    + f'<rect x="20" y="26" width="30" height="36" rx="4" fill="{WHITE}" stroke-dasharray="4 4"/>'
    + f'<circle cx="35" cy="38" r="7" fill="none" stroke-dasharray="3 3"/>'
    + pillbox(66, 40, 28, 22, WHITE, RED) + nope(80, 50, 18))

rem('r-outlet', '手繪提醒：Outlet 之類的部分分店不能用',
    shop(22, 28, 76, 72, '#f2f2f2', GRAY, WHITE, GRAY, smile=False)
    + phone(84, 58, .45) + nope(94, 34, 13))


print(save(F, OUT), 'files')
