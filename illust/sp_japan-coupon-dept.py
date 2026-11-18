# 購物折扣總覽 2026-11-18 新增的百貨（三越伊勢丹、阪急阪神、西武・SOGO、高島屋、小田急、京王）的插圖與提醒卡。
# 畫法沿用大丸那支（sp_japan-coupon-daimaru.py）的小工具：百貨外觀不描任何一家分店，
# 招牌、旗子留白，不畫商標與精品品牌。說明文字在 illust/spots/japan-coupon-<slug>.json。
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kit import *

# 借用大丸那支的繪圖函式：只執行到第一張圖之前（後面那段會畫圖並存檔）
_src = open(os.path.join(HERE, 'sp_japan-coupon-daimaru.py'), encoding='utf-8').read()
exec(_src[:_src.index('# 1. 百貨公司外觀')])

W, H = 240, 180


def build(name, label, inner, bg=CREAM, w=W, h=H):
    return svg(name, w, h, label, inner, bg=bg)


def building_svg(pfx, flags=(RED, NAVY), people=(PINK, TEAL)):
    return build(pfx + 'building', '手繪百貨公司外觀，有圓柱、旗子和大門',
        f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f2fb"/>'
        + floor(152, '#e2dccf')
        + f'<rect x="26" y="34" width="188" height="118" rx="4" fill="{STONE}"/>'
        + f'<rect x="20" y="28" width="200" height="12" rx="3" fill="#d9c8ad"/>'
        + f'<rect x="70" y="10" width="100" height="18" rx="5" fill="{WHITE}"/>' + face(120, 19, .55, blush=False)
        + ''.join(f'<rect x="{36+i*44}" y="50" width="34" height="22" rx="2" fill="{SKY}" stroke-width="1.6"/>' for i in range(4))
        + ''.join(f'<rect x="{36+i*44}" y="80" width="34" height="22" rx="2" fill="{SKY}" stroke-width="1.6"/>' for i in range(4))
        + ''.join(f'<rect x="{x}" y="108" width="10" height="44" rx="2" fill="#f7efe2"/>' for x in (44, 80, 150, 186))
        + f'<rect x="96" y="112" width="48" height="40" rx="3" fill="#fff3c4"/><path d="M120,112 L120,152" stroke-width="1.6"/>'
        + flag(14, 46, flags[0]) + flag(206, 46, flags[1])
        + person(64, 128, people[0], .8) + person(172, 128, people[1], .8, INK)
        + sparkle(226, 22) + sparkle(18, 22), bg='#e6f2fb')


def counter_svg(pfx, item):
    # 免稅櫃台：旅客拿出護照，櫃台人員遞出 item（紙本券或卡）
    return build(pfx + 'counter', '手繪免稅櫃台，旅客拿出護照，櫃台人員遞出券或卡',
        floor(152)
        + f'<rect x="20" y="96" width="200" height="56" rx="6" fill="#d9c8ad"/>'
        + f'<rect x="20" y="90" width="200" height="10" rx="3" fill="{STONE}"/>'
        + person(150, 50, NAVY, 1.4) + f'<rect x="143" y="70" width="14" height="16" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
        + person(64, 66, PINK, 1.5)
        + passport(86, 72, .6) + item
        + f'<rect x="96" y="20" width="48" height="18" rx="5" fill="{WHITE}"/>' + passport(110, 23, .25)
        + sparkle(206, 30) + star(30, 30, 6))


def appphone(x, y, s=1.0):
    # 手機上是 App 畫面：上排小圖示、中間一張券
    t = (f'<rect x="{x}" y="{y}" width="{40*s}" height="{70*s}" rx="{7*s}" fill="{NAVY}"/>'
         f'<rect x="{x+4*s}" y="{y+8*s}" width="{32*s}" height="{54*s}" rx="2" fill="{WHITE}" stroke-width="1.4"/>')
    t += ''.join(f'<rect x="{x+(7+i*9)*s:.1f}" y="{y+12*s:.1f}" width="{6*s:.1f}" height="{6*s:.1f}" rx="1.5" fill="{c}" stroke-width="1"/>'
                 for i, c in enumerate((PINK, GOLD, MINT)))
    t += ticket(x + 7 * s, y + 26 * s, .45 * s, LAV)
    return t


def qrphone(x, y, s=1.0):
    # 手機畫面上是一個不能掃的示意格子（只畫三個定位方塊與幾格）
    t = (f'<rect x="{x}" y="{y}" width="{40*s}" height="{70*s}" rx="{7*s}" fill="{NAVY}"/>'
         f'<rect x="{x+4*s}" y="{y+8*s}" width="{32*s}" height="{54*s}" rx="2" fill="{WHITE}" stroke-width="1.4"/>')
    bx, by, c = x + 8 * s, y + 18 * s, 24 * s
    for dx, dy in ((0, 0), (c - 8 * s, 0), (0, c - 8 * s)):
        t += f'<rect x="{bx+dx:.1f}" y="{by+dy:.1f}" width="{8*s:.1f}" height="{8*s:.1f}" fill="{INK}" stroke="none"/>'
    for i, j in ((10, 2), (14, 6), (11, 12), (17, 14), (13, 18), (19, 19), (4, 12)):
        t += f'<rect x="{bx+i*s:.1f}" y="{by+j*s:.1f}" width="{3*s:.1f}" height="{3*s:.1f}" fill="{INK}" stroke="none"/>'
    return t


def watch(x, y, s=1.0):
    return (f'<rect x="{x-6*s}" y="{y-26*s}" width="{12*s}" height="{52*s}" rx="{4*s}" fill="{BROWN}"/>'
            f'<circle cx="{x}" cy="{y}" r="{14*s}" fill="{GOLD}"/>'
            f'<circle cx="{x}" cy="{y}" r="{10*s}" fill="{WHITE}" stroke-width="1.4"/>'
            f'<path d="M{x},{y} L{x},{y-7*s} M{x},{y} L{x+5*s},{y+2*s}" stroke-width="1.8"/>')


def ring(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{12*s}" fill="none" stroke="{GOLD}" stroke-width="{5*s}"/>'
            f'<circle cx="{x}" cy="{y}" r="{12*s}" fill="none" stroke-width="1.4"/>'
            f'<path d="M{x-7*s},{y-14*s} L{x},{y-24*s} L{x+7*s},{y-14*s} Z" fill="{SKY}" stroke-width="1.6"/>')


def handbag(x, y, s=1.0, col=BRICK):
    return (f'<path d="M{x+10*s},{y} q{12*s},{-22*s} {24*s},0" fill="none" stroke-width="3"/>'
            f'<path d="M{x},{y} L{x+44*s},{y} L{x+40*s},{y+34*s} L{x+4*s},{y+34*s} Z" fill="{col}"/>'
            f'<rect x="{x+18*s}" y="{y+8*s}" width="{8*s}" height="{6*s}" rx="1" fill="{GOLD}" stroke-width="1.2"/>')


def luxury_svg(pfx, label):
    # 精品、鐘錶、珠寶與食品不折
    return build(pfx + 'luxury', label,
        floor(150, '#f3ecf3')
        + f'<rect x="18" y="92" width="204" height="58" rx="6" fill="{WHITE}"/>'
        + f'<rect x="26" y="100" width="188" height="30" rx="3" fill="#eef7fb" stroke-width="1.4"/>'
        + watch(56, 115, .8) + ring(112, 120, .9) + handbag(150, 98, .9)
        + nope(200, 60, 18)
        + person(52, 46, LAV, 1.0) + sparkle(120, 40) + star(30, 70, 6))


def calendar7(pfx):
    # 7 天內可以重複用：一張月曆，前 7 格打勾
    cells = ''
    for i in range(14):
        cx, cy = 52 + (i % 7) * 22, 74 + (i // 7) * 26
        cells += f'<rect x="{cx-9}" y="{cy-9}" width="18" height="18" rx="3" fill="{WHITE if i >= 7 else MINT}" stroke-width="1.4"/>'
        if i < 7:
            cells += f'<path d="M{cx-5},{cy} L{cx-1},{cy+4} L{cx+5},{cy-4}" stroke="{DGREEN}" stroke-width="2.4" fill="none"/>'
    return build(pfx + 'week', '手繪月曆，連續七格打勾，旁邊是一張券',
        f'<rect x="36" y="38" width="168" height="104" rx="8" fill="{WHITE}"/>'
        f'<rect x="36" y="38" width="168" height="20" rx="8" fill="{RED}"/>'
        + ''.join(f'<circle cx="{x}" cy="38" r="4" fill="{WHITE}"/>' for x in (70, 170))
        + cells + paperticket(150, 140, .9) + sparkle(24, 30) + sparkle(220, 150))


def qr_svg(pfx):
    return build(pfx + 'qr', '手繪結帳櫃台，旅客把手機上的 QR code 和護照一起給店員看',
        floor(152)
        + f'<rect x="20" y="104" width="200" height="48" rx="6" fill="#d9c8ad"/>'
        + register(150, 66, .9)
        + person(196, 52, NAVY, 1.2)
        + person(56, 66, PINK, 1.5)
        + qrphone(80, 58, .8) + passport(118, 84, .55)
        + sparkle(30, 30) + star(120, 30, 6))


def app_svg(pfx):
    return build(pfx + 'app', '手繪手機 App 畫面上有一張券，旁邊是護照和免稅櫃台',
        floor(152)
        + f'<rect x="120" y="100" width="104" height="52" rx="6" fill="#d9c8ad"/>'
        + f'<rect x="120" y="94" width="104" height="10" rx="3" fill="{STONE}"/>'
        + person(172, 60, NAVY, 1.2)
        + appphone(30, 40, 1.3) + passport(92, 92, .6)
        + arrow(96, 70, 128, 70, INK, 2.4)
        + ok(196, 30, 12) + sparkle(24, 26))


def card_svg(pfx):
    # 憑護照領一張卡
    return counter_svg(pfx, creditcard(118, 74, .8, LAV))


def barphone(x, y, s=1.0):
    # 手機畫面上是一條示意條碼（粗細不一的直線，不是真的條碼）
    t = (f'<rect x="{x}" y="{y}" width="{40*s}" height="{70*s}" rx="{7*s}" fill="{NAVY}"/>'
         f'<rect x="{x+4*s}" y="{y+8*s}" width="{32*s}" height="{54*s}" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
         f'<rect x="{x+8*s}" y="{y+14*s}" width="{24*s}" height="{10*s}" rx="2" fill="{NAVY}" stroke="none"/>')
    bx = x + 8 * s
    for i, w in enumerate((2, 1, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1)):
        t += f'<rect x="{bx + i*2*s:.1f}" y="{y+30*s:.1f}" width="{w*0.8*s:.1f}" height="{18*s:.1f}" fill="{INK}" stroke="none"/>'
    return t


def barcode_svg(pfx):
    return build(pfx + 'barcode', '手繪結帳櫃台，旅客把手機上的條碼券給店員看，旁邊是一張券卡',
        floor(152)
        + f'<rect x="20" y="104" width="200" height="48" rx="6" fill="#d9c8ad"/>'
        + register(150, 66, .9)
        + person(196, 52, NAVY, 1.2)
        + person(56, 66, PINK, 1.5)
        + barphone(80, 58, .8) + paperticket(110, 112, .7)
        + sparkle(30, 30) + star(120, 30, 6))


def food_svg(pfx):
    # 食品賣場不折：便當、蛋糕、零食，旁邊一個禁止圈
    return build(pfx + 'food', '手繪食品賣場：便當、蛋糕和零食，旁邊一個禁止圈',
        floor(152)
        + f'<rect x="18" y="96" width="204" height="56" rx="6" fill="{WHITE}"/>'
        + f'<rect x="18" y="90" width="204" height="10" rx="3" fill="{STONE}"/>'
        + bento(30, 104, 1.0) + cake(96, 118, 1.1) + snack(150, 46, GOLD, .9)
        + nope(196, 34, 18) + sparkle(30, 30))


# ---- 提醒小圖 ----
def rem_svg(name, label, inner):
    return svg(name, 120, 120, label, inner, bg=YEL)


def r_item(pfx):
    return rem_svg(pfx + 'r-item', '手繪提醒：一件一件算，小東西不折',
        f'<rect x="14" y="56" width="30" height="40" rx="4" fill="{PINK}"/>'
        + f'<rect x="54" y="26" width="48" height="70" rx="6" fill="{TEAL}"/>'
        + face(78, 56, .7) + nope(29, 40, 11) + ok(96, 22, 10))


def r_name(pfx):
    return rem_svg(pfx + 'r-name', '手繪提醒：護照和卡要同一個人',
        passport(12, 26, .9) + creditcard(58, 34, 1.0)
        + f'<path d="M46,50 L56,50" stroke-width="2.4"/>' + f'<path d="M46,56 L56,56" stroke-width="2.4"/>'
        + person(34, 84, PINK, .7) + person(82, 84, TEAL, .7, INK) + cross(58, 96, 7))


def r_sameday(pfx):
    return rem_svg(pfx + 'r-sameday', '手繪提醒：商品和當天的收據一起帶到櫃台',
        f'<rect x="12" y="18" width="46" height="40" rx="5" fill="{WHITE}"/>'
        f'<path d="M12,30 L58,30" stroke-width="1.6"/><rect x="12" y="18" width="46" height="12" rx="5" fill="{RED}"/>'
        f'<circle cx="35" cy="44" r="8" fill="{GOLD}" stroke-width="1.4"/>'
        + receipt(70, 18, .9, 4)
        + f'<path d="M30,96 L18,72 L56,72 L44,96 Z" fill="{PINK}"/><path d="M28,72 q9,-14 18,0" fill="none" stroke-width="2.4"/>'
        + ok(90, 92, 12))


def r_noreturn(pfx):
    return rem_svg(pfx + 'r-noreturn', '手繪提醒：用券買的商品不能退貨換貨',
        handbag(14, 54, .9, BRICK) + handbag(58, 60, .7, LAV)
        + f'<path d="M78,40 q14,-10 24,4" fill="none" stroke-width="2.6"/>' + arrow(96, 28, 102, 44, INK, 2.6)
        + nope(88, 84, 16) + sparkle(20, 22))


def r_points(pfx):
    return rem_svg(pfx + 'r-points', '手繪提醒：店家的點數卡和這張券不能一起用',
        creditcard(10, 40, .9, GOLD) + paperticket(68, 44, .9)
        + f'<path d="M56,54 L64,54 M60,50 L60,58" stroke-width="2.6"/>'
        + cross(60, 92, 9) + sparkle(102, 22))


def r_total(pfx):
    return rem_svg(pfx + 'r-total', '手繪提醒：購物籃裝滿一點，看總額',
        basket(26, 54, 1.1, RED)
        + f'<rect x="38" y="36" width="14" height="20" rx="3" fill="{PINK}"/>'
        + f'<rect x="56" y="30" width="16" height="26" rx="3" fill="{MINT}"/>'
        + f'<rect x="76" y="38" width="12" height="18" rx="3" fill="{GOLD}"/>'
        + ok(98, 22, 11))


def r_ask(pfx):
    return rem_svg(pfx + 'r-ask', '手繪提醒：結帳前先問店員',
        person(40, 58, PINK, 1.2) + person(88, 58, NAVY, 1.2)
        + f'<rect x="44" y="10" width="40" height="30" rx="10" fill="{WHITE}"/>'
        + f'<path d="M58,40 L54,48 L64,40" fill="{WHITE}"/>'
        + f'<path d="M58,20 q6,-6 12,0 q0,6 -6,8 L64,31" fill="none" stroke-width="2.4"/>'
        + f'<circle cx="64" cy="35" r="1.6" fill="{INK}" stroke="none"/>')


PAGES = {
    'japan-coupon-isetan-mitsukoshi': ('im-', lambda p: [
        building_svg(p, (NAVY, RED), (LAV, ORANGE)), app_svg(p),
        luxury_svg(p, '手繪精品櫃：手錶、戒指和包包，旁邊一個禁止圈'),
        r_item(p), r_name(p)]),
    'japan-coupon-hankyu': ('hk-', lambda p: [
        building_svg(p, (GREEN, RED), (PINK, TEAL)), counter_svg(p, paperticket(118, 72, .8)),
        calendar7(p), r_sameday(p), r_name(p)]),
    'japan-coupon-seibu-sogo': ('ss-', lambda p: [
        building_svg(p, (SKY, NAVY), (ORANGE, LAV)), qr_svg(p),
        luxury_svg(p, '手繪精品櫃：手錶、戒指和包包，旁邊一個禁止圈'),
        r_noreturn(p), r_points(p)]),
    'japan-coupon-takashimaya': ('tk-', lambda p: [
        building_svg(p, (RED, GOLD), (TEAL, PINK)), card_svg(p),
        luxury_svg(p, '手繪精品櫃：手錶、戒指和包包，旁邊一個禁止圈'),
        r_total(p), r_ask(p)]),
    'japan-coupon-odakyu': ('od-', lambda p: [
        building_svg(p, (SKY, RED), (PINK, TEAL)), barcode_svg(p), food_svg(p),
        r_points(p), r_total(p)]),
    'japan-coupon-keio': ('ke-', lambda p: [
        building_svg(p, (GOLD, NAVY), (ORANGE, LAV)), counter_svg(p, paperticket(118, 72, .8)), food_svg(p),
        r_points(p), r_sameday(p)]),
}

n = 0
for d, (pfx, fn) in PAGES.items():
    out = os.path.join(HERE, 'sp', d)
    files = {}
    for s in fn(pfx):
        nm = s.split('hd-', 1)[1].split('"', 1)[0][len(pfx):]
        files[nm] = s
    n += save(files, out)
print(n, 'files')
