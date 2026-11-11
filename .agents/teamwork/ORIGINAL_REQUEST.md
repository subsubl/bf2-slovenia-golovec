# Original User Request

## Initial Request — 2026-11-11T00:36:28Z

Complete the Battlefield 2 level package for the Slovenia (Golovec / SE Ljubljana) map to create a fully structured, playable AAA BF2 level.

Working directory: /home/ator/BF2
Integrity mode: development

## Requirements

### R1. OpenStreetMap Building Extraction & StaticObjects.con
Download and extract OpenStreetMap building footprints for the 4096m x 4096m bounding box centered on Golovec (origin (0, 0, 0) Cartesian coordinate mapped to D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E]). Map the footprints to standard Battlefield 2 vanilla static building meshes (European urban/rural building models), sample ground elevation Y from `Heightmap.raw` (2049x2049 uint16 little-endian, 2.0m grid spacing, heightScale 0.01) for each building position, and generate a valid `StaticObjects.con`.

### R2. LiDAR Canopy Processing & OvergrowthSystem.con
Download and process the LiDAR canopy height GeoTIFFs (nDMP) referenced in `tiles_manifest.json` across Golovec. Generate vegetation and forest density channel masks matching the terrain dimensions, and create `OvergrowthSystem.con` configuring overgrowth mesh definitions and density channels for temperate forest coverage.

### R3. BF2 Level Package Assembly & Gameplay Configuration
Assemble the complete level directory structure under `levels/<level_name>/` incorporating all required Battlefield 2 configuration files: `init.con`, `Sky.con`, `Water.con`, `Terrain.con`, `Heightdata.con`, `StaticObjects.con`, and `OvergrowthSystem.con`. Configure `GameplayObjects.con` for Standard Conquest Head-On (US vs MEC or EU vs MEC) with balanced Control Points, Spawn Points, and Combat Area boundaries centered on the Golovec focal point battleground (46.046559 N, 14.592945 E).

## Verification Resources
Automated test scripts to parse generated `.con` configuration files, verify BF2 syntax and mandatory block structure, and validate coordinate boundaries against the map bounds.

## Acceptance Criteria

### Static Objects
- [ ] OpenStreetMap building footprints within the 4096m x 4096m bounding box are extracted and mapped to standard BF2 vanilla static meshes in `StaticObjects.con`.
- [ ] All static object coordinates fall within the [-2048, 2048] Cartesian coordinate limits.
- [ ] Ground elevation Y for each building is correctly sampled from `Heightmap.raw` at the corresponding terrain coordinate.

### Overgrowth System
- [ ] LiDAR canopy GeoTIFFs (nDMP) from `tiles_manifest.json` are processed into valid density channel masks matching the terrain dimensions.
- [ ] `OvergrowthSystem.con` defines valid overgrowth mesh types and assigns the generated density channels for forest coverage across Golovec.

### Level Package Structure & Gameplay
- [ ] Complete level directory exists under `levels/<level_name>/` containing `init.con`, `Sky.con`, `Water.con`, `Terrain.con`, `Heightdata.con`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
- [ ] `GameplayObjects.con` provides a playable Standard Conquest Head-On setup (US vs MEC or EU vs MEC) with Control Points, Spawn Points, and Combat Area centered on the Golovec focal point (46.046559 N, 14.592945 E).
- [ ] Automated verification script validates that all generated `.con` files have correct BF2 syntax, no broken references, and all coordinates within valid map bounds.
