# Forensic Integrity Audit Report: Milestone 1

**Work Product**: `/home/ator/BF2/scripts/extract_osm_buildings.py`, `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con`, `/home/ator/BF2/.osm_cache/`  
**Profile**: General Project  
**Integrity Mode**: development (`ORIGINAL_REQUEST.md` line 8)  
**Auditor**: teamwork_auditor (`auditor_m1`)  
**Verdict**: **CLEAN**  

---

## 1. Observation

### 1.1 Scope and Integrity Mandate
- Directly read `ORIGINAL_REQUEST.md` (lines 8, 12–14, 26–30):
  - Integrity mode: `development`.
  - OpenStreetMap building footprint extraction for 4096m x 4096m bounding box centered on Golovec.
  - Coordinate origin $(0, 0, 0)$ mapped to D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E].
  - Ground elevation $Y$ sampled from `Heightmap.raw` (2049x2049 uint16 little-endian, 2.0m spacing, scale 0.01).
  - Footprints mapped to BF2 European vanilla static meshes in `StaticObjects.con`.
- Directly read `DISPATCH.md`:
  - Static analysis of `scripts/extract_osm_buildings.py` for authentic parsing, transformations, Shoelace area, Green's centroid, bilinear sampling, and absence of hardcoded outputs/bypasses.
  - Runtime execution audit: verify `StaticObjects.con` was genuinely produced from `.osm_cache/` and `Heightmap.raw`.
  - Inspection of `.osm_cache/*.xml` files for authentic OSM responses.

### 1.2 Inspection of `.osm_cache/` XML Files
Inspected all four quadrant XML files in `/home/ator/BF2/.osm_cache/`:
- `osm_SW.xml`: 2,898,298 bytes, 36,031 lines.
  - Header: `<osm version="0.6" generator="openstreetmap-cgimap 2.1.1 (651746 spike-07.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">`
  - Bounds: `<bounds minlat="46.0157500" minlon="14.5664370" maxlat="46.0342710" maxlon="14.5930290"/>`
- `osm_SE.xml`: 4,162,739 bytes, 51,703 lines.
  - Header: generator `openstreetmap-cgimap 2.1.1 (651746 spike-07.openstreetmap.org)`.
  - Bounds: `<bounds minlat="46.0157500" minlon="14.5930290" maxlat="46.0342710" maxlon="14.6196210"/>`
- `osm_NW.xml`: 6,680,463 bytes, 87,771 lines.
  - Header: generator `openstreetmap-cgimap 2.1.1 (714814 spike-07.openstreetmap.org)`.
  - Bounds: `<bounds minlat="46.0342710" minlon="14.5664370" maxlat="46.0527910" maxlon="14.5930290"/>`
- `osm_NE.xml`: 7,185,369 bytes, 92,703 lines.
  - Header: generator `openstreetmap-cgimap 2.1.1 (668226 spike-07.openstreetmap.org)`.
  - Bounds: `<bounds minlat="46.0342710" minlon="14.5930290" maxlat="46.0527910" maxlon="14.6196210"/>`
- Findings: All files contain genuine OSM elements with valid changeset numbers, UTC timestamps, user IDs, real usernames (`martianfreeloader`, `Mark Martinec`, `gustavs`), and Slovenian geographical tags (`Ljubljana Bizovik`, `Papirnica Vevče`, `Športna dvorana Kašelj`). Total elements parsed across files: 75,681 nodes, 8,045 ways, 291 relations.

### 1.3 Static Analysis of `scripts/extract_osm_buildings.py`
Code analysis of all 574 lines in `/home/ator/BF2/scripts/extract_osm_buildings.py`:
- **OSM Parsing** (`parse_osm_data` lines 297–324, `stitch_ways` lines 96–140):
  - Genuinely parses `<node>`, `<way>`, and `<relation>` elements via `xml.etree.ElementTree`.
  - Correctly stitches fragmented outer ways of multipolygon relations into continuous closed boundary rings.
- **Coordinate Transformation** (`wgs_to_cartesian` lines 57–60):
  - Uses `pyproj.Transformer.from_crs('EPSG:4326', 'EPSG:3794', always_xy=True)` to convert WGS84 $(\text{Lon}, \text{Lat})$ to Slovenian national grid D96TM $(E, N)$.
  - Origin offset: $X = E - 468498.0$, $Z = N - 99466.0$.
  - Mathematical verification: Transforming D96TM $(468498.0, 99466.0)$ to WGS84 yields $(46.03427334^\circ\text{ N}, 14.59303787^\circ\text{ E})$, which maps back to Cartesian $(0.00000000, 0.00000000)$ with zero residual error.
- **Shoelace Area & Green's Theorem Centroid** (`compute_polygon_metrics` lines 143–180):
  - Area computed as $A = |0.5 \sum (X_i Z_{i+1} - X_{i+1} Z_i)|$.
  - Centroid computed via Green's Theorem line integral:
    $C_X = \frac{1}{6A_{signed}} \sum (X_i + X_{i+1}) (X_i Z_{i+1} - X_{i+1} Z_i)$,
    $C_Z = \frac{1}{6A_{signed}} \sum (Z_i + Z_{i+1}) (X_i Z_{i+1} - X_{i+1} Z_i)$.
  - Orientation: Longest-edge azimuth $\text{yaw} = \text{atan2}(\Delta X, \Delta Z) \times \frac{180}{\pi}$, normalized to $[-180^\circ, 180^\circ]$.
  - Analytic test: Verified on a $10 \times 20$ rectangle (Area = 200.0, Centroid = $(5.0, 10.0)$) and a $(6, 6)$ triangle (Area = 18.0, Centroid = $(2.0, 2.0)$) — exact match.
- **Heightmap Bilinear Interpolation** (`HeightmapSampler` lines 66–90):
  - Reads raw $2049 \times 2049 \times 2$ bytes uint16 little-endian array from `Heightmap.raw` ($8,396,898$ bytes).
  - Grid indices: $u = (X + 2048.0) / 2.0$, $v = (Z + 2048.0) / 2.0$.
  - Bilinear weights: $s = u - \lfloor u \rfloor$, $t = v - \lfloor v \rfloor$.
  - Elevation scale: $0.01\text{ m/unit}$.
  - Analytic test: On-grid sample $(0.0, 0.0)$ matches raw cell $(1024, 1024) \times 0.01$; off-grid sample $(1.0, 1.0)$ matches four-corner average with $0.0000\text{ m}$ deviation.
- **Prohibited Pattern Search**:
  - Hardcoded test results: None found.
  - Fake coordinates / mock candidate lists: None found.
  - Stubs / dummy facade functions: None found. All logic is genuine and computed dynamically.

### 1.4 Runtime Execution & Byte-Level Reproducibility
- Executed `scripts/extract_osm_buildings.py` to a temporary output file and compared with `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con`:
  - Existing file size: 166,753 bytes, 6,554 lines, 1,309 objects.
  - Re-generated file size: 166,753 bytes, 6,554 lines, 1,309 objects.
  - Byte-for-byte identical: **`True`** (0 byte differences).
- End-to-end data lineage tracing:
  - Selected building #1: `way_93723159` ("Papirnica Vevče") in quadrant NW.
  - Tags in `osm_NW.xml`: `building=industrial`, `name=Papirnica Vevče`, 25 boundary nodes.
  - Independent manual calculation from raw XML nodes:
    - Template: `warehouse_01` (from industrial tag + area $28,400\text{ m}^2 \ge 300\text{ m}^2$).
    - Cartesian position: $-61.151 / 273.481 / 1317.488$.
    - Yaw rotation: $0.294^\circ$.
  - Line 6–9 of `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con`:
    ```con
    Object.create warehouse_01
    Object.absolutePosition -61.151/273.481/1317.488
    Object.rotation 0.294/0.000/0.000
    Object.layer 1
    ```
  - Exact match verified.

### 1.5 Test Suite Results
- `tests/test_tier4_real_world_gameplay.py -k static`: 5/5 PASSED.
- `tests/test_tier2_boundary_corner.py -k static_objects`: 5/5 PASSED.
- `tests/test_tier1_feature_coverage.py -k static`: 4/4 PASSED.
- `tests/test_tier1_feature_coverage.py -k test_case_sensitivity_object_commands`: 1/1 PASSED.
- `tests/test_adversarial_static_objects.py`: 21/21 PASSED.
- `tests/adversarial_m1_2_spatial_check.py`: VERDICT `CONFIRM` (0 collisions, 0 OBB intersections, min distance $30.0036\text{ m}$).

---

## 2. Logic Chain

1. **Authenticity of Raw Data**:
   - The XML files in `.osm_cache/` originate directly from the official OpenStreetMap 0.6 API via `openstreetmap-cgimap`. Real OpenStreetMap node IDs, changesets, and usernames verify the input is genuine real-world geographic data, not simulated or pre-baked data.
2. **Mathematical Correctness**:
   - Coordinate transformation mathematically implements the EPSG:4326 to EPSG:3794 projection with zero offset at the origin.
   - The Shoelace formula and Green's Theorem centroid calculate polygon area and geometric centroid invariant to vertex winding order.
   - Bilinear elevation sampling on `Heightmap.raw` exactly adheres to the 2.0m grid spacing and 0.01 height scale specified in `ORIGINAL_REQUEST.md`.
3. **Data Lineage and Determinism**:
   - Running `scripts/extract_osm_buildings.py` against `.osm_cache/*.xml` and `Heightmap.raw` produces a file that is byte-for-byte identical to `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con`. This proves conclusively that `StaticObjects.con` was genuinely compiled from the raw sources and was not manually edited, mocked, or fabricated.
4. **Absence of Prohibited Patterns**:
   - No hardcoded test results, facade implementations, or test-bypass logic exists in the codebase.
   - Under Development Mode (and even under Demo Mode), library usage (`pyproj`, `numpy`) is permitted and auxiliary to the custom extraction and conversion pipeline.

---

## 3. Caveats

- **OSM Building Density on Golovec Ridge**:
  - Real-world OpenStreetMap data contains no buildings above 300m elevation on the central Golovec ridge because Golovec is a designated forest park and natural upland. This is genuine geographic reality, not an extraction omission. Forest coverage for this area is correctly delegated to Milestone 2 (LiDAR canopy & overgrowth).
- **Subsequent Milestones**:
  - This audit covers Milestone 1 deliverables (`extract_osm_buildings.py`, `StaticObjects.con`, `.osm_cache/`). Milestones 2 and 3 will be verified during their respective audit phases.

---

## 4. Conclusion

The Milestone 1 work product meets all forensic integrity standards:
- **Verdict**: **`CLEAN`**
- All 1,309 static objects in `levels/slovenia_golovec/StaticObjects.con` are derived from authentic OpenStreetMap footprints.
- Ground elevation $Y$ is accurately interpolated from `Heightmap.raw` with a maximum deviation $< 0.0006\text{ m}$.
- All coordinates fall strictly within the $[-2048.0, 2048.0]$ Cartesian boundary.
- Zero integrity violations detected.

---

## 5. Verification Method

To independently reproduce this forensic audit:

### 5.1 Re-run Extraction and Test for Byte-Level Identity
```bash
python3 -c "
from scripts.extract_osm_buildings import extract_buildings, apply_spatial_thinning, write_static_objects_con
import tempfile

raw = extract_buildings('/home/ator/BF2/Heightmap.raw', '/home/ator/BF2/.osm_cache', 35.0, 270.0)
selected = apply_spatial_thinning(raw, 30.0)

with tempfile.NamedTemporaryFile('w+', delete=True) as tmp:
    write_static_objects_con(selected, tmp.name)
    tmp.seek(0)
    generated = tmp.read()

with open('/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con', 'r') as f:
    existing = f.read()

assert generated == existing, 'Byte-level mismatch detected!'
print('CONFIRMED: StaticObjects.con is byte-for-byte reproducible.')
"
```

### 5.2 Run All Verification & Stress Test Suites
```bash
PYTHONPATH=tests python3 -m unittest -v tests/test_tier4_real_world_gameplay.py -k static
PYTHONPATH=tests python3 -m unittest -v tests/test_tier2_boundary_corner.py -k static_objects
PYTHONPATH=tests python3 -m unittest -v tests/test_tier1_feature_coverage.py -k static
PYTHONPATH=tests python3 -m unittest -v tests/test_tier1_feature_coverage.py -k test_case_sensitivity_object_commands
PYTHONPATH=tests python3 -m unittest -v tests/test_adversarial_static_objects.py
python3 tests/adversarial_m1_2_spatial_check.py
```
Expected output: All unit and adversarial tests pass with 0 errors and 0 failures.

### 5.3 Invalidation Conditions
- Any difference between newly generated `StaticObjects.con` and existing `StaticObjects.con`.
- Any static object with $X$ or $Z$ outside $[-2048.0, 2048.0]$.
- Any static object with $Y < 270.0\text{ m}$ or $|Y - \text{Heightmap.raw}(X, Z)| > 0.001\text{ m}$.
- Any presence of hardcoded mock building lists or bypassed calculations in `scripts/extract_osm_buildings.py`.
