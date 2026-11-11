"""
Tier 1: Feature Coverage Test Suite for BF2 Slovenia (Golovec) Level Package.
Covers:
- Mandatory file existence (init.con, Heightdata.con, Terrain.con, Sky.con, Water.con,
  StaticObjects.con, OvergrowthSystem.con, GameplayObjects.con, Overgrowth/Overgrowth.raw).
- Basic syntax & content non-empty.
- Valid command namespaces.
- Block structure (if v_arg1 == BF2Editor ... else ... endIf).
- Vector formatting (X/Y/Z slash-delimited with no spaces).
- Case sensitivity of Refractor 2 commands.
"""

import os
import re
import unittest
from typing import List, Set

from con_parser import ConParser, LEVEL_DIR


class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Comprehensive feature coverage tests for Refractor 2 configuration files."""

    # -------------------------------------------------------------------------
    # 1. Mandatory File Existence (>=5 tests)
    # -------------------------------------------------------------------------
    def test_mandatory_file_init_con_exists(self):
        """Verify master level conductor init.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "init.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_heightdata_con_exists(self):
        """Verify terrain height parameters Heightdata.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "Heightdata.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_terrain_con_exists(self):
        """Verify terrain physics and water definition Terrain.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "Terrain.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_sky_con_exists(self):
        """Verify atmospheric lighting and skydome Sky.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "Sky.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_water_con_exists(self):
        """Verify water surface and river color Water.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "Water.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_staticobjects_con_exists(self):
        """Verify static mesh instances StaticObjects.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_overgrowthsystem_con_exists(self):
        """Verify overgrowth foliage definition OvergrowthSystem.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "OvergrowthSystem.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_gameplayobjects_con_exists(self):
        """Verify Conquest gamemode GameplayObjects.con exists in level package."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        self.assertTrue(os.path.isfile(p), f"Mandatory level file missing: {p}")

    def test_mandatory_file_overgrowth_raw_exists(self):
        """Verify binary density mask Overgrowth/Overgrowth.raw exists in level package."""
        p = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
        self.assertTrue(os.path.isfile(p), f"Mandatory density mask missing: {p}")

    # -------------------------------------------------------------------------
    # 2. Syntax & Content Non-Empty / Clean Encoding (>=5 tests)
    # -------------------------------------------------------------------------
    def test_con_files_non_empty(self):
        """Verify all .con files contain meaningful non-empty configuration content."""
        con_files = [
            "init.con", "Heightdata.con", "Terrain.con", "Sky.con",
            "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"
        ]
        for cf in con_files:
            p = os.path.join(LEVEL_DIR, cf)
            if not os.path.isfile(p):
                self.fail(f"Cannot check content size; file missing: {p}")
            sz = os.path.getsize(p)
            self.assertGreater(sz, 50, f"File {cf} is suspiciously small ({sz} bytes)")

    def test_con_files_have_no_null_bytes(self):
        """Verify plain-text .con files contain no NULL bytes or corrupted binary chars."""
        con_files = [
            "init.con", "Heightdata.con", "Terrain.con", "Sky.con",
            "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"
        ]
        for cf in con_files:
            p = os.path.join(LEVEL_DIR, cf)
            self.assertTrue(os.path.isfile(p), f"File missing: {p}")
            with open(p, "rb") as f:
                content = f.read()
                self.assertNotIn(b"\x00", content, f"Null byte detected in plaintext script {cf}")

    def test_con_files_valid_ascii_or_utf8(self):
        """Verify all .con files decode cleanly as valid UTF-8 without replacement errors."""
        con_files = [
            "init.con", "Heightdata.con", "Terrain.con", "Sky.con",
            "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"
        ]
        for cf in con_files:
            p = os.path.join(LEVEL_DIR, cf)
            self.assertTrue(os.path.isfile(p), f"File missing: {p}")
            with open(p, "rb") as f:
                content = f.read()
                try:
                    content.decode("utf-8")
                except UnicodeDecodeError as e:
                    self.fail(f"Unicode decode error in {cf}: {e}")

    def test_con_files_have_executable_commands(self):
        """Verify .con files contain active engine commands beyond just comments."""
        con_files = [
            "init.con", "Heightdata.con", "Terrain.con", "Sky.con",
            "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"
        ]
        for cf in con_files:
            p = os.path.join(LEVEL_DIR, cf)
            self.assertTrue(os.path.isfile(p), f"File missing: {p}")
            parser = ConParser(p)
            clean_lines = parser.get_clean_lines()
            self.assertGreater(len(clean_lines), 2, f"File {cf} contains no executable commands")

    def test_con_files_no_unterminated_quotes(self):
        """Verify no unterminated quotation marks exist in argument strings."""
        con_files = [
            "init.con", "Heightdata.con", "Terrain.con", "Sky.con",
            "Water.con", "StaticObjects.con", "OvergrowthSystem.con", "GameplayObjects.con"
        ]
        for cf in con_files:
            p = os.path.join(LEVEL_DIR, cf)
            self.assertTrue(os.path.isfile(p), f"File missing: {p}")
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                for line_idx, line in enumerate(f, 1):
                    # Exclude comments
                    s = line.strip()
                    if s.lower().startswith("rem"):
                        continue
                    quote_count = s.count('"')
                    self.assertEqual(quote_count % 2, 0, f"Unterminated quote in {cf} line {line_idx}: {line}")

    # -------------------------------------------------------------------------
    # 3. Valid Command Namespaces per File (>=5 tests)
    # -------------------------------------------------------------------------
    def test_namespaces_init_con(self):
        """Verify init.con uses valid Refractor 2 master initialization commands."""
        p = os.path.join(LEVEL_DIR, "init.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        valid_cmds = {"if", "else", "endIf", "run", "LevelSettings.InitWorld",
                      "LevelSettings.CustomTextureSuffix", "texturemanager.customTextureSuffix"}
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertIn(cmd, valid_cmds, f"Unexpected command '{cmd}' in init.con line {line_idx}")

    def test_namespaces_heightdata_con(self):
        """Verify Heightdata.con uses heightmap.* namespace commands exclusively."""
        p = os.path.join(LEVEL_DIR, "Heightdata.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith("heightmap."), f"Unexpected command '{cmd}' in Heightdata.con line {line_idx}")

    def test_namespaces_terrain_con(self):
        """Verify Terrain.con uses terrain.* namespace commands exclusively."""
        p = os.path.join(LEVEL_DIR, "Terrain.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith("terrain."), f"Unexpected command '{cmd}' in Terrain.con line {line_idx}")

    def test_namespaces_sky_con(self):
        """Verify Sky.con uses Renderer.* and Skydome.* namespace commands."""
        p = os.path.join(LEVEL_DIR, "Sky.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        valid_prefixes = ("Renderer.", "Skydome.")
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith(valid_prefixes), f"Unexpected command '{cmd}' in Sky.con line {line_idx}")

    def test_namespaces_water_con(self):
        """Verify Water.con uses Water.* namespace commands exclusively."""
        p = os.path.join(LEVEL_DIR, "Water.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith("Water."), f"Unexpected command '{cmd}' in Water.con line {line_idx}")

    def test_namespaces_staticobjects_con(self):
        """Verify StaticObjects.con uses Object.* and console.* commands."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        valid_prefixes = ("Object.", "console.", "if", "else", "endIf")
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith(valid_prefixes), f"Unexpected command '{cmd}' in StaticObjects.con line {line_idx}")

    def test_namespaces_overgrowthsystem_con(self):
        """Verify OvergrowthSystem.con uses Overgrowth.* and OvergrowthType.* commands."""
        p = os.path.join(LEVEL_DIR, "OvergrowthSystem.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        valid_prefixes = ("Overgrowth.", "OvergrowthType.")
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith(valid_prefixes), f"Unexpected command '{cmd}' in OvergrowthSystem.con line {line_idx}")

    def test_namespaces_gameplayobjects_con(self):
        """Verify GameplayObjects.con uses CombatArea*, ObjectTemplate*, and Object* commands."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        valid_prefixes = ("CombatAreaManager.", "CombatArea.", "ObjectTemplate.", "Object.", "if", "else", "endIf")
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith(valid_prefixes), f"Unexpected command '{cmd}' in GameplayObjects.con line {line_idx}")

    # -------------------------------------------------------------------------
    # 4. Block Structure Verification (>=5 tests)
    # -------------------------------------------------------------------------
    def test_block_structure_init_con(self):
        """Verify init.con contains balanced BF2Editor conditional block."""
        p = os.path.join(LEVEL_DIR, "init.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        res = parser.check_block_structure()
        self.assertTrue(res["balanced"], f"Unbalanced blocks in init.con: {res['errors']}")
        self.assertGreater(len(res["blocks"]), 0, "init.con missing conditional editor block")
        cond = res["blocks"][0]["condition"]
        self.assertIn("v_arg1 == BF2Editor", cond, f"Unexpected condition in init.con: {cond}")

    def test_block_structure_staticobjects_con(self):
        """Verify StaticObjects.con contains balanced conditional console blocks."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        res = parser.check_block_structure()
        self.assertTrue(res["balanced"], f"Unbalanced blocks in StaticObjects.con: {res['errors']}")

    def test_block_structure_all_con_files_balanced(self):
        """Verify all .con files in level package have balanced if/endIf blocks."""
        self.assertTrue(os.path.isdir(LEVEL_DIR), f"Level directory missing: {LEVEL_DIR}")
        con_count = 0
        for root, _, files in os.walk(LEVEL_DIR):
            for file in files:
                if file.endswith(".con"):
                    con_count += 1
                    p = os.path.join(root, file)
                    parser = ConParser(p)
                    res = parser.check_block_structure()
                    self.assertTrue(res["balanced"], f"Unbalanced blocks in {file}: {res['errors']}")
        self.assertGreaterEqual(con_count, 8, f"Expected at least 8 .con files in {LEVEL_DIR}, found {con_count}")

    def test_block_structure_nested_depth(self):
        """Verify nesting depth of conditional blocks does not exceed Refractor 2 engine limits (<= 4)."""
        p = os.path.join(LEVEL_DIR, "init.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        depth = 0
        max_depth = 0
        for _, line in parser.get_clean_lines():
            cmd = line.split()[0]
            if cmd == "if":
                depth += 1
                max_depth = max(max_depth, depth)
            elif cmd == "endIf":
                depth -= 1
        self.assertLessEqual(max_depth, 4, f"Excessive nesting depth {max_depth} in init.con")

    def test_block_structure_no_orphaned_else(self):
        """Verify no orphaned else statements occur in any script."""
        self.assertTrue(os.path.isdir(LEVEL_DIR), f"Level directory missing: {LEVEL_DIR}")
        con_count = 0
        for root, _, files in os.walk(LEVEL_DIR):
            for file in files:
                if file.endswith(".con"):
                    con_count += 1
                    p = os.path.join(root, file)
                    parser = ConParser(p)
                    res = parser.check_block_structure()
                    for err in res["errors"]:
                        self.assertNotIn("without matching 'if'", err)
        self.assertGreaterEqual(con_count, 8, f"Expected at least 8 .con files in {LEVEL_DIR}, found {con_count}")

    # -------------------------------------------------------------------------
    # 5. Vector Formatting: Slash-delimited with NO spaces (>=5 tests)
    # -------------------------------------------------------------------------
    def test_vector_formatting_staticobjects(self):
        """Verify Object.absolutePosition and Object.rotation have no spaces around slashes."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        violations = parser.check_vector_syntax_no_spaces()
        self.assertEqual(len(violations), 0, f"Found spaces around vector slashes in StaticObjects.con: {violations[:5]}")

    def test_vector_formatting_gameplayobjects(self):
        """Verify CombatArea and Object vectors have no spaces around slashes."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        violations = parser.check_vector_syntax_no_spaces()
        self.assertEqual(len(violations), 0, f"Found spaces around vector slashes in GameplayObjects.con: {violations[:5]}")

    def test_vector_formatting_heightdata(self):
        """Verify heightmap.setScale vectors have no spaces around slashes."""
        p = os.path.join(LEVEL_DIR, "Heightdata.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        violations = parser.check_vector_syntax_no_spaces()
        self.assertEqual(len(violations), 0, f"Found spaces around vector slashes in Heightdata.con: {violations[:5]}")

    def test_vector_formatting_terrain(self):
        """Verify terrain.primaryWorldScale vectors have no spaces around slashes."""
        p = os.path.join(LEVEL_DIR, "Terrain.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        violations = parser.check_vector_syntax_no_spaces()
        self.assertEqual(len(violations), 0, f"Found spaces around vector slashes in Terrain.con: {violations[:5]}")

    def test_vector_formatting_sky_water(self):
        """Verify color vectors in Sky.con and Water.con have no spaces around slashes."""
        for cf in ["Sky.con", "Water.con"]:
            p = os.path.join(LEVEL_DIR, cf)
            if not os.path.isfile(p):
                self.fail(f"File missing: {p}")
            parser = ConParser(p)
            violations = parser.check_vector_syntax_no_spaces()
            self.assertEqual(len(violations), 0, f"Found spaces around vector slashes in {cf}: {violations[:5]}")

    # -------------------------------------------------------------------------
    # 6. Case Sensitivity in Refractor 2 Commands (>=5 tests)
    # -------------------------------------------------------------------------
    def test_case_sensitivity_object_commands(self):
        """Verify 'Object.create' and 'Object.absolutePosition' use canonical PascalCase."""
        p = os.path.join(LEVEL_DIR, "StaticObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            if cmd.lower() == "object.create":
                self.assertEqual(cmd, "Object.create", f"Line {line_idx} has incorrect case '{cmd}'")
            elif cmd.lower() == "object.absoluteposition":
                self.assertEqual(cmd, "Object.absolutePosition", f"Line {line_idx} has incorrect case '{cmd}'")

    def test_case_sensitivity_combatarea_commands(self):
        """Verify CombatArea commands use canonical PascalCase."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            if cmd.lower() == "combatarea.create":
                self.assertEqual(cmd, "CombatArea.create", f"Line {line_idx} has incorrect case '{cmd}'")
            elif cmd.lower() == "combatarea.addareapoint":
                self.assertEqual(cmd, "CombatArea.addAreaPoint", f"Line {line_idx} has incorrect case '{cmd}'")

    def test_case_sensitivity_objecttemplate_commands(self):
        """Verify ObjectTemplate commands use canonical PascalCase."""
        p = os.path.join(LEVEL_DIR, "GameplayObjects.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            if cmd.lower().startswith("objecttemplate."):
                self.assertTrue(cmd.startswith("ObjectTemplate."), f"Line {line_idx} has incorrect namespace case '{cmd}'")

    def test_case_sensitivity_terrain_commands(self):
        """Verify terrain commands use canonical lowercase 'terrain.' namespace."""
        p = os.path.join(LEVEL_DIR, "Terrain.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith("terrain."), f"Line {line_idx} has non-standard case: '{cmd}'")

    def test_case_sensitivity_heightmap_commands(self):
        """Verify heightmap commands use canonical lowercase 'heightmap.' namespace."""
        p = os.path.join(LEVEL_DIR, "Heightdata.con")
        if not os.path.isfile(p):
            self.fail(f"File missing: {p}")
        parser = ConParser(p)
        for line_idx, line in parser.get_clean_lines():
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith("heightmap."), f"Line {line_idx} has non-standard case: '{cmd}'")


if __name__ == "__main__":
    unittest.main()
