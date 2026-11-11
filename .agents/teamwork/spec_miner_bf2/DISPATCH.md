# Dispatch: Survey 2 - BF2 Level Architecture & Spec Mining

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Working Directory: /home/ator/BF2/.agents/teamwork/spec_miner_bf2
- Identity: teamwork_spec_miner
- Role: BF2 Specification Miner

## Objective
Investigate and specify Battlefield 2 level package architecture, syntax, and specs:
1. BF2 `.con` file format, syntax rules, block structures, header comments, and case sensitivity.
2. Exact structure and requirements for: `init.con`, `Sky.con`, `Water.con`, `Terrain.con`, `Heightdata.con`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
3. BF2 coordinate system: Cartesian X, Y (elevation), Z, orientation (yaw, pitch, roll). Map boundaries: 4096m x 4096m with origin at (0,0,0) ranging from [-2048, 2048].
4. Standard BF2 vanilla static building meshes suitable for European urban/rural buildings (e.g. from bf2 vanilla objects/staticobjects: me_house, eu_building, barns, sheds, etc. or standard vanilla object templates).
5. Overgrowth system mesh definitions and density channel formats (raw byte masks, channels, material types).
6. GameplayObjects.con Conquest Head-On requirements: ControlPoints (US vs MEC or EU vs MEC), SpawnPoints, ObjectTemplates, Combat Area boundaries centered around the Golovec focal point (46.046559 N, 14.592945 E).
7. Document all required template names, commands, and valid value ranges.

## 2026-11-11T00:38:38Z
You are teamwork_spec_miner assigned to Survey 2 - BF2 Level Architecture & Spec Mining.
Your working directory is /home/ator/BF2/.agents/teamwork/spec_miner_bf2.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md and /home/ator/BF2/.agents/teamwork/spec_miner_bf2/DISPATCH.md before starting.

Investigate and document the exact Battlefield 2 level package architecture and syntax specs:
1. BF2 `.con` file format, syntax rules, block structures, header comments, and case sensitivity.
2. Exact structure and requirements for: `init.con`, `Sky.con`, `Water.con`, `Terrain.con`, `Heightdata.con`, `StaticObjects.con`, `OvergrowthSystem.con`, and `GameplayObjects.con`.
3. BF2 coordinate system: Cartesian X, Y (elevation), Z, orientation (yaw, pitch, roll). Map boundaries: 4096m x 4096m with origin at (0,0,0) ranging from [-2048, 2048].
4. Standard BF2 vanilla static building meshes suitable for European urban/rural buildings (e.g. from bf2 vanilla objects/staticobjects: me_house, eu_building, barns, sheds, etc. or standard vanilla object templates).
5. Overgrowth system mesh definitions and density channel formats (raw byte masks, channels, material types).
6. GameplayObjects.con Conquest Head-On requirements: ControlPoints (US vs MEC or EU vs MEC), SpawnPoints, ObjectTemplates, Combat Area boundaries centered around the Golovec focal point (46.046559 N, 14.592945 E).
7. Document all required template names, commands, and valid value ranges.
Record your detailed findings in handoff.md in your working directory and notify me when complete. Do not modify or write source files.

## 2026-11-11T00:49:17Z
**Context**: Survey 2 - BF2 Level Architecture & Spec Mining
**Content**: Heartbeat safety check: your progress.md has not been updated since 00:39:30Z.
**Action**: Please report your current investigation status or deliver handoff.md if complete.
