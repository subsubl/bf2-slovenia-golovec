#!/usr/bin/env python3
"""
Unit and integration test for tile_downloader.py
"""

import os
import shutil
import tempfile
from tile_downloader import (
    check_disk_space,
    validate_geotiff,
    parse_retry_after,
    download_tile
)

def test_disk_space():
    ok, free_mb = check_disk_space("/home/ator/BF2/.agents/teamwork/explorer_m2_1", required_mb=100.0)
    assert ok, f"Expected >100MB free, got {free_mb}"
    print(f"PASS: check_disk_space ({free_mb:.1f} MB available)")

def test_parse_retry_after():
    assert parse_retry_after({'Retry-After': '5'}, 2.0) == 5.0
    assert parse_retry_after({'X-Retry-In': '1.5s'}, 2.0) == 1.5
    assert parse_retry_after({'X-Retry-In': '500ms'}, 2.0) == 0.5
    assert parse_retry_after({}, 2.0) == 2.0
    print("PASS: test_parse_retry_after")

def test_validation_logic():
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(b"not a geotiff")
        tmp.flush()
        valid, msg = validate_geotiff(tmp.name)
        assert not valid, f"Expected invalid, got {valid}"
    print(f"PASS: test_validation_logic (rejected fake file: {msg})")

def test_download_and_cache_cycle():
    test_dir = "/home/ator/BF2/.agents/teamwork/explorer_m2_1/test_cache"
    os.makedirs(test_dir, exist_ok=True)
    test_file = os.path.join(test_dir, "nDMP_469_100.tif")
    url = "https://assets.flycom.si/clss/raw/05-ljubljana/zls/ndmp/nDMP_469_100.tif"

    try:
        # Step 1: Initial download
        success, status, b = download_tile(url, test_file)
        assert success and status == "downloaded" and b > 9_000_000, f"Download failed: {status}"
        print(f"PASS: Step 1 Initial download ({b:,} bytes)")

        # Step 2: Idempotent cache hit
        success, status, b = download_tile(url, test_file)
        assert success and status == "cached" and b == 0, f"Expected cache hit, got {status}"
        print("PASS: Step 2 Idempotent cache hit (0 bytes transferred)")

        # Step 3: Corrupt file recovery
        with open(test_file, "wb") as f:
            f.write(b"corrupted partial data")
        
        valid, reason = validate_geotiff(test_file)
        assert not valid, "Expected corrupted file to fail validation"
        print(f"PASS: Step 3 Corruption detected correctly: {reason}")

        # Step 4: Re-download on corruption
        success, status, b = download_tile(url, test_file)
        assert success and status == "downloaded" and b > 9_000_000, f"Recovery download failed: {status}"
        valid, _ = validate_geotiff(test_file)
        assert valid, "Restored file must be valid GeoTIFF"
        print("PASS: Step 4 Re-download on corruption restored valid GeoTIFF")

    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print("PASS: Cleaned up test cache directory")

if __name__ == "__main__":
    test_disk_space()
    test_parse_retry_after()
    test_validation_logic()
    test_download_and_cache_cycle()
    print("\nALL UNIT & INTEGRATION TESTS PASSED!")
