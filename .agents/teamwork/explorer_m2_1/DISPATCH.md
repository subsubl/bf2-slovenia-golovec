# Dispatch: Milestone 2 - Explorer 1 (LiDAR GeoTIFF Download & Throttling Strategy)

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Survey References:
  - Workspace Assets: /home/ator/BF2/.agents/teamwork/explorer_survey_1/handoff.md
  - Geospatial Pipeline: /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md
- Working Directory: /home/ator/BF2/.agents/teamwork/explorer_m2_1
- Identity: teamwork_explorer
- Role: LiDAR Download Strategist

## Objective
Formulate the exact tile acquisition and caching strategy for the 25 LiDAR canopy height GeoTIFFs (nDMP) from `tiles_manifest.json`:
1. Inspect `tiles_manifest.json` and remote Flycom URLs (`ndmp_url`).
2. Design a robust sequential download loop with rate limiting (1.2–1.5s delay) and exponential backoff retry to handle `HTTP 429 Too Many Requests`.
3. Design caching in `/home/ator/BF2/ndmp/` to ensure idempotence.
4. Verify disk space safety (25 files ~ 250 MB; ensure no temporary bloat exceeds 2.1 GB free space).
5. Provide a tested Python module/routine for the Worker in `handoff.md`. Do NOT write implementation files in the project workspace directly.

## 2026-11-11T01:15:48Z
You are teamwork_explorer assigned to Milestone 2 - Explorer 1 (LiDAR GeoTIFF Download & Throttling Strategy).
Your working directory is /home/ator/BF2/.agents/teamwork/explorer_m2_1.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/explorer_m2_1/DISPATCH.md before starting.
Also review the survey handoffs at:
- /home/ator/BF2/.agents/teamwork/explorer_survey_1/handoff.md
- /home/ator/BF2/.agents/teamwork/explorer_survey_geo/handoff.md

Investigate and design the tile acquisition and caching strategy for the 25 nDMP canopy GeoTIFFs from tiles_manifest.json:
1. Inspect remote Flycom URLs and test rate-limiting / retry backoff logic (preventing HTTP 429).
2. Design caching in /home/ator/BF2/ndmp/.
3. Verify disk budget safety (ensure 250MB does not cause disk exhaustion).
4. Provide verified Python implementation routines in handoff.md. Do NOT modify or create implementation files in the project workspace directly.
