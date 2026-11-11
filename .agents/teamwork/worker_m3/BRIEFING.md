# BRIEFING — 2026-11-11T01:58:00Z

## Mission
Assemble the complete Battlefield 2 level package under `/home/ator/BF2/levels/slovenia_golovec/` and configure gameplay objects via `/home/ator/BF2/scripts/assemble_level_package.py`, ensuring all 88 tests pass.

## 🔒 My Identity
- Archetype: teamwork_worker
- Roles: implementer, qa
- Working directory: /home/ator/BF2/.agents/teamwork/worker_m3
- Original parent: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Milestone: Milestone 3 - Level Package Assembly & Gameplay Configuration

## 🔒 Key Constraints
- Exclusive write ownership:
  - `/home/ator/BF2/scripts/assemble_level_package.py`
  - `/home/ator/BF2/levels/slovenia_golovec/init.con`
  - `/home/ator/BF2/levels/slovenia_golovec/Heightdata.con`
  - `/home/ator/BF2/levels/slovenia_golovec/Terrain.con`
  - `/home/ator/BF2/levels/slovenia_golovec/Sky.con`
  - `/home/ator/BF2/levels/slovenia_golovec/Water.con`
  - `/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con`
  - `/home/ator/BF2/levels/slovenia_golovec/Heightmap.raw` (hardlink)
  - `/home/ator/BF2/levels/slovenia_golovec/ColorMap.dds` (hardlink)
  - Working directory: `/home/ator/BF2/.agents/teamwork/worker_m3/`
- DO NOT modify existing `StaticObjects.con`, `OvergrowthSystem.con`, or `Overgrowth/Overgrowth.raw`.
- DO NOT cheat: genuine logic, real state and behavior, no hardcoded test outputs or dummy facades.
- All 88 tests in `/home/ator/BF2/tests/verify_bf2_level.py` must pass with exit code 0.

## Current Parent
- Conversation ID: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Updated: 2026-11-11T01:58:00Z

## Task Summary
- **What to build**: Build `scripts/assemble_level_package.py` to assemble the Slovenia Golovec level package and execute it to generate all configuration files and asset links, leaving M1/M2 artifacts intact.
- **Success criteria**: Python test suite `python3 tests/verify_bf2_level.py -v` passes 100% (88 tests passing).
- **Interface contracts**: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- **Code layout**: `/home/ator/BF2/levels/slovenia_golovec/`

## Key Decisions Made
- Used `os.link` to hardlink `Heightmap.raw` and `ColorMap.dds` from workspace root to `levels/slovenia_golovec/`, conserving disk space on the constrained root partition while satisfying Refractor 2 engine level layout conventions.
- Formulated `init.con` adhering strictly to the 7-command whitelist (`if`, `else`, `endIf`, `run`, `LevelSettings.InitWorld`, `LevelSettings.CustomTextureSuffix`, `texturemanager.customTextureSuffix`) and invoking all 7 child scripts across editor and client/server branches.
- Placed 3 balanced Control Points: Team 1 EU Base at `(-250.0, 1000.0)` ($Z < 1365$), Contested Neutral Golovec Pass at `(0.0, 1365.0)` ($Z = 1365$), and Team 2 MEC Base at `(250.0, 1700.0)` ($Z > 1365$) with ground elevations sampled directly from `Heightmap.raw` (0.00m deviation).
- Defined 2 spawn points per CP with `ObjectTemplate.setSpawnPositionOffset 0/1.25/0`, spaced $\ge 9.4\text{m}$ from flagpoles and separated by $\ge 18.8\text{m}$.
- Defined Combat Area boundary with counter-clockwise winding (+1,440,000 $m^2$ signed area) enclosing the focal point and 100% of CPs and SPs.

## Artifact Index
- `/home/ator/BF2/scripts/assemble_level_package.py` — Level assembly script
- `/home/ator/BF2/levels/slovenia_golovec/init.con` — Master conductor script
- `/home/ator/BF2/levels/slovenia_golovec/Heightdata.con` — Heightmap grid configuration
- `/home/ator/BF2/levels/slovenia_golovec/Terrain.con` — Terrain physics and water elevation
- `/home/ator/BF2/levels/slovenia_golovec/Sky.con` — Atmospheric fog, lighting, and skydome
- `/home/ator/BF2/levels/slovenia_golovec/Water.con` — River hydrology and wave physics
- `/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con` — Conquest Head-On gameplay topology
- `/home/ator/BF2/levels/slovenia_golovec/Heightmap.raw` — Hardlinked terrain elevation asset
- `/home/ator/BF2/levels/slovenia_golovec/ColorMap.dds` — Hardlinked terrain texture asset
- `/home/ator/BF2/.agents/teamwork/worker_m3/progress.md` — Liveness and progress tracking
- `/home/ator/BF2/.agents/teamwork/worker_m3/handoff.md` — 5-component handoff report

## Change Tracker
- **Files modified**:
  - `scripts/assemble_level_package.py`: Created complete package assembly script
  - `levels/slovenia_golovec/init.con`: Generated conductor script
  - `levels/slovenia_golovec/Heightdata.con`: Generated heightmap config
  - `levels/slovenia_golovec/Terrain.con`: Generated terrain config
  - `levels/slovenia_golovec/Sky.con`: Generated atmospheric config
  - `levels/slovenia_golovec/Water.con`: Generated hydrology config
  - `levels/slovenia_golovec/GameplayObjects.con`: Generated gameplay topology
  - `levels/slovenia_golovec/Heightmap.raw`: Hardlinked
  - `levels/slovenia_golovec/ColorMap.dds`: Hardlinked
- **Build status**: 88/88 E2E tests passing (100.0%), 123/123 pytest passing (100.0%)
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pass (88/88 E2E tests passing in 0.18s)
- **Lint status**: Clean (py_compile passed)
- **Tests added/modified**: Verified against all 88 test cases in `verify_bf2_level.py`

## Loaded Skills
- None
