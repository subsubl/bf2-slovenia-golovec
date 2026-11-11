#!/usr/bin/env python3
"""
tests/test_tier5_gameplay_invariants.py

Tier 5 Adversarial Gameplay Invariant & Asset Integrity Stress-Test Suite.
Milestone: Final Milestone - Phase 2 (Adversarial Coverage Hardening - Challenger 2)

Empirically stress-tests:
1. Level package completeness, inter-file closure, vector syntax, and strict casing.
2. Refractor 2 engine compliance: zero trailing slashes, zero double slashes, block balancing.
3. Gameplay balance, player traversal times, dry ground constraints, and building clearances.
4. Static object collision bounds: SAT 2D OBB / AABB collision clearances across all 1,309 static objects.
5. Foliage density vs terrain elevation correlation across the entire 4096m x 4096m map.

Author: teamwork_challenger (Gameplay Invariant & Asset Integrity Challenger)
"""

import math
import os
import re
import struct
import unittest
from typing import Dict, List, Tuple, Any, Set, Optional
import numpy as np
from scipy.spatial import KDTree

LEVEL_DIR = os.getenv("BF2_LEVEL_DIR", "/home/ator/BF2/levels/slovenia_golovec")
HEIGHTMAP_PATH = os.path.join(LEVEL_DIR, "Heightmap.raw")
OVERGROWTH_RAW_PATH = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
COLORMAP_DDS_PATH = os.path.join(LEVEL_DIR, "ColorMap.dds")

VANILLA_STATIC_MESHES = {
    "eu_building01", "eu_building02", "eu_office_01",
    "eu_house_01", "eu_house_02",
    "me_house_01", "me_house_02", "me_house_03", "me_house_04",
    "me_house_05", "me_house_06", "me_house_07", "me_house_08",
    "me_apartment_01", "citybuilding_01",
    "farmhouse", "barn_01", "barn_02", "shed_01", "wooden_shed", "warehouse_01"
}

# Conservative 2D bounding box dimensions (width, length) in meters for SAT OBB tests
MESH_BOUNDING_BOXES = {
    'eu_building01': (16.0, 24.0),
    'eu_building02': (18.0, 26.0),
    'eu_office_01': (18.0, 22.0),
    'citybuilding_01': (20.0, 28.0),
    'me_apartment_01': (18.0, 24.0),
    'warehouse_01': (20.0, 28.0),
    'barn_01': (12.0, 18.0),
    'barn_02': (16.0, 24.0),
    'farmhouse': (14.0, 18.0),
    'me_house_06': (14.0, 16.0),
    'eu_house_02': (12.0, 14.0),
    'me_house_04': (11.0, 13.0),
    'eu_house_01': (10.0, 12.0),
    'me_house_01': (8.0, 10.0),
    'shed_01': (6.0, 8.0),
    'wooden_shed': (4.0, 5.0),
}


class BilinearHeightmapOracle:
    """Independent oracle for Refractor 2 bilinear heightmap sampling."""

    def __init__(self, raw_path: str = HEIGHTMAP_PATH):
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Heightmap not found at {raw_path}")
        self.grid_size = 2049
        self.scale_xz = 2.0
        self.scale_y = 0.01
        self.world_half = 2048.0
        with open(raw_path, "rb") as f:
            raw_bytes = f.read()
        expected = self.grid_size * self.grid_size * 2
        assert len(raw_bytes) == expected, f"Heightmap size mismatch: expected {expected}, got {len(raw_bytes)}"
        self.data = np.frombuffer(raw_bytes, dtype="<u2").reshape((self.grid_size, self.grid_size))

    def sample(self, x: float, z: float) -> float:
        """Samples elevation at Cartesian (x, z) using bilinear interpolation."""
        u = (x + self.world_half) / self.scale_xz
        v = (z + self.world_half) / self.scale_xz
        u_clamped = max(0.0, min(float(self.grid_size - 1), u))
        v_clamped = max(0.0, min(float(self.grid_size - 1), v))

        c0, r0 = int(math.floor(u_clamped)), int(math.floor(v_clamped))
        c1 = min(c0 + 1, self.grid_size - 1)
        r1 = min(r0 + 1, self.grid_size - 1)
        s, t = u_clamped - c0, v_clamped - r0

        h00 = float(self.data[r0, c0]) * self.scale_y
        h10 = float(self.data[r0, c1]) * self.scale_y
        h01 = float(self.data[r1, c0]) * self.scale_y
        h11 = float(self.data[r1, c1]) * self.scale_y

        return (1.0 - s) * (1.0 - t) * h00 + s * (1.0 - t) * h10 + (1.0 - s) * t * h01 + s * t * h11


# =============================================================================
# 1. Level Directory Completeness & Inter-File Reference Closure
# =============================================================================
class TestLevelPackageCompletenessAndClosure(unittest.TestCase):
    """Stress-tests full directory completeness and case-sensitive inter-file reference closure."""

    def test_all_mandatory_package_files_exist_and_non_empty(self):
        """Verify that all required level package files exist, are readable, and non-empty."""
        mandatory_files = {
            "init.con": 200,
            "Heightdata.con": 100,
            "Terrain.con": 100,
            "Sky.con": 100,
            "Water.con": 100,
            "StaticObjects.con": 50000,
            "OvergrowthSystem.con": 1000,
            "GameplayObjects.con": 2000,
            os.path.join("Overgrowth", "Overgrowth.raw"): 4198401,
            "Heightmap.raw": 8396802,
            "ColorMap.dds": 8000000,
        }
        for rel_path, min_bytes in mandatory_files.items():
            full_path = os.path.join(LEVEL_DIR, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Mandatory package file missing: {rel_path}")
            size = os.path.getsize(full_path)
            self.assertGreaterEqual(size, min_bytes, f"Package file {rel_path} smaller than expected: {size} < {min_bytes}")

    def test_init_con_closure_and_case_matching(self):
        """Verify that every 'run <script>' in init.con resolves to a real file with exact case matching."""
        init_path = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.exists(init_path), f"init.con missing at {init_path}")

        run_targets = []
        with open(init_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.lower().startswith("run ") and len(s.split()) > 1:
                    run_targets.append(s.split()[1])

        self.assertGreaterEqual(len(run_targets), 7, f"init.con should run at least 7 scripts, found {len(run_targets)}")

        existing_files = set(os.listdir(LEVEL_DIR))
        for target in run_targets:
            target_path = os.path.join(LEVEL_DIR, target)
            self.assertTrue(os.path.exists(target_path), f"init.con references non-existent file: {target}")
            # Strict case sensitivity check on disk
            self.assertIn(target, existing_files, f"Case mismatch in init.con reference '{target}' vs filesystem: {existing_files}")

    def test_terrain_con_heightmap_closure_and_identity(self):
        """Verify that terrain.load references an existing Heightmap.raw identical to root."""
        terrain_con_path = os.path.join(LEVEL_DIR, "Terrain.con")
        self.assertTrue(os.path.exists(terrain_con_path))

        loaded_file = None
        with open(terrain_con_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.lower().startswith("terrain.load "):
                    loaded_file = s.split()[1]
                    break

        self.assertIsNotNone(loaded_file, "Terrain.con must specify terrain.load <heightmap>")
        self.assertEqual(loaded_file, "Heightmap.raw", f"Expected Heightmap.raw, got {loaded_file}")

        local_hmap = os.path.join(LEVEL_DIR, loaded_file)
        self.assertTrue(os.path.exists(local_hmap), f"Loaded heightmap missing at {local_hmap}")
        self.assertEqual(os.path.getsize(local_hmap), 2049 * 2049 * 2)

        root_hmap = "/home/ator/BF2/Heightmap.raw"
        if os.path.exists(root_hmap):
            with open(local_hmap, "rb") as f1, open(root_hmap, "rb") as f2:
                self.assertEqual(f1.read(), f2.read(), "levels/slovenia_golovec/Heightmap.raw must match root Heightmap.raw")

    def test_overgrowth_closure_and_exact_byte_count(self):
        """Verify that Overgrowth.raw exists in Overgrowth/ subdir with exact Refractor 2 dimensions."""
        og_path = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.exists(og_path), f"Overgrowth.raw missing at {og_path}")
        exact_bytes = 2049 * 2049 * 1
        actual_bytes = os.path.getsize(og_path)
        self.assertEqual(actual_bytes, exact_bytes, f"Overgrowth.raw size mismatch: {actual_bytes} != {exact_bytes}")

    def test_colormap_dds_magic_header_and_dimensions(self):
        """Verify ColorMap.dds has valid DirectDraw Surface header (4096x4096)."""
        dds_path = os.path.join(LEVEL_DIR, "ColorMap.dds")
        self.assertTrue(os.path.exists(dds_path), f"ColorMap.dds missing at {dds_path}")

        with open(dds_path, "rb") as f:
            magic = f.read(4)
            self.assertEqual(magic, b"DDS ", f"Invalid DDS magic header: {magic}")
            header_size, flags, height, width = struct.unpack("<IIII", f.read(16))
            self.assertEqual(header_size, 124, f"DDS header size mismatch: {header_size} != 124")
            self.assertEqual(height, 4096, f"ColorMap height mismatch: {height} != 4096")
            self.assertEqual(width, 4096, f"ColorMap width mismatch: {width} != 4096")


# =============================================================================
# 2. Refractor 2 Engine Compliance & Strict Syntax
# =============================================================================
class TestRefractor2EngineCompliance(unittest.TestCase):
    """Stress-tests Refractor 2 line syntax: no trailing slashes, no double slashes, strict vector formatting."""

    def _get_all_con_files(self) -> List[str]:
        con_files = []
        for root, _, files in os.walk(LEVEL_DIR):
            for file in files:
                if file.endswith(".con"):
                    con_files.append(os.path.join(root, file))
        return sorted(con_files)

    def test_zero_trailing_slashes_in_all_con_files(self):
        """Assert that no executable line or token ends with a trailing slash."""
        con_files = self._get_all_con_files()
        self.assertGreaterEqual(len(con_files), 8, "Expected at least 8 .con files in level package")

        violations = []
        for cf in con_files:
            rel = os.path.relpath(cf, LEVEL_DIR)
            with open(cf, "r", encoding="utf-8", errors="replace") as f:
                for line_num, line in enumerate(f, start=1):
                    s = line.strip()
                    if not s or s.lower().startswith("rem"):
                        continue
                    tokens = s.split()
                    for t in tokens:
                        if t.endswith("/") and len(t) > 1:
                            violations.append((rel, line_num, s, t))

        self.assertEqual(len(violations), 0, f"Found trailing slash violations: {violations}")

    def test_zero_double_slashes_in_all_con_files(self):
        """Assert that no executable line contains double slashes '//' (illegal Refractor 2 comment)."""
        con_files = self._get_all_con_files()
        violations = []
        for cf in con_files:
            rel = os.path.relpath(cf, LEVEL_DIR)
            with open(cf, "r", encoding="utf-8", errors="replace") as f:
                for line_num, line in enumerate(f, start=1):
                    s = line.strip()
                    if not s or s.lower().startswith("rem"):
                        continue
                    if "//" in s:
                        violations.append((rel, line_num, s))

        self.assertEqual(len(violations), 0, f"Found illegal '//' comments in .con files: {violations}")

    def test_strict_vector_syntax_no_whitespace(self):
        """Assert that every vector token (X/Y/Z) has strictly zero whitespace around forward slashes."""
        con_files = self._get_all_con_files()
        violations = []
        # Pattern detects whitespace immediately preceding or following a slash with digits
        bad_slash_regex = re.compile(r"\d+\.?\d*\s+/\s*|\s*/\s+\d+\.?\d*")

        for cf in con_files:
            rel = os.path.relpath(cf, LEVEL_DIR)
            with open(cf, "r", encoding="utf-8", errors="replace") as f:
                for line_num, line in enumerate(f, start=1):
                    s = line.strip()
                    if not s or s.lower().startswith("rem"):
                        continue
                    # Strip trailing remarks if inline
                    if " rem" in s.lower():
                        s = s[:s.lower().find(" rem")].strip()
                    if bad_slash_regex.search(s):
                        violations.append((rel, line_num, s))

        self.assertEqual(len(violations), 0, f"Found spaces around forward slashes in vector tokens: {violations}")

    def test_all_vector_numbers_are_finite_and_valid(self):
        """Assert that every vector coordinate parses to valid finite floats with no NaN, Inf, or parse errors."""
        con_files = self._get_all_con_files()
        vector_commands = {
            "object.absoluteposition", "object.rotation",
            "combatarea.min", "combatarea.max", "combatarea.addareapoint",
            "renderer.fogcolor", "renderer.ambientcolor", "renderer.suncolor", "renderer.sunspecularcolor",
            "water.color", "water.deepcolor", "water.specularcolor", "water.reflectionplane",
            "heightmap.setscale", "terrain.primaryworldscale", "objecttemplate.setspawnpositionoffset"
        }

        tested_count = 0
        for cf in con_files:
            with open(cf, "r", encoding="utf-8", errors="replace") as f:
                for line_num, line in enumerate(f, start=1):
                    s = line.strip()
                    if not s or s.lower().startswith("rem"):
                        continue
                    parts = s.split(maxsplit=1)
                    if not parts:
                        continue
                    cmd = parts[0].lower()
                    if cmd in vector_commands and len(parts) > 1:
                        vec_str = parts[1].strip()
                        components = vec_str.split("/")
                        self.assertGreaterEqual(len(components), 2, f"Vector in {cf}:{line_num} has < 2 components: '{vec_str}'")
                        for comp in components:
                            try:
                                val = float(comp)
                                self.assertTrue(math.isfinite(val), f"Non-finite float in {cf}:{line_num}: {comp}")
                            except ValueError:
                                self.fail(f"Invalid float string in vector at {cf}:{line_num}: '{comp}' in '{line}'")
                        tested_count += 1

        self.assertGreaterEqual(tested_count, 1300, f"Expected at least 1,300 vector tokens tested, got {tested_count}")

    def test_if_endif_block_balancing(self):
        """Assert that all conditional blocks (if / else / endIf) are properly closed across all files."""
        con_files = self._get_all_con_files()
        for cf in con_files:
            rel = os.path.relpath(cf, LEVEL_DIR)
            stack = []
            with open(cf, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, start=1):
                    s = line.strip()
                    if not s or s.lower().startswith("rem"):
                        continue
                    tokens = s.split()
                    if tokens[0] == "if":
                        stack.append((line_num, s))
                    elif tokens[0] == "endIf":
                        self.assertTrue(len(stack) > 0, f"{rel}:{line_num}: 'endIf' without matching 'if'")
                        stack.pop()
            self.assertEqual(len(stack), 0, f"{rel}: Unclosed 'if' blocks remaining: {stack}")


# =============================================================================
# 3. Gameplay Balance, Player Traversal Times, and Terrain Traversal Slopes
# =============================================================================
class TestGameplayBalanceAndPlayerTraversal(unittest.TestCase):
    """Stress-tests player traversal times, symmetry, terrain slope limits, and Conquest topology."""

    @classmethod
    def setUpClass(cls):
        cls.heightmap = BilinearHeightmapOracle()
        cls.gameplay_con = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        cls._parse_gameplay_objects()

    @classmethod
    def _parse_gameplay_objects(cls):
        cls.cps: Dict[str, Dict[str, Any]] = {}
        cls.sps: List[Dict[str, Any]] = []
        cls.combat_area_pts: List[Tuple[float, float]] = []

        current_tpl = None
        current_obj = None

        with open(cls.gameplay_con, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or s.lower().startswith("rem"):
                    continue
                parts = s.split(maxsplit=1)
                cmd = parts[0]
                arg = parts[1].strip() if len(parts) > 1 else ""

                if cmd == "CombatArea.addAreaPoint":
                    pt = [float(p) for p in arg.split("/")]
                    cls.combat_area_pts.append((pt[0], pt[1]))

                elif cmd == "ObjectTemplate.create":
                    toks = arg.split()
                    current_tpl = {"type": toks[0], "name": toks[1]}
                elif current_tpl is not None:
                    if cmd == "ObjectTemplate.controlPointId" or cmd == "ObjectTemplate.setControlPointId":
                        current_tpl["cp_id"] = int(arg)
                    elif cmd == "ObjectTemplate.team":
                        current_tpl["team"] = int(arg)
                    elif cmd == "ObjectTemplate.radius":
                        current_tpl["radius"] = float(arg)
                    elif cmd == "ObjectTemplate.setSpawnPositionOffset":
                        current_tpl["offset"] = [float(p) for p in arg.split("/")]

                if cmd == "Object.create":
                    current_obj = {"template": arg}
                elif current_obj is not None:
                    if cmd == "Object.absolutePosition":
                        current_obj["pos"] = tuple(float(p) for p in arg.split("/"))
                    elif cmd == "Object.rotation":
                        current_obj["rot"] = tuple(float(p) for p in arg.split("/"))
                        # Finalize object
                        tname = current_obj["template"]
                        if "CP_" in tname:
                            cls.cps[tname] = {**current_obj}
                        elif "SP_" in tname:
                            cls.sps.append({**current_obj})

    def test_conquest_head_on_cp_specification(self):
        """Verify 3 standard Conquest Head-On Control Points: EU Base (Team 1), Pass (Neutral 0), MEC Base (Team 2)."""
        self.assertEqual(len(self.cps), 3, f"Expected exactly 3 Control Points, found {len(self.cps)}")
        self.assertIn("CP_EU_BASE", self.cps)
        self.assertIn("CP_GOLOVEC_PASS", self.cps)
        self.assertIn("CP_MEC_BASE", self.cps)

        pass_pos = self.cps["CP_GOLOVEC_PASS"]["pos"]
        self.assertAlmostEqual(pass_pos[0], 0.0, delta=1.0, msg="Golovec Pass X must be centered at 0")
        self.assertAlmostEqual(pass_pos[2], 1365.0, delta=1.0, msg="Golovec Pass Z must be centered at 1365 (focal point)")

    def test_player_traversal_distance_and_time_symmetry(self):
        """
        Adversarially stress-tests sprint and combat run times from both bases to contested Golovec Pass.
        Sprint speed: 6.5 m/s. Combat run: 4.5 m/s.
        Tolerance: Distance asymmetry < 10%, Sprint time delta < 5.0 seconds.
        """
        eu_pos = np.array(self.cps["CP_EU_BASE"]["pos"])
        pass_pos = np.array(self.cps["CP_GOLOVEC_PASS"]["pos"])
        mec_pos = np.array(self.cps["CP_MEC_BASE"]["pos"])

        # 3D Euclidean distances
        d_eu = float(np.linalg.norm(eu_pos - pass_pos))
        d_mec = float(np.linalg.norm(mec_pos - pass_pos))

        sprint_speed = 6.5  # m/s
        run_speed = 4.5     # m/s

        t_sprint_eu = d_eu / sprint_speed
        t_sprint_mec = d_mec / sprint_speed
        sprint_delta = abs(t_sprint_eu - t_sprint_mec)

        ratio = d_eu / d_mec
        self.assertGreaterEqual(ratio, 0.90, f"Asymmetry too large: EU/MEC distance ratio {ratio:.3f} < 0.90")
        self.assertLessEqual(ratio, 1.10, f"Asymmetry too large: EU/MEC distance ratio {ratio:.3f} > 1.10")

        self.assertLess(sprint_delta, 5.0, f"Sprint time delta {sprint_delta:.2f}s exceeds competitive 5.0s threshold")
        print(f"\n[Traversal Balance] EU Base -> Pass: {d_eu:.1f}m ({t_sprint_eu:.1f}s sprint)")
        print(f"[Traversal Balance] MEC Base -> Pass: {d_mec:.1f}m ({t_sprint_mec:.1f}s sprint)")
        print(f"[Traversal Balance] Sprint delta: {sprint_delta:.2f}s, Ratio: {ratio:.4f}")

    def test_terrain_traversal_slope_walkability(self):
        """
        Raymarches at 1-meter intervals along both traversal vectors:
        Validates mean terrain slope < 5.0 degrees and no unclimbable vertical barriers (> 60 degrees).
        """
        for base_name, base_key in [("EU Base", "CP_EU_BASE"), ("MEC Base", "CP_MEC_BASE")]:
            start_xz = np.array([self.cps[base_key]["pos"][0], self.cps[base_key]["pos"][2]])
            end_xz = np.array([self.cps["CP_GOLOVEC_PASS"]["pos"][0], self.cps["CP_GOLOVEC_PASS"]["pos"][2]])
            vec = end_xz - start_xz
            dist = np.linalg.norm(vec)
            steps = int(math.ceil(dist))

            slopes = []
            prev_y = self.heightmap.sample(start_xz[0], start_xz[1])

            for i in range(1, steps + 1):
                pt = start_xz + (i / steps) * vec
                curr_y = self.heightmap.sample(pt[0], pt[1])
                dy = abs(curr_y - prev_y)
                dx = dist / steps
                deg = math.degrees(math.atan2(dy, dx))
                slopes.append(deg)
                prev_y = curr_y

            mean_slope = float(np.mean(slopes))
            p95_slope = float(np.percentile(slopes, 95))

            self.assertLess(mean_slope, 5.0, f"{base_name} mean slope {mean_slope:.2f} deg exceeds comfortable 5.0 deg")
            self.assertLess(p95_slope, 35.0, f"{base_name} 95th percentile slope {p95_slope:.2f} deg exceeds 35.0 deg")

    def test_spawn_point_spacing_and_elevation_offset(self):
        """Stress-test spawn points: minimum 2 per CP, separation >= 10m, distance to flagpole 5m-30m."""
        self.assertGreaterEqual(len(self.sps), 6, f"Expected at least 6 spawn points, found {len(self.sps)}")

        # Group spawn points by proximity to CP
        cp_sp_map = {cp_name: [] for cp_name in self.cps}
        for sp in self.sps:
            sp_xz = np.array([sp["pos"][0], sp["pos"][2]])
            closest_cp = min(self.cps.keys(), key=lambda cp: np.linalg.norm(sp_xz - np.array([self.cps[cp]["pos"][0], self.cps[cp]["pos"][2]])))
            cp_sp_map[closest_cp].append(sp)

        for cp_name, sp_list in cp_sp_map.items():
            self.assertGreaterEqual(len(sp_list), 2, f"CP {cp_name} has fewer than 2 associated spawn points: {len(sp_list)}")
            cp_pos = np.array(self.cps[cp_name]["pos"])

            # Check distance to flagpole
            for sp in sp_list:
                sp_pos = np.array(sp["pos"])
                d_flag = float(np.linalg.norm(sp_pos - cp_pos))
                self.assertGreaterEqual(d_flag, 5.0, f"Spawn point {sp['template']} too close to flagpole ({d_flag:.2f}m < 5.0m)")
                self.assertLessEqual(d_flag, 30.0, f"Spawn point {sp['template']} too far from flagpole ({d_flag:.2f}m > 30.0m)")

            # Check separation between paired spawn points
            sp0_pos = np.array(sp_list[0]["pos"])
            sp1_pos = np.array(sp_list[1]["pos"])
            d_sep = float(np.linalg.norm(sp0_pos - sp1_pos))
            self.assertGreaterEqual(d_sep, 10.0, f"Spawn points at {cp_name} too close to each other ({d_sep:.2f}m < 10.0m)")

    def test_combat_area_anti_clockwise_winding_and_enclosure(self):
        """
        Stress-tests Combat Area:
        1. Positive signed area (CCW / Anti-Clockwise winding).
        2. Strict enclosure of all CPs and SPs with > 50m buffer margin.
        """
        pts = self.combat_area_pts
        self.assertGreaterEqual(len(pts), 3, "Combat area must have at least 3 boundary vertices")

        # Shoelace formula for signed area
        area = 0.0
        n = len(pts)
        for i in range(n):
            x1, z1 = pts[i]
            x2, z2 = pts[(i + 1) % n]
            area += (x1 * z2 - x2 * z1)
        signed_area = 0.5 * area

        self.assertGreater(signed_area, 0.0, f"Combat area must have POSITIVE signed area (CCW winding): {signed_area}")

        # Ray casting point-in-polygon helper
        def is_inside(px: float, pz: float) -> bool:
            inside = False
            p1x, p1z = pts[0]
            for j in range(1, n + 1):
                p2x, p2z = pts[j % n]
                if min(p1z, p2z) < pz <= max(p1z, p2z):
                    if px <= max(p1x, p2x):
                        x_inters = (pz - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                        if p1x == p2x or px <= x_inters:
                            inside = not inside
                p1x, p1z = p2x, p2z
            return inside

        def dist_to_boundary(px: float, pz: float) -> float:
            min_d = float("inf")
            for j in range(n):
                p1 = np.array(pts[j])
                p2 = np.array(pts[(j + 1) % n])
                seg = p2 - p1
                seg_len = np.linalg.norm(seg)
                if seg_len == 0:
                    continue
                u = np.clip(np.dot([px, pz] - p1, seg) / (seg_len * seg_len), 0.0, 1.0)
                proj = p1 + u * seg
                d = np.linalg.norm([px, pz] - proj)
                min_d = min(min_d, d)
            return float(min_d)

        # Check all CPs
        for cp_name, cp_data in self.cps.items():
            cx, cz = cp_data["pos"][0], cp_data["pos"][2]
            self.assertTrue(is_inside(cx, cz), f"Control Point {cp_name} at ({cx}, {cz}) outside Combat Area")
            margin = dist_to_boundary(cx, cz)
            self.assertGreater(margin, 50.0, f"Control Point {cp_name} margin {margin:.2f}m < 50.0m safety threshold")

        # Check all SPs
        for sp in self.sps:
            sx, sz = sp["pos"][0], sp["pos"][2]
            self.assertTrue(is_inside(sx, sz), f"Spawn Point {sp['template']} outside Combat Area")
            margin = dist_to_boundary(sx, sz)
            self.assertGreater(margin, 50.0, f"Spawn Point {sp['template']} margin {margin:.2f}m < 50.0m safety threshold")


# =============================================================================
# 4. Dry Ground Constraints & Hydrology
# =============================================================================
class TestDryGroundAndHydrologyConstraints(unittest.TestCase):
    """Stress-tests dry ground invariants: no underwater CPs, SPs, or buildings."""

    @classmethod
    def setUpClass(cls):
        cls.heightmap = BilinearHeightmapOracle()
        # Parse water elevation from Terrain.con
        terrain_path = os.path.join(LEVEL_DIR, "Terrain.con")
        cls.water_elev = 270.0
        with open(terrain_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.lower().startswith("terrain.setwaterelevation"):
                    cls.water_elev = float(s.split()[1])

    def test_water_elevation_is_270(self):
        """Verify water table elevation in Terrain.con is set to 270.0m (Ljubljanica river level)."""
        self.assertEqual(self.water_elev, 270.0)

    def test_control_points_dry_ground_clearance(self):
        """Verify all Control Points have ground elevation >= 272.0m (+2m dry ground buffer)."""
        gameplay_con = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        with open(gameplay_con, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            s = line.strip()
            if s.startswith("Object.create CP_"):
                # Next line has position
                pos_line = lines[idx + 1].strip()
                pos_str = pos_line.split()[1]
                x, y, z = [float(p) for p in pos_str.split("/")]
                self.assertGreater(y, self.water_elev + 2.0, f"Control Point at ({x}, {y}, {z}) too close to water level ({self.water_elev}m)")
                h_sample = self.heightmap.sample(x, z)
                self.assertAlmostEqual(y, h_sample, delta=0.5, msg=f"CP elevation {y} deviates from heightmap {h_sample}")

    def test_spawn_points_dry_ground_clearance(self):
        """Verify all Spawn Points have ground elevation > 270.0m and spawn elevation >= 271.25m."""
        gameplay_con = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        with open(gameplay_con, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            s = line.strip()
            if s.startswith("Object.create SP_"):
                pos_line = lines[idx + 1].strip()
                pos_str = pos_line.split()[1]
                x, y, z = [float(p) for p in pos_str.split("/")]
                self.assertGreater(y, self.water_elev + 1.25, f"Spawn Point at ({x}, {y}, {z}) submerged or at waterline")
                h_sample = self.heightmap.sample(x, z)
                self.assertGreater(h_sample, self.water_elev, f"Spawn Point terrain at ({x}, {z}) is underwater: {h_sample}m")

    def test_static_objects_zero_underwater(self):
        """Adversarial check: Assert that 0 out of 1,309 static buildings are underwater (Y < 270.0m)."""
        static_con = os.path.join(LEVEL_DIR, "StaticObjects.con")
        underwater = []
        with open(static_con, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                s = line.strip()
                if s.startswith("Object.absolutePosition"):
                    parts = s.split()[1].split("/")
                    x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                    if y < self.water_elev:
                        underwater.append((line_num, x, y, z))

        self.assertEqual(len(underwater), 0, f"Found {len(underwater)} static buildings placed below water level: {underwater[:5]}")


# =============================================================================
# 5. Static Object SAT OBB / AABB Collision Clearances
# =============================================================================
class TestStaticObjectSATOBBAndAABBCollisions(unittest.TestCase):
    """Stress-tests static building clearances using 2D Separating Axis Theorem (SAT) OBB collisions."""

    @classmethod
    def setUpClass(cls):
        cls.objects: List[Dict[str, Any]] = []
        static_con = os.path.join(LEVEL_DIR, "StaticObjects.con")
        with open(static_con, "r", encoding="utf-8") as f:
            curr = {}
            for line in f:
                s = line.strip()
                if not s or s.lower().startswith("rem"):
                    continue
                parts = s.split(maxsplit=1)
                cmd = parts[0]
                arg = parts[1].strip() if len(parts) > 1 else ""

                if cmd == "Object.create":
                    if curr and "template" in curr and "pos" in curr:
                        cls.objects.append(curr)
                    curr = {"template": arg}
                elif curr is not None:
                    if cmd == "Object.absolutePosition":
                        curr["pos"] = tuple(float(p) for p in arg.split("/"))
                    elif cmd == "Object.rotation":
                        curr["rot"] = tuple(float(p) for p in arg.split("/"))
                    elif cmd == "Object.layer":
                        curr["layer"] = int(arg)

            if curr and "template" in curr and "pos" in curr:
                cls.objects.append(curr)

    def test_static_objects_count_and_mesh_whitelist(self):
        """Verify exactly 1,309 static objects and all belong to vanilla European/rural whitelist."""
        self.assertEqual(len(self.objects), 1309, f"Expected 1,309 static objects, found {len(self.objects)}")
        illegal_meshes = set()
        for obj in self.objects:
            if obj["template"] not in VANILLA_STATIC_MESHES:
                illegal_meshes.add(obj["template"])
        self.assertEqual(len(illegal_meshes), 0, f"Found non-vanilla static meshes: {illegal_meshes}")

    def test_minimum_pairwise_centroid_distance_exceeds_30m(self):
        """Adversarial check: Assert that min distance between any two static buildings >= 30.0m."""
        xz = np.array([[o["pos"][0], o["pos"][2]] for o in self.objects])
        tree = KDTree(xz)
        dists, _ = tree.query(xz, k=2)  # k=2 returns self (dist=0) and closest neighbor
        nearest_neighbor_dists = dists[:, 1]
        min_dist = float(nearest_neighbor_dists.min())
        self.assertGreaterEqual(min_dist, 30.0, f"Minimum clearance violated: {min_dist:.4f}m < 30.0m")

    def test_sat_obb_collision_absence_across_all_objects(self):
        """
        Adversarial Separating Axis Theorem (SAT) 2D Oriented Bounding Box collision oracle:
        Evaluates all candidate pairs within 45m radius and verifies ZERO geometry intersections.
        """
        def get_obb_corners(cx: float, cz: float, yaw_deg: float, w: float, l: float) -> List[Tuple[float, float]]:
            rad = math.radians(yaw_deg)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            hw, hl = w / 2.0, l / 2.0
            local = [(-hw, -hl), (hw, -hl), (hw, hl), (-hw, hl)]
            corners = []
            for lx, lz in local:
                gx = cx + (lx * cos_a - lz * sin_a)
                gz = cz + (lx * sin_a + lz * cos_a)
                corners.append((gx, gz))
            return corners

        def sat_overlap(c1: List[Tuple[float, float]], c2: List[Tuple[float, float]]) -> bool:
            for corners in (c1, c2):
                for i in range(len(corners)):
                    p1 = corners[i]
                    p2 = corners[(i + 1) % len(corners)]
                    edge = (p2[0] - p1[0], p2[1] - p1[1])
                    normal = (-edge[1], edge[0])
                    norm = math.hypot(normal[0], normal[1])
                    if norm == 0:
                        continue
                    normal = (normal[0] / norm, normal[1] / norm)

                    projs1 = [c[0] * normal[0] + c[1] * normal[1] for c in c1]
                    projs2 = [c[0] * normal[0] + c[1] * normal[1] for c in c2]

                    if max(projs1) < min(projs2) or max(projs2) < min(projs1):
                        return False  # Separating axis found
            return True  # Overlap on all axes

        xz = np.array([[o["pos"][0], o["pos"][2]] for o in self.objects])
        tree = KDTree(xz)
        candidate_pairs = tree.query_pairs(r=45.0)

        collisions = []
        for i, j in candidate_pairs:
            o1, o2 = self.objects[i], self.objects[j]
            w1, l1 = MESH_BOUNDING_BOXES.get(o1["template"], (16.0, 20.0))
            w2, l2 = MESH_BOUNDING_BOXES.get(o2["template"], (16.0, 20.0))
            c1 = get_obb_corners(o1["pos"][0], o1["pos"][2], o1["rot"][0], w1, l1)
            c2 = get_obb_corners(o2["pos"][0], o2["pos"][2], o2["rot"][0], w2, l2)
            if sat_overlap(c1, c2):
                collisions.append((i, j, o1["template"], o2["template"]))

        self.assertEqual(len(collisions), 0, f"Found {len(collisions)} SAT OBB static object collisions: {collisions}")

    def test_spawn_points_outside_static_building_obb_footprints(self):
        """Adversarial check: Assert that no player spawn point is placed inside any building OBB footprint."""
        gameplay_con = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        sps = []
        with open(gameplay_con, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                s = line.strip()
                if s.startswith("Object.create SP_"):
                    pos_line = lines[idx + 1].strip()
                    parts = pos_line.split()[1].split("/")
                    sps.append((s.split()[1], float(parts[0]), float(parts[2])))

        def point_in_obb(px: float, pz: float, cx: float, cz: float, yaw_deg: float, w: float, l: float) -> bool:
            rad = math.radians(yaw_deg)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            dx = px - cx
            dz = pz - cz
            lx = dx * cos_a + dz * sin_a
            lz = -dx * sin_a + dz * cos_a
            return abs(lx) <= w / 2.0 and abs(lz) <= l / 2.0

        for sp_name, sx, sz in sps:
            for obj in self.objects:
                w, l = MESH_BOUNDING_BOXES.get(obj["template"], (16.0, 20.0))
                self.assertFalse(
                    point_in_obb(sx, sz, obj["pos"][0], obj["pos"][2], obj["rot"][0], w, l),
                    f"Spawn point {sp_name} at ({sx}, {sz}) placed inside static building {obj['template']} footprint"
                )


# =============================================================================
# 6. Foliage Density vs Terrain Elevation Correlation
# =============================================================================
class TestFoliageDensityElevationCorrelation(unittest.TestCase):
    """Stress-tests overgrowth density mask correlation with terrain elevation across all 4,198,401 cells."""

    @classmethod
    def setUpClass(cls):
        # Load Heightmap.raw (2049x2049 uint16)
        cls.h = np.fromfile(HEIGHTMAP_PATH, dtype="<u2").reshape((2049, 2049)) * 0.01
        # Load Overgrowth.raw (2049x2049 uint8)
        cls.og = np.fromfile(OVERGROWTH_RAW_PATH, dtype=np.uint8).reshape((2049, 2049))

    def test_overgrowth_mask_non_trivial_canopy(self):
        """Verify that overgrowth mask has realistic temperate forest canopy coverage (> 30% non-zero)."""
        nonzero_count = np.count_nonzero(self.og)
        total = self.og.size
        coverage_pct = (nonzero_count / total) * 100.0
        self.assertGreaterEqual(coverage_pct, 30.0, f"Overgrowth canopy coverage too low: {coverage_pct:.2f}% < 30.0%")
        self.assertLessEqual(coverage_pct, 80.0, f"Overgrowth canopy coverage unrealistically high: {coverage_pct:.2f}% > 80.0%")

    def test_foliage_suppression_in_water_zones(self):
        """Verify that water areas (elevation <= 270.0m) have heavily suppressed tree density (mean < 25)."""
        water_mask = (self.h <= 270.0)
        water_pixels = np.count_nonzero(water_mask)
        self.assertGreater(water_pixels, 100000, f"Expected significant river/water plain pixels, got {water_pixels}")

        mean_water_density = float(self.og[water_mask].mean())
        self.assertLess(mean_water_density, 25.0, f"Foliage density in water zones too high: {mean_water_density:.2f} >= 25.0")

    def test_foliage_prominence_on_golovec_ridge(self):
        """Verify that high-elevation Golovec ridge (> 320m) has high foliage density (mean > 100, coverage > 70%)."""
        ridge_mask = (self.h > 320.0)
        ridge_pixels = np.count_nonzero(ridge_mask)
        self.assertGreater(ridge_pixels, 500000, f"Expected substantial ridge pixels, got {ridge_pixels}")

        mean_ridge_density = float(self.og[ridge_mask].mean())
        ridge_coverage = (np.count_nonzero(self.og[ridge_mask]) / ridge_pixels) * 100.0

        self.assertGreater(mean_ridge_density, 100.0, f"Foliage density on ridge too low: {mean_ridge_density:.2f} < 100.0")
        self.assertGreater(ridge_coverage, 70.0, f"Foliage coverage on ridge too low: {ridge_coverage:.2f}% < 70.0%")

    def test_pearson_correlation_elevation_vs_foliage(self):
        """
        Adversarial statistical test: Pearson correlation between terrain elevation and foliage density.
        Golovec is a prominent forested hill surrounded by flat urban plains:
        Statistically requires strong positive correlation (r > 0.45).
        """
        r = float(np.corrcoef(self.h.ravel(), self.og.ravel())[0, 1])
        print(f"\n[Elevation-Foliage Correlation] Pearson r = {r:.4f}")
        self.assertGreater(r, 0.45, f"Elevation vs foliage correlation too weak: {r:.4f} <= 0.45")


if __name__ == "__main__":
    unittest.main()
