# 東京哈利波特影城頁的「影城裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網的交通、常見問題頁（wbstudiotour.jp）畫成一般的車站、拍片道具、手機、導覽機、置物櫃與巴士。
# 角色 IP：不畫任何角色、魔杖、眼鏡加閃電疤、學院徽章、城堡、掃帚、特定電影布景、商標或 logo。
# 輸出 illust/sp/japan-harry-potter-tokyo/*.svg。說明文字放在 illust/spots/japan-harry-potter-tokyo.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-harry-potter-tokyo')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('hp-' + name, W, H, label, inner, bg=bg)


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>')


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def txt(x, y, s, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}" stroke="none" '
            f'font-family="sans-serif" font-weight="bold">{s}</text>')


# 1. 豐島園站出來走 2 分鐘
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(138, '#d8d2c6')
     # 車站
     + f'<rect x="14" y="88" width="62" height="50" fill="#f3e6d3"/><path d="M8,90 L45,66 L82,90 Z" fill="{GREEN}"/>'
     + f'<rect x="24" y="104" width="16" height="34" rx="2" fill="{SKY}"/><rect x="48" y="104" width="18" height="14" rx="2" fill="{SKY}"/>'
     + f'<rect x="26" y="74" width="38" height="10" rx="3" fill="{WHITE}" stroke-width="1.4"/>'
     # 大大的攝影棚建築
     + f'<path d="M118,138 L118,58 Q170,30 228,58 L228,138 Z" fill="#cfc6d8"/>'
     + ''.join(f'<path d="M{x},{138} L{x},{62-(x-118)*0+0}" stroke-width="1" opacity=".0"/>' for x in ())
     + f'<path d="M118,74 Q173,48 228,74" fill="none" stroke-width="1.6" opacity=".6"/>'
     + f'<rect x="150" y="100" width="46" height="38" rx="3" fill="{NAVY}"/><path d="M173,100 L173,138" stroke="{GOLD}" stroke-width="1.6"/>'
     + ''.join(f'<rect x="{x}" y="84" width="14" height="10" rx="2" fill="{GOLD}" stroke-width="1.2"/>' for x in (128, 206))
     # 腳印
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="5" fill="{BROWN}" stroke-width="1" transform="rotate(70 {x} {y})"/>'
               for x, y in [(86, 150), (96, 158), (106, 150), (116, 158), (126, 150), (136, 158)])
     + f'<rect x="88" y="112" width="26" height="16" rx="4" fill="{WHITE}"/>' + txt(101, 124, '2分', 10, RED)
     + sparkle(100, 30) + star(40, 30, 6))
card('station', '手繪左邊的小車站、右邊的大型攝影棚建築，中間一串腳印，牌子寫著 2 分', t, bg=SKY)

# 2. 打造布景的團隊與真正用過的服裝：場記板、聚光燈、衣架
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#2f2b45"/>'
     f'<polygon points="56,40 20,170 120,170" fill="{GOLD}" stroke="none" opacity=".18"/>'
     f'<rect x="40" y="22" width="34" height="24" rx="5" fill="{GRAY}" transform="rotate(18 57 34)"/>'
     f'<path d="M57,46 L57,60" stroke="{GRAY}" stroke-width="3"/>'
     # 場記板
     + f'<rect x="34" y="104" width="76" height="52" rx="4" fill="#3a3a3a" stroke="{WHITE}"/>'
     + f'<g transform="rotate(-14 34 104)"><rect x="34" y="88" width="76" height="14" rx="2" fill="{WHITE}" stroke="{WHITE}"/>'
     + ''.join(f'<path d="M{40+i*14},88 L{48+i*14},102" stroke="#3a3a3a" stroke-width="5"/>' for i in range(5)) + '</g>'
     + f'<path d="M42,120 L100,120 M42,134 L100,134" stroke="{WHITE}" stroke-width="1.6"/>'
     # 衣架與服裝
     + f'<path d="M136,40 L222,40 M140,40 L140,160 M218,40 L218,160 M132,160 L148,160 M210,160 L226,160" stroke="{GRAY}" stroke-width="3"/>'
     + ''.join(f'<path d="M{x},42 L{x},48" stroke="{GRAY}" stroke-width="2"/>'
               f'<path d="M{x-14},56 L{x},48 L{x+14},56 L{x+12},120 L{x-12},120 Z" fill="{c}" stroke="{WHITE}" stroke-width="1.8"/>'
               for x, c in [(158, '#c97b6a'), (180, '#7fa58c'), (202, '#c9b6e8')])
     + sparkle(120, 30) + sparkle(214, 150, 4) + star(120, 150, 5))
card('sets', '手繪拍片現場：聚光燈照著一塊場記板，旁邊衣架上掛著三件戲服', t, bg='#2f2b45')

# 3. 拍攝體驗：掃 QR code 之後下載自己的影片
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e3f1f8"/>'
     f'<rect x="20" y="40" width="96" height="70" rx="6" fill="#7fc4a0"/>'
     f'<path d="M20,94 L116,94" stroke-width="1.6" opacity=".5"/>'
     + person(68, 66, PINK, .9)
     + f'<path d="M56,74 L44,62 M80,74 L92,60" stroke-width="2"/>'
     f'<rect x="56" y="118" width="24" height="40" rx="3" fill="{GRAY}"/><rect x="50" y="110" width="36" height="12" rx="4" fill="{NAVY}"/>'
     # 手機與 QR
     + f'<rect x="148" y="30" width="66" height="122" rx="12" fill="{NAVY}"/>'
     + f'<rect x="155" y="42" width="52" height="96" rx="4" fill="{WHITE}"/>'
     + f'<rect x="161" y="50" width="40" height="30" rx="3" fill="#7fc4a0"/>'
     + f'<path d="M176,58 L188,65 L176,72 Z" fill="{WHITE}" stroke-width="1.4"/>'
     + f'<rect x="166" y="90" width="30" height="30" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
     + ''.join(f'<rect x="{166+a*5}" y="{90+b*5}" width="5" height="5" fill="{INK}" stroke="none"/>' for a, b in [(1, 1), (4, 1), (1, 4), (2, 2), (3, 3), (4, 4), (2, 4)])
     + f'<path d="M180,128 L180,136 M176,132 L180,136 L184,132" fill="none" stroke="{RED}" stroke-width="2"/>'
     + f'<path d="M122,90 L140,90 M134,84 L140,90 L134,96" fill="none" stroke="{RED}" stroke-width="2.6"/>'
     + sparkle(30, 24) + star(126, 30, 6))
card('video', '手繪在綠色背景前擺姿勢的人與攝影機，箭頭指向手機上可以下載的影片和 QR code', t, bg='#e3f1f8')

# 4. 數位導覽機，有繁體中文（台灣）
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf0d8"/>'
     f'<rect x="56" y="30" width="80" height="124" rx="14" fill="{GRAY}"/>'
     f'<rect x="64" y="42" width="64" height="76" rx="4" fill="{WHITE}"/>'
     + txt(96, 92, '繁中', 22, RED)
     + f'<path d="M72,56 L120,56" stroke-width="1.6" opacity=".5"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{INK}" stroke="none"/>' for x in (84, 92, 100, 108) for y in (132, 140))
     # 耳機
     + f'<path d="M150,90 Q150,40 186,40 Q222,40 222,90" fill="none" stroke-width="5"/>'
     + f'<rect x="142" y="84" width="18" height="32" rx="8" fill="{RED}"/><rect x="212" y="84" width="18" height="32" rx="8" fill="{RED}"/>'
     + f'<path d="M151,116 Q140,150 128,140" fill="none" stroke-width="2"/>'
     + ''.join(f'<path d="M{x},{y} q6,-4 0,-10" fill="none" stroke="{GOLD}" stroke-width="2"/>' for x, y in [(200, 130), (208, 136)])
     + sparkle(30, 30) + sparkle(30, 140) + star(214, 22, 6))
card('guide', '手繪一台導覽機，螢幕上寫著繁中，旁邊是一副耳機', t, bg='#fdf0d8')

# 5. 置物櫃與兌幣機
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#eef2f6"/>'
     + bottom(150, '#d6d0c4'))
for c in range(4):
    for r in range(3):
        x, y = 20 + c * 34, 40 + r * 36
        t += (f'<rect x="{x}" y="{y}" width="32" height="34" rx="3" fill="{SKY if (c+r) % 2 else "#cfe3f2"}"/>'
              f'<circle cx="{x+24}" cy="{y+17}" r="2.6" fill="{GOLD}" stroke-width="1"/>')
t += (f'<rect x="164" y="58" width="34" height="92" rx="5" fill="{GOLD}"/>'
      f'<rect x="170" y="66" width="22" height="14" rx="2" fill="{WHITE}" stroke-width="1.2"/>'
      f'<rect x="172" y="92" width="18" height="4" rx="1" fill="{INK}" stroke="none"/>'
      f'<circle cx="181" cy="122" r="7" fill="{WHITE}" stroke-width="1.4"/>'
      # 行李箱
      f'<rect x="204" y="104" width="26" height="40" rx="5" fill="{RED}"/><path d="M212,104 L212,94 L222,94 L222,104" fill="none" stroke-width="2"/>'
      f'<circle cx="210" cy="146" r="3" fill="{INK}" stroke="none"/><circle cx="224" cy="146" r="3" fill="{INK}" stroke="none"/>'
      + sparkle(120, 24) + star(214, 24, 6))
card('locker', '手繪一整排置物櫃，旁邊是兌幣機和一個紅色行李箱', t, bg='#eef2f6')

# 6. 羽田機場的利木津巴士停在影城入口
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(132, '#c9c4bb')
     + f'<path d="M3,150 L237,150" stroke="{WHITE}" stroke-width="3" stroke-dasharray="14 10"/>'
     + f'<path d="M160,40 L176,30 L196,36 L200,26 L218,22" fill="none" stroke-width="2"/>'
     + f'<path d="M198,14 L230,22 L210,30 Z" fill="{WHITE}"/>'
     + f'<rect x="24" y="74" width="168" height="62" rx="12" fill="#f4f1ea"/>'
     + f'<rect x="24" y="112" width="168" height="10" fill="{NAVY}" stroke-width="1.6"/>'
     + ''.join(f'<rect x="{x}" y="84" width="24" height="20" rx="3" fill="#bfe0f2" stroke-width="1.6"/>' for x in range(34, 160, 30))
     + f'<rect x="168" y="84" width="20" height="44" rx="3" fill="#bfe0f2"/>'
     + f'<circle cx="60" cy="138" r="11" fill="{GRAY}"/><circle cx="160" cy="138" r="11" fill="{GRAY}"/>'
     + f'<path d="M210,132 L210,80" stroke-width="3"/><circle cx="210" cy="74" r="12" fill="{GOLD}"/>'
     + sparkle(40, 30) + star(110, 30, 6))
card('bus', '手繪一輛利木津巴士停在站牌旁，天上飛過一架飛機', t, bg=SKY)


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('hp-' + name, 120, 120, label, inner, bg='#fff3c4')


# 團體合照要出館再拍
rem('r-group', '手繪提醒：一家人站在樹旁拍合照',
    f'<rect x="80" y="70" width="6" height="30" fill="{DBROWN}"/><circle cx="83" cy="56" r="20" fill="{GREEN}"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#f9d9c0"/><path d="M{x-8},{y+24} q0,-16 8,-16 q8,0 8,16 Z" fill="{c}"/>'
              for x, y, c in [(20, 66, SKY), (38, 62, PINK), (56, 68, GOLD)])
    + f'<rect x="22" y="18" width="34" height="22" rx="4" fill="{GRAY}"/><circle cx="39" cy="29" r="6" fill="{WHITE}"/><rect x="26" y="14" width="10" height="5" rx="2" fill="{GRAY}"/>'
    + f'<path d="M58,24 L70,18 M58,30 L72,30" stroke="{GOLD}" stroke-width="2"/>'
    + f'<path d="M10,104 L106,104" stroke-width="2"/>')

# 拍攝體驗的影片只留 30 天
rem('r-video30', '手繪提醒：手機上的影片和寫著 30 的日曆',
    f'<rect x="12" y="20" width="44" height="80" rx="8" fill="{NAVY}"/>'
    f'<rect x="17" y="28" width="34" height="62" rx="3" fill="{WHITE}"/>'
    f'<rect x="21" y="40" width="26" height="20" rx="2" fill="#7fc4a0"/><path d="M30,44 L38,50 L30,56 Z" fill="{WHITE}" stroke-width="1"/>'
    f'<rect x="64" y="34" width="46" height="46" rx="5" fill="{WHITE}"/>'
    f'<rect x="64" y="34" width="46" height="13" rx="4" fill="{RED}"/>'
    f'<path d="M74,30 L74,40 M100,30 L100,40" stroke-width="2.4"/>'
    + txt(87, 72, '30', 20, INK)
    + star(96, 102, 8))

print(save(F, OUT), 'files')
