# Case Study: Numerical Rocket Flight and Telemetry

## Problem

Engineering simulations translate physical assumptions into time-series data. The challenge is to integrate acceleration over time, produce interpretable outputs, and communicate limitations of the mathematical model.

## Approach

The Python program simulates one-dimensional vertical flight under thrust, gravity, and velocity-dependent drag. It integrates with a configurable timestep, records altitude and velocity, exports CSV telemetry, and draws an SVG altitude chart.

## Architecture

`User parameters → net forces → Euler integration → telemetry samples → CSV and SVG`

## Engineering decisions

- Dataclass configuration centralizes model parameters.
- Standard-library-only exports make the project easy to run.
- Tests compare higher and lower thrust, reject invalid mass, and exercise file generation.
- Documentation explicitly distinguishes numerical output from measured aerospace data.

## Demonstrated outcome

Five tests passed in the cloud environment. The default parameter set produced a simulated apogee around 156 meters. The model intentionally omits variable propellant mass, staging, wind, and altitude-dependent atmosphere.

## Next personal contribution

Alexander can add a two-configuration overlay graph, parameter sensitivity report, or a more accurate integration method and document the tradeoffs. If he wants to showcase his original college capstone, that must be a separate case study based on the original code and evidence.
