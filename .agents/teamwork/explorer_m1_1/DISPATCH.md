# Dispatch: Milestone 1 - Explorer 1 (OSM Footprint Extraction Strategy)

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Survey References:
  - Geospatial Pipeline: /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md
  - BF2 Specs: /home/ator/BF2/.agents/teamwork/spec_miner_bf2/handoff.md
- Working Directory: /home/ator/BF2/.agents/teamwork/explorer_m1_1
- Identity: teamwork_explorer
- Role: OSM Extraction Strategist

## Objective
Formulate the exact extraction and filtering strategy for OpenStreetMap building footprints across the 4096m x 4096m Golovec bounding box:
1. Map bounds in WGS84: `[46.015750 N, 14.566437 E]` to `[46.052791 N, 14.619621 E]`.
2. Confirm the exact API query mechanism (official OSM 0.6 API via 4 quadrants tested by survey: NW, NE, SW, SE) vs Overpass endpoints.
3. Define polygon parsing: ways with `building=*`, relation multipolygons, extracting closed coordinate rings.
4. Define filtering rules: minimum footprint area (e.g. discard sheds < 15 m² to avoid exceeding BF2 static object limits), boundary clipping strictly within Cartesian $[-2048, 2048]$.
5. Define centroid calculation formula and heading/yaw derivation from longest polygon edge.
6. Provide a concrete, executable Python design/script template for the Worker to implement in `scripts/extract_osm_buildings.py`. Do NOT write implementation files in the project workspace directly; put your recommendations and sample code in `handoff.md`.


## 2026-11-11T00:53:39Z
You are teamwork_explorer assigned to Milestone 1 - Explorer 1 (OSM Footprint Extraction Strategy).
Your working directory is /home/ator/BF2/.agents/teamwork/explorer_m1_1.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/explorer_m1_1/DISPATCH.md before starting.
Also review the survey handoff at /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md.

Formulate the exact extraction and filtering strategy for OpenStreetMap building footprints across the 4096m x 4096m Golovec bounding box:
1. Confirm API query mechanism (official OSM 0.6 API via 4 quadrants tested by survey: NW, NE, SW, SE) vs Overpass endpoints.
2. Define polygon parsing: ways with building=*, relation multipolygons, extracting closed coordinate rings.
3. Define filtering rules: minimum footprint area (e.g. discard micro-sheds < 15 m²), boundary clipping strictly within Cartesian [-2048, 2048].
4. Define centroid calculation formula and heading/yaw derivation from longest polygon edge.
5. Provide a concrete Python design/template in your handoff.md for the Worker to implement in scripts/extract_osm_buildings.py.
Do NOT modify or create implementation files in the project workspace directly; report your findings in handoff.md and notify me when complete.
