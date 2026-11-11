import urllib.request
import os
import time
from osgeo import gdal

url = "https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_469_100.tif"
dest_path = "/home/ator/BF2/.agents/teamwork/explorer_m2_1/sample_nDMP_469_100.tif"

print(f"Downloading sample tile from {url}...")
t0 = time.time()
req = urllib.request.Request(url, headers={'User-Agent': 'BF2-Level-Builder/1.0'})
with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path + ".tmp", "wb") as f:
    total_downloaded = 0
    while True:
        chunk = resp.read(65536)
        if not chunk:
            break
        f.write(chunk)
        total_downloaded += len(chunk)

os.replace(dest_path + ".tmp", dest_path)
dt = time.time() - t0
print(f"Downloaded {total_downloaded:,} bytes in {dt:.2f}s ({total_downloaded / (1024*1024) / dt:.2f} MB/s)")

# Validate with GDAL
ds = gdal.Open(dest_path, gdal.GA_ReadOnly)
assert ds is not None, "Failed to open GeoTIFF with GDAL"
band = ds.GetRasterBand(1)
w, h = ds.RasterXSize, ds.RasterYSize
gt = ds.GetGeoTransform()
proj = ds.GetProjectionRef()
nodata = band.GetNoDataValue()
min_val, max_val = band.ComputeRasterMinMax()

print(f"GDAL Verification:")
print(f"  Dimensions: {w} x {h}")
print(f"  GeoTransform: {gt}")
print(f"  Data type: {gdal.GetDataTypeName(band.DataType)}")
print(f"  NoData value: {nodata}")
print(f"  Min value: {min_val}, Max value: {max_val}")
print(f"  Projection contains D96TM: {'D96TM' in proj or 'Slovenia' in proj or 'EPSG' in proj or '3794' in proj}")
ds = None
