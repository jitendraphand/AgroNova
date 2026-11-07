#!/usr/bin/env python3
"""Regenerate AgroNova visuals into docs/media/ (no ROS/Gazebo required).

Outputs (tool that produced each):
  cad_assembly.png        CadQuery geometry (hardware/cad/cadquery) tessellated, drawn with matplotlib 3D
  urdf_in_field.png       URDF expanded by xacro (sim:=false), primitives drawn with matplotlib 3D, rows per A-0
  kinematic_sim.gif       2D kinematic simulation with agronova_kinematics.diff_drive + simulated 2D lidar
  kinematic_sim_final.png last frame of the same simulation
This is a KINEMATIC simulation (no dynamics, no slip, ideal sensors). It is NOT Gazebo.
"""
from __future__ import annotations

import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import animation  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ros2_ws" / "src" / "agronova_kinematics"))
from agronova_kinematics.diff_drive import DiffDriveParams, forward, integrate_odometry, inverse  # noqa: E402

MEDIA = ROOT / "docs" / "media"
ROW_SPACING = 0.90  # SRS A-0
PARAMS = DiffDriveParams(0.15, 0.50, 1.0)
LABEL = "Kinematic simulation (Python, agronova_kinematics) — NOT Gazebo"


# ---------------------------------------------------------------- field / lidar model
def plants(rows=4, length=10.0, gap=0.5, x0=2.0):
    pts = []
    for r in range(rows):
        y = (r - (rows - 1) / 2) * ROW_SPACING
        pts += [(x0 + k * gap, y) for k in range(int(length / gap) + 1)]
    return np.array(pts)


def lidar_scan(pose, obstacles, radius=0.08, n=180, rmax=6.0):
    """Ray-cast against circular obstacles. Returns (angles_world, ranges)."""
    x, y, th = pose
    ang = th + np.linspace(-math.pi, math.pi, n, endpoint=False)
    d = np.stack([np.cos(ang), np.sin(ang)], 1)
    rel = obstacles[:, :2] - np.array([x, y])
    rad = obstacles[:, 2] if obstacles.shape[1] > 2 else np.full(len(obstacles), radius)
    proj = d @ rel.T  # (n, m)
    perp2 = (rel**2).sum(1)[None, :] - proj**2
    hit = (proj > 0) & (perp2 <= rad[None, :] ** 2)
    t = proj - np.sqrt(np.clip(rad[None, :] ** 2 - perp2, 0, None))
    t = np.where(hit, t, np.inf).min(1)
    return ang, np.minimum(t, rmax)


def run_sim(dt=0.05, t_end=14.0, person_xy=(9.0, 0.0), stop_dist=0.6):
    """Drive down the inter-row lane y=0 (rows at +-0.45 m); a person stands in the lane; stop zone 0.6 m (nav2 config)."""
    field = plants()
    obs = np.column_stack([field, np.full(len(field), 0.08)])
    person = np.array([[*person_xy, 0.25]])
    lane_y = 0.0  # centre of the inter-row lane between rows at y=+-0.45 m
    pose = (0.0, lane_y + 0.15, 0.1)  # start slightly off-lane to show convergence
    frames = []
    for k in range(int(t_end / dt)):
        t = k * dt
        all_obs = np.vstack([obs, person]) if t > 4.0 else obs
        ang, rng = lidar_scan(pose, all_obs)
        # Stop zone: front rectangle 0.6 m ahead, +/-0.4 m wide (collision_monitor StopZone)
        rel = ang - pose[2]
        lx, ly = rng * np.cos(rel), rng * np.sin(rel)
        stop = bool(np.any((lx > 0) & (lx < stop_dist) & (np.abs(ly) < 0.30) & (rng < 6.0)))
        # simple lane-keeping law (illustrative, not the Nav2 controller)
        v = 0.0 if stop else 0.6
        omega = 0.0 if stop else float(np.clip(-2.0 * (pose[1] - lane_y) - 2.5 * math.sin(pose[2]), -1, 1))
        wl, wr = inverse(v, omega, PARAMS)
        v_m, w_m = forward(wl, wr, PARAMS)
        pose = integrate_odometry(*pose, v_m, w_m, dt)
        frames.append({"t": t, "pose": pose, "ang": ang, "rng": rng, "stop": stop, "person": t > 4.0,
                       "wl": wl, "wr": wr})
    return field, person[0], frames


# ---------------------------------------------------------------- drawings
def _robot_poly(pose, length=0.70, width=0.62):
    x, y, th = pose
    c = np.array([[length / 2, width / 2], [length / 2, -width / 2], [-length / 2, -width / 2], [-length / 2, width / 2]])
    rot = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    return c @ rot.T + [x, y]


def make_animation(out_gif, out_png, every=4):
    field, person, frames = run_sim()
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=90)
    trace = np.array([f["pose"][:2] for f in frames])

    def draw(i):
        f = frames[i]
        ax.clear()
        ax.set_xlim(-0.8, 12.5)
        ax.set_ylim(-1.9, 1.9)
        ax.set_aspect("equal")
        ax.set_facecolor("#5a4632")
        ax.scatter(field[:, 0], field[:, 1], s=60, c="#2e8b2e", edgecolors="#1b5e1b", label="cotton plants (rows 0.90 m)")
        if f["person"]:
            ax.add_patch(plt.Circle(person[:2], person[2], color="orange", label="person (appears t>4 s)"))
        x, y, th = f["pose"]
        pts = np.column_stack([x + f["rng"] * np.cos(f["ang"]), y + f["rng"] * np.sin(f["ang"])])
        hit = f["rng"] < 6.0
        ax.scatter(pts[hit, 0], pts[hit, 1], s=6, c="red", label="simulated 2D lidar hits")
        ax.plot(trace[: i + 1, 0], trace[: i + 1, 1], "c-", lw=1.5, label="odometry trace")
        ax.add_patch(plt.Polygon(_robot_poly(f["pose"]), color="#d0d0d0", ec="k"))
        sz = np.array([[0, 0.3], [0.6, 0.3], [0.6, -0.3], [0, -0.3]])
        rot = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        ax.add_patch(plt.Polygon(sz @ rot.T + [x + 0.35 * math.cos(th), y + 0.35 * math.sin(th)], fill=False,
                                 ec="red" if f["stop"] else "yellow", lw=1.5, ls="--"))
        state = "STOP (obstacle in stop zone)" if f["stop"] else "driving 0.6 m/s"
        ax.set_title(f"t={f['t']:.1f}s  {state}  wheels L={f['wl']:.2f} R={f['wr']:.2f} rad/s", fontsize=9)
        ax.text(0.01, 0.01, LABEL, transform=ax.transAxes, fontsize=7, color="white")
        ax.legend(loc="upper left", fontsize=6, ncol=2)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")

    idx = list(range(0, len(frames), every))
    anim = animation.FuncAnimation(fig, draw, frames=idx)
    anim.save(out_gif, writer=animation.PillowWriter(fps=10))
    draw(len(frames) - 1)
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)
    return frames


def _box(c, s):
    x, y, z = c
    dx, dy, dz = (v / 2 for v in s)
    v = np.array([[x + i * dx, y + j * dy, z + k * dz] for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)])
    f = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
    return [v[q] for q in f]


def _cyl_y(c, r, length, n=24):
    x, y, z = c
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ring = lambda yy: np.column_stack([x + r * np.cos(a), np.full(n, yy), z + r * np.sin(a)])  # noqa: E731
    p, q = ring(y - length / 2), ring(y + length / 2)
    faces = [p, q] + [np.array([p[i], p[(i + 1) % n], q[(i + 1) % n], q[i]]) for i in range(n)]
    return faces


def urdf_primitives():
    import xacro

    src = (ROOT / "ros2_ws/src/agronova_description/urdf/agronova.urdf.xacro").read_text()
    src = src.replace("$(find agronova_description)", str(ROOT / "ros2_ws/src/agronova_description"))
    tmp = MEDIA / "_tmp.xacro"
    tmp.write_text(src)
    root = ET.fromstring(xacro.process_file(str(tmp), mappings={"sim": "false"}).toxml())
    tmp.unlink()
    joints = {j.find("child").get("link"): j for j in root.findall("joint")}

    def origin(link):
        xyz = np.zeros(3)
        while link in joints:
            o = joints[link].find("origin")
            if o is not None:
                xyz += np.array([float(v) for v in o.get("xyz", "0 0 0").split()])
            link = joints[link].find("parent").get("link")
        return xyz

    prims = []
    for link in root.findall("link"):
        g = link.find("visual/geometry")
        if g is None:
            continue
        o = origin(link.get("name"))
        if g.find("box") is not None:
            prims.append(("box", o, [float(v) for v in g.find("box").get("size").split()]))
        elif g.find("cylinder") is not None:
            c = g.find("cylinder")
            prims.append(("wheel", o, (float(c.get("radius")), float(c.get("length")))))
    return prims


def render_urdf(out):
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(projection="3d")
    for kind, o, s in urdf_primitives():
        faces = _box(o, s) if kind == "box" else _cyl_y(o, *s)
        ax.add_collection3d(Poly3DCollection(faces, facecolor="#b0b8c0" if kind == "box" else "#222", edgecolor="k",
                                             lw=0.2, alpha=0.95))
    for x, y in plants(rows=4, length=3.0, x0=-1.5):
        ax.add_collection3d(Poly3DCollection(_box((x, y + 0.0, 0.3), (0.12, 0.12, 0.6)), facecolor="#2e8b2e", lw=0))
    ax.add_collection3d(Poly3DCollection([np.array([[-2, -2, 0], [2, -2, 0], [2, 2, 0], [-2, 2, 0]])],
                                         facecolor="#6b5340", alpha=0.6))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_zlim(0, 1.2)
    ax.set_box_aspect((3.2, 3.2, 1.2))
    ax.view_init(25, -60)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")
    ax.set_title("AgroNova URDF (xacro-expanded) between 0.90 m cotton rows\nmatplotlib 3D render of URDF primitives — "
                 "NOT Gazebo", fontsize=9)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def render_cad(out):
    sys.path.insert(0, str(ROOT / "hardware/cad/cadquery"))
    import agronova_parts as p

    parts = [(p.frame(), (0, 0, 0), "#7a7f85")]
    parts += [(p.cover_half(-1), (0, 0, p.TUBE / 2), "#d9c27a"), (p.cover_half(1), (0, 0, p.TUBE / 2), "#c9b26a")]
    parts += [(p.sensor_bracket(), (p.FRAME_L / 2 - 40, 0, 60), "#3a6ea5")]
    parts += [(p.estop_housing(), (-p.FRAME_L / 2 + 60, 120, p.TUBE / 2 + p.COVER_H + 25), "#c0392b")]
    fig = plt.figure(figsize=(9, 6), dpi=100)
    ax = fig.add_subplot(projection="3d")
    for shape, off, col in parts:
        verts, tris = shape.val().tessellate(0.5, 0.3)
        v = np.array([[q.x, q.y, q.z] for q in verts]) + off
        ax.add_collection3d(Poly3DCollection(v[np.array(tris)], facecolor=col, edgecolor="none", alpha=0.9))
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    ax.set_zlim(-100, 200)
    ax.set_box_aspect((8, 8, 3))
    ax.view_init(30, -55)
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.set_title("CadQuery draft assembly: steel frame, split ASA cover, sensor bracket, E-stop housing\n"
                 "(wheels/motors not yet modelled; E-stop housing position illustrative)", fontsize=9)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


def main():
    MEDIA.mkdir(parents=True, exist_ok=True)
    make_animation(MEDIA / "kinematic_sim.gif", MEDIA / "kinematic_sim_final.png")
    render_urdf(MEDIA / "urdf_in_field.png")
    try:
        render_cad(MEDIA / "cad_assembly.png")
    except ImportError:
        print("cadquery not installed: skipped cad_assembly.png")


if __name__ == "__main__":
    main()
