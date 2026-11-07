"""Static checks of ROS 2 config/launch/URDF files (no ROS install required)."""
import ast
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml

SRC = Path(__file__).resolve().parents[1] / "ros2_ws" / "src"


@pytest.mark.parametrize("p", sorted(SRC.rglob("*.yaml")), ids=lambda p: p.name)
def test_yaml_parses(p):
    assert yaml.safe_load(p.read_text()) is not None


@pytest.mark.parametrize("p", sorted(SRC.rglob("*.launch.py")), ids=lambda p: p.name)
def test_launch_defines_generator(p):
    tree = ast.parse(p.read_text())
    assert any(isinstance(n, ast.FunctionDef) and n.name == "generate_launch_description" for n in tree.body)


@pytest.mark.parametrize("p", sorted(SRC.rglob("package.xml")), ids=lambda p: p.parent.name)
def test_package_xml(p):
    root = ET.parse(p).getroot()
    assert root.find("name").text == p.parent.name and root.find("license").text == "MIT"


@pytest.mark.parametrize("world", ["cotton_field.sdf", "cotton_field_capture.sdf"])
def test_world_sdf_parses(world):
    root = ET.parse(SRC / "agronova_gazebo" / "worlds" / world).getroot()
    assert len([m for m in root.iter("model") if m.get("name").startswith("plant_")]) > 0


def test_ekf_matrices_have_15_entries():
    cfg = yaml.safe_load((SRC / "agronova_navigation" / "config" / "ekf.yaml").read_text())
    for node in cfg.values():
        for k, v in node["ros__parameters"].items():
            if k.endswith("_config"):
                assert len(v) == 15, k


@pytest.mark.parametrize("sim", ["false", "true"])
def test_xacro_expands(sim, tmp_path):
    xacro = pytest.importorskip("xacro")
    # $(find ...) needs ROS; emulate by substituting the include path
    src = (SRC / "agronova_description" / "urdf" / "agronova.urdf.xacro").read_text()
    src = src.replace("$(find agronova_description)", str(SRC / "agronova_description"))
    f = tmp_path / "r.xacro"
    f.write_text(src)
    out = xacro.process_file(str(f), mappings={"sim": sim}).toxml()
    root = ET.fromstring(out)
    assert len(root.findall("joint")) >= 5
    assert (root.find(".//plugin") is not None) == (sim == "true")
