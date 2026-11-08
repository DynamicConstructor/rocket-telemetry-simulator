# Rocket Flight and Telemetry Simulator

**Type:** Newly built educational physics/programming demo. **Not** Alexander's original academic capstone and must not be represented as such.

## Objective
Simulate the vertical flight of a simplified model rocket using small time steps, produce telemetry CSV, and render a standalone SVG altitude chart. Demonstrates Python, numerical modeling, data export, visualization, and unit testing.

## Assumptions and limits

- One-dimensional vertical flight over flat ground
- Constant gravitational acceleration, constant thrust during motor burn
- Fixed initial mass (no changing propellant mass)
- Quadratic air drag in a fixed-density atmosphere
- Explicit Euler integration; illustrative, **not** flight-certified or suitable for actual vehicle engineering

## Run

```bash
python simulate.py --output telemetry.csv --chart altitude.svg
python simulate.py --thrust 55 --mass 1.5 --burn 2.5 --output telemetry-high-thrust.csv --chart high-thrust.svg
python -m unittest discover -s tests -v
```

Open `altitude.svg` in a browser and inspect `telemetry.csv` in a spreadsheet. The program prints flight duration, estimated apogee, and maximum velocity.

## Engineering discussion

The program integrates acceleration into velocity and altitude, stops at ground impact, and records each sample. It separates data generation from export and includes physics sanity checks. Enhancements include variable mass, staging, wind, parameter sweeps, or a graphical control panel.

## Architecture

```mermaid
flowchart LR
  A[Flight parameters] --> B[Forces and acceleration]
  B --> C[Euler integration]
  C --> D[Telemetry samples]
  D --> E[CSV and SVG]
```

## Reproducible simulated result

Default settings produce an approximate **156 m apogee** and **12.7-second flight** in this simplified model. These are numerical simulation outputs, **not measurements from a physical launch**. Use CLI parameters to test how thrust, mass, motor burn, and timestep alter the estimate.

## Evidence checklist

- [ ] Run simulator and save generated CSV/chart screenshots
- [ ] Explain timestep accuracy and limitations of Euler integration
- [ ] Modify a physical parameter and compare apogee
- [ ] Document original contributions and commit them

## Resume use

Describe this as a **personal simulation project** only after Alexander has personally run, understood, and extended it. His original school rocket capstone should be documented separately if original evidence becomes available.

## Portfolio evidence and technical review

- [Cloud validation report](docs/VALIDATION.md) — dated test results and limitations
- [Technical case study](docs/CASE-STUDY.md) — problem, approach, engineering decisions, and next personal contribution

The cloud run was AI-assisted; it does not establish Alexander's independent authorship. GitHub Actions may be unavailable due to an account-level billing restriction. Follow the local commands in the validation report to reproduce results.
