# 台日 Apple 價差頁的「在日本買會遇到的場景」插圖與提醒卡（2026-11-13）。
# 手機一律畫一般圓角長方形，不畫蘋果標誌、不畫可辨識的機身設計；店面畫一般的玻璃店面與量販店外觀，不畫任何店家招牌。
# 說明依頁面 apple.json、gen.py 的常見問題與 /japan-tax-free-2026/ 引的觀光廳、海關說明。
# 輸出 illust/sp/apple-japan-price/*.svg，說明文字在 illust/spots/apple-japan-price.json。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sp', 'apple-japan-price')
W, H = 240, 180
GLASS = '#e6f2fa'
LILAC = '#e7defa'
F = {}


def card(name, label, inner, bg=CREAM):
    F[name] = svg('ap-' + name, W, H, label, inner, bg=bg)


def phone(x, y, w=44, h=80, body=LILAC, scr=SKY, smile=True):
    # 一般的圓角長方形手機：外殼＋螢幕＋上方一條小膠囊，不畫任何品牌細節
    r = w * .2
    t = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r:.1f}" fill="{body}"/>'
         f'<rect x="{x+4}" y="{y+5}" width="{w-8}" height="{h-10}" rx="{r*.7:.1f}" fill="{scr}" stroke-width="1.6"/>'
         f'<rect x="{x+w/2-5:.1f}" y="{y+8}" width="10" height="3" rx="1.5" fill="{INK}" stroke="none"/>')
    if smile:
        t += face(x + w / 2, y + h * .52, .7 * w / 44)
    return t


def person(x, y, col=RED, s=1.0, hair=DBROWN):
    return (f'<path d="M{x-7*s},{y+22*s} q0,{-14*s} {7*s},{-14*s} q{7*s},0 {7*s},{14*s} Z" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="{6*s}" fill="#f9d9c0"/>'
            f'<path d="M{x-6*s},{y-1*s} q{6*s},{-10*s} {12*s},0 q{-6*s},{-4*s} {-12*s},0 Z" fill="{hair}" stroke-width="1.4"/>')


def passport(x, y, s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{28*s}" height="{38*s}" rx="{3*s}" fill="{NAVY}"/>'
            f'<circle cx="{x+14*s}" cy="{y+17*s}" r="{6.5*s}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<path d="M{x+8*s},{y+31*s} L{x+20*s},{y+31*s}" stroke="{GOLD}" stroke-width="1.6"/>')


def suitcase(x, y, col=SKY, s=1.0):
    return (f'<path d="M{x+10*s},{y} L{x+10*s},{y-8*s} L{x+22*s},{y-8*s} L{x+22*s},{y}" fill="none" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{32*s}" height="{40*s}" rx="{5*s}" fill="{col}"/>'
            f'<path d="M{x+10*s},{y+4*s} L{x+10*s},{y+36*s} M{x+22*s},{y+4*s} L{x+22*s},{y+36*s}" stroke-width="1.4" opacity=".6"/>'
            f'<circle cx="{x+6*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>'
            f'<circle cx="{x+26*s}" cy="{y+43*s}" r="{2.6*s}" fill="{INK}" stroke="none"/>')


def floor(y=150, col='#e9dcc8'):
    return f'<path d="M3,{y} L237,{y} L237,155 Q237,177 215,177 L25,177 Q3,177 3,155 Z" fill="{col}"/>'


def check(x, y, s=1.0, col=GREEN):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{col}"/>'
            f'<path d="M{x-5*s},{y} L{x-1*s},{y+4*s} L{x+6*s},{y-5*s}" fill="none" stroke="{WHITE}" stroke-width="3"/>')


def cross(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{11*s}" fill="{RED}"/>'
            f'<path d="M{x-5*s},{y-5*s} L{x+5*s},{y+5*s} M{x+5*s},{y-5*s} L{x-5*s},{y+5*s}" stroke="{WHITE}" stroke-width="3"/>')


def label(x, y, txt, size=12, col=INK):
    return (f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="bold" '
            f'text-anchor="middle" fill="{col}" stroke="none">{txt}</text>')


# 1. 直營店：一般的玻璃店面、木頭長桌上擺著手機，沒有招牌
card('directstore', '手繪一般的手機直營店，玻璃店面裡有擺著手機的木頭長桌',
     floor(150)
     + f'<rect x="22" y="34" width="196" height="116" rx="6" fill="{GLASS}"/>'
     + f'<rect x="18" y="26" width="204" height="14" rx="5" fill="{GRAY}"/>'
     + ''.join(f'<path d="M{x},40 L{x},150" stroke-width="1.6" opacity=".7"/>' for x in (71, 120, 169))
     + f'<path d="M40,52 L60,52 M140,56 L156,56" stroke="{WHITE}" stroke-width="3" opacity=".9"/>'
     + f'<rect x="40" y="112" width="160" height="9" rx="3" fill="{BROWN}"/>'
     + f'<path d="M52,121 L52,148 M188,121 L188,148" stroke-width="3"/>'
     + phone(56, 88, 16, 26, smile=False) + phone(92, 86, 18, 28) + phone(132, 88, 16, 26, PINK, smile=False)
     + phone(166, 88, 16, 26, '#d8ecd8', smile=False)
     + person(96, 124, PINK, 1.0) + person(150, 126, GOLD, .9, INK)
     + sparkle(206, 18, 5) + star(30, 18, 6))

# 2. 家電量販店：好幾層樓、彩色橫條招牌（不寫店名），門口掛 TAX FREE 牌子
card('bigstore', '手繪多層樓的家電量販店，門口掛著 TAX FREE 的牌子，有人提著購物袋',
     floor(152)
     + f'<rect x="44" y="18" width="152" height="134" rx="4" fill="#f4efe6"/>'
     + f'<rect x="44" y="18" width="152" height="14" rx="3" fill="{RED}"/>'
     + f'<rect x="44" y="52" width="152" height="12" fill="{GOLD}"/>'
     + f'<rect x="44" y="84" width="152" height="12" fill="{SKY}"/>'
     + ''.join(f'<rect x="{x}" y="{y}" width="20" height="12" rx="2" fill="{GLASS}" stroke-width="1.4"/>'
               for y in (36, 68) for x in (54, 82, 110, 138, 166))
     + f'<rect x="96" y="112" width="48" height="40" rx="3" fill="{GLASS}"/>'
     + f'<path d="M120,112 L120,152" stroke-width="1.6"/>'
     + f'<path d="M70,98 L70,104 M110,98 L110,104" stroke-width="1.6"/>'
     + f'<rect x="56" y="104" width="68" height="20" rx="6" fill="{WHITE}"/>'
     + label(90, 118, 'TAX FREE', 11, RED)
     + person(30, 130, GREEN, .95) + f'<path d="M22,140 l-4,14 l12,0 Z" fill="{PINK}" stroke-width="1.4"/>'
     + person(214, 128, PINK, 1.0, INK) + f'<rect x="220" y="140" width="12" height="13" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     + sparkle(24, 30) + sparkle(216, 34, 4))

# 3. 先付全額、出境後才退：收銀台＋收據＋護照，虛線箭頭飛到飛機再退回來
card('payfirst', '手繪收銀台上的收據和護照，箭頭連到飛機，再有錢幣退回來',
     floor(150, '#efe3cf')
     + f'<rect x="14" y="108" width="132" height="42" rx="4" fill="{BROWN}"/>'
     + f'<rect x="22" y="70" width="44" height="38" rx="5" fill="{GRAY}"/>'
     + f'<rect x="28" y="76" width="32" height="12" rx="2" fill="{WHITE}" stroke-width="1.4"/>'
     + ''.join(f'<circle cx="{x}" cy="98" r="2" fill="{INK}" stroke="none"/>' for x in (32, 40, 48, 56))
     + f'<path d="M74,108 L74,64 L104,64 L104,108 Z" fill="{WHITE}"/>'
     + ''.join(f'<path d="M80,{y} L98,{y}" stroke-width="1.4"/>' for y in (74, 82, 90))
     + f'<path d="M80,99 L98,99" stroke="{RED}" stroke-width="2.6"/>'
     + passport(112, 72, .85)
     + f'<path d="M110,56 Q150,18 186,40" fill="none" stroke-width="2" stroke-dasharray="5 5"/>'
     + f'<g transform="translate(196,46) rotate(-20)"><path d="M-22,0 L22,0 Q30,0 30,4 Q30,8 22,8 L-22,8 Z" fill="{WHITE}"/>'
       f'<path d="M-4,4 L-14,-14 L-6,-14 L10,4 Z M-4,6 L-12,22 L-4,22 L10,6 Z" fill="{SKY}"/>'
       f'<path d="M-22,2 L-28,-8 L-22,-8 L-14,2 Z" fill="{SKY}"/></g>'
     + f'<path d="M212,72 Q214,112 172,124" fill="none" stroke="{GREEN}" stroke-width="2.6"/>'
     + f'<path d="M178,116 L170,125 L181,130" fill="none" stroke="{GREEN}" stroke-width="2.6"/>'
     + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="4" fill="{GOLD}"/>' for x, y in [(194, 140), (194, 134), (210, 142)]))

# 4. 出境時先到免稅手續機台刷護照，行李還沒託運
card('kiosk', '手繪機場的免稅手續機台，旅客拿著護照，行李箱還在身邊沒託運',
     floor(148, '#e3e8ef')
     + f'<rect x="40" y="40" width="58" height="108" rx="10" fill="{WHITE}"/>'
     + f'<rect x="48" y="50" width="42" height="32" rx="4" fill="{SKY}"/>'
     + passport(58, 54, .5) + f'<path d="M78,60 L84,60 M78,66 L86,66 M78,72 L84,72" stroke-width="1.4"/>'
     + f'<rect x="52" y="92" width="34" height="8" rx="3" fill="{GRAY}"/>'
     + f'<circle cx="69" cy="116" r="7" fill="{GREEN}"/>'
     + person(128, 108, GOLD, 1.3)
     + passport(108, 112, .55)
     + suitcase(158, 104, PINK, .95)
     + check(72, 28, .9)
     + f'<path d="M214,60 L214,148" stroke-width="2"/><rect x="196" y="44" width="36" height="20" rx="4" fill="{GRAY}"/>'
     + f'<path d="M204,54 L224,54 M218,48 L224,54 L218,60" fill="none" stroke-width="2"/>'
     + sparkle(24, 30) + sparkle(130, 30, 4))

# 5. 日版快門聲：手機在拍照，旁邊冒出聲音波紋，掛著 J/A 小標籤
card('shutter', '手繪正在拍照的手機，旁邊有喀嚓的聲音波紋和 J/A 小標籤',
     f'<g transform="rotate(-8 112 92)">' + phone(78, 30, 64, 120, LILAC, '#fdf2e0', smile=False)
     + f'<rect x="88" y="52" width="44" height="58" rx="4" fill="{SKY}" stroke-width="1.4"/>'
     + f'<path d="M88,96 Q104,84 118,94 T132,90 L132,110 L88,110 Z" fill="#cfe9c8" stroke-width="1.4"/>'
     + f'<circle cx="110" cy="72" r="7" fill="{PINK}"/><circle cx="110" cy="72" r="2.6" fill="{GOLD}" stroke-width="1.2"/>'
     + f'<circle cx="110" cy="130" r="8" fill="{WHITE}"/><circle cx="110" cy="130" r="4.5" fill="{RED}" stroke-width="1.2"/>'
     + '</g>'
     + ''.join(f'<path d="M{160+i*12},{70-i*4} Q{170+i*14},{90} {160+i*12},{110+i*4}" fill="none" stroke="{RED}" stroke-width="2.6"/>' for i in range(3))
     + f'<path d="M190,40 l0,-14 l10,-3 l0,14" fill="none" stroke-width="2"/><circle cx="187" cy="40" r="3.4" fill="{INK}" stroke="none"/><circle cx="197" cy="37" r="3.4" fill="{INK}" stroke="none"/>'
     + f'<rect x="22" y="118" width="44" height="22" rx="6" fill="{GOLD}"/>'
     + f'<path d="M66,129 L80,122" stroke-width="1.6"/>'
     + label(44, 134, 'J/A', 13)
     + sparkle(36, 36) + star(60, 70, 6, PINK))


# ---- 提醒卡的手繪小圖（120×120，米黃底）----
def rem(name, label_, inner):
    F[name] = svg('ap-' + name, 120, 120, label_, inner, bg='#fff3c4')


# 日本官網只配送日本國內：紙箱＋飛機打叉
rem('r-online', '手繪提醒：紙箱和打叉的飛機，日本官網不寄海外',
    f'<path d="M16,60 L56,50 L96,60 L56,70 Z" fill="#e8c597"/>'
    f'<path d="M16,60 L16,96 L56,108 L56,70 Z" fill="{BROWN}"/>'
    f'<path d="M96,60 L96,96 L56,108 L56,70 Z" fill="#d9a877"/>'
    f'<path d="M36,55 L76,65 L76,78" fill="none" stroke-width="1.6"/>'
    + f'<g transform="translate(62,26) rotate(-15)"><path d="M-18,0 L18,0 Q24,0 24,3 Q24,6 18,6 L-18,6 Z" fill="{WHITE}"/>'
      f'<path d="M-3,3 L-11,-11 L-5,-11 L8,3 Z M-3,5 L-9,17 L-3,17 L8,5 Z" fill="{SKY}"/></g>'
    + cross(96, 26, .85))

# 新手機別放託運：行李箱在輸送帶上打叉，手上的手機打勾
rem('r-bag', '手繪提醒：手機不要放進託運行李箱',
    f'<rect x="8" y="92" width="72" height="12" rx="6" fill="{GRAY}"/>'
    + ''.join(f'<circle cx="{x}" cy="98" r="3" fill="{WHITE}" stroke-width="1.2"/>' for x in (18, 34, 50, 66))
    + suitcase(24, 46, PINK, .95)
    + cross(66, 34, .8)
    + phone(84, 48, 26, 46)
    + check(104, 102, .7))

# 退稅後還不是最後的價錢：入境申報單＋紅色印章
rem('r-declare', '手繪提醒：入境申報單和筆',
    f'<rect x="20" y="16" width="58" height="80" rx="4" fill="{WHITE}"/>'
    + ''.join(f'<path d="M28,{y} L70,{y}" stroke-width="1.4"/>' for y in (30, 40, 50, 60))
    + f'<rect x="28" y="70" width="10" height="10" rx="1" fill="{WHITE}" stroke-width="1.4"/>'
    + f'<path d="M29,75 L33,79 L40,68" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    + f'<path d="M44,76 L70,76" stroke-width="1.4"/>'
    + f'<g transform="rotate(30 92 66)"><rect x="86" y="34" width="12" height="56" rx="3" fill="{GOLD}"/>'
      f'<path d="M86,90 L92,102 L98,90 Z" fill="{WHITE}"/><rect x="86" y="34" width="12" height="8" rx="3" fill="{PINK}"/></g>'
    + f'<circle cx="60" cy="100" r="12" fill="none" stroke="{RED}" stroke-width="2.6"/>'
    + f'<path d="M54,100 L66,100" stroke="{RED}" stroke-width="2.4"/>')

print(save(F, OUT), 'files')
