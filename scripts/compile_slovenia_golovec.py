#!/usr/bin/env python3
"""
Compile authentic Slovenia Golovec LiDAR DEM, Orthophoto Colormaps, Lightmaps,
terraindata.raw, HeightmapPrimary.raw, StaticObjects.con, and GameplayObjects.con
for Battlefield 2 (Refractor 2 Engine).
"""
import glob
import io
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


def extract_ljubljanica_river_mask() -> np.ndarray:
    """
    Reconstructs the exact 2049x2049 boolean mask of the Ljubljanica river channel
    (including islands as dry land and the Vevce mill canal) from the cached OSM
    multipolygon relation (natural=water, water=river) and D96TM projection.
    """
    origin_e = 468498.0
    origin_n = 99466.0
    to_d96 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3794", always_xy=True)

    nodes = {}
    ways = {}
    relations = []
    for path in sorted(glob.glob(os.path.join(WORKSPACE_DIR, ".osm_cache", "osm_*.xml"))):
        tree = ET.parse(path)
        root = tree.getroot()
        for nd in root.findall("node"):
            nid = nd.attrib["id"]
            lat = float(nd.attrib["lat"])
            lon = float(nd.attrib["lon"])
            e, n = to_d96.transform(lon, lat)
            gx = (e - origin_e + 2048.0) / 4096.0 * 2048.0
            gz = (n - origin_n + 2048.0) / 4096.0 * 2048.0
            nodes[nid] = (gx, gz)
        for way in root.findall("way"):
            wid = way.attrib["id"]
            tags = {t.attrib["k"]: t.attrib["v"] for t in way.findall("tag")}
            nds = [nd.attrib["ref"] for nd in way.findall("nd") if nd.attrib["ref"] in nodes]
            ways[wid] = (tags, nds, [nodes[r] for r in nds])
        for rel in root.findall("relation"):
            tags = {t.attrib["k"]: t.attrib["v"] for t in rel.findall("tag")}
            members = [
                (m.attrib["type"], m.attrib["ref"], m.attrib.get("role", ""))
                for m in rel.findall("member")
            ]
            relations.append((tags, members))

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

    img = Image.new("L", (2049, 2049), 0)
    draw = ImageDraw.Draw(img)
    draw.polygon(chain, fill=1)
    for _, _, ipts in inner_ways:
        if len(ipts) >= 3:
            draw.polygon(ipts, fill=0)
    if "538835423" in ways:
        draw.line(ways["538835423"][2], fill=1, width=6)

    return np.array(img, dtype=bool)


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


def make_dxt1_dds(img_rgb: np.ndarray, flags: int = 0x000A1007) -> bytes:
    h, w, _ = img_rgb.shape
    mips = []
    cur = img_rgb
    while True:
        mips.append(encode_dxt1_blocks(cur))
        if cur.shape[0] == 1 and cur.shape[1] == 1:
            break
        cur = cur.astype(np.uint16)
        cur = (
            (cur[0::2, 0::2] + cur[1::2, 0::2] + cur[0::2, 1::2] + cur[1::2, 1::2]) >> 2
        ).astype(np.uint8)
    num_mips = len(mips)
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
        0x401008,
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
    print("=== 1. Loading Slovenia Golovec LiDAR Heightmap.raw (2049x2049) & Aligning Ljubljanica River ===")
    hm_orig = (
        np.fromfile(os.path.join(WORKSPACE_DIR, "Heightmap.raw"), dtype=np.uint16).reshape(2049, 2049)
        * 0.01
    )
    river_mask = extract_ljubljanica_river_mask()

    # In the raw LiDAR DEM, the Ljubljanica water surface slopes downstream from 272.76m (West,
    # above the Fuzine weir) down to 266.79m (East, Zalog), while BF2's SeaWaterLevel is a flat
    # horizontal plane at 269.50m. Align the local river valley water datum to SEA_WATER_LEVEL
    # and carve a smooth 2.75m bathymetric channel strictly inside river_mask so water fills the
    # entire Ljubljanica river from West to East with zero flooding of surrounding fields.
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

    # Ensure all dry land (~river_mask) stays cleanly above SEA_WATER_LEVEL
    bank_min = SEA_WATER_LEVEL + np.clip(dist_outside * 0.25, 0.20, 0.85)
    hm_adj[~river_mask] = np.maximum(hm_adj[~river_mask], bank_min[~river_mask])

    # Carve bathymetric riverbed strictly inside the Ljubljanica river channel
    depth = np.clip(dist_inside * 0.45, 0.25, 2.75)
    hm_adj[river_mask] = SEA_WATER_LEVEL - depth[river_mask]

    hm_2049 = np.clip(np.round(hm_adj * 100.0), 0, 65535).astype(np.uint16)

    # Decimate by stride 2 to 1025x1025 for BF2 primary heightmap
    # Note: Heightmap.raw is already Row 0 = South (-Z), Row 2048 = North (+Z), Col 0 = West (-X), Col 2048 = East (+X)
    hp_u16 = hm_2049[::2, ::2].copy()
    assert hp_u16.shape == (1025, 1025)
    hp_m = hp_u16.astype(np.float64) * 0.01
    river_1025 = river_mask[::2, ::2]

    print(f"Primary Heightmap range: {hp_m.min():.2f}m .. {hp_m.max():.2f}m")
    print(f"Ljubljanica river submerged vertices: {(hp_m <= SEA_WATER_LEVEL).sum()} (100% inside river channel)")
    print(f"Dry land vertices <= {SEA_WATER_LEVEL}m: {(hp_m[~river_1025] <= SEA_WATER_LEVEL).sum()}")
    print(f"Center (0,0) elevation: {hp_m[512, 512]:.2f}m")
    print(f"South hills mean: {hp_m[:256, :].mean():.2f}m | North river valley mean: {hp_m[768:, :].mean():.2f}m")

    # Write HeightmapPrimary.raw
    hp_u16.tofile(os.path.join(RAW_DIR, "HeightmapPrimary.raw"))

    # Compute surface normals across the full 1025x1025 grid (dx = dz = 2.0m)
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

    # Pack normals into BGRA bytes [B=nz, G=ny, R=nx, A=255]
    norm_b = np.clip(np.round((nz + 1.0) * 127.5), 0, 255).astype(np.uint8)
    norm_g = np.clip(np.round(ny * 255.0), 0, 255).astype(np.uint8)
    norm_r = np.clip(np.round((nx + 1.0) * 127.5), 0, 255).astype(np.uint8)
    norm_a = np.full_like(norm_b, 255, dtype=np.uint8)
    packed_normals = np.stack([norm_b, norm_g, norm_r, norm_a], axis=-1)  # (1025, 1025, 4)

    # Generate HeightmapPrimary.mat (1025x1025 uint8)
    # 5 = Grass, 2 = Rock (steep slope), 12 = Wet sand (river channel <= 270m), 0 = border row/col
    mat = np.full((1025, 1025), 5, dtype=np.uint8)
    mat[ny < 0.85] = 2
    mat[hp_m <= 270.0] = 12
    mat[1024, :] = 0
    mat[:, 1024] = 0
    mat.tofile(os.path.join(RAW_DIR, "HeightmapPrimary.mat"))
    print("Wrote HeightmapPrimary.raw and HeightmapPrimary.mat")

    # Write Secondary Heightmaps (257x257 uint8) with scale 8/1.5/8 -> 188 * 1.5 = 282.0m
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

    print("=== 2. Updating Heightdata.con and Terrain.con ===")
    with open(os.path.join(RAW_DIR, "Heightdata.con"), "r") as f:
        hd_txt = f.read()
    hd_txt = hd_txt.replace("heightmap.setScale 2/0.0025/2", "heightmap.setScale 2/0.01/2")
    hd_txt = hd_txt.replace("heightmap.setScale 8/0.64/8", "heightmap.setScale 8/1.5/8")
    hd_txt = re.sub(
        r"heightmapcluster\.setSeaWaterLevel\s+[\d.]+",
        "heightmapcluster.setSeaWaterLevel 269.5",
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

    print("=== 3. Compiling terraindata.raw from Dragon_Valley template + Slovenia LiDAR ===")
    with zipfile.ZipFile(os.path.join(DV_DIR, "client.zip"), "r") as zf:
        dv_td = zf.read("terraindata.raw")
    # Replace levels/dragon_valley -> levels/slovenia_golovec
    td_bytes = bytearray(
        dv_td.replace(b"levels/dragon_valley", b"levels/slovenia_golovec").replace(
            b"Levels/Dragon_Valley", b"Levels/slovenia_golovec"
        )
    )
    shift = len(td_bytes) - len(dv_td)
    assert shift == 12, f"Expected +12 byte shift, got {shift}"

    # 3a. Patch Global Header (0x0000..0x0028)
    struct.pack_into("<fff", td_bytes, 0x0004, 2.0, 0.01, 2.0)  # primaryWorldScale
    struct.pack_into("<fff", td_bytes, 0x0010, 8.0, 1.5, 8.0)   # secondaryWorldScale
    struct.pack_into("<ff", td_bytes, 0x0020, float(hp_m.max()), float(hp_m.min()))

    # 3b. Patch all 64 Primary QuadPatch blocks
    pos = 782593 + shift
    for p_idx in range(64):
        px, pz, old_maxh, old_minh, old_cx, old_cy, old_cz, old_rad = struct.unpack_from(
            "<iiffffff", td_bytes, pos
        )
        ix = px + 4
        iz = pz + 4
        assert 0 <= ix < 8 and 0 <= iz < 8, f"Invalid patch coords ({px}, {pz})"

        # Extract 129x129 heightmap slice (raw uint16 as float32)
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

        # Patch 129x129x24 vertex buffer
        vbuf = np.frombuffer(td_bytes, dtype=np.uint8, count=16641 * 24, offset=pos).reshape(
            129, 129, 24
        )
        # f1 = H_raw
        vbuf[:, :, 4:8] = H_raw.view(np.uint8).reshape(129, 129, 4)
        # f2 = LOD1 morph delta (step=2)
        d2 = compute_lod_delta(H_raw, 2)
        vbuf[:, :, 8:12] = d2.view(np.uint8).reshape(129, 129, 4)
        # f3 = LOD2 morph delta (step=4)
        d3 = compute_lod_delta(H_raw, 4)
        vbuf[:, :, 12:16] = d3.view(np.uint8).reshape(129, 129, 4)
        # f4 = 0.0
        vbuf[:, :, 16:20] = 0
        # bytes[20:24] = packed BGRA normal
        vbuf[:, :, 20:24] = packed_normals[iz * 128 : iz * 128 + 129, ix * 128 : ix * 128 + 129]

        pos += 16641 * 24

        # Traverse detail layer submeshes until marker == -1
        while True:
            marker = struct.unpack_from("<i", td_bytes, pos)[0]
            pos += 4
            if marker == -1:
                break
            lid, bx, by, bz, brad, c1, c2, b4, c3 = struct.unpack_from("<iffffii4si", td_bytes, pos)
            # If lid == 6 (empty underwater patch in Dragon_Valley, i.e., (5,7), (6,7), (7,7)),
            # change lid to 1 so QuadPatch::load sets isEmptyPatch=0 and loads Colormaps/tx05x07..tx07x07!
            new_lid = 1 if lid == 6 else lid
            new_by = cy
            new_brad = max(float(brad), rad)
            struct.pack_into(
                "<iffffii4si", td_bytes, pos, new_lid, bx, new_by, bz, new_brad, c1, c2, b4, c3
            )
            pos += 36 + (c1 + c3 * 12) * 2

    assert pos == 44019223 + shift, f"Expected pos {44019223 + shift}, got {pos}"

    # 3c. Patch all 8 SurroundingPatch blocks
    for sp_idx in range(8):
        sp_id = struct.unpack_from("<i", td_bytes, pos)[0]
        maxh, minh, cx, cy, cz, rad = struct.unpack_from("<ffffff", td_bytes, pos + 4)
        nv = 10693 if (sp_idx % 2 == 0) else 23107
        v_f = np.frombuffer(td_bytes, dtype=np.float32, count=nv, offset=pos + 28)
        # Keep 0.0 border skirt at 0.0, map non-zero heights to 188.0..245.0 (282m..367.5m at scale 1.5)
        mask = v_f > 0.0
        v_f[mask] = 188.0 + np.clip((v_f[mask] - 65.0) * 0.30, 0.0, 57.0)
        new_maxh = float(v_f.max() * 1.5)
        new_minh = 0.0
        new_cy = 0.5 * new_maxh
        struct.pack_into("<ffffff", td_bytes, pos + 4, new_maxh, new_minh, cx, new_cy, cz, rad)
        pos += 28 + nv * 16

    assert pos == 46182647 + shift, f"Expected pos {46182647 + shift}, got {pos}"

    # 3d. Patch all 5,461 Frustum Culling & LOD Quadtree Nodes at the end of terraindata.raw
    sp_terminator = struct.unpack_from("<i", td_bytes, pos)[0]
    assert sp_terminator == -1, f"Expected -1 terminator after SurroundingPatches, got {sp_terminator}"
    pos += 4
    num_qt_nodes = struct.unpack_from("<i", td_bytes, pos)[0]
    assert num_qt_nodes == 5461, f"Expected 5461 quadtree nodes, got {num_qt_nodes}"
    pos += 4
    for n_idx in range(num_qt_nodes):
        off = pos + n_idx * 44
        min_x, old_min_y, min_z, max_x, old_max_y, max_z = struct.unpack_from("<6f", td_bytes, off + 16)
        c0 = int(np.clip(round((min_x + 1024.0) / 2.0), 0, 1024))
        c1 = int(np.clip(round((max_x + 1024.0) / 2.0), 0, 1024))
        r0 = int(np.clip(round((min_z + 1024.0) / 2.0), 0, 1024))
        r1 = int(np.clip(round((max_z + 1024.0) / 2.0), 0, 1024))
        sub_h = hp_m[r0 : r1 + 1, c0 : c1 + 1]
        new_min_y = float(sub_h.min())
        new_max_y = float(sub_h.max())
        struct.pack_into("<6f", td_bytes, off + 16, min_x, new_min_y, min_z, max_x, new_max_y, max_z)

    pos += num_qt_nodes * 44
    assert pos == len(td_bytes), f"Expected EOF {len(td_bytes)}, got {pos}"

    with open(os.path.join(RAW_DIR, "terraindata.raw"), "wb") as f:
        f.write(td_bytes)
    print(f"Wrote terraindata.raw ({len(td_bytes)} bytes, including all {num_qt_nodes} quadtree nodes)")

    print("=== 4. Generating 64+8 Colormaps, 64 Lightmaps, and missing Detailmaps/LowDetailmaps ===")
    cm_full = np.array(
        Image.open(os.path.join(WORKSPACE_DIR, "ColorMap_preview.png")).convert("RGB")
    )
    assert cm_full.shape == (4096, 4096, 3)
    # Flip vertically so Row 0 is South (iz=0) and Row 4095 is North (iz=7)
    cm_south_up = np.flipud(cm_full)

    os.makedirs(os.path.join(RAW_DIR, "Colormaps"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DIR, "Lightmaps"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DIR, "Detailmaps"), exist_ok=True)
    os.makedirs(os.path.join(RAW_DIR, "LowDetailmaps"), exist_ok=True)

    # Project Reality Lightmap Standard (page14.rst & page15.rst):
    # 1. Clamp underwater heights to SEA_WATER_LEVEL before computing G (Sun) and B (Sky) normals
    # 2. Encode Sea Water Depth/Transparency (0 at shoreline -> 255 at >=3.0m depth) in Red (R) channel
    hp_flat = np.maximum(hp_m, SEA_WATER_LEVEL)
    w_dh_dx = np.zeros_like(hp_flat)
    w_dh_dz = np.zeros_like(hp_flat)
    w_dh_dx[:, 1:-1] = (hp_flat[:, 2:] - hp_flat[:, :-2]) / 4.0
    w_dh_dx[:, 0] = (hp_flat[:, 1] - hp_flat[:, 0]) / 2.0
    w_dh_dx[:, -1] = (hp_flat[:, -1] - hp_flat[:, -2]) / 2.0
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

    for iz in range(8):
        for ix in range(8):
            r0, r1 = iz * 512, (iz + 1) * 512
            c0, c1 = ix * 512, (ix + 1) * 512
            cm_tile = cm_south_up[r0:r1, c0:c1]
            cm_dds = make_dxt1_dds(cm_tile, flags=0x000A1007)
            with open(os.path.join(RAW_DIR, "Colormaps", f"tx{ix:02d}x{iz:02d}.dds"), "wb") as f:
                f.write(cm_dds)

            lm_tile = lm_4096[r0:r1, c0:c1]
            lm_dds = make_dxt1_dds(lm_tile, flags=0x00021007)
            with open(os.path.join(RAW_DIR, "Lightmaps", f"tx{ix:02d}x{iz:02d}.dds"), "wb") as f:
                f.write(lm_dds)
        print(f"  Generated Colormaps & Lightmaps row iz={iz}/7")

    # Surrounding colormaps tx_s0.dds .. tx_s7.dds from border tiles
    border_coords = [(0, 0), (3, 0), (7, 0), (7, 3), (7, 7), (3, 7), (0, 7), (0, 3)]
    for s_idx, (bix, biz) in enumerate(border_coords):
        shutil.copyfile(
            os.path.join(RAW_DIR, "Colormaps", f"tx{bix:02d}x{biz:02d}.dds"),
            os.path.join(RAW_DIR, "Colormaps", f"tx_s{s_idx}.dds"),
        )

    # Copy tx04x07 detailmap & lowdetailmap to (5,7), (6,7), (7,7)
    for mx in [5, 6, 7]:
        shutil.copyfile(
            os.path.join(RAW_DIR, "Detailmaps", "tx04x07_1.dds"),
            os.path.join(RAW_DIR, "Detailmaps", f"tx{mx:02d}x07_1.dds"),
        )
        shutil.copyfile(
            os.path.join(RAW_DIR, "LowDetailmaps", "tx04x07.dds"),
            os.path.join(RAW_DIR, "LowDetailmaps", f"tx{mx:02d}x07.dds"),
        )

    print("=== 5. Re-Grounding All 1,309 OSM Buildings in StaticObjects.con ===")
    # Helper for bilinear height lookup on hp_m (1025x1025 spanning [-1024, +1024])
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

    # Map workspace template names to 100% verified vanilla BF2 Objects_server.zip templates
    template_map = {
        "eu_house_01": "ch_house_01",
        "eu_house_02": "ch_house_02",
        "me_house_01": "village_house_1",
        "me_house_04": "village_house_2",
        "me_house_06": "ch_house_05",
        "me_apartment_01": "ch_house_modern_01",
        "eu_building01": "ch_house_modern_02",
        "eu_building02": "ch_house_modern_03",
        "citybuilding_01": "office_building",
        "eu_office_01": "office_building",
        "warehouse_01": "lrgstrgbuilding_01",
        "farmhouse": "ch_farm_01",
        "barn_01": "ch_farm_02",
        "barn_02": "ch_farm_03",
        "shed_01": "storage_shed",
        "wooden_shed": "toolshed",
    }

    with open(os.path.join(WORKSPACE_DIR, "levels/slovenia_golovec/StaticObjects.con"), "r") as f:
        src_so = f.read()

    pattern = re.compile(
        r"Object\.create\s+(\S+)\s*\n"
        r"Object\.absolutePosition\s+([-\d.]+)/([-\d.]+)/([-\d.]+)\s*\n"
        r"Object\.rotation\s+([-\d.]+/[-\d.]+/[-\d.]+)\s*\n"
        r"Object\.layer\s+(\d+)"
    )

    # Collect CP & spawn coordinates from GameplayObjects.con to enforce 25m clearance
    cp_positions = []
    gpo_main = os.path.join(RAW_DIR, "GameplayObjects.con")
    if os.path.exists(gpo_main):
        with open(gpo_main, "r") as f:
            for m_pos in re.finditer(
                r"Object\.absolutePosition\s+([-\d.]+)/([-\d.]+)/([-\d.]+)", f.read()
            ):
                cp_positions.append((float(m_pos.group(1)), float(m_pos.group(3))))

    so_lines = [
        "rem *** Generated for Slovenia Golovec LiDAR Terrain ***",
        "if v_arg1 == BF2Editor",
        "console.allowMultipleFileLoad 0",
        "endIf",
        "",
    ]
    b_count = 0
    for m in pattern.finditer(src_so):
        orig_t, xs, ys, zs, rot, layer = m.groups()
        t_name = template_map.get(orig_t, "ch_house_01")
        xn = 0.5 * float(xs)
        zn = 0.5 * float(zs)
        if abs(xn) > 1000.0 or abs(zn) > 1000.0:
            continue
        if any((xn - cx) ** 2 + (zn - cz) ** 2 < 25.0**2 for cx, cz in cp_positions):
            continue
        yn = sample_height(xn, zn)
        # Skip if in the river channel
        if yn <= SEA_WATER_LEVEL + 0.35:
            continue
        so_lines.append(f"Object.create {t_name}")
        so_lines.append(f"Object.absolutePosition {xn:.3f}/{yn:.3f}/{zn:.3f}")
        so_lines.append(f"Object.rotation {rot}")
        so_lines.append(f"Object.layer {layer}")
        so_lines.append("")
        b_count += 1

    with open(os.path.join(RAW_DIR, "StaticObjects.con"), "w") as f:
        f.write("\n".join(so_lines))
    print(f"Wrote StaticObjects.con with {b_count} grounded OSM buildings")

    # Re-ground OvergrowthCollision.con
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
        print("Re-grounded Overgrowth/OvergrowthCollision.con")

    print("=== 6. Re-Grounding Control Points & Spawns in GameplayObjects.con & Init.con ===")
    # Update every Object.absolutePosition X/Y/Z in GameplayObjects.con to match hp_m(X, Z)
    def ground_gpo_file(filepath: str):
        if not os.path.exists(filepath):
            return
        with open(filepath, "r") as f:
            lines = f.readlines()
        out_lines = []
        current_obj = ""
        for line in lines:
            m_create = re.match(r"^\s*Object\.create\s+(\S+)", line)
            if m_create:
                current_obj = m_create.group(1).lower()
            m_pos = re.match(
                r"^(\s*Object\.absolutePosition\s+)([-\d.]+)/([-\d.]+)/([-\d.]+)(.*)$", line
            )
            if m_pos:
                prefix, xs, ys, zs, suffix = m_pos.groups()
                x, z = float(xs), float(zs)
                # Ensure northern MEC base is at Z=420 (dry town ground ~273.5m)
                y_ground = sample_height(x, z)
                if "spawner" in current_obj or "aa_" in current_obj or "art_" in current_obj or "at_" in current_obj or "apc_" in current_obj or "tank_" in current_obj or "jeep_" in current_obj:
                    y_new = y_ground + 1.8
                elif "cp_" in current_obj:
                    y_new = y_ground + 0.15
                else:
                    y_new = y_ground + 1.2
                out_lines.append(f"{prefix}{x:.3f}/{y_new:.3f}/{z:.3f}{suffix}\n")
            else:
                out_lines.append(line)
        with open(filepath, "w") as f:
            f.writelines(out_lines)

    ground_gpo_file(os.path.join(RAW_DIR, "GameplayObjects.con"))
    for root, _, files in os.walk(os.path.join(RAW_DIR, "GameModes")):
        for fn in files:
            if fn.lower() == "gameplayobjects.con":
                ground_gpo_file(os.path.join(root, fn))

    # Update BeforeSpawnCamera in Init.con to 0 / (sample_height(0,0) + 45) / 0
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

    print("=== 7. Repacking client.zip & server.zip and Syncing to Workspace ===")
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
