# Burton 宅配租雪板頁（/japan-burton-rental/）的「租到的東西」插圖與提醒卡（2026-11-13）。
# 依 Burton 日本官網租借頁與 Kauriru 規約（burton-rental.json）的內容畫成可愛版；不畫 Burton 的商標，雪板與箱子都是一般樣子。
# 輸出 illust/sp/japan-burton-rental/*.svg（240×180、提醒小圖 120×120）。
# 說明文字放在 illust/spots/japan-burton-rental.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-burton-rental')
W, H = 240, 180
BOARD = '#7fc4b8'
BOOT = '#4a4f63'
BAG = '#5d6b8a'
BOX = '#d9b07a'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('bt-' + name, W, H, label, inner, bg=bg)


def full(col):
    return f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{col}"/>'


def bottom(path_top, col):
    return f'<path d="{path_top} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def board(x, y, w, h, col=BOARD, rot=0):
    r = h / 2
    return (f'<g transform="rotate({rot} {x + w/2} {y + h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{col}"/>'
            f'<path d="M{x + r},{y + h*.3:.1f} L{x + w - r},{y + h*.3:.1f}" stroke="{WHITE}" stroke-width="2" opacity=".8"/></g>')


def binding(x, y, s=1.0):
    return (f'<path d="M{x - 12*s:.1f},{y} L{x + 12*s:.1f},{y} L{x + 10*s:.1f},{y - 10*s:.1f} L{x - 14*s:.1f},{y - 14*s:.1f} Z" fill="{INK}" stroke-width="1.6"/>'
            f'<path d="M{x - 14*s:.1f},{y - 14*s:.1f} L{x - 16*s:.1f},{y - 22*s:.1f}" stroke-width="{3*s:.1f}"/>')


def boot(x, y, s=1.0, col=BOOT):
    # 側面的雪鞋，鞋頭朝右
    return (f'<path d="M{x},{y} L{x},{y - 30*s:.1f} Q{x},{y - 36*s:.1f} {x + 8*s:.1f},{y - 36*s:.1f} L{x + 18*s:.1f},{y - 36*s:.1f} '
            f'L{x + 20*s:.1f},{y - 16*s:.1f} Q{x + 36*s:.1f},{y - 14*s:.1f} {x + 38*s:.1f},{y - 4*s:.1f} L{x + 38*s:.1f},{y} Z" fill="{col}"/>'
            f'<path d="M{x - 1},{y - 2*s:.1f} L{x + 39*s:.1f},{y - 2*s:.1f}" stroke-width="{3*s:.1f}"/>'
            f'<path d="M{x + 6*s:.1f},{y - 28*s:.1f} L{x + 16*s:.1f},{y - 28*s:.1f} M{x + 6*s:.1f},{y - 22*s:.1f} L{x + 16*s:.1f},{y - 22*s:.1f}" stroke="{WHITE}" stroke-width="1.6"/>')


def person(x, y, col=RED, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{7*s:.1f}" fill="#f9d9c0"/>'
            f'<path d="M{x - 7*s:.1f},{y - 3*s:.1f} Q{x},{y - 13*s:.1f} {x + 7*s:.1f},{y - 3*s:.1f} Z" fill="{col}"/>'
            f'<path d="M{x - 9*s:.1f},{y + 26*s:.1f} q0,{-17*s:.1f} {9*s:.1f},{-17*s:.1f} q{9*s:.1f},0 {9*s:.1f},{17*s:.1f} Z" fill="{col}"/>')


def snowy_hills():
    return (f'<path d="M3,96 L50,40 L80,70 L120,24 L170,80 L200,52 L237,90 L237,120 L3,120 Z" fill="#e8eef7"/>'
            f'<path d="M50,40 L40,52 L48,50 L56,56 L62,50 Z M120,24 L108,40 L118,36 L126,44 L134,38 Z" fill="{WHITE}"/>')


# 1. 三件組：雪板、固定器、鞋子裝在同一個板袋裡
card('set', '手繪打開的板袋，裡面有雪板、固定器和一雙雪鞋',
     full(SKY)
     + f'<rect x="16" y="40" width="208" height="62" rx="31" fill="{BAG}"/>'
     + f'<path d="M30,44 Q120,30 210,44" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-dasharray="4 3"/>'
     + board(28, 52, 184, 40)
     + binding(88, 80, .9) + binding(152, 80, .9)
     + face(120, 70, .8)
     + boot(60, 160, 1.1) + boot(126, 160, 1.1)
     + f'<path d="M30,166 L210,166" stroke-width="2" opacity=".4"/>'
     + sparkle(200, 130) + sparkle(30, 22) + star(214, 22, 7))

# 2. STEP ON：踩進去就固定，拉起後跟的拉桿就鬆開
card('stepon', '手繪雪鞋往下踩進固定器，旁邊畫著後跟的拉桿往上拉',
     full(SKY)
     + board(16, 130, 208, 26)
     + f'<path d="M64,128 L150,128 L146,116 L60,112 Z" fill="{INK}"/>'
     + f'<path d="M60,112 L56,92" stroke-width="4"/>'
     + boot(70, 98, 1.6)
     + f'<path d="M110,20 L110,40 M100,32 L110,42 L120,32" stroke="{GREEN}" stroke-width="4" fill="none"/>'
     + f'<rect x="44" y="84" width="10" height="24" rx="4" fill="{GOLD}" transform="rotate(-12 49 96)"/>'
     + f'<path d="M40,78 L40,50 M32,58 L40,50 L48,58" stroke="{RED}" stroke-width="4" fill="none"/>'
     + face(110, 76, .8)
     + sparkle(190, 40) + sparkle(210, 80))

# 3. 宅配到飯店：卡車送來長長的箱子
card('hotel', '手繪宅配卡車把雪具送到飯店門口',
     full(SKY)
     + f'<rect x="132" y="30" width="92" height="120" rx="4" fill="#f3e3c3"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="16" height="14" rx="2" fill="{SKY}"/>' for x in (142, 168, 194) for y in (42, 68, 94))
     + f'<rect x="164" y="120" width="28" height="30" fill="{BROWN}"/><path d="M156,120 L200,120 L196,112 L160,112 Z" fill="{RED}"/>'
     + bottom('M3,150 L237,150', '#d8dde6')
     + f'<rect x="14" y="84" width="72" height="52" rx="5" fill="{WHITE}"/>'
     + f'<path d="M86,98 L110,98 L122,116 L122,136 L86,136 Z" fill="{GOLD}"/><path d="M92,102 L108,102 L116,114 L92,114 Z" fill="{SKY}"/>'
     + f'<circle cx="34" cy="140" r="9" fill="{INK}"/><circle cx="104" cy="140" r="9" fill="{INK}"/>'
     + face(50, 108, .8)
     + f'<rect x="126" y="130" width="40" height="18" rx="3" fill="{BAG}" transform="rotate(-8 146 139)"/>'
     + sparkle(30, 30) + sparkle(90, 50))

# 4. 只有 7、15、30 天三種方案
cal = lambda x, n, col: (f'<rect x="{x}" y="50" width="62" height="70" rx="6" fill="{WHITE}"/>'
                         f'<rect x="{x}" y="50" width="62" height="18" rx="6" fill="{col}"/>'
                         f'<path d="M{x + 14},44 L{x + 14},56 M{x + 48},44 L{x + 48},56" stroke-width="3"/>'
                         f'<text x="{x + 31}" y="106" font-size="30" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">{n}</text>')
card('days', '手繪三本月曆，分別寫著 7、15、30',
     full(CREAM)
     + cal(16, 7, RED) + cal(89, 15, GREEN) + cal(162, 30, NAVY)
     + f'<path d="M30,146 q10,-10 20,0 t20,0" fill="none" stroke="{BOARD}" stroke-width="4"/>'
     + board(150, 136, 70, 16)
     + face(47, 124, .7, blush=False)
     + sparkle(120, 24) + sparkle(220, 24) + star(20, 24, 6))

# 5. 小孩套組：大人和小孩各一塊板
card('kids', '手繪大人和小孩站在雪地上，各拿一塊大小不同的雪板',
     full(SKY)
     + snowy_hills()
     + bottom('M3,120 Q120,108 237,120', WHITE)
     + person(84, 82, RED, 1.2) + board(110, 52, 18, 96, BOARD, 0)
     + person(160, 108, GOLD, .8) + board(180, 92, 13, 60, '#f6a5ad', 0)
     + face(84, 84, .6, blush=False) + face(160, 110, .45, blush=False)
     + snow([(30, 30), (200, 20), (60, 60), (220, 70), (150, 40)], 2.6, WHITE)
     + sparkle(30, 140))


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('bt-' + name, 120, 120, label, inner, bg='#fff3c4')


# 收貨日就是租借開始日，建議選滑雪前一天
rem('r-day', '手繪提醒：月曆上滑雪前一天就收貨',
    f'<rect x="10" y="22" width="100" height="74" rx="6" fill="{WHITE}"/><rect x="10" y="22" width="100" height="16" rx="6" fill="{RED}"/>'
    + ''.join(f'<rect x="{18 + 30*i}" y="48" width="24" height="38" rx="4" fill="{c}"/>' for i, c in enumerate((GOLD, SKY, SKY)))
    + f'<rect x="22" y="58" width="16" height="12" rx="2" fill="{BOX}" stroke-width="1.4"/>'
    + board(52, 62, 20, 10) + board(82, 62, 20, 10)
    + f'<path d="M30,100 L30,112 M24,106 L30,112 L36,106" stroke="{GREEN}" stroke-width="3" fill="none"/>')

# 收到後 24 小時內要檢查
rem('r-check', '手繪提醒：收到板袋馬上打開檢查',
    f'<rect x="12" y="54" width="70" height="44" rx="10" fill="{BAG}"/><path d="M18,58 Q46,46 76,58" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="4 3"/>'
    f'<circle cx="80" cy="44" r="18" fill="{SKY}"/><circle cx="80" cy="44" r="18" fill="none" stroke-width="3"/>'
    f'<path d="M93,57 L108,72" stroke-width="5"/>'
    f'<path d="M72,44 l6,6 l10,-12" stroke="{GREEN}" stroke-width="3" fill="none"/>'
    f'<circle cx="28" cy="28" r="14" fill="{WHITE}"/><path d="M28,28 L28,18 M28,28 L35,31" stroke-width="2.2"/>')

# 最後一天交給物流就算還了
rem('r-return', '手繪提醒：最後一天把板袋交給物流',
    f'<rect x="8" y="40" width="58" height="40" rx="10" fill="{BAG}"/>'
    f'<rect x="20" y="50" width="24" height="16" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
    f'<path d="M24,55 L40,55 M24,60 L36,60" stroke-width="1.2"/>'
    f'<path d="M70,60 L84,60 M78,54 L84,60 L78,66" stroke="{GREEN}" stroke-width="3" fill="none"/>'
    f'<circle cx="100" cy="46" r="8" fill="#f9d9c0"/><path d="M90,42 Q100,32 110,42 Z" fill="{GOLD}"/>'
    f'<path d="M90,84 q0,-28 10,-28 q10,0 10,28 Z" fill="{GOLD}"/>'
    f'<rect x="20" y="88" width="80" height="20" rx="4" fill="{WHITE}"/>'
    + ''.join(f'<rect x="{24 + 13*i}" y="92" width="10" height="12" rx="2" fill="{RED if i == 5 else GRAY}" stroke-width="1"/>' for i in range(6)))

print(save(F, OUT), 'files')
