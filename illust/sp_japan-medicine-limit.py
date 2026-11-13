# 藥妝帶多少頁（/japan-medicine-limit/）的插圖與提醒卡（2026-11-13）。
# 內容依 medicine.json（報驗稅放辦法第 4 條附表、食藥署公告，查證於 2026-10-16）畫成可愛版；
# 一律畫無品牌的素色藥盒、罐子，不畫任何藥廠或藥妝店的包裝、標誌；圖上不寫數量，數字看頁面上的表。
# 不用紅十字（受保護的標誌），藥盒上畫膠囊。
# 輸出 illust/sp/japan-medicine-limit/*.svg，說明文字在 illust/spots/japan-medicine-limit.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-medicine-limit')
W, H = 240, 180
F = {}
FLOOR = '<path d="M3,150 L237,150 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#e9dcc8"/>'


def card_(name, label, inner, bg=CREAM):
    F[name] = svg('md-' + name, W, H, label, inner, bg=bg)


def rem(name, label, inner):
    F[name] = svg('md-' + name, 120, 120, label, inner, bg='#fff3c4')


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


def capsule(x, y, s=1.0, a=RED, b=WHITE, rot=-30):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x},{y-5*s:.1f} L{x-7*s:.1f},{y-5*s:.1f} a{5*s:.1f},{5*s:.1f} 0 0 0 0,{10*s:.1f} L{x},{y+5*s:.1f} Z" fill="{a}" stroke-width="1.4"/>'
            f'<path d="M{x},{y-5*s:.1f} L{x+7*s:.1f},{y-5*s:.1f} a{5*s:.1f},{5*s:.1f} 0 0 1 0,{10*s:.1f} L{x},{y+5*s:.1f} Z" fill="{b}" stroke-width="1.4"/>'
            '</g>')


def medbox(x, y, w=50, h=34, col=SKY, smile=False):
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
         f'<path d="M{x},{y+7} L{x+w},{y+7}" stroke-width="1.4"/>'
         + capsule(x + w * .32, y + h * .6, .9))
    if smile:
        t += face(x + w * .72, y + h * .58, .55)
    return t


def jar(x, y, w=30, h=40, col=WHITE, cap=GREEN):
    return (f'<rect x="{x+3}" y="{y}" width="{w-6}" height="{h*.22:.1f}" rx="3" fill="{cap}"/>'
            f'<rect x="{x}" y="{y+h*.2:.1f}" width="{w}" height="{h*.8:.1f}" rx="6" fill="{col}"/>'
            f'<rect x="{x+4}" y="{y+h*.42:.1f}" width="{w-8}" height="{h*.32:.1f}" rx="2" fill="{CREAM}" stroke-width="1.2"/>')


# 1. 成藥：按瓶、盒的件數算，每一種與合計各有上限
card_('otc', '手繪疊起來的藥盒，旁邊的便條紙畫著計數的線',
      FLOOR
      + medbox(24, 112, 60, 38, SKY) + medbox(30, 74, 60, 38, PINK, True) + medbox(90, 112, 60, 38, '#cdeccf')
      + medbox(96, 74, 54, 38, GOLD)
      + '<rect x="166" y="46" width="56" height="70" rx="3" fill="#ffffff"/>'
      + '<path d="M172,64 L172,84 M178,64 L178,84 M184,64 L184,84 M190,64 L190,84 M168,80 L196,68" stroke-width="2"/>'
      + '<path d="M204,64 L204,84 M210,64 L210,84" stroke-width="2"/>'
      + '<path d="M172,100 L214,100" stroke-width="1.4"/>'
      + sparkle(40, 40) + star(110, 40, 6))

# 2. 保健食品：錠狀、膠囊狀也有件數上限
card_('supp', '手繪保健食品的罐子和外盒，旁邊散著幾顆膠囊',
      FLOOR
      + '<rect x="30" y="66" width="70" height="84" rx="3" fill="#f6a5ad"/>'
      + '<path d="M30,78 L100,78" stroke-width="1.4"/>' + face(65, 112, .9)
      + jar(110, 82, 40, 68, WHITE, GOLD) + jar(158, 96, 34, 54, '#dfeefa', GREEN)
      + capsule(204, 138, 1.0, GOLD, WHITE, 20) + capsule(214, 120, 1.0, GREEN, WHITE, -40)
      + sparkle(40, 40) + sparkle(200, 40))

# 3. 化妝品：自用限量 2024/7/1 公告廢止
card_('cosme', '手繪一片面膜、一罐乳霜和一支口紅',
      '<ellipse cx="74" cy="90" rx="44" ry="56" fill="#ffffff"/>'
      + '<ellipse cx="58" cy="78" rx="8" ry="5" fill="#fff6e6"/><ellipse cx="90" cy="78" rx="8" ry="5" fill="#fff6e6"/>'
      + '<path d="M64,112 q10,8 20,0" fill="none" stroke-width="2"/>'
      + '<ellipse cx="50" cy="100" rx="6" ry="3.6" fill="#f6a5ad" stroke="none" opacity=".8"/>'
      + '<ellipse cx="98" cy="100" rx="6" ry="3.6" fill="#f6a5ad" stroke="none" opacity=".8"/>'
      + '<rect x="134" y="94" width="58" height="46" rx="8" fill="#f6a5ad"/>'
      + '<rect x="130" y="80" width="66" height="18" rx="5" fill="#ffffff"/>'
      + '<rect x="204" y="96" width="18" height="44" rx="3" fill="#34416e"/>'
      + '<path d="M206,96 L206,80 L220,72 L220,96 Z" fill="#e4625a"/>'
      + sparkle(140, 40) + star(200, 40, 7) + sparkle(30, 150))

# 4. 日拋隱形眼鏡：按片數算，另有品牌與度數的限制
card_('lens', '手繪一排日拋隱形眼鏡的泡殼包裝',
      '<rect x="30" y="56" width="180" height="70" rx="8" fill="#ffffff"/>'
      + ''.join(f'<path d="M{40+i*34},62 L{70+i*34},62 L{70+i*34},120 L{40+i*34},120 Z" fill="none" stroke-width="1.2" stroke-dasharray="3 3"/>'
                f'<circle cx="{55+i*34}" cy="91" r="12" fill="#bfe3f5"/>'
                f'<path d="M{48+i*34},86 q4,-5 9,-4" fill="none" stroke="#ffffff" stroke-width="2"/>' for i in range(5))
      + medbox(92, 134, 56, 30, PINK, True)
      + sparkle(30, 30) + sparkle(210, 30) + star(200, 150, 6))

# 5. 郵寄和手提是兩套規定


def neq(x, y):
    return (f'<path d="M{x-12},{y-5} L{x+12},{y-5} M{x-12},{y+5} L{x+12},{y+5} M{x+7},{y-14} L{x-7},{y+14}" stroke-width="3.2"/>')


card_('mail', '手繪紙箱包裹和行李箱，中間是不等於的符號',
      FLOOR
      + '<rect x="24" y="80" width="78" height="68" rx="3" fill="#c48a5c"/>'
      + '<path d="M24,80 L40,64 L118,64 L102,80 Z" fill="#d9a77c"/>'
      + '<path d="M102,80 L118,64 L118,132 L102,148 Z" fill="#9a6440"/>'
      + '<rect x="54" y="80" width="18" height="68" fill="#f4c152" stroke-width="1.4"/>'
      + '<rect x="32" y="120" width="20" height="14" rx="2" fill="#ffffff" stroke-width="1.2"/>'
      + neq(140, 106)
      + suitcase(168, 82, 50, 60, PINK)
      + sparkle(40, 36) + sparkle(200, 36))

# 6. 超量的話走紅線申報
card_('channel', '手繪兩條通道，上面掛著綠色和紅色的牌子，小人推著行李走向紅色那邊',
      FLOOR
      + '<rect x="24" y="24" width="80" height="26" rx="5" fill="#6bb38a"/>'
      + '<rect x="136" y="24" width="80" height="26" rx="5" fill="#e4625a"/>'
      + '<path d="M64,50 L64,60 M176,50 L176,60" stroke-width="2"/>'
      + '<path d="M120,60 L120,150" stroke-width="2" stroke-dasharray="5 5"/>'
      + legs(172, 124, 1.3) + kid(172, 82, SKY, 1.4)
      + suitcase(196, 104, 26, 32, GOLD)
      + '<path d="M182,110 L196,112" stroke-width="3"/>'
      + sparkle(60, 100) + star(40, 130, 6))

# ---- 提醒卡的手繪小圖（120×120，黃底）----
rem('r-pack', '手繪提醒：原本的外盒打勾，分裝的小夾鏈袋打叉',
    '<rect x="10" y="30" width="46" height="60" rx="3" fill="#f6a5ad"/>'
    '<path d="M10,40 L56,40" stroke-width="1.4"/>'
    + capsule(33, 66, 1.0, GOLD, WHITE, -20)
    + okv(48, 92, 11)
    + '<rect x="66" y="40" width="42" height="50" rx="4" fill="#ffffff" opacity=".9"/>'
    '<path d="M66,50 L108,50" stroke-width="1.6"/>'
    + capsule(80, 70, .8, GOLD, WHITE, 30) + capsule(94, 78, .8, GOLD, WHITE, -40)
    + redx(102, 92, 11))

rem('r-amp', '手繪提醒：細頸的玻璃安瓿打叉',
    '<path d="M48,22 L60,22 L60,38 Q56,44 56,48 L68,60 L68,96 Q68,102 62,102 L46,102 Q40,102 40,96 L40,60 L52,48 Q52,44 48,38 Z" fill="#e6f4fb"/>'
    '<path d="M50,30 L50,36" stroke-width="1.4"/>'
    '<rect x="40" y="70" width="28" height="20" fill="#f4c152" stroke-width="1.4"/>'
    + '<path d="M44,62 L44,96" stroke="#ffffff" stroke-width="2"/>'
    + redx(88, 86, 14) + sparkle(90, 30, 5))

rem('r-cough', '手繪提醒：止咳糖漿的瓶子，放大鏡看著成分標籤',
    '<rect x="26" y="20" width="20" height="12" rx="2" fill="#ffffff"/>'
    '<path d="M28,32 L44,32 L44,40 Q58,44 58,56 L58,100 Q58,104 54,104 L18,104 Q14,104 14,100 L14,56 Q14,44 28,40 Z" fill="#c48a5c"/>'
    '<rect x="18" y="58" width="36" height="34" rx="2" fill="#ffffff"/>'
    + ''.join(f'<path d="M22,{66+i*7} L{50-i*4},{66+i*7}" stroke-width="1.2"/>' for i in range(4))
    + '<circle cx="74" cy="66" r="20" fill="#dfeefa" opacity=".85" stroke-width="3"/>'
    '<path d="M88,80 L106,100" stroke-width="7"/>'
    '<path d="M88,80 L106,100" stroke="#9a6440" stroke-width="3"/>')

print(save(F, OUT), 'files')
