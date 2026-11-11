# Battlefield 2 — Slovenia Golovec (`slovenia_golovec`)

Authentic real-world **Battlefield 2 (Refractor 2 Engine)** level for SE Ljubljana / Golovec, Slovenia ($46.046559^\circ\text{ N}, 14.592945^\circ\text{ E}$), built from 1 m ARSO LiDAR elevation data (`https://clss.si/`), DOF aerial orthophotography, and OpenStreetMap building footprints.

## Contents

- **`levels/slovenia_golovec/`** — Packaged Battlefield 2 level ready to drop into `mods/bf2/Levels/slovenia_golovec/`:
  - `client.zip` — Compiled `terraindata.raw` (64 primary `QuadPatch` vertex buffers + LOD morph deltas + packed normals, 8 `SurroundingPatch` blocks, and 5,461 frustum-culling/LOD quadtree bounding boxes), 64+8 DXT1 orthophoto `Colormaps/`, 64 LiDAR relief `Lightmaps/`, `Detailmaps/`, `LowDetailmaps/`, and HUD minimap (`ingameMap.dds`).
  - `server.zip` — `HeightmapPrimary.raw` (`1025x1025` 16-bit DEM, `266.67 m – 451.32 m`), `HeightmapPrimary.mat`, `StaticObjects.con` (1,234 grounded OpenStreetMap buildings), `GameplayObjects.con` (Conquest 16/32/64 & Coop 16), `Heightdata.con`, `Terrain.con`, `Water.con`, `Sky.con`, and `Init.con`.
  - `Info/` — Level descriptor (`slovenia_golovec.desc`) and menu/loadscreen maps.
- **`Heightmap.raw`** & **`ColorMap_preview.png`** — Full-resolution $2049 \times 2049$ 16-bit LiDAR elevation grid ($0.01\text{ m}$ vertical scale) and $4096 \times 4096$ aerial orthophoto.
- **`scripts/`** — Terrain, colormap, OSM building, overgrowth, and binary `terraindata.raw` compilation scripts (`scripts/compile_slovenia_golovec.py`).
- **`tests/`** — 225 automated unit and integration tests verifying terrain geometry, heightmap continuity, DDS headers, and Refractor 2 `.con` integrity.

## Installation

Copy `levels/slovenia_golovec/client.zip`, `levels/slovenia_golovec/server.zip`, and `levels/slovenia_golovec/Info/` into your Battlefield 2 installation:

```bash
mkdir -p "/path/to/Battlefield 2/mods/bf2/Levels/slovenia_golovec"
cp -r levels/slovenia_golovec/{client.zip,server.zip,Info} "/path/to/Battlefield 2/mods/bf2/Levels/slovenia_golovec/"
```

## Running Tests

```bash
pytest -q
```
