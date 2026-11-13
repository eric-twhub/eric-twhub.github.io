# 主題貼紙組 A（2026-11-13）：機票、交通、信用卡、購物、手機、家電、日曆類頁面。
# 共用工具在 kit.py；跑 `python3 illust/st_a.py` 輸出到 illust/st/。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

FILES = {}


def put(name, label, inner, **kw):
    FILES[name] = sticker(name, label, inner, **kw)


def cloud(x, y, s=1.0, col=WHITE):
    return (f'<path d="M{x},{y} q{-2*s},{-14*s} {12*s},{-14*s} q{4*s},{-12*s} {18*s},{-6*s} '
            f'q{12*s},{-6*s} {16*s},{8*s} q{10*s},{2*s} {6*s},{12*s} Z" fill="{col}"/>')


def plane(x, y, s=1.0, col=WHITE):
    # 機身朝右的小飛機，窗戶與臉
    return (f'<path d="M{x-4*s},{y-2*s} L{x+14*s},{y-30*s} L{x+26*s},{y-30*s} L{x+20*s},{y-2*s} Z" fill="{SKY}"/>'
            f'<path d="M{x-38*s},{y-10*s} L{x-46*s},{y-28*s} L{x-36*s},{y-28*s} L{x-24*s},{y-12*s} Z" fill="{SKY}"/>'
            f'<path d="M{x-44*s},{y-12*s} Q{x-44*s},{y-22*s} {x-30*s},{y-22*s} L{x+30*s},{y-22*s} '
            f'Q{x+50*s},{y-22*s} {x+52*s},{y-8*s} Q{x+50*s},{y+6*s} {x+30*s},{y+6*s} L{x-30*s},{y+6*s} '
            f'Q{x-44*s},{y+6*s} {x-44*s},{y-12*s} Z" fill="{col}"/>'
            + ''.join(f'<circle cx="{x+dx*s}" cy="{y-12*s}" r="{2.6*s}" fill="{SKY}" stroke-width="1.3"/>' for dx in (-24, -14, -4, 6))
            + f'<path d="M{x-2*s},{y+2*s} L{x+16*s},{y+22*s} L{x+26*s},{y+22*s} L{x+20*s},{y+2*s} Z" fill="{SKY}"/>'
            + face(x + 36*s, y - 8*s, .7*s))


# 1 plane：小飛機與雲
put('plane', '手繪可愛小飛機和雲朵',
    cloud(26, 118, 1.2) + cloud(118, 56, 1.0) + plane(84, 92, 1.2)
    + sparkle(150, 100) + star(36, 40, 6))

# 2 plane-fuji：飛過富士山
put('plane-fuji', '手繪小飛機飛過富士山',
    f'<path d="M20,132 L72,64 Q90,56 108,64 L160,132 Z" fill="#8fb3d9"/>'
    f'<path d="M72,64 Q90,56 108,64 L118,78 Q108,84 100,78 Q92,86 84,78 Q74,84 62,78 Z" fill="{WHITE}"/>'
    + face(90, 104, .8)
    + plane(110, 40, .62) + cloud(24, 56, .8) + f'<path d="M14,132 L166,132"/>')

# 3 seat：靠窗座位
put('seat', '手繪飛機靠窗座位，窗外有雲',
    f'<rect x="94" y="22" width="56" height="70" rx="26" fill="{SKY}"/>'
    + cloud(104, 70, .8) + f'<circle cx="134" cy="40" r="7" fill="{GOLD}"/>'
    + f'<rect x="38" y="30" width="44" height="74" rx="14" fill="{RED}"/>'
    f'<rect x="44" y="24" width="32" height="18" rx="7" fill="{WHITE}"/>'
    f'<rect x="30" y="96" width="68" height="18" rx="7" fill="{RED}"/>'
    f'<path d="M30,104 L22,104 L22,82 M98,104 L106,104 L106,82" fill="none" stroke-width="3"/>'
    f'<path d="M42,114 L42,132 M86,114 L86,132" stroke-width="3"/>'
    + face(60, 66, .8) + f'<path d="M14,132 L166,132"/>')

# 4 luggage：行李箱站在磅秤上
put('luggage', '手繪貼滿貼紙的行李箱站在磅秤上',
    f'<path d="M76,34 L76,22 Q76,16 82,16 L98,16 Q104,16 104,22 L104,34" fill="none" stroke-width="3.5"/>'
    f'<rect x="56" y="34" width="68" height="78" rx="10" fill="{GREEN}"/>'
    f'<path d="M72,40 L72,106 M108,40 L108,106" stroke-width="1.6" opacity=".6"/>'
    f'<circle cx="70" cy="56" r="8" fill="{GOLD}" stroke-width="1.6"/>'
    f'<rect x="96" y="80" width="18" height="12" rx="3" fill="{PINK}" stroke-width="1.6" transform="rotate(-12 105 86)"/>'
    + star(108, 52, 6, WHITE) + face(90, 76, .9)
    + f'<rect x="40" y="114" width="100" height="16" rx="5" fill="{GRAY}"/>'
    f'<circle cx="90" cy="122" r="5" fill="{WHITE}" stroke-width="1.6"/><path d="M90,122 L93,119" stroke-width="1.6"/>'
    + sparkle(150, 60))

# 5 nighttrain：夜裡的電車與月亮
put('nighttrain', '手繪夜裡的電車和月亮',
    f'<path d="M34,32 a16,16 0 1,0 20,22 a13,13 0 1,1 -20,-22 Z" fill="{GOLD}"/>'
    + star(130, 30, 5) + star(150, 52, 4) + sparkle(96, 26)
    + f'<rect x="22" y="70" width="136" height="48" rx="12" fill="{SKY}"/>'
    + ''.join(f'<rect x="{x}" y="78" width="20" height="16" rx="3" fill="{GOLD}" stroke-width="1.5"/>' for x in (34, 62, 118))
    + f'<path d="M22,102 L158,102" stroke="{RED}" stroke-width="4"/>'
    + face(100, 88, .8)
    + f'<circle cx="46" cy="120" r="6" fill="{INK}"/><circle cx="134" cy="120" r="6" fill="{INK}"/>'
    f'<path d="M12,128 L168,128" stroke-width="2.6"/>', bg='#e9ecf6')

# 6 subway：地鐵車廂正面
put('subway', '手繪可愛的地鐵車廂',
    f'<rect x="46" y="22" width="88" height="96" rx="20" fill="{WHITE}"/>'
    f'<rect x="58" y="34" width="64" height="34" rx="8" fill="{SKY}"/>'
    + face(90, 52, .9)
    + f'<path d="M46,80 L134,80" stroke="{GREEN}" stroke-width="6"/>'
    f'<circle cx="64" cy="98" r="6" fill="{GOLD}"/><circle cx="116" cy="98" r="6" fill="{GOLD}"/>'
    f'<rect x="80" y="92" width="20" height="10" rx="3" fill="{GRAY}" stroke-width="1.5"/>'
    f'<path d="M60,118 L52,132 M120,118 L128,132" stroke-width="3"/><path d="M24,132 L156,132"/>'
    + sparkle(150, 40) + star(30, 46, 5))

# 7 iccard：交通 IC 卡與感應波紋
put('iccard', '手繪有臉的交通 IC 卡和感應波紋',
    f'<rect x="30" y="44" width="92" height="60" rx="10" fill="{GREEN}"/>'
    f'<rect x="40" y="54" width="22" height="16" rx="3" fill="{GOLD}" stroke-width="1.5"/>'
    + face(82, 82, .9)
    + ''.join(f'<path d="M{132+i*10},{58-i*6} Q{142+i*12},74 {132+i*10},{90+i*6}" fill="none" stroke-width="2.4"/>' for i in range(3))
    + star(36, 30, 5) + sparkle(54, 122))

# 8 card：信用卡與硬幣
put('card', '手繪有臉的信用卡和硬幣',
    f'<rect x="26" y="36" width="100" height="64" rx="10" fill="{RED}"/>'
    f'<path d="M26,54 L126,54" stroke="{INK}" stroke-width="8"/>'
    f'<rect x="38" y="64" width="20" height="14" rx="3" fill="{GOLD}" stroke-width="1.5"/>'
    + face(92, 78, .9)
    + f'<ellipse cx="132" cy="116" rx="18" ry="7" fill="{GOLD}"/><rect x="114" y="104" width="36" height="12" fill="{GOLD}" stroke="none"/>'
    f'<path d="M114,104 L114,116 M150,104 L150,116"/><ellipse cx="132" cy="104" rx="18" ry="7" fill="{GOLD}"/>'
    f'<circle cx="146" cy="84" r="11" fill="{GOLD}"/><circle cx="146" cy="84" r="5" fill="none" stroke-width="1.5"/>'
    + sparkle(40, 120) + star(150, 34, 6))

# 9 coupon：優惠券與購物袋
put('coupon', '手繪剪線優惠券和購物袋',
    f'<path d="M96,58 L150,58 L144,128 L102,128 Z" fill="{PINK}"/>'
    f'<path d="M110,58 Q110,40 123,40 Q136,40 136,58" fill="none" stroke-width="3"/>'
    + face(123, 96, .8)
    + f'<g transform="rotate(-10 60 80)">'
      f'<path d="M24,56 L96,56 L96,72 a8,8 0 0,0 0,16 L96,104 L24,104 L24,88 a8,8 0 0,0 0,-16 Z" fill="{GOLD}"/>'
      f'<path d="M44,60 L44,100" stroke-dasharray="4 4" stroke-width="2"/>'
      f'<circle cx="68" cy="74" r="5" fill="{WHITE}" stroke-width="1.6"/><circle cx="80" cy="88" r="5" fill="{WHITE}" stroke-width="1.6"/>'
      f'<path d="M84,70 L64,92" stroke-width="2"/></g>'
    + star(30, 34, 6) + sparkle(150, 30))

# 10 receipt：收據與護照
put('receipt', '手繪收據和護照',
    f'<rect x="96" y="44" width="56" height="78" rx="6" fill="#4f6fa8"/>'
    f'<circle cx="124" cy="78" r="13" fill="none" stroke="{GOLD}" stroke-width="2.4"/>'
    f'<path d="M111,78 L137,78 M124,65 Q116,78 124,91 Q132,78 124,65" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
    + f'<path d="M30,28 L86,28 L86,124 L80,118 L74,124 L68,118 L62,124 L56,118 L50,124 L44,118 L38,124 L30,118 Z" fill="{WHITE}"/>'
    f'<path d="M50,44 L58,56 L66,44 M58,56 L58,70 M50,60 L66,60 M50,66 L66,66" fill="none" stroke-width="2.2"/>'
    + ''.join(f'<path d="M40,{y} L76,{y}" stroke-width="1.5" opacity=".6"/>' for y in (82, 92, 102))
    + face(58, 110, .6, blush=False) + sparkle(160, 32))

# 11 yen：零錢包與 5 円硬幣
put('yen', '手繪零錢包和日圓硬幣',
    f'<path d="M30,70 Q30,50 50,50 L100,50 Q120,50 120,70 L120,108 Q120,124 104,124 L46,124 Q30,124 30,108 Z" fill="{PINK}"/>'
    f'<path d="M50,50 Q56,34 64,50 M100,50 Q94,34 86,50" fill="none" stroke-width="2.6"/>'
    f'<circle cx="60" cy="40" r="5" fill="{GOLD}"/><circle cx="90" cy="40" r="5" fill="{GOLD}"/>'
    + face(75, 92, 1.0)
    + f'<circle cx="140" cy="100" r="18" fill="{GOLD}"/><circle cx="140" cy="100" r="6" fill="{CREAM}"/>'
    f'<circle cx="146" cy="56" r="13" fill="{GRAY}"/><circle cx="146" cy="56" r="8" fill="none" stroke-width="1.4"/>'
    + sparkle(30, 30) + star(110, 30, 5))

# 12 phone：手機、訊號、SIM
put('phone', '手繪有臉的智慧型手機、訊號和 SIM 卡',
    f'<rect x="56" y="24" width="56" height="104" rx="12" fill="{WHITE}"/>'
    f'<rect x="62" y="36" width="44" height="76" rx="5" fill="{SKY}"/>'
    f'<path d="M78,30 L90,30" stroke-width="2"/>'
    + face(84, 72, .9)
    + ''.join(f'<path d="M{122+i*9},{46-i*5} Q{130+i*11},58 {122+i*9},{70+i*5}" fill="none" stroke-width="2.4"/>' for i in range(3))
    + f'<path d="M22,96 L40,96 L46,102 L46,124 L22,124 Z" fill="{GOLD}"/>'
    f'<rect x="28" y="104" width="12" height="12" rx="2" fill="{CREAM}" stroke-width="1.4"/>'
    + star(30, 40, 6))

# 13 phoneprice：手機掛價格吊牌
put('phoneprice', '手繪掛著價格吊牌的手機',
    f'<rect x="40" y="22" width="56" height="104" rx="12" fill="{GRAY}"/>'
    f'<rect x="46" y="34" width="44" height="78" rx="5" fill="{SKY}"/>'
    f'<path d="M62,28 L74,28" stroke-width="2"/>'
    + face(68, 70, .9)
    + f'<path d="M96,40 Q116,36 120,56" fill="none" stroke-width="1.8"/>'
    f'<g transform="rotate(14 132 80)"><path d="M116,56 L142,56 L150,66 L150,108 L116,108 Z" fill="{GOLD}"/>'
    f'<circle cx="138" cy="64" r="3" fill="{CREAM}" stroke-width="1.4"/>'
    f'<path d="M124,80 L142,80 M124,90 L138,90 M124,98 L134,98" stroke-width="2"/></g>'
    + sparkle(150, 30) + star(28, 116, 5))

# 14 camera：可愛相機
put('camera', '手繪可愛相機',
    f'<rect x="32" y="48" width="116" height="74" rx="14" fill="{GRAY}"/>'
    f'<path d="M64,48 L72,34 L104,34 L112,48 Z" fill="{GRAY}"/>'
    f'<rect x="124" y="56" width="14" height="9" rx="3" fill="{RED}" stroke-width="1.5"/>'
    f'<circle cx="90" cy="86" r="26" fill="{WHITE}"/><circle cx="90" cy="86" r="17" fill="#6c7a8c"/>'
    f'<circle cx="84" cy="80" r="5" fill="{WHITE}" stroke="none"/>'
    f'<circle cx="46" cy="60" r="4" fill="{GOLD}" stroke-width="1.4"/>'
    + face(48, 100, .6) + star(30, 30, 6) + sparkle(152, 30))

# 15 dryer：吹風機
put('dryer', '手繪吹風機吹出風的線條',
    '<g transform="translate(-14 0)">' + f'<path d="M66,84 L58,128 L78,128 L86,84 Z" fill="{PINK}"/>'
    f'<path d="M40,58 Q40,36 62,36 L104,36 L116,44 L116,74 L104,82 L62,82 Q40,82 40,58 Z" fill="{PINK}"/>'
    f'<rect x="116" y="42" width="12" height="38" rx="4" fill="{GRAY}"/>'
    f'<circle cx="60" cy="59" r="12" fill="{WHITE}"/><circle cx="60" cy="59" r="5" fill="none" stroke-width="1.6"/>'
    + face(90, 58, .8)
    + ''.join(f'<path d="M136,{y} q7,-6 14,0 t14,0" fill="none" stroke-width="2.2"/>' for y in (48, 62, 76)) + '</g>'
    + star(30, 116, 5) + sparkle(150, 110))

# 16 car：可愛小車
put('car', '手繪可愛小車',
    f'<path d="M30,98 L30,84 Q30,74 42,72 L56,70 L72,48 Q76,44 84,44 L118,44 Q126,44 130,50 L144,70 '
    f'Q156,72 156,84 L156,98 Q156,104 150,104 L36,104 Q30,104 30,98 Z" fill="{RED}"/>'
    f'<path d="M78,52 L96,52 L96,70 L64,70 Z" fill="{SKY}" stroke-width="1.8"/>'
    f'<path d="M104,52 L122,52 L134,70 L104,70 Z" fill="{SKY}" stroke-width="1.8"/>'
    f'<circle cx="58" cy="104" r="13" fill="{INK}"/><circle cx="58" cy="104" r="5" fill="{GRAY}"/>'
    f'<circle cx="128" cy="104" r="13" fill="{INK}"/><circle cx="128" cy="104" r="5" fill="{GRAY}"/>'
    f'<circle cx="150" cy="82" r="4" fill="{GOLD}" stroke-width="1.4"/>'
    + face(94, 86, .9) + f'<path d="M14,124 L166,124"/>'
    + ''.join(f'<path d="M{x},92 L{x-10},92" stroke-width="2" opacity=".6"/>' for x in (24, 20))
    + sparkle(36, 36))

# 17 calendar：月曆頁、圈起來的日期與愛心
_cal = ''.join(f'<rect x="{44+c*20}" y="{60+r*17}" width="12" height="9" rx="2" fill="{CREAM}" stroke-width="1.3"/>'
               for r in range(4) for c in range(5))
put('calendar', '手繪月曆，幾個日期被圈起來，還有一顆愛心',
    f'<rect x="34" y="28" width="112" height="104" rx="10" fill="{WHITE}"/>'
    f'<path d="M34,52 L34,38 Q34,28 44,28 L136,28 Q146,28 146,38 L146,52 Z" fill="{RED}"/>'
    f'<path d="M58,20 L58,36 M122,20 L122,36" stroke-width="4"/>'
    + _cal
    + f'<circle cx="70" cy="81" r="10" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    f'<circle cx="110" cy="98" r="10" fill="none" stroke="{RED}" stroke-width="2.4"/>'
    + face(90, 40, .7, blush=False)
    + f'<path d="M140,108 q-8,-10 -16,-2 q-6,8 16,22 q22,-14 16,-22 q-8,-8 -16,2 Z" fill="{PINK}"/>'
    + sparkle(26, 120))

if __name__ == '__main__':
    print(save(FILES, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'st')), 'files')
