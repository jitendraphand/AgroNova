#!/usr/bin/env python3
"""Generate a cotton-field SDF world: N crop rows at 0.90 m spacing (SRS A-0) of simple plant cylinders."""
import argparse

HEADER = """<?xml version="1.0"?>
<sdf version="1.9">
<world name="cotton_field">
  <physics name="1ms" type="ignored"><max_step_size>0.001</max_step_size><real_time_factor>1</real_time_factor></physics>
  <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
  <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
  <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
  <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors"><render_engine>ogre2</render_engine></plugin>
  <plugin filename="gz-sim-imu-system" name="gz::sim::systems::Imu"/>
  <plugin filename="gz-sim-navsat-system" name="gz::sim::systems::NavSat"/>
  <!-- Approx. location in Vidarbha, Maharashtra (illustrative only) -->
  <spherical_coordinates><surface_model>EARTH_WGS84</surface_model><world_frame_orientation>ENU</world_frame_orientation>
    <latitude_deg>20.7</latitude_deg><longitude_deg>77.0</longitude_deg><elevation>300</elevation></spherical_coordinates>
  <light type="directional" name="sun"><cast_shadows>true</cast_shadows><pose>0 0 10 0 0 0</pose>
    <diffuse>1 1 1 1</diffuse><direction>-0.5 0.1 -0.9</direction></light>
  <model name="ground"><static>true</static><link name="l">
    <collision name="c"><geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
      <surface><friction><ode><mu>0.6</mu><mu2>0.6</mu2></ode></friction></surface></collision>
    <visual name="v"><geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
      <material><ambient>0.25 0.2 0.15 1</ambient><diffuse>0.3 0.24 0.18 1</diffuse></material></visual></link></model>
"""
PLANT = """  <model name="plant_{r}_{k}"><static>true</static><pose>{x:.2f} {y:.2f} 0.3 0 0 0</pose><link name="l">
    <collision name="c"><geometry><cylinder><radius>0.08</radius><length>0.6</length></cylinder></geometry></collision>
    <visual name="v"><geometry><cylinder><radius>0.08</radius><length>0.6</length></cylinder></geometry>
      <material><diffuse>0.1 0.6 0.1 1</diffuse></material></visual></link></model>
"""


def make(rows=4, length=10.0, spacing=0.90, plant_gap=0.5):
    out = [HEADER]
    for r in range(rows):
        y = (r - (rows - 1) / 2) * spacing
        for k in range(int(length / plant_gap) + 1):
            out.append(PLANT.format(r=r, k=k, x=2.0 + k * plant_gap, y=y))
    out.append("</world>\n</sdf>\n")
    return "".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=4)
    ap.add_argument("-o", default="worlds/cotton_field.sdf")
    a = ap.parse_args()
    open(a.o, "w").write(make(a.rows))
