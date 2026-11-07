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


CAMERAS = """  <model name="overview_cam"><static>true</static><pose>-2.5 -4.0 2.6 0 0.33 0.62</pose><link name="l">
    <sensor name="overview_camera" type="camera"><always_on>1</always_on><update_rate>5</update_rate>
      <topic>overview_camera</topic><camera><horizontal_fov>1.2</horizontal_fov>
      <image><width>1280</width><height>720</height></image><clip><near>0.1</near><far>100</far></clip></camera>
    </sensor></link></model>
  <model name="top_cam"><static>true</static><pose>6.0 0 14.0 0 1.5707 0</pose><link name="l">
    <sensor name="top_camera" type="camera"><always_on>1</always_on><update_rate>5</update_rate>
      <topic>top_camera</topic><camera><horizontal_fov>1.0</horizontal_fov>
      <image><width>1280</width><height>720</height></image><clip><near>0.1</near><far>100</far></clip></camera>
    </sensor></link></model>
"""


def make(rows=4, length=10.0, spacing=0.90, plant_gap=0.5, cameras=False):
    out = [HEADER]
    if cameras:  # static capture cameras used only for documentation screenshots
        out.append(CAMERAS)
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
    ap.add_argument("--cameras", action="store_true", help="add overview/top capture cameras")
    a = ap.parse_args()
    open(a.o, "w").write(make(a.rows, cameras=a.cameras))
