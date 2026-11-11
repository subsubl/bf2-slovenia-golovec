# Dispatch: Milestone 3 - Challenger 2 (`challenger_m3_2`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Worker Handoff: `/home/ator/BF2/.agents/teamwork/worker_m3/handoff.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/challenger_m3_2`
- Identity: `teamwork_challenger`
- Role: `Adversarial CP-Spawn Topology Verifier`

## Challenge Focus
Empirically stress-test the gameplay topology in `/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con`:
1. Control Point & Spawn Point Linkages:
   - Parse all ControlPoints and SpawnPoints.
   - Verify 1-to-N bijection: every SpawnPoint has `setControlPointId` matching an existing ControlPoint.
   - Every ControlPoint has at least 2 associated SpawnPoints.
2. Elevation Grounding Precision:
   - For every ControlPoint and SpawnPoint $(X, Z)$, perform independent bilinear sampling on `/home/ator/BF2/Heightmap.raw` (2049x2049 uint16, 2.0m spacing, scale 0.01).
   - ControlPoint $Y$ must match terrain ground elevation within $\pm 0.05\text{m}$.
   - SpawnPoint $Y$ must equal terrain ground elevation $+ 1.25\text{m} \pm 0.05\text{m}$ (player mesh collision clearance).
3. Base Balance & Focal Distance:
   - Verify distance from EU base to Golovec Pass is balanced with distance from MEC base to Golovec Pass ($\Delta < 20\%$).
   - Verify bases are located on dry ground above the water table ($Y \ge 270.0\text{m}$).
4. Deliver your empirical confirmation report with verdict (`CONFIRM` or `DISPROVE`) in `handoff.md` and report via send_message.

## 2026-11-11T02:00:01Z
You are teamwork_challenger assigned to Milestone 3 - Challenger 2 (Adversarial CP-Spawn Topology Verifier).
Your working directory is /home/ator/BF2/.agents/teamwork/challenger_m3_2.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/challenger_m3_2/DISPATCH.md before starting work.
Also study the worker's handoff report at /home/ator/BF2/.agents/teamwork/worker_m3/handoff.md.

Adversarially challenge and stress-test the gameplay topology in /home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con:
1. Control Point & Spawn Point Linkages: verify every SpawnPoint has matching setControlPointId on an existing CP.
2. Elevation Grounding Precision: verify independently via Heightmap.raw bilinear sampling that CP Y matches terrain within +-0.05m and SP Y matches terrain + 1.25m within +-0.05m.
3. Base Balance: verify EU and MEC bases have symmetric travel distance to Golovec Pass (Delta < 20%) and are above water table (Y >= 270.0m).
Deliver your empirical stress-test report with verdict (CONFIRM or DISPROVE) in handoff.md and report back via send_message.
