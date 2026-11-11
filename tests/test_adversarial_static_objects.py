#!/usr/bin/env python3
"""
Independent Adversarial Stress Testing Suite for StaticObjects.con
Milestone 1 Adversarial Verification

Author: teamwork_challenger (critic & specialist)
Workspace: /home/ator/BF2
"""

import math
import os
import re
import sys
import unittest
from typing import Dict, List, Tuple, Any, Set
import numpy as np

# BF2 vanilla static mesh whitelist (European urban & rural)
VANILLA_STATIC_MESHES = {
    "eu_building01", "eu_building02", "eu_office_01",
    "eu_house_01", "eu_house_02",
    "me_house_01", "me_house_02", "me_house_03", "me_house_04",
    "me_house_05", "me_house_06", "me_house_07", "me_house_08",
    "me_apartment_01", "citybuilding_01",
    "farmhouse", "barn_01", "barn_02", "shed_01", "wooden_shed", "warehouse_01"
}

STATIC_OBJECTS_PATH = "/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con"
HEIGHTMAP_PATH = "/home/ator/BF2/Heightmap.raw"


class IndependentHeightmapSampler:
    """Independent implementation of BF2 Heightmap elevation sampler."""
    def __init__(self, raw_path: str = HEIGHTMAP_PATH):
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Heightmap not found at {raw_path}")
        self.grid_size = 2049
        self.scale_xz = 2.0
        self.scale_y = 0.01
        self.world_half = 2048.0
        with open(raw_path, "rb") as f:
            raw_bytes = f.read()
        expected_bytes = self.grid_size * self.grid_size * 2
        assert len(raw_bytes) == expected_bytes, f"Heightmap byte size mismatch: expected {expected_bytes}, got {len(raw_bytes)}"
        self.data = np.frombuffer(raw_bytes, dtype="<u2").reshape((self.grid_size, self.grid_size))

    def sample_bilinear(self, x: float, z: float) -> float:
        """
        Bilinear elevation interpolation matching Refractor 2 specifications:
        u = (x + 2048.0) / 2.0
        v = (z + 2048.0) / 2.0
        """
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


class AdversarialStaticObjectsStressTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw_bytes: bytes = b""
        cls.raw_lines: List[str] = []
        cls.objects: List[Dict[str, Any]] = []
        cls.blocks: List[Dict[str, Any]] = []
        cls.heightmap = IndependentHeightmapSampler()

        if not os.path.exists(STATIC_OBJECTS_PATH):
            raise FileNotFoundError(f"Missing {STATIC_OBJECTS_PATH}")

        with open(STATIC_OBJECTS_PATH, "rb") as f:
            cls.raw_bytes = f.read()

        cls.raw_lines = cls.raw_bytes.decode("utf-8").splitlines()
        cls._parse_strictly()

    @classmethod
    def _parse_strictly(cls):
        """Strict line-by-line parser verifying object blocks and delimiters."""
        current_obj = None
        state = 0  # 0: waiting Object.create, 1: expect absolutePosition, 2: expect rotation, 3: expect layer

        for line_num, line in enumerate(cls.raw_lines, start=1):
            s = line.strip()
            if not s or s.startswith("rem"):
                continue

            # Header / footer editor commands
            if s.startswith("if ") or s == "endIf" or s.startswith("console."):
                continue

            tokens = s.split(maxsplit=1)
            cmd = tokens[0]
            arg = tokens[1] if len(tokens) > 1 else ""

            if cmd == "Object.create":
                if state != 0:
                    cls.blocks.append({"type": "malformed_block", "line": line_num, "error": f"Unexpected Object.create in state {state}"})
                current_obj = {"template": arg.strip(), "create_line": line_num}
                state = 1
            elif cmd == "Object.absolutePosition":
                if state != 1:
                    cls.blocks.append({"type": "malformed_block", "line": line_num, "error": f"Unexpected Object.absolutePosition in state {state}"})
                if current_obj is not None:
                    current_obj["pos_raw"] = arg.strip()
                    current_obj["pos_line"] = line_num
                state = 2
            elif cmd == "Object.rotation":
                if state != 2:
                    cls.blocks.append({"type": "malformed_block", "line": line_num, "error": f"Unexpected Object.rotation in state {state}"})
                if current_obj is not None:
                    current_obj["rot_raw"] = arg.strip()
                    current_obj["rot_line"] = line_num
                state = 3
            elif cmd == "Object.layer":
                if state != 3:
                    cls.blocks.append({"type": "malformed_block", "line": line_num, "error": f"Unexpected Object.layer in state {state}"})
                if current_obj is not None:
                    current_obj["layer_raw"] = arg.strip()
                    current_obj["layer_line"] = line_num
                    cls.objects.append(current_obj)
                current_obj = None
                state = 0
            else:
                cls.blocks.append({"type": "unrecognized_command", "line": line_num, "command": cmd})

        if state != 0:
            cls.blocks.append({"type": "unclosed_object_block", "error": f"File ended with incomplete object in state {state}"})

    # -------------------------------------------------------------------------
    # 1. Byte-level & Encoding Integrity
    # -------------------------------------------------------------------------
    def test_file_encoding_and_no_bom(self):
        """Stress-test: Verify file is valid UTF-8 without UTF-8 BOM (0xEF, 0xBB, 0xBF)."""
        self.assertFalse(self.raw_bytes.startswith(b"\xef\xbb\xbf"), "StaticObjects.con has illegal UTF-8 BOM header")
        self.assertFalse(b"\x00" in self.raw_bytes, "StaticObjects.con contains illegal null bytes")

    def test_file_line_endings_and_no_carriage_returns(self):
        """Stress-test: Check line ending hygiene (Unix LF vs CRLF)."""
        crlf_count = self.raw_bytes.count(b"\r\n")
        lf_count = self.raw_bytes.count(b"\n")
        self.assertEqual(crlf_count, 0, f"Found {crlf_count} Windows CRLF line endings; standard Unix LF required")
        self.assertGreater(lf_count, 1000, "Too few lines in file")

    # -------------------------------------------------------------------------
    # 2. Structure, Syntax, and Grammar Stress Tests
    # -------------------------------------------------------------------------
    def test_syntax_no_structural_errors(self):
        """Stress-test: Verify no malformed object blocks, missing properties, or unclosed blocks."""
        errors = [b for b in self.blocks if b.get("type") in ("malformed_block", "unclosed_object_block", "unrecognized_command")]
        self.assertEqual(len(errors), 0, f"Found structural syntax violations: {errors}")

    def test_editor_blocks_balanced(self):
        """Stress-test: Header and footer editor conditional blocks must be perfectly balanced."""
        if_count = 0
        endif_count = 0
        for line in self.raw_lines:
            s = line.strip()
            if s.startswith("if "):
                if_count += 1
            elif s == "endIf":
                endif_count += 1
        self.assertEqual(if_count, 2, f"Expected 2 'if' statements, found {if_count}")
        self.assertEqual(endif_count, 2, f"Expected 2 'endIf' statements, found {endif_count}")

    def test_case_sensitivity_of_commands(self):
        """Stress-test: Verify exact casing for all BF2 engine commands (Object.create, etc.)."""
        casing_regex = re.compile(r"^(object\.|console\.|endif|if\b)", re.IGNORECASE)
        for line_num, line in enumerate(self.raw_lines, start=1):
            s = line.strip()
            if not s or s.startswith("rem"):
                continue
            match = casing_regex.match(s)
            if match:
                token = s.split()[0]
                self.assertIn(token, ["Object.create", "Object.absolutePosition", "Object.rotation", "Object.layer", "if", "endIf", "console.allowMultipleFileLoad"],
                              f"Line {line_num}: Illegal command casing '{token}'")

    # -------------------------------------------------------------------------
    # 3. Vector Formatting & Slash Delimiter Whitespace
    # -------------------------------------------------------------------------
    def test_vector_slash_delimiters_no_whitespace(self):
        """Adversarial challenge: Check EVERY line in StaticObjects.con for illegal whitespace around slashes."""
        whitespace_slash_regex = re.compile(r"(\s/|/\s)")
        violations = []
        for line_num, line in enumerate(self.raw_lines, start=1):
            s = line.strip()
            if not s or s.startswith("rem"):
                continue
            if "/" in s:
                if whitespace_slash_regex.search(s):
                    violations.append((line_num, line))
        self.assertEqual(len(violations), 0, f"Found whitespace around slash delimiters at lines: {violations}")

    def test_strict_vector_token_formatting(self):
        """Verify vector format strictly matches -?X.XXX/-?Y.YYY/-?Z.ZZZ (3 decimal float format)."""
        vec3_pattern = re.compile(r"^-?\d+\.\d{3}/-?\d+\.\d{3}/-?\d+\.\d{3}$")
        for obj in self.objects:
            pos_str = obj["pos_raw"]
            self.assertTrue(vec3_pattern.match(pos_str),
                            f"Line {obj['pos_line']}: Malformed position vector '{pos_str}' (expected 3 decimal places without spaces)")
            rot_str = obj["rot_raw"]
            self.assertTrue(vec3_pattern.match(rot_str),
                            f"Line {obj['rot_line']}: Malformed rotation vector '{rot_str}' (expected 3 decimal places without spaces)")

    def test_layer_is_integer_one(self):
        """Verify Object.layer is strictly 1 for static objects."""
        for obj in self.objects:
            layer_str = obj["layer_raw"]
            self.assertEqual(layer_str, "1", f"Line {obj['layer_line']}: Object.layer must be 1, found '{layer_str}'")

    # -------------------------------------------------------------------------
    # 4. Coordinates, Float Validity, Bounds, and NaN/Inf Stress Tests
    # -------------------------------------------------------------------------
    def test_positions_no_nan_or_inf(self):
        """Adversarial stress-test: Check for NaN, Inf, -Inf, or non-finite values in coordinates."""
        for obj in self.objects:
            parts = [float(p) for p in obj["pos_raw"].split("/")]
            self.assertEqual(len(parts), 3, f"Line {obj['pos_line']}: Position must have 3 coordinates")
            for coord, name in zip(parts, ["X", "Y", "Z"]):
                self.assertFalse(math.isnan(coord), f"Line {obj['pos_line']}: Coordinate {name} is NaN")
                self.assertFalse(math.isinf(coord), f"Line {obj['pos_line']}: Coordinate {name} is Inf")

    def test_rotations_no_nan_or_inf(self):
        """Adversarial stress-test: Check for NaN, Inf in rotation vectors."""
        for obj in self.objects:
            parts = [float(p) for p in obj["rot_raw"].split("/")]
            self.assertEqual(len(parts), 3, f"Line {obj['rot_line']}: Rotation must have 3 components")
            for comp, name in zip(parts, ["Yaw", "Pitch", "Roll"]):
                self.assertFalse(math.isnan(comp), f"Line {obj['rot_line']}: Rotation {name} is NaN")
                self.assertFalse(math.isinf(comp), f"Line {obj['rot_line']}: Rotation {name} is Inf")

    def test_coordinates_cartesian_bounds(self):
        """Adversarial test: Check that ALL X, Z strictly fall inside [-2048.0, 2048.0]."""
        for obj in self.objects:
            x, y, z = [float(p) for p in obj["pos_raw"].split("/")]
            self.assertGreaterEqual(x, -2048.0, f"Line {obj['pos_line']}: X={x} < -2048.0 (out of bounds)")
            self.assertLessEqual(x, 2048.0, f"Line {obj['pos_line']}: X={x} > 2048.0 (out of bounds)")
            self.assertGreaterEqual(z, -2048.0, f"Line {obj['pos_line']}: Z={z} < -2048.0 (out of bounds)")
            self.assertLessEqual(z, 2048.0, f"Line {obj['pos_line']}: Z={z} > 2048.0 (out of bounds)")

    def test_no_underwater_placement(self):
        """Adversarial test: Check that NO static object has elevation Y < 270.0m (Ljubljanica water table)."""
        underwater = []
        for obj in self.objects:
            x, y, z = [float(p) for p in obj["pos_raw"].split("/")]
            if y < 270.0:
                underwater.append((obj["pos_line"], obj["template"], y))
        self.assertEqual(len(underwater), 0, f"Found {len(underwater)} underwater buildings (Y < 270.0m): {underwater[:5]}")

    def test_elevation_upper_bound(self):
        """Adversarial test: Check that NO static object has elevation Y > 455.0m (exceeds Golovec terrain peak)."""
        for obj in self.objects:
            _, y, _ = [float(p) for p in obj["pos_raw"].split("/")]
            self.assertLessEqual(y, 455.0, f"Line {obj['pos_line']}: Y={y} exceeds maximum terrain peak 455.0m")

    def test_pitch_and_roll_are_zero(self):
        """Stress-test: BF2 static building instances must have zero Pitch and Roll (standing upright on terrain)."""
        for obj in self.objects:
            yaw, pitch, roll = [float(p) for p in obj["rot_raw"].split("/")]
            self.assertEqual(pitch, 0.0, f"Line {obj['rot_line']}: Non-zero pitch {pitch}")
            self.assertEqual(roll, 0.0, f"Line {obj['rot_line']}: Non-zero roll {roll}")
            self.assertGreaterEqual(yaw, -180.0, f"Line {obj['rot_line']}: Yaw {yaw} < -180.0")
            self.assertLessEqual(yaw, 180.0, f"Line {obj['rot_line']}: Yaw {yaw} > 180.0")

    # -------------------------------------------------------------------------
    # 5. Independent Heightmap Grounding Oracle Stress Tests
    # -------------------------------------------------------------------------
    def test_heightmap_grounding_precision(self):
        """
        Adversarial test: Compute deviation between object Y and independent bilinear heightmap elevation.
        Fails if any building deviation exceeds 0.75m.
        Also verifies statistical distribution: max, mean, std deviation.
        """
        deviations = []
        violations = []
        for obj in self.objects:
            x, y, z = [float(p) for p in obj["pos_raw"].split("/")]
            expected_y = self.heightmap.sample_bilinear(x, z)
            diff = abs(y - expected_y)
            deviations.append(diff)
            if diff > 0.75:
                violations.append((obj["pos_line"], obj["template"], (x, y, z), expected_y, diff))

        max_dev = max(deviations) if deviations else 0.0
        mean_dev = float(np.mean(deviations)) if deviations else 0.0
        p99_dev = float(np.percentile(deviations, 99)) if deviations else 0.0

        print(f"\n[Grounding Analysis] Tested {len(deviations)} objects:")
        print(f"  Max elevation deviation: {max_dev:.6f}m")
        print(f"  Mean elevation deviation: {mean_dev:.6f}m")
        print(f"  99th percentile deviation: {p99_dev:.6f}m")

        self.assertEqual(len(violations), 0, f"Found {len(violations)} grounding violations (>0.75m): {violations[:5]}")
        # Mathematical precision check: max deviation should be < 0.001m
        self.assertLess(max_dev, 0.001, f"Max deviation {max_dev:.6f}m exceeds sub-millimeter precision threshold 0.001m")

    # -------------------------------------------------------------------------
    # 6. Duplicate Positions, Collisions, and Spatial Clearance
    # -------------------------------------------------------------------------
    def test_no_exact_duplicate_positions(self):
        """Adversarial test: Check that no two static buildings share the exact same (X, Z) coordinates."""
        seen_coords = {}
        duplicates = []
        for obj in self.objects:
            x, y, z = [float(p) for p in obj["pos_raw"].split("/")]
            key = (round(x, 3), round(z, 3))
            if key in seen_coords:
                duplicates.append((seen_coords[key], obj["pos_line"], key))
            else:
                seen_coords[key] = obj["pos_line"]
        self.assertEqual(len(duplicates), 0, f"Found duplicate building positions: {duplicates}")

    def test_building_collision_and_clearance(self):
        """
        Adversarial test: Check minimum distance between all pairs of buildings.
        Requires distance >= 2.0m (no direct model overlap).
        Worker claims clearance R >= 30.0m from spatial thinning.
        """
        coords = np.array([[float(p) for p in obj["pos_raw"].split("/")] for obj in self.objects])
        xz = coords[:, [0, 2]]  # N x 2

        # Fast spatial hashing
        cell_size = 35.0
        grid: Dict[Tuple[int, int], List[int]] = {}
        min_dist = float("inf")
        closest_pair = None

        for idx, (x, z) in enumerate(xz):
            gx, gz = int(math.floor(x / cell_size)), int(math.floor(z / cell_size))
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    neighbor = (gx + dx, gz + dz)
                    if neighbor in grid:
                        for other_idx in grid[neighbor]:
                            ox, oz = xz[other_idx]
                            dist = math.hypot(x - ox, z - oz)
                            if dist < min_dist:
                                min_dist = dist
                                closest_pair = (idx, other_idx)
            grid.setdefault((gx, gz), []).append(idx)

        print(f"\n[Clearance Analysis] Minimum distance between any two buildings: {min_dist:.3f}m")
        if closest_pair:
            o1 = self.objects[closest_pair[0]]
            o2 = self.objects[closest_pair[1]]
            print(f"  Closest pair: line {o1['pos_line']} ({o1['template']}) and line {o2['pos_line']} ({o2['template']})")

        self.assertGreaterEqual(min_dist, 2.0, f"Building collision detected: distance {min_dist:.3f}m < 2.0m")
        self.assertGreaterEqual(min_dist, 30.0, f"Worker claimed 30.0m clearance, but min distance is {min_dist:.3f}m")

    # -------------------------------------------------------------------------
    # 7. Template Whitelist and Diversity Stress Tests
    # -------------------------------------------------------------------------
    def test_all_templates_are_vanilla_bf2(self):
        """Adversarial test: Check that every single template name belongs to the BF2 European vanilla set."""
        template_counts: Dict[str, int] = {}
        invalid_templates = []
        for obj in self.objects:
            t = obj["template"]
            template_counts[t] = template_counts.get(t, 0) + 1
            if t not in VANILLA_STATIC_MESHES:
                invalid_templates.append((obj["create_line"], t))

        print("\n[Template Distribution]")
        for t, count in sorted(template_counts.items(), key=lambda x: -x[1]):
            pct = 100.0 * count / len(self.objects)
            print(f"  {t:20s}: {count:4d} ({pct:5.1f}%)")

        self.assertEqual(len(invalid_templates), 0, f"Found non-vanilla static mesh templates: {invalid_templates}")
        self.assertGreaterEqual(len(template_counts), 8, f"Too few unique template types: {len(template_counts)}")

    # -------------------------------------------------------------------------
    # 8. Object Count, Budget, and Spatial Coverage Stress Tests
    # -------------------------------------------------------------------------
    def test_object_count_within_aaa_budget(self):
        """Verify total static object count is within the performance budget [500, 1500]."""
        total = len(self.objects)
        print(f"\n[Object Count] Total objects parsed: {total}")
        self.assertGreaterEqual(total, 500, f"Object count {total} below minimum budget 500")
        self.assertLessEqual(total, 1500, f"Object count {total} exceeds maximum budget 1500")

    def test_spatial_coverage_all_four_quadrants(self):
        """Stress-test: Verify static buildings exist across all 4 spatial quadrants (SW, SE, NW, NE)."""
        quads = {"SW": 0, "SE": 0, "NW": 0, "NE": 0}
        for obj in self.objects:
            x, _, z = [float(p) for p in obj["pos_raw"].split("/")]
            if x < 0 and z < 0:
                quads["SW"] += 1
            elif x >= 0 and z < 0:
                quads["SE"] += 1
            elif x < 0 and z >= 0:
                quads["NW"] += 1
            else:
                quads["NE"] += 1

        print(f"\n[Spatial Distribution Across Quadrants]")
        for q, count in quads.items():
            pct = 100.0 * count / len(self.objects)
            print(f"  Quadrant {q}: {count:4d} buildings ({pct:5.1f}%)")

        for q, count in quads.items():
            self.assertGreater(count, 0, f"Quadrant {q} has no buildings")
            self.assertGreaterEqual(count, 30, f"Quadrant {q} has unexpectedly low representation ({count} < 30)")

    def test_world_span_extent(self):
        """Verify building extents span substantially across the 4096m world."""
        xs = [float(p.split("/")[0]) for p in [o["pos_raw"] for o in self.objects]]
        zs = [float(p.split("/")[2]) for p in [o["pos_raw"] for o in self.objects]]
        span_x = max(xs) - min(xs)
        span_z = max(zs) - min(zs)
        print(f"\n[World Span Extents]")
        print(f"  X span: {span_x:.1f}m (min: {min(xs):.1f}, max: {max(xs):.1f})")
        print(f"  Z span: {span_z:.1f}m (min: {min(zs):.1f}, max: {max(zs):.1f})")
        self.assertGreater(span_x, 3500.0, f"X span {span_x}m is less than expected 3500m")
        self.assertGreater(span_z, 3500.0, f"Z span {span_z}m is less than expected 3500m")


if __name__ == "__main__":
    unittest.main(verbosity=2)
