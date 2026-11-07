# Mechanical design (r0.2 — first design draft, NOT fabricated)

## Architecture (SRS A-0, A-1, A-7)
| Item | Decision | Reason |
|---|---|---|
| Configuration | 4-wheel skid-steer, 4 independent gearmotors | Few moving parts, no steering linkage, repairable by local workshops |
| Frame AN-MECH-001 | Welded ladder frame, 25×25×1.5 mm mild-steel square tube (IS 2062 E250), 700×450 mm | Cheap, weldable anywhere in rural India; FoS 3.27 on rail (see `docs/calculations/RESULTS.md`) — **not 3D printed** |
| Wheels | 300 mm dia. (r = 0.15 m), ≥ 80 mm wide lugged tyre | Black cotton soil sinks/clogs; larger wheels reduce sinkage (model TBD) |
| Ground clearance | ≥ 250 mm target (TBD from motor mount geometry) | Clears young cotton/weeds |
| Covers / brackets | 3D-printed ASA (UV, 45 °C ambient) | PLA rejected: creeps above ~50 °C in sun |
| Electronics | Commercial IP65 ABS/polycarbonate enclosure (size TBD) inside frame | Printed enclosures cannot be relied on for IP65 |
| Tool interface | 2× 25 mm tube rear hitch with M8 bolt pattern 100 mm (draft) | Simple, swappable weeding tine bar |

## Alternatives evaluated
- **Tracks:** better flotation on wet vertisol but higher rolling loss, more wear parts, costlier → rejected for baseline.
- **Ackermann:** needs steering actuator; larger turning radius at headlands → rejected.
- **Aluminium extrusion frame:** lighter, bolt-together, but costlier and less locally repairable → alternative.

## CAD
Source: `hardware/cad/cadquery/agronova_parts.py` (CadQuery 2.x, fully parametric). Run `python hardware/cad/cadquery/agronova_parts.py` to regenerate:
- STEP: `hardware/step/` — frame, every printed part, `AN-ASM-000-rA_master_assembly.step` (frame + covers + sensor bracket; wheels/motors not yet modelled).
- STL: `hardware/stl/` — printed parts only.

Segmentation example: the 700×390 mm top cover exceeds the 400 mm usable bed, so it is split into AN-PRT-004 / AN-PRT-005 with a tongue-and-groove seam (0.4 mm clearance) and 3 bolted M5 tabs — no adhesive structural joint.

## Open items
Motor mounts, wheel hubs/shaft & bearings (await motor selection), dimensioned drawings (DXF/PDF), exploded views, fastener schedule, tolerance study, FEA. Mass roll-up from CAD to replace assumption A-9.
