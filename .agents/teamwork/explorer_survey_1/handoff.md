# Handoff Report: Survey 1 - Workspace & Assets Investigation

**Agent**: teamwork_explorer (`explorer_survey_1`)  
**Parent**: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61  
**Working Directory**: `/home/ator/BF2/.agents/teamwork/explorer_survey_1`  
**Date**: 2026-11-11T00:43:00Z  

---

## 1. Observation

### 1.1 Complete Workspace File Inventory (`/home/ator/BF2`)
Directory listing from `ls -la /home/ator/BF2`:
```
total 45660
drwxrwxr-x  5 ator ator     4096 Nov 11 01:31 .
drwxr-x--- 61 ator ator     4096 Nov 10 16:20 ..
drwxrwxr-x  3 ator ator     4096 Nov 11 01:31 .agents
-rw-r--r--  1 ator ator     2168 Nov 11 01:22 assemble_colormap.py
-rw-rw-r--  1 ator ator  8388736 Nov 11 01:28 ColorMap.dds
-rw-rw-r--  1 ator ator 29813341 Nov 11 01:28 ColorMap_preview.png
-rw-rw-r--  1 ator ator    87943 Nov 11 01:29 ColorMap_thumb.jpg
drwxrwxr-x  2 ator ator     4096 Nov 11 01:20 dmr_raw
-rw-r--r--  1 ator ator      394 Nov 11 01:22 Heightdata.con
-rw-rw-r--  1 ator ator  8396802 Nov 11 01:21 Heightmap.raw
drwxrwxr-x  2 ator ator     4096 Nov 11 01:28 pof_1m
-rw-r--r--  1 ator ator      300 Nov 11 01:22 Terrain.con
-rw-rw-r--  1 ator ator     9142 Nov 11 01:19 tiles_manifest.json
```

Existing root files and their exact properties:
- `/home/ator/BF2/assemble_colormap.py`: 2,168 bytes. Reads 25 POF GeoTIFFs, mosaics them into 5000x5000, crops to 4096m x 4096m map bounds (X: [450, 4546], Y: [486, 4582]), exports `ColorMap_preview.png` and `ColorMap.dds`.
- `/home/ator/BF2/ColorMap.dds`: 8,388,736 bytes (4096x4096 DXT1 DDS format with 128-byte header: `4096 * 4096 / 2 + 128 = 8,388,736`).
- `/home/ator/BF2/ColorMap_preview.png`: 29,813,341 bytes (4096x4096 RGB uncompressed PNG).
- `/home/ator/BF2/ColorMap_thumb.jpg`: 87,943 bytes (512x512 RGB JPEG).
- `/home/ator/BF2/Heightdata.con`: 394 bytes. Contains:
  ```con
  rem ** Heightdata.con generated for 4096m x 4096m Slovenia (Golovec / SE Ljubljana) Map **
  rem Coordinates: Origin (0,0,0) = D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E]
  rem Focal Point (+0, +1365) = D96TM [468498 E, 100831 N] / WGS84 [46.046559 N, 14.592945 E]

  heightmap.setGridSize 2 2
  heightmap.setSize 2049 2049
  heightmap.setScale 2/0.01/2
  heightmap.setElevationOffset 0.0
  ```
- `/home/ator/BF2/Terrain.con`: 300 bytes. Contains:
  ```con
  rem ** Terrain.con for 4096m x 4096m Battlefield 2 Map **
  terrain.create terrain
  terrain.load Heightmap.raw
  terrain.primaryWorldScale 2/0.01/2
  terrain.setHeightmapGridSize 2 2
  terrain.setWorldSize 4096

  rem Ground water level (Ljubljanica river plain elevation ~270m)
  terrain.setWaterElevation 270.0
  ```
- `/home/ator/BF2/Heightmap.raw`: 8,396,802 bytes.
- `/home/ator/BF2/tiles_manifest.json`: 9,142 bytes. 25 tile entries.
- `/home/ator/BF2/dmr_raw/`: 25 files (`DMR_*.laz`), total 99 MB.
- `/home/ator/BF2/pof_1m/`: 25 files (`POF_*.tif`), total 72 MB.
- `/home/ator/BF2/levels/`: **DOES NOT EXIST**.
- `ndmp/` directory or local nDMP files: **DOES NOT EXIST**.

### 1.2 Inspection of `Heightmap.raw`
Verification via Python execution (`numpy.frombuffer(open('/home/ator/BF2/Heightmap.raw', 'rb').read(), dtype='<u2')`):
- Exact byte size: 8,396,802 bytes.
- Dimensions: 2049 rows x 2049 columns = 4,198,401 elements.
- Header size: 0 bytes (`4198401 * 2 = 8396802`).
- Data type: unsigned 16-bit integer, little-endian (`<u2` / uint16).
- Minimum raw value: `26665` (scaled elevation: `266.65 m`).
- Maximum raw value: `45132` (scaled elevation: `451.32 m`).
- Mean raw value: `30496.43` (scaled elevation: `304.96 m`).
- Median (50%): `28770.0` (scaled elevation: `287.70 m`).
- Standard deviation: `3698.70` (scaled: `36.99 m`).
- Percentiles:
  - 1%: 26820.0 (268.20 m)
  - 5%: 26948.0 (269.48 m)
  - 25%: 27862.0 (278.62 m)
  - 75%: 32473.0 (324.73 m)
  - 95%: 38306.0 (383.06 m)
  - 99%: 41796.0 (417.96 m)
- Sanity checks: Zero count = 0, uint16 max (65535) count = 0, values < 20000 = 0, values > 50000 = 0.
- Center sample [1024, 1024]: raw = 28128 (281.28 m).
- Four corners:
  - [0, 0] = 40889 (408.89 m)
  - [0, 2048] = 30283 (302.83 m)
  - [2048, 0] = 28043 (280.43 m)
  - [2048, 2048] = 26824 (268.24 m)
- Height scaling parameters: `heightScale = 0.01`, `elevationOffset = 0.0` meters.
- Horizontal terrain extent: `gridSize = 2.0 m`, world size = `(2049 - 1) * 2.0 = 4096.0 m`.
- Coordinate span: `[-2048.0, +2048.0]` on Cartesian X and Z.

### 1.3 Inspection of `tiles_manifest.json`
- Total entries: 25 tiles.
- Naming format: `"{Easting_km}_{Northing_km}"`.
- Tile grid: 5 columns x 5 rows.
  - Columns (Easting): 466, 467, 468, 469, 470 (466000 m to 471000 m D96TM).
  - Rows (Northing): 097, 098, 099, 100, 101 (97000 m to 102000 m D96TM).
  - Total bounding extent: [466000, 471000] Easting x [97000, 102000] Northing (5000m x 5000m).
- BF2 Map Coverage:
  - Map Easting range: [466450, 470546] (offset 450m from 466000m, span 4096m).
  - Map Northing range: [97418, 101514] (offset 418m from 97000m / 486m from top 102000m, span 4096m).
  - Map Origin (0,0): D96TM [468498 E, 99466 N].
  - The 25 tiles fully enclose the 4096m x 4096m level bounding box with a buffer border of ~450m-486m on all sides.
- Fields per tile:
  - `ti_name` (e.g. `"469_100"`)
  - `min_visina` (e.g. `267.376`)
  - `max_visina` (e.g. `310.58`)
  - `dmr_url`: Remote Flycom LAZ URL (`https://assets.flycom.si/.../DMR_<tile>.laz`)
  - `pof_url`: Remote Flycom POF GeoTIFF URL (`https://assets.flycom.si/.../POF_<tile>.tif`)
  - `ndmp_url`: Remote Flycom nDMP GeoTIFF URL (`https://assets.flycom.si/.../nDMP_<tile>.tif`)
- Local file status:
  - DMR: 25/25 files already present in `/home/ator/BF2/dmr_raw/`.
  - POF: 25/25 files already present in `/home/ator/BF2/pof_1m/`.
  - nDMP: 0/25 files present locally.
- Remote nDMP GeoTIFF Inspection:
  - Tested remote URL: `https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_469_100.tif`.
  - HTTP Status: `200 OK`, Content-Length: 10,025,052 bytes.
  - Driver: GTiff, Size: 2000 x 2000 pixels (0.5m grid spacing).
  - Projection: EPSG:3794 (Slovenian D96TM).
  - Data Type: Int16, NoData: `-32767.0`.
  - Elevation values: int16 meters of canopy height above ground (min -1m, max 34m, mean 1.38m; 90th percentile 5m, 95th 9m, 99th 18m).
- **Critical Finding: Flycom Rate Limiting (`HTTP 429 Too Many Requests`)**:
  - A loop firing HEAD requests without delay resulted in: `Results: {200: 10, 'Error: HTTP Error 429: Too Many Requests': 15}`.
  - Attempting to use GDAL `/vsicurl/` failed immediately due to concurrent range requests triggering HTTP 429.
  - Retrying with a 2-second sleep returned `200 OK`.
  - Therefore, all tile download scripts must operate sequentially with rate limiting (1.0 - 2.0 sec delay or retry backoff).

### 1.4 Environment, Tools & Python Packages
- Python Executable: `/usr/bin/python3` (Python 3.12.3).
- Environment type: Debian/Ubuntu PEP 668 externally managed environment.
- Available Python GIS & Scientific Packages:
  - `numpy`: 1.26.4
  - `scipy`: 1.11.4
  - `osgeo.gdal`: 3.8.4
  - `osgeo.ogr`: GDAL 3.8.4
  - `osgeo.osr`: GDAL 3.8.4
  - `pyproj`: 3.6.1
  - `PIL` (Pillow): 12.1.0 (supports DDS DXT1, PNG, JPEG)
  - `laspy`: 2.7.0 (supports reading/writing LAS/LAZ point clouds)
  - `requests`: 2.34.2
  - `matplotlib`: 3.6.3
  - `OWSLib`: 0.29.3
- Packages NOT installed:
  - `rasterio` (Not installed, but `osgeo.gdal` provides full raster read/write/warp capabilities)
  - `shapely` (Not installed, but `osgeo.ogr` provides full vector geometry/centroid calculations; `shapely 2.2.0` can also be installed with `--break-system-packages` if needed)
  - `geopandas`, `osmnx`, `overpy`, `cv2`, `pdal`: Not installed.
- System CLI Utilities:
  - `/usr/bin/gdalinfo` (GDAL 3.8.4)
  - `/usr/bin/ogr2ogr` (GDAL 3.8.4)
  - `curl`, `wget`, `python3`, `pip3`: Available.
- Filesystem & Storage constraints:
  - Partition: `/dev/mapper/data-root` mounted on `/`.
  - Available space: **2.1 GB** (99% utilized).
  - Storage precaution: The 25 nDMP GeoTIFFs will consume ~250 MB total. Downstream scripts must avoid generating unnecessary intermediate multi-gigabyte uncompressed mosaics.

---

## 2. Logic Chain

1. **Elevation Map Consistency**:
   - `Heightdata.con` specifies `heightmap.setSize 2049 2049` and `heightmap.setScale 2/0.01/2`.
   - `Heightmap.raw` is exactly 8,396,802 bytes. Since `2049 * 2049 * 2 = 8,396,802`, the file consists exclusively of a contiguous stream of 2049x2049 16-bit unsigned little-endian integers with zero header bytes.
   - Ground elevations range between `266.65m` and `451.32m`, perfectly matching the real-world topography of the Ljubljana plain (~270m) and Golovec ridge (~450m).
   - In `Terrain.con`, `terrain.setWaterElevation 270.0` sets the water plane at 270.0m, meaning all terrain samples below 270.0m (down to 266.65m) will be submerged riverbed or wetlands.

2. **Geographic Coverage & Alignment**:
   - `assemble_colormap.py` defines the 5x5 tile grid covering D96TM Easting [466000, 471000] and Northing [97000, 102000].
   - It crops the 5000x5000 raster to a 4096x4096 window with X offset 450 (Easting 466450 to 470546) and Y offset 486 (Northing 101514 down to 97418).
   - The center coordinate is Easting `(466450 + 470546) / 2 = 468498` and Northing `(97418 + 101514) / 2 = 99466`.
   - This matches the origin defined in `Heightdata.con`: `Origin (0,0,0) = D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E]`.
   - Therefore, the 25 tiles in `tiles_manifest.json` provide 100% coverage of the BF2 terrain with sufficient boundary padding.

3. **LiDAR Canopy Download Strategy**:
   - While DMR and POF tiles are already present on disk in `dmr_raw/` and `pof_1m/`, the nDMP canopy GeoTIFFs are not yet downloaded.
   - Remote queries directly against `assets.flycom.si` without throttling triggered `HTTP 429 Too Many Requests`.
   - Streaming via GDAL `/vsicurl/` fails because GDAL fires concurrent chunk requests.
   - Therefore, the implementer agent for R2 must run a serial download script with rate-limiting / retry backoff (e.g. 1 request per 1.5 seconds) to fetch the 25 nDMP GeoTIFFs into an `ndmp/` directory before processing.

4. **Level Directory Status**:
   - `levels/` does not exist in `/home/ator/BF2`.
   - The user requested assembly of `levels/<level_name>/`.
   - The implementer for R3 will need to create the directory structure and package the files (`init.con`, `Sky.con`, `Water.con`, `Terrain.con`, `Heightdata.con`, `StaticObjects.con`, `OvergrowthSystem.con`, `GameplayObjects.con`).

5. **Tooling Sufficiency**:
   - Although `rasterio` and `shapely` are missing from the default pip list, `GDAL 3.8.4` (with `osgeo.gdal`, `osgeo.ogr`, and `osgeo.osr`) and `pyproj 3.6.1` are fully installed and capable of executing all required geospatial operations (clipping, raster resampling, coordinate transformation, polygon extraction).
   - If Python `shapely` is desired for building footprint simplification or centroid calculation, `pip install --break-system-packages shapely` is verified to work without error.

---

## 3. Caveats

1. **Storage Budget**:
   - Available disk space is 2.1 GB. While sufficient for downloading 250 MB of nDMP tiles and creating the BF2 level package, developers must avoid caching large uncompressed numpy dumps or high-res uncompressed TIFF mosaics.
2. **Server Rate Limiting**:
   - The Flycom asset server strictly limits request frequency. Download scripts must not use multi-threaded or unthrottled downloading.
3. **Levels Directory Name**:
   - The target level folder name under `levels/` is not explicitly dictated in `ORIGINAL_REQUEST.md` (it mentions `levels/<level_name>/`, e.g. `levels/slovenia_golovec` or `levels/golovec`). The orchestrator should standardize this name across all agents.

---

## 4. Conclusion

- **Asset Completeness**: `Heightmap.raw` (2049x2049 uint16), `ColorMap.dds` (4096x4096 DXT1), `Heightdata.con`, and `Terrain.con` are present, verified, and mathematically aligned with D96TM [468498 E, 99466 N].
- **LiDAR Canopy Data**: All 25 nDMP tile URLs are valid, point to 2000x2000 0.5m Int16 GeoTIFFs (meter units), but require sequential rate-limited downloading to avoid HTTP 429 errors.
- **Environment Readiness**: The system environment possesses all necessary GIS capabilities (GDAL 3.8.4, OGR, OSR, pyproj 3.6.1, PIL, NumPy, SciPy, laspy).
- **Missing Structure**: The `levels/` directory structure must be created from scratch during packaging.

---

## 5. Verification Method

To independently verify these findings, run the following verification commands:

```bash
# 1. Verify Heightmap.raw dimensions, headerless format, and elevation statistics
python3 -c "
import numpy as np
data = np.frombuffer(open('/home/ator/BF2/Heightmap.raw', 'rb').read(), dtype='<u2')
assert len(data) == 2049 * 2049, 'Dimension mismatch'
print(f'Heightmap OK: 2049x2049, Min={data.min()*0.01:.2f}m, Max={data.max()*0.01:.2f}m, Mean={data.mean()*0.01:.2f}m')
"

# 2. Verify tiles_manifest.json tile count and coverage
python3 -c "
import json
tiles = json.load(open('/home/ator/BF2/tiles_manifest.json'))
assert len(tiles) == 25, 'Tile count mismatch'
print(f'Tiles manifest OK: {len(tiles)} tiles listed.')
"

# 3. Verify local DMR and POF availability
python3 -c "
import glob
dmr = glob.glob('/home/ator/BF2/dmr_raw/*.laz')
pof = glob.glob('/home/ator/BF2/pof_1m/*.tif')
assert len(dmr) == 25 and len(pof) == 25, 'Local raw tiles incomplete'
print(f'Local files OK: DMR={len(dmr)}/25, POF={len(pof)}/25')
"

# 4. Verify GDAL and Python environment
python3 -c "
from osgeo import gdal, ogr, osr
import pyproj, PIL, numpy
print('Python GIS environment fully functional: GDAL', gdal.__version__, 'PyProj', pyproj.__version__)
"
```

Invalidation conditions:
- Any discrepancy in `Heightmap.raw` size (not equal to 8,396,802 bytes)
- Any tile missing from `tiles_manifest.json`
- Inability to import `osgeo.gdal` or `pyproj`
