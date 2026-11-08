# Case Study: Numerical Rocket Flight and Telemetry

## Problem

Engineering simulations translate physical assumptions into time-series data. The challenge is to integrate acceleration over time, produce interpretable outputs, and communicate limitations of the mathematical model.

## Approach

The Python program simulates one-dimensional vertical flight under thrust, gravity, and velocity-dependent drag. It integrates with a configurable timestep, records altitude and velocity, exports CSV telemetry, and draws SVG charts. The comparison script runs baseline, 15% increased thrust, and 50% increased drag scenarios.

## Architecture

`User parameters → net forces → Euler integration → telemetry samples → CSV and SVG`

## Engineering decisions

- Dataclass configuration centralizes model parameters.
- Standard-library-only exports make the project easy to run.
- Tests compare higher and lower thrust, reject invalid mass, and exercise file generation.
- Documentation explicitly distinguishes numerical output from measured aerospace data.

## Demonstrated outcome

Twelve tests passed in the latest cloud environment. The baseline simulated apogee was approximately **156.4 m**, higher-thrust **203.6 m**, and higher-drag **144.1 m**. These are calculated, not physical flight measurements. Invalid non-finite parameters and excessive integration-step counts are rejected. The model omits variable propellant mass, staging, wind, and altitude-dependent atmosphere.

## Next personal contribution

Alexander can add a fourth independently chosen scenario and quantify how the numerical outcome changes. His original college capstone must remain a separate case study based on authentic original code and evidence.
