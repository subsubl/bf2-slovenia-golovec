#!/usr/bin/env python3
"""
test_adversarial_overgrowth_species_syntax.py

Independent adversarial verification suite for Milestone 2 - Challenger 2.
Stress-tests /home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con against:
1. Strict line-by-line grammar and namespace parser (Overgrowth.*, OvergrowthType.*).
2. Refractor 2 engine state machine and command argument contracts.
3. Vanilla BF2 foliage mesh whitelisting.
4. Ecological suitability for Central European temperate mixed forest (Golovec, Slovenia).
5. Poisson-disc radius exclusion and density parameter physics.
6. Frustum rendering distance and LOD billboard impostor transition thresholds.
7. Sensitivity verification via synthetic mutation injections (negative testing oracle).
"""

import os
import re
import unittest
from typing import Dict, List, Tuple, Any, Set

CON_PATH = "/home/ator/BF2/levels/slovenia_golovec/OvergrowthSystem.con"

# Authoritative BF2 Vanilla Foliage Geometries
VANILLA_FOLIAGE_WHITELIST: Set[str] = {
    "fir_mixed02",
    "birch_green_1",
    "birch_green_2",
    "pine_dead",
    "me_olive03",
    "largebush",
    "pine_large",
    "oak_01",
}

# Geometries strictly prohibited in Slovenian temperate continental forest
DISALLOWED_BIOME_GEOMETRIES: Set[str] = {
    "me_olive03",  # Mediterranean / arid biome only
}

# Authorized Refractor 2 Overgrowth Grammar Commands and Arity
RECOGNIZED_COMMANDS: Dict[str, int] = {
    "Overgrowth.addMaterial": 2,          # <name: str> <id: int>
    "Overgrowth.setActiveMaterial": 1,     # <name: str>
    "Overgrowth.addType": 1,               # <name: str>
    "Overgrowth.setActiveType": 1,          # <name: str>
    "Overgrowth.viewDistance": 1,          # <distance: float>
    "Overgrowth.closeDistPercentage": 1,   # <percentage: float>
    "OvergrowthType.geometry": 1,          # <mesh: str>
    "OvergrowthType.density": 1,           # <val: float>
    "OvergrowthType.normalScale": 1,       # <val: float>
    "OvergrowthType.rotationScale": 1,     # <val: float>
    "OvergrowthType.minRadiusToSame": 1,   # <val: float>
    "OvergrowthType.minRadiusToOthers": 1, # <val: float>
}


class StrictOvergrowthConValidator:
    """Independent strict grammar parser and semantic validator for OvergrowthSystem.con."""

    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.errors: List[str] = []
        self.materials_added: Dict[str, int] = {}
        self.active_material: str = ""
        self.types_added: List[str] = []
        self.active_type: str = ""
        self.types_config: Dict[str, Dict[str, Any]] = {}
        self.global_settings: Dict[str, float] = {}
        self.clean_lines: List[Tuple[int, str]] = []
        self._parse()

    def _parse(self):
        lines = self.raw_text.splitlines()

        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue

            # Check remarks
            if stripped.lower().startswith("rem"):
                # Must be followed by space or end of string
                if len(stripped) > 3 and not stripped[3].isspace():
                    self.errors.append(f"Line {idx}: Malformed rem statement '{stripped}'")
                continue

            # Disallow alternative comment markers
            for marker in ("//", "/*", "#", ";", "--"):
                if stripped.startswith(marker):
                    self.errors.append(f"Line {idx}: Disallowed comment style '{marker}' in BF2 .con")

            # Must begin with allowed namespaces
            valid_prefixes = ("Overgrowth.", "OvergrowthType.")
            if not stripped.startswith(valid_prefixes):
                self.errors.append(f"Line {idx}: Non-comment line does not start with {valid_prefixes}: '{stripped}'")
                continue

            # Tokenize by whitespace
            tokens = stripped.split()
            cmd = tokens[0]
            args = tokens[1:]

            if cmd not in RECOGNIZED_COMMANDS:
                self.errors.append(f"Line {idx}: Unrecognized Overgrowth command '{cmd}'")
                continue

            expected_arity = RECOGNIZED_COMMANDS[cmd]
            if len(args) != expected_arity:
                self.errors.append(
                    f"Line {idx}: Command '{cmd}' expects {expected_arity} arguments, but got {len(args)}: {args}"
                )
                continue

            self.clean_lines.append((idx, stripped))

            # Dispatch semantic processing
            if cmd == "Overgrowth.addMaterial":
                mat_name = args[0]
                try:
                    mat_id = int(args[1])
                    if mat_id <= 0:
                        self.errors.append(f"Line {idx}: Material ID must be positive int, got {mat_id}")
                except ValueError:
                    self.errors.append(f"Line {idx}: Material ID must be integer, got '{args[1]}'")
                    mat_id = -1
                if mat_name in self.materials_added:
                    self.errors.append(f"Line {idx}: Duplicate material '{mat_name}'")
                self.materials_added[mat_name] = mat_id

            elif cmd == "Overgrowth.setActiveMaterial":
                mat_name = args[0]
                if mat_name not in self.materials_added:
                    self.errors.append(f"Line {idx}: setActiveMaterial '{mat_name}' before addMaterial")
                self.active_material = mat_name

            elif cmd == "Overgrowth.addType":
                type_name = args[0]
                if not self.active_material:
                    self.errors.append(f"Line {idx}: addType '{type_name}' with no active material")
                if type_name in self.types_added:
                    self.errors.append(f"Line {idx}: Duplicate species type '{type_name}'")
                self.types_added.append(type_name)
                self.types_config[type_name] = {}

            elif cmd == "Overgrowth.setActiveType":
                type_name = args[0]
                if type_name not in self.types_added:
                    self.errors.append(f"Line {idx}: setActiveType '{type_name}' without addType")
                self.active_type = type_name

            elif cmd.startswith("OvergrowthType."):
                prop = cmd.split(".", 1)[1]
                if not self.active_type:
                    self.errors.append(f"Line {idx}: Property '{cmd}' set without active type")
                    continue

                if prop in self.types_config[self.active_type]:
                    self.errors.append(f"Line {idx}: Duplicate property '{prop}' for type '{self.active_type}'")

                val_str = args[0]
                if prop == "geometry":
                    self.types_config[self.active_type][prop] = val_str
                else:
                    try:
                        val_float = float(val_str)
                        self.types_config[self.active_type][prop] = val_float
                    except ValueError:
                        self.errors.append(f"Line {idx}: Property '{prop}' expects float, got '{val_str}'")

            elif cmd == "Overgrowth.viewDistance":
                try:
                    self.global_settings["viewDistance"] = float(args[0])
                except ValueError:
                    self.errors.append(f"Line {idx}: viewDistance expects float, got '{args[0]}'")

            elif cmd == "Overgrowth.closeDistPercentage":
                try:
                    self.global_settings["closeDistPercentage"] = float(args[0])
                except ValueError:
                    self.errors.append(f"Line {idx}: closeDistPercentage expects float, got '{args[0]}'")

        # Semantic post-checks
        REQUIRED_PROPERTIES = {
            "geometry",
            "density",
            "normalScale",
            "rotationScale",
            "minRadiusToSame",
            "minRadiusToOthers",
        }
        for tname, cfg in self.types_config.items():
            missing = REQUIRED_PROPERTIES - set(cfg.keys())
            if missing:
                self.errors.append(f"Species type '{tname}' missing required properties: {missing}")

        for tname, cfg in self.types_config.items():
            if "density" in cfg and cfg["density"] <= 0.0:
                self.errors.append(f"Species type '{tname}' has non-positive density: {cfg['density']}")
            if "minRadiusToSame" in cfg and cfg["minRadiusToSame"] <= 0.0:
                self.errors.append(f"Species type '{tname}' has non-positive minRadiusToSame: {cfg['minRadiusToSame']}")
            if "minRadiusToOthers" in cfg and cfg["minRadiusToOthers"] <= 0.0:
                self.errors.append(f"Species type '{tname}' has non-positive minRadiusToOthers: {cfg['minRadiusToOthers']}")
            if "geometry" in cfg:
                geo = cfg["geometry"]
                if geo not in VANILLA_FOLIAGE_WHITELIST:
                    self.errors.append(f"Species type '{tname}' references non-vanilla mesh: '{geo}'")
                if geo in DISALLOWED_BIOME_GEOMETRIES:
                    self.errors.append(f"Species type '{tname}' references non-temperate mesh: '{geo}'")


class TestAdversarialOvergrowthVerification(unittest.TestCase):
    """Rigorous empirical test suite executed directly on OvergrowthSystem.con."""

    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(CON_PATH):
            raise FileNotFoundError(f"Target file does not exist: {CON_PATH}")
        with open(CON_PATH, "r", encoding="utf-8") as f:
            cls.raw_content = f.read()
        cls.validator = StrictOvergrowthConValidator(cls.raw_content)

    def test_file_integrity_and_cleanliness(self):
        """Verify file size, encoding, zero null bytes, no BOM, valid line endings."""
        sz = os.path.getsize(CON_PATH)
        self.assertGreater(sz, 50, f"File too small: {sz} bytes")
        self.assertLess(sz, 50_000, f"File suspiciously large: {sz} bytes")

        with open(CON_PATH, "rb") as f:
            raw_bytes = f.read()

        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"), "BOM detected in .con file")
        self.assertNotIn(b"\x00", raw_bytes, "Null byte detected in .con file")
        self.assertNotIn(b"\r\r", raw_bytes, "Corrupt double CR detected")

    def test_strict_grammar_and_zero_parser_errors(self):
        """Verify that every command line conforms to Refractor 2 Overgrowth grammar."""
        self.assertEqual(
            self.validator.errors,
            [],
            f"Strict parser encountered errors:\n" + "\n".join(self.validator.errors),
        )

    def test_no_illegal_slash_spacing(self):
        """Verify no illegal spaces exist around slashes if any are present."""
        for idx, line in enumerate(self.raw_content.splitlines(), 1):
            stripped = line.strip()
            if stripped.lower().startswith("rem") or not stripped:
                continue
            # Pattern matches digit or token separated from slash by whitespace
            self.assertFalse(
                re.search(r"\d+\.?\d*\s+/\s*|\s*/\s+\d+\.?\d*", stripped),
                f"Line {idx} has illegal whitespace around slash: '{stripped}'",
            )

    def test_namespace_prefixes_strictness(self):
        """Verify 100% of executable lines start with Overgrowth. or OvergrowthType."""
        valid_prefixes = ("Overgrowth.", "OvergrowthType.")
        clean_lines = self.validator.clean_lines
        self.assertGreater(len(clean_lines), 20, "Insufficient executable lines in OvergrowthSystem.con")

        for idx, line in clean_lines:
            cmd = line.split()[0]
            self.assertTrue(
                cmd.startswith(valid_prefixes),
                f"Line {idx} command '{cmd}' does not start with valid prefixes {valid_prefixes}",
            )

    def test_material_contract_temperate_forest(self):
        """Verify material temperate_forest is defined with ID 1 and activated."""
        materials = self.validator.materials_added
        self.assertEqual(len(materials), 1, f"Expected exactly 1 material, found {len(materials)}: {materials}")
        self.assertIn("temperate_forest", materials, "Missing required 'temperate_forest' material")
        self.assertEqual(materials["temperate_forest"], 1, "Material 'temperate_forest' ID must be 1")
        self.assertEqual(self.validator.active_material, "temperate_forest", "Active material must be 'temperate_forest'")

    def test_species_type_completeness(self):
        """Verify 7 species types are declared and configured with all 6 required properties."""
        types = self.validator.types_added
        self.assertEqual(len(types), 7, f"Expected 7 species types, got {len(types)}: {types}")

        expected_types = {"fir", "pine_large", "birch_1", "birch_2", "oak", "pine_dead", "undergrowth_bush"}
        self.assertEqual(set(types), expected_types, f"Species types mismatch: {set(types)} vs {expected_types}")

        for t in types:
            cfg = self.validator.types_config[t]
            for prop in ["geometry", "density", "normalScale", "rotationScale", "minRadiusToSame", "minRadiusToOthers"]:
                self.assertIn(prop, cfg, f"Type '{t}' missing property '{prop}'")

    def test_vanilla_geometry_whitelist(self):
        """Verify all foliage meshes are genuine BF2 vanilla foliage objects."""
        geometries = [cfg["geometry"] for cfg in self.validator.types_config.values()]
        for geo in geometries:
            self.assertIn(geo, VANILLA_FOLIAGE_WHITELIST, f"Mesh '{geo}' is not in vanilla foliage whitelist")

    def test_biome_suitability_temperate_european_forest(self):
        """Verify species match Slovenian temperate forest and exclude arid Mediterranean flora."""
        geometries = set(cfg["geometry"] for cfg in self.validator.types_config.values())

        # Olive tree strictly forbidden
        self.assertNotIn("me_olive03", geometries, "Mediterranean olive tree detected in Golovec forest!")

        # Key ecological groups
        has_conifer = bool(geometries.intersection({"fir_mixed02", "pine_large"}))
        has_deciduous = bool(geometries.intersection({"birch_green_1", "birch_green_2", "oak_01"}))
        has_deadwood = "pine_dead" in geometries
        has_undergrowth = "largebush" in geometries

        self.assertTrue(has_conifer, "Missing coniferous canopy species (fir/pine)")
        self.assertTrue(has_deciduous, "Missing deciduous broadleaf species (birch/oak)")
        self.assertTrue(has_deadwood, "Missing natural standing deadwood snag (pine_dead)")
        self.assertTrue(has_undergrowth, "Missing understory shrub layer (largebush)")

    def test_density_parameters_validity(self):
        """Verify all densities are strictly positive and satisfy ecological proportions."""
        configs = self.validator.types_config

        for tname, cfg in configs.items():
            d = cfg["density"]
            self.assertGreater(d, 0.0, f"Density for {tname} must be > 0, got {d}")
            self.assertLessEqual(d, 10.0, f"Density for {tname} exceeds upper safety limit 10.0: {d}")

        # Total cumulative density rate
        total_density = sum(cfg["density"] for cfg in configs.values())
        self.assertGreater(total_density, 5.0, f"Cumulative density too low: {total_density}")
        self.assertLess(total_density, 30.0, f"Cumulative density too high (risk of draw call bottleneck): {total_density}")

        # Ecological balance: Fir should have highest conifer density on mountain ridge
        self.assertGreaterEqual(configs["fir"]["density"], configs["pine_dead"]["density"], "Fir must be denser than snags")
        self.assertGreaterEqual(configs["birch_1"]["density"], configs["oak"]["density"], "Birch copse density proportion")

    def test_radius_spacing_physics_and_poisson_constraints(self):
        """Verify minRadiusToSame and minRadiusToOthers parameters are physically sound."""
        configs = self.validator.types_config

        for tname, cfg in configs.items():
            r_same = cfg["minRadiusToSame"]
            r_others = cfg["minRadiusToOthers"]

            self.assertGreater(r_same, 0.0, f"{tname}: minRadiusToSame must be > 0, got {r_same}")
            self.assertGreater(r_others, 0.0, f"{tname}: minRadiusToOthers must be > 0, got {r_others}")

            # Safe spacing: trunks should not overlap (< 0.5m) and forest should not be forced sparse (> 5.0m)
            self.assertGreaterEqual(r_same, 0.50, f"{tname}: minRadiusToSame {r_same} too small (trunk clipping)")
            self.assertLessEqual(r_same, 5.0, f"{tname}: minRadiusToSame {r_same} too large (over-thinning)")

            self.assertGreaterEqual(r_others, 0.30, f"{tname}: minRadiusToOthers {r_others} too small")
            self.assertLessEqual(r_others, 5.0, f"{tname}: minRadiusToOthers {r_others} too large")

        # Specific physical invariants:
        # Large trees (mature pine, oak) require larger crown clearance than birch clusters
        self.assertGreater(configs["pine_large"]["minRadiusToSame"], configs["birch_1"]["minRadiusToSame"])
        self.assertGreater(configs["oak"]["minRadiusToSame"], configs["birch_1"]["minRadiusToSame"])

        # Dead pine snags must be spaced out (isolated dead trees)
        self.assertGreaterEqual(configs["pine_dead"]["minRadiusToSame"], 1.5, "Dead pine snags should be spaced out")

        # Bushes should have smaller exclusion radius to others to grow near tree roots
        self.assertLessEqual(configs["undergrowth_bush"]["minRadiusToOthers"], 0.60, "Bushes must be able to spawn near trees")

    def test_slope_normal_and_rotation_conformance(self):
        """Verify geotropic tree growth (small normalScale) and full 360-degree yaw variation."""
        configs = self.validator.types_config

        tree_types = ["fir", "pine_large", "birch_1", "birch_2", "oak", "pine_dead"]
        for t in tree_types:
            ns = configs[t]["normalScale"]
            self.assertLessEqual(ns, 0.08, f"Tree {t} normalScale {ns} too high (trees would pitch unnaturally on slopes)")
            self.assertGreaterEqual(ns, 0.01, f"Tree {t} normalScale {ns} must be >= 0.01")

        # Shrub undergrowth should have higher normal scale to drape over hill contours
        bush_ns = configs["undergrowth_bush"]["normalScale"]
        self.assertGreaterEqual(bush_ns, 0.15, f"Bush normalScale {bush_ns} should conform more to terrain")

        # Full yaw randomization
        for tname, cfg in configs.items():
            self.assertEqual(cfg["rotationScale"], 180.0, f"{tname} rotationScale should be 180.0 for full 360 azimuthal variation")

    def test_view_distance_and_lod_impostor_thresholds(self):
        """Verify viewDistance is in gameplay range (400m - 800m) and LOD percentage is valid."""
        settings = self.validator.global_settings
        self.assertIn("viewDistance", settings, "Missing Overgrowth.viewDistance")
        self.assertIn("closeDistPercentage", settings, "Missing Overgrowth.closeDistPercentage")

        vd = settings["viewDistance"]
        cdp = settings["closeDistPercentage"]

        # View distance bounds: between 400m and 800m
        self.assertGreaterEqual(vd, 400.0, f"viewDistance {vd} too low for 4096m level")
        self.assertLessEqual(vd, 800.0, f"viewDistance {vd} too high for Refractor 2 DX9 performance budget")

        # Close distance percentage: between 0.15 and 0.35
        self.assertGreaterEqual(cdp, 0.15, f"closeDistPercentage {cdp} too low")
        self.assertLessEqual(cdp, 0.35, f"closeDistPercentage {cdp} too high")

        # Calculated impostor billboard transition distance
        impostor_dist = vd * cdp
        self.assertGreaterEqual(impostor_dist, 100.0, f"Impostor transition distance {impostor_dist}m too close (billboard popping)")
        self.assertLessEqual(impostor_dist, 250.0, f"Impostor transition distance {impostor_dist}m too far (excess high-poly vertex count)")

    def test_oracle_mutation_sensitivity(self):
        """Adversarial oracle validation: verify that validator catches synthetic corruptions."""
        # 1. Test isolated snippet failures
        isolated_mutations = [
            ("OvergrowthType.density 1.0", "Property 'OvergrowthType.density' set without active type"),
            ("Overgrowth.addType fir", "addType 'fir' with no active material"),
        ]
        for snippet, expected_err in isolated_mutations:
            v = StrictOvergrowthConValidator(snippet)
            self.assertTrue(len(v.errors) > 0, f"Oracle failed on snippet '{snippet}'")
            self.assertTrue(any(expected_err in e for e in v.errors), f"Expected '{expected_err}' in {v.errors}")

        # 2. Test corruptions appended to valid file
        appended_mutations = [
            # 1. Missing prefix
            ("addType rogue_tree", "Non-comment line does not start with"),
            # 2. Mediterranean olive tree
            ("Overgrowth.addType olive\nOvergrowth.setActiveType olive\nOvergrowthType.geometry me_olive03", "references non-temperate mesh"),
            # 3. Unknown modded mesh
            ("Overgrowth.addType fantasy\nOvergrowth.setActiveType fantasy\nOvergrowthType.geometry fantasy_tree_x", "references non-vanilla mesh"),
            # 4. Negative density
            ("Overgrowth.addType bad_dens\nOvergrowth.setActiveType bad_dens\nOvergrowthType.density -2.5", "has non-positive density"),
            # 5. Zero radius
            ("Overgrowth.addType zero_rad\nOvergrowth.setActiveType zero_rad\nOvergrowthType.minRadiusToSame 0.0", "has non-positive minRadiusToSame"),
            # 6. Unregistered type activation
            ("Overgrowth.setActiveType non_existent_type", "without addType"),
            # 7. Disallowed C-style comment
            ("// illegal comment", "Disallowed comment style"),
            # 8. Malformed material ID
            ("Overgrowth.addMaterial forest_invalid abc", "Material ID must be integer"),
            # 9. Duplicate property on active type
            ("OvergrowthType.density 1.0", "Duplicate property 'density' for type 'undergrowth_bush'"),
            # 10. Duplicate type definition
            ("Overgrowth.addType fir", "Duplicate species type 'fir'"),
        ]

        for mutation, expected_error_substr in appended_mutations:
            corrupted_content = self.raw_content + "\n" + mutation
            mut_validator = StrictOvergrowthConValidator(corrupted_content)
            self.assertTrue(
                len(mut_validator.errors) > 0,
                f"Oracle failed to reject mutation: '{mutation}'",
            )
            has_expected = any(expected_error_substr in err for err in mut_validator.errors)
            self.assertTrue(
                has_expected,
                f"Expected error substring '{expected_error_substr}' not found in errors: {mut_validator.errors}",
            )
    def test_simulated_poisson_foliage_generation(self):
        """Simulate Refractor 2 procedural foliage placement over Golovec ridge to verify non-zero distribution."""
        raw_path = "/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw"
        if not os.path.isfile(raw_path):
            self.skipTest("Overgrowth.raw not present for spatial simulation")

        import numpy as np
        raw = np.fromfile(raw_path, dtype=np.uint8).reshape((2049, 2049))
        sub = raw[1650:1700, 974:1024] # 100m x 100m patch on Golovec ridge
        mean_density = float(np.mean(sub))
        self.assertGreater(mean_density, 50.0, "Golovec ridge mask must have dense foliage")

        # Species configs parsed from OvergrowthSystem.con
        species_list = []
        for tname, cfg in self.validator.types_config.items():
            species_list.append({
                "name": tname,
                "density": cfg["density"],
                "r_same": cfg["minRadiusToSame"],
                "r_other": cfg["minRadiusToOthers"],
            })

        np.random.seed(1337)
        placed_points = [] # (x, z, species_idx)
        patch_factor = mean_density / 255.0

        for s_idx, sp in enumerate(species_list):
            n_candidates = int(sp["density"] * 50 * patch_factor)
            for _ in range(n_candidates):
                x = np.random.uniform(0.0, 100.0)
                z = np.random.uniform(0.0, 100.0)
                r_same = sp["r_same"]
                r_other = sp["r_other"]

                collision = False
                for px, pz, p_s_idx in placed_points:
                    dist = float(np.hypot(x - px, z - pz))
                    req = r_same if p_s_idx == s_idx else max(r_other, species_list[p_s_idx]["r_other"])
                    if dist < req:
                        collision = True
                        break
                if not collision:
                    placed_points.append((x, z, s_idx))

        self.assertGreater(len(placed_points), 100, f"Too few trees placed: {len(placed_points)}")
        self.assertLess(len(placed_points), 1000, f"Excessive density placed: {len(placed_points)}")

        counts = {}
        for _, _, s_idx in placed_points:
            sname = species_list[s_idx]["name"]
            counts[sname] = counts.get(sname, 0) + 1

        # All 7 species must appear
        self.assertEqual(len(counts), 7, f"Not all species populated: {counts}")
        for sname in self.validator.types_added:
            self.assertGreater(counts.get(sname, 0), 0, f"Species '{sname}' had 0 placed instances")

        # Fir must be the dominant conifer
        self.assertGreater(counts["fir"], counts["pine_large"], "Fir should outnumber large emergent pines")
        self.assertGreater(counts["fir"], counts["pine_dead"], "Fir should outnumber dead snags")


if __name__ == "__main__":
    unittest.main()

