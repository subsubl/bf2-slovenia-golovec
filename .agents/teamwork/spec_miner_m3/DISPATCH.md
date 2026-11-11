# Dispatch: Milestone 3 - Spec Miner (`spec_miner_m3`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/spec_miner_m3`
- Identity: `teamwork_spec_miner`
- Role: `BF2 Environment & Master Con Spec Miner`

## Objective
Extract and formulate the exact BF2 Refractor 2 specifications and syntax for:
1. `levels/slovenia_golovec/init.con`:
   - Conductor script running all configuration files inside `if v_arg1 == BF2Editor` conditional blocks.
   - Exact inclusion syntax for `Heightdata.con`, `Terrain.con`, `Sky.con`, `Water.con`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
   - Engine initialization variables (`gameLogic.createGameManager`, world dimensions, etc.).
2. `levels/slovenia_golovec/Terrain.con`:
   - `terrain.load Heightmap.raw`, `terrain.setWaterElevation 270.0`, `terrain.setWorldSize 4096`.
   - Texture mapping / colormap references (`ColorMap.dds`).
3. `levels/slovenia_golovec/Heightdata.con`:
   - Terrain elevation scaling and grid spacing matching `Heightmap.raw` (2049x2049, 2.0m spacing, scale 0.01).
4. `levels/slovenia_golovec/Sky.con`:
   - Fog colors, fog distance (`Renderer.fogColor 175/190/205`, `Renderer.fogStartEndAndBase 100/1200/1.5/0.4`), skydome setup.
5. `levels/slovenia_golovec/Water.con`:
   - Water surface color, depth color, wave height (`0.12`).

Provide exact, validated templates in `handoff.md`. Do NOT write implementation files in the project workspace directly.


## 2026-11-11T01:45:29Z
You are teamwork_spec_miner assigned to Milestone 3 - Spec Miner (BF2 Environment & Master Con Spec Miner).
Your working directory is /home/ator/BF2/.agents/teamwork/spec_miner_m3.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/spec_miner_m3/DISPATCH.md before starting work.
Also study the survey reports at /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md and /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md.

Mine and formulate exact Refractor 2 specifications and templates for:
1. levels/slovenia_golovec/init.con (conductor script invoking all .con files in conditional blocks).
2. levels/slovenia_golovec/Terrain.con (terrain.load, setWaterElevation 270.0, setWorldSize 4096).
3. levels/slovenia_golovec/Heightdata.con (gridSize 2 2, size 2049 2049, scale 2/0.01/2).
4. levels/slovenia_golovec/Sky.con (fog colors, start/end distances, skydome setup).
5. levels/slovenia_golovec/Water.con (water colors, depth colors, wave height).
Check ConParser rules and E2E tests in tests/test_tier1_feature_coverage.py and tests/test_tier3_cross_feature.py.
Deliver your report in handoff.md and report back via send_message.
