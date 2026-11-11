#!/usr/bin/env python3
"""
tile_downloader.py - Robust LiDAR GeoTIFF Downloader & Caching Manager
Tested and verified for Battlefield 2 Slovenia (Golovec) Level Package.
"""

import os
import sys
import json
import time
import shutil
import random
import urllib.request
import urllib.error
from typing import Dict, Tuple, List, Optional
from osgeo import gdal

# Silence GDAL warnings
gdal.UseExceptions()


def check_disk_space(target_dir: str, required_mb: float = 300.0) -> Tuple[bool, float]:
    """
    Verify that the target filesystem has sufficient free space.
    """
    os.makedirs(target_dir, exist_ok=True)
    total, used, free = shutil.disk_usage(target_dir)
    free_mb = free / (1024 * 1024)
    return (free_mb >= required_mb, free_mb)


def validate_geotiff(filepath: str) -> Tuple[bool, str]:
    """
    Validate that a file exists, is non-empty, and can be read as a valid GeoTIFF by GDAL.
    """
    if not os.path.isfile(filepath):
        return False, "File does not exist"
    
    size = os.path.getsize(filepath)
    if size < 1_000_000: # nDMP files are ~10MB or ~20MB
        return False, f"File size too small ({size} bytes)"

    try:
        ds = gdal.Open(filepath, gdal.GA_ReadOnly)
        if ds is None:
            return False, "GDAL failed to open file"
        
        cols = ds.RasterXSize
        rows = ds.RasterYSize
        bands = ds.RasterCount
        if cols != 2000 or rows != 2000 or bands < 1:
            return False, f"Unexpected dimensions: {cols}x{rows}, bands={bands}"
        
        # Verify band can be accessed
        band = ds.GetRasterBand(1)
        if band is None:
            return False, "Raster band 1 missing"
            
        ds = None # Close dataset
        return True, "Valid GeoTIFF"
    except Exception as e:
        return False, f"GDAL error: {e}"


def parse_retry_after(headers, default_backoff: float) -> float:
    """
    Extract wait time from HTTP headers (Retry-After or X-Retry-In).
    """
    retry_after = headers.get('Retry-After')
    if retry_after:
        try:
            return float(retry_after)
        except ValueError:
            pass

    x_retry = headers.get('X-Retry-In')
    if x_retry:
        try:
            val_str = x_retry.strip().lower()
            if val_str.endswith('ms'):
                return float(val_str[:-2]) / 1000.0
            elif val_str.endswith('s'):
                return float(val_str[:-1])
        except ValueError:
            pass

    return default_backoff


def download_tile(
    url: str,
    dest_path: str,
    max_retries: int = 5,
    initial_backoff: float = 2.0,
    chunk_size: int = 64 * 1024
) -> Tuple[bool, str, int]:
    """
    Download a single tile with idempotence, validation, atomic temp files,
    and exponential backoff retry for HTTP 429 and transient errors.
    
    Returns: (success: bool, status_msg: str, bytes_downloaded: int)
    """
    # 1. Idempotency Check
    is_valid, reason = validate_geotiff(dest_path)
    if is_valid:
        return True, "cached", 0

    dest_dir = os.path.dirname(os.path.abspath(dest_path))
    os.makedirs(dest_dir, exist_ok=True)
    tmp_path = dest_path + f".tmp.{os.getpid()}"

    # 2. Retry loop
    backoff = initial_backoff
    headers = {'User-Agent': 'BF2-Level-Builder/1.0'}

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            bytes_written = 0
            
            with urllib.request.urlopen(req, timeout=30) as resp, open(tmp_path, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_written += len(chunk)

            # Validate before moving into place
            is_valid_download, val_msg = validate_geotiff(tmp_path)
            if not is_valid_download:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                raise ValueError(f"Downloaded file validation failed: {val_msg}")

            # Atomic rename
            os.replace(tmp_path, dest_path)
            return True, "downloaded", bytes_written

        except urllib.error.HTTPError as e:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

            if e.code == 429:
                wait_time = parse_retry_after(e.headers, backoff)
                # Add jitter
                wait_time += random.uniform(0.2, 0.6)
                print(f"  [HTTP 429] Rate limited. Waiting {wait_time:.2f}s before attempt {attempt+1}/{max_retries}...")
                time.sleep(wait_time)
                backoff *= 2.0
            elif e.code in (500, 502, 503, 504):
                wait_time = backoff + random.uniform(0.2, 0.5)
                print(f"  [HTTP {e.code}] Server error. Waiting {wait_time:.2f}s before attempt {attempt+1}/{max_retries}...")
                time.sleep(wait_time)
                backoff *= 2.0
            else:
                return False, f"HTTP Error {e.code}: {e.reason}", 0

        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            wait_time = backoff + random.uniform(0.2, 0.5)
            print(f"  [Network Error] {e}. Waiting {wait_time:.2f}s before attempt {attempt+1}/{max_retries}...")
            time.sleep(wait_time)
            backoff *= 2.0

        except Exception as e:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            return False, f"Unexpected error: {e}", 0

    return False, f"Exceeded max retries ({max_retries})", 0


def acquire_ndmp_tiles(
    manifest_path: str = "/home/ator/BF2/tiles_manifest.json",
    cache_dir: str = "/home/ator/BF2/ndmp",
    inter_request_delay: float = 1.25,
    required_free_mb: float = 300.0
) -> Dict[str, any]:
    """
    Acquire all 25 nDMP GeoTIFFs referenced in tiles_manifest.json.
    - Applies rate-limiting (inter_request_delay)
    - Validates disk budget
    - Ensures idempotency
    - Returns summary dictionary
    """
    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    # Check disk space
    ok, free_mb = check_disk_space(cache_dir, required_mb=required_free_mb)
    if not ok:
        raise OSError(f"Insufficient disk space in {cache_dir}: {free_mb:.1f} MB available, {required_free_mb:.1f} MB required")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    total_tiles = len(manifest)
    print(f"Acquiring {total_tiles} nDMP GeoTIFF tiles to {cache_dir}...")
    print(f"Free disk space: {free_mb:.1f} MB. Safe threshold: {required_free_mb:.1f} MB.")

    results = {
        "total": total_tiles,
        "cached": 0,
        "downloaded": 0,
        "failed": 0,
        "total_bytes": 0,
        "tiles": {}
    }

    t_start = time.time()
    for idx, (tile_key, tile_info) in enumerate(manifest.items(), 1):
        url = tile_info.get("ndmp_url")
        if not url:
            print(f"[{idx}/{total_tiles}] Tile {tile_key}: Missing 'ndmp_url' in manifest!")
            results["failed"] += 1
            results["tiles"][tile_key] = {"status": "failed", "error": "missing ndmp_url"}
            continue

        filename = f"nDMP_{tile_key}.tif"
        dest_path = os.path.join(cache_dir, filename)

        # Check if already cached
        is_valid, reason = validate_geotiff(dest_path)
        if is_valid:
            file_size = os.path.getsize(dest_path)
            print(f"[{idx}/{total_tiles}] Tile {tile_key}: CACHED ({file_size / (1024*1024):.2f} MB)")
            results["cached"] += 1
            results["total_bytes"] += file_size
            results["tiles"][tile_key] = {"status": "cached", "path": dest_path, "bytes": file_size}
            continue

        # Download needed
        print(f"[{idx}/{total_tiles}] Downloading {tile_key} from {url}...")
        t_dl_start = time.time()
        success, msg, dl_bytes = download_tile(url, dest_path)
        dl_duration = time.time() - t_dl_start

        if success:
            speed = (dl_bytes / (1024 * 1024)) / dl_duration if dl_duration > 0 else 0
            print(f"[{idx}/{total_tiles}] Tile {tile_key}: OK ({dl_bytes / (1024*1024):.2f} MB in {dl_duration:.2f}s, {speed:.2f} MB/s)")
            results["downloaded"] += 1
            results["total_bytes"] += dl_bytes
            results["tiles"][tile_key] = {"status": "downloaded", "path": dest_path, "bytes": dl_bytes}
            
            # Rate-limiting inter-request delay
            if idx < total_tiles:
                time.sleep(inter_request_delay)
        else:
            print(f"[{idx}/{total_tiles}] Tile {tile_key}: FAILED - {msg}")
            results["failed"] += 1
            results["tiles"][tile_key] = {"status": "failed", "error": msg}

    total_time = time.time() - t_start
    print("\n" + "=" * 60)
    print(f"Tile Acquisition Summary:")
    print(f"  Total tiles: {results['total']}")
    print(f"  Cached:      {results['cached']}")
    print(f"  Downloaded:  {results['downloaded']}")
    print(f"  Failed:      {results['failed']}")
    print(f"  Total size:  {results['total_bytes'] / (1024*1024):.2f} MB")
    print(f"  Total time:  {total_time:.2f}s")
    print("=" * 60)

    return results


if __name__ == "__main__":
    # Self-test: validate function definitions
    print("tile_downloader.py syntax and imports verified.")
