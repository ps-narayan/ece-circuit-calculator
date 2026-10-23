"""Command-line interface for common introductory circuit calculations."""

from __future__ import annotations

import argparse

from circuit_math import (
    led_series_resistor,
    resistance_parallel,
    resistance_series,
    solve_ohms_law,
    voltage_divider,
)


def _number(value: float) -> str:
    return f"{value:.6g}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate common DC circuit values.",
        epilog="Values use volts (V), amps (A), ohms (ohm), milliamps (mA), and watts (W).",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    ohms = commands.add_parser("ohms", help="solve Ohm's law from any two values")
    ohms.add_argument("--voltage", type=float, help="voltage in volts")
    ohms.add_argument("--current", type=float, help="current in amps")
    ohms.add_argument("--resistance", type=float, help="resistance in ohms")

    for command, help_text in (
        ("series", "find equivalent resistance in series"),
        ("parallel", "find equivalent resistance in parallel"),
    ):
        subparser = commands.add_parser(command, help=help_text)
        subparser.add_argument("resistances", nargs="+", type=float, metavar="OHMS")

    divider = commands.add_parser("divider", help="calculate an unloaded voltage divider")
    divider.add_argument("--input-voltage", required=True, type=float, help="input voltage in volts")
    divider.add_argument("--top", required=True, type=float, help="top resistor in ohms")
    divider.add_argument("--bottom", required=True, type=float, help="bottom resistor in ohms")

    led = commands.add_parser("led", help="estimate a series resistor for one LED")
    led.add_argument("--supply", required=True, type=float, help="supply voltage in volts")
    led.add_argument("--led-drop", required=True, type=float, help="LED forward voltage in volts")
    led.add_argument("--current-ma", required=True, type=float, help="target LED current in milliamps")
    return parser


def run(args: argparse.Namespace) -> str:
    if args.command == "ohms":
        result = solve_ohms_law(voltage=args.voltage, current=args.current, resistance=args.resistance)
        return "\n".join(
            (
                f"Voltage:    {_number(result['voltage'])} V",
                f"Current:    {_number(result['current'])} A ({_number(result['current'] * 1000)} mA)",
                f"Resistance: {_number(result['resistance'])} ohm",
                f"Power:      {_number(result['power'])} W",
            )
        )
    if args.command in {"series", "parallel"}:
        calculate = resistance_series if args.command == "series" else resistance_parallel
        return f"Equivalent resistance ({args.command}): {_number(calculate(args.resistances))} ohm"
    if args.command == "divider":
        output = voltage_divider(args.input_voltage, args.top, args.bottom)
        return f"Output voltage (unloaded): {_number(output)} V"
    if args.command == "led":
        resistance, power = led_series_resistor(args.supply, args.led_drop, args.current_ma)
        return "\n".join(
            (
                f"Ideal series resistance: {_number(resistance)} ohm",
                f"Estimated resistor power: {_number(power)} W",
                "Choose the next higher standard resistor value and check component ratings.",
            )
        )
    raise ValueError(f"Unknown command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        print(run(args))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
