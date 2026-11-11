#!/usr/bin/env python3
"""
audit_milestone3.py - Independent forensic verification script for Milestone 3.
Checks package authenticity, lineage, mathematical accuracy, and absence of cheating.
"""

import os
import sys
import hashlib
import tempfile
import subprocess
import numpy as np

sys.path.insert(0, "/home/ator/BF2/tests")
from con_parser import ConParser, HeightmapSampler, polygon_signed_area, point_in_polygon

LEVEL_DIR = "/home/ator/BF2/levels/slovenia_golovec"
ROOT_DIR = "/home/ator/BF2"

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_forensic_checks():
    print("=" * 80)
    print("FORENSIC INTEGRITY AUDIT - MILESTONE 3 DELIVERABLES")
    print("=" * 80)

    # 1. Check all 8 configuration files
    expected_con_files = [
        "init.con",
        "Heightdata.con",
        "Terrain.con",
        "Sky.con",
        "Water.con",
        "StaticObjects.con",
        "OvergrowthSystem.con",
        "GameplayObjects.con"
    ]
    print("\n--- 1. Configuration Files Existence and Non-Emptiness ---")
    for f in expected_con_files:
        p = os.path.join(LEVEL_DIR, f)
        if not os.path.isfile(p):
            print(f"[FAIL] Missing config file: {p}")
            sys.exit(1)
        sz = os.path.getsize(p)
        if sz == 0:
            print(f"[FAIL] Empty config file: {p}")
            sys.exit(1)
        print(f"[PASS] {f}: {sz} bytes")

    # Also check Overgrowth.raw, Heightmap.raw, ColorMap.dds
    print("\n--- 2. Binary Assets Inodes & Sizes ---")
    raw_path = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
    if not os.path.isfile(raw_path):
        print(f"[FAIL] Missing Overgrowth.raw: {raw_path}")
        sys.exit(1)
    sz_raw = os.path.getsize(raw_path)
    if sz_raw != 4198401:
        print(f"[FAIL] Overgrowth.raw wrong size: {sz_raw} != 4198401")
        sys.exit(1)
    print(f"[PASS] Overgrowth.raw: exactly {sz_raw} bytes")

    hm_dst = os.path.join(LEVEL_DIR, "Heightmap.raw")
    hm_src = os.path.join(ROOT_DIR, "Heightmap.raw")
    if not os.path.samefile(hm_dst, hm_src):
        print(f"[WARN] Heightmap.raw does not share inode with root file")
    else:
        print(f"[PASS] Heightmap.raw shares inode {os.stat(hm_dst).st_ino} (hardlinked)")

    cm_dst = os.path.join(LEVEL_DIR, "ColorMap.dds")
    cm_src = os.path.join(ROOT_DIR, "ColorMap.dds")
    if not os.path.samefile(cm_dst, cm_src):
        print(f"[WARN] ColorMap.dds does not share inode with root file")
    else:
        print(f"[PASS] ColorMap.dds shares inode {os.stat(cm_dst).st_ino} (hardlinked)")

    # 3. Lineage and hash preservation for M1 and M2 deliverables
    print("\n--- 3. M1 and M2 Deliverable Lineage & Hash Preservation ---")
    static_hash = sha256_file(os.path.join(LEVEL_DIR, "StaticObjects.con"))
    expected_static_hash = "f7ac4ebf1de1f6df0df8deef4f4421563e81f38fbd0f3eb62c811ab095d8689b"
    if static_hash != expected_static_hash:
        print(f"[FAIL] StaticObjects.con hash mismatch: {static_hash} != {expected_static_hash}")
        sys.exit(1)
    print(f"[PASS] StaticObjects.con SHA256 preserved: {static_hash}")

    overgrowth_raw_hash = sha256_file(raw_path)
    expected_raw_hash = "e800f8fa09a0c1c99c58272fb82dde1ef7c5ccb33ebab3ab7c825c57f54ff209"
    if overgrowth_raw_hash != expected_raw_hash:
        print(f"[FAIL] Overgrowth.raw hash mismatch: {overgrowth_raw_hash} != {expected_raw_hash}")
        sys.exit(1)
    print(f"[PASS] Overgrowth.raw SHA256 preserved: {overgrowth_raw_hash}")

    # Check OvergrowthSystem.con lines and syntax
    parser_og = ConParser(os.path.join(LEVEL_DIR, "OvergrowthSystem.con"))
    clean_og = parser_og.get_clean_lines()
    print(f"[PASS] OvergrowthSystem.con has {len(clean_og)} active clean lines")

    # 4. Elevation Grounding of Gameplay Objects against Heightmap.raw
    print("\n--- 4. GameplayObjects Ground Elevation & Topology Verification ---")
    sampler = HeightmapSampler(hm_src)
    gameplay_parser = ConParser(os.path.join(LEVEL_DIR, "GameplayObjects.con"))
    gp_data = gameplay_parser.parse_gameplay_objects()
    cps = gp_data["control_points"]
    sps = gp_data["spawn_points"]

    print(f"Parsed {len(cps)} Control Points, {len(sps)} Spawn Points.")
    if len(cps) != 3:
        print(f"[FAIL] Expected 3 Control Points, found {len(cps)}")
        sys.exit(1)
    if len(sps) != 6:
        print(f"[FAIL] Expected 6 Spawn Points, found {len(sps)}")
        sys.exit(1)

    for cp in cps:
        pos = cp["position"]
        x, y, z = pos
        ground_y = sampler.sample_bilinear(x, z)
        diff = abs(y - ground_y)
        print(f"CP '{cp['name']}' (Team {cp.get('team')}): pos=({x}, {y}, {z}), heightmap ground={ground_y:.4f}, diff={diff:.4f}m")
        if diff > 0.5:
            print(f"[FAIL] CP '{cp['name']}' elevation deviation {diff:.4f}m exceeds 0.5m!")
            sys.exit(1)
    print("[PASS] All Control Points grounded within 0.5m of Heightmap.raw")

    for sp in sps:
        pos = sp["position"]
        x, y, z = pos
        ground_y = sampler.sample_bilinear(x, z)
        diff = abs(y - ground_y)
        offset = sp.get("spawnPositionOffset")
        print(f"SP '{sp['name']}' (CP_ID {sp.get('controlPointId')}): pos=({x}, {y}, {z}), offset={offset}, ground={ground_y:.4f}, diff={diff:.4f}m")
        if diff > 0.5:
            print(f"[FAIL] SP '{sp['name']}' elevation deviation {diff:.4f}m exceeds 0.5m!")
            sys.exit(1)
        if offset != [0.0, 1.25, 0.0]:
            print(f"[FAIL] SP '{sp['name']}' spawnPositionOffset is {offset}, expected [0.0, 1.25, 0.0]")
            sys.exit(1)
    print("[PASS] All Spawn Points grounded within 0.5m and offset by +1.25m")

    # 5. Combat Area Verification
    print("\n--- 5. Combat Area Verification ---")
    areas = gameplay_parser.parse_combat_areas()
    if not areas:
        print("[FAIL] No combat areas found")
        sys.exit(1)
    ca = areas[0]
    pts = ca["points"]
    area_val = polygon_signed_area(pts)
    print(f"Combat area points: {pts}")
    print(f"Combat area signed area (Shoelace): {area_val:.1f} m^2")
    if area_val <= 0:
        print(f"[FAIL] Combat area signed area is <= 0 (not CCW winding)!")
        sys.exit(1)
    if area_val < 500000.0:
        print(f"[FAIL] Combat area too small: {area_val:.1f} < 500000.0 m^2")
        sys.exit(1)
    print("[PASS] Combat area has positive signed area >= 500,000 m^2 (CCW winding)")

    # Enclosure checks
    focal_pt = (0.0, 1365.0)
    if not point_in_polygon(focal_pt[0], focal_pt[1], pts):
        print(f"[FAIL] Focal point {focal_pt} not in combat area!")
        sys.exit(1)
    print(f"[PASS] Focal point {focal_pt} enclosed in combat area")

    for cp in cps:
        if not point_in_polygon(cp["position"][0], cp["position"][2], pts):
            print(f"[FAIL] CP {cp['name']} not in combat area!")
            sys.exit(1)
    print("[PASS] All 3 Control Points enclosed in combat area")

    for sp in sps:
        if not point_in_polygon(sp["position"][0], sp["position"][2], pts):
            print(f"[FAIL] SP {sp['name']} not in combat area!")
            sys.exit(1)
    print("[PASS] All 6 Spawn Points enclosed in combat area")

    # 6. Check init.con, Sky.con, Water.con syntax
    print("\n--- 6. init.con, Sky.con, Water.con Syntax & Whitelist ---")
    init_parser = ConParser(os.path.join(LEVEL_DIR, "init.con"))
    runs = init_parser.parse_run_commands()
    print(f"init.con runs: {runs}")
    for req in ["Heightdata.con", "Terrain.con", "Sky.con", "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"]:
        if req not in runs:
            print(f"[FAIL] init.con does not run {req}")
            sys.exit(1)
    print("[PASS] init.con executes all 7 mandatory child scripts")

    block_res = init_parser.check_block_structure()
    if not block_res["balanced"]:
        print(f"[FAIL] init.con unbalanced blocks: {block_res['errors']}")
        sys.exit(1)
    print("[PASS] init.con has balanced conditional block structure")

    # Vector formatting (no spaces around slashes)
    for cf in ["Sky.con", "Water.con", "GameplayObjects.con", "init.con"]:
        cp_p = ConParser(os.path.join(LEVEL_DIR, cf))
        viol = cp_p.check_vector_syntax_no_spaces()
        if viol:
            print(f"[FAIL] Illegal spaces around slashes in {cf}: {viol}")
            sys.exit(1)
    print("[PASS] All configuration files satisfy vector format (no spaces around /)")

    # 7. Absence of Cheating & Facade Analysis
    print("\n--- 7. Absence of Cheating & Facade Analysis in scripts/assemble_level_package.py ---")
    script_path = "/home/ator/BF2/scripts/assemble_level_package.py"
    with open(script_path, "r", encoding="utf-8") as f:
        src = f.read()

    prohibited_keywords = ["mock", "unittest.mock", "patch(", "MagicMock", "pytest.skip", "return True", "return 88"]
    for kw in prohibited_keywords:
        if kw in src:
            print(f"[FAIL] Found suspicious keyword '{kw}' in {script_path}")
            sys.exit(1)
    print("[PASS] Zero mock/facade keywords found in assemble_level_package.py")

    # 8. Test Assemble Script Execution into a Temporary Directory
    print("\n--- 8. Autonomous Execution of assemble_level_package.py into Clean Sandbox ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_level_dir = os.path.join(tmpdir, "test_level")
        # Copy M1 and M2 deliverables into test_level_dir so assembler can verify them
        os.makedirs(os.path.join(test_level_dir, "Overgrowth"), exist_ok=True)
        shutil.copyfile(os.path.join(LEVEL_DIR, "StaticObjects.con"), os.path.join(test_level_dir, "StaticObjects.con"))
        shutil.copyfile(os.path.join(LEVEL_DIR, "OvergrowthSystem.con"), os.path.join(test_level_dir, "OvergrowthSystem.con"))
        shutil.copyfile(raw_path, os.path.join(test_level_dir, "Overgrowth", "Overgrowth.raw"))

        cmd = [sys.executable, script_path, "--level-dir", test_level_dir, "--root-dir", ROOT_DIR]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[FAIL] Assembler script failed in sandbox with exit code {res.returncode}:\n{res.stderr}")
            sys.exit(1)
        print("[PASS] Assembler script executed cleanly in temporary sandbox with exit code 0")

        # Verify output files in sandbox
        for f in expected_con_files:
            sb_p = os.path.join(test_level_dir, f)
            if not os.path.isfile(sb_p):
                print(f"[FAIL] Sandbox missing {f}")
                sys.exit(1)
        print("[PASS] All 8 configuration files generated cleanly in sandbox")

    print("\n" + "=" * 80)
    print("ALL FORENSIC CHECKS PASSED: VERDICT IS CLEAN")
    print("=" * 80)

if __name__ == "__main__":
    import shutil
    run_forensic_checks()
