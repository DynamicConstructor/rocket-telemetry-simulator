"""Compare educational one-dimensional flight scenarios; not flight-certified."""
import argparse
import csv
from dataclasses import replace
from html import escape

from simulate import Config, simulate


def compare_scenarios(base=Config()):
    scenarios = {
        "baseline": base,
        "higher thrust": replace(base, thrust_newtons=base.thrust_newtons * 1.15),
        "higher drag": replace(base, drag_coefficient=base.drag_coefficient * 1.5),
    }
    result = {}
    for name, config in scenarios.items():
        samples = simulate(config)
        result[name] = {
            "config": config,
            "samples": samples,
            "peak_altitude_m": max(row["altitude_m"] for row in samples),
            "peak_speed_m_s": max(abs(row["velocity_m_s"]) for row in samples),
            "flight_time_s": samples[-1]["time_s"],
        }
    return result


def export_summary_csv(result, path):
    with open(path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["scenario", "thrust_n", "drag_coefficient", "peak_altitude_m", "peak_speed_m_s", "flight_time_s"])
        for name, data in result.items():
            writer.writerow([name, data["config"].thrust_newtons, data["config"].drag_coefficient,
                             data["peak_altitude_m"], data["peak_speed_m_s"], data["flight_time_s"]])


def export_comparison_svg(result, path):
    width, height, margin = 960, 480, 65
    max_t = max(row["time_s"] for data in result.values() for row in data["samples"]) or 1
    max_h = max(data["peak_altitude_m"] for data in result.values()) or 1
    colors = ["#5eead4", "#fbbf24", "#c4b5fd"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#101827"/>',
             '<text x="65" y="30" fill="white" font-size="22">Altitude vs time — scenario comparison</text>',
             f'<path d="M{margin} {margin} V{height-margin} H{width-margin}" stroke="#a9bbd5" fill="none"/>']
    for i, (name, data) in enumerate(result.items()):
        points = " ".join(f'{margin + row["time_s"] / max_t * (width-2*margin):.1f},'
                          f'{height-margin-row["altitude_m"] / max_h * (height-2*margin):.1f}'
                          for row in data["samples"])
        color = colors[i % len(colors)]
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.3"/>')
        parts.append(f'<text x="{width-270}" y="{65+25*i}" fill="{color}" font-size="16">'
                     f'{escape(name)}: {data["peak_altitude_m"]:.1f} m</text>')
    parts.append(f'<text x="{width/2}" y="{height-15}" fill="white" text-anchor="middle">Time (seconds)</text>')
    parts.append('</svg>')
    with open(path, "w", encoding="utf-8") as stream:
        stream.write("".join(parts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", default="scenario-summary.csv")
    parser.add_argument("--chart", default="scenario-comparison.svg")
    args = parser.parse_args()
    results = compare_scenarios()
    export_summary_csv(results, args.summary)
    export_comparison_svg(results, args.chart)
    for name, data in results.items():
        print(f'{name}: peak={data["peak_altitude_m"]:.1f}m, flight={data["flight_time_s"]:.2f}s')
    print(f"Saved {args.summary} and {args.chart}")
