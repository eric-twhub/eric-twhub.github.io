# 去日本買什麼划算頁的「排行榜上是哪幾類東西」插圖與提醒卡（2026-11-13）。
# 全部畫一般外型：手機是圓角長方形、吹風機是一般的槍型、相機是一般的小方盒、耳機是圓圓的收納盒，
# 不畫任何品牌標誌，也不照任何一款商品的造型畫。
# 說明依 gen.py 本頁內文、apple.json、dyson.json、panasonic.json（voltage），
# 以及 /japan-tax-free-2026/ 引的觀光廳旅客說明。輸出 illust/sp/japan-worth-buying/*.svg。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-worth-buying')
W, H = 240, 180
GLASS = '#e6f2fa'
LILAC = '#e7defa'
MINT = '#cdeedd'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('wb-' + name, W, H, label, inner, bg=bg)


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


def dryer(x, y, s=1.0, col=PINK):
    # 一般的槍型吹風機：圓筒機身＋出風口＋握把，朝右
    return (f'<rect x="{x+18*s}" y="{y+30*s}" width="{16*s}" height="{44*s}" rx="{7*s}" fill="{col}" transform="rotate(-12 {x+26*s} {y+52*s})"/>'
            f'<rect x="{x}" y="{y}" width="{62*s}" height="{36*s}" rx="{18*s}" fill="{col}"/>'
            f'<rect x="{x+58*s}" y="{y+6*s}" width="{14*s}" height="{24*s}" rx="{4*s}" fill="{WHITE}"/>'
            f'<circle cx="{x+16*s}" cy="{y+18*s}" r="{9*s}" fill="{WHITE}" stroke-width="1.6"/>'
            + ''.join(f'<path d="M{x+16*s},{y+18*s} L{x+16*s+7*s*c},{y+18*s+7*s*d}" stroke-width="1.2"/>' for c, d in [(1, 0), (0, 1), (-1, 0), (0, -1)])
            + face(x + 40 * s, y + 16 * s, .55 * s))


def camera(x, y, s=1.0, col=GRAY):
    return (f'<rect x="{x}" y="{y}" width="{56*s}" height="{40*s}" rx="{8*s}" fill="{col}"/>'
            f'<rect x="{x+8*s}" y="{y-8*s}" width="{16*s}" height="{10*s}" rx="{3*s}" fill="{col}"/>'
            f'<circle cx="{x+30*s}" cy="{y+20*s}" r="{13*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+30*s}" cy="{y+20*s}" r="{6*s}" fill="{SKY}" stroke-width="1.4"/>'
            f'<circle cx="{x+48*s}" cy="{y+8*s}" r="{2.6*s}" fill="{RED}" stroke="none"/>')


def gift(x, y, s=1.0, col=PINK):
    return (f'<rect x="{x}" y="{y+8*s}" width="{34*s}" height="{28*s}" rx="{3*s}" fill="{col}"/>'
            f'<rect x="{x-3*s}" y="{y}" width="{40*s}" height="{10*s}" rx="{3*s}" fill="{col}"/>'
            f'<path d="M{x+17*s},{y} L{x+17*s},{y+36*s}" stroke="{GOLD}" stroke-width="{4*s}"/>'
            f'<path d="M{x+17*s},{y} q{-12*s},{-14*s} {-14*s},{-4*s} q{2*s},{6*s} {14*s},{4*s} q{12*s},{-14*s} {14*s},{-4*s} q{-2*s},{6*s} {-14*s},{4*s}" fill="{GOLD}" stroke-width="1.6"/>')


# 1. 手機：一疊手機盒＋行李箱，旁邊一張要申報的單子
card('phone', '手繪一疊手機盒和一支手機，旁邊是行李箱和申報單',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + ''.join(f'<rect x="28" y="{y}" width="64" height="20" rx="4" fill="{WHITE}"/><path d="M32,{y+6} L88,{y+6}" stroke-width="1.2"/>' for y in (130, 110, 90))
     + phone(100, 56, 48, 94)
     + suitcase(168, 98, SKY, 1.1)
     + f'<rect x="170" y="36" width="44" height="52" rx="4" fill="{WHITE}"/>'
     + ''.join(f'<path d="M178,{y} L206,{y}" stroke-width="1.4"/>' for y in (50, 60, 70))
     + f'<path d="M178,80 L184,80" stroke="{RED}" stroke-width="2.6"/>'
     + sparkle(36, 40) + star(70, 64, 7))

# 2. 美髮：吹風機和梳子，旁邊一個打問號的禮物盒（台灣常附贈品）
card('hair', '手繪吹風機和圓梳，旁邊有個打著問號的禮物盒',
     dryer(26, 46, 1.2, PINK)
     + f'<rect x="130" y="40" width="10" height="70" rx="5" fill="{BROWN}" transform="rotate(20 135 75)"/>'
     + f'<rect x="138" y="22" width="24" height="44" rx="12" fill="{LILAC}" transform="rotate(20 150 44)"/>'
     + ''.join(f'<path d="M{140+i*4},{28+i*7} l-7,-3 M{154+i*4},{24+i*7} l7,3" stroke-width="1.4" transform="rotate(20 150 44)"/>' for i in range(5))
     + gift(176, 104, 1.1, SKY)
     + label(195, 132, '?', 18, RED)
     + sparkle(206, 40) + sparkle(30, 140, 4))

# 3. 電壓：插座旁邊兩塊牌子 100V（日本）、110V（台灣），中間一個不等號
card('volt', '手繪吹風機插頭插在插座上，旁邊寫著 100V 和 110V 兩塊牌子',
     dryer(20, 30, 1.0, GOLD)
     + f'<path d="M50,104 Q70,140 110,128" fill="none" stroke-width="2.4"/>'
     + f'<rect x="108" y="114" width="40" height="44" rx="8" fill="{WHITE}"/>'
     + f'<rect x="120" y="126" width="4" height="10" rx="1" fill="{INK}" stroke="none"/><rect x="132" y="126" width="4" height="10" rx="1" fill="{INK}" stroke="none"/>'
     + f'<rect x="134" y="28" width="46" height="26" rx="6" fill="#fde3e3"/>' + label(157, 46, '100V', 13, RED)
     + f'<rect x="170" y="74" width="46" height="26" rx="6" fill="#e0eefa"/>' + label(193, 92, '110V', 13, NAVY)
     + label(150, 22, 'JP', 10, RED) + label(193, 70, 'TW', 10, NAVY)
     + sparkle(214, 140) + star(110, 92, 6))

# 4. 相機：一般的小相機，兩個大小不同的盒子（兩地套裝內容不同）
card('camera', '手繪一台小相機，旁邊一大一小兩個盒子，裡面裝的東西不一樣',
     f'<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
     + camera(30, 60, 1.3, GRAY) + f'<rect x="58" y="112" width="18" height="38" rx="5" fill="{DBROWN}"/>'
     + f'<rect x="124" y="96" width="44" height="54" rx="4" fill="{WHITE}"/><rect x="176" y="72" width="44" height="78" rx="4" fill="{WHITE}"/>'
     + f'<path d="M124,106 L168,106 M176,82 L220,82" stroke-width="1.4"/>'
     + f'<rect x="136" y="116" width="20" height="24" rx="3" fill="{GRAY}" stroke-width="1.4"/>'
     + f'<rect x="186" y="92" width="20" height="24" rx="3" fill="{GRAY}" stroke-width="1.4"/><rect x="186" y="122" width="12" height="20" rx="3" fill="{PINK}" stroke-width="1.4"/><circle cx="210" cy="132" r="5" fill="{GOLD}" stroke-width="1.4"/>'
     + label(146, 90, 'JP', 10, RED) + label(198, 66, 'TW', 10, NAVY)
     + sparkle(30, 34) + star(110, 40, 6))

# 5. 耳機與手錶：圓圓的耳機盒、一般的方形手錶，旁邊一個「差不多」的波浪等號
card('small', '手繪圓圓的耳機收納盒和一支方形手錶，中間是差不多的波浪等號',
     f'<ellipse cx="66" cy="100" rx="42" ry="32" fill="{MINT}"/>'
     + f'<path d="M24,94 Q66,80 108,94" fill="none" stroke-width="1.8"/>'
     + f'<circle cx="52" cy="80" r="11" fill="{WHITE}"/><circle cx="80" cy="80" r="11" fill="{WHITE}"/>'
     + face(66, 110, .7)
     + f'<rect x="164" y="34" width="22" height="30" rx="6" fill="{NAVY}"/><rect x="164" y="122" width="22" height="30" rx="6" fill="{NAVY}"/>'
     + f'<rect x="150" y="62" width="50" height="62" rx="14" fill="{LILAC}"/>'
     + f'<rect x="157" y="69" width="36" height="48" rx="9" fill="{SKY}" stroke-width="1.6"/>'
     + face(175, 92, .7)
     + f'<path d="M112,86 q6,-6 12,0 t12,0 M112,98 q6,-6 12,0 t12,0" fill="none" stroke-width="2.6"/>'
     + sparkle(210, 40) + star(30, 40, 6))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label_, inner):
    F[name] = svg('wb-' + name, 120, 120, label_, inner, bg='#fff3c4')


# 先付全額：收銀機吐出一張長長的收據，錢包空空
rem('r-payfirst', '手繪提醒：收銀機吐出收據，退款的錢幣要等到坐飛機之後才回來',
    f'<rect x="12" y="52" width="56" height="44" rx="6" fill="{GRAY}"/>'
    + f'<rect x="20" y="60" width="40" height="12" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
    + ''.join(f'<circle cx="{x}" cy="84" r="2.2" fill="{INK}" stroke="none"/>' for x in (24, 34, 44, 54))
    + f'<path d="M30,52 L30,18 L52,18 L52,52" fill="{WHITE}"/>'
    + ''.join(f'<path d="M35,{y} L47,{y}" stroke-width="1.3"/>' for y in (26, 33, 40))
    + f'<g transform="translate(92,30) rotate(-20)"><path d="M-16,0 L16,0 Q22,0 22,3 Q22,6 16,6 L-16,6 Z" fill="{WHITE}"/>'
      f'<path d="M-3,3 L-10,-10 L-5,-10 L7,3 Z M-3,5 L-8,16 L-3,16 L7,5 Z" fill="{SKY}"/></g>'
    + f'<path d="M96,48 Q104,76 84,92" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="4 4"/>'
    + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="3.6" fill="{GOLD}"/>' for x, y in [(82, 104), (82, 98), (98, 106)]))

# 電壓：吹風機插頭和一個寫著 INPUT 的小標籤，放大鏡
rem('r-volt', '手繪提醒：放大鏡看插頭旁邊的 INPUT 電壓標示',
    f'<rect x="14" y="24" width="58" height="40" rx="5" fill="{WHITE}"/>'
    + label(43, 40, 'INPUT', 10) + label(43, 56, '100V', 12, RED)
    + f'<path d="M72,44 Q92,50 88,80" fill="none" stroke-width="2.2"/>'
    + f'<rect x="76" y="80" width="24" height="18" rx="4" fill="{GOLD}"/>'
    + f'<path d="M82,98 L82,108 M94,98 L94,108" stroke-width="2.6"/>'
    + f'<circle cx="38" cy="86" r="14" fill="{GLASS}" stroke-width="2.4"/><path d="M48,96 L60,108" stroke-width="5"/>'
    + label(38, 92, '?', 14, RED))

# 收據連坐：一張收據上一半是零食，被咬了一口的那包打叉
rem('r-receipt', '手繪提醒：同一張收據上的零食被吃了一包，整張打叉',
    f'<path d="M14,16 L66,16 L66,100 L61,96 L56,100 L51,96 L46,100 L41,96 L36,100 L31,96 L26,100 L21,96 L14,100 Z" fill="{WHITE}"/>'
    + f'<rect x="22" y="26" width="18" height="24" rx="3" fill="{PINK}" stroke-width="1.6"/>'
    + f'<rect x="44" y="26" width="16" height="24" rx="3" fill="{GOLD}" stroke-width="1.6"/>'
    + f'<path d="M60,30 q-5,2 -4,7 q-5,1 -4,6" fill="#fff" stroke-width="1.6"/>'
    + ''.join(f'<path d="M22,{y} L58,{y}" stroke-width="1.3"/>' for y in (62, 72, 82))
    + cross(92, 56, 1.1))

print(save(F, OUT), 'files')
