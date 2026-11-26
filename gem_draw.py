#!/usr/bin/env python3
"""用 Gemini API 畫一張插圖（日本旅遊小卡手繪風）。金鑰從 ~/.config/gemini_key 讀，不印出。
用法: python3 -I gem_draw.py <輸出.jpg> <比例 4:3|16:9|21:9...> <尺寸 1K|2K> <提示文字檔> [參考圖...]
每次呼叫記一筆到 ~/.cache/gemini_api_log.tsv（時間、輸出、token 用量）。單次執行上限 1 張；
外層迴圈另外有 MAX 控制。"""
import base64, json, os, sys, time, urllib.request, urllib.error

MODEL = os.environ.get("GEM_MODEL", "gemini-nano-banana-2.1")
LOG = os.path.expanduser(os.environ.get("GEM_LOG", "~/.cache/gemini_api_log.tsv"))

def main():
    out, ratio, size, prompt_file, *refs = sys.argv[1:]
    key = open(os.path.expanduser("~/.config/gemini_key")).read().strip()
    prompt = open(prompt_file, encoding="utf-8").read().strip()
    parts = []
    for r in refs:
        parts.append({"inline_data": {"mime_type": "image/jpeg",
                      "data": base64.b64encode(open(r, "rb").read()).decode()}})
    parts.append({"text": prompt})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": ratio, "imageSize": size}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:600]); sys.exit(2)
    um = d.get("usageMetadata", {})
    img = None
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p or "inline_data" in p:
                img = (p.get("inlineData") or p.get("inline_data"))
        if img is None:
            print("沒有圖。finishReason=", c.get("finishReason"),
                  [p.get("text", "")[:200] for p in c.get("content", {}).get("parts", [])])
    with open(LOG, "a") as f:
        f.write("\t".join([time.strftime("%F %T"), MODEL, out, size, "ok" if img else "fail",
                           json.dumps(um, ensure_ascii=False)]) + "\n")
    if not img:
        print("prompt feedback:", d.get("promptFeedback")); sys.exit(3)
    raw = base64.b64decode(img["data"])
    ext = ".png" if "png" in img.get("mimeType", img.get("mime_type", "")) else ".jpg"
    path = os.path.splitext(out)[0] + ext
    open(path, "wb").write(raw)
    print(f"OK {path} {len(raw)}B {time.time()-t0:.0f}s usage={um}")

main()
