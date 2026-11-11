#!/usr/bin/env python3
"""
test_m2_verification.py - Independent verification suite for Milestone 2 deliverables.
Tests Overgrowth.raw, 25 nDMP GeoTIFFs, and OvergrowthSystem.con.
"""

import os
import sys
import unittest
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

LEVEL_DIR = "/home/ator/BF2/levels/slovenia_golovec"
NDMP_DIR = "/home/ator/BF2/ndmp"
RAW_PATH = os.path.join(LEVEL_DIR, "Overgrowth", "Overgrowth.raw")
CON_PATH = os.path.join(LEVEL_DIR, "OvergrowthSystem.con")
SCRIPT_PATH = "/home/ator/BF2/scripts/process_lidar_canopy.py"


class TestMilestone2Deliverables(unittest.TestCase):
    def test_script_exists_and_executable(self):
        self.assertTrue(os.path.isfile(SCRIPT_PATH), f"Missing script: {SCRIPT_PATH}")
        self.assertTrue(os.access(SCRIPT_PATH, os.X_OK), f"Script not executable: {SCRIPT_PATH}")

    def test_ndmp_tiles_count_and_integrity(self):
        self.assertTrue(os.path.isdir(NDMP_DIR), f"Missing ndmp directory: {NDMP_DIR}")
        tiles = [f for f in os.listdir(NDMP_DIR) if f.startswith("nDMP_") and f.endswith(".tif")]
        self.assertEqual(len(tiles), 25, f"Expected 25 GeoTIFF tiles, found {len(tiles)}")

        for t in tiles:
            p = os.path.join(NDMP_DIR, t)
            sz = os.path.getsize(p)
            self.assertGreaterEqual(sz, 1_000_000, f"Tile {t} too small: {sz} bytes")
            ds = gdal.Open(p, gdal.GA_ReadOnly)
            self.assertIsNotNone(ds, f"Failed to open {t}")
            self.assertEqual(ds.RasterXSize, 2000, f"Unexpected width in {t}")
            self.assertEqual(ds.RasterYSize, 2000, f"Unexpected height in {t}")
            band = ds.GetRasterBand(1)
            self.assertIsNotNone(band, f"Missing band 1 in {t}")
            if "466_101" in t:
                # Float32 annex tile
                self.assertEqual(gdal.GetDataTypeName(band.DataType), "Float32")
                self.assertEqual(band.GetNoDataValue(), 0.0)
            else:
                # Int16 standard tile
                self.assertEqual(gdal.GetDataTypeName(band.DataType), "Int16")
                self.assertEqual(band.GetNoDataValue(), -32767.0)

    def test_overgrowth_raw_size_and_dimensions(self):
        self.assertTrue(os.path.isfile(RAW_PATH), f"Missing {RAW_PATH}")
        sz = os.path.getsize(RAW_PATH)
        self.assertEqual(sz, 4198401, f"Expected 4198401 bytes, got {sz}")

        arr = np.fromfile(RAW_PATH, dtype=np.uint8)
        self.assertEqual(arr.size, 2049 * 2049)
        grid = arr.reshape((2049, 2049))
        self.assertEqual(grid.shape, (2049, 2049))
        self.assertGreaterEqual(int(grid.min()), 0)
        self.assertLessEqual(int(grid.max()), 255)
        self.assertGreater(int(grid.max()), 0)

        # Golovec Pass ridge check
        sub = grid[1650:1750, 974:1074]
        mean_ridge = float(np.mean(sub))
        self.assertGreater(mean_ridge, 50.0, f"Expected dense canopy on Golovec ridge, got {mean_ridge}")

    def test_overgrowthsystem_con_syntax_and_species(self):
        self.assertTrue(os.path.isfile(CON_PATH), f"Missing {CON_PATH}")
        sz = os.path.getsize(CON_PATH)
        self.assertGreater(sz, 50)

        with open(CON_PATH, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().lower().startswith("rem")]

        valid_prefixes = ("Overgrowth.", "OvergrowthType.")
        for idx, line in enumerate(lines, 1):
            cmd = line.split()[0]
            self.assertTrue(cmd.startswith(valid_prefixes), f"Invalid prefix at line {idx}: {cmd}")

        materials = [l.split()[1] for l in lines if l.split()[0] == "Overgrowth.addMaterial"]
        types = [l.split()[1] for l in lines if l.split()[0] == "Overgrowth.addType"]
        geos = [l.split()[1] for l in lines if l.split()[0] == "OvergrowthType.geometry"]

        self.assertEqual(materials, ["temperate_forest"])
        self.assertEqual(len(types), 7)
        self.assertIn("fir", types)
        self.assertIn("birch_1", types)

        vanilla_whitelist = {
            "fir_mixed02", "birch_green_1", "birch_green_2", "pine_dead",
            "me_olive03", "largebush", "pine_large", "oak_01"
        }
        for geo in geos:
            self.assertIn(geo, vanilla_whitelist)
        self.assertNotIn("me_olive03", geos)


if __name__ == "__main__":
    unittest.main()
