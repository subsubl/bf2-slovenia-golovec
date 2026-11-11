# Dispatch: E2E Testing Track - Test Suite & Infra Development

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Survey References:
  - Workspace: /home/ator/BF2/.agents/teamwork/explorer_survey_1/handoff.md
  - BF2 Specs: /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md
  - Geospatial: /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md
- Working Directory: /home/ator/BF2/.agents/teamwork/test_writer_e2e
- Identity: teamwork_test_writer
- Role: E2E Test Suite Architect

## Objective
Design and implement the comprehensive E2E test suite for the Slovenia (Golovec / SE Ljubljana) AAA BF2 level package.
Your tests must be opaque-box and derived strictly from requirements in `ORIGINAL_REQUEST.md` and specifications in `PROJECT.md`:

1. **Test Infrastructure**:
   - Create test harness under `/home/ator/BF2/tests/` (e.g. `/home/ator/BF2/tests/test_bf2_e2e.py` or `/home/ator/BF2/tests/verify_bf2_level.py`).
   - The test runner must execute with standard Python (e.g. `python3 /home/ator/BF2/tests/test_bf2_e2e.py` or `pytest`), returning exit code 0 when all tests pass, and non-zero with detailed failure diagnostics when tests fail.
   - Note: Level files will be placed under `/home/ator/BF2/levels/slovenia_golovec/`. The test suite should check this target directory (and handle cases where some files are not yet created gracefully with clean test failure output).

2. **4-Tier Test Design**:
   - **Tier 1 - Feature Coverage (>=5 tests per feature)**:
     - Verify every mandatory configuration file exists: `init.con`, `Heightdata.con`, `Terrain.con`, `Sky.con`, `Water.con`, `StaticObjects.con`, `OvergrowthSystem.con`, `GameplayObjects.con`, and `Overgrowth/Overgrowth.raw`.
     - Verify basic syntax, non-empty content, valid command namespaces, block structure (`if v_arg1 == BF2Editor ... else ... endIf`), and slash-delimited vector formatting (`X/Y/Z`) with no spaces.
   - **Tier 2 - Boundary & Corner Cases (>=5 tests per feature)**:
     - Coordinate bounds check: Verify ALL static object coordinates $(X, Z)$ fall strictly within $[-2048.0, 2048.0]$.
     - Heightmap bounds check: Verify all sampled elevations $Y$ are $\ge 270.0\text{ m}$ (above water level) and $\le 455.0\text{ m}$, matching ground terrain height at $(X, Z)$.
     - Overgrowth mask check: Verify `Overgrowth/Overgrowth.raw` is exactly $2049 \times 2049 = 4,198,401$ bytes uint8.
     - CombatArea boundary check: Verify polygon vertices enclose the focal point $(0, 1365)$ and have positive signed area (counter-clockwise winding order) to prevent the out-of-bounds desertion bug.
     - Control Points and Spawn Points: Verify team IDs (1, 2, 0), unique CP IDs, and spawn point elevation offset `0/1.25/0`.
   - **Tier 3 - Cross-Feature Combinations**:
     - Verify all SpawnPoints reference valid ControlPoint IDs (`ObjectTemplate.setControlPointId`).
     - Verify `init.con` executes all sibling configuration scripts.
     - Verify CombatArea encloses all ControlPoints and SpawnPoints.
     - Verify overgrowth materials in `OvergrowthSystem.con` match definitions.
   - **Tier 4 - Real-World Gameplay Scenarios**:
     - Verify full Conquest Head-On playability: EU/US base CP 1, contested Golovec Pass CP 2 at focal point $(0, 1365)$, MEC base CP 3, each with >=2 spawn points.
     - Verify static buildings are distributed realistically across Golovec urban/rural zones without overlapping collisions.

3. **Deliverables**:
   - Write `/home/ator/BF2/.agents/teamwork/orchestrator/TEST_INFRA.md` (and `/home/ator/BF2/TEST_INFRA.md`).
   - Write all test implementation files under `/home/ator/BF2/tests/`.
   - Run the test suite against the current workspace (it is expected that files not yet created will fail, confirming the tests are sensitive and genuine).
   - Write `/home/ator/BF2/.agents/teamwork/orchestrator/TEST_READY.md` (and `/home/ator/BF2/TEST_READY.md`) with the coverage summary and exact runner command.
   - Submit handoff report upon completion.


## 2026-11-11T00:53:34Z
You are teamwork_test_writer assigned to the E2E Testing Track for the Slovenia (Golovec / SE Ljubljana) AAA BF2 Level Package.
Your working directory is /home/ator/BF2/.agents/teamwork/test_writer_e2e.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/test_writer_e2e/DISPATCH.md before starting.
Also review the survey handoffs at:
- /home/ator/BF2/.agents/teamwork/explorer_survey_1/handoff.md
- /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md

Follow the 4-Tier Test Design Methodology:
1. Tier 1: Feature Coverage (mandatory configuration files, syntax, block structure, case sensitivity, vector formatting).
2. Tier 2: Boundary & Corner Cases (coordinates in [-2048, 2048], ground elevation >= 270.0m and matching Heightmap.raw, Overgrowth.raw 4,198,401 bytes, CCW combat area winding).
3. Tier 3: Cross-Feature Combinations (SpawnPoints referencing valid CPs, CombatArea enclosing all entities, init.con invoking all child scripts).
4. Tier 4: Real-World Gameplay Scenarios (balanced Conquest Head-On setup, static building distributions).

Deliverables:
- Write /home/ator/BF2/.agents/teamwork/orchestrator/TEST_INFRA.md and /home/ator/BF2/TEST_INFRA.md.
- Write executable test suite files under /home/ator/BF2/tests/.
- Run your test suite to verify it functions properly (expecting failures on missing/unimplemented files).
- Write /home/ator/BF2/.agents/teamwork/orchestrator/TEST_READY.md and /home/ator/BF2/TEST_READY.md with coverage summary and test runner command.
- Write your handoff.md and notify me when complete. Do NOT modify implementation files under levels/ or scripts/.


## 2026-11-11T01:01:45Z
**Context**: E2E Testing Track - Test Suite & Infra Development
**Content**: Heartbeat check: The test files in `tests/` are in place. Please author `TEST_INFRA.md` and `TEST_READY.md` and deliver your `handoff.md` report.
**Action**: Please report status or submit handoff.md when ready.
