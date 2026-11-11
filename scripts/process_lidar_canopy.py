#!/usr/bin/env python3
"""
scripts/process_lidar_canopy.py

Complete LiDAR Canopy Acquisition and Overgrowth Mask Generation Pipeline:
1. Downloads 25 nDMP GeoTIFFs referenced in tiles_manifest.json with rate-limiting
   (1.25s inter-request delay) and exponential backoff into ndmp/.
2. Mosaics tiles via direct window placement into an (8192, 8192) float32 canvas
   (268 MB RAM), correctly handling Float32 / NoData 0.0 (tile 466_101) vs Int16.
3. Resamples 0.5m LiDAR grid to (2049, 2049) 2.0m terrain grid via PIL Bilinear.
4. Flips vertically (np.flipud) to align with Refractor 2 raw terrain convention
   (Row 0 = South, Row 2048 = North).
5. Applies canopy height thresholding and linear density classification
   (H < 1.5m -> 0; 1.5m <= H <= 20.0m -> round((H - 1.5)/18.5 * 255); H > 20.0m -> 255).
6. Writes exactly 4,198,401 bytes uint8 to levels/slovenia_golovec/Overgrowth/Overgrowth.raw.

Usage:
    python3 scripts/process_lidar_canopy.py [options]

Options:
    --manifest PATH       Path to tiles_manifest.json (default: /home/ator/BF2/tiles_manifest.json)
    --ndmp-dir PATH       Path to nDMP GeoTIFF storage (default: /home/ator/BF2/ndmp)
    --output PATH         Path to Overgrowth.raw (default: /home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw)
    --delay FLOAT         Inter-request throttle delay in seconds (default: 1.25)
    --h-min FLOAT         Minimum canopy height in meters (default: 1.5)
    --h-max FLOAT         Maximum canopy saturation height in meters (default: 20.0)
    --skip-download       Skip acquisition phase and process existing local tiles
"""

import os
import sys
import json
import time
import shutil
import random
import argparse
import urllib.request
import urllib.error
from typing import Dict, Tuple, Optional, Any
import numpy as np
from PIL import Image
from osgeo import gdal

# Silence GDAL warnings / exceptions
gdal.UseExceptions()
gdal.PushErrorHandler("CPLQuietErrorHandler")


# ---------------------------------------------------------------------------
# Part 1: Rate-Limited Sequential Downloader with Retry & Backoff
# ---------------------------------------------------------------------------

def check_disk_space(target_dir: str, required_mb: float = 300.0) -> Tuple[bool, float]:
    """Verify target filesystem has sufficient free space."""
    os.makedirs(target_dir, exist_ok=True)
    _, _, free = shutil.disk_usage(target_dir)
    free_mb = free / (1024 * 1024)
    return (free_mb >= required_mb, free_mb)


def validate_geotiff(filepath: str) -> Tuple[bool, str]:
    """Validate file existence, minimum size, and GDAL raster integrity."""
    if not os.path.isfile(filepath):
        return False, "File does not exist"

    size = os.path.getsize(filepath)
    if size < 1_000_000:  # nDMP tiles are ~10 MB or ~20 MB
        return False, f"File size too small ({size} bytes)"

    try:
        ds = gdal.Open(filepath, gdal.GA_ReadOnly)
        if ds is None:
            return False, "GDAL failed to open dataset"

        cols, rows, bands = ds.RasterXSize, ds.RasterYSize, ds.RasterCount
        if cols != 2000 or rows != 2000 or bands < 1:
            return False, f"Unexpected dimensions: {cols}x{rows}, bands={bands}"

        band = ds.GetRasterBand(1)
        if band is None:
            return False, "Raster band 1 missing"

        ds = None
        return True, "Valid GeoTIFF"
    except Exception as e:
        return False, f"GDAL validation error: {e}"


def parse_retry_after(headers: Any, default_backoff: float) -> float:
    """Extract wait time from HTTP response headers (Retry-After or X-Retry-In)."""
    retry_after = headers.get("Retry-After")
    if retry_after:
        try:
            return float(retry_after)
        except ValueError:
            pass

    x_retry = headers.get("X-Retry-In")
    if x_retry:
        try:
            val_str = x_retry.strip().lower()
            if val_str.endswith("ms"):
                return float(val_str[:-2]) / 1000.0
            elif val_str.endswith("s"):
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
    Download a single GeoTIFF tile with idempotence, validation, atomic temp files,
    and adaptive exponential backoff for HTTP 429 and transient errors.
    """
    is_valid, _ = validate_geotiff(dest_path)
    if is_valid:
        return True, "cached", 0

    dest_dir = os.path.dirname(os.path.abspath(dest_path))
    os.makedirs(dest_dir, exist_ok=True)
    tmp_path = dest_path + f".tmp.{os.getpid()}"

    backoff = initial_backoff
    headers = {"User-Agent": "BF2-Level-Builder/1.0"}

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

            # Validate downloaded file before replacing destination
            is_valid_download, val_msg = validate_geotiff(tmp_path)
            if not is_valid_download:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                raise ValueError(f"Downloaded file validation failed: {val_msg}")

            # Atomic rename into destination path
            os.replace(tmp_path, dest_path)
            return True, "downloaded", bytes_written

        except urllib.error.HTTPError as e:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

            if e.code == 429:
                wait_time = parse_retry_after(e.headers, backoff) + random.uniform(0.2, 0.6)
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
    required_free_mb: float = 300.0,
    verbose: bool = True
) -> Dict[str, Any]:
    """Acquire all 25 nDMP GeoTIFFs referenced in tiles_manifest.json."""
    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    ok, free_mb = check_disk_space(cache_dir, required_mb=required_free_mb)
    if not ok:
        raise OSError(f"Insufficient disk space in {cache_dir}: {free_mb:.1f} MB available, {required_free_mb:.1f} MB required")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    total_tiles = len(manifest)
    if verbose:
        print(f"Checking {total_tiles} nDMP GeoTIFF tiles in {cache_dir}...")
        print(f"Free disk space: {free_mb:.1f} MB (Threshold: {required_free_mb:.1f} MB)")

    results: Dict[str, Any] = {
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
            results["failed"] += 1
            results["tiles"][tile_key] = {"status": "failed", "error": "missing ndmp_url"}
            continue

        filename = f"nDMP_{tile_key}.tif"
        dest_path = os.path.join(cache_dir, filename)

        # Fast cache check
        is_valid, _ = validate_geotiff(dest_path)
        if is_valid:
            file_size = os.path.getsize(dest_path)
            if verbose:
                print(f"[{idx:02d}/{total_tiles}] Tile {tile_key}: CACHED ({file_size / (1024*1024):.2f} MB)")
            results["cached"] += 1
            results["total_bytes"] += file_size
            results["tiles"][tile_key] = {"status": "cached", "path": dest_path, "bytes": file_size}
            continue

        # Download needed
        if verbose:
            print(f"[{idx:02d}/{total_tiles}] Downloading {tile_key} from {url}...")
        t_dl_start = time.time()
        success, msg, dl_bytes = download_tile(url, dest_path)
        dl_duration = time.time() - t_dl_start

        if success:
            speed = (dl_bytes / (1024 * 1024)) / dl_duration if dl_duration > 0 else 0
            if verbose:
                print(f"[{idx:02d}/{total_tiles}] Tile {tile_key}: OK ({dl_bytes / (1024*1024):.2f} MB in {dl_duration:.2f}s, {speed:.2f} MB/s)")
            results["downloaded"] += 1
            results["total_bytes"] += dl_bytes
            results["tiles"][tile_key] = {"status": "downloaded", "path": dest_path, "bytes": dl_bytes}

            # Rate-limiting delay between downloads
            if idx < total_tiles:
                time.sleep(inter_request_delay)
        else:
            if verbose:
                print(f"[{idx:02d}/{total_tiles}] Tile {tile_key}: FAILED - {msg}")
            results["failed"] += 1
            results["tiles"][tile_key] = {"status": "failed", "error": msg}

    total_time = time.time() - t_start
    if verbose:
        print(f"Tile Acquisition Complete: {results['downloaded']} downloaded, {results['cached']} cached, {results['failed']} failed ({total_time:.2f}s)")

    if results["failed"] > 0:
        raise RuntimeError(f"Failed to acquire {results['failed']} tiles")

    return results


# ---------------------------------------------------------------------------
# Part 2: Mosaicking, Cropping, Resampling & Density Mask Serialization
# ---------------------------------------------------------------------------

def build_overgrowth_mask(
    manifest_path: str = "/home/ator/BF2/tiles_manifest.json",
    ndmp_dir: str = "/home/ator/BF2/ndmp",
    output_raw_path: str = "/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw",
    h_min: float = 1.5,
    h_max: float = 20.0,
    verbose: bool = True
) -> str:
    """
    Mosaics 25 nDMP GeoTIFFs directly into an (8192, 8192) float32 cropped canvas,
    resamples to 2049x2049 terrain grid via PIL Bilinear, flips vertically
    for Refractor 2 raw terrain layout (Row 0 South to Row 2048 North),
    classifies foliage density, and writes 4,198,401 bytes uint8 binary mask.
    """
    if verbose:
        print("=" * 70)
        print("BF2 OVERGROWTH DENSITY MASK GENERATOR")
        print(f"Manifest:       {manifest_path}")
        print(f"Tile Directory: {ndmp_dir}")
        print(f"Output Raw:     {output_raw_path}")
        print("=" * 70)

    # Coordinate boundaries
    # Mosaic: Easting [466000, 471000], Northing [97000, 102000] (5000m x 5000m)
    # Level:  Easting [466450, 470546], Northing [97418, 101514] (4096m x 4096m)
    cols = [466, 467, 468, 469, 470]
    rows = [101, 100, 99, 98, 97]  # North to South

    # Pixel offsets in 0.5m LiDAR grid
    x_crop_start = int((466450 - 466000) / 0.5)  # 900
    x_crop_end = x_crop_start + int(4096 / 0.5)   # 9092
    y_crop_start = int((102000 - 101514) / 0.5)  # 972
    y_crop_end = y_crop_start + int(4096 / 0.5)   # 9164

    crop_width = x_crop_end - x_crop_start        # 8192
    crop_height = y_crop_end - y_crop_start       # 8192

    if verbose:
        canvas_mb = (crop_height * crop_width * 4) / (1024 * 1024)
        print(f"Allocating cropped canvas: ({crop_height}, {crop_width}) float32 ({canvas_mb:.1f} MB)...")

    cropped = np.zeros((crop_height, crop_width), dtype=np.float32)

    tiles_placed = 0
    missing_tiles = 0

    for r_idx, r in enumerate(rows):
        tile_r_start = r_idx * 2000
        tile_r_end = tile_r_start + 2000

        for c_idx, c in enumerate(cols):
            tile_c_start = c_idx * 2000
            tile_c_end = tile_c_start + 2000

            # Compute intersection of current tile with level crop window
            inter_r_min = max(tile_r_start, y_crop_start)
            inter_r_max = min(tile_r_end, y_crop_end)
            inter_c_min = max(tile_c_start, x_crop_start)
            inter_c_max = min(tile_c_end, x_crop_end)

            if inter_r_min >= inter_r_max or inter_c_min >= inter_c_max:
                continue

            candidates = [
                os.path.join(ndmp_dir, f"nDMP_{c}_{r}.tif"),
                os.path.join(ndmp_dir, f"nDMP_{c}_{int(r):03d}.tif"),
                os.path.join(ndmp_dir, f"nDMP_{c}_{int(r)}.tif"),
            ]
            tile_path = next((p for p in candidates if os.path.exists(p)), None)

            if not tile_path:
                if verbose:
                    print(f"  [MISSING] Tile {c}_{r}: not found in {ndmp_dir}, leaving bare ground (0.0m).")
                missing_tiles += 1
                continue

            ds = gdal.Open(tile_path, gdal.GA_ReadOnly)
            if ds is None:
                if verbose:
                    print(f"  [ERROR] Tile {c}_{r}: failed to open with GDAL: {tile_path}")
                continue

            band = ds.GetRasterBand(1)
            data = band.ReadAsArray().astype(np.float32)
            nodata = band.GetNoDataValue()

            # Normalize NoData:
            # 24 tiles are Int16 with nodata = -32767.0
            # 1 annex tile (466_101) is Float32 with nodata = 0.0
            if nodata is not None and nodata < -100:
                data[data == nodata] = 0.0
            data[data < 0.0] = 0.0
            data[np.isnan(data)] = 0.0
            np.clip(data, 0.0, 50.0, out=data)

            # Map slice from tile to cropped canvas
            tile_slice_r = slice(inter_r_min - tile_r_start, inter_r_max - tile_r_start)
            tile_slice_c = slice(inter_c_min - tile_c_start, inter_c_max - tile_c_start)
            dst_slice_r = slice(inter_r_min - y_crop_start, inter_r_max - y_crop_start)
            dst_slice_c = slice(inter_c_min - x_crop_start, inter_c_max - x_crop_start)

            cropped[dst_slice_r, dst_slice_c] = data[tile_slice_r, tile_slice_c]
            tiles_placed += 1
            ds = None

    if verbose:
        print(f"Mosaicking complete: {tiles_placed} tiles placed, {missing_tiles} missing.")
        print(f"Canopy stats (0.5m grid): min={cropped.min():.2f}m, max={cropped.max():.2f}m, mean={cropped.mean():.2f}m")

    # Resample from 0.5m LiDAR grid (8192x8192) to 2.0m terrain grid (2049x2049)
    if verbose:
        print("Resampling 8192x8192 LiDAR canopy to 2049x2049 terrain grid (PIL Bilinear)...")
    img = Image.fromarray(cropped)
    resampled_h = np.array(img.resize((2049, 2049), resample=Image.Resampling.BILINEAR))
    del img
    del cropped

    # Vertical flip: align image coordinates (Row 0 North) with Refractor 2 raw convention (Row 0 South)
    raw_h = np.flipud(resampled_h)
    del resampled_h

    # Foliage density classification:
    # H < h_min -> 0
    # h_min <= H <= h_max -> round((H - h_min) / (h_max - h_min) * 255.0)
    # H > h_max -> 255
    if verbose:
        print(f"Classifying foliage density (H_min={h_min}m, H_max={h_max}m -> uint8 [0, 255])...")
    density_float = np.where(
        raw_h < h_min,
        0.0,
        np.clip((raw_h - h_min) / (h_max - h_min), 0.0, 1.0) * 255.0
    )
    density_uint8 = np.round(density_float).astype(np.uint8)
    del density_float
    del raw_h

    # Verify Golovec ridge area canopy density
    # Golovec Pass focal point (0, 1365) corresponds to col=1024, row=1707
    sub_grid = density_uint8[1650:1750, 974:1074]
    ridge_mean = float(np.mean(sub_grid))
    if verbose:
        print(f"Golovec Pass ridge test window [1650:1750, 974:1074]: mean density = {ridge_mean:.2f}")

    # Serialize to raw binary
    out_dir = os.path.dirname(os.path.abspath(output_raw_path))
    os.makedirs(out_dir, exist_ok=True)
    raw_bytes = density_uint8.tobytes()

    with open(output_raw_path, "wb") as f:
        f.write(raw_bytes)

    byte_count = os.path.getsize(output_raw_path)
    if verbose:
        print(f"Successfully generated {output_raw_path} ({byte_count:,} bytes)")

    if byte_count != 4198401:
        raise ValueError(f"Byte count mismatch: expected 4198401 bytes, got {byte_count}")

    return output_raw_path


def main() -> None:
    parser = argparse.ArgumentParser(description="LiDAR Canopy Processing & Overgrowth Mask Generator")
    parser.add_argument("--manifest", default="/home/ator/BF2/tiles_manifest.json",
                        help="Path to tiles_manifest.json")
    parser.add_argument("--ndmp-dir", default="/home/ator/BF2/ndmp",
                        help="Path to nDMP GeoTIFF directory")
    parser.add_argument("--output", default="/home/ator/BF2/levels/slovenia_golovec/Overgrowth/Overgrowth.raw",
                        help="Path to output Overgrowth.raw")
    parser.add_argument("--delay", type=float, default=1.25,
                        help="Inter-request delay in seconds for downloading (default: 1.25)")
    parser.add_argument("--h-min", type=float, default=1.5,
                        help="Minimum canopy height in meters (default: 1.5)")
    parser.add_argument("--h-max", type=float, default=20.0,
                        help="Canopy height for 100% saturation (default: 20.0)")
    parser.add_argument("--skip-download", action="store_true",
                        help="Skip tile downloading phase")
    args = parser.parse_args()

    # Step 1: Download tiles if not skipped
    if not args.skip_download:
        acquire_ndmp_tiles(
            manifest_path=args.manifest,
            cache_dir=args.ndmp_dir,
            inter_request_delay=args.delay
        )

    # Step 2: Build density mask
    build_overgrowth_mask(
        manifest_path=args.manifest,
        ndmp_dir=args.ndmp_dir,
        output_raw_path=args.output,
        h_min=args.h_min,
        h_max=args.h_max
    )


if __name__ == "__main__":
    main()
