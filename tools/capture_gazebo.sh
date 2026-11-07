#!/usr/bin/env bash
# Run the real Gazebo Harmonic + ROS 2 Jazzy sim headless, drive the robot, capture Gazebo camera frames,
# RViz2 screenshots (Xvfb + ffmpeg x11grab) and odom/scan logs; then build GIFs.
# Environment: RoboStack via pixi (tools/ros_env/pixi.toml):  pixi install --manifest-path tools/ros_env/pixi.toml
# Needs on host: Xvfb, ffmpeg (with x11grab).   Usage: tools/capture_gazebo.sh
set -euo pipefail
REPO=$(cd "$(dirname "$0")/.." && pwd)
PIXI="pixi run --manifest-path $REPO/tools/ros_env/pixi.toml"
mkdir -p "$REPO/docs/media/gazebo" "$REPO/docs/media/rviz"
cd "$REPO/ros2_ws"
$PIXI colcon build --symlink-install
$PIXI bash -c '
source install/setup.bash
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-43}
Xvfb :99 -screen 0 1280x720x24 >/dev/null 2>&1 & XV=$!
ros2 launch agronova_gazebo sim.launch.py world:=cotton_field_capture.sdf headless:=true > /tmp/agronova_sim.log 2>&1 & LP=$!
ros2 launch agronova_navigation localization.launch.py > /tmp/agronova_loc.log 2>&1 & LL=$!
sleep 20
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 rviz2 -d install/agronova_description/share/agronova_description/rviz/agronova_sim.rviz > /tmp/agronova_rviz.log 2>&1 & RV=$!
sleep 12
(for i in $(seq 1 8); do sleep 2; /usr/bin/ffmpeg -loglevel error -y -f x11grab -video_size 1280x720 -i :99 -frames:v 1 '"$REPO"'/docs/media/rviz/rviz_$i.png; done) &
python3 '"$REPO"'/tools/gazebo_capture.py --out '"$REPO"'/docs/media/gazebo --seconds 16
sleep 2
kill $RV || true; kill -INT $LP $LL || true; sleep 5
pkill -f "gz sim" || true; pkill -f parameter_bridge || true; pkill -f ekf_node || true; pkill -f navsat || true; kill $XV || true
'
$PIXI python3 "$REPO/tools/make_sim_media.py" --prune
