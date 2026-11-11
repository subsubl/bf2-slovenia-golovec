# Project: Slovenia (Golovec / SE Ljubljana) AAA BF2 Level Package

## Architecture
The Battlefield 2 level package provides a complete, playable 4096m x 4096m terrain centered on Golovec, Slovenia.
The system consists of three implementation pipelines feeding into the level package directory `levels/slovenia_golovec/`, verified by an independent opaque-box E2E testing suite.

### Module Boundaries & Data Flow
1. **Geospatial & Coordinate System Core**:
   - Origin $(0, 0, 0)$: D96TM [468498 E, 99466 N], WGS84 [46.034276 N, 14.592945 E].
   - Focal Point $(0, 1365)$: D96TM [468498 E, 100831 N], WGS84 [46.046559 N, 14.592945 E], ground elevation ~273.39m.
   - Bounding Box: Cartesian $X \in [-2048, 2048]$, $Z \in [-2048, 2048]$.
   - Heightmap: `Heightmap.raw` (2049x2049 uint16, 2.0m spacing, scale 0.01, zero header). Bilinear interpolation for elevation $Y$.
2. **OSM Static Objects Pipeline (M1) - [DONE]**:
   - Queries OpenStreetMap 0.6 API across 4 spatial quadrants for the 4096m x 4096m bounding box.
   - Extracts building footprints, computes centroids $(C_X, C_Z)$, samples ground elevation $C_Y$, computes principal yaw heading.
   - Maps building attributes to BF2 vanilla European urban/rural static meshes (`eu_building...`, `me_house_01`-`08`, `barn_01`, `farmhouse`, `wooden_shed`).
   - Generates valid `StaticObjects.con` (1,309 static objects). Gate Passed.
3. **LiDAR Canopy & Overgrowth Pipeline (M2) - [IN_PROGRESS]**:
   - Downloads 25 nDMP GeoTIFFs (2000x2000 0.5m Int16) referenced in `tiles_manifest.json` using rate-limited sequential requests (1.2s delay to prevent HTTP 429).
   - Resamples canopy heights to terrain grid ($2049 \times 2049$), generates density mask `Overgrowth/Overgrowth.raw` ($4,198,401$ bytes uint8).
   - Generates `OvergrowthSystem.con` configuring temperate forest foliage types (`fir_mixed02`, `birch_green_1`), spacing, and density channels.
4. **Level Packaging & Gameplay Pipeline (M3) - [PLANNED]**:
   - Creates `levels/slovenia_golovec/` structure.
   - Assembles `init.con`, `Terrain.con`, `Heightdata.con`, `Sky.con`, `Water.con`, `StaticObjects.con`, `OvergrowthSystem.con`, `Overgrowth/Overgrowth.raw`.
   - Generates `GameplayObjects.con` configured for Conquest Head-On (EU vs MEC): 3 balanced Control Points (EU Base CP 1, contested Golovec Pass CP 2 at $(0, 1365)$, MEC Base CP 3), paired Spawn Points (+1.25m elevation offset), and Combat Area boundary polygon with counter-clockwise winding.
5. **E2E Testing Track (Parallel) - [DONE]**:
   - Independent verification suite covering Tiers 1-4 (88 tests) published in `TEST_READY.md`.
   - Automated parser and validator for all `.con` files, syntax rules, coordinate bounds $[-2048, 2048]$, height grounding, and gameplay structures.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Coordinate Transformation | EPSG:4326 / EPSG:3794 to BF2 Cartesian $X, Z$ with Origin [468498, 99466] | M1 (DONE) | Survey 3 |
| 2 | Heightmap Elevation Sampling | Bilinear sampling from 2049x2049 uint16 `Heightmap.raw` with scale 0.01 | M1 (DONE) | Survey 1 & 3 |
| 3 | OSM Footprint Extraction | 4-quadrant OSM 0.6 API extraction for 4096m x 4096m Golovec bbox | M1 (DONE) | Survey 3 |
| 4 | Building Centroid & Yaw | Calculation of polygon centroid and longest-edge yaw orientation | M1 (DONE) | Survey 3 |
| 5 | Vanilla Static Mesh Mapping | Classification of OSM footprints to BF2 vanilla European static meshes | M1 (DONE) | Survey 2 & 3 |
| 6 | StaticObjects.con Generation | Generation of syntactically valid `StaticObjects.con` within $[-2048, 2048]$ | M1 (DONE) | Survey 2 |
| 7 | LiDAR Canopy Download | Rate-limited sequential download of 25 nDMP GeoTIFFs (preventing HTTP 429) | M2 (DONE) | Survey 1 & 3 |
| 8 | Canopy Resampling & Mosaicking | Resampling 0.5m canopy heights to 2049x2049 over level bounds | M2 (DONE) | Survey 1 & 3 |
| 9 | Overgrowth Density Raw | Generation of 2049x2049 uint8 `Overgrowth.raw` (4,198,401 bytes) | M2 (DONE) | Survey 2 & 3 |
| 10 | OvergrowthSystem.con Config | Configuration of temperate forest foliage types, materials, and spacing | M2 (DONE) | Survey 2 |
| 11 | Level Directory Packaging | Creation of `levels/slovenia_golovec/` and subdirectories | M3 (DONE) | Survey 1 & 2 |
| 12 | Environment & Physics Config | Configuration of `Sky.con`, `Water.con`, `Terrain.con`, `Heightdata.con` | M3 (DONE) | Survey 1 & 2 |
| 13 | Master init.con Conductor | Standard BF2 `init.con` executing all component configuration scripts | M3 (DONE) | Survey 2 |
| 14 | Conquest Head-On Control Points | 3 balanced CPs (EU Base, Golovec Pass at focal point, MEC Base) | M3 (DONE) | Survey 2 |
| 15 | Spawn Points Grounding | Player spawn points linked to CPs with +1.25m elevation offset | M3 (DONE) | Survey 2 |
| 16 | Counter-Clockwise Combat Area | Boundary polygon with positive signed area preventing desertion bug | M3 (DONE) | Survey 2 |
| 17 | E2E Con Syntax Verification | Automated test verifying line-based syntax, block structure, and case | E2E (DONE) | Survey 2 |
| 18 | E2E Coordinate Bounds Verification | Automated test checking all object positions fall in $[-2048, 2048]$ | E2E (DONE) | Survey 2 & 3 |
| 19 | E2E Height Grounding Verification | Automated test validating building elevation against heightmap | E2E (DONE) | Survey 3 |
| 20 | E2E Package Completeness Check | Automated test verifying all mandatory level files exist and are valid | E2E (DONE) | Survey 1 & 2 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Requirement-driven test suite (Tiers 1-4) published via `TEST_READY.md` | none | DONE |
| M1 | OSM Buildings & StaticObjects.con | Footprint extraction, elevation sampling, vanilla mesh mapping, `StaticObjects.con` | none | DONE |
| M2 | LiDAR Canopy & OvergrowthSystem | Throttled download, canopy resampling, density mask `Overgrowth.raw`, `OvergrowthSystem.con` | none | DONE |
| M3 | Level Package Assembly & Gameplay | Directory structure, environment `.con` files, Conquest Head-On `GameplayObjects.con` | M1, M2 | DONE |
| M4 | Final Milestone: E2E Verification & Hardening | Pass 100% of E2E tests (Tiers 1-4) followed by Adversarial Hardening (Tier 5) | E2E, M3 | DONE |

---

## Interface Contracts

### M1 ↔ M3: Static Objects Contract [SATISFIED]
- **Output Artifact**: `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con` (166,753 bytes, 1,309 static objects).
- Verified: All coordinates $X, Z \in [-2048.0, 2048.0]$, $Y \ge 270.0\text{ m}$, max deviation from heightmap $0.0006\text{ m}$, min clearance $30.004\text{ m}$, zero collisions.

### M2 ↔ M3: Overgrowth Contract [SATISFIED]
- **Output Artifacts**:
  - `/home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con` [DONE - 312 lines, material temperate_forest 1, 7 vanilla species]
  - `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw` [DONE - exactly 4,198,401 bytes uint8, row 0 South to row 2048 North]
- **Format**:
  - `Overgrowth.raw`: Exactly $2049 \times 2049 = 4,198,401$ bytes uint8 binary mask, 0 header.
  - `OvergrowthSystem.con`: Defines material `temperate_forest`, foliage types (`fir`, `birch`), densities, and radii.

### M3 ↔ E2E: Level Package Contract [SATISFIED]
- **Level Directory**: `/home/ator/BF2/levels/slovenia_golovec/`
- **Mandatory Files**:
  1. `init.con` [DONE]
  2. `Heightdata.con` [DONE]
  3. `Terrain.con` [DONE]
  4. `Sky.con` [DONE]
  5. `Water.con` [DONE]
  6. `StaticObjects.con` [DONE - 1,309 objects]
  7. `OvergrowthSystem.con` [DONE - 7 species]
  8. `GameplayObjects.con` [DONE - Conquest Head-On EU vs MEC]
  9. `Overgrowth/Overgrowth.raw` [DONE - 4,198,401 bytes]

---

## Code Layout
```text
/home/ator/BF2/
├── Heightmap.raw                              # Base 2049x2049 uint16 terrain elevation
├── ColorMap.dds                               # 4096x4096 DXT1 terrain texture
├── tiles_manifest.json                        # 25 LiDAR tile manifest
├── dmr_raw/                                   # 25 local DMR LAZ point clouds
├── pof_1m/                                    # 25 local POF GeoTIFFs
├── scripts/                                   # Implementation & extraction scripts
│   ├── extract_osm_buildings.py               # M1 extraction & StaticObjects.con generator [DONE]
│   ├── process_lidar_canopy.py                # M2 download & overgrowth mask generator
│   └── assemble_level_package.py              # M3 package assembly & gameplay generator
├── tests/                                     # E2E test suite [DONE]
│   ├── con_parser.py                          # Refractor 2 parser & math oracle
│   ├── test_tier1_feature_coverage.py         # Tier 1 tests
│   ├── test_tier2_boundary_corner.py          # Tier 2 tests
│   ├── test_tier3_cross_feature.py            # Tier 3 tests
│   ├── test_tier4_real_world_gameplay.py      # Tier 4 tests
│   └── verify_bf2_level.py                    # Master E2E test harness
├── levels/
│   └── slovenia_golovec/                      # Final assembled BF2 level package
│       ├── init.con
│       ├── Heightdata.con
│       ├── Terrain.con
│       ├── Sky.con
│       ├── Water.con
│       ├── StaticObjects.con                  # [DONE - 1,309 objects]
│       ├── OvergrowthSystem.con
│       ├── GameplayObjects.con
│       └── Overgrowth/
│           └── Overgrowth.raw
└── .agents/teamwork/                          # Coordination & metadata
```
