"""Regression tests for educational scenario comparison."""
import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from compare_flights import compare_scenarios, export_comparison_svg, export_summary_csv


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.result = compare_scenarios()

    def test_three_scenarios(self):
        self.assertEqual(list(self.result), ["baseline", "higher thrust", "higher drag"])

    def test_thrust_increases_peak_altitude(self):
        self.assertGreater(self.result["higher thrust"]["peak_altitude_m"],
                           self.result["baseline"]["peak_altitude_m"])

    def test_drag_reduces_peak_altitude(self):
        self.assertLess(self.result["higher drag"]["peak_altitude_m"],
                        self.result["baseline"]["peak_altitude_m"])

    def test_csv_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "summary.csv")
            export_summary_csv(self.result, path)
            with open(path, newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 3)
            self.assertIn("peak_altitude_m", rows[0])

    def test_svg_chart(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "comparison.svg")
            export_comparison_svg(self.result, path)
            with open(path, encoding="utf-8") as stream:
                chart = stream.read()
            self.assertEqual(chart.count("<polyline"), 3)
            self.assertIn("higher thrust", chart)


if __name__ == "__main__":
    unittest.main()
