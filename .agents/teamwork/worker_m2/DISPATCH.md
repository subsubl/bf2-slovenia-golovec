# Dispatch: Milestone 2 - Worker (`worker_m2`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/worker_m2`
- Identity: `teamwork_worker`
- Role: `Overgrowth Pipeline Implementer`

## Write Ownership
You have exclusive write ownership of:
- `/home/ator/BF2/scripts/process_lidar_canopy.py`
- `/home/ator/BF2/ndmp/`
- `/home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con`
- `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw`
- Your working directory: `/home/ator/BF2/.agents/teamwork/worker_m2/`

Do NOT modify any other files outside your write ownership.

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Implement and execute the complete LiDAR canopy processing pipeline and OvergrowthSystem configuration:
1. Read the comprehensive exploration reports:
   - `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
   - `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
   - `/home/ator/BF2/.agents/teamwork/explorer_m2_1/handoff.md` (tile downloader, rate limiting, retry backoff)
   - `/home/ator/BF2/.agents/teamwork/explorer_m2_2/handoff.md` (direct window placement, Float32/Int16 handling, PIL bilinear downsampling, South-to-North orientation flip, density mask)
   - `/home/ator/BF2/.agents/teamwork/explorer_m2_3/handoff.md` (OvergrowthSystem.con template, 7 vanilla BF2 species)

2. Create `/home/ator/BF2/scripts/process_lidar_canopy.py`:
   - Incorporate the rate-limited sequential downloader with 1.25s delay and exponential backoff to fetch the 25 nDMP GeoTIFFs from `tiles_manifest.json` into `/home/ator/BF2/ndmp/`.
   - Incorporate the direct window placement into an $(8192, 8192)$ float32 canvas ($268\text{ MB}$ RAM).
   - Correctly handle tile `466_101` (`Float32`, NoData `0.0`) vs the other 24 tiles (`Int16`, NoData `-32767.0`).
   - Resample from $(8192, 8192)$ 0.5m grid to $(2049, 2049)$ 2.0m terrain grid via PIL Bilinear.
   - Flip vertically (`np.flipud`) so Row 0 is South ($Z = -2048$) and Row 2048 is North ($Z = +2048$).
   - Apply canopy thresholding and density classification ($H < 1.5\text{ m} \to 0$; $1.5\text{ m} \le H \le 20.0\text{ m} \to \text{round}((H - 1.5)/18.5 \times 255)$; $H > 20.0\text{ m} \to 255$).
   - Ensure output directory `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/` exists and write `/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw` ($2049 \times 2049 = 4,198,401$ bytes uint8, zero header).

3. Create `/home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con` using the verified Refractor 2 template from `explorer_m2_3/handoff.md`.

4. Execute the pipeline to download all tiles and generate the artifacts.

5. Run test verification:
   ```bash
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier1_feature_coverage.py -k overgrowth
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier2_boundary_corner.py -k overgrowth
   PYTHONPATH=tests python3 -m unittest -v tests/test_tier3_cross_feature.py -k overgrowth
   ```

6. Deliver your completion report in `/home/ator/BF2/.agents/teamwork/worker_m2/handoff.md` and send a completion message to the orchestrator.

## 2026-11-11T01:28:46Z
You are teamwork_worker assigned to Milestone 2 - LiDAR Canopy Processing & OvergrowthSystem.con.
Your working directory is /home/ator/BF2/.agents/teamwork/worker_m2.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/worker_m2/DISPATCH.md before starting work.
Also study the handoff reports from the three M2 explorers:
- /home/ator/BF2/.agents/teamwork/explorer_m2_1/handoff.md (tile acquisition, rate limiting, retry backoff)
- /home/ator/BF2/.agents/teamwork/explorer_m2_2/handoff.md (direct window placement, data type normalization, PIL bilinear resampling, orientation flip, density mask)
- /home/ator/BF2/.agents/teamwork/explorer_m2_3/handoff.md (Refractor 2 OvergrowthSystem.con template, 7 vanilla species)

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Implement /home/ator/BF2/scripts/process_lidar_canopy.py, execute it to download the 25 nDMP GeoTIFFs into /home/ator/BF2/ndmp/ and generate /home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw (4,198,401 bytes uint8, row 0 South to row 2048 North).
Create /home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con.
Run all overgrowth tests across test_tier1_feature_coverage.py, test_tier2_boundary_corner.py, and test_tier3_cross_feature.py.
Document your results in /home/ator/BF2/.agents/teamwork/worker_m2/handoff.md and report back via send_message.

