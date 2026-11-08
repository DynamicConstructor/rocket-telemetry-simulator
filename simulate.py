"""Simplified 1D model-rocket telemetry simulation; educational use only."""
import argparse
import csv
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    mass_kg: float = 1.5
    thrust_newtons: float = 45.0
    burn_seconds: float = 2.5
    drag_coefficient: float = 0.55
    area_m2: float = 0.008
    air_density: float = 1.225
    gravity: float = 9.80665
    timestep: float = 0.01
    max_time: float = 120.0


def simulate(config=Config()):
    numeric_values = vars(config).values()
    if not all(math.isfinite(value) for value in numeric_values):
        raise ValueError("Physical parameters must be finite numbers")
    if (config.mass_kg <= 0 or config.timestep <= 0 or config.max_time <= 0 or
            config.area_m2 < 0 or config.drag_coefficient < 0 or
            config.burn_seconds < 0 or config.thrust_newtons < 0):
        raise ValueError("Invalid physical configuration")
    if config.max_time / config.timestep > 1_000_000:
        raise ValueError("Simulation exceeds the one-million-step safety limit")
    t = altitude = velocity = 0.0
    samples = [{"time_s": t, "altitude_m": altitude, "velocity_m_s": velocity}]
    while t < config.max_time:
        thrust = config.thrust_newtons if t < config.burn_seconds else 0.0
        drag = -0.5 * config.air_density * config.drag_coefficient * config.area_m2 * velocity * abs(velocity)
        acceleration = (thrust + drag) / config.mass_kg - config.gravity
        velocity += acceleration * config.timestep
        altitude += velocity * config.timestep
        t += config.timestep
        if altitude <= 0 and t > config.timestep:
            samples.append({"time_s": round(t, 3), "altitude_m": 0.0,
                            "velocity_m_s": round(velocity, 4)})
            break
        samples.append({"time_s": round(t, 3), "altitude_m": round(altitude, 4),
                        "velocity_m_s": round(velocity, 4)})
    return samples


def export_csv(samples, path):
    with open(path, "w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["time_s", "altitude_m", "velocity_m_s"])
        writer.writeheader()
        writer.writerows(samples)


def export_svg(samples, path):
    width, height, margin = 900, 420, 55
    max_time = max(row["time_s"] for row in samples) or 1
    max_alt = max(row["altitude_m"] for row in samples) or 1
    points = " ".join(
        f"{margin + (row['time_s'] / max_time) * (width-2*margin):.1f},"
        f"{height-margin - (row['altitude_m'] / max_alt) * (height-2*margin):.1f}"
        for row in samples
    )
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
           f'<rect width="100%" height="100%" fill="#101a2d"/>'
           f'<text x="55" y="28" fill="white" font-size="22">Rocket altitude vs time</text>'
           f'<path d="M{margin} {margin} V{height-margin} H{width-margin}" fill="none" stroke="#a9bbd5"/>'
           f'<polyline points="{points}" fill="none" stroke="#70e0cb" stroke-width="2.5"/>'
           f'<text x="{width/2}" y="{height-12}" fill="white" text-anchor="middle">Time (s)</text>'
           f'<text x="65" y="48" fill="white">Peak: {max_alt:.1f} m</text>'
           '</svg>')
    with open(path, "w", encoding="utf-8") as stream:
        stream.write(svg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Educational rocket telemetry simulation")
    parser.add_argument("--output", default="telemetry.csv")
    parser.add_argument("--chart", default="altitude.svg")
    parser.add_argument("--thrust", type=float, default=Config.thrust_newtons,
                        help="Constant motor thrust in newtons")
    parser.add_argument("--mass", type=float, default=Config.mass_kg,
                        help="Initial fixed rocket mass in kg")
    parser.add_argument("--burn", type=float, default=Config.burn_seconds,
                        help="Motor burn duration in seconds")
    parser.add_argument("--timestep", type=float, default=Config.timestep,
                        help="Euler integration timestep in seconds")
    args = parser.parse_args()
    try:
        config = Config(thrust_newtons=args.thrust, mass_kg=args.mass,
                        burn_seconds=args.burn, timestep=args.timestep)
        flight = simulate(config)
    except ValueError as exc:
        parser.error(str(exc))
    export_csv(flight, args.output)
    export_svg(flight, args.chart)
    print(f"Duration: {flight[-1]['time_s']:.2f} s")
    print(f"Peak altitude: {max(s['altitude_m'] for s in flight):.2f} m")
    print(f"Peak speed: {max(abs(s['velocity_m_s']) for s in flight):.2f} m/s")
    print(f"Saved {args.output} and {args.chart}")
