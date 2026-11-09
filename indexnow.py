"""把這一輪內容真的有變的網址通知 IndexNow（Bing、Yandex 等共用）。

比對的是建置前後兩份 sitemap.xml 的 lastmod：gen.py 只在頁面內容雜湊變動時
才更新 lastmod，所以這裡送出的就是「內容有變」的頁，不會每輪把全站重送一次。

金鑰檔 <key>.txt 放在站台根目錄，IndexNow 會去抓它確認站是我們的。
推送後 GitHub Pages 要一兩分鐘才部署好，所以先等金鑰檔在線上抓得到再送。

用法：python3 indexnow.py 建置前的sitemap 建置後的sitemap
"""
import glob, json, re, sys, time, urllib.request

HOST = 'eric-twhub.github.io'
SITE = f'https://{HOST}'
UA = 'Mozilla/5.0 (compatible; taiwan-japan-flights-indexnow/1.0)'


def lastmods(path):
    try:
        x = open(path, encoding='utf-8').read()
    except OSError:
        return {}
    return dict(re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', x))


def main(before, after):
    keys = [f[:-4] for f in glob.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}\.txt', f)]
    if len(keys) != 1:
        print(f'::warning::找不到唯一的 IndexNow 金鑰檔（{len(keys)} 個），略過')
        return
    key = keys[0]
    old, new = lastmods(before), lastmods(after)
    urls = [u for u, d in new.items() if old.get(u) != d]
    if not urls:
        print('IndexNow：沒有內容變動的網址，不送')
        return
    key_url = f'{SITE}/{key}.txt'
    for i in range(20):                      # 最多等約 5 分鐘讓 Pages 部署
        try:
            req = urllib.request.Request(f'{key_url}?t={time.time()}', headers={'User-Agent': UA})
            if urllib.request.urlopen(req, timeout=15).read().decode().strip() == key:
                break
        except Exception:
            pass
        time.sleep(15)
    else:
        print('::warning::金鑰檔在線上一直抓不到，這輪不送 IndexNow')
        return
    time.sleep(30)                           # 金鑰檔上線時，同一次部署的頁面也差不多上線了
    body = json.dumps({'host': HOST, 'key': key, 'keyLocation': key_url,
                       'urlList': urls[:10000]}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8',
                                          'User-Agent': UA})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print(f'IndexNow：送出 {len(urls)} 個網址，HTTP {r.status}')
    except urllib.error.HTTPError as e:
        print(f'::warning::IndexNow 回 HTTP {e.code}：{e.read()[:300]!r}')
    except Exception as e:
        print(f'::warning::IndexNow 送出失敗：{e}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
