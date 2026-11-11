# Dispatch: Milestone 1 - Explorer 3 (Static Mesh Mapping & StaticObjects.con)

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Survey References:
  - BF2 Specs: /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md
  - Geospatial Pipeline: /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md
- Working Directory: /home/ator/BF2/.agents/teamwork/explorer_m1_3
- Identity: teamwork_explorer
- Role: Static Mesh Mapping Strategist

## Objective
Formulate the exact static mesh mapping rules and `StaticObjects.con` formatting specification:
1. Standard BF2 vanilla static meshes suitable for European urban / suburban / rural buildings:
   - Urban / commercial / large buildings (e.g. `eu_building01`, `eu_building02`, `eu_office_01`, `me_apartment_01`, `citybuilding_01`).
   - Suburban residential houses (e.g. `eu_house_01`, `eu_house_02`, `me_house_01`, `me_house_02`, `me_house_03`, `me_house_04`, `me_house_05`, `me_house_06`).
   - Rural / farm / industrial (e.g. `barn_01`, `barn_02`, `farmhouse`, `wooden_shed`, `warehouse_01`).
2. Mapping rules based on OSM tags:
   - Tags like `building=residential`, `building=house`, `building=apartments`, `building=commercial`, `building=industrial`, `building=farm_auxiliary`, `building:levels`, and polygon area $A$.
3. Exact syntax and formatting for `StaticObjects.con`:
   - Editor blocks `if v_arg1 == BF2Editor ... endIf`.
   - Object block structure:
     `Object.create <MeshName>`
     `Object.absolutePosition <X>/<Y>/<Z>`
     `Object.rotation <Yaw>/<Pitch>/<Roll>`
     `Object.layer 1`
   - Strict slash-delimited vector formatting with NO spaces (`-45.200/274.500/1320.800`).
   - 3-decimal float precision.
4. Density and performance budget:
   - Target object count for AAA playability and performance (recommended 500 to 1,500 representative static buildings).
5. Document all recommendations, mapping dictionaries, and output templates in `handoff.md`. Do NOT write implementation files in the project workspace directly.


## 2026-11-11T00:53:51Z
You are teamwork_explorer assigned to Milestone 1 - Explorer 3 (Static Mesh Mapping & StaticObjects.con).
Your working directory is /home/ator/BF2/.agents/teamwork/explorer_m1_3.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/explorer_m1_3/DISPATCH.md before starting.
Also review the survey handoffs at:
- /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md

Formulate the static mesh mapping rules and StaticObjects.con formatting specification:
1. Standard BF2 vanilla static meshes suitable for European urban / suburban / rural buildings:
   - Urban / commercial / large buildings (e.g. eu_building01, eu_building02, eu_office_01, me_apartment_01, citybuilding_01).
   - Suburban residential houses (e.g. eu_house_01, eu_house_02, me_house_01 to me_house_06).
   - Rural / farm / industrial (e.g. barn_01, barn_02, farmhouse, wooden_shed, warehouse_01).
2. Mapping rules based on OSM tags (building=*, building:levels, footprint area A).
3. Exact syntax and formatting for StaticObjects.con:
   - Editor blocks if v_arg1 == BF2Editor ... endIf.
   - Object block structure: Object.create, Object.absolutePosition X/Y/Z, Object.rotation Yaw/Pitch/Roll, Object.layer 1.
   - Strict slash-delimited vector formatting with NO spaces. 3-decimal float precision.
4. Density and performance budget: target object count for AAA playability (500 to 1,500 representative static buildings).
5. Document all recommendations, mapping dictionaries, and output templates in handoff.md and notify me when complete. Do NOT modify or create implementation files in the project workspace directly.
