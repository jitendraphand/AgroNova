# Mechanical design
Status: NOT STARTED (architecture proposed only).
- Configuration: 4-wheel skid-steer (SRS A-1). Chassis: aluminium 2020/3030 extrusion frame proposed — **not 3D printed** (structural, outdoor).
- 3D-printed parts (ASA/PETG, not PLA for loaded outdoor parts): sensor brackets, cable guides, covers.
- CAD: FreeCAD (parametric) + OpenSCAD; exports STEP/STL/3MF in `hardware/`.
- Part numbering: `AN-<SUBSYS>-<NNN>-r<REV>` e.g. `AN-MECH-001-rA`.
- Structural calculations (payload, FoS, CoG, tipping on 10° slope): **TBD** — require final dimensions.
