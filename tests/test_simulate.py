import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulate import Config, simulate, export_csv, export_svg


class RocketTests(unittest.TestCase):
    def test_flight_rises_and_lands(self):
        samples = simulate()
        self.assertGreater(max(point["altitude_m"] for point in samples), 0)
        self.assertEqual(samples[-1]["altitude_m"], 0)

    def test_more_thrust_increases_apogee(self):
        low = max(point["altitude_m"] for point in simulate(Config(thrust_newtons=35)))
        high = max(point["altitude_m"] for point in simulate(Config(thrust_newtons=55)))
        self.assertGreater(high, low)

    def test_invalid_mass_rejected(self):
        with self.assertRaises(ValueError):
            simulate(Config(mass_kg=0))

    def test_nonfinite_input_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            simulate(Config(thrust_newtons=float("nan")))

    def test_step_limit_rejected(self):
        with self.assertRaisesRegex(ValueError, "step"):
            simulate(Config(timestep=0.000001, max_time=120))

    def test_larger_timestep_changes_numerical_estimate(self):
        fine = max(row["altitude_m"] for row in simulate(Config(timestep=0.005)))
        coarse = max(row["altitude_m"] for row in simulate(Config(timestep=0.05)))
        self.assertNotEqual(fine, coarse)

    def test_exports_files(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            csv_path = Path(directory) / "telemetry.csv"
            svg_path = Path(directory) / "altitude.svg"
            data = simulate()
            export_csv(data, csv_path)
            export_svg(data, svg_path)
            self.assertIn("time_s,altitude_m,velocity_m_s", csv_path.read_text())
            self.assertIn("<polyline", svg_path.read_text())


if __name__ == "__main__":
    unittest.main()
