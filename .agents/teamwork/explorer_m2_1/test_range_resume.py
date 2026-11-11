import urllib.request
import hashlib
import time

url = "https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_469_100.tif"

# 1. Fetch first 10000 bytes
req1 = urllib.request.Request(url, headers={'Range': 'bytes=0-9999'})
with urllib.request.urlopen(req1, timeout=10) as r1:
    part1 = r1.read()

# 2. Fetch next 10000 bytes
time.sleep(1.2)
req2 = urllib.request.Request(url, headers={'Range': 'bytes=10000-19999'})
with urllib.request.urlopen(req2, timeout=10) as r2:
    part2 = r2.read()

combined = part1 + part2

# 3. Fetch full 20000 bytes directly
time.sleep(1.2)
req_full = urllib.request.Request(url, headers={'Range': 'bytes=0-19999'})
with urllib.request.urlopen(req_full, timeout=10) as rf:
    full = rf.read()

print(f"Combined len: {len(combined)}, Full len: {len(full)}")
assert combined == full, "Range resume failed!"
print(f"MD5 match: {hashlib.md5(combined).hexdigest()} == {hashlib.md5(full).hexdigest()}")
print("Range resumption verified successfully!")
