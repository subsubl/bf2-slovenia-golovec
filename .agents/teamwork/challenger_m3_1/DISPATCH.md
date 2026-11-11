# Dispatch: Milestone 3 - Challenger 1 (`challenger_m3_1`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Worker Handoff: `/home/ator/BF2/.agents/teamwork/worker_m3/handoff.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/challenger_m3_1`
- Identity: `teamwork_challenger`
- Role: `Adversarial Combat Area & Desertion Verifier`

## Challenge Focus
Empirically stress-test the Combat Area defined in `/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con`:
1. Polygon Winding:
   - Calculate signed polygon area using Green's theorem / shoelace formula.
   - Assert positive signed area (strictly counter-clockwise winding).
   - Verify that in Refractor 2 engine semantics, this winding marks the interior as valid playable space and exterior as desertion zone (not inverted).
2. Spatial Containment:
   - Verify focal point $(0.0, 1365.0)$ is strictly enclosed.
   - Verify all 3 ControlPoints and all 6 SpawnPoints are strictly inside the combat area with safe margin (> 50m from combat boundary).
3. Coordinate Limits:
   - All combat area vertices must lie strictly within $[-2048.0, 2048.0]$.
4. Deliver your empirical confirmation report with verdict (`CONFIRM` or `DISPROVE`) in `handoff.md` and report via send_message.

## 2026-11-11T01:59:56Z
You are teamwork_challenger assigned to Milestone 3 - Challenger 1 (Adversarial Combat Area & Desertion Verifier).
Your working directory is /home/ator/BF2/.agents/teamwork/challenger_m3_1.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/challenger_m3_1/DISPATCH.md before starting work.
Also study the worker's handoff report at /home/ator/BF2/.agents/teamwork/worker_m3/handoff.md.

Adversarially challenge and stress-test the Combat Area in /home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con:
1. Polygon Winding: Assert positive signed area (counter-clockwise winding) preventing instant 10-second desertion bug.
2. Spatial Containment: Assert focal point (0, 1365) is strictly enclosed. Assert all 3 CPs and 6 SPs are inside combat boundary with safe margin.
3. Coordinate bounds: all vertices in [-2048.0, 2048.0].
Deliver your empirical stress-test report with verdict (CONFIRM or DISPROVE) in handoff.md and report back via send_message.
