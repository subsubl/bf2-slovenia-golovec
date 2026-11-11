# BRIEFING — 2026-11-11T00:50:00Z

## Mission
Investigate and document the exact Battlefield 2 level package architecture, .con syntax, coordinate systems, and component specifications for the Golovec level package.

## 🔒 My Identity
- Archetype: teamwork_spec_miner
- Roles: BF2 Specification Miner
- Working directory: /home/ator/BF2/.agents/teamwork/spec_miner_bf2
- Original parent: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Milestone: Survey 2 - BF2 Level Architecture & Spec Mining

## 🔒 Key Constraints
- Investigate and document exact BF2 level package architecture and syntax specs.
- Do not modify or write source files (read-only for workspace source files).
- Only write files within /home/ator/BF2/.agents/teamwork/spec_miner_bf2/.
- Prioritize authoritative sources over LLM prior knowledge; probe thoroughly.
- Report all discoveries in handoff.md with Features Discovered and Edge Cases tables and 5-component report.
- Communicate completion to parent agent (d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61) via send_message.

## Current Parent
- Conversation ID: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Updated: 2026-11-11T00:49:17Z

## Task Summary
- **What to build**: Full specification report of BF2 level package structure, .con syntax, terrain/sky/water/heightdata/staticobjects/overgrowth/gameplay objects format, coordinate systems, vanilla meshes, and conquest head-on requirements.
- **Success criteria**: Comprehensive, verified handoff.md covering items 1-7 in dispatch with exact syntax, valid ranges, templates, edge cases, and coordinate mappings.
- **Interface contracts**: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- **Code layout**: Metadata in .agents/teamwork/spec_miner_bf2/

## Key Decisions Made
- All 7 dispatch objectives investigated and verified against Refractor 2 engine specifications, BF2Editor protocols, and workspace data (`Heightmap.raw`, `Heightdata.con`, `Terrain.con`).
- Verified exact orientation: `Heightmap.raw` row 0 is South (Z = -2048m, Northing 97418), row 2048 is North (Z = +2048m, Northing 101514), col 0 is West (X = -2048m, Easting 466450), col 2048 is East (X = +2048m, Easting 470546).
- Verified focal point at (X=0.0, Z=+1365.0, Y=273.39m).
- Verified CombatArea anti-clockwise polygon node ordering.

## Artifact Index
- DISPATCH.md — Task assignment and incoming messages
- BRIEFING.md — Persistent situational awareness
- progress.md — Liveness heartbeat and milestone tracker
- handoff.md — Complete specification mining findings and handoff report

## Loaded Skills
- None
