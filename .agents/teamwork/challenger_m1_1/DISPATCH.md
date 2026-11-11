# Dispatch: Milestone 1 - Challenger 1

- Original Request: /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md
- Project Scope: /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md
- Worker Handoff: /home/ator/BF2/.agents/teamwork/worker_m1/handoff.md
- Target Artifact: /home/ator/BF2/levels/slovenia_golovec/StaticObjects.con
- Working Directory: /home/ator/BF2/.agents/teamwork/challenger_m1_1
- Identity: teamwork_challenger
- Role: Adversarial Static Objects Verifier

## Objective
Adversarially challenge and stress-test `levels/slovenia_golovec/StaticObjects.con`:
1. Write and execute independent Python stress scripts:
   - Parse every single line and block in `StaticObjects.con`.
   - Verify every object position $(X, Y, Z)$: test for NaN, Inf, out-of-bounds ($X, Z \notin [-2048, 2048]$), underwater placement ($Y < 270.0$), and verify against `Heightmap.raw` bilinear sampling.
   - Test for duplicated coordinates or duplicate instance names.
   - Verify vector formatting: check every single slash delimiter for whitespace (` / ` or `/ ` or ` /`).
2. Document all tests run, results, and provide explicit verdict (`CONFIRM` or `REJECT`) in `handoff.md`.

## 2026-11-11T01:08:01Z
You are teamwork_challenger assigned to Milestone 1 Adversarial Verification 1.
Your working directory is /home/ator/BF2/.agents/teamwork/challenger_m1_1.
Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, /home/ator/BF2/.agents/teamwork/worker_m1/handoff.md, and /home/ator/BF2/.agents/teamwork/challenger_m1_1/DISPATCH.md before starting.

Adversarially challenge levels/slovenia_golovec/StaticObjects.con:
1. Write independent stress testing script to parse every object position (X, Y, Z).
2. Check for NaN, Inf, out-of-bounds outside [-2048, 2048], underwater placement Y < 270.0m, heightmap grounding deviations.
3. Check for whitespace around slash delimiters or malformed syntax.
4. Check for duplicate positions or template names.
5. Record your empirical tests and verdict CONFIRM or REJECT in handoff.md and notify me.
