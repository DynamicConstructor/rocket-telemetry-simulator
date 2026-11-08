# Cloud Validation — November 8, 2026

**Execution:** ChatGPT-managed Linux environment, Python 3.12.14. AI-assisted cloud testing; not Alexander's original academic capstone.

## Reproduce

```bash
python -m unittest discover -s tests -v
python simulate.py --output telemetry.csv --chart altitude.svg
```

**Result:** 5/5 unit tests passed; telemetry CSV and SVG chart were generated successfully.

Default simplified flight outputs in the verification environment were approximately **12.70 seconds**, **156.42 meters peak altitude**, and **48.43 m/s peak speed**. These are simulated values, **not physical launch measurements**.

## Coverage and limitations

Tests cover rising/landing behavior, thrust comparison, invalid mass, timestep sensitivity, and file export. The model assumes one-dimensional flight, fixed mass and atmospheric density, constant burn thrust, simple quadratic drag, and explicit Euler integration. It is not suitable for flight-critical calculations.

## Personal verification still required

- [ ] Alexander runs the simulation independently
- [ ] Alexander compares at least two configurations and explains why outputs change
- [ ] Save real screenshots of generated telemetry/chart
- [ ] Alexander contributes a personally understood model or interface improvement
