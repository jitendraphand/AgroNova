"""Every committed STL must fit the Neptune 4 Max usable envelope; regenerate check if CadQuery present."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_printability import classify, stl_extents  # noqa: E402

STLS = sorted((ROOT / "hardware" / "stl").glob("*.stl"))


def test_stls_exist():
    assert STLS, "no STL files committed"


@pytest.mark.parametrize("path", STLS, ids=lambda p: p.name)
def test_stl_fits_as_modelled(path):
    assert classify(stl_extents(path)) == "FITS"


@pytest.mark.parametrize("path", STLS, ids=lambda p: p.name)
def test_part_number_naming(path):
    assert path.name.startswith("AN-PRT-") and "-r" in path.name


@pytest.mark.skipif(importlib.util.find_spec("cadquery") is None, reason="cadquery not installed")
def test_cad_parts_are_valid_solids():
    sys.path.insert(0, str(ROOT / "hardware" / "cad" / "cadquery"))
    import agronova_parts as p

    for fn in p.PRINTED.values():
        assert fn().val().isValid()
    assert p.frame().val().isValid()
