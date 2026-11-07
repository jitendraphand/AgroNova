"""Compile and run firmware host unit tests (PID) with any available C++ compiler."""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FW = Path(__file__).resolve().parents[1] / "firmware" / "motor_controller"


def _compiler():
    for c in ("g++", "clang++", "c++"):
        if shutil.which(c):
            return [c]
    if importlib.util.find_spec("ziglang"):
        return [sys.executable, "-m", "ziglang", "c++"]
    return None


@pytest.mark.skipif(_compiler() is None, reason="no C++ compiler")
def test_pid_host(tmp_path):
    exe = tmp_path / "test_pid"
    subprocess.run([*_compiler(), "-std=c++17", "-Wall", "-Wextra", "-Werror", "-o", str(exe),
                    str(FW / "test_host" / "test_pid.cpp")], check=True)
    out = subprocess.run([str(exe)], check=True, capture_output=True, text=True).stdout
    assert "PID host tests passed" in out
