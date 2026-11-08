# Demonstration Evidence — Educational Rocket Simulator

**Scope:** Simplified numerical outputs, not flight telemetry from a physical launch and not the original academic capstone.

```bash
python simulate.py --output telemetry.csv --chart altitude.svg
python compare_flights.py --summary scenario-summary.csv --chart scenario-comparison.svg
python -m unittest discover -s tests -v
```

Cloud run, November 8, 2026: baseline peak **156.4 m** with **12.70 s** simulated flight; 15% higher thrust peak **203.6 m** with **14.29 s**; 50% higher drag peak **144.1 m** with **12.27 s**. These values follow the configured simplified Euler model, not physical test results. **12 cloud tests passed.**

Open the SVG charts and CSV summary. Alexander should save authentic screenshots and explain his own modification, as well as the limitations of fixed mass and constant air density.
