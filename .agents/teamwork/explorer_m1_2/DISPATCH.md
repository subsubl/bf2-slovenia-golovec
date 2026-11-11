# Dispatch: Milestone 1 - Explorer 2 (Heightmap Elevation Sampling & Grounding)

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Survey References:
  - Geospatial Pipeline: /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md
  - Workspace Assets: /home/ator/BF2/.agents/teamwork/explorer_survey_1/handoff.md
- Working Directory: /home/ator/BF2/.agents/teamwork/explorer_m1_2
- Identity: teamwork_explorer
- Role: Elevation Sampling Strategist

## Objective
Formulate the exact ground elevation sampling and building vertical placement strategy for Milestone 1:
1. `Heightmap.raw` properties: 2049x2049 uint16 little-endian, 2.0m grid spacing, scale 0.01, zero header.
2. Grid coordinate mapping: $u = (X + 2048.0)/2.0$, $v = (Z + 2048.0)/2.0$. Row 0 = South ($Z=-2048$), Row 2048 = North ($Z=+2048$), Col 0 = West ($X=-2048$), Col 2048 = East ($X=+2048$).
3. Bilinear interpolation sampling formula for continuous ground height $Y(X, Z)$ in meters.
4. Vertical grounding rules:
   - Base water elevation is $270.0\text{ m}$. Buildings must not be placed submerged or below ground.
   - Elevation offset: whether building origin in BF2 static meshes sits at ground level (Y=0 relative to mesh) or needs foundation sinking (e.g. -0.2m or 0.0m).
   - Check if sampling multiple corners of a building footprint to determine ground slope or average elevation is beneficial.
5. Provide verified Python implementation routines for sampling and validation in your `handoff.md`. Do NOT write implementation files in the project workspace directly.

## 2026-11-11T00:53:45Z
You are teamwork_explorer assigned to Milestone 1 - Explorer 2 (Heightmap Elevation Sampling & Grounding).
Your working directory is /home/ator/BF2/.agents/teamwork/explorer_m1_2.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/explorer_m1_2/DISPATCH.md before starting.
Also review the survey handoffs at:
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md
- /home/ator/BF2/.agents/teamwork/explorer_survey_1/handoff.md

Formulate the ground elevation sampling and building vertical placement strategy for Milestone 1:
1. Heightmap.raw properties: 2049x2049 uint16 little-endian, 2.0m grid spacing, scale 0.01, zero header.
2. Grid coordinate mapping: u = (X + 2048.0)/2.0, v = (Z + 2048.0)/2.0. Row 0 = South (Z=-2048), Row 2048 = North (Z=+2048), Col 0 = West (X=-2048), Col 2048 = East (X=+2048).
3. Bilinear interpolation sampling formula for continuous ground height Y(X, Z) in meters.
4. Vertical grounding rules:
   - Base water elevation is 270.0m. Buildings must not be placed submerged or below ground.
   - Elevation offset: whether building origin in BF2 static meshes sits at ground level or needs foundation offset.
   - Check multi-corner sampling vs centroid sampling.
5. Provide verified Python implementation routines for sampling and validation in your handoff.md.
Do NOT modify or create implementation files in the project workspace directly; report your findings in handoff.md and notify me when complete.
