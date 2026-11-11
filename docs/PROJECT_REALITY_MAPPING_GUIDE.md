# Project Reality (PR:BF2) Mapping & Engine Reference Guide

Extracted and synthesized from the official **Project Reality Documentation (`RealityDocs`)** in [`docs/project_reality/`](file:///home/ator/BF2/docs/project_reality/).

---

## 1. Terrain Lightmaps: Sun, Sky & Water Transparency (`tutorials/lightmapping/page14.rst` – `page17.rst`)

Unlike static object lightmaps (where RGB = Point, Sun, Sky), **Battlefield 2 terrain lightmaps** (`Lightmaps/tx00x00.dds` .. `tx07x07.dds`) use a specialized channel encoding:

| Channel | Purpose | PR Standard (`page14.rst` – `page16.rst`) |
|---|---|---|
| **Red (`R`)** | **Sea Water Depth / Transparency** | Controls water opacity based on depth below `seaWaterLevel`. At `0`, water is transparent at the shoreline; ramps up to `255` (fully opaque) at `~3.5 m – 4.5 m` depth (`Near Attenuation End = 3.5m`). Must be `0` on dry land. |
| **Green (`G`)** | **Direct Sunlight (`Sun`)** | Directional sun diffuse + cast shadows. **Crucial (`page14.rst`):** All terrain vertices below `seaWaterLevel` must be flattened to `seaWaterLevel` before baking Sun/Sky lightmaps so shadows/normals are cast onto the flat water surface rather than the riverbed. |
| **Blue (`B`)** | **Sky / Ambient Light (`Sky`)** | Hemisphere sky diffuse / ambient occlusion. |

- **Resolution (`page14.rst`):** Standard terrain lightmap density is `2 pixels/meter` (`4096 x 4096` split into `64` `512 x 512` DXT1 tiles with 10 mipmaps for a 2 km map).
- **Orientation (`page17.rst`):** Full-map lightmaps and colormaps must be flipped vertically (`Flip Canvas Vertical`, South at row 0) before splitting into `tx00x00.dds` .. `tx07x07.dds`, then each tile flipped back or indexed South-to-North so patch `(0,0)` is SW and `(7,7)` is NE.
- **Flat Patch Optimization (`page17.rst`):** Any lightmap tile that is uniform in color can be downsized from `512 x 512` (`683 KB` in RAM) to `8 x 8` DXT1 (`0.1 KB`), saving up to `30 MB` of 32-bit client RAM.

---

## 2. Minimap Engineering (`tutorials/minimaps.rst`)

- **Water Level Offset Bug (`minimaps.rst`):** When BF2's editor renders a minimap, water renders `1.0 m` higher than in-game, flooding shorelines on the minimap unless `Sea Water Level` is lowered by `1.0 m` during minimap capture.
- **High-Res `ingameMap.dds` Without Mipmaps:**
  - Vanilla BF2 saves `Hud/Minimap/ingameMap.dds` at `512 x 512` DXT1 with 10 unused mipmaps (`170 KB`).
  - Project Reality saves `Hud/Minimap/ingameMap.dds` at **`1024 x 1024` (or `2048 x 2048` for 4 km maps) DXT1 with NO mipmaps (`1` mipmap = `512 KB`)**, giving 4×–16× sharper tactical map detail.
  - Unused legacy files `commanderMap.dds` and `commanderMicromap.dds` must **not** be deleted (can cause CTDs), but should be resized to `32 x 32` DXT1 (`1 KB` each).

---

## 3. Overgrowth & Undergrowth Architecture (`tutorials/overgrowth.rst`, `easyovergrowth.rst`, `overgrowthsimplified.rst`, `atlasogug.rst`)

1. **Synchronizing `Undergrowth.raw` & `Overgrowth.raw` (`easyovergrowth.rst`):**
   - Both `Undergrowth.raw` (grass/small plants) and `Overgrowth/Overgrowth.raw` (trees/shrubs) use identical `1025 x 1025` `uint8` material ID grids (`0..15`).
   - Copying `Undergrowth.raw` to `Overgrowth/Overgrowth.raw` with matching material ID slots (`1`, `2`, `3`) automatically synchronizes forest floor grass with tree canopies.
2. **Three-Zone Woodland Placement (`overgrowth.rst`):**
   - Instead of uniform high-density forest (e.g., *Fools Road* with `23,194` OG objects), PR uses a 3-layer zoned layout (*Nuijamaa* with `10,059` OG objects—over 50% fewer objects while looking denser):
     - **Material 1 (`woods`):** Interior forest clusters (`density 4–4.5`, low shrub count because canopy blocks sunlight).
     - **Material 2 (`woodsedge`):** Forest perimeter (`10 m – 20 m` transition belt with deciduous trees + high-density shrubs `density 8` where sunlight hits the edge).
     - **Material 3 (`lowplay`):** Thinned density (`density 1.6–1.8`) at map edges and high altitudes.
3. **Static Overgrowth Conversion (`overgrowthsimplified.rst`):**
   - Overgrowth is converted into `OvergrowthCollision.con` / `StaticObjects.con` entries (`Object.isOvergrowth 1`) so tree trunks have server-authoritative physics collision and render in minimap/lightmap passes.
4. **Texture Atlas Packing (`atlasogug.rst`):**
   - `OvergrowthAtlas0.dds` is saved in `DXT5 ARGB` with 10 mipmaps, indexed by `OvergrowthAtlas.tai` (`<filename> <atlas>, <idx>, <u_off>, <v_off>, <width>, <height>`). Solid trunk textures must be separated from alpha-tested leaf textures to prevent mipmap edge bleeding.

---

## 4. Map Scale: 2 km (`Scale 2`) vs 4 km (`Scale 4`) (`tutorials/mapscale.rst`)

- Both 2 km and 4 km BF2 maps use a `1025 x 1025` `uint16` `HeightmapPrimary.raw` (`heightmap.setSize 1025 1025`).
- **2 km × 2 km (`Scale 2`):**
  - `heightmapcluster.setHeightmapSize 2048`
  - `heightmap.setScale 2/<y_scale>/2`
  - `terrain.primaryWorldScale 2/<y_scale>/2`
- **4 km × 4 km (`Scale 4`):**
  - `heightmapcluster.setHeightmapSize 4096`
  - `heightmap.setScale 4/<y_scale>/4`
  - `terrain.primaryWorldScale 4/<y_scale>/4`

---

## 5. Custom Map-Local Object & Texture Archives (`customzip.rst`)

Maps can ship custom static objects, road intersections, or textures **without modifying base `mods/bf2/` archives**:
- Create `objects_client.zip` (`.staticmesh`, `.bundledmesh`, `.dds`, `.ogg`) and `objects_server.zip` (`.collisionmesh`, `.con`, `.tweak`) inside `Levels/<map_name>/`.
- Mount them by adding `ClientArchives.con` and `ServerArchives.con` inside the level's `server.zip`:
  ```con
  fileManager.mountArchive Levels/slovenia_golovec/objects_server.zip Objects
  fileManager.mountArchive Levels/slovenia_golovec/objects_client.zip Objects
  ```

---

## 6. View Distance & Vehicle Sound Bug (`soundbug.rst`) & Sizing Standards (`guides/sizing_guide.rst`)

- **Minimum View Distance (`soundbug.rst`):** If `GameLogic.MaximumLevelViewDistance` / `Renderer.fogStartEndAndBase` is smaller than the network cull distance of active vehicles, players hear full-volume engine sounds from invisible vehicles:
  - Light vehicles: `>= 300 m`
  - Tanks / APCs: `>= 600 m`
  - Helicopters: `>= 800 m`
  - Jets: `>= 1000 m`
- **Player & Traversal Dimensions (`guides/sizing_guide.rst`):**
  - Standing passage height: `>= 1.7 m` (doorways: `2.0 m × 1.0 m`).
  - Max climbable terrain slope: `< 40°` normal (`~45°` absolute max before sliding).
  - Cover heights: `0.6 m` prone, `1.3 m` crouched, `1.7 m` standing.
  - Firing-over heights: `0.35 m` prone, `0.85 m` crouched, `1.32 m` standing.
