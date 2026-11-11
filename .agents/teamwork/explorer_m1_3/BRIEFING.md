# BRIEFING — 2026-11-11T01:00:00Z

## Mission
Formulate static mesh mapping rules and StaticObjects.con formatting specification for BF2 European map generation.

## 🔒 My Identity
- Archetype: teamwork_explorer
- Roles: Static Mesh Mapping Strategist
- Working directory: /home/ator/BF2/.agents/teamwork/explorer_m1_3
- Original parent: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Milestone: Milestone 1 - Explorer 3

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Do NOT modify or create implementation files in the project workspace directly
- All output in /home/ator/BF2/.agents/teamwork/explorer_m1_3/

## Current Parent
- Conversation ID: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Updated: 2026-11-11T01:00:00Z

## Investigation State
- **Explored paths**:
  - `ORIGINAL_REQUEST.md`, `PROJECT.md`, `spec_miner_bf2/handoff.md`, `explorer_survey_geo/handoff.md`
  - Real-world OSM building footprints in Golovec bounding box (4096m x 4096m)
  - `Heightmap.raw` elevation sampling and water table grounding (270.0m)
- **Key findings**:
  - Raw OSM count in $[-2048, 2048]$ is 4,207 buildings. Unthrottled placement exceeds BF2 draw-call/memory budgets and creates mesh clipping.
  - Spatial thinning with $R = 30\text{ m}$ produces ~1,375 buildings, perfectly matching the 500-1,500 target budget while preventing mesh collisions.
  - Standard BF2 vanilla European catalog identified: urban (`eu_building01`, `eu_building02`, `eu_office_01`, `me_apartment_01`, `citybuilding_01`), suburban (`eu_house_01`, `eu_house_02`, `me_house_01` to `me_house_06`), rural/industrial (`barn_01`, `barn_02`, `farmhouse`, `wooden_shed`, `shed_01`, `warehouse_01`).
  - `StaticObjects.con` requires Refractor 2 editor blocks `if v_arg1 == BF2Editor`, `Object.create`, `Object.absolutePosition X/Y/Z` (slash-delimited, NO spaces, 3-decimal precision), `Object.rotation Yaw/Pitch/Roll`, `Object.layer 1`.
  - OSM API throttles rapid repeated calls (HTTP 429), necessitating 1.5s delay and caching.
- **Unexplored areas**: None within scope.

## Key Decisions Made
- Standardized mesh mapping taxonomy with explicit priority ordering and area/level fallbacks.
- Recommended 30m spatial thinning radius to balance density, performance, and collision avoidance.
- Enforced minimum elevation clamp $Y \ge 270.0\text{ m}$ to prevent flooded/submerged static meshes.

## Artifact Index
- `/home/ator/BF2/.agents/teamwork/explorer_m1_3/DISPATCH.md` — Incoming task assignments
- `/home/ator/BF2/.agents/teamwork/explorer_m1_3/BRIEFING.md` — Persistent agent state
- `/home/ator/BF2/.agents/teamwork/explorer_m1_3/progress.md` — Liveness heartbeat and milestone tracking
- `/home/ator/BF2/.agents/teamwork/explorer_m1_3/handoff.md` — Authoritative Static Mesh Mapping & StaticObjects.con Specification
