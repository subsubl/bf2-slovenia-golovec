"""
Refractor 2 .con Configuration Parser and Geospatial Helper for BF2 Levels.
Used by the E2E verification test suite.
"""

import os
import re
import struct
from typing import List, Dict, Any, Tuple, Optional
import numpy as np


class DynamicLevelDir(os.PathLike):
    """Dynamic path-like object returning current BF2_LEVEL_DIR from environment."""
    def __fspath__(self) -> str:
        return os.getenv("BF2_LEVEL_DIR", "/home/ator/BF2/levels/slovenia_golovec")

    def __str__(self) -> str:
        return os.getenv("BF2_LEVEL_DIR", "/home/ator/BF2/levels/slovenia_golovec")


LEVEL_DIR = DynamicLevelDir()


def get_level_dir() -> str:
    """Returns target BF2 level directory from environment or default."""
    return os.getenv("BF2_LEVEL_DIR", "/home/ator/BF2/levels/slovenia_golovec")


class ConParser:
    """Parses Battlefield 2 Refractor 2 .con configuration files."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lines: List[str] = []
        self.raw_content = ""
        self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Configuration file not found: {self.filepath}")
        with open(self.filepath, "r", encoding="utf-8", errors="replace") as f:
            self.raw_content = f.read()
        self.lines = self.raw_content.splitlines()

    def get_clean_lines(self) -> List[Tuple[int, str]]:
        """Returns (line_number, stripped_line) excluding empty lines and remarks."""
        clean = []
        for idx, line in enumerate(self.lines, start=1):
            s = line.strip()
            if not s or s.lower().startswith("rem"):
                continue
            clean.append((idx, s))
        return clean

    def check_vector_syntax_no_spaces(self) -> List[Tuple[int, str]]:
        """
        Detects illegal spaces around forward slashes in vector arguments.
        BF2 engine requires vectors strictly formatted as X/Y/Z with NO spaces.
        Returns list of (line_num, line_str) containing illegal spaces.
        """
        violations = []
        # Pattern matches a slash preceded or followed by whitespace within a command line
        slash_space_regex = re.compile(r"(\S+\s+/\s*\S+|\S*\s*/\s+\S+)")
        for idx, line in enumerate(self.lines, start=1):
            s = line.strip()
            if not s or s.lower().startswith("rem"):
                continue
            # Split off comment if inline
            if "rem " in s.lower():
                s = s[:s.lower().find("rem ")].strip()
            # Look for tokens with space around slash
            if re.search(r"\d+\.?\d*\s+/\s*|\s*/\s+\d+\.?\d*", s):
                violations.append((idx, line))
        return violations

    def check_block_structure(self) -> Dict[str, Any]:
        """
        Checks balancing of if / else / endIf blocks.
        """
        stack = []
        errors = []
        blocks = []
        for idx, line in enumerate(self.lines, start=1):
            s = line.strip()
            if not s or s.lower().startswith("rem"):
                continue
            tokens = s.split()
            cmd = tokens[0]
            if cmd == "if":
                condition = " ".join(tokens[1:])
                stack.append((idx, condition))
            elif cmd == "else":
                if not stack:
                    errors.append(f"Line {idx}: 'else' without matching 'if'")
            elif cmd == "endIf":
                if not stack:
                    errors.append(f"Line {idx}: 'endIf' without matching 'if'")
                else:
                    start_idx, cond = stack.pop()
                    blocks.append({"start_line": start_idx, "end_line": idx, "condition": cond})
        while stack:
            start_idx, cond = stack.pop()
            errors.append(f"Line {start_idx}: Unclosed 'if {cond}' block")
        return {"balanced": len(errors) == 0, "errors": errors, "blocks": blocks}

    def parse_run_commands(self) -> List[str]:
        """Extracts scripts invoked via 'run <path>'."""
        runs = []
        for _, line in self.get_clean_lines():
            tokens = line.split()
            if tokens and tokens[0].lower() == "run" and len(tokens) > 1:
                runs.append(tokens[1])
        return runs

    def parse_static_objects(self) -> List[Dict[str, Any]]:
        """
        Parses StaticObjects.con:
        Extracts list of instances:
        {
            'template': str,
            'position': (X, Y, Z),
            'rotation': (Yaw, Pitch, Roll),
            'layer': int,
            'line': int
        }
        """
        objects = []
        current = {}
        for idx, line in self.get_clean_lines():
            tokens = line.split(maxsplit=1)
            if not tokens:
                continue
            cmd = tokens[0]
            arg = tokens[1] if len(tokens) > 1 else ""

            if cmd == "Object.create":
                if current and "template" in current and "position" in current:
                    objects.append(current)
                current = {"template": arg.strip(), "line": idx}
            elif cmd == "Object.absolutePosition":
                parts = [float(p) for p in arg.strip().split("/")]
                if len(parts) == 3:
                    current["position"] = tuple(parts)
            elif cmd == "Object.rotation":
                parts = [float(p) for p in arg.strip().split("/")]
                if len(parts) == 3:
                    current["rotation"] = tuple(parts)
            elif cmd == "Object.layer":
                try:
                    current["layer"] = int(arg.strip())
                except ValueError:
                    current["layer"] = 1

        if current and "template" in current and "position" in current:
            objects.append(current)
        return objects

    def parse_combat_areas(self) -> List[Dict[str, Any]]:
        """
        Parses CombatArea definitions from GameplayObjects.con.
        Returns list of areas:
        {
            'name': str,
            'points': [(X, Z), ...],
            'team': int,
            'vehicles': int
        }
        """
        areas = []
        current_area = None
        for idx, line in self.get_clean_lines():
            tokens = line.split(maxsplit=1)
            cmd = tokens[0]
            arg = tokens[1] if len(tokens) > 1 else ""

            if cmd == "CombatArea.create":
                if current_area:
                    areas.append(current_area)
                current_area = {"name": arg.strip(), "points": [], "line": idx, "team": 0}
            elif cmd == "CombatArea.addAreaPoint" and current_area is not None:
                parts = [float(p) for p in arg.strip().split("/")]
                if len(parts) == 2:
                    current_area["points"].append(tuple(parts))
            elif cmd == "CombatArea.team" and current_area is not None:
                try:
                    current_area["team"] = int(arg.strip())
                except ValueError:
                    pass

        if current_area:
            areas.append(current_area)
        return areas

    def parse_gameplay_objects(self) -> Dict[str, Any]:
        """
        Parses ControlPoints and SpawnPoints from GameplayObjects.con.
        """
        templates: Dict[str, Dict[str, Any]] = {}
        instances: List[Dict[str, Any]] = []

        curr_template = None
        curr_obj = None

        for idx, line in self.get_clean_lines():
            tokens = line.split(maxsplit=1)
            cmd = tokens[0]
            arg = tokens[1] if len(tokens) > 1 else ""

            if cmd == "ObjectTemplate.create":
                parts = arg.strip().split()
                if len(parts) >= 2:
                    ttype, tname = parts[0], parts[1]
                    curr_template = {"type": ttype, "name": tname, "line": idx}
                    templates[tname] = curr_template
            elif curr_template is not None:
                if cmd == "ObjectTemplate.controlPointId":
                    curr_template["controlPointId"] = int(arg.strip())
                elif cmd == "ObjectTemplate.setControlPointId":
                    curr_template["controlPointId"] = int(arg.strip())
                elif cmd == "ObjectTemplate.team":
                    curr_template["team"] = int(arg.strip())
                elif cmd == "ObjectTemplate.radius":
                    curr_template["radius"] = float(arg.strip())
                elif cmd == "ObjectTemplate.timeToGetControl":
                    curr_template["timeToGetControl"] = float(arg.strip())
                elif cmd == "ObjectTemplate.timeToLoseControl":
                    curr_template["timeToLoseControl"] = float(arg.strip())
                elif cmd == "ObjectTemplate.setSpawnPositionOffset":
                    curr_template["spawnPositionOffset"] = [float(p) for p in arg.strip().split("/")]

            if cmd == "Object.create":
                if curr_obj and "template" in curr_obj and "position" in curr_obj:
                    instances.append(curr_obj)
                curr_obj = {"template": arg.strip(), "line": idx}
            elif curr_obj is not None:
                if cmd == "Object.absolutePosition":
                    curr_obj["position"] = tuple([float(p) for p in arg.strip().split("/")])
                elif cmd == "Object.rotation":
                    curr_obj["rotation"] = tuple([float(p) for p in arg.strip().split("/")])
                elif cmd == "Object.layer":
                    curr_obj["layer"] = int(arg.strip())

        if curr_obj and "template" in curr_obj and "position" in curr_obj:
            instances.append(curr_obj)

        # Merge templates with instances
        cps = []
        sps = []
        for inst in instances:
            tname = inst["template"]
            tinfo = templates.get(tname, {})
            merged = {**tinfo, **inst}
            if tinfo.get("type") == "ControlPoint":
                cps.append(merged)
            elif tinfo.get("type") == "SpawnPoint":
                sps.append(merged)

        return {"templates": templates, "instances": instances, "control_points": cps, "spawn_points": sps}


class HeightmapSampler:
    """Provides ground elevation sampling from Heightmap.raw."""

    def __init__(self, raw_path: str = "/home/ator/BF2/Heightmap.raw"):
        self.raw_path = raw_path
        self.grid_size = 2049
        self.scale_xz = 2.0
        self.scale_y = 0.01
        self.world_half = 2048.0
        self.data: Optional[np.ndarray] = None
        self._load()

    def _load(self):
        if not os.path.exists(self.raw_path):
            raise FileNotFoundError(f"Heightmap file not found: {self.raw_path}")
        self.data = np.fromfile(self.raw_path, dtype="<u2").reshape((self.grid_size, self.grid_size))

    def sample_bilinear(self, x: float, z: float) -> float:
        """
        Bilinear elevation interpolation matching Refractor 2 specifications:
        u = (x + 2048.0) / 2.0
        v = (z + 2048.0) / 2.0
        Row 0 is South (z=-2048), Row 2048 is North (z=+2048)
        Col 0 is West (x=-2048), Col 2048 is East (x=+2048)
        """
        u = np.clip((x + self.world_half) / self.scale_xz, 0.0, float(self.grid_size - 1))
        v = np.clip((z + self.world_half) / self.scale_xz, 0.0, float(self.grid_size - 1))

        c0, r0 = int(np.floor(u)), int(np.floor(v))
        c1, r1 = min(c0 + 1, self.grid_size - 1), min(r0 + 1, self.grid_size - 1)
        s, t = u - c0, v - r0

        h00 = self.data[r0, c0] * self.scale_y
        h10 = self.data[r0, c1] * self.scale_y
        h01 = self.data[r1, c0] * self.scale_y
        h11 = self.data[r1, c1] * self.scale_y

        return float((1.0 - s) * (1.0 - t) * h00 + s * (1.0 - t) * h10 + (1.0 - s) * t * h01 + s * t * h11)


def polygon_signed_area(pts: List[Tuple[float, float]]) -> float:
    """
    Computes signed area of a 2D polygon using the Shoelace formula.
    Positive area indicates Counter-Clockwise (CCW) winding.
    Negative area indicates Clockwise (CW) winding.
    """
    n = len(pts)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        x1, z1 = pts[i]
        x2, z2 = pts[(i + 1) % n]
        area += (x1 * z2 - x2 * z1)
    return 0.5 * area


def point_in_polygon(x: float, z: float, pts: List[Tuple[float, float]]) -> bool:
    """Ray casting algorithm to determine if point (x, z) is inside polygon."""
    n = len(pts)
    if n < 3:
        return False
    inside = False
    p1x, p1z = pts[0]
    for i in range(1, n + 1):
        p2x, p2z = pts[i % n]
        if min(p1z, p2z) < z <= max(p1z, p2z):
            if x <= max(p1x, p2x):
                x_inters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                if p1x == p2x or x <= x_inters:
                    inside = not inside
        p1x, p1z = p2x, p2z
    return inside
