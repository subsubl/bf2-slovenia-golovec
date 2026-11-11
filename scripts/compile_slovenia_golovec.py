#!/usr/bin/env python3
"""
Compile authentic Slovenia Golovec LiDAR DEM, GURS nDMP Canopy & Building Heights,
RABA-KGZ Landuse & OSM Road Detailmaps, Project Reality Water-Depth Lightmaps,
5 Ljubljanica River Bridges, Curated OSM Infrastructure, 3-Zone Forest Overgrowth,
Shoreline Undergrowth, 3D Spatial Soundscape, and 6-CP Gameplay Layout
for Battlefield 2 (Refractor 2 Engine).
"""
import glob
import io
import math
import os
import re
import shutil
import struct
import time
import xml.etree.ElementTree as ET
import zipfile
import numpy as np
import pyproj
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt, gaussian_filter1d

WORKSPACE_DIR = "/home/ator/BF2"
LEVEL_DIR = "/media/ator/Tera/Bf2/Battlefield 2/mods/bf2/Levels/slovenia_golovec"
RAW_DIR = os.path.join(LEVEL_DIR, "_raw_files")
DV_DIR = "/media/ator/Tera/Bf2/Battlefield 2/mods/bf2/Levels/Dragon_Valley"
SEA_WATER_LEVEL = 269.50

# Five authentic Ljubljanica river bridge crossings from OSM & LiDAR:
# (name, bridge_type, cx, cz, yaw_deg, y_road, half_span_m)
LJUBLJANICA_BRIDGES = [
    ("A1_Motorway_Bridge", "highway_low", -674.5, 771.5, 169.8, 275.50, 28.25),
    ("Fuzine_Castle_Bridge", "stone", -26.0, 788.4, 116.0, 272.50, 9.827),
    ("Vevce_Bridge", "woodsteel_3", 41.3, 795.5, 6.8, 273.60, 15.00),
    ("Zadvor_Vevce_South_Bridge", "stone", 269.0, 464.0, 12.0, 272.30, 9.827),
    ("Kaselj_Zalog_Bridge", "woodsteel_3", 677.6, 882.5, 152.7, 274.20, 15.00),
]

# Six real-world Control Points spanning Golovec Ridge, Litijska Valley, and Ljubljanica Crossings:
# (cp_id, cp_name, team, radius, cx, cz)
CONTROL_POINTS = [
    (1, "CP_EU_BASE", 1, 20, -100.0, -400.0),
    (2, "CP_GOLOVEC_PASS", 0, 25, 0.0, 0.0),
    (3, "CP_STEPANJSKO_A1", 0, 22, -620.0, 680.0),
    (4, "CP_GRAD_FUZINE", 0, 22, -26.0, 735.0),
    (5, "CP_ZADVOR_SOUTH_BEND", 0, 22, 150.0, 420.0),
    (6, "CP_MEC_BASE", 2, 20, 80.0, 860.0),
]


def extract_osm_and_raba_layers():
    """
    Parses cached OSM XML + Slovenian Ministry of Agriculture (RABA-KGZ) polygons
    in a single pass and returns:
      - river_mask (2049x2049 bool, South-up)
      - road_mask_2048 (2048x2048 uint8, South-up: 2=paved road, 1=track/path/rail)
      - meadow_mask_2048 (2048x2048 bool, South-up: RABA farmland/meadow/orchard)
      - infra_props: list of (template_name, wx, wz, yaw_deg)
    """
    origin_e = 468498.0
    origin_n = 99466.0
    to_d96 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3794", always_xy=True)

    nodes = {}
    ways = {}
    relations = []
    power_towers = {}
    power_poles = {}
    street_lamps = {}
    fuel_stations = {}

    for path in sorted(glob.glob(os.path.join(WORKSPACE_DIR, ".osm_cache", "osm_*.xml"))):
        tree = ET.parse(path)
        root = tree.getroot()
        for nd in root.findall("node"):
            nid = nd.attrib["id"]
            if nid in nodes:
                continue
            lat = float(nd.attrib["lat"])
            lon = float(nd.attrib["lon"])
            e, n = to_d96.transform(lon, lat)
            gx = (e - origin_e + 2048.0) / 4096.0 * 2048.0
            gz = (n - origin_n + 2048.0) / 4096.0 * 2048.0
            wx = (e - origin_e) * 0.5
            wz = (n - origin_n) * 0.5
            nodes[nid] = (gx, gz, wx, wz)

            tags = {t.attrib["k"]: t.attrib["v"] for t in nd.findall("tag")}
            if tags and abs(wx) <= 985.0 and abs(wz) <= 985.0:
                if tags.get("power") == "tower":
                    power_towers[nid] = (wx, wz)
                elif tags.get("power") == "pole":
                    power_poles[nid] = (wx, wz)
                elif tags.get("highway") == "street_lamp":
                    street_lamps[nid] = (wx, wz)
                elif tags.get("amenity") == "fuel":
                    fuel_stations[nid] = (wx, wz)

        for way in root.findall("way"):
            wid = way.attrib["id"]
            if wid in ways:
                continue
            tags = {t.attrib["k"]: t.attrib["v"] for t in way.findall("tag")}
            nds = [nd.attrib["ref"] for nd in way.findall("nd") if nd.attrib["ref"] in nodes]
            if nds:
                ways[wid] = (tags, nds, [(nodes[r][0], nodes[r][1]) for r in nds])

        for rel in root.findall("relation"):
            tags = {t.attrib["k"]: t.attrib["v"] for t in rel.findall("tag")}
            members = [
                (m.attrib["type"], m.attrib["ref"], m.attrib.get("role", ""))
                for m in rel.findall("member")
            ]
            relations.append((tags, members))

    # 1. Reconstruct Ljubljanica river mask (2049x2049)
    rel_members = next(m for t, m in relations if t.get("water") == "river")
    outer_ways = [
        (ref, ways[ref][1], ways[ref][2])
        for t, ref, role in rel_members
        if ref in ways and role == "outer"
    ]
    inner_ways = [
        (ref, ways[ref][1], ways[ref][2])
        for t, ref, role in rel_members
        if ref in ways and role == "inner"
    ]

    segs = [list(pts) for _, _, pts in outer_ways]
    chain = segs.pop(0)
    while segs:
        best_i, best_rev, best_d = 0, False, 1e18
        for i, s in enumerate(segs):
            d0 = (s[0][0] - chain[-1][0]) ** 2 + (s[0][1] - chain[-1][1]) ** 2
            d1 = (s[-1][0] - chain[-1][0]) ** 2 + (s[-1][1] - chain[-1][1]) ** 2
            if d0 < best_d:
                best_i, best_rev, best_d = i, False, d0
            if d1 < best_d:
                best_i, best_rev, best_d = i, True, d1
        s = segs.pop(best_i)
        if best_rev:
            s = list(reversed(s))
        chain.extend(s[1:] if best_d < 1.0 else s)

    river_img = Image.new("L", (2049, 2049), 0)
    r_draw = ImageDraw.Draw(river_img)
    r_draw.polygon(chain, fill=1)
    for _, _, ipts in inner_ways:
        if len(ipts) >= 3:
            r_draw.polygon(ipts, fill=0)
    if "538835423" in ways:
        r_draw.line(ways["538835423"][2], fill=1, width=6)
    river_mask = np.array(river_img, dtype=bool)

    # 2. Rasterize RABA-KGZ Farmland/Meadow/Orchard polygons & OSM Roads onto 2048x2048 South-up grids
    meadow_img = Image.new("L", (2048, 2048), 0)
    m_draw = ImageDraw.Draw(meadow_img)
    road_img = Image.new("L", (2048, 2048), 0)
    rd_draw = ImageDraw.Draw(road_img)

    fence_ways = []
    motorway_ways = []

    for wid, (tags, nds, pts) in ways.items():
        lu = tags.get("landuse", "")
        raba = tags.get("raba:id", "")
        if (
            lu in ("farmland", "meadow", "grass", "orchard", "pasture")
            or raba in ("1100", "1300", "1222", "1221")
        ) and len(pts) >= 3:
            m_draw.polygon(pts, fill=1)

        hw = tags.get("highway", "")
        rw = tags.get("railway", "")
        if hw in ("motorway", "motorway_link", "primary", "secondary", "tertiary"):
            rd_draw.line(pts, fill=2, width=7 if "motorway" in hw else 5)
            if hw in ("motorway", "secondary"):
                motorway_ways.append((hw, pts))
        elif hw in ("residential", "unclassified", "service", "living_street"):
            rd_draw.line(pts, fill=2, width=3)
        elif hw in ("track", "path", "footway", "cycleway") or rw == "rail":
            rd_draw.line(pts, fill=1, width=2)

        if tags.get("barrier") in ("fence", "wall") and len(pts) >= 2:
            fence_ways.append((tags.get("barrier"), pts))

    meadow_mask_2048 = np.array(meadow_img, dtype=bool)
    road_mask_2048 = np.array(road_img, dtype=np.uint8)

    # 3. Build Curated OSM Infrastructure & Landmark Props (~180 props for old-hardware FPS)
    infra_props = []
    placed_xy = []

    def can_place_prop(x: float, z: float, min_dist: float) -> bool:
        if abs(x) > 980.0 or abs(z) > 980.0:
            return False
        for px, pz in placed_xy:
            if (x - px) ** 2 + (z - pz) ** 2 < min_dist * min_dist:
                return False
        return True

    # 3a. MHE Fuzine Hydroelectric Weir & Powerhouse + Grad Fuzine Courtyard Walls + Golovec Peak Antenna
    infra_props.append(("chpowerstation", -52.0, 782.0, 20.0))
    infra_props.append(("dam_ironbridge_part2", -42.0, 771.0, 69.6))
    infra_props.append(("dam_ironbridge_part2", -25.0, 777.0, 69.6))
    # Grad Fuzine castle courtyard perimeter walls
    infra_props.append(("stonefence_10m", -42.0, 804.0, 26.0))
    infra_props.append(("stonefence_10m", -33.0, 808.5, 26.0))
    infra_props.append(("stonefence_10m", -28.5, 799.5, 116.0))
    # Golovec Observatory / Ridge Radio Mast
    infra_props.append(("mi_antenna", -220.0, -520.0, 0.0))
    infra_props.append(("antennamast", 120.0, -480.0, 0.0))
    # Vevce Paper Mill industrial smokestack & silos
    infra_props.append(("chimney_02", 145.0, 745.0, 0.0))
    infra_props.append(("silo_02", 165.0, 738.0, 35.0))

    for _, px, pz, _ in infra_props:
        placed_xy.append((px, pz))

    # 3b. High-voltage power towers (14 in OSM)
    for wx, wz in power_towers.values():
        if can_place_prop(wx, wz, 55.0):
            infra_props.append(("antennamast", wx, wz, 0.0))
            placed_xy.append((wx, wz))

    # 3c. Utility poles (thinned to >=55m spacing, max 50)
    pole_cnt = 0
    for wx, wz in power_poles.values():
        if pole_cnt >= 50:
            break
        if can_place_prop(wx, wz, 55.0):
            infra_props.append(("cablepole", wx, wz, 0.0))
            placed_xy.append((wx, wz))
            pole_cnt += 1

    # 3d. Street lamps from OSM nodes + spaced along A1 motorway & Litijska cesta (max 65)
    lamp_cnt = 0
    for wx, wz in street_lamps.values():
        if lamp_cnt >= 35:
            break
        if can_place_prop(wx, wz, 45.0):
            infra_props.append(("lamp_post", wx, wz, 0.0))
            placed_xy.append((wx, wz))
            lamp_cnt += 1

    for hw, pts in motorway_ways:
        if lamp_cnt >= 65:
            break
        for i in range(len(pts) - 1):
            wx0, wz0 = pts[i][0] - 1024.0, pts[i][1] - 1024.0
            wx1, wz1 = pts[i + 1][0] - 1024.0, pts[i + 1][1] - 1024.0
            seg_len = math.hypot(wx1 - wx0, wz1 - wz0)
            if seg_len < 15.0:
                continue
            yaw = math.degrees(math.atan2(wx1 - wx0, wz1 - wz0)) % 360.0
            if can_place_prop(wx0, wz0, 75.0):
                tmpl = "lamppost_highway_01" if hw == "motorway" else "lamp_post"
                infra_props.append((tmpl, wx0, wz0, yaw))
                placed_xy.append((wx0, wz0))
                lamp_cnt += 1
                if lamp_cnt >= 65:
                    break

    # 3e. OSM Walls & Fences (thinned to >=35m spacing, max 45)
    fence_cnt = 0
    for btype, pts in fence_ways:
        if fence_cnt >= 45:
            break
        wx0, wz0 = pts[0][0] - 1024.0, pts[0][1] - 1024.0
        wx1, wz1 = pts[-1][0] - 1024.0, pts[-1][1] - 1024.0
        if math.hypot(wx1 - wx0, wz1 - wz0) < 10.0:
            continue
        yaw = math.degrees(math.atan2(wx1 - wx0, wz1 - wz0)) % 180.0
        if can_place_prop(wx0, wz0, 35.0):
            tmpl = "stonefence_10m" if btype == "wall" else "wirefence_24m"
            infra_props.append((tmpl, wx0, wz0, yaw))
            placed_xy.append((wx0, wz0))
            fence_cnt += 1

    return river_mask, road_mask_2048, meadow_mask_2048, infra_props


def encode_dxt1_blocks(img_rgb: np.ndarray) -> bytes:
    h, w, _ = img_rgb.shape
    ph, pw = max(4, h), max(4, w)
    if ph != h or pw != w:
        img_rgb = np.pad(img_rgb, ((0, ph - h), (0, pw - w), (0, 0)), mode="edge")
    blocks = (
        img_rgb.reshape(ph // 4, 4, pw // 4, 4, 3)
        .transpose(0, 2, 1, 3, 4)
        .reshape(-1, 16, 3)
        .astype(np.int32)
    )
    cmax = blocks.max(axis=1)
    cmin = blocks.min(axis=1)
    c0 = ((cmax[:, 0] >> 3) << 11) | ((cmax[:, 1] >> 2) << 5) | (cmax[:, 2] >> 3)
    c1 = ((cmin[:, 0] >> 3) << 11) | ((cmin[:, 1] >> 2) << 5) | (cmin[:, 2] >> 3)
    swap = c0 < c1
    c0_s = np.where(swap, c1, c0).astype(np.uint16)
    c1_s = np.where(swap, c0, c1).astype(np.uint16)
    cmax_s = np.where(swap[:, None], cmin, cmax)
    cmin_s = np.where(swap[:, None], cmax, cmin)
    p0, p1 = cmax_s, cmin_s
    p2 = (2 * p0 + p1) // 3
    p3 = (p0 + 2 * p1) // 3
    pal = np.stack([p0, p1, p2, p3], axis=1)
    diff = blocks[:, :, None, :] - pal[:, None, :, :]
    dist = (diff * diff).sum(axis=-1)
    idx = dist.argmin(axis=-1).astype(np.uint32)
    idx[c0_s == c1_s] = 0
    shifts = np.arange(0, 32, 2, dtype=np.uint32)
    packed_idx = (idx << shifts[None, :]).sum(axis=1, dtype=np.uint32)
    out = np.empty(len(c0_s), dtype=[("c0", "<u2"), ("c1", "<u2"), ("idx", "<u4")])
    out["c0"], out["c1"], out["idx"] = c0_s, c1_s, packed_idx
    return out.tobytes()


def make_dxt1_dds(img_rgb: np.ndarray, flags: int = 0x000A1007, mipmaps: bool = True) -> bytes:
    h, w, _ = img_rgb.shape
    mips = []
    cur = img_rgb
    while True:
        mips.append(encode_dxt1_blocks(cur))
        if not mipmaps or (cur.shape[0] == 1 and cur.shape[1] == 1):
            break
        cur = cur.astype(np.uint16)
        cur = (
            (cur[0::2, 0::2] + cur[1::2, 0::2] + cur[0::2, 1::2] + cur[1::2, 1::2]) >> 2
        ).astype(np.uint8)
    num_mips = len(mips) if mipmaps else 0
    caps = 0x401008 if mipmaps else 0x1000
    pitch = max(1, w // 4) * max(1, h // 4) * 8
    hdr = b"DDS " + struct.pack(
        "<7I44xII4s20xII12x",
        124,
        flags,
        h,
        w,
        pitch,
        0,
        num_mips,
        32,
        4,
        b"DXT1",
        caps,
        0,
    )
    return hdr + b"".join(mips)


def compute_lod_delta(H: np.ndarray, step: int) -> np.ndarray:
    half = step // 2
    d = np.zeros((129, 129), dtype=np.float32)
    for r in range(0, 129, half):
        for c in range(0, 129, half):
            ro = (r % step) != 0
            co = (c % step) != 0
            if not ro and not co:
                continue
            elif not ro and co:
                d[r, c] = H[r, c] - 0.5 * (H[r, c - half] + H[r, c + half])
            elif ro and not co:
                d[r, c] = H[r, c] - 0.5 * (H[r - half, c] + H[r + half, c])
            else:
                d[r, c] = H[r, c] - 0.5 * (H[r + half, c - half] + H[r - half, c + half])
    return d


def main():
    t_start = time.time()
    print("=== 1. Extracting OSM Roads, RABA-KGZ Landuse, Infrastructure & Ljubljanica River ===")
    river_mask, road_mask_2048, meadow_mask_2048, infra_props = extract_osm_and_raba_layers()
    print(f"Extracted Ljubljanica mask ({river_mask.sum()} px), road network, RABA meadows, and {len(infra_props)} curated infrastructure props")

    hm_orig = (
        np.fromfile(os.path.join(WORKSPACE_DIR, "Heightmap.raw"), dtype=np.uint16).reshape(2049, 2049)
        * 0.01
    )

    # Align the local river valley water datum to SEA_WATER_LEVEL (269.50m)
    # and carve a smooth 2.75m bathymetric channel strictly inside river_mask.
    h_river_col = np.zeros(2049, dtype=np.float64)
    for x in range(2049):
        rows = np.where(river_mask[:, x])[0]
        if len(rows):
            h_river_col[x] = np.percentile(hm_orig[rows, x], 30)
        else:
            h_river_col[x] = h_river_col[x - 1] if x > 0 else 272.76
    h_river_smooth = gaussian_filter1d(h_river_col, sigma=16)

    dist_outside = distance_transform_edt(~river_mask)
    dist_inside = distance_transform_edt(river_mask)

    delta_col = (SEA_WATER_LEVEL - h_river_smooth)[None, :]
    w_elev = np.clip((305.0 - hm_orig) / 20.0, 0.0, 1.0)
    hm_adj = hm_orig + delta_col * w_elev

    bank_min = SEA_WATER_LEVEL + np.clip(dist_outside * 0.25, 0.20, 0.85)
    hm_adj[~river_mask] = np.maximum(hm_adj[~river_mask], bank_min[~river_mask])

    depth = np.clip(dist_inside * 0.45, 0.25, 2.75)
    hm_adj[river_mask] = SEA_WATER_LEVEL - depth[river_mask]

    # Smoothly grade dry-land approach embankments at both ends of each Ljubljanica bridge
    yy, xx = np.mgrid[0:2049, 0:2049]
    wx_grid = xx.astype(np.float64) - 1024.0
    wz_grid = yy.astype(np.float64) - 1024.0
    for b_name, b_type, bcx, bcz, byaw, by_road, b_half in LJUBLJANICA_BRIDGES:
        rad = math.radians(byaw)
        ux, uz = math.sin(rad), math.cos(rad)
        vx, vz = math.cos(rad), -math.sin(rad)
        dx = wx_grid - bcx
        dz = wz_grid - bcz
        along = dx * ux + dz * uz
        across = np.abs(dx * vx + dz * vz)
        for sign in (-1.0, 1.0):
            d_center = sign * (b_half + 2.0)
            dist_along = np.abs(along - d_center)
            pad_mask = (~river_mask) & (dist_along <= 10.0) & (across <= 10.0)
            w_pad = (
                np.clip(1.0 - dist_along / 10.0, 0.0, 1.0)
                * np.clip(1.0 - across / 10.0, 0.0, 1.0)
            )
            target_h = by_road - 0.15
            hm_adj[pad_mask] = (
                (1.0 - w_pad[pad_mask]) * hm_adj[pad_mask] + w_pad[pad_mask] * target_h
            )

    hm_2049 = np.clip(np.round(hm_adj * 100.0), 0, 65535).astype(np.uint16)
    hp_u16 = hm_2049[::2, ::2].copy()
    assert hp_u16.shape == (1025, 1025)
    hp_m = hp_u16.astype(np.float64) * 0.01
    river_1025 = river_mask[::2, ::2]
    dist_out_1025 = dist_outside[::2, ::2]

    print(f"Primary Heightmap range: {hp_m.min():.2f}m .. {hp_m.max():.2f}m")
    print(f"Ljubljanica river submerged vertices: {(hp_m <= SEA_WATER_LEVEL).sum()} (100% inside river channel)")
    print(f"Dry land vertices <= {SEA_WATER_LEVEL}m: {(hp_m[~river_1025] <= SEA_WATER_LEVEL).sum()}")

    hp_u16.tofile(os.path.join(RAW_DIR, "HeightmapPrimary.raw"))

    # Compute surface normals across 1025x1025 grid
    dh_dx = np.zeros_like(hp_m)
    dh_dz = np.zeros_like(hp_m)
    dh_dx[:, 1:-1] = (hp_m[:, 2:] - hp_m[:, :-2]) / 4.0
    dh_dx[:, 0] = (hp_m[:, 1] - hp_m[:, 0]) / 2.0
    dh_dx[:, -1] = (hp_m[:, -1] - hp_m[:, -2]) / 2.0

    dh_dz[1:-1, :] = (hp_m[2:, :] - hp_m[:-2, :]) / 4.0
    dh_dz[0, :] = (hp_m[1, :] - hp_m[0, :]) / 2.0
    dh_dz[-1, :] = (hp_m[-1, :] - hp_m[-2, :]) / 2.0

    nx = -dh_dx
    ny = np.ones_like(hp_m)
    nz = -dh_dz
    nlen = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx /= nlen
    ny /= nlen
    nz /= nlen

    norm_b = np.clip(np.round((nz + 1.0) * 127.5), 0, 255).astype(np.uint8)
    norm_g = np.clip(np.round(ny * 255.0), 0, 255).astype(np.uint8)
    norm_r = np.clip(np.round((nx + 1.0) * 127.5), 0, 255).astype(np.uint8)
    norm_a = np.full_like(norm_b, 255, dtype=np.uint8)
    packed_normals = np.stack([norm_b, norm_g, norm_r, norm_a], axis=-1)

    # Generate HeightmapPrimary.mat (1025x1025 uint8) with OSM Road & River Physics
    # 5 = Grass, 4 = Tarmac/Road, 2 = Rock (steep slope), 12 = Wet sand (riverbank/bed), 0 = border
    road_1025 = np.zeros((1025, 1025), dtype=np.uint8)
    road_1025[:1024, :1024] = road_mask_2048[::2, ::2]
    mat = np.full((1025, 1025), 5, dtype=np.uint8)
    mat[ny < 0.86] = 2
    mat[road_1025 > 0] = 4
    mat[hp_m <= SEA_WATER_LEVEL + 0.5] = 12
    mat[1024, :] = 0
    mat[:, 1024] = 0
    mat.tofile(os.path.join(RAW_DIR, "HeightmapPrimary.mat"))
    print("Wrote HeightmapPrimary.raw and GIS-mapped HeightmapPrimary.mat")

    sec_u8 = np.full((257, 257), 188, dtype=np.uint8)
    for sec_name in [
        "HeightmapSecondary_L1U1.raw",
        "HeightmapSecondary_U1.raw",
        "HeightmapSecondary_R1U1.raw",
        "HeightmapSecondary_L1.raw",
        "HeightmapSecondary_R1.raw",
        "HeightmapSecondary_L1D1.raw",
        "HeightmapSecondary_D1.raw",
        "HeightmapSecondary_R1D1.raw",
    ]:
        sec_u8.tofile(os.path.join(RAW_DIR, sec_name))

    print("=== 2. Updating Heightdata.con, Terrain.con, and Ljubljanica Emerald-Green Water.con ===")
    with open(os.path.join(RAW_DIR, "Heightdata.con"), "r") as f:
        hd_txt = f.read()
    hd_txt = hd_txt.replace("heightmap.setScale 2/0.0025/2", "heightmap.setScale 2/0.01/2")
    hd_txt = hd_txt.replace("heightmap.setScale 8/0.64/8", "heightmap.setScale 8/1.5/8")
    hd_txt = re.sub(
        r"heightmapcluster\.setSeaWaterLevel\s+[\d.]+",
        f"heightmapcluster.setSeaWaterLevel {SEA_WATER_LEVEL:.1f}",
        hd_txt,
    )
    with open(os.path.join(RAW_DIR, "Heightdata.con"), "w") as f:
        f.write(hd_txt)

    with open(os.path.join(RAW_DIR, "Terrain.con"), "r") as f:
        tc_txt = f.read()
    tc_txt = tc_txt.replace("terrain.primaryWorldScale 2/0.0025/2", "terrain.primaryWorldScale 2/0.01/2")
    tc_txt = tc_txt.replace("terrain.secondaryWorldScale 8/0.64/8", "terrain.secondaryWorldScale 8/1.5/8")
    with open(os.path.join(RAW_DIR, "Terrain.con"), "w") as f:
        f.write(tc_txt)

    # Tune Water.con to Ljubljanica's Alpine-karst emerald-green color and West-to-East flow
    water_con_txt = "\r\n".join(
        [
            "rem *** Slovenia Golovec - Ljubljanica Karst River Settings ***",
            "renderer.waterScroll 1/0",
            "renderer.waterAnimSpeed 45",
            "renderer.waterColor 0.04/0.14/0.09",
            "renderer.waterSpecularColor 0.72/0.76/0.70/1.6",
            "renderer.waterSpecularPower 28",
            "renderer.waterFogColor 32.00/72.00/56.00",
            "renderer.waterFogStartEndAndBase 4.00/120.00/1.00/0.50",
            "terrain.waterSunIntensity 0.85",
            "",
        ]
    )
    with open(os.path.join(RAW_DIR, "Water.con"), "w") as f:
        f.write(water_con_txt)

    print("=== 3. Compiling terraindata.raw from Dragon_Valley template + Slovenia LiDAR ===")
    with zipfile.ZipFile(os.path.join(DV_DIR, "client.zip"), "r") as zf:
        dv_td = zf.read("terraindata.raw")
    td_bytes = bytearray(
        dv_td.replace(b"levels/dragon_valley", b"levels/slovenia_golovec").replace(
            b"Levels/Dragon_Valley", b"Levels/slovenia_golovec"
        )
    )
    shift = len(td_bytes) - len(dv_td)
    assert shift == 12

    struct.pack_into("<fff", td_bytes, 0x0004, 2.0, 0.01, 2.0)
    struct.pack_into("<fff", td_bytes, 0x0010, 8.0, 1.5, 8.0)
    struct.pack_into("<ff", td_bytes, 0x0020, float(hp_m.max()), float(hp_m.min()))

    pos = 782593 + shift
    for p_idx in range(64):
        px, pz, old_maxh, old_minh, old_cx, old_cy, old_cz, old_rad = struct.unpack_from(
            "<iiffffff", td_bytes, pos
        )
        ix = px + 4
        iz = pz + 4
        H_raw = hp_u16[iz * 128 : iz * 128 + 129, ix * 128 : ix * 128 + 129].astype(np.float32)
        H_meters = H_raw * 0.01
        maxh = float(H_meters.max())
        minh = float(H_meters.min())
        cx = float(px * 256.0 + 128.0)
        cy = 0.5 * (maxh + minh)
        cz = float(pz * 256.0 + 128.0)
        rad = float(np.sqrt(128.0**2 + 128.0**2 + (0.5 * (maxh - minh)) ** 2))

        struct.pack_into("<iiffffff", td_bytes, pos, px, pz, maxh, minh, cx, cy, cz, rad)
        pos += 32

        vbuf = np.frombuffer(td_bytes, dtype=np.uint8, count=16641 * 24, offset=pos).reshape(
            129, 129, 24
        )
        vbuf[:, :, 4:8] = H_raw.view(np.uint8).reshape(129, 129, 4)
        d2 = compute_lod_delta(H_raw, 2)
        vbuf[:, :, 8:12] = d2.view(np.uint8).reshape(129, 129, 4)
        d3 = compute_lod_delta(H_raw, 4)
        vbuf[:, :, 12:16] = d3.view(np.uint8).reshape(129, 129, 4)
        vbuf[:, :, 16:20] = 0
        vbuf[:, :, 20:24] = packed_normals[iz * 128 : iz * 128 + 129, ix * 128 : ix * 128 + 129]
        pos += 16641 * 24

        while True:
            marker = struct.unpack_from("<i", td_bytes, pos)[0]
            pos += 4
            if marker == -1:
                break
            lid, bx, by, bz, brad, c1, c2, b4, c3 = struct.unpack_from("<iffffii4si", td_bytes, pos)
            new_lid = 1 if lid == 6 else lid
            new_by = cy
            new_brad = max(float(brad), rad)
            struct.pack_into(
                "<iffffii4si", td_bytes, pos, new_lid, bx, new_by, bz, new_brad, c1, c2, b4, c3
            )
            pos += 36 + (c1 + c3 * 12) * 2

    assert pos == 44019223 + shift

    for sp_idx in range(8):
        sp_id = struct.unpack_from("<i", td_bytes, pos)[0]
        maxh, minh, cx, cy, cz, rad = struct.unpack_from("<ffffff", td_bytes, pos + 4)
        nv = 10693 if (sp_idx % 2 == 0) else 23107
        v_f = np.frombuffer(td_bytes, dtype=np.float32, count=nv, offset=pos + 28)
        mask = v_f > 0.0
        v_f[mask] = 188.0 + np.clip((v_f[mask] - 65.0) * 0.30, 0.0, 57.0)
        new_maxh = float(v_f.max() * 1.5)
        new_minh = 0.0
        new_cy = 0.5 * new_maxh
        struct.pack_into("<ffffff", td_bytes, pos + 4, new_maxh, new_minh, cx, new_cy, cz, rad)
        pos += 28 + nv * 16

    assert pos == 46182647 + shift

    sp_terminator = struct.unpack_from("<i", td_bytes, pos)[0]
    assert sp_terminator == -1
    pos += 4
    num_qt_nodes = struct.unpack_from("<i", td_bytes, pos)[0]
    assert num_qt_nodes == 5461
    pos += 4
    for n_idx in range(num_qt_nodes):
        off = pos + n_idx * 44
        min_x, old_min_y, min_z, max_x, old_max_y, max_z = struct.unpack_from("<6f", td_bytes, off + 16)
        c0 = int(np.clip(round((min_x + 1024.0) / 2.0), 0, 1024))
        c1 = int(np.clip(round((max_x + 1024.0) / 2.0), 0, 1024))
        r0 = int(np.clip(round((min_z + 1024.0) / 2.0), 0, 1024))
        r1 = int(np.clip(round((max_z + 1024.0) / 2.0), 0, 1024))
        sub_h = hp_m[r0 : r1 + 1, c0 : c1 + 1]
        struct.pack_into("<6f", td_bytes, off + 16, min_x, float(sub_h.min()), min_z, max_x, float(sub_h.max()), max_z)

    pos += num_qt_nodes * 44
    assert pos == len(td_bytes)

    with open(os.path.join(RAW_DIR, "terraindata.raw"), "wb") as f:
        f.write(td_bytes)
    print(f"Wrote terraindata.raw ({len(td_bytes)} bytes)")

    print("=== 4. Generating GIS Detailmaps, LowDetailmaps, Colormaps & PR Lightmaps ===")
    cm_full = np.array(
        Image.open(os.path.join(WORKSPACE_DIR, "ColorMap_preview.png")).convert("RGB")
    )
    cm_south_up = np.flipud(cm_full)

    os.makedirs(os.path.join(RAW_DIR, "Colormaps"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DIR, "Lightmaps"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DIR, "Detailmaps"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DIR, "LowDetailmaps"), exist_ok=True)

    # Build 2048x2048 GIS Detailmap weights (R=dirt/road/sand, G=grass/meadow, B=rock/slope, R+G+B=255)
    ny_2048 = np.array(
        Image.fromarray((ny[:1024, :1024] * 255.0).astype(np.uint8)).resize(
            (2048, 2048), Image.Resampling.BILINEAR
        ),
        dtype=np.float32,
    ) / 255.0
    hp_2048 = hm_adj[:2048, :2048]
    dist_out_2048 = dist_outside[:2048, :2048]

    # Rock weight on steep Golovec slopes
    w_rock = np.clip((0.92 - ny_2048) / 0.14, 0.0, 1.0)
    # Dirt/road/riverbank weight on OSM roads & riverbanks/bed
    w_dirt = np.zeros((2048, 2048), dtype=np.float32)
    w_dirt[road_mask_2048 == 1] = 0.78
    w_dirt[road_mask_2048 == 2] = 0.95
    w_dirt[dist_out_2048 <= 3.0] = np.maximum(w_dirt[dist_out_2048 <= 3.0], 0.85)
    w_dirt[hp_2048 <= SEA_WATER_LEVEL] = 0.95
    # RABA meadows & farmland boost grass weight unless road/river
    w_rock[meadow_mask_2048] *= 0.25

    rem = np.clip(1.0 - w_dirt, 0.0, 1.0)
    b_ch = np.clip(np.round(rem * w_rock * 255.0), 0, 255).astype(np.uint8)
    r_ch = np.clip(np.round(w_dirt * 255.0), 0, 255).astype(np.uint8)
    g_ch = (255 - r_ch.astype(np.int32) - b_ch.astype(np.int32)).clip(0, 255).astype(np.uint8)
    detail_2048 = np.stack([r_ch, g_ch, b_ch], axis=-1)

    lowdetail_2048 = np.stack([255 - b_ch, np.zeros_like(b_ch), b_ch], axis=-1)

    # Project Reality Lightmap Standard (page14.rst & page15.rst)
    hp_flat = np.maximum(hp_m, SEA_WATER_LEVEL)
    w_dh_dx = np.zeros_like(hp_flat)
    w_dh_dz = np.zeros_like(hp_flat)
    w_dh_dx[:, 1:-1] = (hp_flat[:, 2:] - hp_flat[:, :-2]) / 4.0
    w_dh_dx[:, 0] = (hp_flat[:, 1] - hp_flat[:, 0]) / 2.0
    w_dx_end = (hp_flat[:, -1] - hp_flat[:, -2]) / 2.0
    w_dh_dx[:, -1] = w_dx_end
    w_dh_dz[1:-1, :] = (hp_flat[2:, :] - hp_flat[:-2, :]) / 4.0
    w_dh_dz[0, :] = (hp_flat[1, :] - hp_flat[0, :]) / 2.0
    w_dh_dz[-1, :] = (hp_flat[-1, :] - hp_flat[-2, :]) / 2.0

    wnx = -w_dh_dx
    wny = np.ones_like(hp_flat)
    wnz = -w_dh_dz
    wnlen = np.sqrt(wnx * wnx + wny * wny + wnz * wnz)
    wnx /= wnlen
    wny /= wnlen
    wnz /= wnlen

    lx, ly, lz = -0.45, 0.75, -0.48
    llen = np.sqrt(lx * lx + ly * ly + lz * lz)
    lx /= llen
    ly /= llen
    lz /= llen
    ndotl = np.clip(wnx * lx + wny * ly + wnz * lz, 0.0, 1.0)
    lm_g_1025 = np.clip(np.round(55.0 + 190.0 * ndotl), 0, 255).astype(np.uint8)
    lm_b_1025 = np.clip(np.round(185.0 + 45.0 * wny), 0, 255).astype(np.uint8)
    water_depth_1025 = np.clip(SEA_WATER_LEVEL - hp_m, 0.0, 3.0)
    lm_r_1025 = np.clip(np.round((water_depth_1025 / 3.0) * 255.0), 0, 255).astype(np.uint8)
    lm_1025 = np.stack([lm_r_1025, lm_g_1025, lm_b_1025], axis=-1)
    lm_4096 = np.array(Image.fromarray(lm_1025).resize((4096, 4096), Image.Resampling.BILINEAR))

    zero_256 = np.zeros((256, 256, 3), dtype=np.uint8)
    zero_dm_dds = make_dxt1_dds(zero_256, flags=0x00081007, mipmaps=False)

    for iz in range(8):
        for ix in range(8):
            r0, r1 = iz * 512, (iz + 1) * 512
            c0, c1 = ix * 512, (ix + 1) * 512
            cm_tile = cm_south_up[r0:r1, c0:c1]
            cm_dds = make_dxt1_dds(cm_tile, flags=0x000A1007, mipmaps=True)
            with open(os.path.join(RAW_DIR, "Colormaps", f"tx{ix:02d}x{iz:02d}.dds"), "wb") as f:
                f.write(cm_dds)

            lm_tile = lm_4096[r0:r1, c0:c1]
            lm_dds = make_dxt1_dds(lm_tile, flags=0x00021007, mipmaps=True)
            with open(os.path.join(RAW_DIR, "Lightmaps", f"tx{ix:02d}x{iz:02d}.dds"), "wb") as f:
                f.write(lm_dds)

            dr0, dr1 = iz * 256, (iz + 1) * 256
            dc0, dc1 = ix * 256, (ix + 1) * 256
            dm_tile = detail_2048[dr0:dr1, dc0:dc1]
            dm_dds = make_dxt1_dds(dm_tile, flags=0x00081007, mipmaps=False)
            with open(os.path.join(RAW_DIR, "Detailmaps", f"tx{ix:02d}x{iz:02d}_1.dds"), "wb") as f:
                f.write(dm_dds)

            p2_path = os.path.join(RAW_DIR, "Detailmaps", f"tx{ix:02d}x{iz:02d}_2.dds")
            if os.path.exists(p2_path):
                with open(p2_path, "wb") as f:
                    f.write(zero_dm_dds)

            ldm_tile = lowdetail_2048[dr0:dr1, dc0:dc1]
            ldm_dds = make_dxt1_dds(ldm_tile, flags=0x000A1007, mipmaps=True)
            with open(os.path.join(RAW_DIR, "LowDetailmaps", f"tx{ix:02d}x{iz:02d}.dds"), "wb") as f:
                f.write(ldm_dds)
        print(f"  Generated Colormaps, PR Lightmaps, GIS Detailmaps & LowDetailmaps row iz={iz}/7")

    border_coords = [(0, 0), (3, 0), (7, 0), (7, 3), (7, 7), (3, 7), (0, 7), (0, 3)]
    for s_idx, (bix, biz) in enumerate(border_coords):
        shutil.copyfile(
            os.path.join(RAW_DIR, "Colormaps", f"tx{bix:02d}x{biz:02d}.dds"),
            os.path.join(RAW_DIR, "Colormaps", f"tx_s{s_idx}.dds"),
        )

    print("=== 5. Configuring PR 3-Zone LiDAR Overgrowth & Shoreline Undergrowth ===")
    ndmp_u8 = np.fromfile(
        os.path.join(WORKSPACE_DIR, "levels/slovenia_golovec/Overgrowth/Overgrowth.raw"),
        dtype=np.uint8,
    ).reshape(2049, 2049)
    ndmp_1025 = ndmp_u8[::2, ::2]
    canopy_h_1025 = np.where(ndmp_1025 > 0, 1.5 + (ndmp_1025.astype(np.float32) / 255.0) * 18.5, 0.0)

    # Overgrowth.con: 3 zones using existing OvergrowthAtlas0.dds meshes
    og_con_txt = "\r\n".join(
        [
            "Overgrowth.viewDistance 500",
            "Overgrowth.viewDistanceScale 1",
            "Overgrowth.closeDistPercentage 0.15",
            "",
            "Overgrowth.addMaterial Bushes 1",
            "Overgrowth.setActiveMaterial Bushes",
            "Overgrowth.addType a",
            "Overgrowth.setActiveType a",
            "OvergrowthType.geometry nc_medbush01",
            "OvergrowthType.density 8",
            "OvergrowthType.normalScale 1",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 2",
            "OvergrowthType.minRadiusToOthers 2",
            "Overgrowth.addType b",
            "Overgrowth.setActiveType b",
            "OvergrowthType.geometry nc_leafybush01",
            "OvergrowthType.density 7",
            "OvergrowthType.normalScale 1",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 2",
            "OvergrowthType.minRadiusToOthers 2",
            "",
            "Overgrowth.addMaterial WoodsEdge 2",
            "Overgrowth.setActiveMaterial WoodsEdge",
            "Overgrowth.addType a",
            "Overgrowth.setActiveType a",
            "OvergrowthType.geometry nc_birch01",
            "OvergrowthType.density 5",
            "OvergrowthType.normalScale 0.4",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 4",
            "OvergrowthType.minRadiusToOthers 3",
            "Overgrowth.addType b",
            "Overgrowth.setActiveType b",
            "OvergrowthType.geometry nc_oak02",
            "OvergrowthType.density 4",
            "OvergrowthType.normalScale 0.4",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 5",
            "OvergrowthType.minRadiusToOthers 4",
            "Overgrowth.addType c",
            "Overgrowth.setActiveType c",
            "OvergrowthType.geometry nc_medbush01",
            "OvergrowthType.density 6",
            "OvergrowthType.normalScale 1",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 2",
            "OvergrowthType.minRadiusToOthers 2",
            "",
            "Overgrowth.addMaterial WoodsInterior 3",
            "Overgrowth.setActiveMaterial WoodsInterior",
            "Overgrowth.addType a",
            "Overgrowth.setActiveType a",
            "OvergrowthType.geometry nc_pinebig01",
            "OvergrowthType.density 5",
            "OvergrowthType.normalScale 0.25",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 5",
            "OvergrowthType.minRadiusToOthers 4",
            "Overgrowth.addType b",
            "Overgrowth.setActiveType b",
            "OvergrowthType.geometry nc_oak01",
            "OvergrowthType.density 4",
            "OvergrowthType.normalScale 0.3",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 5",
            "OvergrowthType.minRadiusToOthers 4",
            "Overgrowth.addType c",
            "Overgrowth.setActiveType c",
            "OvergrowthType.geometry nc_pine_cluster01",
            "OvergrowthType.density 3",
            "OvergrowthType.normalScale 0.3",
            "OvergrowthType.rotationScale 0",
            "OvergrowthType.minRadiusToSame 6",
            "OvergrowthType.minRadiusToOthers 5",
            "",
            r"Overgrowth.path levels\slovenia_golovec\overgrowth\\",
            "Overgrowth.preLoad",
            "",
        ]
    )
    with open(os.path.join(RAW_DIR, "Overgrowth", "Overgrowth.con"), "w") as f:
        f.write(og_con_txt)

    og_raw_1025 = np.zeros((1025, 1025), dtype=np.uint8)
    og_raw_1025[(canopy_h_1025 >= 1.5) & (canopy_h_1025 < 4.5)] = 1
    og_raw_1025[(canopy_h_1025 >= 4.5) & (canopy_h_1025 < 11.5)] = 2
    og_raw_1025[canopy_h_1025 >= 11.5] = 3
    og_raw_1025[road_1025 > 0] = 0
    og_raw_1025[hp_m <= SEA_WATER_LEVEL + 0.6] = 0
    og_raw_1025.tofile(os.path.join(RAW_DIR, "Overgrowth", "Overgrowth.raw"))

    # Undergrowth.raw (1025x1025 uint8):
    # 2 = ambientgrass (meadows/fields), 6 = Reed (forest floor sticks/rocks), 14 = reed (river shoreline cattails), 15 = erase
    meadow_1025 = np.zeros((1025, 1025), dtype=bool)
    meadow_1025[:1024, :1024] = meadow_mask_2048[::2, ::2]
    ug_raw_1025 = np.full((1025, 1025), 15, dtype=np.uint8)
    ug_raw_1025[meadow_1025 | (og_raw_1025 == 1) | (og_raw_1025 == 2)] = 2
    ug_raw_1025[og_raw_1025 == 3] = 6
    # River shoreline cattails (1m to 5m outside river edge)
    ug_raw_1025[(~river_1025) & (dist_out_1025 <= 3.5)] = 14
    ug_raw_1025[road_1025 > 0] = 15
    ug_raw_1025[river_1025] = 15
    ug_raw_1025.tofile(os.path.join(RAW_DIR, "Undergrowth.raw"))
    print("Wrote 3-zone Overgrowth.con, Overgrowth.raw, and shoreline/meadow Undergrowth.raw")

    print("=== 6. Grounding nDMP-Classified OSM Buildings, 5 Bridges & Infrastructure in StaticObjects.con ===")
    def sample_height(x: float, z: float) -> float:
        col = np.clip((x + 1024.0) / 2.0, 0.0, 1024.0)
        row = np.clip((z + 1024.0) / 2.0, 0.0, 1024.0)
        r0 = min(int(np.floor(row)), 1023)
        c0 = min(int(np.floor(col)), 1023)
        dr = row - r0
        dc = col - c0
        return float(
            (1 - dr) * (1 - dc) * hp_m[r0, c0]
            + (1 - dr) * dc * hp_m[r0, c0 + 1]
            + dr * (1 - dc) * hp_m[r0 + 1, c0]
            + dr * dc * hp_m[r0 + 1, c0 + 1]
        )

    def classify_building_with_ndmp(orig_t: str, x_4k: float, z_4k: float, idx: int) -> str:
        c = int(np.clip(round((x_4k + 2048.0) / 2.0), 0, 2048))
        r = int(np.clip(round((z_4k + 2048.0) / 2.0), 0, 2048))
        v = int(ndmp_u8[max(0, r - 2) : min(2049, r + 3), max(0, c - 2) : min(2049, c + 3)].max())
        h_roof = 0.0 if v == 0 else (1.5 + (v / 255.0) * 18.5)

        if orig_t == "warehouse_01":
            return "lrgfactorybuilding" if h_roof >= 11.0 else "lrgstrgbuilding_01"
        if h_roof >= 15.5 or orig_t in ("citybuilding_01", "eu_office_01", "me_apartment_01"):
            return "office_building" if (idx % 2 == 0) else "ch_house_modern_01"
        if h_roof >= 11.2 or orig_t in ("eu_building01", "eu_building02"):
            return "ch_house_modern_02" if (idx % 2 == 0) else "ch_house_modern_03"
        if h_roof < 5.2 or orig_t in ("shed_01", "wooden_shed", "barn_01", "barn_02", "farmhouse"):
            shed_pool = ["storage_shed", "toolshed", "ch_farm_01", "ch_farm_02", "ch_farm_03"]
            return shed_pool[idx % len(shed_pool)]
        house_pool = [
            "ch_house_01",
            "ch_house_02",
            "ch_house_05",
            "ch_house_05_v2",
            "village_house_1",
            "village_house_2",
        ]
        return house_pool[idx % len(house_pool)]

    with open(os.path.join(WORKSPACE_DIR, "levels/slovenia_golovec/StaticObjects.con"), "r") as f:
        src_so = f.read()

    pattern = re.compile(
        r"Object\.create\s+(\S+)\s*\n"
        r"Object\.absolutePosition\s+([-\d.]+)/([-\d.]+)/([-\d.]+)\s*\n"
        r"Object\.rotation\s+([-\d.]+/[-\d.]+/[-\d.]+)\s*\n"
        r"Object\.layer\s+(\d+)"
    )

    cp_positions = [(cx, cz) for _, _, _, _, cx, cz in CONTROL_POINTS]

    so_lines = [
        "rem *** Generated for Slovenia Golovec LiDAR & GURS nDMP Terrain ***",
        "if v_arg1 == BF2Editor",
        "console.allowMultipleFileLoad 0",
        "endIf",
        "",
    ]
    b_count = 0
    for idx, m in enumerate(pattern.finditer(src_so)):
        orig_t, xs, ys, zs, rot, layer = m.groups()
        x_4k, z_4k = float(xs), float(zs)
        xn = 0.5 * x_4k
        zn = 0.5 * z_4k
        if abs(xn) > 1000.0 or abs(zn) > 1000.0:
            continue
        if any((xn - cx) ** 2 + (zn - cz) ** 2 < 28.0**2 for cx, cz in cp_positions):
            continue
        if any(
            (xn - bcx) ** 2 + (zn - bcz) ** 2 < (b_half + 16.0) ** 2
            for _, _, bcx, bcz, _, _, b_half in LJUBLJANICA_BRIDGES
        ):
            continue
        yn = sample_height(xn, zn)
        if yn <= SEA_WATER_LEVEL + 0.35:
            continue
        t_name = classify_building_with_ndmp(orig_t, x_4k, z_4k, idx)
        so_lines.append(f"Object.create {t_name}")
        so_lines.append(f"Object.absolutePosition {xn:.3f}/{yn:.3f}/{zn:.3f}")
        so_lines.append(f"Object.rotation {rot}")
        so_lines.append(f"Object.layer {layer}")
        so_lines.append("")
        b_count += 1

    # Emit the 5 Ljubljanica river bridges
    bridge_obj_count = 0
    so_lines.append("rem *** Ljubljanica River Bridges (OSM & LiDAR Aligned) ***")
    for b_name, b_type, bcx, bcz, byaw, by_road, b_half in LJUBLJANICA_BRIDGES:
        rad = math.radians(byaw)
        ux, uz = math.sin(rad), math.cos(rad)
        yaw_opp = (byaw + 180.0) % 360.0
        if yaw_opp > 180.0:
            yaw_opp -= 360.0

        def add_bridge_part(tmpl: str, dist_m: float, pos_y: float, rot_yaw: float):
            nonlocal bridge_obj_count
            px = bcx + dist_m * ux
            pz = bcz + dist_m * uz
            so_lines.append(f"Object.create {tmpl}")
            so_lines.append(f"Object.absolutePosition {px:.3f}/{pos_y:.3f}/{pz:.3f}")
            so_lines.append(f"Object.rotation {rot_yaw:.1f}/0.0/0.0")
            so_lines.append("Object.layer 1")
            so_lines.append("Object.setLightSourceMask 6")
            so_lines.append("")
            bridge_obj_count += 1

        if b_type == "highway_low":
            seg_y = by_road - 5.05
            add_bridge_part("highway_bridge_low_head", -28.25, seg_y - 0.018, yaw_opp)
            add_bridge_part("highway_bridge_low_segment", -9.00, seg_y, byaw)
            add_bridge_part("highway_bridge_support", 0.00, seg_y - 13.95, byaw)
            add_bridge_part("highway_bridge_low_segment", 9.00, seg_y, byaw)
            add_bridge_part("highway_bridge_low_head", 28.25, seg_y - 0.018, byaw)
        elif b_type == "stone":
            seg_y = by_road - 4.67
            add_bridge_part("lrg_stonebridge_head", -9.827, seg_y, yaw_opp)
            add_bridge_part("lrg_stonebridge", 0.00, seg_y, byaw)
            add_bridge_part("lrg_stonebridge_head", 9.827, seg_y, byaw)
        elif b_type == "woodsteel_3":
            seg_y = by_road
            head_y = by_road - 4.90
            add_bridge_part("woodsteel_bridge_head", -15.00, head_y, yaw_opp)
            add_bridge_part("woodsteel_bridge_segment", -10.00, seg_y, byaw)
            add_bridge_part("woodsteel_bridge_segment", 0.00, seg_y, byaw)
            add_bridge_part("woodsteel_bridge_segment", 10.00, seg_y, byaw)
            add_bridge_part("woodsteel_bridge_head", 15.00, head_y, byaw)

    # Emit Curated OSM Infrastructure & Landmark Props
    infra_count = 0
    so_lines.append("rem *** Curated OSM Infrastructure & Slovenian Landmarks ***")
    for tmpl, ix, iz, iyaw in infra_props:
        if any((ix - cx) ** 2 + (iz - cz) ** 2 < 22.0**2 for cx, cz in cp_positions):
            continue
        iy = sample_height(ix, iz)
        if tmpl != "dam_ironbridge_part2" and iy <= SEA_WATER_LEVEL + 0.25:
            continue
        if tmpl == "dam_ironbridge_part2":
            iy = SEA_WATER_LEVEL + 1.80
        so_lines.append(f"Object.create {tmpl}")
        so_lines.append(f"Object.absolutePosition {ix:.3f}/{iy:.3f}/{iz:.3f}")
        so_lines.append(f"Object.rotation {iyaw:.1f}/0.0/0.0")
        so_lines.append("Object.layer 1")
        so_lines.append("")
        infra_count += 1

    with open(os.path.join(RAW_DIR, "StaticObjects.con"), "w") as f:
        f.write("\n".join(so_lines))
    print(
        f"Wrote StaticObjects.con: {b_count} nDMP-classified buildings, {bridge_obj_count} bridge parts, {infra_count} infrastructure props"
    )

    og_col_path = os.path.join(RAW_DIR, "Overgrowth", "OvergrowthCollision.con")
    if os.path.exists(og_col_path):
        with open(og_col_path, "r") as f:
            og_lines = f.readlines()
        og_out = []
        for line in og_lines:
            m_pos = re.match(
                r"^(\s*Object\.absolutePosition\s+)([-\d.]+)/([-\d.]+)/([-\d.]+)(.*)$", line
            )
            if m_pos:
                prefix, xs, ys, zs, suffix = m_pos.groups()
                x, z = float(xs), float(zs)
                og_out.append(f"{prefix}{x:.2f}/{sample_height(x, z):.2f}/{z:.2f}{suffix}\n")
            else:
                og_out.append(line)
        with open(og_col_path, "w") as f:
            f.writelines(og_out)

    print("=== 7. Generating 3D Spatial Audio Landscape (AmbientObjects.con) ===")
    ambient_emitters = [
        ("S_Golovec_Weir_Dam", "common/sound/levelambients/dragon_valley/dam_ambient_1.ogg", -40.0, 773.0, 140),
        ("S_Golovec_Weir_Gen", "common/sound/levelambients/dragon_valley/generators.ogg", -52.0, 782.0, 45),
        ("S_River_Bridge_A1", "common/sound/levelambients/dragon_valley/small_river_1.ogg", -674.5, 771.5, 90),
        ("S_River_Bridge_Fuzine", "common/sound/levelambients/dragon_valley/small_river_1.ogg", -26.0, 788.4, 80),
        ("S_River_Bridge_Vevce", "common/sound/levelambients/dragon_valley/small_river_1.ogg", 41.3, 795.5, 80),
        ("S_River_Bridge_Zadvor", "common/sound/levelambients/dragon_valley/small_river_1.ogg", 269.0, 464.0, 80),
        ("S_River_Bridge_Kaselj", "common/sound/levelambients/dragon_valley/small_river_1.ogg", 677.6, 882.5, 80),
        ("S_Vevce_PaperMill", "common/sound/levelambients/dragon_valley/factory_ambient.ogg", 145.0, 745.0, 130),
        ("S_Forest_Golovec_W", "common/sound/levelambients/dragon_valley/forest_1.ogg", -450.0, -350.0, 180),
        ("S_Forest_Golovec_C", "common/sound/levelambients/dragon_valley/forest_2.ogg", -100.0, -400.0, 180),
        ("S_Forest_Golovec_E", "common/sound/levelambients/dragon_valley/forest_3.ogg", 300.0, -350.0, 180),
        ("S_Forest_Zadvor_S", "common/sound/levelambients/dragon_valley/forest_1.ogg", 550.0, -200.0, 180),
        ("S_Town_Stepanjsko", "common/sound/levelambients/dragon_valley/village_ambient.ogg", -550.0, 580.0, 140),
        ("S_Town_Fuzine", "common/sound/levelambients/dragon_valley/village_ambient.ogg", -150.0, 680.0, 140),
        ("S_Town_Hrusica", "common/sound/levelambients/dragon_valley/village_ambient.ogg", -50.0, 100.0, 140),
        ("S_Town_Zadvor", "common/sound/levelambients/dragon_valley/village_ambient.ogg", 350.0, 220.0, 140),
    ]
    amb_lines = [
        "rem *** Slovenia Golovec 3D Spatial Audio Soundscape ***",
        "ObjectTemplate.create Sound S_AmbientDefault",
        "ObjectTemplate.activeSafe Sound S_AmbientDefault",
        'ObjectTemplate.soundFilename "common/sound/levelambients/dragon_valley/dragon_valley_global_ambient.ogg"',
        "ObjectTemplate.loopCount 0",
        "ObjectTemplate.is3dSound 0",
        "ObjectTemplate.stopType 0",
        "ObjectTemplate.volume 0.75",
        "ObjectTemplate.pitch 1",
        "ObjectTemplate.pan 0.5",
        "ObjectTemplate.reverbLevel 0",
        "ObjectTemplate.minDistance 300000",
        "",
    ]
    for s_name, s_file, sx, sz, s_dist in ambient_emitters:
        sy = max(sample_height(sx, sz), SEA_WATER_LEVEL) + 2.0
        amb_lines.extend(
            [
                f"ObjectTemplate.create Sound {s_name}",
                f"ObjectTemplate.activeSafe Sound {s_name}",
                "ObjectTemplate.isNotSaveable 1",
                f'ObjectTemplate.soundFilename "{s_file}"',
                "ObjectTemplate.loopCount 0",
                "ObjectTemplate.is3dSound 0",
                "ObjectTemplate.stopType 0",
                "ObjectTemplate.volume 0.9",
                "ObjectTemplate.pitch 1",
                "ObjectTemplate.pan 0.5",
                "ObjectTemplate.reverbLevel 0",
                f"ObjectTemplate.position {sx:.3f}/{sy:.3f}/{sz:.3f}",
                f"ObjectTemplate.minDistance {s_dist}",
                "",
                f"Object.create {s_name}",
                f"Object.absolutePosition {sx:.3f}/{sy:.3f}/{sz:.3f}",
                "Object.rotation 0.000/0.000/0.000",
                "Object.layer 1",
                "",
            ]
        )
    with open(os.path.join(RAW_DIR, "AmbientObjects.con"), "w") as f:
        f.write("\r\n".join(amb_lines))

    print("=== 8. Generating 6-CP Landmark & Bridge GameplayObjects.con with Vehicles ===")
    gpo_lines = [
        "rem *** Slovenia Golovec - 6-Landmark Conquest Layout (Full River & Bridge Combat Area) ***",
        "CombatAreaManager.use 1",
        "CombatAreaManager.timeAllowedOutside 10.000000",
        "",
        "CombatArea.create CombatArea_Golovec",
        "CombatArea.min 0.000000/0.000000",
        "CombatArea.max 0.000000/0.000000",
        "CombatArea.addAreaPoint -950.000/-950.000",
        "CombatArea.addAreaPoint 950.000/-950.000",
        "CombatArea.addAreaPoint 950.000/950.000",
        "CombatArea.addAreaPoint -950.000/950.000",
        "CombatArea.team 0",
        "CombatArea.vehicles 4",
        "CombatArea.layer 1",
        "CombatArea.usedByPathFinding 1",
        "",
        "if v_arg1 == host",
        "",
    ]

    # Vehicle spawner definitions per CP: (spawner_suffix, team1_veh, team2_veh, dx, dz, yaw)
    cp_vehicles = {
        1: [
            ("tank", "tnk_type98", "ustnk_m1a2", 14.0, 12.0, 0.0),
            ("apc", "apc_wz551", "usapc_lav25", -14.0, 12.0, 0.0),
            ("jeep1", "jep_paratrooper", "jeep_faav", 10.0, 20.0, 0.0),
        ],
        2: [
            ("apc", "apc_wz551", "usapc_lav25", 14.0, 10.0, 0.0),
            ("jeep", "jep_paratrooper", "jeep_faav", -12.0, 10.0, 0.0),
        ],
        3: [
            ("tank", "tnk_type98", "ustnk_m1a2", 15.0, 10.0, 20.0),
            ("jeep", "jep_paratrooper", "jeep_faav", -12.0, 12.0, 20.0),
        ],
        4: [
            ("apc", "apc_wz551", "usapc_lav25", 14.0, -10.0, 116.0),
            ("jeep", "jep_paratrooper", "jeep_faav", -12.0, -10.0, 116.0),
        ],
        5: [
            ("apc", "apc_wz551", "usapc_lav25", -14.0, 10.0, 12.0),
            ("jeep", "jep_paratrooper", "jeep_faav", 12.0, 10.0, 12.0),
        ],
        6: [
            ("tank", "tnk_type98", "ustnk_m1a2", -14.0, -12.0, 180.0),
            ("apc", "apc_wz551", "usapc_lav25", 14.0, -12.0, 180.0),
            ("jeep1", "jep_paratrooper", "jeep_faav", -10.0, -20.0, 180.0),
        ],
    }

    for cp_id, cp_name, team, radius, cx, cz in CONTROL_POINTS:
        for suf, v1, v2, vdx, vdz, vyaw in cp_vehicles.get(cp_id, []):
            sp_name = f"{cp_name}_{suf}"
            vx, vz = cx + vdx, cz + vdz
            vy = sample_height(vx, vz) + 1.80
            gpo_lines.extend(
                [
                    f"ObjectTemplate.create ObjectSpawner {sp_name}",
                    f"ObjectTemplate.activeSafe ObjectSpawner {sp_name}",
                    "ObjectTemplate.isNotSaveable 1",
                    "ObjectTemplate.hasMobilePhysics 0",
                    f"ObjectTemplate.setObjectTemplate 1 {v1}",
                    f"ObjectTemplate.setObjectTemplate 2 {v2}",
                    "ObjectTemplate.minSpawnDelay 20",
                    "ObjectTemplate.maxSpawnDelay 40",
                    "",
                    f"Object.create {sp_name}",
                    f"Object.absolutePosition {vx:.3f}/{vy:.3f}/{vz:.3f}",
                    f"Object.rotation {vyaw:.1f}/0.0/0.0",
                    f"Object.setControlPointId {cp_id}",
                    "Object.layer 1",
                    "",
                ]
            )

    gpo_lines.append("endIf")
    gpo_lines.append("")

    for cp_id, cp_name, team, radius, cx, cz in CONTROL_POINTS:
        cy = sample_height(cx, cz) + 0.15
        gpo_lines.extend(
            [
                f"ObjectTemplate.create ControlPoint {cp_name}",
                f"ObjectTemplate.activeSafe ControlPoint {cp_name}",
                'ObjectTemplate.modifiedByUser "BF2"',
                "ObjectTemplate.setNetworkableInfo ControlPointInfo",
                "ObjectTemplate.isNotSaveable 1",
                "ObjectTemplate.hasMobilePhysics 0",
                "ObjectTemplate.hasCollisionPhysics 1",
                "ObjectTemplate.physicsType Mesh",
                "ObjectTemplate.addTemplate flagpole",
                f"ObjectTemplate.setControlPointName {cp_name}",
                f"ObjectTemplate.radius {radius}",
                f"ObjectTemplate.team {team}",
                f"ObjectTemplate.controlPointId {cp_id}",
                "ObjectTemplate.timeToGetControl 15",
                "ObjectTemplate.timeToLoseControl 15",
                "ObjectTemplate.unableToChangeTeam 0",
                "ObjectTemplate.onlyTakeableByTeam 0",
                "",
                f"Object.create {cp_name}",
                f"Object.absolutePosition {cx:.3f}/{cy:.3f}/{cz:.3f}",
                "Object.rotation 0.000/0.000/0.000",
                "Object.layer 1",
                "",
            ]
        )
        for sp_idx, (sdx, sdz, syaw) in enumerate([(-6.0, -5.0, 0.0), (6.0, 5.0, 180.0)], start=1):
            sp_id = f"SP_{cp_name}_{sp_idx}"
            sx, sz = cx + sdx, cz + sdz
            sy = sample_height(sx, sz) + 1.25
            gpo_lines.extend(
                [
                    f"ObjectTemplate.create SpawnPoint {sp_id}",
                    f"ObjectTemplate.activeSafe SpawnPoint {sp_id}",
                    "ObjectTemplate.isNotSaveable 1",
                    "ObjectTemplate.setSpawnPositionOffset 0/1.25/0",
                    f"ObjectTemplate.setControlPointId {cp_id}",
                    "",
                    f"Object.create {sp_id}",
                    f"Object.absolutePosition {sx:.3f}/{sy:.3f}/{sz:.3f}",
                    f"Object.rotation {syaw:.1f}/0.000/0.000",
                    "Object.layer 1",
                    "",
                ]
            )

    gpo_txt = "\n".join(gpo_lines)
    with open(os.path.join(RAW_DIR, "GameplayObjects.con"), "w") as f:
        f.write(gpo_txt)
    for root, _, files in os.walk(os.path.join(RAW_DIR, "GameModes")):
        for fn in files:
            if fn.lower() == "gameplayobjects.con":
                with open(os.path.join(root, fn), "w") as f:
                    f.write(gpo_txt)

    cam_y = sample_height(0.0, 0.0) + 45.0
    with open(os.path.join(RAW_DIR, "Init.con"), "r") as f:
        init_txt = f.read()
    init_txt = re.sub(
        r"gameLogic\.setBeforeSpawnCamera\s+\S+\s+\S+",
        f"gameLogic.setBeforeSpawnCamera 0/{cam_y:.1f}/0 0/-12/0",
        init_txt,
    )
    with open(os.path.join(RAW_DIR, "Init.con"), "w") as f:
        f.write(init_txt)

    print("=== 9. Repacking client.zip & server.zip and Syncing to Workspace ===")
    for archive_name in ["client.zip", "server.zip"]:
        zip_path = os.path.join(LEVEL_DIR, archive_name)
        with zipfile.ZipFile(zip_path, "r") as zf_in:
            names = zf_in.namelist()
        tmp_zip = zip_path + ".tmp"
        with zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf_out:
            for name in names:
                raw_file = os.path.join(RAW_DIR, name)
                if os.path.isfile(raw_file):
                    zf_out.write(raw_file, name)
        os.replace(tmp_zip, zip_path)
        shutil.copy2(zip_path, os.path.join(WORKSPACE_DIR, "levels/slovenia_golovec", archive_name))
        print(f"  Packed & synced {archive_name} ({os.path.getsize(zip_path):,} bytes)")

    print(f"=== Compilation finished in {time.time() - t_start:.1f}s ===")


if __name__ == "__main__":
    main()
