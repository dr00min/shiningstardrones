#!/usr/bin/env python3
"""Rotate a Z-up glTF/GLB so its up axis is Y, which is what glTF requires.

ODM's textured model is in a local ENU-style frame with **Z up**. `obj2glb`
copies the vertices straight through without an axis remap, so the .glb arrives
lying on its back: one node, `{"mesh": 0}`, with no rotation and no matrix.

Every glTF viewer assumes Y-up and orbits about Y. With a Z-up model that means
dragging rolls the building like a clock face instead of turning it about its
own vertical — you cannot orbit it, and no amount of constraining the camera
fixes that, because the camera is not the thing that is wrong.

How to tell, without opening it in anything: the vertical axis is the one whose
bounds never cross zero, because it is an elevation above a datum rather than an
offset from a centre. Here Z sat at 54.2..67.7 m while X and Y straddled zero.

The fix is a -90 degree rotation about X, which maps (x, y, z) -> (x, z, -y), so
the old Z becomes the new Y. Written into the node as a quaternion rather than
applied to the vertices: it costs nothing, survives Draco compression untouched,
and works in every viewer rather than relying on one viewer's own orientation
attribute and its Euler convention.

A translation is added too, so the model's base sits at y=0 instead of floating
at its original altitude above the origin.

Usage:  python3 scripts/fix_glb_up_axis.py media/model.glb
        python3 scripts/fix_glb_up_axis.py media/model.glb --check
"""
import json
import math
import struct
import sys
from pathlib import Path

# -90 degrees about X, as [x, y, z, w]
ROT_X_MINUS_90 = [-math.sin(math.pi / 4), 0.0, 0.0, math.cos(math.pi / 4)]


def read_glb(path):
    raw = path.read_bytes()
    magic, version, _ = struct.unpack_from("<III", raw, 0)
    if magic != 0x46546C67:
        raise SystemExit(f"{path} is not a GLB")
    off, chunks = 12, []
    while off < len(raw):
        clen, ctype = struct.unpack_from("<II", raw, off)
        chunks.append((ctype, raw[off + 8: off + 8 + clen]))
        off += 8 + clen
    gltf = json.loads(chunks[0][1])
    return version, gltf, chunks


def write_glb(path, version, gltf, chunks):
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)                      # JSON chunk pads with spaces
    out = [(0x4E4F534A, js)]
    for ctype, data in chunks[1:]:
        data += b"\x00" * (-len(data) % 4)           # BIN chunk pads with nulls
        out.append((ctype, data))
    total = 12 + sum(8 + len(d) for _, d in out)
    buf = bytearray(struct.pack("<III", 0x46546C67, version, total))
    for ctype, data in out:
        buf += struct.pack("<II", len(data), ctype) + data
    path.write_bytes(buf)


def bounds(gltf):
    lo, hi = [1e30] * 3, [-1e30] * 3
    for a in gltf.get("accessors", []):
        if a.get("type") == "VEC3" and a.get("componentType") == 5126 and "min" in a:
            for k in range(3):
                lo[k] = min(lo[k], a["min"][k])
                hi[k] = max(hi[k], a["max"][k])
    return lo, hi


def vertical_axis(lo, hi):
    """The axis that never crosses zero is an elevation, i.e. the up axis."""
    for k in range(3):
        if lo[k] > 0 or hi[k] < 0:
            return k
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    check = "--check" in sys.argv
    if not args:
        raise SystemExit(__doc__)
    path = Path(args[0])

    version, gltf, chunks = read_glb(path)
    lo, hi = bounds(gltf)
    axis = vertical_axis(lo, hi)
    names = "XYZ"

    for k in range(3):
        marker = "  <- vertical" if k == axis else ""
        print(f"  {names[k]}  {lo[k]:8.1f} .. {hi[k]:7.1f}   ({hi[k]-lo[k]:5.1f} m){marker}")

    scene = gltf.get("scenes", [{}])[gltf.get("scene", 0)]
    roots = scene.get("nodes", [])
    node = gltf["nodes"][roots[0]] if roots else None

    if node is None:
        raise SystemExit("  no root node to correct")
    if axis is None:
        print("  no axis is unambiguously vertical — nothing done")
        return
    if axis == 1:
        print("  already Y-up — nothing to do")
        return
    if "rotation" in node or "matrix" in node:
        print("  root node already carries a transform — not touching it")
        return
    if check:
        print("  WOULD PATCH: add -90deg X rotation and ground the base")
        return

    node["rotation"] = ROT_X_MINUS_90
    node["translation"] = [0.0, -lo[axis], 0.0]
    write_glb(path, version, gltf, chunks)
    print(f"  patched: rotation {['%.4f' % v for v in ROT_X_MINUS_90]}, "
          f"translation Y {-lo[axis]:.1f}")
    print(f"  {names[axis]}-up is now Y-up; base sits at y=0")


if __name__ == "__main__":
    main()
