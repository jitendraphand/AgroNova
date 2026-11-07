#!/usr/bin/env python3
"""Turn raw Gazebo/RViz captures (from tools/capture_gazebo.sh) into docs/media GIFs + plots.

Inputs:  docs/media/gazebo/{overview,top}_*.png, run_log.npz ; docs/media/rviz/rviz_*.png
Outputs: docs/media/gazebo_overview.gif, gazebo_top.gif, rviz.gif, gazebo_odom_scan.png
Raw frames are reduced to a few stills afterwards (--prune) to keep the repo small.
"""
import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

MEDIA = Path(__file__).resolve().parents[1] / "docs" / "media"
KEEP = {"overview_00_start.png", "overview_08.png", "overview_99_end.png", "top_99_end.png", "rviz_6.png",
        "run_log.npz"}


def gif(frames, out, width=640, ms=250):
    imgs = [Image.open(f).convert("RGB") for f in frames]
    imgs = [i.resize((width, int(i.height * width / i.width))) for i in imgs]
    imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=ms, loop=0, optimize=True)


def odom_plot(log, out):
    d = np.load(log)
    od = d["odom"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4), dpi=100)
    a1.plot(od[:, 1], od[:, 2], "b-")
    a1.set_title("Gazebo /wheel/odom trace (DiffDrive plugin)")
    a1.set_xlabel("x [m]")
    a1.set_ylabel("y [m]")
    a1.axis("equal")
    a1.grid(True)
    r = d["scan_ranges"]
    if r.size:
        ang = d["scan_angle_min"] + d["scan_angle_inc"] * np.arange(r.size)
        ok = np.isfinite(r)
        a2.scatter(r[ok] * np.cos(ang[ok]), r[ok] * np.sin(ang[ok]), s=4, c="r")
        a2.add_patch(plt.Rectangle((-0.35, -0.31), 0.7, 0.62, fill=False))
        a2.set_title("Last Gazebo /scan in robot frame (gpu_lidar)")
        a2.axis("equal")
        a2.grid(True)
        a2.set_xlabel("x [m]")
        a2.set_ylabel("y [m]")
    fig.suptitle("Data recorded from a real Gazebo Harmonic run; plotted with matplotlib", fontsize=9)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    dist = float(np.sum(np.hypot(np.diff(od[:, 1]), np.diff(od[:, 2]))))
    return dist, float(od[-1, 2]), math.degrees(float(od[-1, 3]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true")
    a = ap.parse_args()
    g, rv = MEDIA / "gazebo", MEDIA / "rviz"
    gif(sorted(g.glob("overview_*.png")), MEDIA / "gazebo_overview.gif")
    gif(sorted(g.glob("top_*.png")), MEDIA / "gazebo_top.gif")
    if list(rv.glob("rviz_*.png")):
        gif(sorted(rv.glob("rviz_*.png")), MEDIA / "rviz.gif", ms=400)
    print("odom: distance %.2f m, final y %.3f m, final yaw %.2f deg" % odom_plot(g / "run_log.npz",
                                                                                  MEDIA / "gazebo_odom_scan.png"))
    if a.prune:
        for f in list(g.iterdir()) + list(rv.iterdir()):
            if f.name not in KEEP:
                f.unlink()


if __name__ == "__main__":
    main()
