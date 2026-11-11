"""
Tier 2: Boundary & Corner Cases Test Suite for BF2 Slovenia (Golovec) Level Package.
Covers:
- Coordinate bounds check: All static objects, CPs, SPs, and CombatArea in [-2048.0, 2048.0].
- Heightmap bounds check: Elevation Y >= 270.0m, <= 455.0m, matching ground terrain height.
- Overgrowth mask check: Exactly 2049 x 2049 = 4,198,401 bytes uint8 binary mask.
- CombatArea boundary check: Encloses focal point (0, 1365), positive signed area (CCW winding).
- Control Points & Spawn Points: Valid team IDs (1, 2, 0), unique CP IDs, offset 0/1.25/0.
"""

import os
import unittest
import numpy as np

from con_parser import ConParser, HeightmapSampler, polygon_signed_area, point_in_polygon, LEVEL_DIR

HEIGHTMAP_PATH = "/home/ator/BF2/Heightmap.raw"


class TestTier2BoundaryCorner(unittest.TestCase):
    """Tier 2: Comprehensive boundary, corner-case, and mathematical integrity tests."""

    @classmethod
    def setUpClass(cls):
        cls.heightmap_sampler = None
        if os.path.isfile(HEIGHTMAP_PATH):
            cls.heightmap_sampler = HeightmapSampler(HEIGHTMAP_PATH)

    # -------------------------------------------------------------------------
    # 1. Coordinate Bounds: [-2048.0, 2048.0] (5 tests)
    # -------------------------------------------------------------------------
    def test_static_objects_x_within_bounds(self):
        """Verify all static building instances have X coordinates strictly in [-2048.0, 2048.0]."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 0, "No static objects parsed in StaticObjects.con")
        for obj in objects:
            x, _, _ = obj["position"]
            self.assertTrue(-2048.0 <= x <= 2048.0,
                            f"Static object at line {obj['line']} X={x} exceeds bounds [-2048, 2048]")

    def test_static_objects_z_within_bounds(self):
        """Verify all static building instances have Z coordinates strictly in [-2048.0, 2048.0]."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 0, "No static objects parsed in StaticObjects.con")
        for obj in objects:
            _, _, z = obj["position"]
            self.assertTrue(-2048.0 <= z <= 2048.0,
                            f"Static object at line {obj['line']} Z={z} exceeds bounds [-2048, 2048]")

    def test_control_points_xz_within_bounds(self):
        """Verify all ControlPoint instances have (X, Z) coordinates strictly in [-2048.0, 2048.0]."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        self.assertGreater(len(cps), 0, "No control points parsed in GameplayObjects.con")
        for cp in cps:
            x, _, z = cp["position"]
            self.assertTrue(-2048.0 <= x <= 2048.0 and -2048.0 <= z <= 2048.0,
                            f"ControlPoint {cp.get('name', 'CP')} at ({x}, {z}) exceeds bounds [-2048, 2048]")

    def test_spawn_points_xz_within_bounds(self):
        """Verify all SpawnPoint instances have (X, Z) coordinates strictly in [-2048.0, 2048.0]."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        sps = gameplay["spawn_points"]
        self.assertGreater(len(sps), 0, "No spawn points parsed in GameplayObjects.con")
        for sp in sps:
            x, _, z = sp["position"]
            self.assertTrue(-2048.0 <= x <= 2048.0 and -2048.0 <= z <= 2048.0,
                            f"SpawnPoint {sp.get('name', 'SP')} at ({x}, {z}) exceeds bounds [-2048, 2048]")

    def test_combat_area_vertices_within_bounds(self):
        """Verify all CombatArea polygon vertices have (X, Z) strictly in [-2048.0, 2048.0]."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        areas = parser.parse_combat_areas()
        self.assertGreater(len(areas), 0, "No combat areas parsed in GameplayObjects.con")
        for area in areas:
            for pt_idx, (x, z) in enumerate(area["points"]):
                self.assertTrue(-2048.0 <= x <= 2048.0 and -2048.0 <= z <= 2048.0,
                                f"CombatArea vertex {pt_idx} ({x}, {z}) exceeds bounds [-2048, 2048]")

    # -------------------------------------------------------------------------
    # 2. Heightmap & Elevation Bounds (5 tests)
    # -------------------------------------------------------------------------
    def test_static_objects_elevation_above_water(self):
        """Verify all static building instances have elevation Y >= 270.0m (above water level)."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 0, "No static objects parsed in StaticObjects.con")
        for obj in objects:
            _, y, _ = obj["position"]
            self.assertGreaterEqual(y, 270.0,
                                    f"Static object at line {obj['line']} elevation {y}m is below water level (270.0m)")

    def test_static_objects_elevation_below_peak(self):
        """Verify all static building instances have elevation Y <= 455.0m (below Golovec peak)."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 0, "No static objects parsed in StaticObjects.con")
        for obj in objects:
            _, y, _ = obj["position"]
            self.assertLessEqual(y, 455.0,
                                 f"Static object at line {obj['line']} elevation {y}m exceeds max peak height (455.0m)")

    def test_static_objects_elevation_matches_heightmap(self):
        """Verify static building elevation Y matches ground elevation sampled from Heightmap.raw (+-0.75m)."""
        self.assertIsNotNone(self.heightmap_sampler, f"Heightmap missing at {HEIGHTMAP_PATH}")
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        objects = parser.parse_static_objects()
        self.assertGreater(len(objects), 0, "No static objects parsed in StaticObjects.con")
        # Check tolerance across objects
        mismatches = []
        for obj in objects:
            x, y, z = obj["position"]
            expected_y = self.heightmap_sampler.sample_bilinear(x, z)
            diff = abs(y - expected_y)
            if diff > 0.75:
                mismatches.append(f"Line {obj['line']} pos=({x:.1f},{y:.2f},{z:.1f}) terrain_y={expected_y:.2f} (diff={diff:.2f}m)")
        self.assertEqual(len(mismatches), 0, f"Found {len(mismatches)} elevation grounding mismatches: {mismatches[:5]}")

    def test_control_points_elevation_matches_heightmap(self):
        """Verify ControlPoint elevation Y matches ground elevation sampled from Heightmap.raw (+-0.5m)."""
        self.assertIsNotNone(self.heightmap_sampler, f"Heightmap missing at {HEIGHTMAP_PATH}")
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        self.assertGreater(len(cps), 0, "No control points parsed in GameplayObjects.con")
        for cp in cps:
            x, y, z = cp["position"]
            expected_y = self.heightmap_sampler.sample_bilinear(x, z)
            diff = abs(y - expected_y)
            self.assertLessEqual(diff, 0.5,
                                 f"ControlPoint {cp.get('name', 'CP')} elevation {y:.2f}m deviates from terrain {expected_y:.2f}m by {diff:.2f}m")

    def test_terrain_con_water_elevation_is_270(self):
        """Verify Terrain.con specifies water elevation at 270.0m matching plain hydrology."""
        p = os.path.join(LEVEL_DIR, "Terrain.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("terrain.setWaterElevation 270.0", content,
                      "Terrain.con must define 'terrain.setWaterElevation 270.0'")

    # -------------------------------------------------------------------------
    # 3. Overgrowth Mask Check (5 tests)
    # -------------------------------------------------------------------------
    def test_overgrowth_raw_exact_byte_count(self):
        """Verify Overgrowth/Overgrowth.raw is exactly 2049 x 2049 = 4,198,401 bytes."""
        p = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        sz = os.path.getsize(p)
        self.assertEqual(sz, 4198401, f"Overgrowth.raw byte size mismatch: expected 4198401 bytes, got {sz}")

    def test_overgrowth_raw_shape_dimensions(self):
        """Verify Overgrowth.raw reshapes perfectly into (2049, 2049) uint8 array without header."""
        p = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        data = np.fromfile(p, dtype=np.uint8)
        self.assertEqual(data.size, 2049 * 2049, f"Unexpected element count: {data.size}")
        grid = data.reshape((2049, 2049))
        self.assertEqual(grid.shape, (2049, 2049))

    def test_overgrowth_raw_uint8_data_range(self):
        """Verify Overgrowth.raw contains unsigned 8-bit density values in [0, 255]."""
        p = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        data = np.fromfile(p, dtype=np.uint8)
        self.assertGreaterEqual(int(data.min()), 0)
        self.assertLessEqual(int(data.max()), 255)

    def test_overgrowth_raw_non_trivial_content(self):
        """Verify Overgrowth.raw is not an empty all-zero dummy array."""
        p = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        data = np.fromfile(p, dtype=np.uint8)
        self.assertGreater(int(data.max()), 0, "Overgrowth.raw is all zeros (no vegetation density present)")

    def test_overgrowth_raw_dense_canopy_on_golovec_ridge(self):
        """Verify Golovec forested ridge region contains active foliage density."""
        p = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        data = np.fromfile(p, dtype=np.uint8).reshape((2049, 2049))
        # Golovec ridge center around X=0, Z=1365 -> col=1024, row=1707
        sub_grid = data[1650:1750, 974:1074]
        mean_density = float(np.mean(sub_grid))
        self.assertGreater(mean_density, 0.0, "Expected non-zero vegetation density in Golovec ridge area")

    # -------------------------------------------------------------------------
    # 4. CombatArea Boundary Check (5 tests)
    # -------------------------------------------------------------------------
    def test_combat_area_encloses_focal_point(self):
        """Verify CombatArea boundary polygon encloses Golovec focal point (0.0, 1365.0)."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        areas = parser.parse_combat_areas()
        self.assertGreater(len(areas), 0, "No combat areas parsed in GameplayObjects.con")
        area = areas[0]
        pts = area["points"]
        self.assertGreaterEqual(len(pts), 3, "CombatArea polygon must have at least 3 vertices")
        enclosed = point_in_polygon(0.0, 1365.0, pts)
        self.assertTrue(enclosed, f"CombatArea '{area['name']}' fails to enclose focal point (0.0, 1365.0)")

    def test_combat_area_counter_clockwise_winding(self):
        """Verify CombatArea polygon vertices have positive signed area (counter-clockwise winding)."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        areas = parser.parse_combat_areas()
        self.assertGreater(len(areas), 0, "No combat areas parsed in GameplayObjects.con")
        for area in areas:
            pts = area["points"]
            sarea = polygon_signed_area(pts)
            self.assertGreater(sarea, 0.0,
                               f"CombatArea '{area['name']}' has negative/zero signed area ({sarea:.1f}). "
                               f"Clockwise winding causes Refractor 2 out-of-bounds desertion bug!")

    def test_combat_area_minimum_playable_area(self):
        """Verify CombatArea playable area is at least 500,000 m^2 for multi-base conquest warfare."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        areas = parser.parse_combat_areas()
        self.assertGreater(len(areas), 0, "No combat areas parsed in GameplayObjects.con")
        area = areas[0]
        sarea = abs(polygon_signed_area(area["points"]))
        self.assertGreaterEqual(sarea, 500000.0, f"CombatArea '{area['name']}' area {sarea} m^2 is too cramped (< 500k m^2)")

    def test_combat_area_time_allowed_outside(self):
        """Verify CombatAreaManager.timeAllowedOutside is set to 10.0 seconds."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertRegex(content, r"CombatAreaManager\.timeAllowedOutside\s+10(\.0*)?",
                         "GameplayObjects.con must define CombatAreaManager.timeAllowedOutside 10.0")

    def test_combat_area_manager_active(self):
        """Verify CombatAreaManager.use is enabled (1)."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertRegex(content, r"CombatAreaManager\.use\s+1",
                         "GameplayObjects.con must define CombatAreaManager.use 1")

    # -------------------------------------------------------------------------
    # 5. Control Points & Spawn Points Attributes (5 tests)
    # -------------------------------------------------------------------------
    def test_control_points_valid_teams(self):
        """Verify Control Points have valid team assignments (0=Neutral, 1=Team 1, 2=Team 2)."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        self.assertGreater(len(cps), 0, "No control points parsed in GameplayObjects.con")
        for cp in cps:
            team = cp.get("team", -1)
            self.assertIn(team, [0, 1, 2], f"ControlPoint {cp.get('name')} has invalid team ID {team}")

    def test_control_points_unique_ids(self):
        """Verify every ControlPoint has a unique integer ID."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        self.assertGreater(len(cps), 0, "No control points parsed in GameplayObjects.con")
        ids = [cp["controlPointId"] for cp in cps if "controlPointId" in cp]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate ControlPoint IDs found: {ids}")

    def test_spawn_points_offset_is_one_point_two_five(self):
        """Verify SpawnPoints specify ObjectTemplate.setSpawnPositionOffset 0/1.25/0 to avoid falling through terrain."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        sps = gameplay["spawn_points"]
        self.assertGreater(len(sps), 0, "No spawn points parsed in GameplayObjects.con")
        for sp in sps:
            offset = sp.get("spawnPositionOffset")
            self.assertIsNotNone(offset, f"SpawnPoint {sp.get('name')} missing spawnPositionOffset")
            self.assertEqual(offset, [0.0, 1.25, 0.0],
                             f"SpawnPoint {sp.get('name')} offset {offset} must be [0.0, 1.25, 0.0]")

    def test_control_points_positive_capture_radius(self):
        """Verify ControlPoint capture radius is between 15.0m and 50.0m."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        self.assertGreater(len(cps), 0, "No control points parsed in GameplayObjects.con")
        for cp in cps:
            rad = cp.get("radius", 0.0)
            self.assertTrue(15.0 <= rad <= 50.0, f"ControlPoint {cp.get('name')} radius {rad}m out of bounds [15, 50]")

    def test_control_points_positive_capture_time(self):
        """Verify ControlPoint timeToGetControl is between 10.0s and 30.0s."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        self.assertGreater(len(cps), 0, "No control points parsed in GameplayObjects.con")
        for cp in cps:
            t = cp.get("timeToGetControl", 0.0)
            self.assertTrue(10.0 <= t <= 30.0, f"ControlPoint {cp.get('name')} timeToGetControl {t}s out of bounds [10, 30]")


if __name__ == "__main__":
    unittest.main()
