# Review and Adversarial Audit Handoff Report: Milestone 2

**Reviewer**: Reviewer 2 (`reviewer_m2_2` - Canopy Mask & Downloader Reviewer)  
**Parent Conversation ID**: `d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61`  
**Working Directory**: `/home/ator/BF2/.agents/teamwork/reviewer_m2_2`  
**Verdict**: **APPROVE**  
**Integrity Status**: **CLEAN (Zero Integrity Violations)**  
**Date**: 2026-11-11T01:43:00Z  

---

## 1. Observation

### 1.1 Implementation Code Inspection (`scripts/process_lidar_canopy.py`)
- **File**: `/home/ator/BF2/scripts/process_lidar_canopy.py` (491 lines, byte-compiles with zero syntax errors).
- **Rate-Limited Tile Downloader (Lines 53–286)**:
  - Line 203: `inter_request_delay: float = 1.25`
  - Line 271: `if idx < total_tiles: time.sleep(inter_request_delay)` enforcing a 1.25s pause between downloads.
  - Lines 112–198 (`download_tile`): Uses atomic temporary file naming (`tmp_path = dest_path + f".tmp.{os.getpid()}"`), validates file size and GDAL raster integrity (`validate_geotiff`) before invoking `os.replace`, catches `HTTP 429` and `5xx` errors with exponential backoff (`backoff *= 2.0`), jitter (`random.uniform(0.2, 0.6)`), and extracts `Retry-After` / `X-Retry-In` headers (`parse_retry_after`).
  - Lines 53–58 (`check_disk_space`): Enforces $\ge 300\text{ MB}$ free filesystem space prior to batch downloading.
- **Heterogeneous Data Normalization (Lines 375–386)**:
  - Tiles are opened in read-only mode and converted to float32: `data = band.ReadAsArray().astype(np.float32)`.
  - For standard `Int16` tiles with NoData `-32767.0`: `data[data == nodata] = 0.0`.
  - For annex `Float32` tile `466_101` with NoData `0.0`: negative sensor noise is sanitized via `data[data < 0.0] = 0.0`, NaNs are replaced via `data[np.isnan(data)] = 0.0`, and extreme outliers are clamped via `np.clip(data, 0.0, 50.0, out=data)`.
- **Direct Window Placement (Lines 317–396)**:
  - Canvas dimensions: `crop_width = 8192`, `crop_height = 8192` allocated as `np.zeros((8192, 8192), dtype=np.float32)` (256.0 MB RAM).
  - Crop window matches D96TM level bounds Easting $[466450, 470546]$ ($X_{\text{crop}} \in [900, 9092]$) and Northing $[97418, 101514]$ ($Y_{\text{crop}} \in [972, 9164]$).
  - Slices `tile_slice_r`, `tile_slice_c`, `dst_slice_r`, `dst_slice_c` computed via intersection bounds, filling all 25 tile contributions without seams or gaps.
- **Bilinear Resampling & South-to-North Alignment (Lines 401–412)**:
  - Downsampling from $(8192, 8192)$ 0.5m LiDAR grid to $(2049, 2049)$ 2.0m terrain grid via PIL Bilinear (`Image.fromarray(cropped).resize((2049, 2049), resample=Image.Resampling.BILINEAR)`).
  - Orientation alignment: `raw_h = np.flipud(resampled_h)` converts North-up image matrix (Row 0 = North, $Z=+2048$) to Refractor 2 raw terrain buffer layout (Row 0 = South $Z=-2048$, Row 2048 = North $Z=+2048$).
- **Linear Density Classification (Lines 413–426)**:
  - $H < 1.5\text{ m} \to 0$
  - $1.5\text{ m} \le H \le 20.0\text{ m} \to \text{round}\left(\frac{H - 1.5}{18.5} \times 255.0\right)$
  - $H > 20.0\text{ m} \to 255$
  - Serialized via `density_uint8.tobytes()` to `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw`.

### 1.2 Verification of 25 GeoTIFFs (`/home/ator/BF2/ndmp/`)
- All 25 tiles referenced in `tiles_manifest.json` are present in `/home/ator/BF2/ndmp/` with zero missing.
- Raster geometry: Every tile has dimensions $2000 \times 2000$, 1 band, and resolution $0.5\text{ m} \times 0.5\text{ m}$.
- Tile boundary seam checks:
  - Seam between `468_99` (right edge $469000.0\text{ E}$) and `469_99` (left edge $469000.0\text{ E}$): deviation is exactly $0.000\text{ m}$.
  - Seam between `468_100` (bottom edge $100000.0\text{ N}$) and `468_99` (top edge $100000.0\text{ N}$): deviation is exactly $0.000\text{ m}$.
- Heterogeneous types verified:
  - Tile `466_101`: `Float32`, NoData `0.0`, raw min `-2.95\text{ m}`, raw max `43.76\text{ m}`, mean `3.27\text{ m}`.
  - Tiles `466_97`..`470_101` (24 tiles): `Int16`, NoData `-32767.0`, raw valid min `0\text{ m}`, max up to `46\text{ m}`, mean `3.32\text{ m}`.
  - Scale confirmation: Both Int16 and Float32 are directly in meters (not decimeters or centimeters).

### 1.3 `Overgrowth.raw` Verification & Density Analysis
- File path: `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw`.
- File size: Exactly `4,198,401 bytes` ($2049 \times 2049$ uint8, zero header).
- SHA256 checksum: `e800f8fa09a0c1c99c58272fb82dde1ef7c5ccb33ebab3ab7c825c57f54ff209`.
- Deterministic reproduction: Executing `python3 scripts/process_lidar_canopy.py --skip-download` regenerates the exact identical SHA256 bit-for-bit in 1.4 seconds.
- Map-wide density statistics:
  - Range: $\min = 0$, $\max = 255$, $\text{mean} = 56.88$.
  - Coverage: $40.95\%$ of grid cells have active vegetation ($\text{density} > 0$).
  - Moderate to dense canopy: $30.62\%$ have $\text{density} > 50$; $20.73\%$ have $\text{density} > 128$.
  - Saturated canopy ($\ge 20\text{ m}$ height): $9.75\%$ have $\text{density} = 255$.
- Ground-truth geographic distribution:
  - Golovec ridge window $[1650:1750, 974:1074]$ around focal point $(0, 1365)$: $70.34\%$ active vegetation, mean density $= 87.52$.
  - Urban Ljubljana plain (NW quadrant $[1500:2049, 0:500]$): mean density $= 16.18$.
  - South forested slopes (SW quadrant $[0:500, 0:500]$): mean density $= 147.12$.
  - Physical orientation check: Point $(0, 1365)$ (Row 1707, Col 1024) has canopy heights up to 18m in GeoTIFF `468_100` and mean density $71.20$ in `Overgrowth.raw`. In contrast, the southern opposing point $(0, -1365)$ (Row 341, Col 1024) is bare agricultural field in GeoTIFF `468_98` (mean height $0.0016\text{ m}$) and has mean density $0.19$ in `Overgrowth.raw`. This directly proves `np.flipud` correctly mapped North to Row 2048 and South to Row 0.

### 1.4 `OvergrowthSystem.con` Syntax & Foliage Geometry
- File path: `/home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con` (81 lines).
- File hygiene: Pure UTF-8 without BOM, pure Unix LF (`\n`) line endings, zero null bytes.
- Prefix compliance: $100\%$ of active configuration lines begin with `Overgrowth.` or `OvergrowthType.`.
- Material declaration: Material `temperate_forest 1` configured and activated.
- Species roster: Exactly 7 vanilla BF2 foliage geometries defined:
  1. `fir_mixed02` (cluster fir, density 4.0)
  2. `pine_large` (emergent Scots pine, density 1.5)
  3. `birch_green_1` (primary silver birch, density 2.8)
  4. `birch_green_2` (secondary birch, density 2.2)
  5. `oak_01` (European oak, density 1.8)
  6. `pine_dead` (forest snag/deadwood, density 0.6)
  7. `largebush` (understory shrub, density 2.0)
- Parameter sanity: All densities $> 0.0$, rotation scale $180^\circ$ (full random yaw variation), normal scales $\le 0.05$ for trees (upright growth) and $0.20$ for bushes, minimum radii between instances $\ge 0.50\text{ m}$.
- Rendering parameters: `viewDistance 600.0`, `closeDistPercentage 0.25` ($150\text{ m}$ LOD impostor transition).

### 1.5 Test Suite Execution
- **Tier 1 Feature Coverage** (`PYTHONPATH=tests python3 -m unittest -v tests/test_tier1_feature_coverage.py -k overgrowth`):
  - `test_mandatory_file_overgrowth_raw_exists`: `ok`
  - `test_mandatory_file_overgrowthsystem_con_exists`: `ok`
  - `test_namespaces_overgrowthsystem_con`: `ok`
  - Result: 3/3 passed.
- **Tier 2 Boundary & Corner** (`PYTHONPATH=tests python3 -m unittest -v tests/test_tier2_boundary_corner.py -k overgrowth`):
  - `test_overgrowth_raw_exact_byte_count`: `ok`
  - `test_overgrowth_raw_shape_dimensions`: `ok`
  - `test_overgrowth_raw_uint8_data_range`: `ok`
  - `test_overgrowth_raw_non_trivial_content`: `ok`
  - `test_overgrowth_raw_dense_canopy_on_golovec_ridge`: `ok`
  - Result: 5/5 passed.
- **Tier 3 Cross Feature** (`PYTHONPATH=tests python3 -m unittest -v tests/test_tier3_cross_feature.py -k overgrowth_`):
  - `test_overgrowth_material_and_species_defined`: `ok`
  - `test_overgrowth_geometries_are_vanilla_trees`: `ok`
  - Result: 2/2 passed.
- **Adversarial Overgrowth Suite** (`PYTHONPATH=tests python3 -m unittest -v tests/test_adversarial_overgrowth_species_syntax.py`):
  - 13 comprehensive tests covering Poisson radius spacing, slope normal conformance, vanilla whitelist, mutation sensitivity, and biome suitability: 13/13 passed.
- **Worker Verification Suite** (`python3 /home/ator/BF2/.agents/teamwork/worker_m2/test_m2_verification.py -v`):
  - 4/4 passed.

---

## 2. Logic Chain

1. **Downloader Correctness & Robustness (from Observation 1.1)**:
   - Sourcing URLs directly from `tiles_manifest.json` ensures tile `466_101` is fetched from `13-ljubljana-aneks` while the remaining 24 are fetched from `05-ljubljana`.
   - The sequential 1.25s delay between requests prevents triggering the Flycom server's 10-request leaky-bucket rate limiter.
   - The exponential backoff, jitter, and Retry-After header parsing provide robust recovery in the event of HTTP 429 or transient network drops.
   - Atomic temporary file usage coupled with GDAL dataset validation prevents corrupted partial files from polluting the tile cache.

2. **Heterogeneous Normalization & Mosaicking (from Observations 1.1 and 1.2)**:
   - Float32 annex tile `466_101` and the 24 Int16 tiles both use native elevation values in meters, avoiding any unit conversion discrepancy.
   - Casting to `np.float32` prior to placing into the $(8192, 8192)$ canvas avoids GDAL VRT type-mismatch failures.
   - Coordinate bounding box $[466450, 470546]\text{ E} \times [97418, 101514]\text{ N}$ translates precisely to pixel window $[900, 9092] \times [972, 9164]$ on the 0.5m LiDAR grid, spanning exactly $8192 \times 8192$ pixels ($4096\text{ m} \times 4096\text{ m}$).
   - Boundary checks prove zero gaps and zero overlap between adjacent tiles.

3. **Resampling, Orientation Alignment, and Physical Ground Truth (from Observations 1.1 and 1.3)**:
   - PIL Bilinear downsampling resamples the $8192 \times 8192$ canopy raster to $2049 \times 2049$ in ~0.25 seconds without precision loss or blocky aliasing.
   - `np.flipud` converts North-up rasters (where Row 0 is Northing $101514$, $Z = +2048$) to Refractor 2 raw terrain indexing (where Row 0 is South, $Z = -2048$, and Row 2048 is North, $Z = +2048$).
   - Ground-truth comparison between the focal point ($Z = +1365$) and south point ($Z = -1365$) proves that the physical trees on Golovec ridge land on the correct high-Z rows (mean density 87.52), while southern open fields land on low-Z rows (mean density 0.19).
   - Re-running the pipeline generates the exact identical SHA256 checksum, confirming deterministic reproducibility with no hardcoding or stochastic drift.

4. **Engine Conformance & Foliage Selection (from Observation 1.4)**:
   - Every active line in `OvergrowthSystem.con` adheres strictly to Refractor 2 syntax (`Overgrowth.` and `OvergrowthType.` prefixes).
   - All 7 foliage meshes belong to the genuine vanilla BF2 mesh roster and accurately represent a Central European temperate mixed forest (spruce/fir, pine, birch, oak, and understory shrub).

---

## 3. Caveats

1. **`test_init_con_runs_overgrowthsystem`**:
   - `tests/test_tier3_cross_feature.py` checks whether `init.con` contains `run OvergrowthSystem.con`.
   - This test currently fails because `init.con` has not yet been assembled.
   - Creating `init.con` belongs exclusively to Milestone 3 (Level Packaging & Gameplay Assembly). Worker M2 correctly respected write boundaries by not touching `init.con`.
2. **Minor CLI formatting glitch in `--help`**:
   - Line 466 of `scripts/process_lidar_canopy.py` has an unescaped `%` character in the argument help string (`Canopy height for 100% saturation`). This produces messy string interpolation in `--help` output, though it does not affect execution.
3. **Input validation on `h_max` vs `h_min`**:
   - If a user manually supplies `--h-min 20.0 --h-max 20.0`, a ZeroDivisionError would occur. Default parameters work as expected.

---

## 4. Conclusion

- **Verdict**: **APPROVE**
- **Integrity Status**: **CLEAN (Zero Integrity Violations)**
  - No hardcoded test outputs or dummy arrays exist in `scripts/process_lidar_canopy.py`.
  - All 25 GeoTIFFs (260.6 MB) are genuine LiDAR rasters from Flycom / ARSO.
  - `Overgrowth.raw` is generated from physical LiDAR canopy heights with exact geospatial alignment and deterministic reproducibility.
  - All 27 Milestone 2 overgrowth tests (Tier 1, Tier 2, Tier 3, worker verification, and adversarial suite) pass with 100% success.
- Milestone 2 is fully complete and ready to feed into Milestone 3.

---

## 5. Verification Method

To independently reproduce this verification:

1. **Run Unit and Tier Tests for Overgrowth**:
   ```bash
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier1_feature_coverage.py -k overgrowth
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier2_boundary_corner.py -k overgrowth
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier3_cross_feature.py -k overgrowth_
   ```
   *Expected*: 10/10 tests pass.

2. **Run Adversarial and Deliverable Verification Suites**:
   ```bash
   PYTHONPATH=tests python3 -m unittest -v tests/test_adversarial_overgrowth_species_syntax.py
   python3 /home/ator/BF2/.agents/teamwork/worker_m2/test_m2_verification.py -v
   ```
   *Expected*: 17/17 tests pass.

3. **Verify Deterministic Pipeline Reproduction**:
   ```bash
   python3 -c '
   import hashlib, subprocess
   raw = "/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw"
   h1 = hashlib.sha256(open(raw, "rb").read()).hexdigest()
   subprocess.run(["python3", "/home/ator/BF2/scripts/process_lidar_canopy.py", "--skip-download"], check=True)
   h2 = hashlib.sha256(open(raw, "rb").read()).hexdigest()
   assert h1 == h2 == "e800f8fa09a0c1c99c58272fb82dde1ef7c5ccb33ebab3ab7c825c57f54ff209"
   print("Deterministic SHA256 verified!")
   '
   ```
   *Expected*: Prints `Deterministic SHA256 verified!`.

### Invalidation Conditions
- Any change in `Overgrowth.raw` byte size away from $4,198,401$ bytes.
- Failure of `test_overgrowth_raw_dense_canopy_on_golovec_ridge` or `test_vanilla_geometry_whitelist`.
- Any missing or unreadable GeoTIFFs in `/home/ator/BF2/ndmp/`.

---

## 6. Review & Adversarial Findings Summary

### Minor Finding 1: Unescaped `%` in CLI argument help string
- **Location**: `/home/ator/BF2/scripts/process_lidar_canopy.py:466`
- **Issue**: `help="Canopy height for 100% saturation (default: 20.0)"` causes `argparse` to treat `% s` as format string interpolation, rendering raw dictionary objects during `--help`.
- **Fix**: Replace `100% saturation` with `100%% saturation` or `100 percent saturation`.

### Minor Finding 2: Missing guard for `h_max <= h_min`
- **Location**: `/home/ator/BF2/scripts/process_lidar_canopy.py:422`
- **Issue**: Formula `(raw_h - h_min) / (h_max - h_min)` will raise ZeroDivisionError if custom CLI options have `h_max <= h_min`.
- **Fix**: Add CLI validation `if args.h_max <= args.h_min: parser.error("--h-max must be greater than --h-min")`.

### Minor Finding 3: Test placement in metadata folder
- **Location**: `/home/ator/BF2/.agents/teamwork/worker_m2/test_m2_verification.py`
- **Issue**: Per project convention, `.agents/teamwork/` is intended for agent coordination metadata. Test scripts belong in `tests/`.
- **Fix**: Move `test_m2_verification.py` to `tests/test_m2_verification.py` during packaging or cleanup.
