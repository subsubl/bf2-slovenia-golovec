# Dispatch: Milestone 3 - Worker (`worker_m3`)

- Original Request: `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
- Project Scope: `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
- Working Directory: `/home/ator/BF2/.agents/teamwork/worker_m3`
- Identity: `teamwork_worker`
- Role: `Level Package Assembler`

## Write Ownership
You have exclusive write ownership of:
- `/home/ator/BF2/scripts/assemble_level_package.py`
- `/home/ator/BF2/levels/slovenia_golovec/init.con`
- `/home/ator/BF2/levels/slovenia_golovec/Heightdata.con`
- `/home/ator/BF2/levels/slovenia_golovec/Terrain.con`
- `/home/ator/BF2/levels/slovenia_golovec/Sky.con`
- `/home/ator/BF2/levels/slovenia_golovec/Water.con`
- `/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con`
- `/home/ator/BF2/levels/slovenia_golovec/Heightmap.raw` (hardlink)
- `/home/ator/BF2/levels/slovenia_golovec/ColorMap.dds` (hardlink)
- Your working directory: `/home/ator/BF2/.agents/teamwork/worker_m3/`

Note: Do NOT modify existing `StaticObjects.con`, `OvergrowthSystem.con`, or `Overgrowth/Overgrowth.raw` which were generated in M1 and M2.

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective
Assemble the complete level directory structure under `/home/ator/BF2/levels/slovenia_golovec/` and configure gameplay objects:
1. Read the comprehensive exploration reports:
   - `/home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md`
   - `/home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md`
   - `/home/ator/BF2/.agents/teamwork/spec_miner_m3/handoff.md` (exact templates for init.con, Terrain.con, Heightdata.con, Sky.con, Water.con)
   - `/home/ator/BF2/.agents/teamwork/explorer_m3_gameplay/handoff.md` and `/home/ator/BF2/.agents/teamwork/explorer_m3_gameplay/proposed_GameplayObjects.con` (Conquest Head-On EU vs MEC, 3 CPs, 6 SPs, CCW combat area)
   - `/home/ator/BF2/.agents/teamwork/explorer_m3_packaging/handoff.md` (packaging routine, hardlinking Heightmap.raw/ColorMap.dds, init.con conductor)

2. Create `/home/ator/BF2/scripts/assemble_level_package.py`:
   - Automates the assembly of all configuration files in `levels/slovenia_golovec/`.
   - Links or creates `Heightmap.raw` and `ColorMap.dds`.
   - Writes `init.con`, `Heightdata.con`, `Terrain.con`, `Sky.con`, `Water.con`, and `GameplayObjects.con`.

3. Execute the assembly script to instantiate all configuration files.

4. Run the full test suite to verify:
   ```bash
   python3 /home/ator/BF2/tests/verify_bf2_level.py -v
   ```
   Assert that all 88 tests pass with exit code 0.

5. Deliver your completion report in `/home/ator/BF2/.agents/teamwork/worker_m3/handoff.md` and send a message to the orchestrator.

## 2026-11-11T01:53:29Z
You are teamwork_worker assigned to Milestone 3 - Level Package Assembly & Gameplay Configuration.
Your working directory is /home/ator/BF2/.agents/teamwork/worker_m3.

MANDATORY: Read /home/ator/BF2/.agents/teamwork/ORIGINAL_REQUEST.md, /home/ator/BF2/.agents/teamwork/orchestrator/PROJECT.md, and /home/ator/BF2/.agents/teamwork/worker_m3/DISPATCH.md before starting work.
Also study the handoff reports from the three M3 explorers:
- /home/ator/BF2/.agents/teamwork/spec_miner_m3/handoff.md (templates for init.con, Terrain.con, Heightdata.con, Sky.con, Water.con)
- /home/ator/BF2/.agents/teamwork/explorer_m3_gameplay/handoff.md and /home/ator/BF2/.agents/teamwork/explorer_m3_gameplay/proposed_GameplayObjects.con (gameplay setup)
- /home/ator/BF2/.agents/teamwork/explorer_m3_packaging/handoff.md (packaging routine, hardlinking, test suite alignment)

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Implement /home/ator/BF2/scripts/assemble_level_package.py and execute it to assemble all required files in /home/ator/BF2/levels/slovenia_golovec/.
Ensure existing StaticObjects.con, OvergrowthSystem.con, and Overgrowth/Overgrowth.raw remain intact.
Run the full test suite: python3 /home/ator/BF2/tests/verify_bf2_level.py -v
Document your results in /home/ator/BF2/.agents/teamwork/worker_m3/handoff.md and report back via send_message.
