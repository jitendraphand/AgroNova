import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_printability import classify, main  # noqa: E402


def test_fits():
    assert classify((100, 100, 100)) == "FITS"


def test_reorient():
    assert classify((450, 100, 100)) == "FITS_IF_REORIENTED"


def test_segmentation():
    assert classify((500, 500, 500)) == "NEEDS_SEGMENTATION"


def test_empty_dir(tmp_path):
    assert main([str(tmp_path)]) == 0


def test_real_stl(tmp_path):
    import numpy as np
    from stl import mesh

    m = mesh.Mesh(np.zeros(1, dtype=mesh.Mesh.dtype))
    m.vectors[0] = [[0, 0, 0], [500, 0, 0], [0, 500, 500]]
    m.save(str(tmp_path / "big.stl"))
    assert main([str(tmp_path)]) == 1
