# 大相撲門票頁（/japan-sumo/）的「土俵和座位」插圖與提醒卡（2026-11-13）。
# 只畫一般的力士與場館（不像任何真實力士），座位與規定依 sumo.json（チケット大相撲英文站與日文席種頁原文）。
# sumo.or.jp 日文頁會 403，所以不另外參考協會官網照片。
# 輸出 illust/sp/japan-sumo/*.svg（240×180、提醒小圖 120×120）。
# 說明文字放在 illust/spots/japan-sumo.json。
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'japan-sumo')
W, H = 240, 180
CLAY = '#e2c08f'
STRAW = '#c9b26a'
SKIN = '#f9d9c0'
MAWASHI = ['#34416e', '#8a4f9e', '#3f8a63', '#c0504a']
ROOF = '#6f6a72'
TASSELS = [GREEN, RED, WHITE, NAVY]
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('sm-' + name, W, H, label, inner, bg=bg)


def full(col):
    return f'<rect x="3" y="3" width="234" height="174" rx="22" fill="{col}"/>'


def rikishi(x, y, s=1.0, col=MAWASHI[0], flip=False, crouch=False):
    # 圓滾滾的力士：頭頂髮髻、圓肚子、腰上兜襠布（まわし）
    d = -1 if flip else 1
    t = ''
    body_y = y + (6 if crouch else 0) * s
    t += f'<ellipse cx="{x}" cy="{body_y + 28*s:.1f}" rx="{24*s:.1f}" ry="{26*s:.1f}" fill="{SKIN}"/>'
    t += f'<path d="M{x - 23*s:.1f},{body_y + 36*s:.1f} Q{x},{body_y + 44*s:.1f} {x + 23*s:.1f},{body_y + 36*s:.1f} L{x + 20*s:.1f},{body_y + 48*s:.1f} Q{x},{body_y + 56*s:.1f} {x - 20*s:.1f},{body_y + 48*s:.1f} Z" fill="{col}"/>'
    if crouch:
        t += f'<path d="M{x - 18*s:.1f},{body_y + 50*s:.1f} q{-6*s:.1f},{10*s:.1f} {-2*s:.1f},{14*s:.1f} M{x + 18*s:.1f},{body_y + 50*s:.1f} q{6*s:.1f},{10*s:.1f} {2*s:.1f},{14*s:.1f}" stroke-width="2.4" fill="none"/>'
        t += f'<path d="M{x + d*20*s:.1f},{body_y + 24*s:.1f} q{d*14*s:.1f},{10*s:.1f} {d*12*s:.1f},{36*s:.1f}" stroke-width="2.4" fill="none"/>'
    else:
        t += f'<rect x="{x - 16*s:.1f}" y="{body_y + 50*s:.1f}" width="{11*s:.1f}" height="{14*s:.1f}" rx="4" fill="{SKIN}"/>'
        t += f'<rect x="{x + 5*s:.1f}" y="{body_y + 50*s:.1f}" width="{11*s:.1f}" height="{14*s:.1f}" rx="4" fill="{SKIN}"/>'
    hy = y - 2 * s
    t += f'<circle cx="{x + d*4*s:.1f}" cy="{hy:.1f}" r="{14*s:.1f}" fill="{SKIN}"/>'
    t += f'<path d="M{x + d*4*s - 13*s:.1f},{hy - 4*s:.1f} Q{x + d*4*s:.1f},{hy - 18*s:.1f} {x + d*4*s + 13*s:.1f},{hy - 4*s:.1f} Q{x + d*4*s:.1f},{hy - 10*s:.1f} {x + d*4*s - 13*s:.1f},{hy - 4*s:.1f} Z" fill="{INK}"/>'
    t += f'<ellipse cx="{x + d*4*s:.1f}" cy="{hy - 17*s:.1f}" rx="{7*s:.1f}" ry="{3.4*s:.1f}" fill="{INK}"/>'
    t += face(x + d*6*s, hy + 2*s, .75 * s)
    return t


def roof(y=16):
    t = f'<path d="M40,{y + 20} L120,{y} L200,{y + 20} Z" fill="{ROOF}"/><rect x="48" y="{y + 20}" width="144" height="6" fill="{DBROWN}"/>'
    for i, x in enumerate((52, 188)):
        t += f'<path d="M{x},{y + 26} L{x},{y + 40}" stroke-width="2"/><circle cx="{x}" cy="{y + 44}" r="5" fill="{TASSELS[i]}"/>'
    return t


def head(x, y, col=PINK, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{6*s:.1f}" fill="{SKIN}"/>'
            f'<path d="M{x - 7*s:.1f},{y + 18*s:.1f} q0,{-11*s:.1f} {7*s:.1f},{-11*s:.1f} q{7*s:.1f},0 {7*s:.1f},{11*s:.1f} Z" fill="{col}"/>')


# 1. 土俵：架高的土台、草袋圍成的圓圈，兩位力士蹲低準備
card('dohyo', '手繪土俵，兩位圓滾滾的力士蹲低面對面，上面吊著屋頂',
     full(CREAM)
     + roof(10)
     + f'<path d="M14,150 L40,118 L200,118 L226,150 Z" fill="{CLAY}"/>'
     + f'<rect x="14" y="150" width="212" height="14" fill="#cfa772"/>'
     + f'<ellipse cx="120" cy="134" rx="78" ry="14" fill="none" stroke="{STRAW}" stroke-width="5"/>'
     + f'<path d="M110,132 L110,138 M130,132 L130,138" stroke="{WHITE}" stroke-width="3"/>'
     + rikishi(78, 64, .9, MAWASHI[0], crouch=True) + rikishi(162, 64, .9, MAWASHI[1], flip=True, crouch=True)
     + sparkle(24, 30) + sparkle(216, 30))

# 2. 枡席：地板上一格一格的方格，4 個人坐坐墊
masu = ''
for j, y in enumerate((86, 122)):
    for i, x in enumerate((14, 90, 166)):
        masu += f'<rect x="{x}" y="{y}" width="64" height="32" fill="#f3e3c3"/>'
        for k in range(4):
            if (i, j) == (1, 1):
                continue
            cx = x + 10 + 15 * k
            masu += f'<rect x="{cx - 6}" y="{y + 18}" width="12" height="9" rx="2" fill="{[RED, PINK, SKY, GOLD][(k + i + j) % 4]}" stroke-width="1.2"/>'
card('masu', '手繪枡席，地板上一格一格的方格，一格坐四個人',
     full(CREAM)
     + f'<path d="M3,80 L237,80" stroke-width="2"/>'
     + f'<path d="M60,74 L180,74 L196,30 L44,30 Z" fill="{CLAY}"/>'
     + f'<ellipse cx="120" cy="52" rx="44" ry="10" fill="none" stroke="{STRAW}" stroke-width="3"/>'
     + masu
     + head(100, 130, PINK, .75) + head(115, 128, SKY, .75) + head(130, 130, GOLD, .75) + head(145, 128, GREEN, .75)
     + f'<rect x="90" y="122" width="64" height="32" fill="none" stroke="{RED}" stroke-width="3"/>'
     + sparkle(20, 20))

# 3. 椅子席：後面一排排的椅子
card('chair', '手繪椅子席，一排一排的椅子，每個人一張',
     full(CREAM)
     + ''.join(f'<path d="M14,{y} L226,{y}" stroke-width="2"/>' for y in (70, 112, 154))
     + ''.join(f'<rect x="{x}" y="{y - 22}" width="22" height="22" rx="4" fill="{c}"/>'
               f'<rect x="{x - 2}" y="{y - 6}" width="26" height="6" rx="2" fill="{c}"/>'
               for row, y in enumerate((70, 112, 154)) for k, (x, c) in enumerate(
                   [(20 + 30 * n + (row % 2) * 10, [RED, GOLD, SKY][row]) for n in range(7)]))
     + head(60, 74, PINK, .9) + head(130, 116, GREEN, .9) + head(170, 32, NAVY, .9) + head(100, 32, RED, .9)
     + face(130, 116, .6, blush=False)
     + sparkle(120, 14))

# 4. 溜席：土俵旁邊坐地上的位子，不能拍照、用手機、吃東西
card('tamari', '手繪溜席，觀眾直接坐在土俵旁邊，旁邊有不能用手機的標誌',
     full(CREAM)
     + f'<path d="M40,110 L70,60 L230,60 L230,110 Z" fill="{CLAY}"/>'
     + f'<rect x="40" y="110" width="190" height="12" fill="#cfa772"/>'
     + f'<path d="M84,92 Q150,70 216,92" fill="none" stroke="{STRAW}" stroke-width="5"/>'
     + rikishi(170, 28, .62, MAWASHI[2])
     + ''.join(head(x, 136, c, .9) + f'<rect x="{x - 9}" y="152" width="18" height="8" rx="2" fill="{GRAY}"/>' for x, c in [(70, PINK), (100, SKY), (130, GOLD), (160, GREEN), (190, RED)])
     + f'<rect x="14" y="28" width="22" height="36" rx="4" fill="{NAVY}"/><rect x="18" y="33" width="14" height="24" rx="2" fill="{WHITE}"/>'
     + f'<circle cx="25" cy="46" r="20" fill="none" stroke="{RED}" stroke-width="4"/><path d="M11,32 L39,60" stroke="{RED}" stroke-width="4"/>')

# 5. 一天的時間：一大早開門，幕內力士下午才上場
card('day', '手繪時鐘指著下午兩點，力士走上場',
     full(SKY)
     + f'<circle cx="64" cy="74" r="44" fill="{WHITE}"/>'
     + ''.join(f'<path d="M{64 + 36*math.cos(a):.1f},{74 + 36*math.sin(a):.1f} L{64 + 40*math.cos(a):.1f},{74 + 40*math.sin(a):.1f}" stroke-width="2"/>'
               for a in [i * math.pi / 6 for i in range(12)])
     + f'<path d="M64,74 L{64 + 22*math.cos(math.radians(-30)):.1f},{74 + 22*math.sin(math.radians(-30)):.1f}" stroke-width="3.4"/>'
     + f'<path d="M64,74 L64,42" stroke-width="2.4"/><circle cx="64" cy="74" r="3" fill="{INK}"/>'
     + f'<path d="M3,140 L237,140 L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{CLAY}"/>'
     + rikishi(170, 70, .95, MAWASHI[3])
     + f'<path d="M134,150 l6,-6 M206,150 l-6,-6" stroke-width="2"/>'
     + sparkle(130, 26) + sparkle(220, 40) + sparkle(30, 150))


# ---- 提醒卡的手繪小圖（120×120 正方，米黃底）----
def rem(name, label, inner):
    F[name] = svg('sm-' + name, 120, 120, label, inner, bg='#fff3c4')


# 只能在日本的超商印票，座位號碼印出來才知道
rem('r-print', '手繪提醒：在日本的超商機台印票，座位號碼印出來才知道',
    f'<rect x="14" y="30" width="56" height="74" rx="5" fill="{GRAY}"/><rect x="22" y="38" width="40" height="26" rx="3" fill="{SKY}"/>'
    f'<rect x="24" y="74" width="36" height="6" rx="2" fill="{INK}" stroke="none"/>'
    f'<rect x="68" y="44" width="40" height="58" rx="3" fill="{WHITE}" transform="rotate(10 88 73)"/>'
    f'<text x="90" y="86" font-size="26" font-weight="bold" text-anchor="middle" fill="{RED}" stroke="none" font-family="sans-serif">?</text>'
    + star(96, 30, 7))

# 兩國國技館只能再入場一次，17:00 前回來
rem('r-reentry', '手繪提醒：出去只能再進來一次，時鐘指著五點',
    f'<rect x="14" y="30" width="44" height="72" rx="4" fill="{BROWN}"/><circle cx="50" cy="68" r="3" fill="{GOLD}"/>'
    f'<path d="M20,104 L52,104" stroke-width="2"/>'
    f'<circle cx="34" cy="20" r="10" fill="{GOLD}"/>'
    f'<text x="34" y="25" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">1</text>'
    f'<circle cx="86" cy="70" r="24" fill="{WHITE}"/>'
    f'<path d="M86,70 L86,52 M86,70 L{86 + 14*math.cos(math.radians(60)):.1f},{70 + 14*math.sin(math.radians(60)):.1f}" stroke-width="2.6"/>'
    f'<path d="M60,40 q14,-14 28,-4" fill="none" stroke="{GREEN}" stroke-width="3"/><path d="M84,32 L90,37 L83,41" fill="none" stroke="{GREEN}" stroke-width="3"/>')

# 4 歲以上就要買票
rem('r-age', '手繪提醒：小孩也要一張票',
    f'<circle cx="40" cy="44" r="14" fill="{SKIN}"/>' + face(40, 46, .7)
    + f'<path d="M26,96 q0,-36 14,-36 q14,0 14,36 Z" fill="{SKY}"/>'
    + f'<rect x="64" y="50" width="44" height="28" rx="4" fill="{GOLD}"/><path d="M76,50 L76,78" stroke-width="1.6" stroke-dasharray="3 3"/>'
    + f'<text x="94" y="70" font-size="16" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none" font-family="sans-serif">4+</text>'
    + star(84, 30, 6))

print(save(F, OUT), 'files')
