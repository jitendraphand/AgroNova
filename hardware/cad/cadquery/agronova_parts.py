#!/usr/bin/env python3
"""Parametric AgroNova parts (CadQuery). Generates STEP + STL into hardware/step and hardware/stl.

Usage: python hardware/cad/cadquery/agronova_parts.py
Part numbers: AN-<SUBSYS>-<NNN>-r<REV>. Dimensions in mm. Geometry is a FIRST DESIGN DRAFT,
not reviewed, not printed, not load-tested.
"""
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[2]
TUBE = 25.0  # frame tube outer size (tools/sizing.py)
CLEAR = 0.4  # printed-fit clearance per side (A-22, verify with test coupon)
M5 = 5.5  # M5 clearance hole
INSERT_M4 = 5.6  # hole for M4 heat-set insert (check insert vendor datasheet)

# Frame (steel, NOT printed)
FRAME_L, FRAME_W, FRAME_H = 700.0, 450.0, 25.0
COVER_L, COVER_W, COVER_T, COVER_H = 700.0, 390.0, 3.0, 40.0


def frame():
    """AN-MECH-001-rA welded 25x25x1.5 mild-steel ladder frame (rails + 3 cross members)."""
    def tube(length, along_x):
        outer = cq.Workplane("XY").box(length, TUBE, TUBE) if along_x else cq.Workplane("XY").box(TUBE, length, TUBE)
        inner = cq.Workplane("XY").box(length + 1, TUBE - 3, TUBE - 3) if along_x else \
            cq.Workplane("XY").box(TUBE - 3, length + 1, TUBE - 3)
        return outer.cut(inner)
    f = tube(FRAME_L, True).translate((0, (FRAME_W - TUBE) / 2, 0))
    f = f.union(tube(FRAME_L, True).translate((0, -(FRAME_W - TUBE) / 2, 0)))
    for x in (-(FRAME_L - TUBE) / 2, 0, (FRAME_L - TUBE) / 2):
        f = f.union(tube(FRAME_W - 2 * TUBE, False).translate((x, 0, 0)))
    return f


def tube_clip():
    """AN-PRT-002-rA cable clip that snaps on the 25 mm tube, holds a 12 mm cable bundle."""
    ring = (cq.Workplane("XY").rect(TUBE + 2 * CLEAR + 6, TUBE + 2 * CLEAR + 6).extrude(15)
            .cut(cq.Workplane("XY").rect(TUBE + 2 * CLEAR, TUBE + 2 * CLEAR).extrude(15))
            .cut(cq.Workplane("XY").center(0, (TUBE + 6) / 2).rect(TUBE * 0.6, 4).extrude(15)))
    loop = (cq.Workplane("XY").center((TUBE + 6) / 2 + 8, 0).circle(9).extrude(15)
            .cut(cq.Workplane("XY").center((TUBE + 6) / 2 + 8, 0).circle(6.2).extrude(15)))
    return ring.union(loop)


def sensor_bracket():
    """AN-PRT-001-rA bracket clamping to frame tube; 80x80 plate with M4 insert grid for lidar/camera."""
    base = cq.Workplane("XY").box(80, 80, 6).translate((0, 0, 3))
    upright = cq.Workplane("XY").box(80, 6, 60).translate((0, -37, 36))
    clamp = (cq.Workplane("XY").box(TUBE + 2 * CLEAR + 10, 40, TUBE + 2 * CLEAR + 10)
             .cut(cq.Workplane("XY").box(TUBE + 2 * CLEAR, 41, TUBE + 2 * CLEAR))
             .translate((0, -37 - 20, 60 + (TUBE + 10) / 2)))
    b = base.union(upright).union(clamp)
    b = b.faces(">Z").workplane(origin=(0, 0, 6)).rect(60, 60, forConstruction=True).vertices().hole(INSERT_M4)
    gusset = cq.Workplane("YZ").polyline([(-34, 6), (-34, 50), (10, 6)]).close().extrude(6).translate((-3, 0, 0))
    return b.union(gusset)


def estop_housing():
    """AN-PRT-003-rA housing for a 22 mm panel-mount E-stop operator, 60x60x50, M5 base holes."""
    box = cq.Workplane("XY").box(60, 60, 50).faces("<Z").shell(-3)
    box = box.faces(">Z").workplane().hole(22.5)
    box = box.faces("<Z").workplane().rect(40, 40, forConstruction=True).vertices().hole(M5)
    return box.faces("<Y").workplane().center(0, -10).hole(12.5)  # M12 cable gland


def cover_half(side: int):
    """AN-PRT-004-rA (side=-1) / AN-PRT-005-rA (side=+1): top cover split into 2 halves (350x390) with
    tongue-and-groove seam + 3 bolted M5 tabs. Full cover (700x390) exceeds the 400 mm usable X/Y."""
    half_l = COVER_L / 2
    shell = (cq.Workplane("XY").box(half_l, COVER_W, COVER_H).faces("<Z").shell(-COVER_T)
             .translate((side * half_l / 2, 0, COVER_H / 2)))
    if side < 0:  # tongue on the seam face
        tongue = cq.Workplane("XY").box(6, COVER_W - 20, 2).translate((3, 0, COVER_H - 1.5))
        shell = shell.union(tongue)
    else:  # groove (tongue + clearance)
        groove = cq.Workplane("XY").box(6 + CLEAR, COVER_W - 20 + 2 * CLEAR, 2 + CLEAR).translate(
            ((6 + CLEAR) / 2, 0, COVER_H - 1.5))
        shell = shell.cut(groove)
    for y in (-150, 0, 150):
        tab = (cq.Workplane("XY").box(12, 20, 6).translate((side * 6, y, COVER_H - COVER_T - 3))
               .faces(">X" if side < 0 else "<X").workplane().hole(M5))
        shell = shell.union(tab.cut(cq.Workplane("YZ").circle(M5 / 2).extrude(30, both=True)
                                    .translate((side * 6, y, COVER_H - COVER_T - 3))))
    return shell


PRINTED = {
    "AN-PRT-001-rA_sensor_bracket": sensor_bracket,
    "AN-PRT-002-rA_tube_clip": tube_clip,
    "AN-PRT-003-rA_estop_housing": estop_housing,
    "AN-PRT-004-rA_cover_left": lambda: cover_half(-1),
    "AN-PRT-005-rA_cover_right": lambda: cover_half(+1),
}


def build():
    (ROOT / "stl").mkdir(exist_ok=True)
    (ROOT / "step").mkdir(exist_ok=True)
    asm = cq.Assembly(name="AN-ASM-000-rA_agronova_master")
    fr = frame()
    cq.exporters.export(fr, str(ROOT / "step" / "AN-MECH-001-rA_frame.step"))
    asm.add(fr, name="frame")
    for name, fn in PRINTED.items():
        s = fn()
        cq.exporters.export(s, str(ROOT / "stl" / f"{name}.stl"), tolerance=0.05, angularTolerance=0.2)
        cq.exporters.export(s, str(ROOT / "step" / f"{name}.step"))
    asm.add(cover_half(-1), name="cover_left", loc=cq.Location((0, 0, TUBE / 2)))
    asm.add(cover_half(+1), name="cover_right", loc=cq.Location((0, 0, TUBE / 2)))
    asm.add(sensor_bracket(), name="sensor_bracket", loc=cq.Location((FRAME_L / 2 - 40, 0, 60)))
    asm.save(str(ROOT / "step" / "AN-ASM-000-rA_master_assembly.step"))


if __name__ == "__main__":
    build()
