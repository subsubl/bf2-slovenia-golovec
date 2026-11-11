# Dispatch: Milestone 1 - Worker (OSM Building Extraction & StaticObjects.con Implementation)

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Explorer Handoff Reports:
  - Explorer 1 (OSM extraction & script template): /home/ator/BF2/.agents/teamwork/explorer_m1_1/handoff.md
  - Explorer 2 (Heightmap sampling & grounding): /home/ator/BF2/.agents/teamwork/explorer_m1_2/handoff.md
  - Explorer 3 (Static mesh mapping & density budget): /home/ator/BF2/.agents/teamwork/explorer_m1_3/handoff.md
- Working Directory: /home/ator/BF2/.agents/teamwork/worker_m1
- Identity: teamwork_worker
- Role: Static Objects Implementer

## Mandatory Integrity Warning
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Write Ownership
You have exclusive write ownership over:
- `/home/ator/BF2/scripts/extract_osm_buildings.py`
- `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con`
- `/home/ator/BF2/.osm_cache/` (cache directory)
- Your metadata directory `/home/ator/BF2/.agents/teamwork/worker_m1/`
Do NOT modify files in `tests/`, `levels/slovenia_golovec/` other than `StaticObjects.con`, or other agents' folders.

## Objectives
1. Implement the complete, production-grade extraction script in `/home/ator/BF2/scripts/extract_osm_buildings.py` following the designs in Explorer 1, 2, and 3 reports:
   - Official OSM 0.6 API via 4 quadrants (SW, SE, NW, NE) with local caching in `/home/ator/BF2/.osm_cache/` and 1.5s delay between network calls.
   - Parse ways and relation multipolygons; extract closed rings.
   - Compute true geometric centroids $(C_X, C_Z)$ via Green's Theorem and area via Shoelace formula.
   - Calculate heading yaw from longest polygon edge $(\Delta X, \Delta Z)$ matching Refractor 2 rotation convention.
   - Bilinear elevation sampling from `/home/ator/BF2/Heightmap.raw` with $0.0\text{ m}$ foundation offset.
   - Filter: Area $\ge 35.0\text{ m}^2$, coordinates strictly in $[-2048.0, 2048.0]$, ground elevation $Y \ge 270.0\text{ m}$ (water level).
   - Apply spatial thinning (R=30.0m greedy non-maximum suppression) to produce ~1,000–1,400 buildings (within 500–1,500 budget).
   - Classify building tags and dimensions into BF2 European vanilla static meshes (`eu_building01`, `eu_building02`, `eu_office_01`, `me_apartment_01`, `citybuilding_01`, `eu_house_01`, `eu_house_02`, `me_house_01`-`06`, `barn_01`, `barn_02`, `farmhouse`, `wooden_shed`, `warehouse_01`).
   - Format output `/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con` with editor conditionals, slash-delimited vectors with NO spaces (`X/Y/Z`, `Yaw/0.000/0.000`), 3-decimal float precision, and Layer 1.
2. Execute your script: `python3 /home/ator/BF2/scripts/extract_osm_buildings.py`.
3. Verify that `levels/slovenia_golovec/StaticObjects.con` is generated, syntactically valid, has between 500 and 1,500 objects, all coordinates in $[-2048, 2048]$, and all $Y \ge 270.0\text{ m}$.
4. Document commands run, test results, and file paths in `handoff.md` and notify orchestrator when done.


## 2026-11-11T01:02:07Z
Sender: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
Message: You are teamwork_worker assigned to Milestone 1 Implementation (OSM Building Extraction & StaticObjects.con).
Your working directory is /home/ator/BF2/.agents/teamwork/worker_m1.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/worker_m1/DISPATCH.md before starting.
Also review the Explorer handoff reports at:
- /home/ator/BF2/.agents/teamwork/explorer_m1_1/handoff.md
- /home/ator/BF2/.agents/teamwork/explorer_m1_2/handoff.md
- /home/ator/BF2/.agents/teamwork/explorer_m1_3/handoff.md
