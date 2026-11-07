# Contributing to AgroNova
1. Open an issue using the matching template (bug, mechanical, electrical, software, feature, manufacturing).
2. Branch from `main`, keep commits logically separated, use semantic versioning for releases.
3. Run `pytest -q` and `ruff check .` before opening a PR; fill in the PR template (design impact, test evidence, safety impact).
4. Never mark a test PASSED without recorded evidence; distinguish simulated vs. physical validation.
5. Use SI units and part numbers `AN-<SUBSYS>-<NNN>-r<REV>`. Do not invent component specifications — cite datasheets.
