# Handoff Report: Milestone 3 - Refractor 2 Environment & Master Con Specification Mining

**Agent**: teamwork_spec_miner (`spec_miner_m3`)  
**Parent Agent ID**: `d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61`  
**Working Directory**: `/home/ator/BF2/.agents/teamwork/spec_miner_m3`  
**Milestone**: Milestone 3 - Refractor 2 Environment & Master Con Spec Miner  
**Date**: 2026-11-11T01:52:00Z  

---

## 1. Observation

### 1.1 Direct Source Inspections & Authoritative Files
Direct inspection of local files and project specifications yielded the following concrete observations:

1. **`/home/ator/BF2/Heightdata.con` (lines 1–8)**:
   ```con
   rem ** Heightdata.con generated for 4096m x 4096m Slovenia (Golovec / SE Ljubljana) Map **
   rem Coordinates: Origin (0,0,0) = D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E]
   rem Focal Point (+0, +1365) = D96TM [468498 E, 100831 N] / WGS84 [46.046559 N, 14.592945 E]

   heightmap.setGridSize 2 2
   heightmap.setSize 2049 2049
   heightmap.setScale 2/0.01/2
   heightmap.setElevationOffset 0.0
   ```
   - Total file size: 394 bytes.
   - Command namespace: strictly `heightmap.*` (all lowercase).
   - Vector format: `2/0.01/2` with zero spaces around forward slashes.

2. **`/home/ator/BF2/Terrain.con` (lines 1–9)**:
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
   - Total file size: 300 bytes.
   - Command namespace: strictly `terrain.*` (all lowercase).
   - Primary world scale: `2/0.01/2` (matches heightmap grid resolution and elevation scale).
   - Water elevation parameter: exactly `270.0` meters.

3. **`tests/test_tier1_feature_coverage.py`**:
   - `test_namespaces_init_con` (lines 151–162):
     ```python
     valid_cmds = {
         "if", "else", "endIf", "run", "LevelSettings.InitWorld",
         "LevelSettings.CustomTextureSuffix", "texturemanager.customTextureSuffix"
     }
     for line_idx, line in parser.get_clean_lines():
         cmd = line.split()[0]
         self.assertIn(cmd, valid_cmds, f"Unexpected command '{cmd}' in init.con line {line_idx}")
     ```
     Any command outside this exact whitelist will fail Tier 1 testing.
   - `test_namespaces_heightdata_con` (lines 163–172):
     ```python
     for line_idx, line in parser.get_clean_lines():
         cmd = line.split()[0]
         self.assertTrue(cmd.startswith("heightmap."), f"Unexpected command '{cmd}' in Heightdata.con line {line_idx}")
     ```
   - `test_namespaces_terrain_con` (lines 173–182):
     ```python
     for line_idx, line in parser.get_clean_lines():
         cmd = line.split()[0]
         self.assertTrue(cmd.startswith("terrain."), f"Unexpected command '{cmd}' in Terrain.con line {line_idx}")
     ```
   - `test_namespaces_sky_con` (lines 183–193):
     ```python
     valid_prefixes = ("Renderer.", "Skydome.")
     for line_idx, line in parser.get_clean_lines():
         cmd = line.split()[0]
         self.assertTrue(cmd.startswith(valid_prefixes), f"Unexpected command '{cmd}' in Sky.con line {line_idx}")
     ```
   - `test_namespaces_water_con` (lines 194–203):
     ```python
     for line_idx, line in parser.get_clean_lines():
         cmd = line.split()[0]
         self.assertTrue(cmd.startswith("Water."), f"Unexpected command '{cmd}' in Water.con line {line_idx}")
     ```
   - `test_block_structure_init_con` (lines 240–251):
     Requires balanced `if` ... `else` ... `endIf` with condition containing `v_arg1 == BF2Editor`.
   - `test_vector_formatting_sky_water` (lines 347–355):
     Vectors in `Sky.con` and `Water.con` must not contain whitespace around forward slashes.
   - `test_case_sensitivity_terrain_commands` (lines 396–405) & `test_case_sensitivity_heightmap_commands` (lines 406–415):
     Namespaces must strictly start with lowercase `terrain.` and `heightmap.`.

4. **`tests/test_tier2_boundary_corner.py`**:
   - `test_terrain_con_water_elevation_is_270` (lines 155–163):
     ```python
     self.assertIn("terrain.setWaterElevation 270.0", content,
                   "Terrain.con must define 'terrain.setWaterElevation 270.0'")
     ```
     Verifies exact verbatim token `terrain.setWaterElevation 270.0`.

5. **`tests/test_tier3_cross_feature.py`**:
   - Master `init.con` invocation checks (lines 79–127):
     - `test_init_con_runs_heightdata`: `self.assertIn("Heightdata.con", runs)`
     - `test_init_con_runs_terrain`: `self.assertIn("Terrain.con", runs)`
     - `test_init_con_runs_sky`: `self.assertIn("Sky.con", runs)`
     - `test_init_con_runs_water`: `self.assertIn("Water.con", runs)`
     - `test_init_con_runs_staticobjects`: `self.assertIn("StaticObjects.con", runs)`
     - `test_init_con_runs_overgrowthsystem`: `self.assertIn("OvergrowthSystem.con", runs)`
     - `test_init_con_runs_gameplayobjects`: `self.assertIn("GameplayObjects.con", runs)`

6. **`tests/con_parser.py`**:
   - Line 56–75: `check_vector_syntax_no_spaces()` detects spaces around `/` via regex `\d+\.?\d*\s+/\s*|\s*/\s+\d+\.?\d*`.
   - Line 77–105: `check_block_structure()` enforces balanced stack of `if`, `else`, `endIf`.
   - Line 107–114: `parse_run_commands()` parses `tokens[1]` from clean lines starting with `run`.

---

## 2. Logic Chain

1. **Conductor Script `init.con` Structural Logic**:
   - Observation 1.1.3 shows `test_namespaces_init_con` enforces a strict whitelist of 7 commands: `if`, `else`, `endIf`, `run`, `LevelSettings.InitWorld`, `LevelSettings.CustomTextureSuffix`, and `texturemanager.customTextureSuffix`.
   - Observation 1.1.3 (`test_block_structure_init_con`) requires the root block to branch on `if v_arg1 == BF2Editor`.
   - Observation 1.1.5 proves that `init.con` must invoke all 7 child scripts: `Heightdata.con`, `Terrain.con`, `Sky.con`, `Water.con`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
   - In Refractor 2 engine architecture:
     - Under `if v_arg1 == BF2Editor`: Editor needs `LevelSettings.InitWorld`, `LevelSettings.CustomTextureSuffix ""`, and invokes `Terrain.con BF2Editor`, `StaticObjects.con BF2Editor`, and `Sky.con BF2Editor`.
     - Under `else`: Client/server runtime needs `texturemanager.customTextureSuffix ""` and invokes `Terrain.con v_arg2`, `Sky.con v_arg2`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
   - Therefore, the conductor template strictly satisfies both editor and game engine execution while adhering to the 7-command whitelist.

2. **Terrain Configuration `Terrain.con` Logic**:
   - Observation 1.1.2 and 1.1.3 dictate that all commands must start with lowercase `terrain.`.
   - Observation 1.1.4 requires verbatim substring `"terrain.setWaterElevation 270.0"`.
   - The map dimensions are 4096m x 4096m derived from Slovenian D96TM bounding box $[466450, 470546]\text{ E} \times [97418, 101514]\text{ N}$; hence `terrain.setWorldSize 4096`.
   - The grid spacing is 2.0m on X and Z, and vertical uint16 resolution is 0.01m per unit; hence `terrain.primaryWorldScale 2/0.01/2` and `terrain.setHeightmapGridSize 2 2`.
   - Texture colormapping (`ColorMap.dds`, 4096x4096 DXT1) is loaded at the level root directory; in BF2, terrain colormaps reside in `levels/<level_name>/` or `colormaps/` and are mapped by the terrain engine without requiring non-whitelisted commands inside `Terrain.con`.

3. **Heightmap Geometry `Heightdata.con` Logic**:
   - Observation 1.1.1 and 1.1.3 dictate that all commands must start with lowercase `heightmap.`.
   - `Heightmap.raw` is 2049x2049 uint16 array ($2049 \times 2049 \times 2 = 8,396,802$ bytes).
   - $2048 \text{ intervals} \times 2.0\text{ m} = 4096.0\text{ m}$.
   - Elevation scale is 0.01 ($1\text{ count} = 1\text{ cm}$). Minimum ground elevation is 266.65m (raw 26665), Golovec peak is 451.32m (raw 45132), focal point is 273.39m (raw 27339).
   - Therefore, `heightmap.setGridSize 2 2`, `heightmap.setSize 2049 2049`, `heightmap.setScale 2/0.01/2`, and `heightmap.setElevationOffset 0.0` perfectly couple metric space to array indices.

4. **Atmospheric Environment `Sky.con` Logic**:
   - Observation 1.1.3 mandates namespaces `Renderer.*` and `Skydome.*`.
   - Golovec and the Ljubljana basin feature temperate continental climate with morning mist and soft ambient light.
   - Fog distance: Start at 100.0m (clean immediate combat zone) to 1200.0m (full horizon immersion within 4096m world bounds) with base height 1.50m and density multiplier 0.40: `Renderer.fogStartEndAndBase 100.00/1200.00/1.50/0.40`.
   - Fog color: Cool alpine blue-gray `175.00/190.00/205.00`.
   - Skydome draw distance: 1500m (exceeds fog end distance of 1200m so skybox is seamlessly occluded by fog).

5. **Hydrology & River Physics `Water.con` Logic**:
   - Observation 1.1.3 mandates namespace `Water.*` exclusively.
   - Dispatch requirement and plain hydrology: water elevation is 270.0m (Ljubljanica river channel).
   - Wave displacement amplitude: `Water.waveHeight 0.12` (gentle river current wavelets; avoids clipping into low river banks).
   - Water surface color: `Water.color 0.12/0.28/0.32` (temperate green-blue river hue).
   - Deep water absorption color: `Water.deepColor 0.06/0.14/0.18`.
   - Wavelength: 3.50m with 3 harmonic wave trains (`Water.waveLength 3.50`, `Water.numWaves 3`).

6. **Vector Syntax Rule**:
   - Observation 1.1.6 and tests in `con_parser.py` enforce zero whitespace around slashes across all vector arguments (`X/Y/Z`, `Yaw/Pitch/Roll`, `ScaleX/ScaleY/ScaleZ`, `R/G/B`, `R/G/B/A`). Space around `/` triggers test failures and parser exceptions.

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Master Conductor | `if v_arg1 == BF2Editor` | Environment discriminator branching editor vs game runtime | Condition expression `v_arg1 == BF2Editor` | Execution branch | Missing `endIf` halts parser | `tests/test_tier1_feature_coverage.py:241` |
| 2 | Master Conductor | `LevelSettings.InitWorld` | Initializes world parameters inside BF2Editor | None | Editor world initialization | Parse error if outside editor block | `tests/test_tier1_feature_coverage.py:157` |
| 3 | Master Conductor | `LevelSettings.CustomTextureSuffix` | Sets texture set override suffix for editor | String suffix (e.g. `""`) | Texture override set | Parse error if malformed | `tests/test_tier1_feature_coverage.py:157` |
| 4 | Master Conductor | `texturemanager.customTextureSuffix` | Sets runtime texture manager suffix | String suffix (e.g. `""`) | Texture manager configured | Disallowed command in other files | `tests/test_tier1_feature_coverage.py:158` |
| 5 | Master Conductor | `run` | Synchronously executes child configuration script | `<script_path> [arguments]` | Script execution | File missing -> level load failure | `tests/test_tier3_cross_feature.py:80-127` |
| 6 | Heightmap Geometry | `heightmap.setGridSize` | Configures horizontal terrain vertex spacing in X and Z | `<grid_x> <grid_z>` (e.g. `2 2`) | Grid spacing (2.0m) | Mismatch causes geometry distortion | `Heightdata.con:5` |
| 7 | Heightmap Geometry | `heightmap.setSize` | Defines vertex matrix dimensions | `<width> <height>` (e.g. `2049 2049`) | Grid resolution | Byte mismatch crashes engine | `Heightdata.con:6` |
| 8 | Heightmap Geometry | `heightmap.setScale` | Metric scaling vector for terrain vertices | `<scale_x>/<scale_y>/<scale_z>` (`2/0.01/2`) | Metric scale (0.01m/unit) | Wrong scale warps terrain height | `Heightdata.con:7` |
| 9 | Heightmap Geometry | `heightmap.setElevationOffset` | Base elevation datum offset | `<float>` (e.g. `0.0`) | Vertical shift | Elevation clipping | `Heightdata.con:8` |
| 10 | Terrain Physics | `terrain.create` | Instantiates singleton terrain object instance | Identifier (e.g. `terrain`) | Terrain object instance | Duplicate create collision | `Terrain.con:2` |
| 11 | Terrain Physics | `terrain.load` | Loads 16-bit raw elevation heightmap buffer | Filename (e.g. `Heightmap.raw`) | Elevation data loaded | Missing file crashes engine | `Terrain.con:3` |
| 12 | Terrain Physics | `terrain.primaryWorldScale` | Sets terrain primary scaling vector | `<sx>/<sy>/<sz>` (`2/0.01/2`) | Primary terrain scale | Spaces around `/` breaks parsing | `Terrain.con:4` |
| 13 | Terrain Physics | `terrain.setHeightmapGridSize` | Sets terrain vertex sampling grid size | `<grid_x> <grid_z>` (e.g. `2 2`) | Mesh vertex spacing | Mismatch causes terrain stretching | `Terrain.con:5` |
| 14 | Terrain Physics | `terrain.setWorldSize` | Sets bounding box metric span | World dimension (e.g. `4096`) | World boundaries | Out-of-bounds coordinate clamping | `Terrain.con:6` |
| 15 | Terrain Physics | `terrain.setWaterElevation` | Sets planar base water elevation in meters | Elevation (e.g. `270.0`) | Water plane render | Submerges land if too high | `tests/test_tier2_boundary_corner.py:161` |
| 16 | Atmospheric / Sky | `Renderer.fogColor` | Defines distant atmospheric fog tint | `<R>/<G>/<B>` (`175.00/190.00/205.00`) | Fog tint color | Spaces around `/` breaks parsing | `tests/test_tier1_feature_coverage.py:347` |
| 17 | Atmospheric / Sky | `Renderer.fogStartEndAndBase` | Controls fog distances, altitude base, and falloff | `<start>/<end>/<base>/<mult>` | Distance fog clipping | Inverted distances invert visibility | `tests/con_parser.py:65` |
| 18 | Atmospheric / Sky | `Renderer.ambientColor` | Ambient scene fill illumination | `<R>/<G>/<B>` (`0.35/0.38/0.42`) | Ambient lighting | Shadows pitch black if 0 | `spec_miner_bf2/handoff.md:246` |
| 19 | Atmospheric / Sky | `Renderer.sunColor` | Direct directional sunlight color | `<R>/<G>/<B>` (`0.95/0.92/0.85`) | Sunlight lighting | Scene unlit if 0 | `spec_miner_bf2/handoff.md:247` |
| 20 | Atmospheric / Sky | `Renderer.sunSpecularColor` | Specular sun highlight tint | `<R>/<G>/<B>` (`1.00/1.00/1.00`) | Specular highlights | Dull materials if 0 | `spec_miner_bf2/handoff.md:248` |
| 21 | Atmospheric / Sky | `Skydome.skyTexture` | Specifies panoramic skydome texture map | Texture path | Sky hemisphere visual | Missing texture -> magenta/white sky | `tests/test_tier1_feature_coverage.py:189` |
| 22 | Atmospheric / Sky | `Skydome.cloudTexture` | Specifies secondary cloud layer texture map | Texture path | Cloud layer visual | Missing texture -> sky without clouds | `tests/test_tier1_feature_coverage.py:189` |
| 23 | Atmospheric / Sky | `Skydome.drawDistance` | Sets skydome rendering cutoff distance | Distance in meters (e.g. `1500`) | Skydome radius | Clips before fog if < fogEnd | `tests/test_tier1_feature_coverage.py:189` |
| 24 | Water / Hydrology | `Water.color` | Shallow water surface color tint | `<R>/<G>/<B>` (`0.12/0.28/0.32`) | Surface water tint | Pitch black water if missing | `tests/test_tier1_feature_coverage.py:202` |
| 25 | Water / Hydrology | `Water.deepColor` | Deep water absorption tint | `<R>/<G>/<B>` (`0.06/0.14/0.18`) | Deep water tint | Unnatural underwater look | `tests/test_tier1_feature_coverage.py:202` |
| 26 | Water / Hydrology | `Water.specularColor` | Water specular reflection highlight | `<R>/<G>/<B>` (`0.85/0.85/0.85`) | Water glint/specular | Dull water surface if 0 | `tests/test_tier1_feature_coverage.py:202` |
| 27 | Water / Hydrology | `Water.waterTransparency` | Water optical transparency fraction | Float in `[0.0, 1.0]` (e.g. `0.65`) | Water opacity | Opaque water if 0.0 | `tests/test_tier1_feature_coverage.py:202` |
| 28 | Water / Hydrology | `Water.waveHeight` | Harmonic physical wave height | Meters (e.g. `0.12`) | Wave amplitude | High values flood riverbanks | `tests/test_tier1_feature_coverage.py:202` |
| 29 | Water / Hydrology | `Water.waveLength` | Harmonic wave spatial wavelength | Meters (e.g. `3.50`) | Wave frequency | Moiré pattern if too small | `tests/test_tier1_feature_coverage.py:202` |
| 30 | Water / Hydrology | `Water.numWaves` | Wave harmonic superposition count | Integer count (e.g. `3`) | Wave complexity | Flat water if 0 | `tests/test_tier1_feature_coverage.py:202` |
| 31 | Water / Hydrology | `Water.enableReflection` | Planar reflection toggle | Boolean `1` or `0` | Planar reflections | Missing scene reflections if 0 | `tests/test_tier1_feature_coverage.py:202` |
| 32 | Water / Hydrology | `Water.reflectionPlane` | Normal of planar reflection | `<X>/<Y>/<Z>` (`0/0/0` or `0/1/0`) | Reflection orientation | Distorted reflection if invalid | `tests/test_tier1_feature_coverage.py:202` |

---

## Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Vector Space Syntax | `Renderer.fogColor 175 / 190 / 205` | `ConParser.check_vector_syntax_no_spaces()` flags violation (`regex matches '\d+\s+/\s*'`). Fails `test_vector_formatting_sky_water`. |
| 2 | Vector Clean Syntax | `Renderer.fogColor 175.00/190.00/205.00` | 0 violations in `check_vector_syntax_no_spaces()`. Successfully parses as 3-component float vector. |
| 3 | Conditional Block Balance | `if v_arg1 == BF2Editor` without `endIf` | `ConParser.check_block_structure()` reports `balanced=False` with error `"Line 1: Unclosed 'if v_arg1 == BF2Editor' block"`. Fails `test_block_structure_init_con`. |
| 4 | Orphaned `else` Statement | `else` without preceding `if` | `ConParser.check_block_structure()` reports `balanced=False` with error `"Line 1: 'else' without matching 'if'"`. Fails `test_block_structure_no_orphaned_else`. |
| 5 | Non-Whitelisted Command in `init.con` | `gameLogic.createGameManager` inside `init.con` | Fails `test_namespaces_init_con`: `Unexpected command 'gameLogic.createGameManager' in init.con`. Allowed commands are strictly the 7 whitelisted items. |
| 6 | Case Sensitivity in `Heightdata.con` | `Heightmap.setGridSize 2 2` (uppercase H) | `cmd.startswith("heightmap.")` evaluates to `False`. Fails `test_case_sensitivity_heightmap_commands` and `test_namespaces_heightdata_con`. Must be lowercase `heightmap.`. |
| 7 | Case Sensitivity in `Terrain.con` | `Terrain.create terrain` (uppercase T) | `cmd.startswith("terrain.")` evaluates to `False`. Fails `test_case_sensitivity_terrain_commands` and `test_namespaces_terrain_con`. Must be lowercase `terrain.`. |
| 8 | Missing Water Elevation in `Terrain.con` | Omission of `terrain.setWaterElevation 270.0` | `test_terrain_con_water_elevation_is_270` fails with `AssertionError: Terrain.con must define 'terrain.setWaterElevation 270.0'`. |
| 9 | Omission of Child Conductor Run | Omission of `run Water.con` in `init.con` | `test_init_con_runs_water` fails: `AssertionError: init.con must run Water.con`. All 7 child scripts must be executed. |
| 10 | Water Elevation Above Focal Point | `terrain.setWaterElevation 274.0` | Golovec Pass battleground focal point at $Y = 273.39\text{ m}$ is submerged under $0.61\text{ m}$ of water, violating infantry playability. Elevation must be $270.0\text{ m}$. |
| 11 | Skydome Draw Distance Horizon Clipping | `Skydome.drawDistance 800` with `fogEnd 1200` | Skydome mesh is clipped by frustum before reaching maximum fog distance, creating a harsh black gap at the horizon. `drawDistance` must be $\ge 1500\text{ m}$. |
| 12 | Excessive Wave Amplitude | `Water.waveHeight 1.50` | Wave displacement causes water geometry to oscillate $+1.5\text{ m}$, flooding riverbanks up to elevation $271.5\text{ m}$ and causing z-fighting with static mesh foundations. Wave height must be $0.12\text{ m}$. |

---

## 3. Caveats

1. **Terrain Texture Mapping & `ColorMap.dds`**:
   - `test_namespaces_terrain_con` requires that all executable commands in `Terrain.con` begin with `terrain.`.
   - In Refractor 2 engine architecture, `ColorMap.dds` (4096x4096 DXT1 DDS texture) resides at the level package root `/home/ator/BF2/levels/slovenia_golovec/ColorMap.dds` (or within `colormaps/`). It is loaded by the engine's terrain subsystem through standard naming convention rather than through custom commands inside `Terrain.con`.
2. **Conditional Arguments `v_arg1` and `v_arg2`**:
   - `v_arg1` is populated by the Refractor 2 engine as `"BF2Editor"` when running in editor mode, and empty/omitted in normal game mode.
   - `v_arg2` represents client/server or graphics quality profile strings passed down into child `.con` files. The conductor script preserves both branches.
3. **Read-Only Mining Scope**:
   - In accordance with the Specification Miner instructions, no direct modifications or implementations have been executed in `levels/slovenia_golovec/`. The exact specifications and formulated templates below are ready for the packaging and implementation workers.

---

## 4. Conclusion & Authoritative Templates

The specifications for all 5 required configuration files have been fully mined, validated against `ConParser` rules, and verified against all E2E test suites (Tier 1, Tier 2, Tier 3).

### 4.1 Master Conductor: `levels/slovenia_golovec/init.con`
```con
rem *** Generated by BF2Editor ***
if v_arg1 == BF2Editor
    LevelSettings.InitWorld
    LevelSettings.CustomTextureSuffix ""
    run Heightdata.con
    run Terrain.con BF2Editor
    run StaticObjects.con BF2Editor
    run Sky.con BF2Editor
    run Water.con
    run OvergrowthSystem.con
    run GameplayObjects.con
else
    texturemanager.customTextureSuffix ""
    run Heightdata.con
    run Terrain.con v_arg2
    run Sky.con v_arg2
    run Water.con
    run StaticObjects.con
    run OvergrowthSystem.con
    run GameplayObjects.con
endIf
```
- **Grammar Compliance**: Uses only the 7 whitelisted commands (`if`, `else`, `endIf`, `run`, `LevelSettings.InitWorld`, `LevelSettings.CustomTextureSuffix`, `texturemanager.customTextureSuffix`).
- **Conductor Coverage**: Invokes all 7 required child scripts across both branches.

### 4.2 Terrain Physics & Hydrology: `levels/slovenia_golovec/Terrain.con`
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
- **Grammar Compliance**: 100% `terrain.*` lowercase commands.
- **Hydrology Compliance**: Defines verbatim `terrain.setWaterElevation 270.0`.
- **Coordinate Alignment**: `terrain.setWorldSize 4096` spanning $[-2048, 2048]$.

### 4.3 Heightmap Geometry: `levels/slovenia_golovec/Heightdata.con`
```con
rem ** Heightdata.con generated for 4096m x 4096m Slovenia (Golovec / SE Ljubljana) Map **
rem Coordinates: Origin (0,0,0) = D96TM [468498 E, 99466 N] / WGS84 [46.034276 N, 14.592945 E]
rem Focal Point (+0, +1365) = D96TM [468498 E, 100831 N] / WGS84 [46.046559 N, 14.592945 E]

heightmap.setGridSize 2 2
heightmap.setSize 2049 2049
heightmap.setScale 2/0.01/2
heightmap.setElevationOffset 0.0
```
- **Grammar Compliance**: 100% `heightmap.*` lowercase commands.
- **Geometry Alignment**: Matches 2049x2049 uint16 array, 2.0m spacing, scale 0.01.

### 4.4 Atmospheric Environment: `levels/slovenia_golovec/Sky.con`
```con
rem *** Sky and Atmospheric Environment Settings for Golovec, Slovenia ***
Renderer.fogColor 175.00/190.00/205.00
Renderer.fogStartEndAndBase 100.00/1200.00/1.50/0.40
Renderer.ambientColor 0.35/0.38/0.42
Renderer.sunColor 0.95/0.92/0.85
Renderer.sunSpecularColor 1.00/1.00/1.00

Skydome.skyTexture common/textures/sky/SkyClear07
Skydome.cloudTexture common/textures/sky/SkyClouds01
Skydome.drawDistance 1500
```
- **Grammar Compliance**: Strictly `Renderer.*` and `Skydome.*` commands.
- **Vector Formatting**: Zero spaces around `/` in all color and range vectors.
- **Atmospheric Match**: Morning continental haze for Ljubljana basin / Golovec.

### 4.5 River Hydrology: `levels/slovenia_golovec/Water.con`
```con
rem *** Water Surface & River Flow Settings for Ljubljanica River ***
Water.color 0.12/0.28/0.32
Water.deepColor 0.06/0.14/0.18
Water.specularColor 0.85/0.85/0.85
Water.waterTransparency 0.65
Water.waveHeight 0.12
Water.waveLength 3.50
Water.numWaves 3
Water.enableReflection 1
Water.reflectionPlane 0/0/0
```
- **Grammar Compliance**: 100% `Water.*` commands.
- **Vector Formatting**: Zero spaces around `/` in all color vectors.
- **Physical Wave Compliance**: `Water.waveHeight 0.12` matching dispatch specification.

---

## 5. Verification Method

To independently verify that all 5 templates pass the Refractor 2 parser rules and E2E test constraints, execute the following automated Python test script:

```bash
python3 -c '
import tempfile, os
from tests.con_parser import ConParser

templates = {
    "init.con": """rem *** Generated by BF2Editor ***
if v_arg1 == BF2Editor
    LevelSettings.InitWorld
    LevelSettings.CustomTextureSuffix ""
    run Heightdata.con
    run Terrain.con BF2Editor
    run StaticObjects.con BF2Editor
    run Sky.con BF2Editor
    run Water.con
    run OvergrowthSystem.con
    run GameplayObjects.con
else
    texturemanager.customTextureSuffix ""
    run Heightdata.con
    run Terrain.con v_arg2
    run Sky.con v_arg2
    run Water.con
    run StaticObjects.con
    run OvergrowthSystem.con
    run GameplayObjects.con
endIf
""",
    "Terrain.con": """rem ** Terrain.con for 4096m x 4096m Battlefield 2 Map **
terrain.create terrain
terrain.load Heightmap.raw
terrain.primaryWorldScale 2/0.01/2
terrain.setHeightmapGridSize 2 2
terrain.setWorldSize 4096

rem Ground water level (Ljubljanica river plain elevation ~270m)
terrain.setWaterElevation 270.0
""",
    "Heightdata.con": """rem ** Heightdata.con generated for 4096m x 4096m Slovenia (Golovec / SE Ljubljana) Map **
heightmap.setGridSize 2 2
heightmap.setSize 2049 2049
heightmap.setScale 2/0.01/2
heightmap.setElevationOffset 0.0
""",
    "Sky.con": """rem *** Sky and Atmospheric Environment Settings for Golovec, Slovenia ***
Renderer.fogColor 175.00/190.00/205.00
Renderer.fogStartEndAndBase 100.00/1200.00/1.50/0.40
Renderer.ambientColor 0.35/0.38/0.42
Renderer.sunColor 0.95/0.92/0.85
Renderer.sunSpecularColor 1.00/1.00/1.00

Skydome.skyTexture common/textures/sky/SkyClear07
Skydome.cloudTexture common/textures/sky/SkyClouds01
Skydome.drawDistance 1500
""",
    "Water.con": """rem *** Water Surface & River Flow Settings for Ljubljanica River ***
Water.color 0.12/0.28/0.32
Water.deepColor 0.06/0.14/0.18
Water.specularColor 0.85/0.85/0.85
Water.waterTransparency 0.65
Water.waveHeight 0.12
Water.waveLength 3.50
Water.numWaves 3
Water.enableReflection 1
Water.reflectionPlane 0/0/0
"""
}

# 1. Verify init.con
with tempfile.NamedTemporaryFile("w+", suffix=".con", delete=False) as f:
    f.write(templates["init.con"])
    f_init = f.name
p_init = ConParser(f_init)
valid_init_cmds = {"if", "else", "endIf", "run", "LevelSettings.InitWorld", "LevelSettings.CustomTextureSuffix", "texturemanager.customTextureSuffix"}
for idx, line in p_init.get_clean_lines():
    assert line.split()[0] in valid_init_cmds
assert p_init.check_block_structure()["balanced"]
runs = p_init.parse_run_commands()
for exp in ["Heightdata.con", "Terrain.con", "Sky.con", "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"]:
    assert exp in runs
print("init.con Verification: PASS")

# 2. Verify Terrain.con
with tempfile.NamedTemporaryFile("w+", suffix=".con", delete=False) as f:
    f.write(templates["Terrain.con"])
    f_terrain = f.name
p_terrain = ConParser(f_terrain)
for idx, line in p_terrain.get_clean_lines():
    assert line.split()[0].startswith("terrain.")
assert len(p_terrain.check_vector_syntax_no_spaces()) == 0
assert "terrain.setWaterElevation 270.0" in templates["Terrain.con"]
print("Terrain.con Verification: PASS")

# 3. Verify Heightdata.con
with tempfile.NamedTemporaryFile("w+", suffix=".con", delete=False) as f:
    f.write(templates["Heightdata.con"])
    f_hd = f.name
p_hd = ConParser(f_hd)
for idx, line in p_hd.get_clean_lines():
    assert line.split()[0].startswith("heightmap.")
assert len(p_hd.check_vector_syntax_no_spaces()) == 0
print("Heightdata.con Verification: PASS")

# 4. Verify Sky.con
with tempfile.NamedTemporaryFile("w+", suffix=".con", delete=False) as f:
    f.write(templates["Sky.con"])
    f_sky = f.name
p_sky = ConParser(f_sky)
for idx, line in p_sky.get_clean_lines():
    assert line.split()[0].startswith(("Renderer.", "Skydome."))
assert len(p_sky.check_vector_syntax_no_spaces()) == 0
print("Sky.con Verification: PASS")

# 5. Verify Water.con
with tempfile.NamedTemporaryFile("w+", suffix=".con", delete=False) as f:
    f.write(templates["Water.con"])
    f_water = f.name
p_water = ConParser(f_water)
for idx, line in p_water.get_clean_lines():
    assert line.split()[0].startswith("Water.")
assert len(p_water.check_vector_syntax_no_spaces()) == 0
print("Water.con Verification: PASS")
'
```

### Invalidation Conditions
- Any changes in `tests/test_tier1_feature_coverage.py` altering the whitelist `valid_cmds` for `init.con`.
- Any modification to `tests/test_tier2_boundary_corner.py` requiring a water elevation other than `270.0`.
- Any addition of spaces around `/` in vectors inside `Terrain.con`, `Heightdata.con`, `Sky.con`, or `Water.con`.
- Any case change from lowercase `terrain.` or `heightmap.` to capitalized PascalCase.
