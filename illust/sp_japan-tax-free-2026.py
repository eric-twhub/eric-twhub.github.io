# 免稅新制頁（/japan-tax-free-2026/）的「退稅那天會經過這幾步」插圖與提醒卡（2026-11-13）。
# 流程依觀光廳旅客說明與問答、國稅廳線上海關確認常見問題（繁中）畫成可愛版；
# 不畫任何店家、退稅業者、機台廠商的標誌，也不畫信用卡品牌。
# 輸出 illust/sp/japan-tax-free-2026/*.svg，說明文字在 illust/spots/japan-tax-free-2026.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-tax-free-2026')
W, H = 240, 180
F = {}
FLOOR = '<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'


def card_(name, label, inner, bg=CREAM):
    F[name] = svg('tf-' + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg('tf-' + name, 120, 120, label, inner, bg='#fff3c4')


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


# 1. 結帳：出示護照，先付含稅全額
card_('pay', '手繪結帳櫃台，旅客拿出護照，收銀機吐出收據',
      FLOOR
      + '<rect x="100" y="110" width="130" height="40" fill="#c48a5c"/>'
      + '<rect x="96" y="102" width="138" height="9" rx="3" fill="#9a6440"/>'
      + receipt(184, 46, 20, 26, 2)
      + '<rect x="150" y="70" width="58" height="34" rx="5" fill="#cfd8e6"/>'
      + '<rect x="156" y="56" width="44" height="18" rx="3" fill="#dfeefa"/>'
      + ''.join(f'<rect x="{158+i*12}" y="{80+j*9}" width="8" height="5" rx="1.5" fill="{WHITE}" stroke-width="1.1"/>'
                for i in range(4) for j in range(2))
      + coin(118, 96, 7) + coin(134, 96, 7) + coin(126, 88, 7)
      + legs(56, 126, 1.4) + kid(56, 80, PINK, 1.5)
      + '<path d="M66,108 L86,104" stroke-width="3"/>'
      + passport(82, 86, 20, 26)
      + sparkle(30, 36) + star(212, 30, 6) + sparkle(120, 32))

# 2. 先別託運：帶著免稅品到出境大廳
card_('bag', '手繪報到櫃台的輸送帶上有行李箱，打上禁止符號；旁邊的人提著購物袋',
      FLOOR
      + '<rect x="142" y="66" width="86" height="52" rx="4" fill="#dfeefa"/>'
      + '<rect x="150" y="74" width="30" height="16" rx="2" fill="#ffffff" stroke-width="1.4"/>'
      + '<rect x="128" y="118" width="100" height="14" rx="7" fill="#cfd8e6"/>'
      + ''.join(f'<circle cx="{138+i*16}" cy="125" r="3" fill="{WHITE}" stroke-width="1.2"/>' for i in range(6))
      + suitcase(168, 82, 32, 33, PINK)
      + nosign(184, 98, 30)
      + legs(64, 124, 1.4) + kid(64, 78, GREEN, 1.5)
      + '<path d="M50,102 L38,118 M78,102 L90,118" stroke-width="3"/>'
      + bag(24, 118, 26, 26, GOLD) + bag(78, 118, 26, 26, PINK)
      + sparkle(30, 34) + sparkle(110, 40))

# 3. 機台刷護照，或在 7 個機場用手機
card_('kiosk', '手繪免稅手續機台，護照放在讀取處；旁邊的手機連上無線網路',
      FLOOR
      + '<rect x="104" y="36" width="66" height="114" rx="10" fill="#cfd8e6"/>'
      + '<rect x="112" y="46" width="50" height="36" rx="4" fill="#dfeefa"/>'
      + passport(127, 50, 20, 27)
      + '<rect x="112" y="94" width="50" height="16" rx="3" fill="#5b6f8f"/>'
      + '<rect x="122" y="86" width="30" height="10" rx="2" fill="#34416e" transform="rotate(-8 137 91)"/>'
      + legs(58, 126, 1.4) + kid(58, 80, RED, 1.5)
      + '<path d="M70,106 L104,98" stroke-width="3"/>'
      + phone(190, 82, 34, 58)
      + '<rect x="198" y="118" width="18" height="10" rx="3" fill="#6bb38a" stroke-width="1.2"/>'
      + ''.join(f'<path d="M{207-r},{70-r*.2:.1f} q{r},{-r*.9:.1f} {2*r},0" fill="none" stroke-width="2.2"/>' for r in (6, 11, 16))
      + '<circle cx="207" cy="70" r="2" fill="#5a3d2b" stroke="none"/>'
      + sparkle(30, 34) + sparkle(84, 40))

# 4. 綠燈就完成，紅燈去給關員看
card_('light', '手繪綠色打勾和行李箱，旁邊是紅色驚嘆號和檢查台上的購物袋',
      FLOOR
      + '<path d="M120,20 L120,168" stroke-width="1.6" stroke-dasharray="4 5"/>'
      + okv(62, 46, 22)
      + '<rect x="18" y="138" width="88" height="10" rx="5" fill="#cfd8e6"/>'
      + suitcase(44, 96, 34, 38, SKY)
      + '<circle cx="178" cy="46" r="22" fill="#e4625a"/>'
      + '<path d="M178,34 L178,50" stroke="#ffffff" stroke-width="4"/>'
      + '<circle cx="178" cy="58" r="2.6" fill="#ffffff" stroke="none"/>'
      + kid(212, 94, NAVY, 1.0)
      + '<path d="M201,88 q11,-14 22,0 Z" fill="#34416e"/>'
      + '<path d="M199,88 L225,88" stroke-width="2.4"/>'
      + '<rect x="134" y="112" width="96" height="36" rx="3" fill="#c48a5c"/>'
      + bag(140, 94, 24, 20, PINK) + bag(168, 96, 20, 18, GOLD)
      + sparkle(100, 36))

# 5. 出境後，由店家或退稅業者退款


def plane(x, y):
    return (f'<path d="M{x-30},{y-2} L{x-40},{y-18} L{x-30},{y-18} L{x-18},{y-4} Z" fill="{SKY}"/>'
            f'<path d="M{x-40},{y} q0,-10 20,-10 L{x+26},{y-10} q16,0 16,10 q0,10 -16,10 L{x-20},{y+10} q-20,0 -20,-10 Z" fill="{WHITE}"/>'
            f'<path d="M{x-6},{y+2} L{x-22},{y+22} L{x-10},{y+22} L{x+12},{y+4} Z" fill="{SKY}"/>'
            + ''.join(f'<circle cx="{x-14+i*9}" cy="{y-3}" r="2" fill="{SKY}" stroke-width="1"/>' for i in range(4))
            + f'<circle cx="{x+30}" cy="{y-2}" r="1.8" fill="{INK}" stroke="none"/>'
            + f'<path d="M{x+28},{y+4} q4,3 8,0" fill="none" stroke-width="1.4"/>')


card_('refund', '手繪飛機飛走之後，退款分成手機、卡片和硬幣三種方式回來',
      '<rect x="3" y="3" width="234" height="174" rx="22" fill="#dfeefa"/>'
      + plane(120, 40)
      + '<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'
      + '<path d="M104,62 Q70,80 52,98" fill="none" stroke-width="2" stroke-dasharray="4 5"/>'
      + '<path d="M120,64 L120,108" fill="none" stroke-width="2" stroke-dasharray="4 5"/>'
      + '<path d="M138,62 Q172,80 190,104" fill="none" stroke-width="2" stroke-dasharray="4 5"/>'
      + phone(32, 100, 34, 56) + '<circle cx="49" cy="126" r="8" fill="#f4c152" stroke-width="1.4"/>'
      + card(94, 116, 52, 34, PINK)
      + coin(178, 136, 11) + coin(202, 140, 11) + coin(190, 120, 11)
      + sparkle(30, 30) + sparkle(210, 70) + star(214, 26, 6), bg='#dfeefa')

# ---- 提醒卡的手繪小圖（120×120，黃底）----

rem('r-stamp', '手繪提醒：攤開的護照被蓋上入境章',
    '<rect x="14" y="48" width="92" height="58" rx="5" fill="#34416e"/>'
    '<rect x="18" y="52" width="41" height="50" rx="2" fill="#fff6e6" stroke-width="1.6"/>'
    '<rect x="61" y="52" width="41" height="50" rx="2" fill="#fff6e6" stroke-width="1.6"/>'
    + ''.join(f'<path d="M24,{62+i*9} L52,{62+i*9}" stroke-width="1.2"/>' for i in range(4))
    + '<circle cx="82" cy="80" r="13" fill="none" stroke="#e4625a" stroke-width="2.6"/>'
    '<circle cx="82" cy="80" r="7" fill="none" stroke="#e4625a" stroke-width="1.6"/>'
    '<ellipse cx="82" cy="16" rx="9" ry="6" fill="#9a6440"/>'
    '<rect x="78" y="20" width="8" height="14" fill="#c48a5c"/>'
    '<rect x="68" y="33" width="28" height="9" rx="2" fill="#e4625a"/>'
    '<path d="M82,46 L82,56" stroke="#e4625a" stroke-width="2" stroke-dasharray="2 3"/>')

rem('r-qr', '手繪提醒：手機上的條碼可以，截圖的照片不行',
    phone(14, 20, 44, 80)
    + qr(22, 42, 28)
    + '<rect x="66" y="44" width="40" height="32" rx="3" fill="#ffffff"/>'
    '<path d="M70,72 L82,58 L90,66 L96,60 L102,72 Z" fill="#6bb38a" stroke-width="1.4"/>'
    '<circle cx="96" cy="52" r="4" fill="#f4c152" stroke-width="1.2"/>'
    + redx(100, 82, 12))

rem('r-turn', '手繪提醒：把手機轉成橫的',
    '<rect x="20" y="52" width="80" height="44" rx="7" fill="#34416e"/>'
    '<rect x="28" y="56" width="64" height="36" rx="3" fill="#dfeefa" stroke-width="1.4"/>'
    + ''.join(f'<path d="M34,{64+i*8} L{82-i*10},{64+i*8}" stroke-width="1.3"/>' for i in range(3))
    + '<path d="M30,40 Q60,10 92,38" fill="none" stroke="#e4625a" stroke-width="3"/>'
    '<path d="M82,36 L92,38 L92,27" fill="none" stroke="#e4625a" stroke-width="3"/>')

rem('r-cert', '手繪提醒：手錶旁邊放著有金色封印的保證書',
    '<rect x="26" y="20" width="18" height="80" rx="6" fill="#c48a5c"/>'
    '<circle cx="35" cy="60" r="17" fill="#ffffff"/>'
    '<path d="M35,60 L35,49 M35,60 L43,64" stroke-width="2.2"/>'
    '<rect x="60" y="26" width="46" height="62" rx="3" fill="#ffffff"/>'
    + ''.join(f'<path d="M67,{38+i*8} L{99-(i%2)*10},{38+i*8}" stroke-width="1.3"/>' for i in range(4))
    + '<path d="M90,80 L86,100 L91,96 L95,101 L96,80 Z" fill="#e4625a" stroke-width="1.4"/>'
    '<circle cx="92" cy="78" r="9" fill="#f4c152"/>'
    + sparkle(14, 16, 4))

print(save(F, OUT), 'files')
