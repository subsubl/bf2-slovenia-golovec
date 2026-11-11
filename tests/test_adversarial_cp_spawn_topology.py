"""
Milestone 3 Challenger 2: Adversarial CP-Spawn Topology Verifier.
Empirically stress-tests:
1. Control Point & Spawn Point Linkages (1-to-N bijection, min 2 SPs/CP, unique IDs, offsets).
2. Elevation Grounding Precision (independent bilinear sampling on Heightmap.raw, tolerance <= 0.05m).
3. Base Balance & Focal Distance (EU vs MEC distance to Golovec Pass Delta < 20%, elevation >= 270.0m dry ground).
4. Spawn clearance, inter-spawn separation, and combat area containment margin.
"""

import os
import unittest
import math
import struct
import numpy as np
from typing import List, Dict, Any, Tuple


HEIGHTMAP_PATH = "/home/ator/BF2/Heightmap.raw"
GAMEPLAY_PATH = "/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con"
TERRAIN_PATH = "/home/ator/BF2/levels/slovenia_golovec/Terrain.con"


class IndependentBilinearHeightmapSampler:
    """Independent implementation of Refractor 2 terrain bilinear sampling."""

    def __init__(self, raw_path: str = HEIGHTMAP_PATH):
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Heightmap raw file missing: {raw_path}")
        self.grid_size = 2049
        self.scale_xz = 2.0
        self.scale_y = 0.01
        self.world_half = 2048.0
        # Load uint16 little endian
        file_size = os.path.getsize(raw_path)
        expected_size = self.grid_size * self.grid_size * 2
        if file_size != expected_size:
            raise ValueError(f"Heightmap size mismatch: expected {expected_size}, got {file_size}")
        self.data = np.fromfile(raw_path, dtype="<u2").reshape((self.grid_size, self.grid_size))

    def sample(self, x: float, z: float) -> float:
        """
        Bilinear sample at world coordinate (x, z):
        u = (x + 2048.0) / 2.0
        v = (z + 2048.0) / 2.0
        Row 0 = South (z = -2048), Row 2048 = North (z = +2048)
        Col 0 = West (x = -2048), Col 2048 = East (x = +2048)
        """
        u = (x + self.world_half) / self.scale_xz
        v = (z + self.world_half) / self.scale_xz

        u = max(0.0, min(float(self.grid_size - 1), u))
        v = max(0.0, min(float(self.grid_size - 1), v))

        c0 = int(math.floor(u))
        r0 = int(math.floor(v))
        c1 = min(c0 + 1, self.grid_size - 1)
        r1 = min(r0 + 1, self.grid_size - 1)

        s = u - c0
        t = v - r0

        h00 = float(self.data[r0, c0]) * self.scale_y
        h10 = float(self.data[r0, c1]) * self.scale_y
        h01 = float(self.data[r1, c0]) * self.scale_y
        h11 = float(self.data[r1, c1]) * self.scale_y

        h = (1.0 - s) * (1.0 - t) * h00 + s * (1.0 - t) * h10 + (1.0 - s) * t * h01 + s * t * h11
        return h


def parse_gameplay_con(filepath: str) -> Dict[str, Any]:
    """Independent parser for GameplayObjects.con."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    templates = {}
    objects = []
    combat_areas = []

    curr_template = None
    curr_obj = None
    curr_area = None

    for line_idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.lower().startswith("rem"):
            continue

        # Split command and arg
        parts = line.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "CombatArea.create":
            if curr_area:
                combat_areas.append(curr_area)
            curr_area = {"name": arg.strip(), "points": [], "line": line_idx}
        elif cmd == "CombatArea.addAreaPoint" and curr_area:
            coords = [float(p) for p in arg.strip().split("/")]
            curr_area["points"].append(tuple(coords))

        elif cmd == "ObjectTemplate.create":
            sub = arg.strip().split()
            if len(sub) >= 2:
                curr_template = {"type": sub[0], "name": sub[1], "line": line_idx}
                templates[sub[1]] = curr_template
        elif curr_template:
            if cmd in ("ObjectTemplate.controlPointId", "ObjectTemplate.setControlPointId"):
                curr_template["controlPointId"] = int(arg.strip())
            elif cmd == "ObjectTemplate.team":
                curr_template["team"] = int(arg.strip())
            elif cmd == "ObjectTemplate.radius":
                curr_template["radius"] = float(arg.strip())
            elif cmd == "ObjectTemplate.setSpawnPositionOffset":
                curr_template["spawnPositionOffset"] = [float(p) for p in arg.strip().split("/")]
            elif cmd == "ObjectTemplate.timeToGetControl":
                curr_template["timeToGetControl"] = float(arg.strip())
            elif cmd == "ObjectTemplate.timeToLoseControl":
                curr_template["timeToLoseControl"] = float(arg.strip())

        if cmd == "Object.create":
            if curr_obj and "position" in curr_obj:
                objects.append(curr_obj)
            curr_obj = {"template": arg.strip(), "line": line_idx}
        elif curr_obj:
            if cmd == "Object.absolutePosition":
                coords = [float(p) for p in arg.strip().split("/")]
                curr_obj["position"] = tuple(coords)
            elif cmd == "Object.rotation":
                coords = [float(p) for p in arg.strip().split("/")]
                curr_obj["rotation"] = tuple(coords)
            elif cmd == "Object.layer":
                curr_obj["layer"] = int(arg.strip())

    if curr_obj and "position" in curr_obj:
        objects.append(curr_obj)
    if curr_area:
        combat_areas.append(curr_area)

    cps = []
    sps = []
    for obj in objects:
        tname = obj["template"]
        tinfo = templates.get(tname, {})
        merged = {**tinfo, **obj}
        if tinfo.get("type") == "ControlPoint":
            cps.append(merged)
        elif tinfo.get("type") == "SpawnPoint":
            sps.append(merged)

    return {
        "templates": templates,
        "objects": objects,
        "control_points": cps,
        "spawn_points": sps,
        "combat_areas": combat_areas,
    }


def point_in_poly(x: float, z: float, poly: List[Tuple[float, float]]) -> bool:
    """Ray casting algorithm for point in polygon."""
    n = len(poly)
    inside = False
    p1x, p1z = poly[0]
    for i in range(n + 1):
        p2x, p2z = poly[i % n]
        if min(p1z, p2z) < z <= max(p1z, p2z):
            if x <= max(p1x, p2x):
                if p1z != p2z:
                    xinters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
        p1x, p1z = p2x, p2z
    return inside


def min_dist_to_polygon_edges(x: float, z: float, poly: List[Tuple[float, float]]) -> float:
    """Calculates min perpendicular distance from point to any polygon segment."""
    min_d = float("inf")
    n = len(poly)
    for i in range(n):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % n]
        dx = x2 - x1
        dz = z2 - z1
        seg_len_sq = dx * dx + dz * dz
        if seg_len_sq == 0:
            d = math.hypot(x - x1, z - z1)
        else:
            t = max(0.0, min(1.0, ((x - x1) * dx + (z - z1) * dz) / seg_len_sq))
            proj_x = x1 + t * dx
            proj_z = z1 + t * dz
            d = math.hypot(x - proj_x, z - proj_z)
        if d < min_d:
            min_d = d
    return min_d


class TestAdversarialCpSpawnTopology(unittest.TestCase):
    """Empirical adversarial test suite for GameplayObjects.con topology."""

    @classmethod
    def setUpClass(cls):
        cls.sampler = IndependentBilinearHeightmapSampler(HEIGHTMAP_PATH)
        cls.gp = parse_gameplay_con(GAMEPLAY_PATH)

    # =========================================================================
    # Task 1: Control Point & Spawn Point Linkages
    # =========================================================================
    def test_cp_and_sp_counts(self):
        """Verify exactly 3 Control Points and at least 6 Spawn Points (>= 2 per CP)."""
        cps = self.gp["control_points"]
        sps = self.gp["spawn_points"]
        self.assertEqual(len(cps), 3, f"Expected exactly 3 Control Points, found {len(cps)}")
        self.assertGreaterEqual(len(sps), 6, f"Expected at least 6 Spawn Points, found {len(sps)}")

    def test_sp_to_cp_linkage_bijection(self):
        """Verify 1-to-N mapping: every SpawnPoint has matching setControlPointId on an existing CP."""
        cps = self.gp["control_points"]
        sps = self.gp["spawn_points"]
        cp_ids = {cp["controlPointId"] for cp in cps}

        self.assertEqual(len(cp_ids), 3, "Control Point IDs must be distinct")
        for sp in sps:
            sp_cpid = sp.get("controlPointId")
            self.assertIsNotNone(sp_cpid, f"SpawnPoint {sp['name']} missing controlPointId")
            self.assertIn(sp_cpid, cp_ids,
                          f"SpawnPoint {sp['name']} links to non-existent CP ID {sp_cpid}")

    def test_every_cp_has_minimum_two_spawn_points(self):
        """Verify each CP has at least 2 associated SpawnPoints to ensure fair respawning."""
        cps = self.gp["control_points"]
        sps = self.gp["spawn_points"]

        for cp in cps:
            cpid = cp["controlPointId"]
            linked_sps = [sp for sp in sps if sp.get("controlPointId") == cpid]
            self.assertGreaterEqual(
                len(linked_sps), 2,
                f"CP '{cp['name']}' (ID={cpid}) has {len(linked_sps)} spawn points, minimum required is 2"
            )

    def test_unique_cp_and_sp_identifiers(self):
        """Verify unique IDs and template names across all gameplay objects."""
        cps = self.gp["control_points"]
        sps = self.gp["spawn_points"]

        cp_names = [cp["name"] for cp in cps]
        self.assertEqual(len(cp_names), len(set(cp_names)), f"Duplicate CP names: {cp_names}")

        sp_names = [sp["name"] for sp in sps]
        self.assertEqual(len(sp_names), len(set(sp_names)), f"Duplicate SP names: {sp_names}")

        cp_ids = [cp["controlPointId"] for cp in cps]
        self.assertEqual(len(cp_ids), len(set(cp_ids)), f"Duplicate CP IDs: {cp_ids}")

    def test_sp_spawn_position_offset_structure(self):
        """Verify all SpawnPoints define setSpawnPositionOffset 0/1.25/0."""
        sps = self.gp["spawn_points"]
        for sp in sps:
            offset = sp.get("spawnPositionOffset")
            self.assertIsNotNone(offset, f"SpawnPoint {sp['name']} missing spawnPositionOffset")
            self.assertEqual(offset, [0.0, 1.25, 0.0],
                             f"SpawnPoint {sp['name']} offset must be [0.0, 1.25, 0.0], got {offset}")

    def test_sp_distance_to_parent_flagpole(self):
        """Verify SP distance to parent flagpole is >= 3.0m (no collision) and <= 120.0m (tactical range)."""
        cps = {cp["controlPointId"]: cp for cp in self.gp["control_points"]}
        sps = self.gp["spawn_points"]

        for sp in sps:
            cpid = sp["controlPointId"]
            parent_cp = cps[cpid]
            dist = math.hypot(sp["position"][0] - parent_cp["position"][0],
                              sp["position"][2] - parent_cp["position"][2])
            self.assertGreaterEqual(
                dist, 3.0,
                f"SpawnPoint {sp['name']} is too close ({dist:.2f}m < 3.0m) to parent CP {parent_cp['name']}"
            )
            self.assertLessEqual(
                dist, 120.0,
                f"SpawnPoint {sp['name']} is too far ({dist:.2f}m > 120.0m) from parent CP {parent_cp['name']}"
            )

    def test_inter_spawn_separation_distance(self):
        """Verify spawn points sharing a CP are separated by >= 2.0m to prevent telefragging."""
        cps = self.gp["control_points"]
        sps = self.gp["spawn_points"]

        for cp in cps:
            cpid = cp["controlPointId"]
            group = [sp for sp in sps if sp.get("controlPointId") == cpid]
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    sp1, sp2 = group[i], group[j]
                    d = math.hypot(sp1["position"][0] - sp2["position"][0],
                                   sp1["position"][2] - sp2["position"][2])
                    self.assertGreaterEqual(
                        d, 2.0,
                        f"Spawn points {sp1['name']} and {sp2['name']} too close ({d:.2f}m < 2.0m)"
                    )

    # =========================================================================
    # Task 2: Elevation Grounding Precision (Independent Bilinear Sampling)
    # =========================================================================
    def test_control_point_elevation_grounding_precision(self):
        """Verify CP Y matches independent bilinear sampled terrain elevation within +-0.05m."""
        cps = self.gp["control_points"]
        max_error = 0.05

        for cp in cps:
            x, y, z = cp["position"]
            terrain_y = self.sampler.sample(x, z)
            err = abs(y - terrain_y)
            self.assertLessEqual(
                err, max_error,
                f"ControlPoint {cp['name']} Y={y:.3f} deviates from terrain Y={terrain_y:.3f} by {err:.3f}m (> {max_error}m)"
            )

    def test_spawn_point_elevation_grounding_precision(self):
        """Verify SP Y matches terrain elevation within +-0.05m, and effective spawn Y = terrain + 1.25m +- 0.05m."""
        sps = self.gp["spawn_points"]
        max_error = 0.05

        for sp in sps:
            x, y, z = sp["position"]
            terrain_y = self.sampler.sample(x, z)
            # Direct base position error against terrain ground
            ground_err = abs(y - terrain_y)
            self.assertLessEqual(
                ground_err, max_error,
                f"SpawnPoint {sp['name']} base Y={y:.3f} deviates from terrain Y={terrain_y:.3f} by {ground_err:.3f}m (> {max_error}m)"
            )

            # Effective player capsule elevation: base Y + spawnPositionOffset Y
            offset_y = sp.get("spawnPositionOffset", [0, 1.25, 0])[1]
            effective_y = y + offset_y
            target_effective_y = terrain_y + 1.25
            effective_err = abs(effective_y - target_effective_y)
            self.assertLessEqual(
                effective_err, max_error,
                f"SpawnPoint {sp['name']} effective Y={effective_y:.3f} deviates from target {target_effective_y:.3f} by {effective_err:.3f}m (> {max_error}m)"
            )

    # =========================================================================
    # Task 3: Base Balance & Focal Distance
    # =========================================================================
    def test_focal_point_control_point_position(self):
        """Verify neutral contested CP is located at Golovec Pass (0, 1365) within 15.0m."""
        cps = self.gp["control_points"]
        pass_cp = next((cp for cp in cps if cp.get("team") == 0), None)
        self.assertIsNotNone(pass_cp, "Missing contested neutral Control Point (team 0)")

        x, y, z = pass_cp["position"]
        focal_x, focal_z = 0.0, 1365.0
        dist = math.hypot(x - focal_x, z - focal_z)
        self.assertLessEqual(
            dist, 15.0,
            f"Neutral CP '{pass_cp['name']}' at ({x}, {z}) is {dist:.2f}m from focal point (0, 1365)"
        )

    def test_base_opposition_across_focal_pass(self):
        """Verify EU (Team 1) and MEC (Team 2) bases oppose each other across Z=1365."""
        cps = self.gp["control_points"]
        eu_cp = next((cp for cp in cps if cp.get("team") == 1), None)
        mec_cp = next((cp for cp in cps if cp.get("team") == 2), None)

        self.assertIsNotNone(eu_cp, "EU CP (team 1) missing")
        self.assertIsNotNone(mec_cp, "MEC CP (team 2) missing")

        eu_z = eu_cp["position"][2]
        mec_z = mec_cp["position"][2]

        self.assertLess(eu_z, 1365.0, f"EU Base Z={eu_z} should be south of Pass (Z < 1365)")
        self.assertGreater(mec_z, 1365.0, f"MEC Base Z={mec_z} should be north of Pass (Z > 1365)")

    def test_base_balance_travel_distance_symmetry(self):
        """Verify EU and MEC bases have symmetric travel distance to Golovec Pass (Delta < 20%)."""
        cps = self.gp["control_points"]
        eu_cp = next(cp for cp in cps if cp.get("team") == 1)
        pass_cp = next(cp for cp in cps if cp.get("team") == 0)
        mec_cp = next(cp for cp in cps if cp.get("team") == 2)

        p_x, p_y, p_z = pass_cp["position"]
        eu_x, eu_y, eu_z = eu_cp["position"]
        mec_x, mec_y, mec_z = mec_cp["position"]

        # 2D horizontal travel distance
        d_eu_2d = math.hypot(eu_x - p_x, eu_z - p_z)
        d_mec_2d = math.hypot(mec_x - p_x, mec_z - p_z)

        # 3D spatial travel distance
        d_eu_3d = math.sqrt((eu_x - p_x)**2 + (eu_y - p_y)**2 + (eu_z - p_z)**2)
        d_mec_3d = math.sqrt((mec_x - p_x)**2 + (mec_y - p_y)**2 + (mec_z - p_z)**2)

        # Relative delta = |d1 - d2| / max(d1, d2)
        delta_2d = abs(d_eu_2d - d_mec_2d) / max(d_eu_2d, d_mec_2d)
        delta_3d = abs(d_eu_3d - d_mec_3d) / max(d_eu_3d, d_mec_3d)

        self.assertLess(
            delta_2d, 0.20,
            f"2D base distance asymmetry {delta_2d * 100:.2f}% exceeds 20% limit (EU: {d_eu_2d:.1f}m, MEC: {d_mec_2d:.1f}m)"
        )
        self.assertLess(
            delta_3d, 0.20,
            f"3D base distance asymmetry {delta_3d * 100:.2f}% exceeds 20% limit (EU: {d_eu_3d:.1f}m, MEC: {d_mec_3d:.1f}m)"
        )

    def test_bases_and_spawns_above_water_table(self):
        """Verify all CPs and SPs are located on dry ground above the water table (Y >= 270.0m)."""
        cps = self.gp["control_points"]
        sps = self.gp["spawn_points"]

        water_elevation = 270.0
        if os.path.exists(TERRAIN_PATH):
            with open(TERRAIN_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                for line in content.splitlines():
                    if "setwaterelevation" in line.lower():
                        parts = line.split()
                        if len(parts) > 1:
                            water_elevation = float(parts[1])

        for cp in cps:
            x, y, z = cp["position"]
            self.assertGreaterEqual(
                y, water_elevation,
                f"ControlPoint {cp['name']} Y={y:.2f} is submerged or at water table ({water_elevation}m)"
            )
            terrain_y = self.sampler.sample(x, z)
            self.assertGreaterEqual(
                terrain_y, water_elevation,
                f"ControlPoint {cp['name']} terrain Y={terrain_y:.2f} is submerged"
            )

        for sp in sps:
            x, y, z = sp["position"]
            self.assertGreaterEqual(
                y, water_elevation,
                f"SpawnPoint {sp['name']} Y={y:.2f} is submerged or at water table ({water_elevation}m)"
            )
            terrain_y = self.sampler.sample(x, z)
            self.assertGreaterEqual(
                terrain_y, water_elevation,
                f"SpawnPoint {sp['name']} terrain Y={terrain_y:.2f} is submerged"
            )

    # =========================================================================
    # Task 4: Spatial Containment & Combat Area Buffer
    # =========================================================================
    def test_combat_area_enclosure_and_buffer_margin(self):
        """Verify all CPs and SPs are inside the combat area with a safety buffer margin > 50.0m."""
        areas = self.gp["combat_areas"]
        self.assertGreater(len(areas), 0, "No combat areas found")
        poly = areas[0]["points"]

        for cp in self.gp["control_points"]:
            x, _, z = cp["position"]
            self.assertTrue(point_in_poly(x, z, poly), f"CP {cp['name']} is outside CombatArea!")
            margin = min_dist_to_polygon_edges(x, z, poly)
            self.assertGreaterEqual(
                margin, 50.0,
                f"CP {cp['name']} buffer to boundary is too small ({margin:.1f}m < 50.0m)"
            )

        for sp in self.gp["spawn_points"]:
            x, _, z = sp["position"]
            self.assertTrue(point_in_poly(x, z, poly), f"SP {sp['name']} is outside CombatArea!")
            margin = min_dist_to_polygon_edges(x, z, poly)
            self.assertGreaterEqual(
                margin, 50.0,
                f"SP {sp['name']} buffer to boundary is too small ({margin:.1f}m < 50.0m)"
            )


if __name__ == "__main__":
    unittest.main()
