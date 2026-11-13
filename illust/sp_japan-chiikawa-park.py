# 吉伊卡哇樂園頁的「樂園裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網的園區介紹（chiikawapark-tokyo.jp/about/）與利用指南，畫成一般的劇場、鏡子走廊、3D 眼鏡、遊戲台與商店。
# 角色 IP：不畫任何角色、角色的臉或耳朵、角色造型的物件（車子、房子、抱枕等）、商標或 logo。
# 輸出 illust/sp/japan-chiikawa-park/*.svg。說明文字放在 illust/spots/japan-chiikawa-park.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-chiikawa-park')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ck-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def txt(x, y, s, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}" stroke="none" '
            f'font-family="sans-serif" font-weight="bold">{s}</text>')


def scene(x1, y1, x2, y2, x3, y3, x4, y4, sky='#dff0fd', hill='#b6e3c6'):
    # 一面螢幕（四邊形），裡面是天空和山丘
    return (f'<polygon points="{x1},{y1} {x2},{y2} {x3},{y3} {x4},{y4}" fill="{sky}"/>'
            f'<polygon points="{x4},{(y1+y4*2)/3:.0f} {(x3+x4)/2:.0f},{(y2+y3*2)/3-6:.0f} {x3},{(y2+y3*2)/3:.0f} {x3},{y3} {x4},{y4}" fill="{hill}" stroke-width="1.4"/>')


# 1. 迎賓劇場：三面相連的大螢幕
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#3b3658"/>'
     + scene(14, 24, 70, 40, 70, 112, 14, 128)
     + scene(76, 40, 164, 40, 164, 112, 76, 112, '#fde7ea', '#f6c9a8')
     + scene(170, 40, 226, 24, 226, 128, 170, 112)
     + f'<circle cx="120" cy="64" r="10" fill="{GOLD}"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{WHITE}" stroke="none"/>' for x, y in [(36, 46), (52, 56), (196, 52), (210, 44)])
     + ''.join(person(x, 136 + (k % 2) * 4, c, .8) for k, (x, c) in enumerate([(52, SKY), (84, PINK), (116, GOLD), (148, GREEN), (180, PINK)]))
     + sparkle(120, 20))
card('theater3', '手繪三面相連的大螢幕，觀眾站在前面看', t, bg='#3b3658')

# 2. 色彩繽紛、看起來沒有盡頭的鏡子走廊
t = f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#2f2b45"/>'
cols = [PINK, GOLD, SKY, '#b6e3c6', '#c9b6e8', '#f7c9a0']
for i in range(6):
    m = i * 11
    t += (f'<rect x="{24+m}" y="{20+m*.7:.0f}" width="{192-2*m}" height="{140-m*1.4:.0f}" rx="{12-i}" '
          f'fill="none" stroke="{cols[i]}" stroke-width="5"/>')
t += (f'<rect x="88" y="66" width="64" height="48" rx="4" fill="#3d3860" stroke="{WHITE}" stroke-width="1.6"/>'
      + person(120, 118, GOLD, .9)
      + ''.join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{WHITE}" stroke="none"/>' for x, y in [(104, 80), (136, 76), (120, 92), (110, 100), (132, 102)])
      + sparkle(30, 30) + sparkle(210, 150))
card('mirror', '手繪一層層彩色框線往裡延伸的鏡子走廊，走廊中間站著一個人', t, bg='#2f2b45')

# 3. 森林觀測所：3D 劇場
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#1f3a34"/>'
     f'<rect x="20" y="16" width="200" height="86" rx="6" fill="#cfe8b8"/>'
     + ''.join(f'<path d="M{x},{96} L{x},{80}" stroke="{DBROWN}" stroke-width="3"/><circle cx="{x}" cy="{70}" r="{r}" fill="{c}"/>'
               for x, r, c in [(48, 16, DGREEN), (90, 12, GREEN), (150, 18, DGREEN), (196, 13, GREEN)])
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="3" fill="{c}" stroke-width="1.2"/>' for x, y, c in [(118, 40, PINK), (128, 34, GOLD), (70, 34, '#c9b6e8')])
     # 3D 眼鏡
     + f'<path d="M48,126 L192,126" stroke-width="3"/>'
     + f'<rect x="60" y="118" width="54" height="36" rx="10" fill="#e4625a" opacity=".9"/>'
     + f'<rect x="126" y="118" width="54" height="36" rx="10" fill="#7fb6e4" opacity=".9"/>'
     + f'<path d="M114,130 Q120,124 126,130" fill="none" stroke-width="3"/>'
     + f'<path d="M60,128 L36,120 M180,128 L204,120" stroke-width="3"/>'
     + txt(206, 160, '3D', 16, GOLD)
     + sparkle(30, 150))
card('3d', '手繪森林畫面的大銀幕，前面一副紅藍鏡片的 3D 眼鏡', t, bg='#1f3a34')

# 4. 遊戲區：滾球進洞、用網子接
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fff0dc"/>'
     + bottom(150, '#e8d6bb')
     # 滾球台
     + f'<polygon points="20,140 120,140 100,60 40,60" fill="#7fc4a0"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="#2f5d4a"/>' for x, y in [(54, 78), (86, 78), (70, 100), (48, 120), (94, 118)])
     + f'<path d="M20,140 L120,140" stroke-width="3"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>' for x, y, c in [(74, 132, '#c9893a'), (88, 150, '#c9893a')])
     + f'<path d="M70,148 q-6,4 -14,2" fill="none" stroke-width="1.6" stroke-dasharray="3 3"/>'
     # 撈網：圓框加垂下來的網袋
     + f'<path d="M150,140 L170,70" stroke="{DBROWN}" stroke-width="4"/>'
     + f'<path d="M166,62 L182,104 L198,104 L214,62" fill="{WHITE}" opacity=".8"/>'
     + ''.join(f'<path d="M{170+i*9},63 L{184+i*3},104" stroke-width="1" opacity=".6"/>' for i in range(5))
     + ''.join(f'<path d="M{168+i*2.6:.1f},{70+i*8} L{212-i*2.6:.1f},{70+i*8}" stroke-width="1" opacity=".6"/>' for i in range(4))
     + f'<ellipse cx="190" cy="62" rx="26" ry="8" fill="none" stroke-width="3"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}"/>' for x, y, c in [(188, 32, PINK), (204, 26, GOLD), (184, 92, '#b6e3c6')])
     # 獎品盒
     + f'<rect x="176" y="136" width="40" height="28" rx="3" fill="{PINK}"/><path d="M196,136 L196,164 M176,148 L216,148" stroke="{GOLD}" stroke-width="3"/>'
     + star(140, 30, 7) + sparkle(30, 30))
card('game', '手繪兩種遊戲：左邊是有洞的滾球台，右邊是撈東西的網子，旁邊放著獎品盒', t, bg='#fff0dc')

# 5. 1 樓商店區：布偶、文具、衣服、爆米花、客製名字
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf3e6"/>'
     + bottom(150, '#e8d6bb')
     + f'<rect x="14" y="32" width="212" height="112" rx="6" fill="#f3dfc4"/>'
     + f'<path d="M14,88 L226,88" stroke-width="2.4"/>'
     # 上層：T 恤、文具
     + f'<path d="M30,48 L44,42 Q50,48 56,42 L70,48 L66,58 L60,56 L60,82 L40,82 L40,56 L34,58 Z" fill="{SKY}"/>'
     + ''.join(f'<rect x="{x}" y="50" width="6" height="32" rx="2" fill="{c}" transform="rotate({r} {x+3} 66)"/>' for x, c, r in [(88, GOLD, -8), (98, PINK, 0), (108, GREEN, 8)])
     + f'<rect x="126" y="50" width="34" height="32" rx="3" fill="{WHITE}"/><path d="M132,58 L154,58 M132,66 L150,66 M132,74 L146,74" stroke-width="1.4"/>'
     + f'<path d="M176,82 L176,56 Q192,44 208,56 L208,82 Z" fill="#fde7ea"/><path d="M182,66 L202,66" stroke-width="1.4"/>'
     # 下層：爆米花、名牌、小布偶（畫成普通圓球）
     + f'<path d="M30,140 L36,104 L66,104 L72,140 Z" fill="{WHITE}"/>'
     + ''.join(f'<path d="M{x},104 L{x+3},140" stroke="{RED}" stroke-width="3"/>' for x in (42, 54))
     + ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#fbf0c8" stroke-width="1.4"/>' for x, y in [(40, 100), (50, 96), (60, 100), (46, 92), (56, 90)])
     + f'<rect x="90" y="106" width="44" height="30" rx="6" fill="{GOLD}"/><circle cx="98" cy="114" r="3" fill="{WHITE}" stroke-width="1"/>'
     + txt(114, 128, 'NAME', 9, DBROWN)
     + ''.join(f'<circle cx="{x}" cy="122" r="14" fill="{c}"/>' for x, c in [(160, WHITE), (192, PINK)])
     + f'<rect x="206" y="112" width="14" height="20" rx="4" fill="{SKY}"/>'
     + sparkle(120, 18) + star(214, 18, 6))
card('shop', '手繪商店貨架：上層有 T 恤、筆和筆記本，下層有爆米花桶、寫著 NAME 的名牌和圓圓的軟布偶', t, bg='#fdf3e6')

# 6. 入口在陽光城 Annex 的地下一樓
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef2f6"/>'
     + f'<rect x="20" y="20" width="96" height="92" fill="#dfe6ee"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="16" height="12" rx="2" fill="{SKY}" stroke-width="1.2"/>' for x in (28, 50, 72, 94) for y in (28, 48, 68))
     + bottom(112, '#cfc6b8'))
for i in range(6):
    y = 112 + i * 10
    t += f'<rect x="{120 + i * 6}" y="{y}" width="{100 - i * 6}" height="10" fill="{"#e9e3d6" if i % 2 else "#f4efe6"}" stroke-width="1.4"/>'
t += (f'<path d="M120,112 L156,172" stroke-width="2.4"/>'
      + f'<path d="M188,78 L188,112" stroke-width="3"/>'
      + f'<rect x="164" y="54" width="48" height="28" rx="6" fill="{NAVY}"/>' + txt(188, 74, 'B1', 16, WHITE)
      + f'<path d="M150,128 L170,152 M170,152 L170,140 M170,152 L158,152" fill="none" stroke="{RED}" stroke-width="3"/>'
      + person(60, 116, PINK, .8) + person(86, 120, GOLD, .7)
      + sparkle(140, 26) + star(220, 26, 6))
card('entrance', '手繪大樓旁往下走的樓梯，牌子寫著 B1，紅色箭頭指向地下', t, bg='#eef2f6')


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('ck-' + name, 120, 120, label, inner, bg='#fff3c4')


# 上了 1 樓商店就回不去 B1
rem('r-oneway', '手繪提醒：往上的樓梯，旁邊往下的箭頭打叉',
    ''.join(f'<rect x="{12 + i * 12}" y="{90 - i * 14}" width="{58 - i * 12 + 12}" height="14" fill="{"#e9e3d6" if i % 2 else "#f4efe6"}" stroke-width="1.4"/>' for i in range(4))
    + f'<path d="M24,84 L52,40 M52,40 L52,52 M52,40 L40,44" fill="none" stroke="{GREEN}" stroke-width="3"/>'
    + f'<rect x="80" y="18" width="30" height="20" rx="4" fill="{NAVY}"/>' + txt(95, 33, '1F', 12, WHITE)
    + f'<path d="M94,52 L94,88 M86,80 L94,88 L102,80" fill="none" stroke-width="3"/>'
    + f'<path d="M80,58 L108,86 M108,58 L80,86" stroke="{RED}" stroke-width="4"/>')

# 沒有智慧型手機不能入場
rem('r-phone', '手繪提醒：手機上的 QR code 門票',
    f'<rect x="34" y="12" width="52" height="96" rx="10" fill="{NAVY}"/>'
    f'<rect x="40" y="22" width="40" height="74" rx="4" fill="{WHITE}"/>'
    f'<rect x="46" y="38" width="28" height="28" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
    + ''.join(f'<rect x="{46+a*4.6:.1f}" y="{38+b*4.6:.1f}" width="4.6" height="4.6" fill="{INK}" stroke="none"/>' for a, b in [(1, 1), (4, 1), (1, 4), (2, 3), (3, 2), (4, 4), (5, 2)])
    + f'<rect x="46" y="74" width="28" height="8" rx="3" fill="{GOLD}" stroke-width="1.2"/>'
    + star(100, 26, 8) + sparkle(18, 96))

# 三腳架、伸長的自拍棒不能用
rem('r-tripod', '手繪提醒：三腳架和伸長的自拍棒打叉',
    f'<path d="M34,30 L18,96 M34,30 L34,98 M34,30 L50,96" stroke-width="3"/>'
    f'<rect x="22" y="18" width="24" height="14" rx="3" fill="{GRAY}"/>'
    f'<path d="M80,98 L94,24" stroke-width="4"/>'
    f'<rect x="88" y="12" width="16" height="24" rx="3" fill="{NAVY}" transform="rotate(11 96 24)"/>'
    f'<path d="M14,22 L106,104 M106,22 L14,104" stroke="{RED}" stroke-width="5"/>')

print(save(F, OUT), 'files')
