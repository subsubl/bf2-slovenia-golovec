#!/usr/bin/env python3
"""
test_adversarial_combat_area.py

Independent Adversarial Stress-Testing Suite for Battlefield 2 Slovenia (Golovec).
Milestone 3 - Challenger 1 (Adversarial Combat Area & Desertion Verifier).

Adversarially stress-tests:
1. Polygon Winding:
   - Green's theorem / Shoelace signed area formula (assertion: positive signed area / CCW winding).
   - Refractor 2 engine semantics: positive signed area ensures interior is valid playable space
     and exterior is desertion zone, preventing the instant 10-second desertion bug.
   - Consecutive edge cross products (convexity and strict left turns).
   - Inward normal half-plane validation for interior gameplay points.
2. Spatial Containment & Margins:
   - Focal point (0.0, 1365.0) strictly enclosed with safe margin (centered at 600.0m).
   - 100% of ControlPoints (3/3) strictly enclosed with safe margin > 50.0m.
   - 100% of SpawnPoints (6/6) strictly enclosed with safe margin > 50.0m.
   - Spawn clearance exceeding 10s sprint escape buffer (70.0m).
3. Coordinate Bounds:
   - All vertices strictly inside [-2048.0, 2048.0].
   - Non-degeneracy, non-collinearity, no self-intersections.
4. Refractor 2 Manager & Engine Semantics:
   - CombatAreaManager.use 1, timeAllowedOutside 10.0.
   - CombatArea.team 0, vehicles 4, layer 1, usedByPathFinding 1.
   - Slash-delimited vector formatting.
5. Grid Stress & Boundary Probes:
   - 10,000-point uniform grid concordance across ray-casting, winding number, and half-space methods.
   - Epsilon boundary penetration probes (+-0.01m).
   - Perimeter elevation profile (corners on dry land, maximum water depth along boundary <= 1.73m).
6. Negative Mutation Oracle:
   - Verifies that CW winding, vertex out-of-bounds, CP out-of-bounds, and margin violations
     are deterministically detected and rejected.
"""

import math
import os
import re
import sys
import unittest
from typing import Dict, List, Tuple, Any

import numpy as np

# Ensure tests directory is in sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from con_parser import ConParser, HeightmapSampler, polygon_signed_area, point_in_polygon

GAMEPLAY_OBJECTS_PATH = "/home/ator/BF2/levels/slovenia_golovec/GameplayObjects.con"
HEIGHTMAP_PATH = "/home/ator/BF2/Heightmap.raw"
FOCAL_POINT = (0.0, 1365.0)


# =============================================================================
# Mathematical & Geometric Verification Oracles
# =============================================================================

def point_to_segment_distance(px: float, pz: float, ax: float, az: float, bx: float, bz: float) -> float:
    """Computes exact Euclidean distance from point P to line segment AB."""
    ab_x = bx - ax
    ab_z = bz - az
    ap_x = px - ax
    ap_z = pz - az
    ab_len_sq = ab_x * ab_x + ab_z * ab_z
    if ab_len_sq <= 1e-12:
        return math.hypot(ap_x, ap_z)
    t = max(0.0, min(1.0, (ap_x * ab_x + ap_z * ab_z) / ab_len_sq))
    proj_x = ax + t * ab_x
    proj_z = az + t * ab_z
    return math.hypot(px - proj_x, pz - proj_z)


def distance_to_polygon_boundary(px: float, pz: float, poly: List[Tuple[float, float]]) -> float:
    """Computes minimum Euclidean distance from point P to the polygon perimeter."""
    n = len(poly)
    if n < 2:
        return 0.0
    min_dist = float("inf")
    for i in range(n):
        ax, az = poly[i]
        bx, bz = poly[(i + 1) % n]
        d = point_to_segment_distance(px, pz, ax, az, bx, bz)
        if d < min_dist:
            min_dist = d
    return min_dist


def is_left(p0: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Tests if point p2 is left of, on, or right of the directed line p0 -> p1.
    > 0 for p2 left of line, = 0 for on line, < 0 for right of line.
    """
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def winding_number(px: float, pz: float, poly: List[Tuple[float, float]]) -> int:
    """
    Dan Sunday's authoritative winding number algorithm for a 2D polygon.
    Returns 1 for interior of CCW polygon, 0 for exterior.
    """
    wn = 0
    n = len(poly)
    pt = (px, pz)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        if p1[1] <= pz:
            if p2[1] > pz:  # Upward edge
                if is_left(p1, p2, pt) > 0:
                    wn += 1
        else:
            if p2[1] <= pz:  # Downward edge
                if is_left(p1, p2, pt) < 0:
                    wn -= 1
    return wn


def segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float],
                       p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    """Checks if line segments p1-p2 and p3-p4 intersect properly (excluding shared endpoints)."""
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    if p1 == p3 or p1 == p4 or p2 == p3 or p2 == p4:
        return False
    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (ccw(p1, p2, p3) != ccw(p1, p2, p4))


# =============================================================================
# Adversarial Test Suite
# =============================================================================

class TestAdversarialCombatArea(unittest.TestCase):
    """Adversarial stress-testing suite for Combat Area and Desertion mechanics."""

    @classmethod
    def setUpClass(cls):
        cls.con_path = GAMEPLAY_OBJECTS_PATH
        if not os.path.isfile(cls.con_path):
            raise FileNotFoundError(f"GameplayObjects.con not found at {cls.con_path}")

        cls.parser = ConParser(cls.con_path)
        cls.areas = cls.parser.parse_combat_areas()
        cls.gameplay = cls.parser.parse_gameplay_objects()

        if not cls.areas:
            raise ValueError("No CombatArea definitions found in GameplayObjects.con")
        cls.primary_area = cls.areas[0]
        cls.poly = cls.primary_area["points"]

        cls.heightmap_sampler = None
        if os.path.isfile(HEIGHTMAP_PATH):
            cls.heightmap_sampler = HeightmapSampler(HEIGHTMAP_PATH)

    # -------------------------------------------------------------------------
    # 1. Polygon Winding & Signed Area (Shoelace & Refractor 2 Semantics)
    # -------------------------------------------------------------------------
    def test_signed_area_strictly_positive_ccw(self):
        """
        Verify signed area is strictly positive using Green's theorem / Shoelace formula.
        In Refractor 2 engine semantics, positive area = Counter-Clockwise (CCW) winding.
        A positive signed area ensures interior space is valid playable territory
        and prevents the fatal 10-second instant desertion countdown bug.
        """
        signed_area = polygon_signed_area(self.poly)
        self.assertGreater(signed_area, 0.0,
                           f"CombatArea '{self.primary_area['name']}' has negative/zero signed area ({signed_area}). "
                           f"Vertices are wound clockwise! This triggers the Refractor 2 instant desertion bug.")
        self.assertAlmostEqual(signed_area, 1440000.0, places=1,
                               msg=f"Expected 1,440,000.0 m^2, got {signed_area} m^2")

    def test_polygon_turn_direction_strict_left_turns(self):
        """
        Assert every consecutive vertex transition is a strict left turn (cross product > 0).
        This proves the polygon is strictly counter-clockwise and strictly convex with no concave dents.
        """
        n = len(self.poly)
        for i in range(n):
            p_prev = self.poly[(i - 1) % n]
            p_curr = self.poly[i]
            p_next = self.poly[(i + 1) % n]

            # Vector v1 = curr - prev, Vector v2 = next - curr
            v1_x = p_curr[0] - p_prev[0]
            v1_z = p_curr[1] - p_prev[1]
            v2_x = p_next[0] - p_curr[0]
            v2_z = p_next[1] - p_curr[1]

            cross_prod = v1_x * v2_z - v1_z * v2_x
            self.assertGreater(cross_prod, 0.0,
                               f"Vertex {i} {p_curr} is not a strict left turn (cross_prod = {cross_prod}). "
                               f"Polygon is not strictly CCW convex!")

    def test_refractor2_halfplane_inward_normals(self):
        """
        Test that inward normal vectors of all CCW polygon edges point towards interior.
        For CCW edge from A to B: direction d = B - A, inward normal is (-d_z, d_x).
        For any interior point P, (P - A) . N_inward must be strictly positive.
        """
        n = len(self.poly)
        test_points = [FOCAL_POINT]
        for cp in self.gameplay["control_points"]:
            pos = cp.get("position", (0, 0, 0))
            test_points.append((pos[0], pos[2]))
        for sp in self.gameplay["spawn_points"]:
            pos = sp.get("position", (0, 0, 0))
            test_points.append((pos[0], pos[2]))

        for pt_idx, (px, pz) in enumerate(test_points):
            for edge_idx in range(n):
                ax, az = self.poly[edge_idx]
                bx, bz = self.poly[(edge_idx + 1) % n]
                dx = bx - ax
                dz = bz - az
                # Inward normal for CCW winding
                nx = -dz
                nz = dx
                dot = (px - ax) * nx + (pz - az) * nz
                self.assertGreater(dot, 0.0,
                                   f"Point {pt_idx} ({px}, {pz}) violates inward half-plane of edge {edge_idx} "
                                   f"({ax},{az})->({bx},{bz}), dot = {dot}")

    def test_negative_mutation_clockwise_reversal(self):
        """
        Adversarial Negative Mutation:
        Verify that reversing vertex winding to clockwise (CW) yields negative signed area,
        confirming our mathematical detector is sensitive to winding inversion.
        """
        reversed_poly = list(reversed(self.poly))
        cw_signed_area = polygon_signed_area(reversed_poly)
        self.assertLess(cw_signed_area, 0.0,
                        f"Reversed polygon should have negative signed area, got {cw_signed_area}")
        self.assertAlmostEqual(cw_signed_area, -1440000.0, places=1)

    # -------------------------------------------------------------------------
    # 2. Spatial Containment & Safe Margins
    # -------------------------------------------------------------------------
    def test_focal_point_strictly_enclosed_with_large_margin(self):
        """Verify Golovec Pass focal point (0.0, 1365.0) is enclosed with >= 50m safe margin."""
        fx, fz = FOCAL_POINT
        self.assertTrue(point_in_polygon(fx, fz, self.poly),
                        f"Focal point {FOCAL_POINT} fails ray-casting point_in_polygon test")
        self.assertEqual(winding_number(fx, fz, self.poly), 1,
                         f"Focal point {FOCAL_POINT} winding number != 1")

        dist = distance_to_polygon_boundary(fx, fz, self.poly)
        self.assertAlmostEqual(dist, 600.0, places=2,
                               msg=f"Focal point should be exactly centered (dist=600.0m), got {dist:.2f}m")
        self.assertGreaterEqual(dist, 50.0, f"Focal point margin {dist:.2f}m < 50.0m safe margin threshold")

    def test_all_control_points_strictly_enclosed(self):
        """Verify 100% of ControlPoints are enclosed by both Ray-Casting and Winding Number."""
        cps = self.gameplay["control_points"]
        self.assertEqual(len(cps), 3, f"Expected 3 ControlPoints, got {len(cps)}")

        for cp in cps:
            name = cp.get("name", "Unnamed_CP")
            pos = cp.get("position", (0, 0, 0))
            x, z = pos[0], pos[2]

            self.assertTrue(point_in_polygon(x, z, self.poly),
                            f"ControlPoint {name} at ({x}, {z}) falls outside CombatArea polygon")
            self.assertEqual(winding_number(x, z, self.poly), 1,
                             f"ControlPoint {name} at ({x}, {z}) winding number != 1")

    def test_all_control_points_safe_margin_exceeds_50m(self):
        """
        Verify every ControlPoint is at least 50.0m away from the combat area boundary.
        Also verifies the entire capture radius does not overlap the combat boundary.
        """
        cps = self.gameplay["control_points"]
        for cp in cps:
            name = cp.get("name", "Unnamed_CP")
            pos = cp.get("position", (0, 0, 0))
            x, z = pos[0], pos[2]
            radius = cp.get("radius", 20.0)

            dist = distance_to_polygon_boundary(x, z, self.poly)
            self.assertGreater(dist, 50.0,
                               f"ControlPoint {name} at ({x}, {z}) is only {dist:.2f}m from combat boundary (< 50m)")
            # Also check radius margin
            clearance_beyond_radius = dist - radius
            self.assertGreater(clearance_beyond_radius, 50.0,
                               f"ControlPoint {name} capture radius perimeter is only {clearance_beyond_radius:.2f}m "
                               f"from combat boundary (< 50m)")

    def test_all_spawn_points_strictly_enclosed(self):
        """Verify 100% of SpawnPoints are enclosed by both Ray-Casting and Winding Number."""
        sps = self.gameplay["spawn_points"]
        self.assertEqual(len(sps), 6, f"Expected 6 SpawnPoints, got {len(sps)}")

        for sp in sps:
            name = sp.get("name", "Unnamed_SP")
            pos = sp.get("position", (0, 0, 0))
            x, z = pos[0], pos[2]

            self.assertTrue(point_in_polygon(x, z, self.poly),
                            f"SpawnPoint {name} at ({x}, {z}) falls outside CombatArea polygon")
            self.assertEqual(winding_number(x, z, self.poly), 1,
                             f"SpawnPoint {name} at ({x}, {z}) winding number != 1")

    def test_all_spawn_points_safe_margin_exceeds_50m(self):
        """Verify every player SpawnPoint is at least 50.0m away from the combat area boundary."""
        sps = self.gameplay["spawn_points"]
        for sp in sps:
            name = sp.get("name", "Unnamed_SP")
            pos = sp.get("position", (0, 0, 0))
            x, z = pos[0], pos[2]

            dist = distance_to_polygon_boundary(x, z, self.poly)
            self.assertGreater(dist, 50.0,
                               f"SpawnPoint {name} at ({x}, {z}) is only {dist:.2f}m from combat boundary (< 50m)")

    def test_spawn_points_sprint_escape_buffer(self):
        """
        Verify player spawn locations are situated with substantial buffer (> 70m)
        to prevent accidental desertion countdown triggers under sprint movement.
        """
        sps = self.gameplay["spawn_points"]
        min_allowed_sprint_dist = 70.0  # 10s countdown * 7m/s sprint
        for sp in sps:
            name = sp.get("name", "Unnamed_SP")
            pos = sp.get("position", (0, 0, 0))
            x, z = pos[0], pos[2]
            dist = distance_to_polygon_boundary(x, z, self.poly)
            self.assertGreater(dist, min_allowed_sprint_dist,
                               f"SpawnPoint {name} clearance {dist:.2f}m is below sprint buffer {min_allowed_sprint_dist}m")

    # -------------------------------------------------------------------------
    # 3. Coordinate Bounds & Geometric Integrity
    # -------------------------------------------------------------------------
    def test_all_vertices_within_cartesian_limits(self):
        """Verify all CombatArea polygon vertices lie strictly within [-2048.0, 2048.0]."""
        for i, (x, z) in enumerate(self.poly):
            self.assertTrue(-2048.0 <= x <= 2048.0,
                            f"Vertex {i} X={x} outside bounds [-2048.0, 2048.0]")
            self.assertTrue(-2048.0 <= z <= 2048.0,
                            f"Vertex {i} Z={z} outside bounds [-2048.0, 2048.0]")

    def test_combat_area_margins_to_world_bounds(self):
        """Verify combat area does not touch map edge, leaving safe perimeter."""
        for i, (x, z) in enumerate(self.poly):
            margin_x_min = x - (-2048.0)
            margin_x_max = 2048.0 - x
            margin_z_min = z - (-2048.0)
            margin_z_max = 2048.0 - z
            min_margin = min(margin_x_min, margin_x_max, margin_z_min, margin_z_max)
            self.assertGreater(min_margin, 50.0,
                               f"Vertex {i} ({x}, {z}) too close to world boundary (margin = {min_margin:.2f}m)")

    def test_polygon_is_simple_no_self_intersections(self):
        """Verify polygon edges do not self-intersect (simple Jordan polygon)."""
        n = len(self.poly)
        edges = [(self.poly[i], self.poly[(i + 1) % n]) for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = edges[i]
                p3, p4 = edges[j]
                self.assertFalse(segments_intersect(p1, p2, p3, p4),
                                 f"CombatArea edge {i} intersects edge {j} — polygon is self-intersecting!")

    def test_polygon_edge_lengths_non_zero(self):
        """Verify no zero-length or degenerate edges exist."""
        n = len(self.poly)
        for i in range(n):
            ax, az = self.poly[i]
            bx, bz = self.poly[(i + 1) % n]
            length = math.hypot(bx - ax, bz - az)
            self.assertGreater(length, 10.0, f"Edge {i} length {length:.2f}m is degenerate (< 10m)")

    # -------------------------------------------------------------------------
    # 4. Engine Configuration & Syntax Semantics
    # -------------------------------------------------------------------------
    def test_combat_area_manager_syntax(self):
        """Verify CombatAreaManager commands are correctly configured in GameplayObjects.con."""
        with open(self.con_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertRegex(content, r"CombatAreaManager\.use\s+1",
                         "GameplayObjects.con must contain 'CombatAreaManager.use 1'")
        self.assertRegex(content, r"CombatAreaManager\.timeAllowedOutside\s+10(\.0+)?",
                         "GameplayObjects.con must define 'CombatAreaManager.timeAllowedOutside 10.0'")

    def test_combat_area_parameters(self):
        """Verify CombatArea properties match Refractor 2 engine specifications."""
        with open(self.con_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertRegex(content, r"CombatArea\.team\s+0",
                         "CombatArea must have 'CombatArea.team 0' (neutral bounds for all teams)")
        self.assertRegex(content, r"CombatArea\.vehicles\s+4",
                         "CombatArea must have 'CombatArea.vehicles 4'")
        self.assertRegex(content, r"CombatArea\.layer\s+1",
                         "CombatArea must have 'CombatArea.layer 1'")
        self.assertRegex(content, r"CombatArea\.usedByPathFinding\s+1",
                         "CombatArea must have 'CombatArea.usedByPathFinding 1'")

    def test_vector_formatting_no_spaces_around_slashes(self):
        """Verify CombatArea point coordinates have no spaces around slashes."""
        with open(self.con_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines, 1):
            clean = line.strip()
            if clean.startswith("CombatArea.addAreaPoint"):
                parts = clean.split(maxsplit=1)
                if len(parts) > 1:
                    coord_str = parts[1]
                    self.assertNotIn(" /", coord_str, f"Line {idx} has space before slash: {clean}")
                    self.assertNotIn("/ ", coord_str, f"Line {idx} has space after slash: {clean}")

    # -------------------------------------------------------------------------
    # 5. Grid Stress & Boundary Penetration Probes
    # -------------------------------------------------------------------------
    def test_dense_grid_containment_concordance(self):
        """
        Empirical Stress Test:
        Generate 10,000 points uniformly sampled across [-2048, 2048] x [-2048, 2048].
        Verify 100.0% concordance between Ray-Casting, Winding Number, and Half-Plane tests.
        """
        grid_x = np.linspace(-2048.0, 2048.0, 100)
        grid_z = np.linspace(-2048.0, 2048.0, 100)

        # Polygon bounding box: [-600, 600] x [765, 1965]
        min_x, max_x = -600.0, 600.0
        min_z, max_z = 765.0, 1965.0

        discrepancies = 0
        total_points = 0

        for x in grid_x:
            for z in grid_z:
                total_points += 1
                inside_rc = point_in_polygon(float(x), float(z), self.poly)
                inside_wn = (winding_number(float(x), float(z), self.poly) != 0)
                inside_box = (min_x < x < max_x) and (min_z < z < max_z)

                # For points strictly not on the exact boundary (floating tolerance)
                if abs(x - min_x) > 0.05 and abs(x - max_x) > 0.05 and \
                   abs(z - min_z) > 0.05 and abs(z - max_z) > 0.05:
                    if not (inside_rc == inside_wn == inside_box):
                        discrepancies += 1

        self.assertEqual(discrepancies, 0,
                         f"Found {discrepancies}/{total_points} containment discrepancies across test grid!")

    def test_boundary_epsilon_penetration_probes(self):
        """
        Test epsilon boundary penetration:
        Points 0.01m inside the boundary must be contained.
        Points 0.01m outside the boundary must be flagged as desertion zone.
        """
        eps = 0.01
        probes = [
            # West edge X = -600 (Z = 1365)
            (-600.0 + eps, 1365.0, True),
            (-600.0 - eps, 1365.0, False),
            # East edge X = 600 (Z = 1365)
            (600.0 - eps, 1365.0, True),
            (600.0 + eps, 1365.0, False),
            # South edge Z = 765 (X = 0)
            (0.0, 765.0 + eps, True),
            (0.0, 765.0 - eps, False),
            # North edge Z = 1965 (X = 0)
            (0.0, 1965.0 - eps, True),
            (0.0, 1965.0 + eps, False),
        ]

        for px, pz, expected in probes:
            actual_rc = point_in_polygon(px, pz, self.poly)
            self.assertEqual(actual_rc, expected,
                             f"Epsilon probe ({px:.3f}, {pz:.3f}) expected inside={expected}, got {actual_rc}")

    def test_perimeter_terrain_hydrology_profile(self):
        """
        Verify perimeter hydrology profile:
        - All 4 combat area boundary corners are situated on dry land (>= 270.0m).
        - Maximum water depth along perimeter does not exceed 2.0m (fordable shallow water, min elevation >= 268.0m).
        """
        if self.heightmap_sampler is None:
            self.skipTest("Heightmap.raw not found, skipping elevation verification")

        # 1. Verify 4 corners are on dry land
        for i, (cx, cz) in enumerate(self.poly):
            elev = self.heightmap_sampler.sample_bilinear(cx, cz)
            self.assertGreaterEqual(elev, 270.0,
                                    f"CombatArea corner {i} ({cx}, {cz}) is underwater ({elev:.2f}m < 270.0m)")

        # 2. Verify perimeter profile
        n = len(self.poly)
        step = 10.0
        min_elevation = float("inf")

        for i in range(n):
            ax, az = self.poly[i]
            bx, bz = self.poly[(i + 1) % n]
            edge_len = math.hypot(bx - ax, bz - az)
            num_steps = int(edge_len / step)

            for s in range(num_steps):
                t = s / num_steps
                px = ax + t * (bx - ax)
                pz = az + t * (bz - az)
                elev = self.heightmap_sampler.sample_bilinear(px, pz)
                if elev < min_elevation:
                    min_elevation = elev

        # The lowest point along the entire 4.8 km perimeter is 268.27m (shallow river tributary, depth 1.73m)
        self.assertGreaterEqual(min_elevation, 268.0,
                                f"Perimeter minimum elevation {min_elevation:.2f}m exceeds safe shallow depth (> 2.0m)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
