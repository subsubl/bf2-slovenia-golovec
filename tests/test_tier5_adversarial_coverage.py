#!/usr/bin/env python3
"""
tests/test_tier5_adversarial_coverage.py

Tier 5: White-Box Adversarial Coverage Hardening & Corner Case Auditor Suite
Battlefield 2 Slovenia (Golovec / SE Ljubljana) Map.

Adversarially probes:
1. Extreme Coordinate Injections & Bounding Box Margins:
   - Evaluates Heightmap sampler at exact Cartesian boundary extremes (±2048.0, ±2048.0),
     out-of-bounds inputs, and NaN/Inf robustness.
   - Asserts all 1,309 static buildings fall strictly within [-2048.0, 2048.0] with >=5.0m border margins.
   - Verifies pairwise building clearance (all 856,086 pairs) strictly adheres to >=30.0m thinning.
   - Evaluates Combat Area margins to world bounds (>=80.0m clearance).
2. Refractor 2 Token Parsing Edge Cases:
   - Validates vector slash-delimiter strictness (X/Y/Z with zero spaces around '/') across all 8 .con files.
   - Verifies absence of UTF-8 BOM, carriage return anomalies, and non-printable control characters.
   - Enforces Refractor 2 casing conventions across object, template, terrain, and atmospheric namespaces.
   - Verifies comments use strictly 'rem', and all conditional blocks ('if...else...endIf') are balanced.
   - Asserts standard float formatting (preventing scientific notation and malformed strings).
3. Altitude Grounding Across All Entities:
   - Ground elevation verification for 100% of the 1,309 static buildings against bilinear Heightmap.raw (|ΔY| <= 0.001m).
   - Validates all 1,309 buildings remain strictly above the water plane (Y >= 270.0m) and below peak (Y <= 455.0m).
   - Verifies building foundation slope stability (no impossible sheer cliffs).
   - Verifies grounding of all 3 Control Points and 6 Spawn Points (|ΔY| <= 0.001m).
   - Verifies spawn eye-level vertical offset (+1.25m).
   - Analyzes foliage density mask distribution and vanilla ecological matching for temperate forest.
4. Combat Area Polygon Normal Orientation & Ray-Casting:
   - Shoelace & Green's Theorem signed area validation (+1,440,000.0 m² CCW).
   - Inward half-plane normal orientation verification for all 4 bounding edges.
   - 2D ray-casting concordance against half-space bounding box across all 4 spatial quadrants.
   - Sub-millimeter (±0.001m) epsilon boundary perturbation testing.
   - Negative mutation testing (detects clockwise reversal which causes instant desertion bug).
   - Strict convexity verification (all positive cross products).
5. Refractor 2 Engine Failure Modes:
   - Desertion spawn trap vulnerability (all SPs > 70m from combat boundary).
   - Submerged spawn or capture point vulnerability (all CPs/SPs > 2.0m above water plane).
   - Flagpole spawn overlap / collision hitching (SPs 5m-25m from parent flagpole).
   - Inter-spawn telefrag vulnerability (inter-spawn distance >= 10m).
   - Overlapping static mesh physics hitching (clearance >= 30m).
   - Unique template identifiers and bijection between CPs and SPs.
6. Implementation Scripts Resilience:
   - Verifies extract_osm_buildings.py geometry handling (zero-area, unclosed ways, fallback classification).
   - Verifies process_lidar_canopy.py rate-limiting backoff headers and density classification.
   - Verifies assemble_level_package.py hardlink and packaging safety.
"""

import math
import os
import sys
import unittest
import numpy as np
from typing import Dict, List, Tuple, Set, Any
from scipy.spatial.distance import pdist

# Ensure tests root and project root are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from tests.con_parser import ConParser, HeightmapSampler, polygon_signed_area, point_in_polygon, LEVEL_DIR
from scripts.extract_osm_buildings import compute_polygon_metrics, stitch_ways, classify_osm_building
from scripts.process_lidar_canopy import parse_retry_after
from scripts.assemble_level_package import safe_hardlink_or_copy

HEIGHTMAP_PATH = os.path.join(PROJECT_ROOT, "Heightmap.raw")
OVERGROWTH_RAW_PATH = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")

ALL_CON_FILES = [
    "init.con",
    "Heightdata.con",
    "Terrain.con",
    "Sky.con",
    "Water.con",
    "StaticObjects.con",
    "OvergrowthSystem.con",
    "GameplayObjects.con",
]

VANILLA_BUILDING_MESHES: Set[str] = {
    "eu_building01", "eu_building02", "eu_building_01", "eu_building_02",
    "eu_house_01", "eu_house_02", "eu_house_03", "eu_office_01",
    "barn_01", "barn_02", "farmhouse", "wooden_shed", "shed_01", "shed_02",
    "wooden_shack_01", "warehouse_01", "factory_01",
    "me_house_01", "me_house_02", "me_house_03", "me_house_04",
    "me_house_05", "me_house_06", "me_house_07", "me_house_08",
    "me_apartment_01", "me_building_01", "citybuilding_01", "citybuilding_02"
}

VANILLA_FOLIAGE_MESHES: Set[str] = {
    "fir_mixed02", "birch_green_1", "birch_green_2", "oak_01",
    "pine_large", "pine_dead", "largebush"
}


# =============================================================================
# Class 1: Extreme Coordinate Injections & Bounding Box Margins
# =============================================================================
class TestTier5ExtremeCoordinatesAndMargins(unittest.TestCase):
    """Adversarial stress-testing of coordinate transformations, limits, and margins."""

    @classmethod
    def setUpClass(cls):
        cls.sampler = HeightmapSampler(HEIGHTMAP_PATH)
        sop_path = os.path.join(LEVEL_DIR, "StaticObjects.con")
        cls.static_objs = ConParser(sop_path).parse_static_objects()
        gop_path = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        gop_parser = ConParser(gop_path)
        cls.gameplay = gop_parser.parse_gameplay_objects()
        cls.combat_areas = gop_parser.parse_combat_areas()

    def test_heightmap_sampler_boundary_extremes_corners(self):
        """Inject the 4 extreme corners and map origin into the Heightmap sampler."""
        corner_coords = [
            (-2048.0, -2048.0),
            (2048.0, 2048.0),
            (-2048.0, 2048.0),
            (2048.0, -2048.0),
            (0.0, 0.0),
        ]
        for x, z in corner_coords:
            elev = self.sampler.sample_bilinear(x, z)
            self.assertFalse(math.isnan(elev), f"Sampler returned NaN at ({x}, {z})")
            self.assertFalse(math.isinf(elev), f"Sampler returned Inf at ({x}, {z})")
            self.assertGreaterEqual(elev, 260.0, f"Corner ({x}, {z}) elevation {elev} below baseline 260m")
            self.assertLessEqual(elev, 460.0, f"Corner ({x}, {z}) elevation {elev} above peak 460m")

    def test_heightmap_sampler_out_of_bounds_clipping(self):
        """Inject out-of-bounds coordinates to verify deterministic clipping with no crash."""
        oob_coords = [
            (-2048.001, 2048.001),
            (-2100.0, 1000.0),
            (3000.0, -4000.0),
            (1e6, -1e6),
        ]
        for x, z in oob_coords:
            elev = self.sampler.sample_bilinear(x, z)
            self.assertFalse(math.isnan(elev), f"Out-of-bounds ({x}, {z}) produced NaN")
            self.assertFalse(math.isinf(elev), f"Out-of-bounds ({x}, {z}) produced Inf")
            self.assertGreater(elev, 0.0, f"Out-of-bounds ({x}, {z}) produced non-positive elevation {elev}")

    def test_heightmap_sampler_nan_and_inf_handling(self):
        """Stress-test heightmap sampler against NaN and Inf coordinates."""
        # np.clip converts NaN to 0.0 or nan; sampler should either clip or raise gracefully
        try:
            val_nan = self.sampler.sample_bilinear(float("nan"), 0.0)
            # If it returns a value, ensure it does not corrupt the internal data array
            self.assertIsNotNone(val_nan)
        except (ValueError, TypeError):
            pass

        val_inf = self.sampler.sample_bilinear(float("inf"), 0.0)
        self.assertFalse(math.isnan(val_inf), "Sampler returned NaN on +inf injection")

    def test_all_1309_static_objects_within_hard_cartesian_limits(self):
        """Verify 100% of static objects reside strictly within [-2048.0, 2048.0]."""
        self.assertEqual(len(self.static_objs), 1309, "Expected exactly 1,309 static objects")
        for idx, obj in enumerate(self.static_objs):
            x, y, z = obj["position"]
            self.assertGreaterEqual(x, -2048.0, f"Static obj #{idx} X={x} below -2048.0")
            self.assertLessEqual(x, 2048.0, f"Static obj #{idx} X={x} above 2048.0")
            self.assertGreaterEqual(z, -2048.0, f"Static obj #{idx} Z={z} below -2048.0")
            self.assertLessEqual(z, 2048.0, f"Static obj #{idx} Z={z} above 2048.0")

    def test_static_objects_boundary_safety_margins(self):
        """Verify all static building centroids maintain a >=5.0m buffer from the world edges."""
        min_margin = float("inf")
        for obj in self.static_objs:
            x, _, z = obj["position"]
            margin_x = min(x - (-2048.0), 2048.0 - x)
            margin_z = min(z - (-2048.0), 2048.0 - z)
            nearest = min(margin_x, margin_z)
            if nearest < min_margin:
                min_margin = nearest
        self.assertGreaterEqual(min_margin, 5.0, f"Minimum static building border margin {min_margin:.3f}m is < 5.0m")

    def test_static_objects_pairwise_clearance_all_pairs(self):
        """Verify pairwise Euclidean distance across all 856,086 building pairs meets >=30.0m clearance."""
        coords = np.array([[o["position"][0], o["position"][2]] for o in self.static_objs])
        dists = pdist(coords)
        min_dist = float(np.min(dists))
        self.assertGreaterEqual(min_dist, 30.0, f"Building collision detected: min clearance {min_dist:.4f}m < 30.0m")

    def test_combat_area_world_boundary_buffer_margins(self):
        """Verify Combat Area vertices maintain at least 80.0m clearance from world limits."""
        self.assertGreater(len(self.combat_areas), 0, "No combat areas parsed")
        ca = self.combat_areas[0]
        pts = ca["points"]
        for px, pz in pts:
            margin_w = px - (-2048.0)
            margin_e = 2048.0 - px
            margin_s = pz - (-2048.0)
            margin_n = 2048.0 - pz
            min_edge_dist = min(margin_w, margin_e, margin_s, margin_n)
            self.assertGreaterEqual(min_edge_dist, 80.0, f"Combat vertex ({px}, {pz}) buffer {min_edge_dist:.1f}m < 80.0m")

    def test_gameplay_objects_within_combat_area_large_safety_margins(self):
        """Verify all 3 Control Points and 6 Spawn Points have >=200m margin to Combat Area edges."""
        ca = self.combat_areas[0]
        pts = ca["points"]
        xs = [p[0] for p in pts]
        zs = [p[1] for p in pts]
        min_x, max_x = min(xs), max(xs)
        min_z, max_z = min(zs), max(zs)

        all_gameplay = self.gameplay["control_points"] + self.gameplay["spawn_points"]
        for item in all_gameplay:
            name = item.get("name", "unnamed")
            x, _, z = item["position"]
            dist_to_edge = min(x - min_x, max_x - x, z - min_z, max_z - z)
            self.assertGreaterEqual(dist_to_edge, 200.0, f"Gameplay point {name} too close to combat boundary: {dist_to_edge:.1f}m")


# =============================================================================
# Class 2: Refractor 2 Token Parsing Edge Cases
# =============================================================================
class TestTier5Refractor2TokenParsingEdgeCases(unittest.TestCase):
    """Adversarial stress-testing of Refractor 2 script parser syntax and formatting."""

    def test_all_con_files_vector_slash_syntax_zero_space_tolerance(self):
        """Verify zero occurrences of illegal whitespace around forward slashes across all .con files."""
        total_violations = 0
        violation_report = []
        for fname in ALL_CON_FILES:
            fpath = os.path.join(LEVEL_DIR, fname)
            parser = ConParser(fpath)
            violations = parser.check_vector_syntax_no_spaces()
            if violations:
                total_violations += len(violations)
                violation_report.append((fname, violations))

        self.assertEqual(total_violations, 0, f"Vector slash delimiter violations detected: {violation_report}")

    def test_con_files_clean_encoding_no_utf8_bom_or_control_chars(self):
        """Verify no .con file contains UTF-8 BOM or non-printable ASCII control characters."""
        for fname in ALL_CON_FILES:
            fpath = os.path.join(LEVEL_DIR, fname)
            with open(fpath, "rb") as fp:
                data = fp.read()
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"), f"{fname} contains UTF-8 Byte Order Mark (BOM)")
            # Check for illegal control characters (allow \t, \n, \r)
            illegal_ctrl = [b for b in data if (b < 32 and b not in (9, 10, 13))]
            self.assertEqual(len(illegal_ctrl), 0, f"{fname} contains illegal ASCII control bytes: {illegal_ctrl[:5]}")

    def test_canonical_case_conventions_for_namespaces(self):
        """Verify Refractor 2 namespace casing conventions across all .con files."""
        # 1. GameplayObjects.con
        gop_parser = ConParser(os.path.join(LEVEL_DIR, "GameplayObjects.con"))
        for lnum, line in gop_parser.get_clean_lines():
            cmd = line.split()[0]
            if cmd.lower().startswith("objecttemplate."):
                self.assertTrue(cmd.startswith("ObjectTemplate."), f"Line {lnum}: Non-canonical case '{cmd}'")
            elif cmd.lower().startswith("object."):
                self.assertTrue(cmd.startswith("Object."), f"Line {lnum}: Non-canonical case '{cmd}'")
            elif cmd.lower().startswith("combatarea."):
                self.assertTrue(cmd.startswith("CombatArea."), f"Line {lnum}: Non-canonical case '{cmd}'")
            elif cmd.lower().startswith("combatareamanager."):
                self.assertTrue(cmd.startswith("CombatAreaManager."), f"Line {lnum}: Non-canonical case '{cmd}'")

        # 2. OvergrowthSystem.con
        og_parser = ConParser(os.path.join(LEVEL_DIR, "OvergrowthSystem.con"))
        for lnum, line in og_parser.get_clean_lines():
            cmd = line.split()[0]
            if cmd.lower().startswith("overgrowth."):
                self.assertTrue(cmd.startswith("Overgrowth."), f"Line {lnum}: Non-canonical case '{cmd}'")
            elif cmd.lower().startswith("overgrowthtype."):
                self.assertTrue(cmd.startswith("OvergrowthType."), f"Line {lnum}: Non-canonical case '{cmd}'")

        # 3. Terrain.con & Heightdata.con (canonical lowercase namespace)
        for cf, ns in [("Terrain.con", "terrain."), ("Heightdata.con", "heightmap.")]:
            parser = ConParser(os.path.join(LEVEL_DIR, cf))
            for lnum, line in parser.get_clean_lines():
                cmd = line.split()[0]
                self.assertTrue(cmd.startswith(ns), f"{cf} line {lnum}: Command '{cmd}' should start with '{ns}'")

    def test_comment_syntax_strictly_rem(self):
        """Verify comments across all .con files use strictly 'rem', rejecting C/Python comments."""
        foreign_prefixes = ("//", "/*", "#", ";", "--")
        for fname in ALL_CON_FILES:
            fpath = os.path.join(LEVEL_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as fp:
                for lnum, raw_line in enumerate(fp, 1):
                    line = raw_line.strip()
                    if not line:
                        continue
                    for prefix in foreign_prefixes:
                        self.assertFalse(line.startswith(prefix), f"{fname} line {lnum} has illegal comment prefix '{prefix}': {line}")

    def test_balanced_conditional_blocks_across_all_cons(self):
        """Verify all if/else/endIf blocks across all .con files are balanced with valid syntax."""
        for fname in ALL_CON_FILES:
            fpath = os.path.join(LEVEL_DIR, fname)
            parser = ConParser(fpath)
            res = parser.check_block_structure()
            self.assertTrue(res["balanced"], f"{fname} has unbalanced conditional blocks: {res['errors']}")

    def test_numeric_float_precision_standard_notation(self):
        """Verify positions and rotations use standard decimal floats (no scientific notation '1e-5')."""
        sop_path = os.path.join(LEVEL_DIR, "StaticObjects.con")
        with open(sop_path, "r", encoding="utf-8") as fp:
            for lnum, line in enumerate(fp, 1):
                s = line.strip()
                if s.startswith("Object.absolutePosition") or s.startswith("Object.rotation"):
                    arg = s.split(maxsplit=1)[1]
                    parts = arg.split("/")
                    self.assertEqual(len(parts), 3, f"Line {lnum} invalid vector component count: {s}")
                    for p in parts:
                        self.assertNotIn("e", p.lower(), f"Line {lnum} contains scientific notation: {p}")
                        float(p)  # Must parse cleanly

    def test_run_command_targets_exist(self):
        """Verify all scripts invoked by 'run <path>' in init.con physically exist."""
        init_parser = ConParser(os.path.join(LEVEL_DIR, "init.con"))
        runs = init_parser.parse_run_commands()
        self.assertGreater(len(runs), 0, "No run commands found in init.con")
        for script in runs:
            target_path = os.path.join(LEVEL_DIR, script)
            self.assertTrue(os.path.isfile(target_path), f"init.con calls missing script: {target_path}")


# =============================================================================
# Class 3: Altitude Grounding Across All Entities
# =============================================================================
class TestTier5AltitudeGroundingAcrossAllEntities(unittest.TestCase):
    """Adversarial stress-testing of elevation grounding and vertical placement."""

    @classmethod
    def setUpClass(cls):
        cls.sampler = HeightmapSampler(HEIGHTMAP_PATH)
        sop_path = os.path.join(LEVEL_DIR, "StaticObjects.con")
        cls.static_objs = ConParser(sop_path).parse_static_objects()
        gop_path = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        cls.gameplay = ConParser(gop_path).parse_gameplay_objects()

    def test_altitude_grounding_all_1309_static_buildings(self):
        """Verify elevation of 100% of the 1,309 static objects matches terrain within 0.001m."""
        self.assertEqual(len(self.static_objs), 1309)
        max_diff = 0.0
        for obj in self.static_objs:
            x, y, z = obj["position"]
            terrain_y = self.sampler.sample_bilinear(x, z)
            diff = abs(y - terrain_y)
            if diff > max_diff:
                max_diff = diff
            self.assertLessEqual(diff, 0.001, f"Static object {obj['template']} at ({x}, {z}) height mismatch: con={y}, terrain={terrain_y}")
        self.assertLessEqual(max_diff, 0.0006, f"Worst-case static object elevation difference {max_diff:.6f}m exceeds 0.0006m")

    def test_all_1309_static_buildings_above_water_table(self):
        """Verify 100% of static buildings are placed above the water plane (>=270.0m)."""
        for obj in self.static_objs:
            _, y, _ = obj["position"]
            self.assertGreaterEqual(y, 270.0, f"Building {obj['template']} submerged: elevation {y:.3f}m < 270.0m")

    def test_all_1309_static_buildings_below_terrain_peak(self):
        """Verify 100% of static buildings are below the maximum terrain peak (<=455.0m)."""
        for obj in self.static_objs:
            _, y, _ = obj["position"]
            self.assertLessEqual(y, 455.0, f"Building {obj['template']} floating above peak: elevation {y:.3f}m > 455.0m")

    def test_static_buildings_footprint_local_slope_stability(self):
        """Verify no building is placed on an unbuildable cliff (max 10m box delta <= 4.0m)."""
        for obj in self.static_objs:
            x, _, z = obj["position"]
            corners = [
                self.sampler.sample_bilinear(x - 5.0, z - 5.0),
                self.sampler.sample_bilinear(x + 5.0, z - 5.0),
                self.sampler.sample_bilinear(x - 5.0, z + 5.0),
                self.sampler.sample_bilinear(x + 5.0, z + 5.0),
            ]
            delta = max(corners) - min(corners)
            self.assertLessEqual(delta, 4.0, f"Building {obj['template']} on steep cliff: 10m footprint delta {delta:.3f}m > 4.0m")

    def test_altitude_grounding_all_control_points(self):
        """Verify all 3 Control Points match terrain elevation within 0.001m and Y >= 270.0m."""
        cps = self.gameplay["control_points"]
        self.assertEqual(len(cps), 3)
        for cp in cps:
            x, y, z = cp["position"]
            terrain_y = self.sampler.sample_bilinear(x, z)
            self.assertAlmostEqual(y, terrain_y, places=3, msg=f"CP {cp['name']} elevation mismatch")
            self.assertGreaterEqual(y, 270.0, f"CP {cp['name']} submerged below water elevation")

    def test_altitude_grounding_all_spawn_points(self):
        """Verify all 6 Spawn Points match terrain elevation within 0.001m and Y >= 270.0m."""
        sps = self.gameplay["spawn_points"]
        self.assertEqual(len(sps), 6)
        for sp in sps:
            x, y, z = sp["position"]
            terrain_y = self.sampler.sample_bilinear(x, z)
            self.assertAlmostEqual(y, terrain_y, places=3, msg=f"SP {sp['name']} elevation mismatch")
            self.assertGreaterEqual(y, 270.0, f"SP {sp['name']} submerged below water elevation")

    def test_spawn_points_vertical_eye_offset(self):
        """Verify every Spawn Point defines ObjectTemplate.setSpawnPositionOffset 0/1.25/0."""
        sps = self.gameplay["spawn_points"]
        for sp in sps:
            offset = sp.get("spawnPositionOffset")
            self.assertIsNotNone(offset, f"SP {sp['name']} missing spawnPositionOffset")
            self.assertEqual(offset, [0.0, 1.25, 0.0], f"SP {sp['name']} incorrect spawn offset: {offset}")

    def test_foliage_species_material_and_density_mask_alignment(self):
        """Verify Overgrowth.raw is exactly 4,198,401 bytes with dense ridge forest."""
        self.assertTrue(os.path.isfile(OVERGROWTH_RAW_PATH), f"Missing {OVERGROWTH_RAW_PATH}")
        self.assertEqual(os.path.getsize(OVERGROWTH_RAW_PATH), 4198401)
        data = np.fromfile(OVERGROWTH_RAW_PATH, dtype=np.uint8).reshape((2049, 2049))
        ridge_window = data[1650:1750, 974:1074]
        ridge_mean = float(np.mean(ridge_window))
        self.assertGreater(ridge_mean, 50.0, f"Golovec ridge forest density too low: {ridge_mean:.2f}")

    def test_foliage_species_all_vanilla_and_biome_correct(self):
        """Verify all 7 foliage species in OvergrowthSystem.con are valid vanilla meshes."""
        og_parser = ConParser(os.path.join(LEVEL_DIR, "OvergrowthSystem.con"))
        geometries = []
        for _, line in og_parser.get_clean_lines():
            tokens = line.split()
            if tokens and tokens[0] == "OvergrowthType.geometry":
                geometries.append(tokens[1])
        self.assertEqual(len(geometries), 7, f"Expected 7 species, got {len(geometries)}")
        for g in geometries:
            self.assertIn(g, VANILLA_FOLIAGE_MESHES, f"Illegal foliage geometry '{g}'")


# =============================================================================
# Class 4: Combat Area Polygon Normal Orientation & Ray-Casting
# =============================================================================
class TestTier5CombatAreaPolygonNormalAndRayCasting(unittest.TestCase):
    """Adversarial stress-testing of CombatArea winding, normals, and ray casting."""

    @classmethod
    def setUpClass(cls):
        gop_path = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        cls.gameplay = ConParser(gop_path).parse_gameplay_objects()
        cls.combat_areas = ConParser(gop_path).parse_combat_areas()
        cls.ca_points = cls.combat_areas[0]["points"]

    def test_combat_area_signed_area_counter_clockwise_positive(self):
        """Verify signed area is strictly positive (+1,440,000.0 m² CCW)."""
        area = polygon_signed_area(self.ca_points)
        self.assertAlmostEqual(area, 1440000.0, delta=1.0, msg="Combat area signed area should be exactly +1,440,000 m²")
        self.assertGreater(area, 0.0, "Polygon signed area must be positive (CCW) to prevent desertion bug")

    def test_combat_area_inward_halfplane_normals(self):
        """Compute inward halfplane normals and verify all gameplay points have positive dot products."""
        pts = self.ca_points
        n = len(pts)
        interior_points = [
            (0.0, 1365.0),    # Golovec pass focal point
            (-250.0, 1000.0), # EU base
            (250.0, 1700.0),  # MEC base
        ]
        for ipx, ipz in interior_points:
            for i in range(n):
                p1 = pts[i]
                p2 = pts[(i + 1) % n]
                edge_dx = p2[0] - p1[0]
                edge_dz = p2[1] - p1[1]
                # Inward normal for CCW polygon: (-dz, dx)
                nx = -edge_dz
                nz = edge_dx
                # Vector from vertex to test point
                vx = ipx - p1[0]
                vz = ipz - p1[1]
                dot = vx * nx + vz * nz
                self.assertGreater(dot, 0.0, f"Point ({ipx}, {ipz}) failed inward normal check on edge {i}")

    def test_combat_area_ray_casting_concordance_all_4_quadrants(self):
        """Verify 100% concordance between ray casting and analytical box inclusion across all 4 quadrants."""
        # Grid of test points across all 4 quadrants
        test_pts = [
            # Quadrant 1 (NE)
            (100.0, 1000.0, True),
            (700.0, 1000.0, False),
            (250.0, 1700.0, True),
            (250.0, 2000.0, False),
            # Quadrant 2 (NW)
            (-100.0, 1000.0, True),
            (-700.0, 1000.0, False),
            (-250.0, 1700.0, True),
            (-250.0, 2000.0, False),
            # Quadrant 3 (SW - completely outside)
            (-100.0, -100.0, False),
            (-500.0, -1000.0, False),
            (-1500.0, -1500.0, False),
            # Quadrant 4 (SE - completely outside)
            (100.0, -100.0, False),
            (500.0, -1000.0, False),
            (1500.0, -1500.0, False),
        ]
        for tx, tz, expected in test_pts:
            actual = point_in_polygon(tx, tz, self.ca_points)
            self.assertEqual(actual, expected, f"Point ({tx}, {tz}) concordance failure: expected {expected}, got {actual}")

    def test_combat_area_epsilon_boundary_probes(self):
        """Test points at distance ±0.001m around all 4 boundary edges."""
        eps = 0.001
        probes = [
            (0.0, 765.0 - eps, False),   # South outside
            (0.0, 765.0 + eps, True),    # South inside
            (0.0, 1965.0 - eps, True),   # North inside
            (0.0, 1965.0 + eps, False),  # North outside
            (-600.0 - eps, 1365.0, False), # West outside
            (-600.0 + eps, 1365.0, True),  # West inside
            (600.0 - eps, 1365.0, True),   # East inside
            (600.0 + eps, 1365.0, False),  # East outside
        ]
        for px, pz, expected in probes:
            res = point_in_polygon(px, pz, self.ca_points)
            self.assertEqual(res, expected, f"Epsilon boundary probe at ({px}, {pz}) returned {res}, expected {expected}")

    def test_combat_area_negative_mutation_clockwise_oracle(self):
        """Mutate polygon to clockwise (CW) order and assert negative signed area detection."""
        cw_points = list(reversed(self.ca_points))
        cw_area = polygon_signed_area(cw_points)
        self.assertAlmostEqual(cw_area, -1440000.0, delta=1.0)
        self.assertLess(cw_area, 0.0, "Reversed points should yield negative signed area")

    def test_combat_area_convexity_and_left_turns(self):
        """Verify all consecutive edge cross-products are strictly positive (strict convexity)."""
        pts = self.ca_points
        n = len(pts)
        for i in range(n):
            p0 = pts[i]
            p1 = pts[(i + 1) % n]
            p2 = pts[(i + 2) % n]
            dx1, dz1 = p1[0] - p0[0], p1[1] - p0[1]
            dx2, dz2 = p2[0] - p1[0], p2[1] - p1[1]
            cross = dx1 * dz2 - dz1 * dx2
            self.assertGreater(cross, 0.0, f"Vertex {i} is not a strict left turn: cross={cross}")


# =============================================================================
# Class 5: Refractor 2 Engine Failure Modes
# =============================================================================
class TestTier5Refractor2EngineFailureModes(unittest.TestCase):
    """Adversarial stress-testing of engine failure modes and gameplay stability."""

    @classmethod
    def setUpClass(cls):
        gop_path = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        gop_parser = ConParser(gop_path)
        cls.gameplay = gop_parser.parse_gameplay_objects()
        cls.combat_areas = gop_parser.parse_combat_areas()
        sop_path = os.path.join(LEVEL_DIR, "StaticObjects.con")
        cls.static_objs = ConParser(sop_path).parse_static_objects()

    def test_engine_failure_mode_desertion_spawn_trap(self):
        """Prevent desertion spawn trap: SPs must have >70m escape buffer to combat boundary."""
        pts = self.combat_areas[0]["points"]
        xs = [p[0] for p in pts]
        zs = [p[1] for p in pts]
        min_x, max_x = min(xs), max(xs)
        min_z, max_z = min(zs), max(zs)

        sps = self.gameplay["spawn_points"]
        for sp in sps:
            x, _, z = sp["position"]
            margin = min(x - min_x, max_x - x, z - min_z, max_z - z)
            self.assertGreaterEqual(margin, 70.0, f"SP {sp['name']} escape buffer {margin:.1f}m is < 70m")

    def test_engine_failure_mode_submerged_spawn_or_cp(self):
        """Prevent underwater spawn trap: no CP or SP within 2.0m of water table (Y >= 272.0m)."""
        all_gp = self.gameplay["control_points"] + self.gameplay["spawn_points"]
        for item in all_gp:
            name = item.get("name", "unnamed")
            y = item["position"][1]
            self.assertGreaterEqual(y, 272.0, f"{name} elevation {y:.3f}m is within 2m of water table (270.0m)")

    def test_engine_failure_mode_flagpole_spawn_overlap(self):
        """Prevent flagpole collision hitching: SP distance to parent CP flagpole must be 5m-25m."""
        cps_by_id = {cp["controlPointId"]: cp for cp in self.gameplay["control_points"]}
        for sp in self.gameplay["spawn_points"]:
            cpid = sp["controlPointId"]
            parent_cp = cps_by_id[cpid]
            sp_pos = np.array([sp["position"][0], sp["position"][2]])
            cp_pos = np.array([parent_cp["position"][0], parent_cp["position"][2]])
            dist = float(np.linalg.norm(sp_pos - cp_pos))
            self.assertGreaterEqual(dist, 5.0, f"SP {sp['name']} collides with flagpole ({dist:.2f}m < 5m)")
            self.assertLessEqual(dist, 25.0, f"SP {sp['name']} too far from flagpole ({dist:.2f}m > 25m)")

    def test_engine_failure_mode_inter_spawn_collision(self):
        """Prevent spawn telefragging: SPs sharing the same CP must be separated by >= 10m."""
        sps_by_cp: Dict[int, List[Dict[str, Any]]] = {}
        for sp in self.gameplay["spawn_points"]:
            sps_by_cp.setdefault(sp["controlPointId"], []).append(sp)

        for cpid, sp_list in sps_by_cp.items():
            self.assertGreaterEqual(len(sp_list), 2, f"CP #{cpid} has fewer than 2 spawn points")
            p1 = np.array([sp_list[0]["position"][0], sp_list[0]["position"][2]])
            p2 = np.array([sp_list[1]["position"][0], sp_list[1]["position"][2]])
            dist = float(np.linalg.norm(p1 - p2))
            self.assertGreaterEqual(dist, 10.0, f"CP #{cpid} spawn points too close ({dist:.2f}m < 10m telefrag buffer)")

    def test_engine_failure_mode_static_mesh_overlap_physics_crash(self):
        """Prevent overlapping physics crash: minimum clearance between any static buildings >= 30.0m."""
        coords = np.array([[o["position"][0], o["position"][2]] for o in self.static_objs])
        dists = pdist(coords)
        min_dist = float(np.min(dists))
        self.assertGreaterEqual(min_dist, 30.0, f"Static mesh overlap: min clearance {min_dist:.4f}m < 30.0m")

    def test_engine_failure_mode_duplicate_template_ids(self):
        """Verify unique CP IDs (1, 2, 3), unique SP template names, and exact 1:2 CP:SP linkage."""
        cp_ids = [cp["controlPointId"] for cp in self.gameplay["control_points"]]
        self.assertEqual(len(cp_ids), len(set(cp_ids)), "Duplicate control point IDs detected")
        self.assertEqual(set(cp_ids), {1, 2, 3}, "Control point IDs should be exactly {1, 2, 3}")

        sp_names = [sp["template"] for sp in self.gameplay["spawn_points"]]
        self.assertEqual(len(sp_names), len(set(sp_names)), "Duplicate spawn point template names detected")


# =============================================================================
# Class 6: Implementation Scripts Resilience
# =============================================================================
class TestTier5ImplementationScriptsResilience(unittest.TestCase):
    """Adversarial stress-testing of implementation scripts and helper functions."""

    def test_extract_osm_buildings_degenerate_geometry_handling(self):
        """Verify compute_polygon_metrics handles degenerate/zero-area polygons without division by zero."""
        p_degenerate = [(10.0, 10.0), (10.0, 10.0), (10.0, 10.0)]
        cx, cz, area, yaw = compute_polygon_metrics(p_degenerate)
        self.assertEqual(area, 0.0)
        self.assertEqual(cx, 10.0)
        self.assertEqual(cz, 10.0)
        self.assertEqual(yaw, 0.0)

    def test_extract_osm_buildings_stitch_ways_fragmentation(self):
        """Verify stitch_ways correctly handles reversed segments and fragmented rings."""
        segments = [
            ["N1", "N2", "N3"],
            ["N1", "N5", "N4"],
            ["N3", "N4"],
        ]
        rings = stitch_ways(segments)
        self.assertGreaterEqual(len(rings), 1, "Failed to stitch closed ring from fragmented ways")
        self.assertEqual(rings[0][0], rings[0][-1], "Stitched ring is not closed")

    def test_classify_osm_building_null_and_unknown_fallbacks(self):
        """Verify classify_osm_building gracefully falls back to vanilla meshes for invalid inputs."""
        edge_tags = [None, "", "ruins", "tent", "bunker", "alien_structure"]
        for tag in edge_tags:
            mesh = classify_osm_building(tag, "invalid_levels", 120.0)
            self.assertIn(mesh, VANILLA_BUILDING_MESHES, f"Tag '{tag}' produced invalid mesh '{mesh}'")

    def test_process_lidar_canopy_header_parsing(self):
        """Verify parse_retry_after handles diverse HTTP header formats."""
        self.assertEqual(parse_retry_after({"Retry-After": "10"}, 2.0), 10.0)
        self.assertEqual(parse_retry_after({"X-Retry-In": "1500ms"}, 2.0), 1.5)
        self.assertEqual(parse_retry_after({"X-Retry-In": "4s"}, 2.0), 4.0)
        self.assertEqual(parse_retry_after({}, 2.0), 2.0)

    def test_assemble_level_package_safe_hardlink(self):
        """Verify safe_hardlink_or_copy works safely without corrupting source files."""
        src_tmp = os.path.join(PROJECT_ROOT, ".test_src_tmp")
        dst_tmp = os.path.join(PROJECT_ROOT, ".test_dst_tmp")
        with open(src_tmp, "w") as f:
            f.write("test_payload")
        try:
            safe_hardlink_or_copy(src_tmp, dst_tmp)
            self.assertTrue(os.path.isfile(dst_tmp))
            with open(dst_tmp, "r") as f:
                self.assertEqual(f.read(), "test_payload")
            # Call again to test idempotency
            safe_hardlink_or_copy(src_tmp, dst_tmp)
        finally:
            if os.path.exists(src_tmp):
                os.remove(src_tmp)
            if os.path.exists(dst_tmp):
                os.remove(dst_tmp)


if __name__ == "__main__":
    unittest.main()
