"""
Tier 3: Cross-Feature Combinations Test Suite for BF2 Slovenia (Golovec) Level Package.
Covers:
- SpawnPoints referencing valid ControlPoint IDs (ObjectTemplate.setControlPointId).
- Master init.con executing all child scripts (Heightdata, Terrain, Sky, Water, StaticObjects, OvergrowthSystem, GameplayObjects).
- CombatArea enclosing all ControlPoints and SpawnPoints.
- Overgrowth materials and types in OvergrowthSystem.con matching engine definitions and vanilla tree geometries.
"""

import os
import unittest
import math
from typing import List, Tuple

from con_parser import ConParser, point_in_polygon, LEVEL_DIR


class TestTier3CrossFeature(unittest.TestCase):
    """Tier 3: Cross-feature integrations and referential integrity tests."""

    # -------------------------------------------------------------------------
    # 1. SpawnPoints & ControlPoints Referential Integrity
    # -------------------------------------------------------------------------
    def test_all_spawn_points_reference_valid_cp_ids(self):
        """Verify every SpawnPoint references an existing ControlPoint ID via ObjectTemplate.setControlPointId."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        sps = gameplay["spawn_points"]

        self.assertGreater(len(cps), 0, "No control points found")
        self.assertGreater(len(sps), 0, "No spawn points found")

        valid_cp_ids = {cp["controlPointId"] for cp in cps if "controlPointId" in cp}
        for sp in sps:
            sp_cpid = sp.get("controlPointId")
            self.assertIsNotNone(sp_cpid, f"SpawnPoint {sp.get('name')} missing controlPointId")
            self.assertIn(sp_cpid, valid_cp_ids,
                          f"SpawnPoint {sp.get('name')} references non-existent CP ID {sp_cpid}. Valid IDs: {valid_cp_ids}")

    def test_every_control_point_has_associated_spawn_points(self):
        """Verify that every ControlPoint has at least one associated SpawnPoint."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        gameplay = parser.parse_gameplay_objects()
        cps = gameplay["control_points"]
        sps = gameplay["spawn_points"]

        sp_cp_ids = {sp.get("controlPointId") for sp in sps}
        for cp in cps:
            cpid = cp.get("controlPointId")
            self.assertIn(cpid, sp_cp_ids, f"ControlPoint {cp.get('name')} (ID={cpid}) has no associated spawn points!")

    def test_spawn_points_proximity_to_parent_control_point(self):
        """Verify spawn points are located within reasonable tactical proximity (<= 120m) of their parent CP."""
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
                self.assertLessEqual(dist, 120.0,
                                     f"SpawnPoint {sp.get('name')} is {dist:.1f}m away from its parent CP {parent_cp.get('name')} (exceeds 120m limit)")

    # -------------------------------------------------------------------------
    # 2. Master init.con Conductor Scripts Invocation
    # -------------------------------------------------------------------------
    def test_init_con_runs_heightdata(self):
        """Verify init.con invokes Heightdata.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("Heightdata.con", runs, "init.con must run Heightdata.con")

    def test_init_con_runs_terrain(self):
        """Verify init.con invokes Terrain.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("Terrain.con", runs, "init.con must run Terrain.con")

    def test_init_con_runs_sky(self):
        """Verify init.con invokes Sky.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("Sky.con", runs, "init.con must run Sky.con")

    def test_init_con_runs_water(self):
        """Verify init.con invokes Water.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("Water.con", runs, "init.con must run Water.con")

    def test_init_con_runs_staticobjects(self):
        """Verify init.con invokes StaticObjects.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("StaticObjects.con", runs, "init.con must run StaticObjects.con")

    def test_init_con_runs_overgrowthsystem(self):
        """Verify init.con invokes OvergrowthSystem.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("OvergrowthSystem.con", runs, "init.con must run OvergrowthSystem.con")

    def test_init_con_runs_gameplayobjects(self):
        """Verify init.con invokes GameplayObjects.con."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        runs = ConParser(p).parse_run_commands()
        self.assertIn("GameplayObjects.con", runs, "init.con must run GameplayObjects.con")

    # -------------------------------------------------------------------------
    # 3. CombatArea Spatial Enclosure of Gameplay Entities
    # -------------------------------------------------------------------------
    def test_combat_area_encloses_all_control_points(self):
        """Verify CombatArea polygon encloses 100% of ControlPoints."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        areas = parser.parse_combat_areas()
        gameplay = parser.parse_gameplay_objects()
        self.assertGreater(len(areas), 0, "No combat area found")
        pts = areas[0]["points"]
        for cp in gameplay["control_points"]:
            x, _, z = cp["position"]
            self.assertTrue(point_in_polygon(x, z, pts),
                            f"ControlPoint {cp.get('name')} at ({x}, {z}) falls OUTSIDE the CombatArea polygon!")

    def test_combat_area_encloses_all_spawn_points(self):
        """Verify CombatArea polygon encloses 100% of player SpawnPoints."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        areas = parser.parse_combat_areas()
        gameplay = parser.parse_gameplay_objects()
        self.assertGreater(len(areas), 0, "No combat area found")
        pts = areas[0]["points"]
        for sp in gameplay["spawn_points"]:
            x, _, z = sp["position"]
            self.assertTrue(point_in_polygon(x, z, pts),
                            f"SpawnPoint {sp.get('name')} at ({x}, {z}) falls OUTSIDE the CombatArea polygon!")

    # -------------------------------------------------------------------------
    # 4. Overgrowth Materials & Geometry Definitions
    # -------------------------------------------------------------------------
    def test_overgrowth_material_and_species_defined(self):
        """Verify OvergrowthSystem.con defines materials and foliage types."""
        p = os.path.join(LEVEL_DIR, "OvergrowthSystem.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        clean = parser.get_clean_lines()

        materials_added = []
        types_added = []
        for _, line in clean:
            tokens = line.split()
            if tokens[0] == "Overgrowth.addMaterial" and len(tokens) > 1:
                materials_added.append(tokens[1])
            elif tokens[0] == "Overgrowth.addType" and len(tokens) > 1:
                types_added.append(tokens[1])

        self.assertGreater(len(materials_added), 0, "No Overgrowth materials declared")
        self.assertGreater(len(types_added), 0, "No Overgrowth species types declared")

    def test_overgrowth_geometries_are_vanilla_trees(self):
        """Verify OvergrowthType.geometry references valid BF2 vanilla foliage meshes."""
        p = os.path.join(LEVEL_DIR, "OvergrowthSystem.con")
        self.assertTrue(os.path.isfile(p), f"File missing: {p}")
        parser = ConParser(p)
        clean = parser.get_clean_lines()

        geometries = []
        for _, line in clean:
            tokens = line.split()
            if tokens[0] == "OvergrowthType.geometry" and len(tokens) > 1:
                geometries.append(tokens[1])

        self.assertGreater(len(geometries), 0, "No Overgrowth geometries specified")
        vanilla_foliage = {
            "fir_mixed02", "birch_green_1", "birch_green_2", "pine_dead",
            "me_olive03", "largebush", "pine_large", "oak_01"
        }
        for geo in geometries:
            self.assertIn(geo, vanilla_foliage, f"Geometry '{geo}' is not a recognized vanilla BF2 foliage mesh")


if __name__ == "__main__":
    unittest.main()
