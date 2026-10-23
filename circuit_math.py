"""Core calculations for the ECE Circuit Calculator."""

from __future__ import annotations

import math
from collections.abc import Iterable


def _positive(value: float, name: str) -> float:
    """Return a finite positive value, or explain what needs correcting."""
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be a finite number greater than zero.")
    return number


def solve_ohms_law(
    *, voltage: float | None = None, current: float | None = None, resistance: float | None = None
) -> dict[str, float]:
    """Calculate the missing Ohm's-law value and power from any two inputs."""
    values = {"voltage": voltage, "current": current, "resistance": resistance}
    supplied = {key: _positive(value, key) for key, value in values.items() if value is not None}
    if len(supplied) != 2:
        raise ValueError("Provide exactly two of --voltage, --current, and --resistance.")

    if "voltage" not in supplied:
        result_voltage = supplied["current"] * supplied["resistance"]
        result_current = supplied["current"]
        result_resistance = supplied["resistance"]
    elif "current" not in supplied:
        result_voltage = supplied["voltage"]
        result_resistance = supplied["resistance"]
        result_current = result_voltage / result_resistance
    else:
        result_voltage = supplied["voltage"]
        result_current = supplied["current"]
        result_resistance = result_voltage / result_current

    return {
        "voltage": result_voltage,
        "current": result_current,
        "resistance": result_resistance,
        "power": result_voltage * result_current,
    }


def _resistor_values(values: Iterable[float]) -> list[float]:
    resistors = [_positive(value, "Each resistance") for value in values]
    if not resistors:
        raise ValueError("Provide at least one resistor value.")
    return resistors


def resistance_series(values: Iterable[float]) -> float:
    """Return total resistance for resistors connected in series."""
    return sum(_resistor_values(values))


def resistance_parallel(values: Iterable[float]) -> float:
    """Return total resistance for resistors connected in parallel."""
    resistors = _resistor_values(values)
    return 1.0 / sum(1.0 / resistance for resistance in resistors)


def voltage_divider(input_voltage: float, top_resistance: float, bottom_resistance: float) -> float:
    """Return the unloaded output voltage across the bottom resistor."""
    vin = _positive(input_voltage, "Input voltage")
    r_top = _positive(top_resistance, "Top resistance")
    r_bottom = _positive(bottom_resistance, "Bottom resistance")
    return vin * r_bottom / (r_top + r_bottom)


def led_series_resistor(supply_voltage: float, led_drop: float, current_ma: float) -> tuple[float, float]:
    """Return the ideal resistor value in ohms and its estimated power in watts."""
    supply = _positive(supply_voltage, "Supply voltage")
    forward = _positive(led_drop, "LED forward voltage")
    milliamps = _positive(current_ma, "LED current")
    if supply <= forward:
        raise ValueError("Supply voltage must be greater than LED forward voltage.")
    current_a = milliamps / 1000.0
    resistor = (supply - forward) / current_a
    return resistor, current_a**2 * resistor
