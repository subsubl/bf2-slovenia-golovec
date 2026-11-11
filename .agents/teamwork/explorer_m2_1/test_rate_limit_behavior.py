import urllib.request
import urllib.error
import time

url = "https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_469_100.tif"

print("--- Testing rapid sequential requests to inspect rate limit threshold & 429 headers ---")
got_429 = False
for i in range(20):
    req = urllib.request.Request(url, headers={'User-Agent': 'BF2-Level-Builder/1.0', 'Range': 'bytes=0-10'})
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"Req {i+1}: Status {resp.status} in {time.time()-t0:.3f}s")
    except urllib.error.HTTPError as e:
        print(f"Req {i+1}: HTTPError {e.code} - {e.reason}")
        print("  Headers received:")
        for h, v in e.headers.items():
            print(f"    {h}: {v}")
        got_429 = True
        break
    except Exception as e:
        print(f"Req {i+1}: Exception {e}")
        break
    time.sleep(0.05) # very short delay to observe rate limiter

if not got_429:
    print("No 429 triggered with 0.05s delay over 20 requests.")
