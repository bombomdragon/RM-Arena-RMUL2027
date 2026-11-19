"""Extract RMUL 2027 3V3 field geometry from RMUL2027_3V3_1to1.blend and export map-rmul2027.glb.

Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b ../RMUL2027_3V3_1to1.blend \
      --python scripts/extract_rmul2027_blend.py
"""
import json
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
GLB_OUT = ROOT / "frontend/public/assets/map-rmul2027.glb"
GEOM_OUT = Path(
    "/Users/bombomdragon_mac/.gemini/antigravity/brain/d2e54910-0075-4da6-a01f-8708da3560d3/scratch/rmul2027_geometry.json"
)


def world_verts(obj, depsgraph):
    ev = obj.evaluated_get(depsgraph)
    mesh = ev.to_mesh()
    verts = [ev.matrix_world @ v.co for v in mesh.vertices]
    ev.to_mesh_clear()
    return verts


def bbox(verts):
    xs = [v.x for v in verts]
    ys = [v.y for v in verts]
    zs = [v.z for v in verts]
    return {
        "min_x": round(min(xs), 6),
        "max_x": round(max(xs), 6),
        "min_y": round(min(ys), 6),
        "max_y": round(max(ys), 6),
        "min_z": round(min(zs), 6),
        "max_z": round(max(zs), 6),
    }


def to_arena(x, y, width, height):
    return [round(x + width / 2.0, 6), round(height / 2.0 - y, 6)]


def arena_bbox(b, width, height):
    ax0 = round(b["min_x"] + width / 2.0, 6)
    ax1 = round(b["max_x"] + width / 2.0, 6)
    ay0 = round(height / 2.0 - b["max_y"], 6)
    ay1 = round(height / 2.0 - b["min_y"], 6)
    return {
        "x": ax0,
        "y": ay0,
        "w": round(ax1 - ax0, 6),
        "h": round(ay1 - ay0, 6),
        "cx": round((ax0 + ax1) / 2.0, 6),
        "cy": round((ay0 + ay1) / 2.0, 6),
        "bottom": b["min_z"],
        "top": b["max_z"],
        "height": round(b["max_z"] - b["min_z"], 6),
    }


def z_profile(verts, width, height, axis="y"):
    """Summarize max Z across coordinate slices along X or Y (in Arena-1 coordinates)."""
    buckets = {}
    for v in verts:
        ax, ay = to_arena(v.x, v.y, width, height)
        key = round(ay if axis == "y" else ax, 2)
        buckets.setdefault(key, []).append(round(v.z, 4))
    out = []
    for k in sorted(buckets):
        zs = buckets[k]
        out.append([k, min(zs), max(zs)])
    return out


def convex_hull_2d(points):
    pts = sorted(set((round(p[0], 4), round(p[1], 4)) for p in points))
    if len(pts) <= 2:
        return [list(p) for p in pts]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [list(p) for p in lower[:-1] + upper[:-1]]


def main():
    depsgraph = bpy.context.evaluated_depsgraph_get()
    ground_col = bpy.data.collections.get("01_Ground_地板")
    ground_verts = []
    for obj in ground_col.all_objects:
        if obj.type == "MESH":
            ground_verts.extend(world_verts(obj, depsgraph))
    gb = bbox(ground_verts)
    width = round(gb["max_x"] - gb["min_x"], 6)
    height = round(gb["max_y"] - gb["min_y"], 6)

    struct_names = [
        "Red_Highland_Core",
        "Blue_Highland_Core",
        "Red_Highland_Barrier",
        "Blue_Highland_Barrier",
        "Red_Tunnel_Metal_Bridge",
        "Blue_Tunnel_Metal_Bridge",
        "Red_Tunnel_Outer_Support",
        "Blue_Tunnel_Outer_Support",
        "Red_Workbench_Core",
        "Blue_Workbench_Core",
        "Centre_Control_Bed",
        "Red_Control_PVC",
        "Blue_Control_PVC",
        "Centre_Control_PVC",
        "Red_Supply_PVC",
        "Blue_Supply_PVC",
        "Red_Supply_Card_Bed",
        "Blue_Supply_Card_Bed",
        "Red_Tunnel_Buff_PVC",
        "Blue_Tunnel_Buff_PVC",
        "Red_Highland_PVC",
        "Blue_Highland_PVC",
        "Red_Workbench_PVC",
        "Blue_Workbench_PVC",
    ]
    objects_info = {}
    for name in struct_names:
        obj = bpy.data.objects.get(name)
        if not obj or obj.type != "MESH":
            continue
        verts = world_verts(obj, depsgraph)
        b = bbox(verts)
        ab = arena_bbox(b, width, height)
        pts_2d = [to_arena(v.x, v.y, width, height) for v in verts]
        entry = {
            "raw_bbox": b,
            "arena_bbox": ab,
            "hull_2d": convex_hull_2d(pts_2d),
        }
        if "Highland_Core" in name or "Tunnel" in name or "Control_Bed" in name:
            entry["z_along_y"] = z_profile(verts, width, height, axis="y")
            entry["z_along_x"] = z_profile(verts, width, height, axis="x")
        objects_info[name] = entry

    rfid_groups = {}
    rfid_prefixes = [
        "RFID_Red_Highland",
        "RFID_Blue_Highland",
        "RFID_Red_Supply",
        "RFID_Blue_Supply",
        "RFID_Red_Tunnel",
        "RFID_Blue_Tunnel",
        "RFID_Centre",
    ]
    for prefix in rfid_prefixes:
        verts = []
        for obj in bpy.data.objects:
            if obj.type == "MESH" and obj.name.startswith(prefix):
                verts.extend(world_verts(obj, depsgraph))
        if verts:
            b = bbox(verts)
            ab = arena_bbox(b, width, height)
            pts_2d = [to_arena(v.x, v.y, width, height) for v in verts]
            rfid_groups[prefix] = {
                "raw_bbox": b,
                "arena_bbox": ab,
                "hull_2d": convex_hull_2d(pts_2d),
            }

    payload = {
        "width": width,
        "height": height,
        "ground_raw_bbox": gb,
        "objects": objects_info,
        "rfid_groups": rfid_groups,
    }
    GEOM_OUT.parent.mkdir(parents=True, exist_ok=True)
    GEOM_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"WROTE {GEOM_OUT} (width={width}, height={height})")

    # Export GLB without cameras/lights or RFID marker meshes
    hide_cols = {"90_Views_灯光相机", "07_RFID_隐蔽铺设示意"}
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        in_hidden = any(col.name in hide_cols for col in obj.users_collection)
        if not in_hidden:
            obj.select_set(True)
    GLB_OUT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(GLB_OUT),
        export_format="GLB",
        use_selection=True,
        export_yup=True,
        export_apply=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
    )
    print(f"EXPORTED {GLB_OUT} ({GLB_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
