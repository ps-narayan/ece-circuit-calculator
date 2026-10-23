import math
import unittest

from circuit_math import (
    led_series_resistor,
    resistance_parallel,
    resistance_series,
    solve_ohms_law,
    voltage_divider,
)


class CircuitMathTests(unittest.TestCase):
    def test_ohms_law_from_voltage_and_resistance(self):
        result = solve_ohms_law(voltage=12, resistance=220)
        self.assertAlmostEqual(result["current"], 12 / 220)
        self.assertAlmostEqual(result["power"], 12 * 12 / 220)

    def test_ohms_law_requires_exactly_two_inputs(self):
        for values in ({}, {"voltage": 5}, {"voltage": 5, "current": 0.1, "resistance": 50}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                solve_ohms_law(**values)

    def test_series_and_parallel_resistance(self):
        self.assertEqual(resistance_series([100, 220, 330]), 650)
        self.assertAlmostEqual(resistance_parallel([1000, 1000]), 500)

    def test_voltage_divider(self):
        self.assertEqual(voltage_divider(5, 10_000, 10_000), 2.5)

    def test_led_resistor_and_power(self):
        resistance, power = led_series_resistor(5, 2, 15)
        self.assertAlmostEqual(resistance, 200)
        self.assertAlmostEqual(power, 0.045)

    def test_invalid_inputs_are_rejected(self):
        for operation in (
            lambda: resistance_series([]),
            lambda: resistance_series([None]),
            lambda: resistance_parallel([100, 0]),
            lambda: solve_ohms_law(voltage=math.inf, current=1),
            lambda: voltage_divider(5, -1, 100),
            lambda: led_series_resistor(2, 2, 10),
        ):
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                operation()


if __name__ == "__main__":
    unittest.main()
