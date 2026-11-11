import json
import urllib.request
import time

manifest_path = '/home/ator/BF2/tiles_manifest.json'
with open(manifest_path, 'r') as f:
    tiles = json.load(f)

total_bytes = 0
sizes = {}

for i, (key, info) in enumerate(tiles.items()):
    url = info['ndmp_url']
    req = urllib.request.Request(url, headers={'User-Agent': 'BF2-Level-Builder/1.0', 'Range': 'bytes=0-0'})
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=10) as resp:
            cr = resp.headers.get('Content-Range') # e.g. bytes 0-0/10025052
            length = int(cr.split('/')[-1]) if cr else int(resp.headers.get('Content-Length', 0))
            sizes[key] = length
            total_bytes += length
            dt = time.time() - t0
            print(f"[{i+1}/25] {key}: {length:,} bytes ({length / 1024 / 1024:.2f} MB) in {dt:.3f}s")
    except Exception as e:
        print(f"[{i+1}/25] {key}: ERROR {e}")
    time.sleep(1.2)

print(f"\nTotal estimated size for all 25 nDMP GeoTIFFs: {total_bytes:,} bytes ({total_bytes / (1024*1024):.2f} MB)")
