#!/usr/bin/env python3
"""
scripts/extract_osm_buildings.py

Extracts OpenStreetMap building footprints for the 4096m x 4096m Slovenia
(Golovec / SE Ljubljana) Battlefield 2 map, samples ground elevation from
Heightmap.raw, classifies footprints to BF2 vanilla static meshes, applies
spatial thinning, and generates levels/slovenia_golovec/StaticObjects.con.

Usage:
    python3 scripts/extract_osm_buildings.py [options]

Options:
    --heightmap PATH    Path to Heightmap.raw (default: /home/ator/BF2/Heightmap.raw)
    --output PATH       Path to StaticObjects.con (default: /home/ator/BF2/levels/slovenia_golovec/StaticObjects.con)
    --cache-dir PATH    Path to OSM XML cache (default: /home/ator/BF2/.osm_cache)
    --min-area FLOAT    Minimum footprint area in m2 (default: 35.0)
    --water-level FLOAT Water surface elevation in meters (default: 270.0)
    --radius FLOAT      Spatial thinning clearance radius in meters (default: 30.0)
"""

import os
import sys
import math
import time
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pyproj

# ---------------------------------------------------------------------------
# Constants & Coordinate References
# ---------------------------------------------------------------------------
# D96TM / Slovenia 1996 national grid origin corresponding to BF2 Cartesian (0, 0, 0)
ORIGIN_E = 468498.0
ORIGIN_N = 99466.0

# 4096m x 4096m Cartesian Bounds
BOUND_MIN = -2048.0
BOUND_MAX = 2048.0

# WGS84 Extents for the 4 Quadrants covering Golovec 4096m x 4096m
# Midpoint: Lon 14.593029 E, Lat 46.034271 N
QUADRANTS = {
    'SW': (14.566437, 46.015750, 14.593029, 46.034271),
    'SE': (14.593029, 46.015750, 14.619621, 46.034271),
    'NW': (14.566437, 46.034271, 14.593029, 46.052791),
    'NE': (14.593029, 46.034271, 14.619621, 46.052791),
}

# Coordinate Transformer: WGS84 (EPSG:4326) to D96TM (EPSG:3794)
TO_D96 = pyproj.Transformer.from_crs('EPSG:4326', 'EPSG:3794', always_xy=True)


def wgs_to_cartesian(lat: float, lon: float) -> Tuple[float, float]:
    """Convert WGS84 (Lat, Lon) to BF2 Cartesian (X, Z)."""
    e, n = TO_D96.transform(lon, lat)
    return float(e - ORIGIN_E), float(n - ORIGIN_N)


# ---------------------------------------------------------------------------
# Heightmap Sampler
# ---------------------------------------------------------------------------
class HeightmapSampler:
    """Loads 2049x2049 uint16 little-endian heightmap and samples ground elevation."""

    def __init__(self, raw_path: str):
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Heightmap not found at: {raw_path}")
        size = os.path.getsize(raw_path)
        expected = 2049 * 2049 * 2
        if size != expected:
            raise ValueError(f"Heightmap size mismatch: expected {expected} bytes, got {size}")
        self.data = np.fromfile(raw_path, dtype='<u2').reshape((2049, 2049))

    def sample_bilinear(self, x: float, z: float) -> float:
        """Bilinear elevation sampling for Cartesian (X, Z) with 0.0m foundation offset."""
        u = np.clip((x + 2048.0) / 2.0, 0.0, 2048.0)
        v = np.clip((z + 2048.0) / 2.0, 0.0, 2048.0)
        c0, r0 = int(np.floor(u)), int(np.floor(v))
        c1, r1 = min(c0 + 1, 2048), min(r0 + 1, 2048)
        s, t = u - c0, v - r0
        h00 = self.data[r0, c0] * 0.01
        h10 = self.data[r0, c1] * 0.01
        h01 = self.data[r1, c0] * 0.01
        h11 = self.data[r1, c1] * 0.01
        return float((1.0 - s) * (1.0 - t) * h00 + s * (1.0 - t) * h10 +
                     (1.0 - s) * t * h01 + s * t * h11)


# ---------------------------------------------------------------------------
# Geometry Mathematics
# ---------------------------------------------------------------------------
def stitch_ways(way_node_lists: List[List[str]]) -> List[List[str]]:
    """Stitches unclosed or closed way segments into closed coordinate rings."""
    closed_rings: List[List[str]] = []
    open_segments: List[List[str]] = []

    for w in way_node_lists:
        if len(w) >= 4 and w[0] == w[-1]:
            closed_rings.append(w)
        elif len(w) >= 2:
            open_segments.append(list(w))

    while open_segments:
        current_ring = open_segments.pop(0)
        extended = True
        while extended and current_ring[0] != current_ring[-1]:
            extended = False
            for i, seg in enumerate(open_segments):
                if seg[0] == current_ring[-1]:
                    current_ring.extend(seg[1:])
                    open_segments.pop(i)
                    extended = True
                    break
                elif seg[-1] == current_ring[-1]:
                    current_ring.extend(list(reversed(seg))[1:])
                    open_segments.pop(i)
                    extended = True
                    break
                elif seg[-1] == current_ring[0]:
                    current_ring = seg[:-1] + current_ring
                    open_segments.pop(i)
                    extended = True
                    break
                elif seg[0] == current_ring[0]:
                    current_ring = list(reversed(seg))[:-1] + current_ring
                    open_segments.pop(i)
                    extended = True
                    break

        if current_ring[0] == current_ring[-1]:
            closed_rings.append(current_ring)
        else:
            # Uncloseable segment discarded
            break

    return closed_rings


def compute_polygon_metrics(pts: List[Tuple[float, float]]) -> Tuple[float, float, float, float]:
    """
    Computes Centroid (Cx, Cz), Area (m2), and Longest-Edge Yaw (deg)
    using Green's Theorem and Refractor 2 vector heading.
    """
    n = len(pts) - 1
    c_terms = [pts[i][0] * pts[i + 1][1] - pts[i + 1][0] * pts[i][1] for i in range(n)]
    a_signed = 0.5 * sum(c_terms)
    area = abs(a_signed)

    if area < 1e-6:
        cx = sum(p[0] for p in pts[:-1]) / n
        cz = sum(p[1] for p in pts[:-1]) / n
    else:
        # Green's Theorem centroid (invariant to winding direction)
        cx = (1.0 / (6.0 * a_signed)) * sum((pts[i][0] + pts[i + 1][0]) * c_terms[i] for i in range(n))
        cz = (1.0 / (6.0 * a_signed)) * sum((pts[i][1] + pts[i + 1][1]) * c_terms[i] for i in range(n))

    # Longest edge yaw derivation
    max_len_sq = -1.0
    best_dx = 0.0
    best_dz = 0.0
    for i in range(n):
        dx = pts[i + 1][0] - pts[i][0]
        dz = pts[i + 1][1] - pts[i][1]
        lsq = dx * dx + dz * dz
        if lsq > max_len_sq:
            max_len_sq = lsq
            best_dx = dx
            best_dz = dz

    if max_len_sq <= 1e-6:
        yaw = 0.0
    else:
        yaw = math.degrees(math.atan2(best_dx, best_dz))
        yaw = ((yaw + 180.0) % 360.0) - 180.0

    return cx, cz, area, yaw


# ---------------------------------------------------------------------------
# Static Mesh Classifier (Vanilla BF2 European Urban/Rural Models)
# ---------------------------------------------------------------------------
def classify_osm_building(tag_val: str, levels_val: str, area: float) -> str:
    """
    Deterministic classification mapping OSM building tags, levels, and footprint area
    to standard Battlefield 2 vanilla European static mesh templates.
    """
    b = str(tag_val).lower().strip() if tag_val else 'yes'
    try:
        levels = float(str(levels_val).replace(',', '.')) if levels_val else 1.0
    except (ValueError, TypeError):
        levels = 1.0

    # 1. Civic, Office, Public Administration & Institutional
    if b in ['office', 'public', 'civic', 'government', 'school', 'hospital', 'university', 'kindergarten']:
        if area >= 500.0 or levels >= 3.0:
            return 'citybuilding_01'
        return 'eu_office_01'

    # 2. Commercial, Retail & Shopping
    if b in ['commercial', 'retail', 'supermarket', 'mall']:
        if area >= 500.0:
            return 'eu_office_01'
        elif area >= 250.0:
            return 'eu_building01'
        return 'eu_building02'

    # 3. High-Density Residential Apartments & Dormitories
    if b in ['apartments', 'dormitory', 'residential_apartments']:
        if levels >= 3.0 or area >= 500.0:
            return 'citybuilding_01'
        elif area >= 250.0:
            return 'me_apartment_01'
        return 'eu_building02'

    # 4. Industrial, Logistics & Manufacturing
    if b in ['industrial', 'warehouse', 'manufacture', 'factory', 'storage_tank', 'depot']:
        if area >= 300.0:
            return 'warehouse_01'
        return 'barn_02'

    # 5. Rural, Agricultural & Farmsteads
    if b in ['barn', 'farm', 'farm_auxiliary', 'stable', 'cowshed', 'hayrack', 'silo']:
        if area >= 300.0:
            return 'barn_02'
        elif area >= 140.0:
            return 'barn_01'
        return 'farmhouse'

    # 6. Secondary Outbuildings, Garages & Sheds
    if b in ['shed', 'garage', 'garages', 'carport', 'hut', 'cabin', 'allotment_house', 'greenhouse', 'service', 'kiosk']:
        if area < 35.0:
            return 'wooden_shed'
        return 'shed_01'

    # 7. Religious / Landmark
    if b in ['church', 'chapel', 'cathedral']:
        return 'citybuilding_01'

    # 8. Generic / Residential (building=yes, house, detached, semi_detached, terrace, residential)
    if levels >= 3.0:
        if area >= 400.0:
            return 'citybuilding_01'
        return 'me_apartment_01'

    # Area-based fallback cascade
    if area >= 600.0:
        return 'eu_building02'
    elif area >= 350.0:
        return 'eu_building01'
    elif area >= 220.0:
        return 'me_house_06'
    elif area >= 160.0:
        return 'eu_house_02'
    elif area >= 110.0:
        return 'me_house_04'
    elif area >= 75.0:
        return 'eu_house_01'
    elif area >= 40.0:
        return 'me_house_01'
    else:
        return 'wooden_shed'


# ---------------------------------------------------------------------------
# OSM Downloader & Parser
# ---------------------------------------------------------------------------
def fetch_quadrant_xml(name: str, bbox: Tuple[float, float, float, float], cache_dir: str) -> str:
    """Fetches OSM XML for a quadrant or loads from local cache."""
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"osm_{name}.xml")

    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 1000:
        print(f"Loaded cached OSM data for quadrant {name} ({os.path.getsize(cache_file):,} bytes).")
        return cache_file

    min_lon, min_lat, max_lon, max_lat = bbox
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={min_lon:.6f},{min_lat:.6f},{max_lon:.6f},{max_lat:.6f}"
    headers = {'User-Agent': 'BF2SloveniaLevelMapExtractor/1.0'}
    req = urllib.request.Request(url, headers=headers)

    print(f"Downloading quadrant {name} from {url}...")
    with urllib.request.urlopen(req, timeout=45) as resp:
        content = resp.read()
        with open(cache_file, 'wb') as f:
            f.write(content)

    print(f"Successfully downloaded quadrant {name} ({len(content):,} bytes).")
    # Polite throttling delay between quadrant requests to prevent HTTP 429
    time.sleep(1.5)
    return cache_file


def parse_osm_data(cache_dir: str):
    """Loads all 4 quadrants, deduplicates elements, and returns nodes, ways, relations."""
    all_nodes: Dict[str, Tuple[float, float]] = {}
    all_ways: Dict[str, Tuple[Dict[str, str], List[str]]] = {}
    all_relations: Dict[str, Tuple[Dict[str, str], List[Tuple[str, str, str]]]] = {}

    for name, bbox in QUADRANTS.items():
        xml_path = fetch_quadrant_xml(name, bbox, cache_dir)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for n in root.findall('node'):
            all_nodes[n.get('id')] = (float(n.get('lat')), float(n.get('lon')))

        for w in root.findall('way'):
            tags = {t.get('k'): t.get('v') for t in w.findall('tag')}
            nds = [nd.get('ref') for nd in w.findall('nd')]
            all_ways[w.get('id')] = (tags, nds)

        for r in root.findall('relation'):
            tags = {t.get('k'): t.get('v') for t in r.findall('tag')}
            members = [(m.get('type'), m.get('ref'), m.get('role')) for m in r.findall('member')]
            all_relations[r.get('id')] = (tags, members)

    print(f"Parsed OSM elements: {len(all_nodes):,} nodes, {len(all_ways):,} ways, {len(all_relations):,} relations.")
    return all_nodes, all_ways, all_relations


# ---------------------------------------------------------------------------
# Extraction Pipeline
# ---------------------------------------------------------------------------
def extract_buildings(
    raw_heightmap_path: str,
    cache_dir: str,
    min_area: float = 35.0,
    water_level: float = 270.0,
    max_slope_delta: float = 2.5
) -> List[Dict[str, Any]]:
    """Extracts, validates, grounds, and filters raw building candidates."""
    sampler = HeightmapSampler(raw_heightmap_path)
    nodes, ways, relations = parse_osm_data(cache_dir)

    raw_candidates = []
    consumed_ways = set()

    # 1. Process Multipolygon Relations
    for rid, (tags, members) in relations.items():
        if tags.get('type') == 'multipolygon' and 'building' in tags and tags['building'] != 'no':
            outer_way_ids = [mref for mtype, mref, mrole in members if mtype == 'way' and mrole == 'outer']
            consumed_ways.update(outer_way_ids)
            way_node_lists = [ways[wid][1] for wid in outer_way_ids if wid in ways]
            rings = stitch_ways(way_node_lists)

            for ring in rings:
                pts = [wgs_to_cartesian(*nodes[nid]) for nid in ring if nid in nodes]
                if len(pts) != len(ring) or len(pts) < 4:
                    continue

                # Check all polygon vertices strictly inside world bounds
                if not all(BOUND_MIN <= px <= BOUND_MAX and BOUND_MIN <= pz <= BOUND_MAX for px, pz in pts):
                    continue

                cx, cz, area, yaw = compute_polygon_metrics(pts)
                if area < min_area:
                    continue
                if not (BOUND_MIN <= cx <= BOUND_MAX and BOUND_MIN <= cz <= BOUND_MAX):
                    continue

                cy = sampler.sample_bilinear(cx, cz)
                if cy < water_level or cy > 455.0:
                    continue

                # Multi-corner elevation and slope check
                corner_elevs = [sampler.sample_bilinear(px, pz) for px, pz in pts[:-1]]
                if min(corner_elevs) < water_level:
                    continue
                if (max(corner_elevs) - min(corner_elevs)) > max_slope_delta:
                    continue

                template = classify_osm_building(tags.get('building'), tags.get('building:levels'), area)
                raw_candidates.append({
                    'id': f"rel_{rid}",
                    'template': template,
                    'x': cx,
                    'y': cy,
                    'z': cz,
                    'yaw': yaw,
                    'area': area,
                    'building_tag': tags.get('building', 'yes'),
                    'levels_tag': tags.get('building:levels', '1')
                })

    # 2. Process Standalone Building Ways
    for wid, (tags, nds) in ways.items():
        if wid in consumed_ways or 'building' not in tags or tags['building'] == 'no':
            continue
        if len(nds) < 4 or nds[0] != nds[-1]:
            continue

        pts = [wgs_to_cartesian(*nodes[nid]) for nid in nds if nid in nodes]
        if len(pts) != len(nds):
            continue

        # Check all polygon vertices strictly inside world bounds
        if not all(BOUND_MIN <= px <= BOUND_MAX and BOUND_MIN <= pz <= BOUND_MAX for px, pz in pts):
            continue

        cx, cz, area, yaw = compute_polygon_metrics(pts)
        if area < min_area:
            continue
        if not (BOUND_MIN <= cx <= BOUND_MAX and BOUND_MIN <= cz <= BOUND_MAX):
            continue

        cy = sampler.sample_bilinear(cx, cz)
        if cy < water_level or cy > 455.0:
            continue

        # Multi-corner elevation and slope check
        corner_elevs = [sampler.sample_bilinear(px, pz) for px, pz in pts[:-1]]
        if min(corner_elevs) < water_level:
            continue
        if (max(corner_elevs) - min(corner_elevs)) > max_slope_delta:
            continue

        template = classify_osm_building(tags.get('building'), tags.get('building:levels'), area)
        raw_candidates.append({
            'id': f"way_{wid}",
            'template': template,
            'x': cx,
            'y': cy,
            'z': cz,
            'yaw': yaw,
            'area': area,
            'building_tag': tags.get('building', 'yes'),
            'levels_tag': tags.get('building:levels', '1')
        })

    print(f"Total valid, grounded raw building candidates: {len(raw_candidates)}")
    return raw_candidates


# ---------------------------------------------------------------------------
# Spatial Thinning (Greedy Priority Non-Maximum Suppression)
# ---------------------------------------------------------------------------
def apply_spatial_thinning(candidates: List[Dict[str, Any]], radius: float = 30.0) -> List[Dict[str, Any]]:
    """
    Applies priority-based greedy Non-Maximum Suppression with radius R.
    Prioritizes designated POIs, high-density residential blocks, and large buildings.
    """
    poi_tags = {
        'office', 'school', 'hospital', 'apartments', 'commercial', 'industrial',
        'warehouse', 'church', 'barn', 'public', 'civic', 'government', 'university'
    }

    # Priority score: POI bonus (1000.0) + footprint area
    def priority_score(b: Dict[str, Any]) -> float:
        bonus = 1000.0 if b['building_tag'].lower() in poi_tags else 0.0
        return bonus + b['area']

    sorted_candidates = sorted(candidates, key=priority_score, reverse=True)

    grid: Dict[Tuple[int, int], List[Tuple[float, float]]] = {}
    selected: List[Dict[str, Any]] = []
    r_sq = radius * radius

    for b in sorted_candidates:
        bx, bz = b['x'], b['z']
        gx = int(math.floor(bx / radius))
        gz = int(math.floor(bz / radius))

        conflict = False
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                neighbor = (gx + dx, gz + dz)
                if neighbor in grid:
                    for ox, oz in grid[neighbor]:
                        dist_sq = (bx - ox) ** 2 + (bz - oz) ** 2
                        if dist_sq < r_sq:
                            conflict = True
                            break
                if conflict:
                    break
            if conflict:
                break

        if not conflict:
            selected.append(b)
            grid.setdefault((gx, gz), []).append((bx, bz))

    print(f"Spatial thinning (R={radius:.1f}m): selected {len(selected)} buildings from {len(candidates)} candidates.")
    return selected


# ---------------------------------------------------------------------------
# StaticObjects.con Serializer
# ---------------------------------------------------------------------------
def write_static_objects_con(buildings: List[Dict[str, Any]], output_path: str):
    """
    Writes valid Refractor 2 StaticObjects.con file with strict syntax formatting:
    - Balanced console editor conditional blocks
    - Slash-delimited vectors with NO spaces (X/Y/Z, Yaw/0.000/0.000)
    - 3-decimal float precision
    - Layer 1 assignment
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("rem *** Generated by BF2Editor ***\n")
        f.write("if v_arg1 == BF2Editor\n")
        f.write("console.allowMultipleFileLoad 0\n")
        f.write("endIf\n\n")

        for b in buildings:
            x, y, z = b['x'], b['y'], b['z']
            yaw = b['yaw']
            pos_str = f"{x:.3f}/{y:.3f}/{z:.3f}"
            rot_str = f"{yaw:.3f}/0.000/0.000"

            f.write(f"Object.create {b['template']}\n")
            f.write(f"Object.absolutePosition {pos_str}\n")
            f.write(f"Object.rotation {rot_str}\n")
            f.write("Object.layer 1\n\n")

        f.write("if v_arg1 == BF2Editor\n")
        f.write("console.allowMultipleFileLoad 1\n")
        f.write("endIf\n")

    print(f"Successfully generated {output_path} with {len(buildings)} static objects.")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Extract OSM buildings to BF2 StaticObjects.con")
    parser.add_argument("--heightmap", default="/home/ator/BF2/Heightmap.raw", help="Path to Heightmap.raw")
    parser.add_argument("--output", default="/home/ator/BF2/levels/slovenia_golovec/StaticObjects.con", help="Output con path")
    parser.add_argument("--cache-dir", default="/home/ator/BF2/.osm_cache", help="Directory for OSM XML cache")
    parser.add_argument("--min-area", type=float, default=35.0, help="Minimum footprint area in m2")
    parser.add_argument("--water-level", type=float, default=270.0, help="Minimum ground elevation in meters")
    parser.add_argument("--radius", type=float, default=30.0, help="Spatial thinning clearance radius in meters")

    args = parser.parse_args()

    print("=" * 70)
    print("BF2 OSM Building Extraction Pipeline - Milestone 1")
    print(f"Heightmap:   {args.heightmap}")
    print(f"Output:      {args.output}")
    print(f"Cache Dir:   {args.cache_dir}")
    print(f"Min Area:    {args.min_area} m²")
    print(f"Water Level: {args.water_level} m")
    print(f"Thin Radius: {args.radius} m")
    print("=" * 70)

    # 1. Extract raw valid candidates
    raw_candidates = extract_buildings(
        raw_heightmap_path=args.heightmap,
        cache_dir=args.cache_dir,
        min_area=args.min_area,
        water_level=args.water_level
    )

    # 2. Apply spatial thinning for performance and collision budget
    selected_buildings = apply_spatial_thinning(raw_candidates, radius=args.radius)

    # Verify budget constraint
    if len(selected_buildings) < 500 or len(selected_buildings) > 1500:
        print(f"WARNING: Building count {len(selected_buildings)} is outside [500, 1500] budget!")
    else:
        print(f"SUCCESS: Building count {len(selected_buildings)} meets AAA performance budget [500, 1500].")

    # 3. Generate StaticObjects.con
    write_static_objects_con(selected_buildings, args.output)


if __name__ == "__main__":
    main()
