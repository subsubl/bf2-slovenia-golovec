#!/usr/bin/env python3
"""
tests/adversarial_m1_2_spatial_check.py

Independent adversarial spatial clearance, geometry, and distribution
verification suite for levels/slovenia_golovec/StaticObjects.con.
"""

import os
import sys
import math
import json
from collections import Counter, defaultdict
import numpy as np

CON_FILE = "/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con"
HEIGHTMAP_FILE = "/home/ator/BF2/Heightmap.raw"
WATER_LEVEL = 270.0
MAP_BOUND_MIN = -2048.0
MAP_BOUND_MAX = 2048.0
MAP_SPAN = 4096.0

# Approximate bounding dimensions [length, width, height] for BF2 vanilla templates
# Based on BF2 engine mesh definitions (length along primary yaw axis, width along perpendicular)
TEMPLATE_DIMENSIONS = {
    'eu_building01': (20.0, 16.0, 14.0),
    'eu_building02': (24.0, 18.0, 16.0),
    'eu_office_01': (28.0, 20.0, 15.0),
    'me_apartment_01': (26.0, 16.0, 12.0),
    'citybuilding_01': (30.0, 22.0, 18.0),
    'eu_house_01': (12.0, 10.0, 8.0),
    'eu_house_02': (15.0, 12.0, 9.0),
    'me_house_01': (9.0, 9.0, 7.0),
    'me_house_02': (10.0, 10.0, 8.0),
    'me_house_03': (12.0, 9.0, 8.0),
    'me_house_04': (14.0, 11.0, 8.0),
    'me_house_05': (16.0, 12.0, 9.0),
    'me_house_06': (18.0, 14.0, 9.0),
    'barn_01': (22.0, 14.0, 10.0),
    'barn_02': (26.0, 16.0, 11.0),
    'farmhouse': (16.0, 12.0, 8.0),
    'wooden_shed': (6.0, 5.0, 4.0),
    'shed_01': (8.0, 6.0, 4.0),
    'warehouse_01': (36.0, 20.0, 12.0),
}


def parse_static_objects_con(filepath):
    """
    Independent parser for StaticObjects.con.
    Verifies structure and parses all instances into structured records.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Missing {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_valid = False
    footer_valid = False

    # Check header
    header_lines = [l.strip() for l in lines[:4] if l.strip()]
    if (len(header_lines) >= 3 and 
        header_lines[0].startswith("rem") and
        header_lines[1] == "if v_arg1 == BF2Editor" and
        header_lines[2] == "console.allowMultipleFileLoad 0" and
        lines[3].strip() == "endIf"):
        header_valid = True

    # Check footer
    footer_lines = [l.strip() for l in lines[-4:] if l.strip()]
    if ("if v_arg1 == BF2Editor" in footer_lines and
        "console.allowMultipleFileLoad 1" in footer_lines and
        "endIf" in footer_lines):
        footer_valid = True

    objects = []
    current_obj = {}
    formatting_errors = []

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("rem") or line.startswith("if") or line.startswith("endIf") or line.startswith("console."):
            continue

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            formatting_errors.append((idx, f"Invalid token count: '{line}'"))
            continue

        cmd, val = parts[0], parts[1]

        if cmd == "Object.create":
            if current_obj:
                formatting_errors.append((idx, f"Unfinalized object before new Object.create: {current_obj}"))
            current_obj = {"line_start": idx, "template": val}
        elif cmd == "Object.absolutePosition":
            if "template" not in current_obj:
                formatting_errors.append((idx, f"Object.absolutePosition without Object.create"))
                continue
            # Check for whitespace around slashes
            if " /" in val or "/ " in val or "  " in val:
                formatting_errors.append((idx, f"Whitespace in vector: '{val}'"))
            coords = val.split('/')
            if len(coords) != 3:
                formatting_errors.append((idx, f"Expected 3 components in position: '{val}'"))
                continue
            try:
                current_obj["x"] = float(coords[0])
                current_obj["y"] = float(coords[1])
                current_obj["z"] = float(coords[2])
                current_obj["raw_pos"] = val
            except ValueError as e:
                formatting_errors.append((idx, f"Non-numeric position '{val}': {e}"))
        elif cmd == "Object.rotation":
            if "template" not in current_obj:
                formatting_errors.append((idx, f"Object.rotation without Object.create"))
                continue
            if " /" in val or "/ " in val or "  " in val:
                formatting_errors.append((idx, f"Whitespace in rotation vector: '{val}'"))
            rots = val.split('/')
            if len(rots) != 3:
                formatting_errors.append((idx, f"Expected 3 components in rotation: '{val}'"))
                continue
            try:
                current_obj["yaw"] = float(rots[0])
                current_obj["pitch"] = float(rots[1])
                current_obj["roll"] = float(rots[2])
                current_obj["raw_rot"] = val
            except ValueError as e:
                formatting_errors.append((idx, f"Non-numeric rotation '{val}': {e}"))
        elif cmd == "Object.layer":
            if "template" not in current_obj:
                formatting_errors.append((idx, f"Object.layer without Object.create"))
                continue
            try:
                current_obj["layer"] = int(val)
            except ValueError:
                current_obj["layer"] = val
            objects.append(current_obj)
            current_obj = {}
        else:
            formatting_errors.append((idx, f"Unknown command '{cmd}'"))

    return objects, header_valid, footer_valid, formatting_errors


def sample_heightmap_bilinear(hmap, x, z):
    """Bilinear elevation lookup from Heightmap.raw."""
    u = np.clip((x + 2048.0) / 2.0, 0.0, 2048.0)
    v = np.clip((z + 2048.0) / 2.0, 0.0, 2048.0)
    c0, r0 = int(np.floor(u)), int(np.floor(v))
    c1, r1 = min(c0 + 1, 2048), min(r0 + 1, 2048)
    s, t = u - c0, v - r0
    h00 = hmap[r0, c0] * 0.01
    h10 = hmap[r0, c1] * 0.01
    h01 = hmap[r1, c0] * 0.01
    h11 = hmap[r1, c1] * 0.01
    return float((1.0 - s) * (1.0 - t) * h00 + s * (1.0 - t) * h10 +
                 (1.0 - s) * t * h01 + s * t * h11)


def check_obb_intersection(obj1, obj2):
    """
    Separating Axis Theorem (SAT) check for 2D Oriented Bounding Boxes of two buildings.
    Returns (intersects: bool, min_separation: float).
    """
    dim1 = TEMPLATE_DIMENSIONS.get(obj1['template'], (15.0, 12.0, 8.0))
    dim2 = TEMPLATE_DIMENSIONS.get(obj2['template'], (15.0, 12.0, 8.0))

    hw1, hl1 = dim1[1] * 0.5, dim1[0] * 0.5
    hw2, hl2 = dim2[1] * 0.5, dim2[0] * 0.5

    # Rotations (yaw in degrees, Refractor 2 yaw: 0 is +Z, 90 is +X)
    # Long axis is along yaw direction: heading vector = (sin(yaw), cos(yaw))
    # Perpendicular axis = (cos(yaw), -sin(yaw))
    rad1 = math.radians(obj1['yaw'])
    dir1 = np.array([math.sin(rad1), math.cos(rad1)])
    perp1 = np.array([math.cos(rad1), -math.sin(rad1)])

    rad2 = math.radians(obj2['yaw'])
    dir2 = np.array([math.sin(rad2), math.cos(rad2)])
    perp2 = np.array([math.cos(rad2), -math.sin(rad2)])

    c1 = np.array([obj1['x'], obj1['z']])
    c2 = np.array([obj2['x'], obj2['z']])

    # 4 potential separating axes
    axes = [dir1, perp1, dir2, perp2]

    # Center translation vector
    d = c2 - c1

    min_separation = float('inf')

    for axis in axes:
        # Normalize axis
        axis = axis / np.linalg.norm(axis)

        # Project half-extents of box 1
        proj1 = hl1 * abs(np.dot(dir1, axis)) + hw1 * abs(np.dot(perp1, axis))
        # Project half-extents of box 2
        proj2 = hl2 * abs(np.dot(dir2, axis)) + hw2 * abs(np.dot(perp2, axis))

        # Center distance projected on axis
        dist_proj = abs(np.dot(d, axis))

        separation = dist_proj - (proj1 + proj2)
        if separation > 0:
            # Separating axis found -> No intersection!
            return False, separation
        if separation > min_separation or min_separation == float('inf'):
            min_separation = separation

    # If no separating axis found, they intersect!
    return True, min_separation


def run_adversarial_suite():
    print("=" * 70)
    print("BF2 LEVEL ADVERSARIAL VERIFICATION: StaticObjects.con")
    print("=" * 70)

    # 1. Parse and syntax check
    objects, header_valid, footer_valid, formatting_errors = parse_static_objects_con(CON_FILE)
    print(f"[*] Parsed {len(objects)} static objects.")
    print(f"[*] Header valid: {header_valid}")
    print(f"[*] Footer valid: {footer_valid}")
    print(f"[*] Formatting errors count: {len(formatting_errors)}")
    if formatting_errors:
        for err in formatting_errors[:10]:
            print(f"    ERROR at line {err[0]}: {err[1]}")

    N = len(objects)
    assert N > 0, "No objects parsed!"

    # 2. Pairwise Euclidean Distances (Full O(N^2))
    print("\n" + "-" * 70)
    print(f"[*] Running Full O(N^2) Pairwise Distance Calculation on N={N} objects...")
    
    xs = np.array([obj['x'] for obj in objects], dtype=np.float64)
    ys = np.array([obj['y'] for obj in objects], dtype=np.float64)
    zs = np.array([obj['z'] for obj in objects], dtype=np.float64)

    # 2D coordinates (X, Z) and 3D coordinates (X, Y, Z)
    coords_2d = np.column_stack((xs, zs))
    coords_3d = np.column_stack((xs, ys, zs))

    # Pairwise differences
    # We can do full matrix computation with numpy
    diff_2d = coords_2d[:, np.newaxis, :] - coords_2d[np.newaxis, :, :]  # (N, N, 2)
    dist_2d_sq = np.sum(diff_2d ** 2, axis=-1)                           # (N, N)
    dist_2d = np.sqrt(dist_2d_sq)

    diff_3d = coords_3d[:, np.newaxis, :] - coords_3d[np.newaxis, :, :]  # (N, N, 3)
    dist_3d_sq = np.sum(diff_3d ** 2, axis=-1)                           # (N, N)
    dist_3d = np.sqrt(dist_3d_sq)

    # Mask self-distances (diagonal)
    np.fill_diagonal(dist_2d, np.inf)
    np.fill_diagonal(dist_3d, np.inf)

    min_dist_2d = np.min(dist_2d)
    min_dist_3d = np.min(dist_3d)

    # Find the indices of minimum distance
    min_idx_2d = np.unravel_index(np.argmin(dist_2d), dist_2d.shape)
    min_idx_3d = np.unravel_index(np.argmin(dist_3d), dist_3d.shape)

    obj_a = objects[min_idx_2d[0]]
    obj_b = objects[min_idx_2d[1]]

    print(f"[*] Absolute minimum 2D horizontal distance: {min_dist_2d:.4f} m")
    print(f"[*] Absolute minimum 3D Euclidean distance:   {min_dist_3d:.4f} m")
    print(f"[*] Closest pair: #{min_idx_2d[0]} ({obj_a['template']} at {obj_a['x']:.2f}, {obj_a['z']:.2f}) <-> "
          f"#{min_idx_2d[1]} ({obj_b['template']} at {obj_b['x']:.2f}, {obj_b['z']:.2f})")

    # Check for duplicate coordinates
    duplicate_pairs = []
    under_2m_pairs = []
    under_30m_pairs = []

    # Get upper triangle pairs
    i_indices, j_indices = np.triu_indices(N, k=1)
    pair_distances_2d = dist_2d[i_indices, j_indices]
    pair_distances_3d = dist_3d[i_indices, j_indices]

    for k in range(len(pair_distances_2d)):
        d2 = pair_distances_2d[k]
        d3 = pair_distances_3d[k]
        i = i_indices[k]
        j = j_indices[k]
        if d2 < 1e-4:
            duplicate_pairs.append((i, j, d2))
        if d2 < 2.0:
            under_2m_pairs.append((i, j, d2, d3))
        if d2 < 30.0:
            under_30m_pairs.append((i, j, d2, d3))

    print(f"[*] Duplicate coordinate pairs: {len(duplicate_pairs)}")
    print(f"[*] Pairs with 2D distance < 2.0 m: {len(under_2m_pairs)}")
    print(f"[*] Pairs with 2D distance < 30.0 m (R thinning threshold): {len(under_30m_pairs)}")

    # Sort and display closest 10 pairs
    sorted_pair_order = np.argsort(pair_distances_2d)[:10]
    print("\n[*] Top 10 Closest Pairs:")
    for rank, p_idx in enumerate(sorted_pair_order, 1):
        i = i_indices[p_idx]
        j = j_indices[p_idx]
        d2 = pair_distances_2d[p_idx]
        d3 = pair_distances_3d[p_idx]
        oa = objects[i]
        ob = objects[j]
        print(f"    {rank:2d}. Dist 2D={d2:6.3f}m, 3D={d3:6.3f}m | Obj {i:4d} ({oa['template']:15s}) <-> Obj {j:4d} ({ob['template']:15s})")

    # 3. Oriented Bounding Box (OBB) Mesh Collision Check
    print("\n" + "-" * 70)
    print("[*] Running 2D Oriented Bounding Box (OBB) Separating Axis Theorem (SAT) Collision Test...")
    # Check all pairs with distance < 60m (since max diagonal is ~41m)
    candidate_collision_pairs = np.where(pair_distances_2d < 60.0)[0]
    print(f"[*] Checking {len(candidate_collision_pairs)} building pairs within 60.0m for 3D/2D OBB intersection...")

    obb_intersections = []
    min_obb_clearance = float('inf')
    min_obb_pair = None

    for p_idx in candidate_collision_pairs:
        i = i_indices[p_idx]
        j = j_indices[p_idx]
        oa = objects[i]
        ob = objects[j]
        intersects, sep = check_obb_intersection(oa, ob)
        if intersects:
            obb_intersections.append((i, j, sep))
        else:
            if sep < min_obb_clearance:
                min_obb_clearance = sep
                min_obb_pair = (i, j, sep)

    print(f"[*] OBB Intersections found: {len(obb_intersections)}")
    if obb_intersections:
        for inter in obb_intersections[:5]:
            i, j, sep = inter
            print(f"    COLLISION: Obj #{i} ({objects[i]['template']}) and Obj #{j} ({objects[j]['template']}) overlap! Penetration: {-sep:.3f}m")
    else:
        i, j, sep = min_obb_pair
        print(f"[*] ZERO OBB Collisions! Minimum physical mesh clearance: {min_obb_clearance:.3f} m "
              f"(between #{i} {objects[i]['template']} and #{j} {objects[j]['template']})")

    # 4. Rotation Angles Verification
    print("\n" + "-" * 70)
    print("[*] Checking Rotation Angles (Pitch, Roll, Yaw)...")
    pitches = np.array([obj['pitch'] for obj in objects])
    rolls = np.array([obj['roll'] for obj in objects])
    yaws = np.array([obj['yaw'] for obj in objects])

    pitch_exact_zeros = np.all(pitches == 0.0)
    roll_exact_zeros = np.all(rolls == 0.0)
    non_zero_pitch = np.where(pitches != 0.0)[0]
    non_zero_roll = np.where(rolls != 0.0)[0]

    yaw_in_bounds = np.all((yaws >= -180.0) & (yaws <= 180.0))
    yaw_out_of_bounds = np.where((yaws < -180.0) | (yaws > 180.0))[0]

    print(f"[*] Pitch == 0.0: {pitch_exact_zeros} (non-zero count: {len(non_zero_pitch)})")
    print(f"[*] Roll == 0.0:  {roll_exact_zeros} (non-zero count: {len(non_zero_roll)})")
    print(f"[*] Yaw in [-180.0, 180.0]: {yaw_in_bounds} (out of bounds count: {len(yaw_out_of_bounds)})")
    print(f"[*] Yaw range: [{np.min(yaws):.3f}, {np.max(yaws):.3f}], mean: {np.mean(yaws):.3f}, std: {np.std(yaws):.3f}")

    # Check for NaN / Inf in positions and rotations
    any_nan_pos = np.any(np.isnan(coords_3d))
    any_inf_pos = np.any(np.isinf(coords_3d))
    any_nan_rot = np.any(np.isnan(np.column_stack((yaws, pitches, rolls))))
    print(f"[*] NaN in positions: {any_nan_pos}, Inf in positions: {any_inf_pos}, NaN in rotations: {any_nan_rot}")

    # Check formatting of raw strings
    improper_precision_count = 0
    for obj in objects:
        for val_str in obj['raw_pos'].split('/') + obj['raw_rot'].split('/'):
            parts = val_str.split('.')
            if len(parts) != 2 or len(parts[1]) != 3:
                improper_precision_count += 1
    print(f"[*] Values without exactly 3 decimal places: {improper_precision_count}")

    # 5. Ground Elevation & Water Table Submergence
    print("\n" + "-" * 70)
    print(f"[*] Loading heightmap from {HEIGHTMAP_FILE}...")
    hmap = np.fromfile(HEIGHTMAP_FILE, dtype='<u2').reshape((2049, 2049))
    print(f"[*] Heightmap range: min={hmap.min()*0.01:.2f}m, max={hmap.max()*0.01:.2f}m")

    submerged_buildings = []
    elev_deviations = []
    for idx, obj in enumerate(objects):
        x, y, z = obj['x'], obj['y'], obj['z']
        if y < WATER_LEVEL:
            submerged_buildings.append((idx, obj))
        sampled_y = sample_heightmap_bilinear(hmap, x, z)
        elev_deviations.append(abs(y - sampled_y))

    elev_deviations = np.array(elev_deviations)
    max_elev_dev = np.max(elev_deviations)
    mean_elev_dev = np.mean(elev_deviations)

    print(f"[*] Submerged buildings (Y < {WATER_LEVEL}m): {len(submerged_buildings)}")
    print(f"[*] Maximum elevation deviation from bilinear heightmap: {max_elev_dev:.6f} m")
    print(f"[*] Mean elevation deviation: {mean_elev_dev:.6f} m")
    print(f"[*] Minimum building elevation: {np.min(ys):.3f} m, Maximum: {np.max(ys):.3f} m")

    # 6. Spatial Distribution across Sectors
    print("\n" + "-" * 70)
    print("[*] Analyzing Spatial Distribution Across Map Sectors...")
    # Analyze 4x4 Grid (16 macro-sectors, 1024m x 1024m each)
    sector_size = 1024.0
    macro_sectors = defaultdict(list)
    grid_res = 4

    for obj in objects:
        # Map X, Z from [-2048, 2048] to [0, 4)
        col = int(math.floor((obj['x'] + 2048.0) / sector_size))
        row = int(math.floor((obj['z'] + 2048.0) / sector_size))
        col = min(max(col, 0), grid_res - 1)
        row = min(max(row, 0), grid_res - 1)
        macro_sectors[(row, col)].append(obj)

    # Compute terrain dry-land proportion for each macro sector
    # Heightmap is 2049x2049, each sector corresponds to ~512x512 pixels
    sector_stats = []
    print("\n[*] 4x4 Macro-Sectors (1024m x 1024m):")
    print(f"{'Sector':<10} | {'X Bounds (m)':<18} | {'Z Bounds (m)':<18} | {'Dry Land %':<12} | {'Buildings':<10} | {'Status'}")
    print("-" * 85)

    for row in range(grid_res - 1, -1, -1):  # North to South
        for col in range(grid_res):           # West to East
            x_min = -2048.0 + col * sector_size
            x_max = x_min + sector_size
            z_min = -2048.0 + row * sector_size
            z_max = z_min + sector_size

            # Heightmap pixel slice
            r_start = int(row * (2048 / grid_res))
            r_end = int((row + 1) * (2048 / grid_res)) + 1
            c_start = int(col * (2048 / grid_res))
            c_end = int((col + 1) * (2048 / grid_res)) + 1

            h_slice = hmap[r_start:r_end, c_start:c_end] * 0.01
            dry_pixels = np.sum(h_slice >= WATER_LEVEL)
            total_pixels = h_slice.size
            dry_pct = (dry_pixels / total_pixels) * 100.0

            b_count = len(macro_sectors[(row, col)])

            status = "HEALTHY"
            if dry_pct < 1.0 and b_count == 0:
                status = "FULLY_SUBMERGED (Expected 0)"
            elif b_count == 0:
                status = "STARVED (Defect!)"
            elif b_count < 10:
                status = "SPARSE"

            sector_name = f"R{row}C{col}"
            print(f"{sector_name:<10} | [{x_min:6.0f}, {x_max:6.0f}] | [{z_min:6.0f}, {z_max:6.0f}] | {dry_pct:10.1f}% | {b_count:10d} | {status}")
            sector_stats.append({
                "sector": sector_name,
                "row": row, "col": col,
                "x_min": x_min, "x_max": x_max,
                "z_min": z_min, "z_max": z_max,
                "dry_pct": dry_pct,
                "building_count": b_count,
                "status": status
            })

    # Named Geographic Sectors Verification
    print("\n[*] Checking Key Named Geographic Sectors:")
    named_regions = {
        "Golovec Focal Point & Pass": {
            "x_range": (-600.0, 600.0), "z_range": (800.0, 1800.0), "min_elev": 270.0
        },
        "Golovec Ridge & Forest Uplands": {
            "x_range": (-1800.0, 600.0), "z_range": (-1200.0, 1200.0), "min_elev": 270.0
        },
        "Golovec High Ridge (Y >= 300m)": {
            "x_range": (-2048.0, 2048.0), "z_range": (-2048.0, 2048.0), "min_elev": 300.0
        },
        "Bizovik Sector": {
            "x_range": (-2000.0, 1400.0), "z_range": (200.0, 1800.0), "min_elev": 270.0
        },
        "Sostro (East / NE Valley)": {
            "x_range": (500.0, 2040.0), "z_range": (-300.0, 1500.0), "min_elev": 270.0
        },
        "Ljubljana / Poljane Urban Edge (NW)": {
            "x_range": (-2040.0, -200.0), "z_range": (800.0, 2040.0), "min_elev": 270.0
        },
        "Rudnik / Barje Fringe (SW)": {
            "x_range": (-2040.0, -400.0), "z_range": (-2040.0, -400.0), "min_elev": 270.0
        },
        "Lavrica / Orle Countryside (SE)": {
            "x_range": (200.0, 2040.0), "z_range": (-2040.0, 200.0), "min_elev": 270.0
        },
    }

    named_results = {}
    for r_name, r_bounds in named_regions.items():
        xr = r_bounds["x_range"]
        zr = r_bounds["z_range"]
        me = r_bounds["min_elev"]

        matching = [
            obj for obj in objects
            if xr[0] <= obj['x'] <= xr[1] and zr[0] <= obj['z'] <= zr[1] and obj['y'] >= me
        ]
        named_results[r_name] = len(matching)
        print(f"    - {r_name:40s}: {len(matching):4d} buildings")

    # 7. Mesh Catalog Distribution
    print("\n" + "-" * 70)
    print("[*] Checking Static Mesh Catalog Distribution...")
    mesh_counts = Counter(obj['template'] for obj in objects)
    for mesh, cnt in mesh_counts.most_common():
        pct = (cnt / N) * 100.0
        print(f"    - {mesh:20s}: {cnt:4d} ({pct:5.1f}%)")

    # 8. Boundary Margins
    print("\n" + "-" * 70)
    print("[*] Checking Map Boundary Margins (X, Z in [-2048, 2048])...")
    min_x, max_x = np.min(xs), np.max(xs)
    min_z, max_z = np.min(zs), np.max(zs)
    print(f"[*] X limits: [{min_x:.3f}, {max_x:.3f}] (margin West: {min_x - MAP_BOUND_MIN:.3f}m, margin East: {MAP_BOUND_MAX - max_x:.3f}m)")
    print(f"[*] Z limits: [{min_z:.3f}, {max_z:.3f}] (margin South: {min_z - MAP_BOUND_MIN:.3f}m, margin North: {MAP_BOUND_MAX - max_z:.3f}m)")
    out_of_bounds = [obj for obj in objects if not (MAP_BOUND_MIN <= obj['x'] <= MAP_BOUND_MAX and MAP_BOUND_MIN <= obj['z'] <= MAP_BOUND_MAX)]
    print(f"[*] Buildings out of bounds: {len(out_of_bounds)}")

    # 9. Summary Verdict
    print("\n" + "=" * 70)
    print("VERDICT EVALUATION:")
    
    pass_clearance = (min_dist_2d >= 2.0 and len(under_2m_pairs) == 0 and len(obb_intersections) == 0)
    pass_thinning = (min_dist_2d >= 30.0 and len(under_30m_pairs) == 0)
    pass_rotation = (pitch_exact_zeros and roll_exact_zeros and yaw_in_bounds)
    pass_sectors = all(res > 0 for res in named_results.values()) and not any(s['status'] == "STARVED (Defect!)" for s in sector_stats)
    pass_submergence = (len(submerged_buildings) == 0)
    pass_syntax = (header_valid and footer_valid and len(formatting_errors) == 0)

    print(f"1. Minimum Pairwise Distance >= 2.0m:   {'PASS' if pass_clearance else 'FAIL'} (min={min_dist_2d:.4f}m)")
    print(f"2. R=30.0m Spatial Thinning Compliance:  {'PASS' if pass_thinning else 'FAIL'} (min={min_dist_2d:.4f}m)")
    print(f"3. Rotation Angles (Pitch=0, Roll=0):    {'PASS' if pass_rotation else 'FAIL'}")
    print(f"4. Spatial Coverage Across Dry Sectors:  {'PASS' if pass_sectors else 'FAIL'}")
    print(f"5. Zero Submerged Buildings (Y >= 270):  {'PASS' if pass_submergence else 'FAIL'}")
    print(f"6. Refractor 2 Syntax and Formatting:    {'PASS' if pass_syntax else 'FAIL'}")

    overall_verdict = "CONFIRM" if (pass_clearance and pass_thinning and pass_rotation and pass_sectors and pass_submergence and pass_syntax) else "REJECT"
    print(f"\nFINAL VERDICT: {overall_verdict}")
    print("=" * 70)

    # Output detailed report JSON for verification artifact
    results_summary = {
        "verdict": overall_verdict,
        "total_buildings": N,
        "min_dist_2d": float(min_dist_2d),
        "min_dist_3d": float(min_dist_3d),
        "duplicate_pairs": len(duplicate_pairs),
        "pairs_under_2m": len(under_2m_pairs),
        "pairs_under_30m": len(under_30m_pairs),
        "obb_intersections": len(obb_intersections),
        "min_obb_clearance": float(min_obb_clearance),
        "pitch_exact_zero": bool(pitch_exact_zeros),
        "roll_exact_zero": bool(roll_exact_zeros),
        "yaw_in_bounds": bool(yaw_in_bounds),
        "yaw_min": float(np.min(yaws)),
        "yaw_max": float(np.max(yaws)),
        "submerged_buildings": len(submerged_buildings),
        "max_elevation_deviation": float(max_elev_dev),
        "named_regions": named_results,
        "unique_templates": len(mesh_counts),
        "top_mesh": mesh_counts.most_common(1)[0],
        "bounds": {
            "x_min": float(min_x), "x_max": float(max_x),
            "z_min": float(min_z), "z_max": float(max_z),
            "y_min": float(np.min(ys)), "y_max": float(np.max(ys))
        }
    }
    with open("/home/ator/BF2/tests/adversarial_spatial_results.json", "w") as f:
        json.dump(results_summary, f, indent=2)
    print("[*] Saved detailed test results to /home/ator/BF2/tests/adversarial_spatial_results.json")

    return overall_verdict == "CONFIRM"


if __name__ == "__main__":
    success = run_adversarial_suite()
    sys.exit(0 if success else 1)
