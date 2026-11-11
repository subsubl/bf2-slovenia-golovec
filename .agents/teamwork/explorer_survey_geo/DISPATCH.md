# Dispatch: Survey 3 - Geospatial Pipeline & Heightmap Sampling

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Working Directory: /home/ator/BF2/.agents/teamwork/explorer_survey_geo
- Identity: teamwork_explorer
- Role: Geospatial Data Researcher

## Objective
Investigate and design the geospatial transformation & sampling pipelines for the Golovec map:
1. Coordinate transformations:
   - Origin (0, 0, 0) maps to D96TM [468498 E, 99466 N] and WGS84 [46.034276 N, 14.592945 E].
   - Map bounds: 4096m x 4096m, Cartesian limits [-2048, 2048] for X and Z.
   - Golovec focal point: WGS84 [46.046559 N, 14.592945 E]. Convert this to D96TM and Cartesian (X, Z).
   - D96TM (EPSG:3794) to Cartesian (X, Z) and WGS84 (EPSG:4326) mapping formulas. Notice BF2 convention: X is East-West or North-South? And Z is North-South or East-West? Clarify standard BF2 terrain grid orientation.
2. Heightmap ground elevation sampling:
   - `Heightmap.raw`: 2049x2049 uint16 little-endian, 2.0m grid spacing, heightScale 0.01.
   - Sampling formula: given Cartesian (X, Z) in [-2048, 2048], how to map to pixel (col, row) in the 2049x2049 grid, read uint16 elevation, and convert via heightScale 0.01 to Y in meters.
3. OSM building extraction:
   - Methods to extract building footprints in the 4096m x 4096m bounding box around Golovec (e.g. Overpass API, local cache, osmnx, shapefiles).
   - Building polygon centroids/orientations and bounding box limits.
4. LiDAR canopy processing:
   - Check `tiles_manifest.json`, download/process canopy height GeoTIFFs (nDMP).
   - How to rasterize/resample canopy heights to terrain dimensions and generate overgrowth density masks.


## 2026-11-11T00:38:45Z
You are teamwork_explorer assigned to Survey 3 - Geospatial Pipeline & Heightmap Sampling.
Your working directory is /home/ator/BF2/.agents/teamwork/explorer_survey_geo.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md and /home/ator/BF2/.agents/teamwork/explorer_survey_geo/DISPATCH.md before starting.

Investigate and specify the geospatial transformation and sampling pipelines for the Golovec map:
1. Coordinate transformations:
   - Origin (0, 0, 0) maps to D96TM [468498 E, 99466 N] and WGS84 [46.034276 N, 14.592945 E].
   - Map bounds: 4096m x 4096m, Cartesian limits [-2048, 2048] for X and Z.
   - Golovec focal point: WGS84 [46.046559 N, 14.592945 E]. Convert this to D96TM and Cartesian (X, Z).
   - D96TM (EPSG:3794) to Cartesian (X, Z) and WGS84 (EPSG:4326) mapping formulas. Check how BF2 X and Z align with Easting and Northing.
2. Heightmap ground elevation sampling:
   - `Heightmap.raw`: 2049x2049 uint16 little-endian, 2.0m grid spacing, heightScale 0.01.
   - Sampling formula: given Cartesian (X, Z) in [-2048, 2048], how to map to pixel (col, row) in the 2049x2049 grid, read uint16 elevation, and convert via heightScale 0.01 to Y in meters.
3. OSM building extraction:
   - Methods to extract building footprints in the 4096m x 4096m bounding box around Golovec (e.g. Overpass API, local cache, osmnx, shapefiles).
   - Building polygon centroids/orientations and bounding box limits.
4. LiDAR canopy processing:
   - Check `tiles_manifest.json`, download/process canopy height GeoTIFFs (nDMP).
   - How to rasterize/resample canopy heights to terrain dimensions and generate overgrowth density masks.
Record your findings in handoff.md in your working directory and notify me when complete. Do not modify or write source files.
