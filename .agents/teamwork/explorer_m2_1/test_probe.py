import json
import urllib.request
import urllib.error
import time
import os

manifest_path = '/home/ator/BF2/tiles_manifest.json'
with open(manifest_path, 'r') as f:
    tiles = json.load(f)

print(f"Total tiles in manifest: {len(tiles)}")

# Test HEAD request or GET with Range: bytes=0-1023 to check server headers
sample_keys = ['469_100', '466_101']
for key in sample_keys:
    url = tiles[key]['ndmp_url']
    req = urllib.request.Request(url, headers={'User-Agent': 'BF2-Level-Builder/1.0', 'Range': 'bytes=0-1023'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"Key: {key}, URL: {url}")
            print(f"  Status: {resp.status}")
            print(f"  Content-Range: {resp.headers.get('Content-Range')}")
            print(f"  Content-Length: {resp.headers.get('Content-Length')}")
            print(f"  Content-Type: {resp.headers.get('Content-Type')}")
            print(f"  Server: {resp.headers.get('Server')}")
            print(f"  Accept-Ranges: {resp.headers.get('Accept-Ranges')}")
    except Exception as e:
        print(f"Error for {key}: {e}")
    time.sleep(1.0)
