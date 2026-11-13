# 東京聖誕市集頁的手繪風插圖（2026-11-13）。共用工具在 kit.py。
# 改圖就改這支，跑 `python3 illust/make_xmas.py` 重新輸出 illust/xmas/*.svg，gen.py 會把 SVG 直接內嵌進頁面。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xmas')

FILES = {}

# ---- 封面：夜晚的市集，東京鐵塔在後面 ----
W, H = 720, 330
body = (f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="26" fill="{NAVY}"/>'
        + snow([(40, 40), (120, 70), (210, 30), (300, 60), (380, 25), (470, 50), (640, 36), (690, 90), (90, 120), (330, 110), (560, 110)], 2.6)
        + ''.join(sparkle(x, y) for x, y in [(160, 40), (430, 90), (610, 70)])
        # 月亮
        + f'<path d="M96,58 a22,22 0 1,0 26,30 a18,18 0 1,1 -26,-30 Z" fill="{GOLD}"/>'
        # 東京鐵塔（右後方）
        + f'<path d="M585,40 L556,262 L614,262 Z" fill="{RED}"/>'
        + f'<path d="M574,124 L596,124 L599,140 L571,140 Z" fill="{WHITE}"/>'
        + f'<rect x="566" y="166" width="38" height="16" rx="4" fill="{WHITE}"/>'
        + face(585, 173, .75, blush=True)
        + f'<path d="M585,40 L585,22" stroke-width="2.4"/>'
        + f'<path d="M562,262 Q585,226 608,262" fill="{NAVY}"/>'
        # 地面
        + f'<path d="M3,262 Q180,236 360,254 T717,248 L717,304 Q717,327 694,327 L26,327 Q3,327 3,304 Z" fill="{WHITE}"/>'
        # 燈串
        + lights(20, 120, 260, 128, 26, 9) + lights(260, 128, 520, 116, 26, 9)
        # 小屋
        + hut(150, 206, 84, 56, RED) + hut(266, 196, 96, 64, DGREEN) + hut(392, 210, 80, 52, RED)
        + face(308, 222, .9)
        # 大聖誕樹
        + tree(70, 262, 120, 86)
        # 熱紅酒杯
        + mug(486, 238, 1.15, RED)
        # 前景雪點
        + snow([(200, 290), (420, 300), (620, 296), (520, 286)], 3, GRAY)
        )
FILES['hero'] = svg('hero', W, H, '手繪插圖：夜晚的聖誕市集，有小木屋、聖誕樹、熱紅酒和東京鐵塔', body, frame=False)

# ---- 景點小插圖（統一 180×150）----
W, H = 180, 150


def spot(name, label, inner, bg=CREAM):
    FILES[name] = svg(name, W, H, label, inner + snow([(22, 24), (158, 30), (150, 112)], 2.2, GRAY), bg=bg)


# 東京鐵塔
spot('tower', '手繪東京鐵塔',
     f'<path d="M90,20 L62,130 L118,130 Z" fill="{RED}"/>'
     f'<path d="M83,52 L97,52 L99,62 L81,62 Z" fill="{WHITE}"/>'
     f'<rect x="70" y="74" width="40" height="18" rx="5" fill="{WHITE}"/>' + face(90, 81, .8)
     + f'<path d="M90,20 L90,8" /><path d="M68,130 Q90,104 112,130" fill="{CREAM}"/>'
     + f'<path d="M30,132 L150,132" />' + star(40, 50, 6) + sparkle(140, 60))

# 晴空塔
spot('skytree', '手繪東京晴空塔',
     f'<path d="M90,10 L78,132 L102,132 Z" fill="{SKY}"/>'
     f'<rect x="80" y="40" width="20" height="9" rx="3" fill="{GRAY}"/>'
     f'<rect x="73" y="64" width="34" height="16" rx="5" fill="{GRAY}"/>' + face(90, 70, .75)
     + f'<path d="M30,132 L150,132" />' + tree(140, 128, 40, 30, smile=False) + star(42, 48, 6))

# 東京車站（丸之內）
spot('station', '手繪東京車站紅磚站舍',
     f'<rect x="22" y="72" width="136" height="56" rx="3" fill="{BRICK}"/>'
     f'<path d="M22,92 L158,92 M22,110 L158,110" stroke="{WHITE}" stroke-width="2.6"/>'
     f'<path d="M24,72 Q40,40 56,72 Z" fill="#6c7a8c"/><path d="M124,72 Q140,40 156,72 Z" fill="#6c7a8c"/>'
     + ''.join(f'<rect x="{x}" y="78" width="8" height="10" rx="2" fill="{CREAM}" stroke-width="1.4"/>' for x in (66, 82, 98, 114))
     + tree(90, 128, 46, 34) + f'<path d="M14,132 L166,132" />')

# 六本木之丘＋麻布台之丘
spot('hills', '手繪六本木之丘與麻布台之丘的高樓和聖誕樹',
     f'<rect x="36" y="34" width="44" height="96" rx="18" fill="{GRAY}"/>'
     + ''.join(f'<path d="M44,{y} L72,{y}" stroke-width="1.3" opacity=".6"/>' for y in range(52, 128, 12))
     + f'<rect x="104" y="18" width="30" height="112" rx="13" fill="{SKY}"/>'
     + ''.join(f'<path d="M110,{y} L128,{y}" stroke-width="1.3" opacity=".6"/>' for y in range(36, 128, 12))
     + tree(90, 128, 54, 40) + f'<path d="M20,132 L160,132" />' + sparkle(150, 46))

# 上野：戴聖誕帽的熊貓
spot('panda', '手繪戴聖誕帽的熊貓',
     f'<ellipse cx="90" cy="112" rx="34" ry="24" fill="{WHITE}"/>'
     f'<ellipse cx="62" cy="108" rx="9" ry="13" fill="{INK}"/><ellipse cx="118" cy="108" rx="9" ry="13" fill="{INK}"/>'
     f'<circle cx="64" cy="46" r="11" fill="{INK}"/><circle cx="116" cy="46" r="11" fill="{INK}"/>'
     f'<circle cx="90" cy="70" r="30" fill="{WHITE}"/>'
     f'<ellipse cx="78" cy="70" rx="7" ry="9" fill="{INK}" transform="rotate(-25 78 70)"/>'
     f'<ellipse cx="102" cy="70" rx="7" ry="9" fill="{INK}" transform="rotate(25 102 70)"/>'
     f'<circle cx="79" cy="69" r="2" fill="{WHITE}" stroke="none"/><circle cx="101" cy="69" r="2" fill="{WHITE}" stroke="none"/>'
     f'<ellipse cx="90" cy="80" rx="4" ry="3" fill="{INK}"/>'
     f'<ellipse cx="72" cy="84" rx="4" ry="2.4" fill="{PINK}" stroke="none"/><ellipse cx="108" cy="84" rx="4" ry="2.4" fill="{PINK}" stroke="none"/>'
     f'<path d="M64,48 Q84,8 120,30 Q110,40 116,46 Z" fill="{RED}"/>'
     f'<path d="M62,50 Q90,40 118,48" stroke="{WHITE}" stroke-width="7"/>'
     f'<circle cx="122" cy="28" r="7" fill="{WHITE}"/>')

# 惠比壽：小城堡和廣場時鐘
spot('ebisu', '手繪惠比壽花園廣場的城堡建築和時鐘',
     f'<rect x="36" y="70" width="80" height="58" fill="{CREAM}"/>'
     f'<path d="M30,72 L76,44 L122,72 Z" fill="#6c7a8c"/>'
     f'<rect x="28" y="56" width="16" height="72" fill="{CREAM}"/><path d="M24,58 L36,32 L48,58 Z" fill="#6c7a8c"/>'
     f'<rect x="108" y="56" width="16" height="72" fill="{CREAM}"/><path d="M104,58 L116,32 L128,58 Z" fill="#6c7a8c"/>'
     f'<path d="M66,128 L66,106 Q76,94 86,106 L86,128" fill="{DBROWN}"/>'
     f'<rect x="50" y="84" width="10" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/><rect x="92" y="84" width="10" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/>'
     f'<path d="M150,128 L150,66" stroke-width="3"/><circle cx="150" cy="56" r="13" fill="{WHITE}"/>'
     f'<path d="M150,56 L150,48 M150,56 L156,59" stroke-width="2"/>'
     f'<path d="M14,130 L166,130" />')

# 日比谷 Creema：手作市集（毛線球＋棒針）
spot('craft', '手繪毛線球和棒針，代表手作市集',
     f'<circle cx="84" cy="88" r="34" fill="{RED}"/>'
     f'<path d="M56,72 Q84,96 112,70 M52,92 Q84,116 116,90 M66,60 Q90,84 104,120" fill="none" stroke-width="1.8"/>'
     f'<path d="M110,30 L64,128 M128,40 L96,132" stroke="{DBROWN}" stroke-width="4"/>'
     f'<circle cx="110" cy="30" r="5" fill="{GOLD}"/><circle cx="128" cy="40" r="5" fill="{GOLD}"/>'
     + face(84, 88, .9) + f'<path d="M118,104 q20,8 30,26" fill="none" stroke="{RED}" stroke-width="2.6"/>' + star(40, 40, 7))

# 東京聖誕市集（新豐洲、芝公園）：德式小屋＋熱紅酒
spot('market', '手繪聖誕市集的木頭小屋和熱紅酒杯',
     hut(30, 76, 82, 50, RED) + face(71, 92, .8) + mug(124, 92, .8, GREEN)
     + lights(14, 34, 166, 34, 16, 8) + f'<path d="M14,132 L166,132" />')

# 目黑：友善環境（葉子＋紙袋）
spot('eco', '手繪紙袋和葉子，代表友善環境的市集',
     f'<path d="M54,62 L126,62 L120,130 L60,130 Z" fill="{BROWN}"/>'
     f'<path d="M72,62 Q72,38 90,38 Q108,38 108,62" fill="none" stroke-width="3"/>'
     + face(90, 96, .9)
     + f'<path d="M126,44 Q160,40 156,78 Q122,82 126,44 Z" fill="{GREEN}"/><path d="M128,46 L152,74" stroke-width="1.6"/>'
     + f'<path d="M30,52 Q50,30 62,54 Q42,66 30,52 Z" fill="{DGREEN}"/>')

# 橫濱紅磚倉庫
spot('brick', '手繪橫濱紅磚倉庫',
     f'<rect x="20" y="66" width="140" height="62" rx="2" fill="{BRICK}"/>'
     f'<path d="M18,66 L162,66" stroke-width="3"/>'
     + ''.join(f'<path d="M{x},116 L{x},100 Q{x+6},92 {x+12},100 L{x+12},116 Z" fill="{CREAM}" stroke-width="1.6"/>' for x in (30, 54, 78, 102, 126))
     + ''.join(f'<rect x="{x}" y="76" width="10" height="12" rx="2" fill="{GOLD}" stroke-width="1.4"/>' for x in (32, 56, 80, 104, 128))
     + lights(20, 50, 160, 50, 10, 8) + tree(150, 128, 34, 26, smile=False) + f'<path d="M12,130 L168,130" />')

# 幕張：禮物盒（角色市集不能畫角色本人，只畫禮物）
spot('gift', '手繪聖誕禮物盒',
     f'<rect x="48" y="66" width="84" height="62" rx="6" fill="{GREEN}"/>'
     f'<rect x="42" y="54" width="96" height="18" rx="5" fill="{GREEN}"/>'
     f'<path d="M90,54 L90,128" stroke="{RED}" stroke-width="9"/>'
     f'<path d="M90,54 Q66,26 70,46 Q72,56 90,54 Q114,26 110,46 Q108,56 90,54 Z" fill="{RED}"/>'
     + face(90, 98, 1.0) + star(38, 40, 7) + sparkle(146, 44))

# ---- 裝飾：分隔線的燈串（橫長）----
FILES['garland'] = svg('garland', 720, 60, '', lights(10, 14, 360, 14, 26, 12) + lights(360, 14, 710, 14, 26, 12)
                       + ''.join(f'<path d="M{x},10 l0,-6" stroke-width="1.4"/>' for x in (10, 360, 710)), frame=False)

print(save(FILES, OUT), 'files')
