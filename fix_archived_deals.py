# -*- coding: utf-8 -*-
"""一次性修補封存的特價貼文措辭。

舊版用「低於本站近期紀錄中位價 X%」描述折扣，但中位數被冷門日期與
轉機貴票拉高，該百分比不實；而封存頁沒有當時的每日最低價可重算，
因此不編造新數字，改為當時可驗證的事實：該價格本來就是發布當日
此航線紀錄中的最低價（pick_deals 取 min）。

gen.py 只會重寫當日入選的貼文，其餘封存頁不會再產生，故需本腳本。
用法：python3 fix_archived_deals.py
"""
import re, glob, sys

PATCHES = [
    (re.compile(r'低於本站近期紀錄中位價\s*\d+%'), '發布當日此航線紀錄中的最低價'),
    (re.compile(r'此航線目前共 (\d+) 筆來回票價，中位價 NT\$[\d,]+。'),
     r'發布當時此航線共 \1 筆來回票價紀錄。'),
]


def main():
    files = sorted(glob.glob('deals/*/index.html'))
    n_files = n_hits = 0
    for f in files:
        h = open(f, encoding='utf-8').read()
        o, hits = h, 0
        for pat, rep in PATCHES:
            h, k = pat.subn(rep, h)
            hits += k
        if h != o:
            open(f, 'w', encoding='utf-8').write(h)
            n_files += 1
            n_hits += hits
    print(f"✅ 修補 {n_files}/{len(files)} 則貼文，共 {n_hits} 處")
    left = sum(len(re.findall(r'本站近期紀錄|中位價',
               re.sub(r'<[^>]+>', ' ', open(f, encoding='utf-8').read())))
               for f in files)
    print(f"   殘留 {left} 處" + ("" if left == 0 else "  ← 需檢查"))
    return 0 if left == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
