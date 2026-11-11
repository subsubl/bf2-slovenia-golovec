import urllib.request
import urllib.error
import time

url = "https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_469_100.tif"

print("--- Testing recovery after 429 using Retry-After ---")
for i in range(15):
    req = urllib.request.Request(url, headers={'User-Agent': 'BF2-Level-Builder/1.0', 'Range': 'bytes=0-10'})
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"Req {i+1}: Status {resp.status} in {time.time()-t0:.3f}s")
    except urllib.error.HTTPError as e:
        retry_after = e.headers.get('Retry-After')
        x_retry = e.headers.get('X-Retry-In')
        print(f"Req {i+1}: HTTPError 429! Retry-After={retry_after}, X-Retry-In={x_retry}")
        wait_time = float(retry_after) if retry_after else 2.0
        print(f"Waiting {wait_time}s...")
        time.sleep(wait_time + 0.1)
        # retry
        try:
            with urllib.request.urlopen(req, timeout=5) as resp2:
                print(f"  Retry succeeded! Status {resp2.status}")
        except Exception as e2:
            print(f"  Retry failed: {e2}")
    time.sleep(0.05)
