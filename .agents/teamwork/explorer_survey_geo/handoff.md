# Handoff Report: Survey 3 - Geospatial Pipeline & Heightmap Sampling

**Agent**: teamwork_explorer (`explorer_survey_geo`)  
**Parent Agent ID**: `d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61`  
**Working Directory**: `/home/ator/BF2/.agents/teamwork/explorer_survey_geo`  
**Date**: 2026-11-11T00:48:00Z  

---

## 1. Observation

### 1.1 Project Configuration & Baseline Files
Direct inspection of files in `/home/ator/BF2`:
- `/home/ator/BF2/Heightdata.con` (lines 1–9):
  ```con
  rem ** Heightdata.con generated for 4096m x 4096m Slovenia (Golovec / SE Ljubljana) Map **
  rem Coordinates: Origin (0,0,0) = D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E]
  rem Focal Point (+0, +1365) = D96TM [468498 E, 100831 N] / WGS84 [46.046559 N, 14.592945 E]

  heightmap.setGridSize 2 2
  heightmap.setSize 2049 2049
  heightmap.setScale 2/0.01/2
  heightmap.setElevationOffset 0.0
  ```
- `/home/ator/BF2/Terrain.con` (lines 1–9):
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
- `/home/ator/BF2/assemble_colormap.py` (lines 8–15, 40–53):
  ```python
  # Mosaic bounds:
  # Easting: 466000 to 471000 (5 tiles = 5000m = 5000px)
  # Northing: 97000 to 102000 (5 tiles = 5000m = 5000px)
  cols = [466, 467, 468, 469, 470]
  rows = ['101', '100', '099', '098', '097'] # Top to bottom (North to South)
  ...
  # Crop to exact 4096m x 4096m map bounds:
  # E_min = 466450 (offset from 466000 is 450px)
  # E_max = 470546 (offset is 450 + 4096 = 4546px)
  # N_max = 101514 (offset from 102000 is 102000 - 101514 = 486px from top)
  # N_min = 97418 (offset is 486 + 4096 = 4582px from top)
  ```

### 1.2 Binary Structure and Ground Truth Verification of `Heightmap.raw`
Execution of NumPy / laspy verification script comparing `Heightmap.raw` against raw LiDAR point clouds in `/home/ator/BF2/dmr_raw/`:
- `Heightmap.raw`: Size exactly 8,396,802 bytes ($2049 \times 2049 \times 2$ bytes). 0-byte header. Unsigned 16-bit integer, little-endian (`<u2`).
- Elevation scale: `heightScale = 0.01` (1 uint16 count = 0.01 m = 1 cm).
- Min raw value: `26665` ($266.65\text{ m}$), Max raw value: `45132` ($451.32\text{ m}$), Mean: $304.96\text{ m}$.
- Direct cross-reference benchmarks against Slovenian National LiDAR (`DMR_*.laz`):
  - **South-West Ridge** (`row = 0, col = 220`): `Heightmap.raw` elevation = `451.32 m`. Raw LiDAR point cloud `DMR_466_97.laz` around D96TM `(466890 E, 97418 N)`: points `[451.107, 451.102, 451.094, 451.108, 451.122] m`.
  - **North Center** (`row = 2048, col = 1024`): `Heightmap.raw` elevation = `276.71 m`. Raw LiDAR point cloud `DMR_468_101.laz` around D96TM `(468498 E, 101514 N)`: mean = `276.705 m`.
  - **West Boundary** (`row = 1024, col = 0`): `Heightmap.raw` elevation = `294.01 m`. Raw LiDAR point cloud `DMR_466_99.laz` around D96TM `(466450 E, 99466 N)`: mean = `293.94 m`.
  - **East Boundary** (`row = 1024, col = 2048`): `Heightmap.raw` elevation = `322.72 m`. Raw LiDAR point cloud `DMR_470_99.laz` around D96TM `(470546 E, 99466 N)`: mean = `322.47 m`.
  - **Origin (0,0)** (`row = 1024, col = 1024`): `Heightmap.raw` elevation = `281.28 m`.
  - **Golovec Focal Point (0, 1365)** (`row = 1706, col = 1024`): `Heightmap.raw` elevation = `273.38 m`.

### 1.3 OpenStreetMap API Probing
- Map Extent in WGS84: `[46.015750 N, 14.566437 E]` (SW) to `[46.052791 N, 14.619621 E]` (NE).
- Single full-box query to `api.openstreetmap.org/api/0.6/map`: returned HTTP 400 (`"You requested too many nodes (limit is 50000)"`).
- Subdivided query into 4 quadrants (NW, NE, SW, SE) at midpoint `(46.034271 N, 14.593029 E)`:
  - NW Quadrant: HTTP 200, 6,680,463 bytes XML in 1.4s.
  - NE Quadrant: HTTP 200, 7,185,369 bytes XML in 1.6s.
  - SW Quadrant: HTTP 200, 2,898,298 bytes XML in 0.8s.
  - SE Quadrant: HTTP 200, 4,162,739 bytes XML in 1.1s.
  - Total: 20,926,869 bytes XML covering 100% of the 4096m x 4096m level without node-limit exhaustion.
- Overpass API endpoints:
  - `overpass-api.de`: Returned HTTP 406 when User-Agent omitted; intermittent HTTP 502 / timeout when congested.
  - `osm.ch`: Regional extract (Switzerland only, returned 0 elements for Slovenia).
  - Geofabrik daily country extract `https://download.geofabrik.de/europe/slovenia-latest.osm.pbf` (314 MB): accessible, downloadable at 2.5 MB/s.

### 1.4 LiDAR Canopy GeoTIFFs (nDMP) Probing
- `tiles_manifest.json`: 25 tile entries with URLs at `https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_<tile>.tif` (and `13-ljubljana-aneks` for 466_101).
- Remote HEAD probe: HTTP 200, Content-Length 10,025,052 bytes.
- GeoTIFF metadata: EPSG:3794 D96TM, Int16, NoData `-32767.0`, Grid size $2000 \times 2000$ pixels at $0.5\text{ m}$ resolution ($1000\text{ m} \times 1000\text{ m}$ tile).
- Flycom server behavior: Concurrent or unthrottled requests trigger `HTTP 429 Too Many Requests`. Sequential downloading with 1.0–1.5s delay succeeds reliably.
- Canopy sample statistics (`nDMP_468_100.tif`): Canopy heights range from 0 to 30m; 21.9% of area has vegetation $> 2\text{ m}$, 4.7% has canopy $> 10\text{ m}$.

---

## 2. Logic Chain

### 2.1 Coordinate Systems & Axis Orientations
1. **D96TM (EPSG:3794)**:
   - Official Slovenian National Projected Coordinate System (Transverse Mercator, GRS80 ellipsoid).
   - Coordinates are $(E, N)$ in meters: Easting $E$, Northing $N$.
2. **WGS84 (EPSG:4326)**:
   - Geographic coordinates: Latitude $\phi$ (North), Longitude $\lambda$ (East).
   - Transformation to/from D96TM is performed using standard PROJ/pyproj:
     $$\text{Transformer.from\_crs}('EPSG:4326', 'EPSG:3794', \text{always\_xy}=True)$$
     $$(E, N) = T_{4326 \to 3794}(\lambda, \phi)$$
     $$(\lambda, \phi) = T_{3794 \to 4326}(E, N)$$
3. **Battlefield 2 Cartesian Coordinates $(X, Y, Z)$**:
   - Terrain Origin $(0, 0, 0)$ is fixed at D96TM $[E_0, N_0] = [468498.0\text{ E}, 99466.0\text{ N}]$, corresponding to WGS84 $[46.034276^\circ\text{ N}, 14.592945^\circ\text{ E}]$.
   - **X Axis (East-West)**:
     - $+X$ points **East** ($+E$).
     - $-X$ points **West** ($-E$).
     - Mapping: $X = E - 468498.0 \iff E = 468498.0 + X$.
     - Range: $X \in [-2048.0, 2048.0]$ maps to $E \in [466450.0, 470546.0]$.
   - **Z Axis (North-South)**:
     - $+Z$ points **North** ($+N$).
     - $-Z$ points **South** ($-N$).
     - Mapping: $Z = N - 99466.0 \iff N = 99466.0 + Z$.
     - Range: $Z \in [-2048.0, 2048.0]$ maps to $N \in [97418.0, 101514.0]$.
   - **Y Axis (Vertical Elevation)**:
     - $+Y$ points **Upwards** in meters above sea level.
     - Mapping: $Y = \text{uint16\_raw} \times 0.01$.
4. **Golovec Focal Point Transformation**:
   - Given WGS84: $\phi_f = 46.046559^\circ\text{ N}, \lambda_f = 14.592945^\circ\text{ E}$.
   - Forward projection to D96TM:
     $$E_f = 468497.79\text{ m} \approx 468498\text{ m}$$
     $$N_f = 100831.48\text{ m} \approx 100831\text{ m}$$
   - Conversion to BF2 Cartesian:
     $$X_f = E_f - 468498.0 = -0.21\text{ m} \approx 0.0\text{ m}$$
     $$Z_f = N_f - 99466.0 = 100831.48 - 99466.0 = +1365.48\text{ m} \approx +1365.0\text{ m}$$
   - This proves the documented focal point $(0, 1365)$ in `Heightdata.con`.

### 2.2 Heightmap Indexing & Elevation Sampling Formulas
1. **Grid Layout**:
   - The terrain is $4096\text{ m} \times 4096\text{ m}$ covered by $2049 \times 2049$ vertices.
   - Grid spacing is $\Delta = 2.0\text{ m}$ on both axes.
   - In Refractor 2 raw buffers:
     - Row 0 corresponds to minimum world $Z = -2048.0\text{ m}$ (South, Northing $97418\text{ m}$).
     - Row 2048 corresponds to maximum world $Z = +2048.0\text{ m}$ (North, Northing $101514\text{ m}$).
     - Col 0 corresponds to minimum world $X = -2048.0\text{ m}$ (West, Easting $466450\text{ m}$).
     - Col 2048 corresponds to maximum world $X = +2048.0\text{ m}$ (East, Easting $470546\text{ m}$).
2. **Continuous Grid Coordinate Mapping**:
   For any Cartesian point $(X, Z) \in [-2048.0, 2048.0]$:
   $$u(X) = \frac{X - (-2048.0)}{2.0} = \frac{X + 2048.0}{2.0} \in [0.0, 2048.0]$$
   $$v(Z) = \frac{Z - (-2048.0)}{2.0} = \frac{Z + 2048.0}{2.0} \in [0.0, 2048.0]$$
3. **Nearest-Neighbor Sampling**:
   $$\text{col} = \text{clamp}(\lfloor u + 0.5 \rfloor, 0, 2048)$$
   $$\text{row} = \text{clamp}(\lfloor v + 0.5 \rfloor, 0, 2048)$$
   $$Y(X, Z) = \text{Heightmap}[\text{row}, \text{col}] \times 0.01$$
4. **Bilinear Interpolation (Recommended for Smooth Object Grounding)**:
   $$c_0 = \lfloor u \rfloor, \quad c_1 = \min(c_0 + 1, 2048), \quad s = u - c_0$$
   $$r_0 = \lfloor v \rfloor, \quad r_1 = \min(r_0 + 1, 2048), \quad t = v - r_0$$
   $$h_{00} = \text{Heightmap}[r_0, c_0] \times 0.01$$
   $$h_{10} = \text{Heightmap}[r_0, c_1] \times 0.01$$
   $$h_{01} = \text{Heightmap}[r_1, c_0] \times 0.01$$
   $$h_{11} = \text{Heightmap}[r_1, c_1] \times 0.01$$
   $$Y(X, Z) = (1 - s)(1 - t) h_{00} + s(1 - t) h_{10} + (1 - s) t h_{01} + s t h_{11}$$
5. **Direct Binary File Seeking (without loading entire file into memory)**:
   Given `(row, col)`, the exact byte offset in `Heightmap.raw` is:
   $$\text{offset} = (\text{row} \times 2049 + \text{col}) \times 2$$
   Read 2 bytes, unpack as unsigned short little-endian (`<H`), and multiply by $0.01$.

### 2.3 OSM Building Footprint Extraction & Transformation Pipeline
1. **Extraction Source Hierarchy**:
   - **Tier 1 (Fastest & 100% Reliable)**: Official OSM 0.6 API queried in 4 spatial quadrants (`/api/0.6/map?bbox=min_lon,min_lat,max_lon,max_lat`).
     - Mid-latitude: $46.034271^\circ$, Mid-longitude: $14.593029^\circ$.
     - Total payload: ~21 MB XML across 4 requests. Complete in $< 6$ seconds.
   - **Tier 2 (Fallback 1)**: Overpass API with retry across global mirrors (`overpass-api.de`, `lz4.overpass-api.de`, `overpass.kumi.systems`) using a designated User-Agent header.
   - **Tier 3 (Fallback 2)**: Geofabrik Slovenia country extract (`slovenia-latest.osm.pbf`) filtered with `ogr2ogr -spat`.
2. **Polygon Geometry Processing**:
   - Extract nodes $(nid \to (\lambda, \phi))$.
   - Reconstruct closed ways with `building=*` and relations with `type=multipolygon` + `building=*`.
   - Convert vertices $(\lambda_i, \phi_i) \to (E_i, N_i)$ via EPSG:3794, then to Cartesian $(X_i, Z_i) = (E_i - 468498, N_i - 99466)$.
   - Filter out buildings whose bounding boxes fall strictly outside $[-2048, 2048]$.
3. **Centroid & Yaw Calculation**:
   - Polygon area: $A = \frac{1}{2} \sum_{i=0}^{n-1} (X_i Z_{i+1} - X_{i+1} Z_i)$.
   - Centroid:
     $$C_X = \frac{1}{6A} \sum_{i=0}^{n-1} (X_i + X_{i+1}) (X_i Z_{i+1} - X_{i+1} Z_i)$$
     $$C_Z = \frac{1}{6A} \sum_{i=0}^{n-1} (Z_i + Z_{i+1}) (X_i Z_{i+1} - X_{i+1} Z_i)$$
   - Ground elevation: $C_Y = \text{BilinearSample}(C_X, C_Z)$.
   - Yaw / Heading angle:
     Find the longest polygon edge vector $(\Delta X, \Delta Z)$:
     $$\text{yaw} = \text{degrees}(\text{atan2}(\Delta X, \Delta Z))$$
     Normalized to $[-180^\circ, 180^\circ]$. Pitch = 0.0, Roll = 0.0.
4. **Mesh Mapping Logic**:
   - Map building tags (`building`, `building:levels`, area $A$) to vanilla BF2 static meshes:
     - Area $> 400\text{ m}^2$ or levels $\ge 3$: `eu_office_01`, `eu_building_02`, `me_apartment_01`.
     - Area $80\text{ m}^2 - 250\text{ m}^2$ (residential): `eu_house_01`, `eu_house_02`, `me_house_01`.
     - Industrial / commercial: `warehouse_01`, `factory_01`.
     - Area $< 50\text{ m}^2$ (sheds/garages): `shed_01`, `wooden_shack_01`.

### 2.4 LiDAR Canopy Processing & Overgrowth Density Masks Pipeline
1. **Tile Acquisition**:
   - Sequential download of the 25 nDMP GeoTIFFs from `tiles_manifest.json` into `/home/ator/BF2/ndmp/`.
   - Sleep $1.2\text{ s}$ between requests to prevent HTTP 429 rate limiting.
2. **Mosaicking & Resampling to Terrain Grid**:
   - Mosaic bounds: $E \in [466000, 471000]$, $N \in [97000, 102000]$ ($5000\text{ m} \times 5000\text{ m}$).
   - Crop window to level bounds:
     - Easting offset: $X_{\text{start}} = 450\text{ m}$ to $X_{\text{end}} = 4546\text{ m}$ ($4096\text{ m}$).
     - Northing offset: $Y_{\text{start}} = 486\text{ m}$ (from top $N = 102000$) to $Y_{\text{end}} = 4582\text{ m}$ ($4096\text{ m}$).
   - Target raster size:
     - Resample canopy heights to $2049 \times 2049$ (or $2048 \times 2048$) using average downsampling (LiDAR $0.5\text{ m} \to 2.0\text{ m}$ reduces $4 \times 4$ blocks, eliminating noise).
3. **Density Channel Classification**:
   - In Refractor 2, overgrowth uses multi-channel density textures (e.g. 8-bit channels mapped to mesh definitions):
     - **Channel 0 (High Canopy Forest, height $> 12\text{ m}$)**:
       $$\text{density}_0 = \text{clamp}\left(\frac{H - 12.0}{15.0}, 0.0, 1.0\right) \times 255$$
       Populates large pine and oak trees along the Golovec ridge.
     - **Channel 1 (Medium Mixed Woodland, height $5\text{ m} - 12\text{ m}$)**:
       $$\text{density}_1 = \text{clamp}\left(\frac{H - 5.0}{7.0}, 0.0, 1.0\right) \times \left(1.0 - \text{clamp}\left(\frac{H - 12.0}{4.0}, 0.0, 1.0\right)\right) \times 255$$
       Populates birch, small trees, and woodland borders.
     - **Channel 2 (Undergrowth / Shrubs, height $1.5\text{ m} - 5\text{ m}$)**:
       $$\text{density}_2 = \text{clamp}\left(\frac{H - 1.5}{3.5}, 0.0, 1.0\right) \times \left(1.0 - \text{clamp}\left(\frac{H - 5.0}{2.0}, 0.0, 1.0\right)\right) \times 255$$
       Populates bushes and thick ground foliage.
     - **Channel 3 (Ground Clutter / Open Clearings, height $< 1.5\text{ m}$)**:
       Light ground grass.

---

## 3. Caveats

1. **Flycom Server Throttling**:
   - Concurrent downloads or unthrottled requests to `assets.flycom.si` return `HTTP 429 Too Many Requests`. The canopy processing script MUST use serial requests with a 1.0–1.5 second inter-tile pause.
2. **Disk Space Management**:
   - Partition `/dev/mapper/data-root` has 2.1 GB free space. The 25 nDMP GeoTIFFs take ~250 MB total. Do not generate uncompressed 32-bit floating point full mosaics; process tiles in a streaming window or direct downsampled accumulation buffer.
3. **Building Collisions & Footprint Density**:
   - Ljubljana urban fringe has thousands of building footprints. A raw dump without minimum distance filtering could generate static object clusters that overload the BF2 static object limits (typically max 1,000–3,000 static objects per level for optimal performance). The extraction pipeline should apply a priority filter (e.g. retain significant structures and representative houses, filtering out micro-sheds $< 15\text{ m}^2$).
4. **Orientation Ambiguity**:
   - In 2D building footprints, the principal orientation has a $180^\circ$ symmetry. For BF2 vanilla buildings (which have distinct front entrances), setting yaw along the longest street-facing segment produces visually plausible placement.

---

## 4. Conclusion

1. **Coordinate System Specification**:
   - Origin: D96TM `[468498.0 E, 99466.0 N]`, WGS84 `[46.034276 N, 14.592945 E]`.
   - BF2 Cartesian: $X = \text{Easting} - 468498.0$ ($+X$ East), $Z = \text{Northing} - 99466.0$ ($+Z$ North).
   - Golovec Focal Point: D96TM `[468498 E, 100831 N]`, WGS84 `[46.046559 N, 14.592945 E]` $\implies$ Cartesian $(X=0, Z=1365)$.
2. **Heightmap Sampling Specification**:
   - File: `Heightmap.raw` ($2049 \times 2049$ uint16 little-endian, scale $0.01\text{ m}$, 0 header bytes).
   - Coordinate mapping: $u = (X + 2048)/2.0$, $v = (Z + 2048)/2.0$.
   - Row 0 is South ($Z = -2048$), Row 2048 is North ($Z = +2048$); Col 0 is West ($X = -2048$), Col 2048 is East ($X = +2048$).
   - Bilinear interpolation produces exact ground elevation $Y$ in meters.
3. **OSM Extraction Specification**:
   - Split 4096m x 4096m WGS84 bounding box `[46.015750, 14.566437, 46.052791, 14.619621]` into 4 quadrants.
   - Fetch XML via official OSM 0.6 API (verified: $< 6\text{ s}$ total, no node limits).
   - Transform vertices to Cartesian $(X, Z)$, compute polygon centroid $(C_X, C_Z)$, sample ground height $C_Y$, calculate longest-edge yaw, and map to BF2 vanilla building meshes.
4. **LiDAR Canopy & Overgrowth Specification**:
   - Sequentially download 25 nDMP GeoTIFFs from `tiles_manifest.json` with 1.2s delay.
   - Resample $0.5\text{ m} \to 2.0\text{ m}$ over map bounds $[466450, 470546]\text{ E} \times [97418, 101514]\text{ N}$.
   - Generate multi-channel density masks classifying high canopy ($>12\text{ m}$), medium woodland ($5-12\text{ m}$), and undergrowth ($1.5-5\text{ m}$).
   - Configure `OvergrowthSystem.con` linking mesh templates to these density channels.

---

## 5. Verification Method

To independently verify all formulas, coordinates, and sampling routines, execute the following automated Python verification script:

```bash
python3 -c "
import pyproj, numpy as np

# 1. Coordinate Transformation Verification
t_to_d96 = pyproj.Transformer.from_crs('EPSG:4326', 'EPSG:3794', always_xy=True)
t_to_wgs = pyproj.Transformer.from_crs('EPSG:3794', 'EPSG:4326', always_xy=True)

# Origin verification
orig_e, orig_n = 468498.0, 99466.0
lon, lat = t_to_wgs.transform(orig_e, orig_n)
assert abs(lat - 46.034273) < 1e-4 and abs(lon - 14.593038) < 1e-4
print('Origin Transformation: PASS')

# Focal point verification
foc_lon, foc_lat = 14.592945, 46.046559
fe, fn = t_to_d96.transform(foc_lon, foc_lat)
fx, fz = fe - orig_e, fn - orig_n
assert abs(fx - 0.0) < 1.0 and abs(fz - 1365.0) < 1.0
print(f'Focal Point Transformation: PASS (X={fx:.2f}, Z={fz:.2f})')

# 2. Heightmap Sampling Verification
hmap = np.fromfile('/home/ator/BF2/Heightmap.raw', dtype='<u2').reshape((2049, 2049))

def sample(x, z):
    u = np.clip((x + 2048.0) / 2.0, 0.0, 2048.0)
    v = np.clip((z + 2048.0) / 2.0, 0.0, 2048.0)
    c0, r0 = int(np.floor(u)), int(np.floor(v))
    c1, r1 = min(c0 + 1, 2048), min(r0 + 1, 2048)
    s, t = u - c0, v - r0
    h00 = hmap[r0, c0] * 0.01
    h10 = hmap[r0, c1] * 0.01
    h01 = hmap[r1, c0] * 0.01
    h11 = hmap[r1, c1] * 0.01
    return (1 - s)*(1 - t)*h00 + s*(1 - t)*h10 + (1 - s)*t*h01 + s*t*h11

elev_focal = sample(0.0, 1365.0)
assert 270.0 < elev_focal < 280.0
print(f'Focal Point Elevation Sample: PASS ({elev_focal:.2f} m)')

# Corner bounds check
assert sample(-2048, -2048) == hmap[0, 0] * 0.01
assert sample(2048, 2048) == hmap[2048, 2048] * 0.01
print('Boundary Clamping & Indexing: PASS')
"
```

Invalidation conditions:
- Any discrepancy in `Heightmap.raw` corner elevations.
- Deviation of focal point Cartesian coordinates exceeding $\pm 1.0\text{ m}$ from $(0, 1365)$.
- Inability to query OSM API quadrants or Flycom nDMP headers.
