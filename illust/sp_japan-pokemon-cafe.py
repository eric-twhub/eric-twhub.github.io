# 寶可夢咖啡廳頁的「店裡有什麼」插圖與提醒卡（2026-11-13）。
# 參考官網（pokemon-cafe.jp/ja/cafe/）的菜單分類與店舖資訊，只畫一般的餐點、杯子與百貨公司外觀。
# 角色 IP：店裡的餐點與周邊都是角色造型，這裡一律畫成沒有角色的普通餐點；不畫角色、紅白球、商標或 logo。
# 輸出 illust/sp/japan-pokemon-cafe/*.svg。說明文字放在 illust/spots/japan-pokemon-cafe.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-pokemon-cafe')
W, H = 240, 180
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('pc-' + name, W, H, label, inner, bg=bg)


def bottom(y, col):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def txt(x, y, s, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{col}" stroke="none" '
            f'font-family="sans-serif" font-weight="bold">{s}</text>')


def store(x, w, top, floors, hl, roof):
    # 百貨公司大樓：hl 是咖啡廳所在樓層（從 1 起算）
    base = 150
    fh = (base - top) / floors
    s = f'<rect x="{x}" y="{top}" width="{w}" height="{base-top}" fill="#f3e6d3"/>'
    s += f'<rect x="{x-4}" y="{top-8}" width="{w+8}" height="10" rx="3" fill="{roof}"/>'
    for i in range(floors):
        y = base - (i + 1) * fh
        col = GOLD if i + 1 == hl else SKY
        for k in range(3):
            s += f'<rect x="{x+6+k*(w-12)/3:.1f}" y="{y+3:.1f}" width="{(w-12)/3-4:.1f}" height="{fh-6:.1f}" rx="1.5" fill="{col}" stroke-width="1.2"/>'
    s += f'<rect x="{x+w/2-9}" y="{base-14}" width="18" height="14" fill="{DBROWN}"/>'
    return s


# 1. 兩家店都在百貨公司裡：東京 5 樓、大阪 9 樓
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{SKY}"/>'
     + bottom(150, '#d8d2c6')
     + store(22, 76, 70, 7, 5, RED)
     + store(136, 80, 50, 10, 9, GREEN)
     + txt(60, 50, '東京 5F', 14, RED)
     + txt(176, 30, '大阪 9F', 14, DGREEN)
     + f'<path d="M150,160 L222,160" stroke-width="2"/><path d="M150,160 L150,150 M222,160 L222,150" stroke-width="2"/>'
     + '<g transform="translate(-16,-4)">'
     + f'<rect x="194" y="148" width="26" height="22" rx="6" fill="{NAVY}"/>'
     + f'<rect x="198" y="152" width="8" height="7" rx="1.5" fill="{SKY}" stroke-width="1"/><rect x="208" y="152" width="8" height="7" rx="1.5" fill="{SKY}" stroke-width="1"/>'
     + f'<circle cx="200" cy="165" r="1.6" fill="{GOLD}" stroke="none"/><circle cx="214" cy="165" r="1.6" fill="{GOLD}" stroke="none"/>'
     + '</g>'
     + sparkle(118, 40) + sparkle(112, 130, 4))
card('stores', '手繪兩棟百貨公司：東京店在 5 樓、大阪店在 9 樓，大阪那棟地下接地鐵', t, bg=SKY)

# 2. 主餐：咖哩、漢堡、蛋包飯（畫成一般的餐點）
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fdf0d8"/>'
     + bottom(120, '#e8c9a0')
     # 咖哩
     + f'<ellipse cx="60" cy="118" rx="46" ry="16" fill="{WHITE}"/>'
     f'<path d="M24,116 Q30,96 56,98 Q60,112 40,122 Z" fill="#fbf6ea"/>'
     f'<path d="M56,100 Q90,98 94,116 Q74,128 46,122 Q62,112 56,100 Z" fill="#c9893a"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="7" height="6" rx="2" fill="{c}" stroke-width="1.1"/>' for x, y, c in [(66, 106, '#f2a46b'), (78, 112, GOLD), (62, 114, '#f2a46b')])
     # 漢堡
     + f'<path d="M126,100 Q150,62 174,100 Z" fill="#e4a95e"/>'
     f'<rect x="124" y="100" width="52" height="7" rx="3" fill="{GREEN}"/>'
     f'<rect x="126" y="107" width="48" height="9" rx="4" fill="{DBROWN}"/>'
     f'<path d="M126,116 L174,116 Q174,126 164,126 L136,126 Q126,126 126,116 Z" fill="#e4a95e"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="2" ry="1.2" fill="{WHITE}" stroke="none"/>' for x, y in [(140, 88), (152, 82), (160, 92)])
     # 蛋包飯
     + f'<ellipse cx="206" cy="126" rx="26" ry="8" fill="{WHITE}"/>'
     f'<path d="M184,124 Q186,98 206,98 Q226,98 228,124 Z" fill="#f7d35c"/>'
     f'<path d="M196,108 q5,-5 10,0 q5,-5 10,0" fill="none" stroke="{RED}" stroke-width="2.4"/>'
     + ''.join(f'<path d="M{x},60 q-5,-6 0,-12 q5,-6 0,-12" fill="none" stroke-width="1.6" opacity=".5"/>' for x in (54, 70, 150))
     + f'<path d="M18,150 L44,150 M196,150 L222,150" stroke-width="1.6" opacity=".5"/>'
     + sparkle(200, 40) + star(110, 30, 6))
card('meal', '手繪三樣主餐：咖哩飯、漢堡、淋了番茄醬的蛋包飯', t, bg='#fdf0d8')

# 3. 甜點：聖代、水果鬆餅
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fde7ea"/>'
     + bottom(130, '#f3c9cf')
     # 聖代
     + f'<path d="M50,140 L94,140 L84,146 L60,146 Z" fill="{SKY}"/>'
     f'<path d="M72,140 L72,120" stroke-width="3"/>'
     f'<path d="M44,62 L100,62 L86,120 L58,120 Z" fill="{SKY}"/>'
     f'<path d="M48,78 L96,78 L93,90 L51,90 Z" fill="#c9893a" stroke="none"/>'
     f'<path d="M52,92 L92,92 L89,104 L55,104 Z" fill="{PINK}" stroke="none"/>'
     f'<path d="M44,62 L100,62 L86,120 L58,120 Z" fill="none"/>'
     f'<path d="M46,62 Q50,42 62,46 Q66,30 80,38 Q96,36 98,62 Z" fill="{WHITE}"/>'
     f'<circle cx="72" cy="34" r="6" fill="{RED}"/><path d="M72,28 q2,-6 6,-8" fill="none" stroke-width="1.4"/>'
     f'<rect x="86" y="30" width="6" height="22" rx="2" fill="#c9893a" transform="rotate(20 89 41)"/>'
     # 鬆餅
     + f'<ellipse cx="166" cy="136" rx="52" ry="10" fill="{WHITE}"/>'
     + ''.join(f'<rect x="126" y="{y}" width="80" height="14" rx="7" fill="#e9b26a"/>' for y in (116, 102, 88))
     + f'<path d="M134,88 Q166,78 198,88 L194,96 Q186,92 182,100 Q176,92 166,98 Q156,92 150,100 Q144,92 134,96 Z" fill="#fbf6ea"/>'
     + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke-width="1.3"/>' for x, y, r, c in [(150, 80, 6, RED), (164, 76, 5, '#7fa9d6'), (178, 80, 6, '#f2a46b'), (190, 84, 4, '#c792d6')])
     + sparkle(130, 40) + sparkle(210, 50) + star(30, 30, 6))
card('sweets', '手繪兩樣甜點：鋪滿奶油與水果的聖代，和疊了三層的水果鬆餅', t, bg='#fde7ea')

# 4. 附杯子的飲料：喝完杯子可以帶回家
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#e6f3ec"/>'
     + bottom(132, '#cfe3d6')
     # 馬克杯
     + f'<path d="M70,82 q22,0 22,18 q0,18 -22,18" fill="none" stroke-width="5"/>'
     f'<rect x="22" y="66" width="52" height="68" rx="10" fill="{WHITE}"/>'
     f'<ellipse cx="48" cy="70" rx="22" ry="5" fill="#c9893a"/>'
     f'<path d="M40,70 q8,-6 16,0" fill="none" stroke="{WHITE}" stroke-width="2"/>'
     f'<path d="M30,96 L66,96" stroke="{PINK}" stroke-width="4"/>'
     # 玻璃杯
     f'<path d="M112,56 L156,56 L150,134 L118,134 Z" fill="#dff3fb"/>'
     f'<path d="M115,86 L153,86 L150,134 L118,134 Z" fill="#f7a8b8" stroke="none" opacity=".9"/>'
     f'<path d="M112,56 L156,56 L150,134 L118,134 Z" fill="none"/>'
     f'<path d="M140,56 L150,30" stroke="{RED}" stroke-width="3"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{WHITE}" stroke-width="1.2" opacity=".9"/>' for x, y in [(122, 92), (136, 102), (126, 112)])
     # 不鏽鋼杯
     + f'<path d="M180,70 L216,70 L212,134 L184,134 Z" fill="{GRAY}"/>'
     f'<path d="M188,76 L192,128" stroke="{WHITE}" stroke-width="3" opacity=".8"/>'
     # 回家的小箭頭與房子
     + f'<path d="M174,30 L190,16 L206,30 L206,46 L174,46 Z" fill="{GOLD}"/>'
     f'<path d="M150,40 q10,-14 20,-4" fill="none" stroke="{RED}" stroke-width="2"/><path d="M166,30 L171,37 L163,38" fill="none" stroke="{RED}" stroke-width="2"/>'
     + sparkle(30, 30) + sparkle(96, 30, 4))
card('cup', '手繪三種附杯子的飲料：馬克杯、玻璃杯和不鏽鋼杯，旁邊畫一個小房子表示可以帶回家', t, bg='#e6f3ec')

# 5. 池袋的外帶甜點店：不用預約
t = (f'<rect x="3" y="3" width="234" height="174" rx="22" fill="#fff0dc"/>'
     f'<path d="M22,40 L218,40 L210,64 L30,64 Z" fill="{GOLD}"/>'
     + ''.join(f'<path d="M{30+i*20},40 L{38+i*20},64" stroke-width="1.2" opacity=".6"/>' for i in range(9))
     + f'<path d="M30,64 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0" fill="{WHITE}" stroke-width="1.6"/>'
     + f'<rect x="30" y="96" width="180" height="50" rx="4" fill="#f6e3c8"/>'
     + f'<rect x="38" y="104" width="164" height="22" rx="3" fill="{SKY}"/>'
     + ''.join(f'<circle cx="{x}" cy="116" r="7" fill="{c}" stroke-width="1.3"/>' for x, c in [(56, PINK), (82, '#c9893a'), (108, GOLD), (134, PINK), (160, '#f2a46b'), (184, '#c9893a')])
     # 外帶紙袋與盒子
     + f'<rect x="170" y="140" width="34" height="30" rx="3" fill="{WHITE}"/><path d="M178,140 q9,-14 18,0" fill="none" stroke-width="2"/>'
     + f'<rect x="132" y="150" width="30" height="20" rx="3" fill="{PINK}"/><path d="M147,150 L147,170 M132,160 L162,160" stroke="{WHITE}" stroke-width="2"/>'
     # 不用預約：沒有日曆的時鐘 → 畫一個「隨時來」的打勾
     + f'<circle cx="54" cy="158" r="12" fill="{GREEN}"/><path d="M48,158 L53,163 L61,153" fill="none" stroke="{WHITE}" stroke-width="3"/>'
     + sparkle(214, 22) + star(26, 22, 6))
card('takeout', '手繪外帶甜點店的櫃台，玻璃櫃裡擺著甜點，旁邊是外帶紙袋和盒子', t, bg='#fff0dc')


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('pc-' + name, 120, 120, label, inner, bg='#fff3c4')


# 認證碼信不見了：按重新寄送；信箱打錯：回上一頁
rem('r-mailcode', '手繪提醒：信封裡的驗證碼和一個往回的箭頭',
    f'<rect x="10" y="40" width="66" height="46" rx="5" fill="{WHITE}"/>'
    f'<path d="M10,42 L43,66 L76,42" fill="none" stroke-width="2"/>'
    f'<rect x="20" y="68" width="46" height="14" rx="3" fill="{GOLD}" stroke-width="1.4"/>'
    + txt(43, 79, '1 2 3 4', 10)
    + f'<path d="M100,30 a14,14 0 1 1 -14,14" fill="none" stroke="{RED}" stroke-width="3"/>'
    f'<path d="M80,40 L86,46 L92,38" fill="none" stroke="{RED}" stroke-width="3"/>'
    + star(96, 96, 8))

# 拆成兩筆還想坐在一起
rem('r-together', '手繪提醒：兩組人的桌子靠在一起',
    f'<rect x="10" y="62" width="46" height="12" rx="4" fill="{BROWN}"/><path d="M18,74 L18,96 M48,74 L48,96" stroke-width="3"/>'
    f'<rect x="64" y="62" width="46" height="12" rx="4" fill="{BROWN}"/><path d="M72,74 L72,96 M102,74 L102,96" stroke-width="3"/>'
    + ''.join(f'<circle cx="{x}" cy="40" r="6" fill="#f9d9c0"/><path d="M{x-8},62 q0,-14 8,-14 q8,0 8,14 Z" fill="{c}"/>' for x, c in [(22, SKY), (42, PINK), (76, GOLD), (96, GREEN)])
    + f'<path d="M48,22 q12,-10 24,0" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    f'<path d="M50,104 L70,104" stroke="{RED}" stroke-width="3"/><path d="M50,98 L44,104 L50,110 M70,98 L76,104 L70,110" fill="none" stroke="{RED}" stroke-width="2.4"/>')

# 附杯子的飲料：點了之後不能改冷熱
rem('r-cup', '手繪提醒：杯子旁邊的冰塊和熱氣，中間打叉',
    f'<path d="M64,50 q16,0 16,14 q0,14 -16,14" fill="none" stroke-width="4"/>'
    f'<rect x="20" y="40" width="48" height="56" rx="9" fill="{WHITE}"/>'
    f'<path d="M30,58 L58,58" stroke="{PINK}" stroke-width="4"/>'
    f'<rect x="88" y="20" width="12" height="12" rx="2" fill="#dff3fb"/><rect x="100" y="30" width="10" height="10" rx="2" fill="#dff3fb"/>'
    f'<path d="M30,34 q-4,-6 0,-12 q4,-6 0,-12 M44,34 q-4,-6 0,-12 q4,-6 0,-12" fill="none" stroke-width="1.6" opacity=".6"/>'
    f'<path d="M84,70 L104,90 M104,70 L84,90" stroke="{RED}" stroke-width="4"/>')

print(save(F, OUT), 'files')
