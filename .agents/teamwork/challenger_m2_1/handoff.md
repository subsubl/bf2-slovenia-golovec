# Handoff Report: Milestone 2 - Challenger 1 (`challenger_m2_1`)
**Adversarial Canopy Mask Verifier**

- **Agent**: teamwork_challenger (`challenger_m2_1`)
- **Roles**: critic, specialist
- **Parent Conversation ID**: `d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61`
- **Working Directory**: `/home/ator/BF2/.agents/teamwork/challenger_m2_1`
- **Date**: 2026-11-11T01:42:00Z
- **Verdict**: **`CONFIRM`**

---

## Challenge Summary

**Overall risk assessment**: **`LOW`**

The generated canopy density mask `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw` and companion foliage configuration `/home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con` were subjected to an exhaustive battery of adversarial empirical stress tests. All four challenge criteria specified in the dispatch instructions are fully satisfied with rigorous mathematical and physical evidence.

---

## 1. Observation

### 1.1 Binary Artifact Integrity & File Size
- Direct filesystem inspection of `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw`:
  - Byte size: Exactly `4,198,401` bytes ($2049 \times 2049 \times 1\text{ byte}$).
  - Data type: `uint8` with zero-byte header (`data = np.fromfile(..., dtype=np.uint8)` yields element count `4,198,401`).
  - SHA256 checksum: `e800f8fa09a0c1c99c58272fb82dde1ef7c5ccb33ebab3ab7c825c57f54ff209`.

### 1.2 Value Bounds & Distribution
- Value range: $\min = 0$, $\max = 255$, $\text{mean} = 56.88$, $\text{std} = 90.48$.
- Value support: Exactly 256 unique values present out of 256 possible `uint8` values ($0 \dots 255$).
- Sentinel leakage analysis:
  - Count at $0$: $2,478,987$ ($59.05\%$ of total map, corresponding to bare ground, waterways, and non-forested urban/agricultural zones).
  - Count at $1$: $12,031$ ($0.29\%$).
  - Count at $2$: $11,925$ ($0.28\%$).
  - Count at $3$: $11,588$ ($0.28\%$).
  - Count at $4$: $11,224$ ($0.27\%$).
  - Count at $254$: $3,974$ ($0.09\%$).
  - Count at $255$: $409,387$ ($9.75\%$, saturation plateau for tall/mature tree crowns $\ge 20.0\text{ m}$).
  - Smooth monotonic frequency gradient at low values confirms that raw LiDAR NoData sentinels (`-32767` in Int16) were properly sanitized and clamped to $0.0$, with zero wrap-around to $1$ or $255$.

### 1.3 Spatial Density Validation
- **Golovec Pass ridge test window** (`[1650:1750, 974:1074]`, centered near $X = 0, Z = 1365$):
  - Mean canopy density: `87.52` (exceeds the $> 50$ threshold requirement).
  - Active vegetation coverage ($> 0$): $70.34\%$ ($7,034$ / $10,000$ pixels).
  - Dense vegetation ($> 50$): $59.15\%$ ($5,915$ / $10,000$ pixels).
  - Maximum canopy density: `255`.
- **Ljubljana urban lowlands window** (`[1274:1774, 274:774]`, 250,000 pixels):
  - Mean canopy density: `7.17`.
  - Median canopy density: `0.0`.
  - Non-vegetated pixels ($= 0$): $89.81\%$.
  - Low density ($\le 30$): $93.57\%$.
- **Water / River floor elevation band** ($Y < 270.0\text{ m}$):
  - Mean canopy density: `14.70`.
  - Median canopy density: `0.0`.
  - Non-vegetated pixels ($= 0$): $83.8\%$.
- **Elevation vs Canopy Density Gradient Table**:
  | Elevation Band | Pixel Count | Mean Density | Median | % Zeros | % Dense (>150) |
  |---|---:|---:|---:|---:|---:|
  | Water / River floor ($< 270\text{ m}$) | 269,063 | 14.70 | 0.0 | 83.8% | 3.7% |
  | Lowland Plain ($270 - 280\text{ m}$) | 1,026,298 | 16.87 | 0.0 | 76.4% | 3.0% |
  | Lower Foothills ($280 - 300\text{ m}$) | 1,245,757 | 16.29 | 0.0 | 81.6% | 3.9% |
  | Mid Slopes ($300 - 350\text{ m}$) | 1,058,359 | 110.40 | 83.0 | 30.8% | 38.7% |
  | Upper Ridge ($350 - 400\text{ m}$) | 489,586 | 131.70 | 137.0 | 22.4% | 47.6% |
  | Peaks / High Ridge ($\ge 400\text{ m}$) | 109,338 | 145.54 | 170.0 | 16.3% | 54.1% |

### 1.4 Orientation & Terrain Cross-Correlation
- Pearson correlation coefficient $r$ between `Heightmap.raw` ($2049 \times 2049$ uint16 $\times 0.01\text{ m}$) and `Overgrowth.raw` tested across all 8 spatial planar symmetries:
  - **Identity (as-is)**: **$r = +0.5233$**
  - FlipUD (inverted Z): $r = -0.2211$
  - FlipLR (inverted X): $r = +0.2018$
  - Transpose (swapped X, Z): $r = +0.3449$
  - Rot90: $r = -0.1031$
  - Rot180: $r = -0.3108$
  - Rot270: $r = -0.0150$
  - FlipUD + FlipLR: $r = -0.3108$
- High terrain peaks ($\ge 350\text{ m}$):
  - Out of 19 interior prominent peaks, forested ridges exhibit peak 20m-radius neighborhood mean densities up to $210.12$.
  - For un-forested peaks (e.g., peak at Row 947, Col 1780 with density 0), direct inspection of source LiDAR GeoTIFF `nDMP_470_99.tif` confirms genuine bare ground/open meadow in the ground-truth data ($0\text{ m}$ canopy height).
- Seam continuity across 1000m tile grid lines:
  - Mean pixel difference across tile boundary columns ($275, 775, 1275, 1775$) is $7.79 - 24.83$, matching normal intra-tile column variance ($5.53 - 25.94$). Zero seam step-artifacts exist.
- Pipeline Idempotence:
  - Running `/home/ator/BF2/scripts/process_lidar_canopy.py` on cached tiles executes in $< 2.0\text{ s}$ and generates bit-for-bit identical `Overgrowth.raw` (SHA256: `e800f8fa09a0c1c99c58272fb82dde1ef7c5ccb33ebab3ab7c825c57f54ff209`).

---

## 2. Logic Chain

1. **Byte & Type Integrity** (Observation 1.1):
   - Refractor 2 requires exact $(2049 \times 2049) \times 1\text{ byte} = 4,198,401\text{ bytes}$ for overgrowth channel density masks.
   - The file size matches this specification to the byte. Absence of headers or multi-byte values prevents engine deserialization crash.

2. **Data Cleansing & Distribution** (Observation 1.2):
   - In raw LiDAR GeoTIFFs, NoData is encoded as `-32767.0` (Int16) or `0.0` (Float32).
   - If signed negative sentinels leaked through downsampling into `uint8`, a severe artificial spike at value `1` or `255` would appear in water and lowland areas.
   - Empirical bin counts demonstrate a smooth, continuous falloff from value 1 ($0.29\%$) upward, proving that sanitization (`data < 0.0 -> 0.0`, `data == nodata -> 0.0`, `np.isnan -> 0.0`) was completely effective.

3. **Spatial Distribution Alignment** (Observation 1.3):
   - The Golovec ridge window `[1650:1750, 974:1074]` has a mean density of `87.52`, comfortably surpassing the required $> 50$ benchmark.
   - The lowlands and river floor show $> 83\%$ non-vegetated pixels and mean density $\le 16.87$, while the urban quadrant shows $89.81\%$ zeros and mean density $7.17$.
   - A steep, monotonic transition from bare lowlands ($14.70$ mean) to dense ridge forests ($145.54$ mean) verifies authentic spatial distribution matching real-world geography.

4. **Coordinate Orientation Symmetries** (Observation 1.4):
   - The Refractor 2 terrain buffer maps Row 0 to South ($Z = -2048$) and Row 2048 to North ($Z = +2048$), whereas GeoTIFF image rasters map Row 0 to North.
   - Testing 8 planar symmetries against `Heightmap.raw` reveals that `Identity (as-is)` achieves the global maximum correlation ($r = +0.5233$). Inverting the vertical coordinate (`FlipUD`) collapses the correlation to $r = -0.2211$.
   - This proves conclusively that the `np.flipud` applied in `process_lidar_canopy.py` is physically and geometrically correct.

---

## 3. Caveats

1. **Cross-Feature Test `test_init_con_runs_overgrowthsystem`**:
   - In `tests/test_tier3_cross_feature.py`, the test `test_init_con_runs_overgrowthsystem` fails because `init.con` does not exist yet.
   - As documented in `PROJECT.md`, `init.con` is scheduled for Milestone 3 (Level Packaging & Gameplay Pipeline). Worker M2 adhered to write boundaries by leaving `init.con` for M3.
2. **LiDAR nDMP Building Ingestion**:
   - nDMP represents normalized surface height (ground to surface). In dense urban areas, building rooftops contribute to raw surface height.
   - However, the 1,309 static buildings are largely outside the Golovec forest reserve in the agricultural/urban lowlands, and the overgrowth system does not displace buildings in Refractor 2 (static object meshes render on top of overgrowth).

---

## 4. Conclusion

- **Verdict**: **`CONFIRM`**
- `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw` is fully verified, robust, and mathematically sound:
  1. Exact byte count: $4,198,401$ bytes uint8 ($2049 \times 2049$).
  2. Value range: $[0, 255]$ with all 256 discrete levels populated and zero sentinel leakage.
  3. Spatial fidelity: Golovec ridge mean density is $87.52$ ($> 50$ requirement), while lowlands and river floor are predominantly clear ($> 83\%$ zeros).
  4. Orientation alignment: Verified to match real terrain peaks and orientation in `Heightmap.raw` with global maximal correlation ($r = +0.5233$).
- The Milestone 2 Overgrowth deliverables are fully approved to advance to Milestone 3 packaging.

---

## 5. Verification Method

To independently reproduce all empirical findings:

1. **Verify File Size & SHA256**:
   ```bash
   python3 -c "
   import os, hashlib
   p = '/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw'
   assert os.path.getsize(p) == 4198401
   h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
   assert h == 'e800f8fa09a0c1c99c58272fb82dde1ef7c5ccb33ebab3ab7c825c57f54ff209'
   print('Byte count & SHA256 verified!')
   "
   ```

2. **Verify 8-Symmetry Orientation & Ridge Density**:
   ```bash
   python3 -c "
   import numpy as np
   raw = np.fromfile('/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw', dtype=np.uint8).reshape((2049, 2049))
   hmap = np.fromfile('/home/ator/BF2/Heightmap.raw', dtype='<u2').reshape((2049, 2049)).astype(float) * 0.01
   r_win = raw[1650:1750, 974:1074].mean()
   corr = np.corrcoef(hmap[::4, ::4].ravel(), raw[::4, ::4].ravel())[0, 1]
   print(f'Golovec ridge window mean: {r_win:.2f} (Required > 50)')
   print(f'Elevation correlation: {corr:.4f}')
   assert r_win > 50.0
   assert corr > 0.50
   "
   ```

3. **Execute Tier 1 & Tier 2 Overgrowth Test Suites**:
   ```bash
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier1_feature_coverage.py -k overgrowth
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier2_boundary_corner.py -k overgrowth
   ```
