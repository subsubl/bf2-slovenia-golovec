# Dispatch: Milestone 2 - Forensic Auditor (`auditor_m2`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Worker Handoff: `/home/ator/BF2/.agents/teamwork/worker_m2/handoff.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/auditor_m2`
- Identity: `teamwork_auditor`
- Role: `Forensic Integrity Auditor`

## Audit Focus & Hard Invariants
Perform an exhaustive forensic audit on the Milestone 2 deliverables:
1. **Source Authenticity & Lineage**:
   - Verify that `ndmp/` contains all 25 genuine GeoTIFFs downloaded from the remote Flycom URLs specified in `tiles_manifest.json`.
   - Verify file sizes, GeoTIFF tags, dimensions ($2000 \times 2000$), and projections.
   - Verify `scripts/process_lidar_canopy.py` is genuine logic, not hardcoded test bypasses or canned values.
2. **Output Integrity**:
   - Verify `levels/slovenia_golovec/Overgrowth/Overgrowth.raw` is genuinely generated from the GeoTIFF canopy heights via the transformation pipeline, not fabricated or hardcoded.
   - Verify that test assertions in `test_tier2_boundary_corner.py` pass genuinely due to real data rather than mocks or overrides.
3. **Absence of Cheating**:
   - Ensure no hardcoded outputs, mock test files, monkey-patched functions, or dummy facades.
   - Ensure full byte-for-byte reproducibility of `Overgrowth.raw`.
4. Deliver your binary verdict (`CLEAN` or `INTEGRITY VIOLATION`) with complete forensic evidence in `handoff.md` and report via send_message.

## 2026-11-11T01:37:21Z
You are teamwork_auditor assigned to Milestone 2 - Forensic Auditor (auditor_m2).
Your working directory is /home/ator/BF2/.agents/teamwork/auditor_m2.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/auditor_m2/DISPATCH.md before starting work.
Also study the worker's handoff report at /home/ator/BF2/.agents/teamwork/worker_m2/handoff.md.

Perform an exhaustive forensic integrity audit on Milestone 2 deliverables:
1. Source Authenticity: Verify that the 25 GeoTIFFs in /home/ator/BF2/ndmp/ are genuinely from Flycom URLs, with genuine dimensions (2000x2000), file sizes, and metadata.
2. Logic Authenticity: Verify that scripts/process_lidar_canopy.py genuinely performs data extraction, window placement, downsampling, and classification (no hardcoded outputs, fake files, or canned data).
3. Output Authenticity: Verify that Overgrowth.raw is byte-for-byte reproducible from the input GeoTIFFs.
4. Absence of Integrity Violations: Check for hardcoding, monkey-patching, or bypasses.

Deliver your binary audit verdict (CLEAN or INTEGRITY VIOLATION) in handoff.md and report back via send_message.
