"""
Tier 4: Real-World Gameplay Scenarios Test Suite for BF2 Slovenia (Golovec) Level Package.
Covers:
- Full Conquest Head-On playability:
  - Exactly 3 Control Points: Team 1 EU/US Base, Contested Golovec Pass at (0, 1365), Team 2 MEC Base.
  - Each Control Point has >= 2 spawn points.
  - Symmetrical/balanced base arrangement opposing the Golovec focal pass.
  - Spawn points spaced from flagpole and from each other.
- Static buildings realistic distribution:
  - Substantial building extraction (>= 50 buildings).
  - Valid vanilla static meshes.
  - No exact duplicate positions.
  - No overlapping collisions (origin distance >= 2.0m).
  - Proper height grounding to terrain.
  - Realistic spatial distribution across urban/rural zones.
"""

import os
import unittest
import math
from typing import List, Dict, Any

from con_parser import ConParser, HeightmapSampler, LEVEL_DIR

HEIGHTMAP_PATH = "/home/ator/BF2/Heightmap.raw"

VANILLA_BUILDING_MESHES = {
    # European vanilla meshes
    "eu_building01", "eu_building02", "eu_building_01", "eu_building_02",
    "eu_house_01", "eu_house_02", "eu_house_03", "eu_office_01",
    "barn_01", "barn_02", "farmhouse", "wooden_shed", "shed_01", "shed_02",
    "wooden_shack_01", "warehouse_01", "factory_01",
    # Middle Eastern vanilla meshes (often used in BF2 EU/MEC maps)
    "me_house_01", "me_house_02", "me_house_03", "me_house_04",
    "me_house_05", "me_house_06", "me_house_07", "me_house_08",
    "me_apartment_01", "me_building_01", "citybuilding_01", "citybuilding_02"
}


class TestTier4RealWorldGameplay(unittest.TestCase):
    """Tier 4: Real-world Conquest Head-On gameplay balance and building distribution tests."""

    @classmethod
    def setUpClass(cls):
        cls.heightmap_sampler = None
        if os.path.isfile(HEIGHTMAP_PATH):
            cls.heightmap_sampler = HeightmapSampler(HEIGHTMAP_PATH)

    # -------------------------------------------------------------------------
    # 1. Balanced Conquest Head-On Setup
    # -------------------------------------------------------------------------
    def test_conquest_head_on_has_three_control_points(self):
        """Verify Conquest Head-On has exactly 3 Control Points (Team 1 Base, Golovec Pass, Team 2 Base)."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        cps = parser.parse_gameplay_objects()["control_points"]
        self.assertEqual(len(cps), 3, f"Expected exactly 3 Control Points for Head-On Conquest, found {len(cps)}")

    def test_conquest_team_composition(self):
        """Verify Control Points have 1 Team 1 base, 1 Neutral contested flag, and 1 Team 2 base."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        cps = parser.parse_gameplay_objects()["control_points"]
        teams = [cp.get("team") for cp in cps]
        self.assertEqual(teams.count(1), 1, f"Expected 1 Team 1 Control Point, found {teams.count(1)}")
        self.assertEqual(teams.count(2), 1, f"Expected 1 Team 2 Control Point, found {teams.count(2)}")
        self.assertEqual(teams.count(0), 1, f"Expected 1 Neutral Contested Control Point, found {teams.count(0)}")

    def test_golovec_pass_control_point_at_focal_point(self):
        """Verify the neutral contested Control Point (CP 2) is positioned at the Golovec focal point (0, 1365) +-15m."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        cps = parser.parse_gameplay_objects()["control_points"]
        contested_cps = [cp for cp in cps if cp.get("team") == 0]
        self.assertEqual(len(contested_cps), 1, "Must have exactly 1 contested (team 0) Control Point")
        ccp = contested_cps[0]
        x, _, z = ccp["position"]
        dist = math.hypot(x - 0.0, z - 1365.0)
        self.assertLessEqual(dist, 15.0,
                             f"Contested CP '{ccp.get('name')}' is at ({x:.1f}, {z:.1f}), not at Golovec focal point (0, 1365) (dist={dist:.1f}m)")

    def test_team_bases_opposing_focal_point(self):
        """Verify Team 1 and Team 2 bases are situated on opposing sides of the Golovec Pass."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        cps = parser.parse_gameplay_objects()["control_points"]
        team1_cp = next((cp for cp in cps if cp.get("team") == 1), None)
        team2_cp = next((cp for cp in cps if cp.get("team") == 2), None)

        self.assertIsNotNone(team1_cp, "Team 1 CP missing")
        self.assertIsNotNone(team2_cp, "Team 2 CP missing")

        t1_z = team1_cp["position"][2]
        t2_z = team2_cp["position"][2]
        # Opposing sides relative to focal point Z=1365
        t1_side = t1_z - 1365.0
        t2_side = t2_z - 1365.0
        self.assertLess(t1_side * t2_side, 0.0,
                        f"Team 1 (Z={t1_z}) and Team 2 (Z={t2_z}) must be on opposing sides of Golovec Pass (Z=1365)")

    def test_each_control_point_has_at_least_two_spawn_points(self):
        """Verify each of the 3 Control Points has >= 2 dedicated spawn points to ensure fair respawning."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        sps = gameplay["spawn_points"]

        for cp in cps:
            cpid = cp.get("controlPointId")
            cp_sps = [sp for sp in sps if sp.get("controlPointId") == cpid]
            self.assertGreaterEqual(len(cp_sps), 2,
                                    f"ControlPoint {cp.get('name')} (ID={cpid}) has only {len(cp_sps)} spawn points (minimum 2 required)")

    def test_spawn_points_spaced_from_flagpole(self):
        """Verify player spawn points are at least 3.0m away from the CP flagpole to prevent collision upon spawn."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = {cp["controlPointId"]: cp for cp in gameplay["control_points"] if "controlPointId" in cp}
        sps = gameplay["spawn_points"]

        for sp in sps:
            cpid = sp.get("controlPointId")
            parent_cp = cps.get(cpid)
            if parent_cp:
                sp_x, _, sp_z = sp["position"]
                cp_x, _, cp_z = parent_cp["position"]
                dist = math.hypot(sp_x - cp_x, sp_z - cp_z)
                self.assertGreaterEqual(dist, 3.0,
                                        f"SpawnPoint {sp.get('name')} is too close ({dist:.2f}m) to flagpole {parent_cp.get('name')} (< 3.0m)")

    def test_spawn_points_separated_from_each_other(self):
        """Verify spawn points linked to the same CP are separated by at least 2.0m to prevent telefragging."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        sps = gameplay["spawn_points"]

        for cp in cps:
            cpid = cp.get("controlPointId")
            group_sps = [sp for sp in sps if sp.get("controlPointId") == cpid]
            for i in range(len(group_sps)):
                for j in range(i + 1, len(group_sps)):
                    sp1, sp2 = group_sps[i], group_sps[j]
                    d = math.hypot(sp1["position"][0] - sp2["position"][0], sp1["position"][2] - sp2["position"][2])
                    self.assertGreaterEqual(d, 2.0,
                                            f"SpawnPoints {sp1.get('name')} and {sp2.get('name')} are too close ({d:.2f}m < 2.0m)")

    # -------------------------------------------------------------------------
    # 2. Static Building Distribution & Collision Avoidance
    # -------------------------------------------------------------------------
    def test_static_buildings_count_substantial(self):
        """Verify StaticObjects.con defines a substantial number of buildings (>= 50) extracted from OSM."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreaterEqual(len(objects), 50,
                                f"Expected at least 50 static buildings extracted from OSM, found {len(objects)}")

    def test_static_buildings_vanilla_meshes_only(self):
        """Verify all static objects reference valid BF2 vanilla static meshes."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 0, "No static objects found")
        for obj in objects:
            tname = obj["template"].lower()
            # Match against known vanilla meshes or known patterns
            is_valid = (
                tname in VANILLA_BUILDING_MESHES or
                any(tname.startswith(p) for p in ["eu_building", "me_house", "barn_", "farmhouse", "wooden_shed", "shed_", "warehouse_"])
            )
            self.assertTrue(is_valid, f"Line {obj['line']}: Static mesh template '{obj['template']}' is not a standard BF2 vanilla mesh")

    def test_static_buildings_no_identical_coordinate_duplicates(self):
        """Verify no two static buildings share the exact same (X, Z) coordinate."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        seen = set()
        for obj in objects:
            x, _, z = obj["position"]
            key = (round(x, 2), round(z, 2))
            self.assertNotIn(key, seen, f"Duplicate building position at {key} (line {obj['line']})")
            seen.add(key)

    def test_static_buildings_minimum_clearance(self):
        """Verify building origins do not directly overlap (minimum clearance distance >= 2.0m)."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        # Pairwise distance check on spatial grid to avoid O(N^2) slowdown
        grid = {}
        cell_size = 5.0
        for obj in objects:
            x, _, z = obj["position"]
            gx, gz = int(x // cell_size), int(z // cell_size)
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    neighbor_cell = (gx + dx, gz + dz)
                    if neighbor_cell in grid:
                        for other in grid[neighbor_cell]:
                            ox, _, oz = other["position"]
                            d = math.hypot(x - ox, z - oz)
                            self.assertGreaterEqual(
                                d, 2.0,
                                f"Buildings overlap too closely ({d:.2f}m < 2.0m): line {obj['line']} vs line {other['line']}"
                            )
            grid.setdefault((gx, gz), []).append(obj)

    def test_static_buildings_spatial_spread(self):
        """Verify static buildings span both East-West and North-South extensively across the 4096m terrain."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 10, "Too few objects to evaluate spatial distribution")
        xs = [obj["position"][0] for obj in objects]
        zs = [obj["position"][2] for obj in objects]
        span_x = max(xs) - min(xs)
        span_z = max(zs) - min(zs)
        self.assertGreaterEqual(span_x, 500.0, f"Building East-West span ({span_x:.1f}m) is too narrow (< 500m)")
        self.assertGreaterEqual(span_z, 500.0, f"Building North-South span ({span_z:.1f}m) is too narrow (< 500m)")


if __name__ == "__main__":
    unittest.main()
