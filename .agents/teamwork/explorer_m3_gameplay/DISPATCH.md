# Dispatch: Milestone 3 - Explorer (Gameplay Topology) (`explorer_m3_gameplay`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/explorer_m3_gameplay`
- Identity: `teamwork_explorer`
- Role: `Gameplay Topology Strategist`

## Objective
Design and formulate the exact gameplay configuration for `levels/slovenia_golovec/GameplayObjects.con`:
1. Game Mode: Standard Conquest Head-On (EU vs MEC):
   - Team 1: EU (Southern base, Cartesian $(-250, 282.5, 1000)$).
   - Team 2: MEC (Northern base, Cartesian $(250, 272.8, 1700)$).
   - Neutral / Contested: CP 2 `CP_GOLOVEC_PASS` (Team 0, Cartesian $(0.0, 273.39, 1365.0)$ at Golovec focal point 46.046559 N, 14.592945 E).
2. Spawn Points:
   - At least 2 SpawnPoints per Control Point (`SP_EU_BASE_1`, `SP_EU_BASE_2`, `SP_GOLOVEC_1`, etc.).
   - Exact elevation grounding sampled from `Heightmap.raw` + standard Refractor 2 player collision offset of $+1.25\text{m}$.
   - Strict linkage between `ObjectTemplate.setControlPointId` on SpawnPoints and `ObjectTemplate.setControlPointId` on ControlPoints.
3. Combat Area:
   - `CombatArea_Golovec`: Encloses the Golovec battleground focal point $(0, 1365)$.
   - Polygon winding MUST be strictly counter-clockwise (positive signed area) to prevent the instant 10-second desertion kill.
   - `CombatAreaManager.use 1`.
4. Validate design against `tests/test_tier1_feature_coverage.py`, `tests/test_tier2_boundary_corner.py`, `tests/test_tier3_cross_feature.py`, and `tests/test_tier4_real_world_gameplay.py`.

Provide exact, validated templates and coordinate tables in `handoff.md`. Do NOT write implementation files in the project workspace directly.

## 2026-11-11T01:45:34Z
You are teamwork_explorer assigned to Milestone 3 - Explorer (Gameplay Topology Strategist).
Your working directory is /home/ator/BF2/.agents/teamwork/explorer_m3_gameplay.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/explorer_m3_gameplay/DISPATCH.md before starting work.
Also study the survey reports at /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md and /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md.

Design the exact gameplay topology for levels/slovenia_golovec/GameplayObjects.con:
1. Conquest Head-On (EU vs MEC): 3 balanced CPs (EU Base, Contested Golovec Pass at focal point 46.046559 N, 14.592945 E -> Cartesian (0, 1365), MEC Base).
2. SpawnPoints: at least 2 per CP, grounded on Heightmap.raw + 1.25m offset, properly linked via setControlPointId.
3. CombatArea: CCW winding enclosing focal point (0, 1365) with positive signed area.
Validate against tests in tests/test_tier1_feature_coverage.py, tests/test_tier2_boundary_corner.py, tests/test_tier3_cross_feature.py, and tests/test_tier4_real_world_gameplay.py.
Deliver your report in handoff.md and report back via send_message.
