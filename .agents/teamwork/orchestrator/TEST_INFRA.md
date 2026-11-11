# Battlefield 2 Level Package: Test Infrastructure & Specification

## 1. Overview
This document specifies the automated, independent E2E test harness and 4-tier verification suite developed for the Slovenia (Golovec / SE Ljubljana) AAA Battlefield 2 Level Package (`levels/slovenia_golovec/`).

The test suite implements rigorous, opaque-box validation derived directly from the requirements in `ORIGINAL_REQUEST.md`, Refractor 2 engine specifications in `PROJECT.md`, and geospatial ground truth in Slovenian National LiDAR data (`Heightmap.raw`, `dmr_raw/`, `pof_1m/`).

---

## 2. Test Suite Architecture & File Layout

```text
/home/ator/BF2/
├── tests/
│   ├── con_parser.py                      # Refractor 2 .con parser & geospatial/heightmap utility
│   ├── verify_bf2_level.py                # Master E2E runner & diagnostic CLI
│   ├── test_tier1_feature_coverage.py     # Tier 1: Feature Coverage (37 tests)
│   ├── test_tier2_boundary_corner.py      # Tier 2: Boundary & Corner Cases (25 tests)
│   ├── test_tier3_cross_feature.py        # Tier 3: Cross-Feature Combinations (14 tests)
│   └── test_tier4_real_world_gameplay.py  # Tier 4: Real-World Gameplay Scenarios (12 tests)
├── TEST_INFRA.md                          # Test infrastructure specification
└── TEST_READY.md                          # Test suite execution & readiness report
```

### Module Responsibilities
- **`con_parser.py`**:
  - `ConParser`: Refractor 2 line-by-line parser; handles command namespaces, arguments, quotes, comments (`rem`), and balanced blocks (`if ... else ... endIf`).
  - `HeightmapSampler`: Memory-efficient bilinear elevation interpolation from `Heightmap.raw` (2049x2049 uint16, 2.0m grid spacing, scale 0.01).
  - `polygon_signed_area`: Computes signed area using Shoelace formula to verify Counter-Clockwise (CCW) winding.
  - `point_in_polygon`: Ray-casting algorithm to verify entities are enclosed by the CombatArea boundary.
  - `LEVEL_DIR`: Dynamic path-like object (`DynamicLevelDir`) responding to the `BF2_LEVEL_DIR` environment variable.
- **`verify_bf2_level.py`**:
  - Diagnostic CLI runner supporting tier selection (`--tier 1,2,3,4,all`), custom target directory (`--level-dir`), verbose tracebacks (`--verbose`), and JSON reporting (`--report`).
  - Returns standard exit code `0` on 100% pass, and exit code `1` with actionable failure diagnostics on failure.

---

## 3. 4-Tier Test Design Methodology

### Tier 1: Feature Coverage (37 Tests)
Verifies baseline structural, syntactical, and namespace integrity for all mandatory level files:
1. **Mandatory File Existence**:
   - `init.con`, `Heightdata.con`, `Terrain.con`, `Sky.con`, `Water.con`, `StaticObjects.con`, `OvergrowthSystem.con`, `GameplayObjects.con`, and `Overgrowth/Overgrowth.raw`.
2. **File Content & Encoding Integrity**:
   - Files are non-empty (>50 bytes), contain valid UTF-8/ASCII characters with no NULL bytes (`\x00`), and have no unterminated quotation marks.
   - Files contain active engine commands beyond comments.
3. **Valid Refractor 2 Command Namespaces**:
   - `init.con`: `LevelSettings.*`, `texturemanager.*`, `run`, `if`, `else`, `endIf`.
   - `Heightdata.con`: `heightmap.*`.
   - `Terrain.con`: `terrain.*`.
   - `Sky.con`: `Renderer.*`, `Skydome.*`.
   - `Water.con`: `Water.*`.
   - `StaticObjects.con`: `Object.*`, `console.*`, `if`, `else`, `endIf`.
   - `OvergrowthSystem.con`: `Overgrowth.*`, `OvergrowthType.*`.
   - `GameplayObjects.con`: `CombatAreaManager.*`, `CombatArea.*`, `ObjectTemplate.*`, `Object.*`.
4. **Conditional Block Structure**:
   - `init.con`: Balanced `if v_arg1 == BF2Editor ... else ... endIf`.
   - `StaticObjects.con`: Balanced `if v_arg1 == BF2Editor ... endIf`.
   - Engine nesting limit $\le 4$ and no orphaned `else` statements.
5. **Vector Formatting**:
   - Enforces slash-delimited vectors with **NO spaces** (`X/Y/Z`, `Yaw/Pitch/Roll`, `2/0.01/2`). Refractor 2 fails to parse vectors if whitespace surrounds slashes.
6. **Case Sensitivity**:
   - Enforces canonical PascalCase for object templates (`Object.create`, `ObjectTemplate.create`, `CombatArea.create`) and lowercase for terrain commands (`terrain.create`, `heightmap.setSize`).

### Tier 2: Boundary & Corner Cases (25 Tests)
Verifies metric, binary, and boundary constraints:
1. **Coordinate Boundaries**:
   - All static objects, ControlPoints, SpawnPoints, and CombatArea polygon vertices must satisfy $X, Z \in [-2048.0, 2048.0]$.
2. **Heightmap & Grounding Bounds**:
   - Ground elevations $Y \ge 270.0\text{ m}$ (above water level defined in `Terrain.con`).
   - Ground elevations $Y \le 455.0\text{ m}$ (within maximum Golovec terrain elevation).
   - Bilinear elevation verification: $|Y_{\text{building}} - Y_{\text{terrain}}| \le 0.75\text{ m}$.
   - ControlPoint elevation verification: $|Y_{\text{cp}} - Y_{\text{terrain}}| \le 0.50\text{ m}$.
3. **Overgrowth Mask Integrity**:
   - `Overgrowth/Overgrowth.raw` size is exactly $2049 \times 2049 = 4,198,401$ bytes uint8.
   - Array is headerless and values fall within $[0, 255]$.
   - Non-trivial density with active canopy over the Golovec ridge.
4. **CombatArea Anti-Clockwise Rule**:
   - Boundary polygon has strictly **positive signed area** (counter-clockwise vertex ordering). Clockwise ordering in Refractor 2 triggers the fatal 10-second desertion kill zone bug.
   - Encloses the focal point $(0.0, 1365.0)$.
   - Minimum playable area $\ge 500,000\text{ m}^2$.
   - `CombatAreaManager.timeAllowedOutside 10.0` and `CombatAreaManager.use 1`.
5. **Control Points & Spawn Points Attributes**:
   - Team IDs restricted to $\{0, 1, 2\}$.
   - Unique CP IDs across all flags.
   - Spawn point elevation offset vector strictly `0/1.25/0` (prevents players falling through terrain mesh upon spawning).
   - Capture radius $\in [15.0, 50.0]\text{ m}$, capture time $\in [10.0, 30.0]\text{ s}$.

### Tier 3: Cross-Feature Combinations (14 Tests)
Verifies multi-file and multi-system integration:
1. **Spawn-to-ControlPoint Linkage**:
   - Every `SpawnPoint` references an active `ControlPoint` via `ObjectTemplate.setControlPointId`.
   - Every `ControlPoint` has associated spawn points.
   - Spawn points are within tactical proximity ($\le 120\text{ m}$) of parent CP.
2. **Master `init.con` Execution Flow**:
   - Verifies `init.con` invokes all child configuration files: `Heightdata.con`, `Terrain.con`, `Sky.con`, `Water.con`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
3. **Spatial Containment**:
   - 100% of ControlPoints fall inside the CombatArea polygon.
   - 100% of SpawnPoints fall inside the CombatArea polygon.
4. **Overgrowth System Referential Consistency**:
   - Declared materials (`Overgrowth.addMaterial`) are activated (`Overgrowth.setActiveMaterial`).
   - Foliage geometries match vanilla BF2 models (`fir_mixed02`, `birch_green_1`, etc.).

### Tier 4: Real-World Gameplay Scenarios (12 Tests)
Verifies playable gameplay balance and realistic asset distribution:
1. **Conquest Head-On Playability**:
   - Exactly 3 Control Points: Team 1 (EU Base), Team 0 (Contested Golovec Pass), Team 2 (MEC Base).
   - Contested flag located at Golovec Pass focal point $(0.0, 1365.0)$ within $\pm 15\text{ m}$.
   - Team bases positioned on opposing sides of the focal point ($Z < 1365$ vs $Z > 1365$).
   - $\ge 2$ spawn points per Control Point for respawn reliability.
   - Spawn points separated from the flagpole ($\ge 3.0\text{ m}$) and from each other ($\ge 2.0\text{ m}$) to prevent telefragging and collision.
2. **Static Building Distribution**:
   - $\ge 50$ static buildings extracted from OSM.
   - Only vanilla Refractor 2 meshes (`eu_building...`, `me_house...`, `barn_01`, `farmhouse`, `wooden_shed`, etc.).
   - No duplicate coordinates.
   - Origin separation distance $\ge 2.0\text{ m}$ to prevent physical mesh overlap.
   - Spatial distribution spanning $\ge 500\text{ m}$ across both East-West and North-South axes.

---

## 4. Test Execution Instructions

### A. Run via Master E2E Harness
```bash
# Run complete 4-tier suite against standard level package
python3 /home/ator/BF2/tests/verify_bf2_level.py

# Run in verbose mode with failure diagnostics
python3 /home/ator/BF2/tests/verify_bf2_level.py -v

# Run specific tier (e.g. Tier 1 or Tier 2)
python3 /home/ator/BF2/tests/verify_bf2_level.py --tier 1
python3 /home/ator/BF2/tests/verify_bf2_level.py --tier 2

# Export JSON summary report
python3 /home/ator/BF2/tests/verify_bf2_level.py --report /tmp/verification_report.json

# Test a custom level directory
python3 /home/ator/BF2/tests/verify_bf2_level.py --level-dir /path/to/custom_level
```

### B. Run via Pytest
```bash
python3 -m pytest /home/ator/BF2/tests/ -v
```

### C. Run via Standard Python Unittest
```bash
python3 -m unittest discover -s /home/ator/BF2/tests -v
```
