# BRIEFING — 2026-11-11T00:39:00Z

## Mission
Investigate and specify the geospatial transformation, heightmap sampling, OSM building extraction, and LiDAR canopy processing pipelines for the Golovec BF2 map.

## 🔒 My Identity
- Archetype: explorer
- Roles: Geospatial Data Researcher, Pipeline Analyst
- Working directory: /home/ator/BF2/.agents/teamwork/explorer_survey_geo
- Original parent: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Milestone: Survey 3 - Geospatial Pipeline & Heightmap Sampling

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Do NOT modify or write source files (only write in own teamwork directory)

## Current Parent
- Conversation ID: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Updated: 2026-11-11T00:39:00Z

## Investigation State
- **Explored paths**: `/home/ator/BF2` workspace files, `Heightmap.raw`, `tiles_manifest.json`, `assemble_colormap.py`, `dmr_raw/` (LAZ), `pof_1m/` (TIFF), `kodeljevo.osm`, Flycom LiDAR assets server (`assets.flycom.si`), official OpenStreetMap 0.6 API endpoints, pyproj, GDAL/OGR/OSR, laspy.
- **Key findings**:
  1. Coordinate System: Origin (0,0,0) = D96TM [468498 E, 99466 N], WGS84 [46.034276 N, 14.592945 E]. Cartesian limits [-2048, 2048] for X and Z. BF2 +X is East, +Z is North, +Y is Elevation. Focal Point (0, 1365) = D96TM [468498 E, 100831 N] / WGS84 [46.046559 N, 14.592945 E].
  2. Heightmap Sampling: `Heightmap.raw` is 2049x2049 uint16 little-endian (8,396,802 bytes, 0 header). Row 0 is South (Z = -2048m, Northing 97418m); Row 2048 is North (Z = +2048m, Northing 101514m); Col 0 is West (X = -2048m, Easting 466450m); Col 2048 is East (X = +2048m, Easting 470546m). Formula: $u = (X + 2048)/2$, $v = (Z + 2048)/2$. Elevation $Y = \text{uint16} \times 0.01\text{m}$.
  3. OSM Building Extraction: Bounding box [46.015750 N, 14.566437 E] to [46.052791 N, 14.619621 E]. Downloadable via official OSM 0.6 API in 4 quadrants (NW, NE, SW, SE) in ~1-2s each. Polygon centroids, longest-edge yaw, and ground elevation Y calculated cleanly.
  4. LiDAR Canopy Processing: 25 nDMP GeoTIFFs (2000x2000 0.5m Int16) on Flycom asset server; sequential rate-limited download required due to HTTP 429. Resampling and classification into 3-4 density channels (high forest >12m, woodland 5-12m, shrubs 1.5-5m, grass).
- **Unexplored areas**: None remaining for this survey.

## Key Decisions Made
- Confirmed row 0 is South (Z = -2048m) and col 0 is West (X = -2048m) by cross-referencing elevation values against raw LAZ point clouds at multiple benchmark points (SW ridge 451.32m, N center 276.71m, West 294.01m, East 322.72m).
- Recommended 4-quadrant official OSM 0.6 API download as primary strategy (fastest, zero rate-limit issues, 100% reliable) with Overpass API and Geofabrik country extract as secondary backups.

## Artifact Index
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/DISPATCH.md — Received task specifications
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/BRIEFING.md — Persistent state and identity
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/progress.md — Liveness heartbeat and step tracking
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md — Final 5-component report

