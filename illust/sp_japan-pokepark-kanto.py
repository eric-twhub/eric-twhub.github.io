# 寶可夢公園頁的「園區裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網的園區介紹、交通與園區服務頁（pokepark-kanto.co.jp/ppark/，繁中版）畫成一般的森林步道、小鎮與纜車。
# 角色 IP：園內到處是寶可夢，這裡一律不畫；不畫角色、紅白球、寶可夢中心的招牌、商標或 logo。
# 輸出 illust/sp/japan-pokepark-kanto/*.svg。說明文字放在 illust/spots/japan-pokepark-kanto.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-pokepark-kanto')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('pk-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def roundtree(x, base, r=16, col=GREEN, trunk=12):
    return (f'<rect x="{x-3}" y="{base-trunk}" width="6" height="{trunk}" fill="{DBROWN}" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{base-trunk-r*.8:.1f}" r="{r}" fill="{col}"/>')


def grass(x, y):
    return f'<path d="M{x},{y} l-4,-10 M{x},{y} l0,-12 M{x},{y} l4,-10" stroke="{DGREEN}" stroke-width="2"/>'


# 1. 從京王讀賣樂園站搭空中纜車上山
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     f'<path d="M3,120 Q70,90 130,70 Q190,50 237,58 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#9ccc8a"/>'
     + roundtree(150, 70, 12, DGREEN) + roundtree(200, 62, 14, DGREEN) + roundtree(110, 98, 11, GREEN) + roundtree(60, 132, 12, GREEN)
     + f'<path d="M14,150 L226,34" stroke-width="2"/>'
     + f'<rect x="12" y="140" width="40" height="30" rx="3" fill="#f3e6d3"/><path d="M8,142 L56,142 L48,130 L16,130 Z" fill="{RED}"/>'
     + f'<rect x="206" y="30" width="26" height="22" rx="3" fill="#f3e6d3"/>')
for x, c in [(78, GOLD), (150, PINK)]:
    y = 150 - (x - 14) * 116 / 212
    t += (f'<path d="M{x},{y:.1f} L{x},{y+12:.1f}" stroke-width="2"/>'
          f'<rect x="{x-14}" y="{y+12:.1f}" width="28" height="26" rx="8" fill="{c}"/>'
          f'<rect x="{x-9}" y="{y+17:.1f}" width="18" height="10" rx="3" fill="{WHITE}" stroke-width="1.4"/>')
t += sparkle(40, 30) + sparkle(120, 22) + star(180, 22, 6)
card('gondola', '手繪從車站往山上的空中纜車，兩台小車廂掛在纜線上', t, bg=SKY)

# 2. 讀賣樂園的大門，進去後照指標走
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf0d8"/>'
     + bottom(140, '#e3d3b2')
     + f'<rect x="30" y="60" width="22" height="80" fill="{PINK}"/><rect x="188" y="60" width="22" height="80" fill="{PINK}"/>'
     + f'<path d="M24,64 Q120,10 216,64 L216,76 Q120,26 24,76 Z" fill="{GOLD}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}" stroke-width="1.2"/>' for x, y, c in [(60, 46, RED), (90, 34, SKY), (120, 30, GREEN), (150, 34, SKY), (180, 46, RED)])
     + f'<path d="M30,60 L20,48 M52,60 L46,44 M188,60 L194,44 M210,60 L220,48" stroke-width="1.6"/>'
     # 指標
     + f'<path d="M150,140 L150,92" stroke-width="3"/>'
     + f'<path d="M150,96 L184,96 L192,104 L184,112 L150,112 Z" fill="{GREEN}"/>'
     + f'<path d="M150,116 L118,116 L110,124 L118,132 L150,132 Z" fill="{SKY}"/>'
     + person(82, 112, SKY, .9) + person(102, 116, RED, .8)
     + f'<path d="M66,160 L78,160 M90,164 L100,164" stroke-width="1.6" opacity=".5"/>'
     + sparkle(120, 60) + star(214, 24, 6))
card('gate', '手繪遊樂園的拱門大門，門裡立著指路的牌子', t, bg='#fdf0d8')

# 3. 寶可夢森林：高低起伏的步道、草叢、隧道
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f3dc"/>'
     + roundtree(30, 70, 18, DGREEN) + roundtree(78, 56, 14, GREEN) + roundtree(206, 60, 18, DGREEN) + roundtree(160, 44, 12, GREEN)
     + f'<path d="M3,96 Q60,80 120,92 T237,86 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="#a8d394"/>'
     + f'<path d="M100,177 Q90,150 130,136 Q170,124 150,110 Q130,100 162,94" fill="none" stroke="#e8d3a8" stroke-width="22"/>'
     + f'<path d="M100,177 Q90,150 130,136 Q170,124 150,110 Q130,100 162,94" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 6" opacity=".4"/>'
     # 隧道
     + f'<path d="M150,100 Q150,70 176,70 Q202,70 202,100 Z" fill="#8a7a6a"/>'
     + f'<path d="M160,100 Q160,80 176,80 Q192,80 192,100 Z" fill="#3e3440"/>'
     + ''.join(grass(x, y) for x, y in [(40, 130), (56, 150), (24, 156), (200, 140), (216, 124), (186, 160), (70, 116)])
     + roundtree(46, 112, 12, DGREEN) + roundtree(222, 112, 10, GREEN)
     + person(118, 140, GOLD, .8)
     + sparkle(120, 26) + sparkle(220, 24))
card('forest', '手繪森林裡彎彎曲曲的步道，前方有一座小隧道，路邊是草叢', t, bg='#e6f3dc')

# 4. 森林裡的 110 階階梯
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f3dc"/>'
     + roundtree(30, 90, 18, DGREEN) + roundtree(210, 80, 18, DGREEN) + roundtree(186, 140, 12, GREEN) + roundtree(52, 150, 12, GREEN))
for i in range(9):
    y = 166 - i * 15
    x1, x2 = 70 + i * 6, 160 + i * 2
    t += f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="10" rx="2" fill="#e8d3a8"/>'
t += (f'<path d="M64,174 L118,40 M166,174 L178,40" stroke-width="2.4"/>'
      + person(108, 92, RED, .8) + person(136, 122, SKY, .8)
      + f'<rect x="184" y="14" width="44" height="22" rx="6" fill="{WHITE}"/>'
      + f'<text x="206" y="30" font-size="13" text-anchor="middle" fill="{RED}" stroke="none" font-family="sans-serif" font-weight="bold">110</text>'
      + sparkle(30, 26) + star(150, 22, 6))
card('stairs', '手繪森林裡一路往上的長階梯，旁邊標著 110', t, bg='#e6f3dc')

# 5. 草紗鎮：商店、市集與每天有表演的建築
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(140, '#e8dccb')
     + f'<rect x="14" y="78" width="60" height="62" fill="#fbf3e4"/><path d="M8,80 L44,52 L80,80 Z" fill="{BRICK}"/>'
     + f'<path d="M14,100 L74,100" stroke-width="2"/>'
     + ''.join(f'<path d="M{14+i*12},100 L{20+i*12},112 L{26+i*12},100" fill="{PINK if i % 2 else WHITE}" stroke-width="1.4"/>' for i in range(5))
     + f'<rect x="32" y="116" width="22" height="24" rx="2" fill="{DBROWN}"/>'
     # 中間：舞台建築
     + f'<rect x="88" y="62" width="70" height="78" fill="#f6e3a8"/>'
     + f'<path d="M82,64 Q123,26 164,64 Z" fill="#7fa9d6"/>'
     + f'<rect x="100" y="90" width="46" height="36" rx="4" fill="{NAVY}"/>'
     + ''.join(f'<path d="M{x},126 L{x},96" stroke="{GOLD}" stroke-width="1.6" opacity=".7"/>' for x in (110, 123, 136))
     + star(123, 82, 7)
     # 右邊：市集攤子
     + f'<rect x="172" y="96" width="56" height="44" fill="#fbf3e4"/>'
     + f'<path d="M168,98 L232,98 L226,82 L174,82 Z" fill="{GREEN}"/>'
     + ''.join(f'<rect x="{x}" y="112" width="10" height="12" rx="2" fill="{c}" stroke-width="1.2"/>' for x, c in [(178, PINK), (192, GOLD), (206, SKY), (218, '#c9b6e8')])
     + person(76, 146, GOLD, .7) + person(170, 148, PINK, .7)
     + sparkle(40, 30) + sparkle(200, 36))
card('town', '手繪小鎮街景：左邊是商店，中間是有舞台的建築，右邊是賣東西的攤子', t, bg=SKY)

# 6. 部分表演與商店要在 App 拿號碼牌
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf0d8"/>'
     f'<rect x="80" y="18" width="80" height="146" rx="14" fill="{NAVY}"/>'
     f'<rect x="88" y="32" width="64" height="116" rx="4" fill="{WHITE}"/>'
     f'<rect x="96" y="42" width="48" height="10" rx="3" fill="{GOLD}" stroke-width="1.2"/>'
     f'<rect x="96" y="60" width="48" height="54" rx="6" fill="#fde7ea"/>'
     f'<text x="120" y="96" font-size="22" text-anchor="middle" fill="{RED}" stroke="none" font-family="sans-serif" font-weight="bold">25</text>'
     f'<rect x="100" y="122" width="40" height="16" rx="8" fill="{GREEN}"/>'
     f'<path d="M112,130 L118,135 L128,125" fill="none" stroke="{WHITE}" stroke-width="2.4"/>'
     # 旁邊的小票
     + f'<g transform="rotate(-12 44 96)"><rect x="18" y="74" width="52" height="40" rx="5" fill="{GOLD}"/>'
     f'<path d="M30,88 L58,88 M30,98 L50,98" stroke-width="1.8"/></g>'
     + f'<g transform="rotate(10 196 96)"><rect x="172" y="74" width="50" height="44" rx="5" fill="{SKY}"/>'
     f'<circle cx="197" cy="96" r="12" fill="{WHITE}"/><path d="M197,96 L197,88 M197,96 L203,99" stroke-width="2"/></g>'
     + sparkle(40, 30) + sparkle(204, 150) + star(30, 150, 6))
card('app', '手繪手機畫面上的號碼牌，旁邊是一張票和一個時鐘', t, bg='#fdf0d8')


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('pk-' + name, 120, 120, label, inner, bg='#fff3c4')


# 開車導航要輸入讀賣樂園的地址
rem('r-nav', '手繪提醒：車子和導航畫面上的定位針',
    f'<rect x="54" y="14" width="56" height="44" rx="6" fill="{NAVY}"/>'
    f'<rect x="59" y="19" width="46" height="34" rx="3" fill="#cfe8b8"/>'
    f'<path d="M62,44 L80,30 L102,40" fill="none" stroke="{WHITE}" stroke-width="3"/>'
    f'<path d="M82,44 q-8,-10 -8,-16 a8,8 0 1 1 16,0 q0,6 -8,16 Z" fill="{RED}" stroke-width="1.6"/>'
    f'<circle cx="82" cy="28" r="3" fill="{WHITE}" stroke-width="1"/>'
    f'<path d="M14,86 L20,70 Q22,66 28,66 L58,66 Q64,66 66,70 L72,86 Z" fill="{SKY}"/>'
    f'<rect x="8" y="84" width="70" height="20" rx="6" fill="{RED}"/>'
    f'<circle cx="24" cy="106" r="7" fill="{GRAY}"/><circle cx="62" cy="106" r="7" fill="{GRAY}"/>')

# 嬰兒車與輪椅在讀賣樂園入口租
rem('r-stroller', '手繪提醒：嬰兒車和遊樂園的大門',
    f'<path d="M70,40 Q88,12 106,40" fill="none" stroke="{GOLD}" stroke-width="7"/>'
    f'<path d="M72,40 L72,64 M104,40 L104,64" stroke-width="4"/>'
    f'<path d="M14,56 Q14,30 40,30 L40,56 Z" fill="{PINK}"/>'
    f'<path d="M14,56 L62,56 Q62,78 40,78 L30,78 Q14,78 14,56 Z" fill="{PINK}"/>'
    f'<path d="M62,56 L68,46" stroke-width="3"/>'
    f'<circle cx="22" cy="90" r="9" fill="{GRAY}"/><circle cx="54" cy="90" r="9" fill="{GRAY}"/>'
    f'<path d="M30,78 L24,82 M44,78 L50,82" stroke-width="2"/>'
    + star(96, 92, 8))

print(save(F, OUT), 'files')
