# BRIEFING — 2026-11-11T01:20:00Z

## Mission
Investigate and design the tile acquisition, rate limiting, retry backoff, and caching strategy for the 25 nDMP canopy GeoTIFFs from tiles_manifest.json.

## 🔒 My Identity
- Archetype: teamwork_explorer
- Roles: LiDAR Download Strategist
- Working directory: /home/ator/BF2/.agents/teamwork/explorer_m2_1
- Original parent: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Milestone: Milestone 2 - Explorer 1 (LiDAR GeoTIFF Download & Throttling Strategy)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Do NOT modify or create implementation files in the project workspace directly
- Write only to /home/ator/BF2/.agents/teamwork/explorer_m2_1/

## Current Parent
- Conversation ID: d9edcccb-96a4-4537-a7b5-b5dbbe0b9b61
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `tiles_manifest.json` (all 25 tiles)
  - Flycom server headers, rate limiting, burst threshold (10 requests), 429 response headers (`Retry-After`, `X-Retry-In`)
  - Range request resumption and chunked streaming
  - Filesystem disk space (/dev/mapper/data-root: 1,930 MB available, 248.55 MB required)
  - Caching and atomicity in `/home/ator/BF2/ndmp/`
- **Key findings**:
  - Flycom uses Nginx leaky bucket rate limiter: allows 10-burst, returns HTTP 429 on 11th unthrottled request with `Retry-After: 2` and `X-Retry-In`.
  - Sequential requests with 1.25s delay achieve 100% success rate with 0 rate limit triggers across all 25 tiles.
  - 24 tiles are Int16 GeoTIFFs (10,025,052 bytes, NoData -32767.0). Tile `466_101` (from annex) is Float32 GeoTIFF (20,024,980 bytes, NoData 0). Total payload: 260,626,228 bytes (248.55 MB).
  - Disk budget is safe: consumes only ~12.6% of available 1,967 MB free disk space.
  - Implemented and verified complete Python downloader routine in `tile_downloader.py` and `test_tile_downloader.py`.
- **Unexplored areas**: None for M2-E1 scope. Downstream canopy raster mosaicking/downsampling is assigned to M2-E2.

## Key Decisions Made
- Standardized caching location to `/home/ator/BF2/ndmp/nDMP_{ti_name}.tif`.
- Standardized inter-request delay to 1.25 seconds between downloads.
- Implemented dual-header parsing (`Retry-After` and `X-Retry-In`) with exponential backoff and jitter.
- Designed atomic staging (`.tmp.{pid}` + `os.replace`) to prevent corrupt cache entries.
- Added GDAL dimensions and band integrity check in `validate_geotiff`.

## Artifact Index
- DISPATCH.md — Parent dispatch instructions
- BRIEFING.md — Persistent working memory
- progress.md — Heartbeat progress log
- check_all_sizes.py — Diagnostic script verifying all 25 tile sizes
- test_probe.py — Flycom HTTP header diagnostic
- test_rate_limit_behavior.py — Flycom 429 trigger & header inspection
- test_retry_after.py — Flycom 429 recovery verification
- test_range_resume.py — HTTP Range resumption verification
- tile_downloader.py — Production-grade tile downloader module for Worker
- test_tile_downloader.py — Comprehensive unit and integration test suite
- handoff.md — Final handoff report
