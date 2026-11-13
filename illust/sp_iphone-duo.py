# iPhone Duo 頁的「買一支回台灣要過的幾關」插圖與提醒卡（2026-11-13）。
# 手機畫一般圓角長方形，不畫蘋果標誌、不畫機身設計（Duo 的外型不畫，不猜）；店面不畫招牌。
# 說明依 apple.json（預約時間）、gen.py 本頁與台日 Apple 價差頁的常見問題，
# 以及 /japan-tax-free-2026/ 引的觀光廳旅客說明。輸出 illust/sp/iphone-duo/*.svg。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'iphone-duo')
W, H = 240, 180
GLASS = '#e6f2fa'
LILAC = '#e7defa'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('du-' + name, W, H, label, inner, bg=bg)


def phone(x, y, w=44, h=80, body=LILAC, scr=SKY, smile=True):
    # 一般的圓角長方形手機：外殼＋螢幕＋上方一條小膠囊，不畫任何品牌細節
    r = w * .2
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r:.1f}" fill="{body}"/>'
         f'<rect x="{x+4}" y="{y+5}" width="{w-8}" height="{h-10}" rx="{r*.7:.1f}" fill="{scr}" stroke-width="1.6"/>'
         f'<rect x="{x+w/2-5:.1f}" y="{y+8}" width="10" height="3" rx="1.5" fill="{INK}" stroke="none"/>')
    if smile:
        t += face(x + w / 2, y + h * .52, .7 * w / 44)
    return t


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-6*s},{y-1*s} q{6*s},{-10*s} {12*s},0 q{-6*s},{-4*s} {-12*s},0 Z" fill="{hair}" stroke-width="1.4"/>')


def passport(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{28*s}" height="{38*s}" rx="{3*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+14*s}" cy="{y+17*s}" r="{6.5*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+8*s},{y+31*s} L{x+20*s},{y+31*s}" stroke="{GOLD}" stroke-width="1.6"/>')


def suitcase(x, y, col=SKY, s=1.0):
    return (f'<path d="M{x+10*s},{y} L{x+10*s},{y-8*s} L{x+22*s},{y-8*s} L{x+22*s},{y}" fill="none" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{32*s}" height="{40*s}" rx="{5*s}" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+4*s} L{x+10*s},{y+36*s} M{x+22*s},{y+4*s} L{x+22*s},{y+36*s}" stroke-width="1.4" opacity=".6"/>'
            f'<circle cx="{x+6*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+26*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>')


def floor(y=150, col='#e9dcc8'):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def check(x, y, s=1.0, col=GREEN):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{col}"/>'
            f'<path d="M{x-5*s},{y} L{x-1*s},{y+4*s} L{x+6*s},{y-5*s}" fill="none" stroke="{WHITE}" stroke-width="3"/>')


def cross(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{RED}"/>'
            f'<path d="M{x-5*s},{y-5*s} L{x+5*s},{y+5*s} M{x+5*s},{y-5*s} L{x-5*s},{y+5*s}" stroke="{WHITE}" stroke-width="3"/>')


def label(x, y, txt, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="bold" '
            f'text-anchor="middle" fill="{col}" stroke="none">{txt}</text>')


def clock(x, y, r, hh, mm, col=WHITE):
    import math
    ah = math.radians((hh % 12 + mm / 60) * 30 - 90)
    am = math.radians(mm * 6 - 90)
    t = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'
    t += ''.join(f'<circle cx="{x + r*.78*math.cos(math.radians(i*30)):.1f}" cy="{y + r*.78*math.sin(math.radians(i*30)):.1f}" r="1.6" fill="{INK}" stroke="none"/>' for i in range(12))
    t += (f'<path d="M{x},{y} L{x + r*.45*math.cos(ah):.1f},{y + r*.45*math.sin(ah):.1f}" stroke-width="3"/>'
          f'<path d="M{x},{y} L{x + r*.68*math.cos(am):.1f},{y + r*.68*math.sin(am):.1f}" stroke-width="2.2"/>'
          f'<circle cx="{x}" cy="{y}" r="2.6" fill="{RED}" stroke="none"/>')
    return t


def box(x, y, w=40, h=56, col=WHITE):
    # 一般的白色手機盒，蓋子上只畫一支手機的輪廓
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{col}"/>'
            f'<path d="M{x},{y+8} L{x+w},{y+8}" stroke-width="1.4"/>'
            f'<rect x="{x+w*.3:.1f}" y="{y+16}" width="{w*.4:.1f}" height="{h-26}" rx="4" fill="{LILAC}" stroke-width="1.4"/>')


# 1. 日本 21:00 和台灣 20:00 是同一時刻：兩個時鐘＋一條等號
card('clocks', '手繪兩個時鐘，日本 21 點和台灣 20 點中間畫上等號',
     f'<rect x="20" y="30" width="86" height="110" rx="14" fill="#fde3e3"/>'
     + f'<rect x="134" y="30" width="86" height="110" rx="14" fill="#e0eefa"/>'
     + clock(63, 82, 30, 9, 0) + clock(177, 82, 30, 8, 0)
     + label(63, 132, '21:00', 14) + label(177, 132, '20:00', 14)
     + label(63, 46, 'JP', 11, RED) + label(177, 46, 'TW', 11, NAVY)
     + f'<path d="M110,78 L130,78 M110,88 L130,88" stroke-width="3.4"/>'
     + sparkle(120, 40, 5) + star(120, 150, 7))

# 2. 量販店結帳：櫃台上一個手機盒、護照、TAX FREE 小立牌
card('counter', '手繪量販店收銀台，上面有手機盒、護照和 TAX FREE 小立牌',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + f'<rect x="14" y="104" width="212" height="46" rx="4" fill="{BROWN}"/>'
     + f'<path d="M14,116 L226,116" stroke-width="1.4" opacity=".5"/>'
     + box(40, 50, 44, 54) + passport(100, 66, 1.0)
     + f'<rect x="146" y="64" width="64" height="26" rx="6" fill="{WHITE}"/>'
     + f'<path d="M160,90 L156,104 M196,90 L200,104" stroke-width="2"/>'
     + label(178, 82, 'TAX FREE', 11, RED)
     + sparkle(24, 30) + sparkle(214, 34, 4) + star(120, 30, 6))

# 3. 出境時在免稅手續機台刷護照
card('kiosk', '手繪機場的免稅手續機台，旅客拿著護照，行李箱還在身邊沒託運',
     f'<path d="M3,148 L237,148 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e3e8ef"/>'
     + f'<rect x="40" y="40" width="58" height="108" rx="10" fill="{WHITE}"/>'
     + f'<rect x="48" y="50" width="42" height="32" rx="4" fill="{SKY}"/>'
     + passport(58, 54, .5) + f'<path d="M78,60 L84,60 M78,66 L86,66 M78,72 L84,72" stroke-width="1.4"/>'
     + f'<rect x="52" y="92" width="34" height="8" rx="3" fill="{GRAY}"/>'
     + f'<circle cx="69" cy="116" r="7" fill="{GREEN}"/>'
     + person(128, 108, PINK, 1.3, INK)
     + suitcase(158, 104, GOLD, .95)
     + check(72, 28, .9)
     + sparkle(24, 30) + sparkle(200, 36, 5))

# 4. 回台灣入境：綠色免申報、紅色應申報兩條通道，提著行李走紅色那條
card('redline', '手繪入境的兩條通道，綠色免申報、紅色應申報，旅客拉著行李走紅色那條',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e3e8ef"/>'
     + f'<rect x="24" y="24" width="84" height="26" rx="6" fill="{GREEN}"/>'
     + f'<rect x="132" y="24" width="84" height="26" rx="6" fill="{RED}"/>'
     + f'<path d="M50,37 L58,44 L74,30" fill="none" stroke="{WHITE}" stroke-width="3.4"/>'
     + f'<rect x="160" y="30" width="28" height="14" rx="2" fill="{WHITE}" stroke-width="1.6"/>'
     + f'<path d="M165,35 L183,35 M165,39 L178,39" stroke-width="1.2"/>'
     + f'<path d="M66,50 L66,150 M174,50 L174,150" stroke-width="2" stroke-dasharray="4 6"/>'
     + f'<path d="M120,60 L120,150" stroke-width="3"/>'
     + person(178, 98, SKY, 1.4)
     + suitcase(196, 112, PINK, .8)
     + f'<path d="M150,128 L150,96 M142,106 L150,94 L158,106" fill="none" stroke="{RED}" stroke-width="3"/>'
     + person(70, 100, GOLD, 1.2, INK) + sparkle(96, 80, 4))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label_, inner):
    F[name] = svg('du-' + name, 120, 120, label_, inner, bg='#fff3c4')


# 結帳先付全額：一張收據寫著全額、錢包打開，鐘表示要等
rem('r-payfirst', '手繪提醒：先付全額的收據，退款要等到出境之後',
    f'<path d="M14,18 L60,18 L60,96 L55,92 L50,96 L45,92 L40,96 L35,92 L30,96 L25,92 L20,96 L14,92 Z" fill="{WHITE}"/>'
    + ''.join(f'<path d="M22,{y} L52,{y}" stroke-width="1.4"/>' for y in (32, 42, 52))
    + f'<path d="M22,70 L52,70" stroke="{RED}" stroke-width="3"/>'
    + f'<rect x="64" y="58" width="44" height="32" rx="6" fill="{PINK}"/>'
    + f'<path d="M64,68 L108,68" stroke-width="1.4"/><circle cx="98" cy="78" r="3" fill="{GOLD}" stroke-width="1.2"/>'
    + clock(88, 32, 16, 4, 0))

# 整張收據連坐：收據上的手機、充電線、殼，少一件就整張打叉
rem('r-receipt', '手繪提醒：同一張收據的東西少一件就整張不退',
    f'<rect x="12" y="20" width="56" height="84" rx="4" fill="{WHITE}"/>'
    + phone(20, 30, 16, 28, smile=False)
    + f'<path d="M44,34 q10,0 10,10 q0,10 10,10" fill="none" stroke-width="2.4"/>'
    + f'<rect x="22" y="66" width="14" height="22" rx="4" fill="{SKY}"/>'
    + f'<rect x="44" y="66" width="14" height="22" rx="4" fill="none" stroke-dasharray="3 3" stroke-width="1.8"/>'
    + f'<path d="M48,74 q3,-4 6,0 q0,4 -3,6 M51,84 l0,0.1" fill="none" stroke-width="1.8"/>'
    + cross(92, 60, 1.1))

print(save(F, OUT), 'files')
