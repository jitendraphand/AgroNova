#!/usr/bin/env python3
"""Check STL files against the Elegoo Neptune 4 Max usable build envelope.

Nominal 420x420x480 mm; usable envelope assumed 400x400x460 mm (verify on your printer).
Reports, per part: FITS (as-modelled), FITS_IF_REORIENTED (another axis permutation fits),
or NEEDS_SEGMENTATION. Exit code 1 if any part needs segmentation.
"""
from __future__ import annotations

import argparse
import itertools
import pathlib
import sys

USABLE = (400.0, 400.0, 460.0)


def classify(extents, envelope=USABLE):
    ex = tuple(float(e) for e in extents)
    if all(e <= m for e, m in zip(ex, envelope, strict=True)):
        return "FITS"
    if any(all(e <= m for e, m in zip(p, envelope, strict=True)) for p in itertools.permutations(ex)):
        return "FITS_IF_REORIENTED"
    return "NEEDS_SEGMENTATION"


def stl_extents(path):
    from stl import mesh  # numpy-stl

    m = mesh.Mesh.from_file(str(path))
    return tuple((m.max_ - m.min_).tolist())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="hardware/stl")
    a = ap.parse_args(argv)
    files = sorted(pathlib.Path(a.root).rglob("*.stl"))
    if not files:
        print(f"No STL files under {a.root} (no printable parts yet).")
        return 0
    bad = 0
    print("| Part | X | Y | Z | Result |\n|---|---|---|---|---|")
    for f in files:
        ex = stl_extents(f)
        r = classify(ex)
        bad += r == "NEEDS_SEGMENTATION"
        print(f"| {f.name} | {ex[0]:.1f} | {ex[1]:.1f} | {ex[2]:.1f} | {r} |")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
