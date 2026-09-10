# -*- coding: utf-8 -*-
"""更新 apple.json 的日圓匯率。

臺灣銀行牌告頁會阻擋程式化請求，故改用公開 API 取得中間匯率，
再加上換匯成本估算實際負擔。抓取失敗時保留原值，不讓頁面壞掉。
"""
import json, urllib.request, datetime, sys

API = "https://open.er-api.com/v6/latest/JPY"
SPREAD = 0.016   # 中間匯率→現金賣出的價差，實測臺銀約 1.6%


def fetch_mid():
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0"})
    d = json.loads(urllib.request.urlopen(req, timeout=25).read())
    r = (d.get("rates") or {}).get("TWD")
    if not r:
        raise ValueError("回應中沒有 TWD")
    return float(r), d.get("time_last_update_utc", "")


def main():
    ap = json.load(open("apple.json", encoding="utf-8"))
    old = ap["rate"]["jpy_twd"]
    try:
        mid, when = fetch_mid()
    except Exception as e:
        print(f"⚠️ 匯率取得失敗（{type(e).__name__}），保留原值 {old}")
        return 0

    cash = round(mid * (1 + SPREAD), 4)
    ap["rate"] = {
        "jpy_twd": cash,
        "jpy_twd_mid": round(mid, 6),
        "spread": SPREAD,
        "source": "open.er-api.com 中間匯率，加計約 1.6% 換匯成本",
        "quoted_at": (when or datetime.datetime.utcnow().isoformat()[:16]),
    }
    ap["updated"] = datetime.date.today().isoformat()
    json.dump(ap, open("apple.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    diff = (cash - old) / old * 100 if old else 0
    print(f"✅ 匯率更新：中間 {mid:.6f} → 換算用 {cash}（原 {old}，變動 {diff:+.2f}%）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
