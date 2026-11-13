# 任天堂博物館頁的「博物館裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網的設施介紹與參觀指南（museum.nintendo.com）畫成一般的建築、展示櫃、代幣、花札與漢堡。
# 角色 IP：不畫任何遊戲角色、遊戲機或手把的外型、商標或 logo；花札畫成傳統的松、梅、櫻圖案。
# 輸出 illust/sp/japan-nintendo-museum/*.svg。說明文字放在 illust/spots/japan-nintendo-museum.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-nintendo-museum')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('nm-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def roundtree(x, base, r=14, col=GREEN, trunk=12):
    return (f'<rect x="{x-3}" y="{base-trunk}" width="6" height="{trunk}" fill="{DBROWN}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{base-trunk-r*.8:.1f}" r="{r}" fill="{col}"/>')


def fuda(x, y, kind, w=34, h=52, rot=0):
    # 一張花札：紅色底框＋傳統圖案（松、梅、櫻）
    s = f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{RED}"/>'
    s += f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="2" fill="#fbf3e4" stroke-width="1.2"/>'
    cx = x + w / 2
    if kind == 'pine':
        s += (f'<path d="M{cx},{y+h-6} L{cx},{y+22}" stroke="{DBROWN}" stroke-width="3"/>'
              f'<ellipse cx="{cx-6}" cy="{y+18}" rx="9" ry="6" fill="{DGREEN}" stroke-width="1.2"/>'
              f'<ellipse cx="{cx+6}" cy="{y+26}" rx="8" ry="5" fill="{DGREEN}" stroke-width="1.2"/>'
              f'<circle cx="{cx+4}" cy="{y+10}" r="5" fill="{RED}" stroke-width="1"/>')
    elif kind == 'plum':
        s += (f'<path d="M{x+5},{y+h-8} Q{cx},{y+24} {x+w-5},{y+12}" fill="none" stroke="{DBROWN}" stroke-width="2.4"/>'
              + ''.join(f'<circle cx="{px}" cy="{py}" r="3.6" fill="{RED}" stroke-width="1"/>' for px, py in [(cx-6, y+30), (cx+4, y+22), (cx+10, y+14)])
              + f'<rect x="{x+6}" y="{y+36}" width="{w-12}" height="8" rx="1" fill="{RED}" stroke-width="1"/>')
    else:
        s += (f'<path d="M{x+5},{y+h-6} L{x+w-5},{y+h-6}" stroke="{DBROWN}" stroke-width="2"/>'
              + ''.join(f'<circle cx="{px}" cy="{py}" r="4.4" fill="{PINK}" stroke-width="1"/>' for px, py in [(cx-7, y+14), (cx+5, y+12), (cx-2, y+22), (cx+8, y+24), (cx-8, y+30)]))
    return s + '</g>'


# 1. 由舊工廠改建的博物館
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(140, '#d6d0c4')
     + f'<rect x="28" y="62" width="184" height="78" fill="#f7f4ee"/>'
     + f'<path d="M28,62 L58,44 L58,62 L88,44 L88,62 L118,44 L118,62 L148,44 L148,62 L178,44 L178,62 L208,44 L212,62" fill="#e9e3d6" stroke-width="2"/>'
     + ''.join(f'<rect x="{x}" y="78" width="22" height="18" rx="2" fill="{SKY}" stroke-width="1.6"/>' for x in range(40, 200, 32))
     + f'<path d="M28,108 L212,108" stroke="{RED}" stroke-width="4"/>'
     + f'<rect x="104" y="114" width="32" height="26" rx="2" fill="{GRAY}"/><path d="M120,114 L120,140" stroke-width="1.6"/>'
     + roundtree(16, 140, 10, GREEN) + roundtree(226, 140, 10, GREEN)
     + person(70, 128, GOLD, .7) + person(170, 128, PINK, .7)
     + f'<text x="190" y="30" font-size="13" text-anchor="middle" fill="{DBROWN}" stroke="none" font-family="sans-serif" font-weight="bold">1969</text>'
     + sparkle(40, 26) + star(120, 24, 6))
card('factory', '手繪由舊工廠改建的白色長形建築，屋頂是鋸齒狀，旁邊寫著 1969', t, bg=SKY)

# 2. 展示櫃：從花札開始的各種產品
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#f6efe6"/>'
     + bottom(146, '#e3d7c6'))
for i, x in enumerate((18, 126)):
    t += (f'<rect x="{x}" y="34" width="96" height="104" rx="4" fill="#e3f1f8"/>'
          f'<path d="M{x},70 L{x+96},70 M{x},104 L{x+96},104" stroke-width="2"/>'
          f'<path d="M{x+8},40 L{x+20},64" stroke="{WHITE}" stroke-width="3" opacity=".8"/>')
t += (''.join(f'<rect x="{x}" y="40" width="18" height="26" rx="2" fill="{RED}"/><rect x="{x+3}" y="43" width="12" height="20" rx="1" fill="#fbf3e4" stroke-width="1"/>'
              f'<circle cx="{x+9}" cy="53" r="4" fill="{c}" stroke-width="1"/>' for x, c in [(28, DGREEN), (52, RED), (76, PINK)])
      + f'<rect x="28" y="80" width="28" height="20" rx="3" fill="{SKY}"/><path d="M30,86 L54,86" stroke-width="1.2"/>'
      + f'<rect x="64" y="76" width="22" height="24" rx="3" fill="{GOLD}"/>'
      + f'<rect x="92" y="84" width="20" height="16" rx="3" fill="{PINK}"/>'
      + f'<rect x="30" y="112" width="30" height="20" rx="4" fill="#c9b6e8"/>'
      + f'<circle cx="80" cy="122" r="10" fill="{GREEN}"/>'
      + f'<rect x="136" y="44" width="34" height="22" rx="3" fill="{WHITE}"/><path d="M140,50 L166,50 M140,56 L160,56" stroke-width="1.2"/>'
      + f'<rect x="178" y="40" width="36" height="26" rx="4" fill="{SKY}"/>'
      + f'<rect x="136" y="78" width="22" height="22" rx="11" fill="{RED}"/>'
      + f'<rect x="166" y="80" width="44" height="20" rx="4" fill="{GOLD}"/>'
      + f'<rect x="138" y="112" width="74" height="20" rx="4" fill="#b6e3c6"/>'
      + person(120, 150, SKY, .7) + sparkle(120, 20, 4))
card('display', '手繪兩座玻璃展示櫃，裡面擺著花札和各式各樣的小盒子、玩具', t, bg='#f6efe6')

# 3. 入館證裡的 10 枚代幣
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf0d8"/>'
     f'<rect x="36" y="30" width="168" height="112" rx="12" fill="{WHITE}"/>'
     f'<path d="M106,30 L106,20 M134,30 L134,20 M106,20 L134,20" stroke-width="2"/>'
     f'<rect x="48" y="44" width="60" height="10" rx="4" fill="{GRAY}" stroke-width="1.2"/>'
     f'<rect x="168" y="42" width="24" height="24" rx="3" fill="#e9e3d6" stroke-width="1.2"/>'
     + ''.join(f'<rect x="{171+a}" y="{45+b}" width="6" height="6" fill="{INK}" stroke="none"/>' for a, b in [(0, 0), (12, 0), (0, 12), (8, 8), (12, 12)]))
for k in range(10):
    cx = 64 + (k % 5) * 28
    cy = 86 + (k // 5) * 30
    t += (f'<circle cx="{cx}" cy="{cy}" r="11" fill="{GOLD}"/>'
          f'<circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke-width="1.4"/>')
t += (f'<text x="206" y="160" font-size="16" text-anchor="middle" fill="{RED}" stroke="none" font-family="sans-serif" font-weight="bold">×10</text>'
      + sparkle(24, 26) + sparkle(218, 24) + star(26, 156, 6))
card('coins', '手繪一張入館證，上面排著 10 枚金色代幣', t, bg='#fdf0d8')

# 4. 花札工作坊
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef4e2"/>'
     + bottom(130, '#d9c2a0')
     + fuda(28, 40, 'pine', 44, 66, -10) + fuda(96, 30, 'plum', 44, 66, 0) + fuda(164, 40, 'sakura', 44, 66, 10)
     # 桌上的刷子與小盒子
     + f'<path d="M40,150 L96,140" stroke="{DBROWN}" stroke-width="4"/><path d="M96,140 L110,137" stroke="{GOLD}" stroke-width="6"/>'
     + f'<rect x="140" y="138" width="60" height="26" rx="4" fill="{RED}"/><rect x="146" y="142" width="48" height="8" rx="2" fill="#fbf3e4" stroke-width="1.2"/>'
     + sparkle(120, 118) + star(30, 24, 6) + sparkle(214, 24))
card('hanafuda', '手繪三張紅框花札，畫著松、梅、櫻，桌上放著刷子和裝花札的小盒子', t, bg='#eef4e2')

# 5. 咖啡廳：自己挑配料的漢堡
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fff0dc"/>'
     + bottom(140, '#e8c9a0')
     + f'<ellipse cx="96" cy="142" rx="66" ry="10" fill="{WHITE}"/>'
     + f'<path d="M50,136 L142,136 Q142,146 130,146 L62,146 Q50,146 50,136 Z" fill="#e4a95e"/>'
     + f'<rect x="50" y="124" width="92" height="12" rx="5" fill="{DBROWN}"/>'
     + f'<path d="M48,124 q8,-8 16,0 q8,-8 16,0 q8,-8 16,0 q8,-8 16,0 q8,-8 16,0 q8,-8 16,0 L144,124 Z" fill="{GREEN}"/>'
     + f'<rect x="52" y="108" width="88" height="10" rx="4" fill="{GOLD}"/>'
     + ''.join(f'<ellipse cx="{x}" cy="104" rx="11" ry="4" fill="{RED}"/>' for x in (70, 96, 122))
     + f'<path d="M50,100 Q96,40 142,100 Z" fill="#e4a95e"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="2.4" ry="1.4" fill="{WHITE}" stroke="none"/>' for x, y in [(80, 76), (96, 68), (112, 76), (90, 86), (104, 84)])
     # 旁邊的配料小碟
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="6" fill="{WHITE}"/><circle cx="{x}" cy="{y-4}" r="6" fill="{c}"/>'
               for x, y, c in [(190, 70, RED), (196, 100, GREEN), (190, 130, GOLD)])
     + f'<path d="M160,72 L150,82 M166,102 L152,104" stroke="{RED}" stroke-width="2" stroke-dasharray="3 4"/>'
     + sparkle(30, 30) + star(214, 24, 6))
card('burger', '手繪一個疊得很高的漢堡，旁邊幾個小碟子裝著番茄、生菜、起司等配料', t, bg='#fff0dc')


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('nm-' + name, 120, 120, label, inner, bg='#fff3c4')


def qr(x, y, s=24):
    o = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
    u = s / 6
    for a, b in [(1, 1), (4, 1), (1, 4), (3, 3), (4, 4), (2, 3)]:
        o += f'<rect x="{x+a*u:.1f}" y="{y+b*u:.1f}" width="{u:.1f}" height="{u:.1f}" fill="{INK}" stroke="none"/>'
    return o


# 同行的人沒有帳號也能進：購票人出示所有人的 QR 票
rem('r-distribute', '手繪提醒：一支手機裡有好幾張 QR 票，旁邊是一家人',
    f'<rect x="10" y="20" width="44" height="78" rx="8" fill="{NAVY}"/>'
    f'<rect x="15" y="28" width="34" height="62" rx="3" fill="{WHITE}"/>'
    + qr(18, 32, 13) + qr(33, 32, 13) + qr(18, 50, 13) + qr(33, 50, 13)
    + ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#f9d9c0"/><path d="M{x-8},{y+24} q0,-16 8,-16 q8,0 8,16 Z" fill="{c}"/>'
              for x, y, c in [(72, 56, SKY), (92, 54, PINK), (110, 64, GOLD)])
    + star(92, 22, 8))

# 安檢門刷 QR 票後，記得拿換入館證的兌換券
rem('r-gate', '手繪提醒：閘門吐出一張兌換券，箭頭指向掛繩入館證',
    f'<rect x="10" y="44" width="44" height="62" rx="6" fill="{GRAY}"/>'
    f'<rect x="16" y="52" width="32" height="18" rx="3" fill="#cfe8b8" stroke-width="1.4"/>'
    f'<rect x="18" y="80" width="28" height="5" rx="2" fill="{INK}" stroke="none"/>'
    f'<path d="M22,82 L22,104 L42,104 L42,82" fill="{WHITE}" stroke-width="1.6" transform="translate(0,-60)"/>'
    f'<path d="M26,30 L38,30 M26,36 L36,36" stroke-width="1.4"/>'
    f'<path d="M50,30 L66,30 M66,30 L60,24 M66,30 L60,36" fill="none" stroke="{RED}" stroke-width="2.6"/>'
    f'<path d="M78,14 L90,40 L102,14" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    f'<rect x="74" y="40" width="32" height="42" rx="4" fill="{WHITE}"/>'
    f'<rect x="80" y="48" width="20" height="14" rx="2" fill="{SKY}" stroke-width="1.2"/>'
    f'<path d="M80,70 L100,70 M80,76 L94,76" stroke-width="1.4"/>'
    + star(96, 100, 8))

# 計程車也不行
rem('r-taxi', '手繪提醒：計程車打叉，旁邊是電車',
    f'<rect x="38" y="20" width="16" height="10" rx="2" fill="{GOLD}"/>'
    f'<path d="M14,58 L22,36 Q24,30 32,30 L60,30 Q68,30 70,36 L78,58 Z" fill="{GOLD}"/>'
    f'<rect x="8" y="56" width="76" height="20" rx="6" fill="{GOLD}"/>'
    f'<circle cx="24" cy="78" r="7" fill="{GRAY}"/><circle cx="68" cy="78" r="7" fill="{GRAY}"/>'
    f'<path d="M8,24 L84,92 M84,24 L8,92" stroke="{RED}" stroke-width="5"/>'
    f'<rect x="72" y="84" width="32" height="24" rx="6" fill="{SKY}"/>'
    f'<rect x="76" y="88" width="10" height="9" rx="2" fill="{WHITE}" stroke-width="1.2"/><rect x="90" y="88" width="10" height="9" rx="2" fill="{WHITE}" stroke-width="1.2"/>')

print(save(F, OUT), 'files')
