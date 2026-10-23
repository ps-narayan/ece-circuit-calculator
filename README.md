# ECE Circuit Calculator

A small command-line toolkit for common first-year circuit calculations. It uses only the Python standard library, so there is nothing to install.

## Requirements

- Python 3.10 or newer

## Quick start

```powershell
python main.py ohms --voltage 12 --resistance 220
python main.py series 220 330 1000
python main.py parallel 1000 2200 4700
python main.py divider --input-voltage 5 --top 10000 --bottom 10000
python main.py led --supply 5 --led-drop 2 --current-ma 15
```

Run `python main.py --help` or `python main.py <command> --help` for the full command list.

## Features

- Solve Ohm's law when any two of voltage, current, and resistance are given; also report power.
- Find equivalent resistance for series and parallel resistor networks.
- Calculate a two-resistor voltage divider output.
- Estimate a current-limiting resistor for a single LED.
- Reject missing, non-finite, zero, or negative electrical values with a clear message.

## Example

```text
$ python main.py ohms --voltage 12 --resistance 220
Voltage:    12 V
Current:    0.0545455 A (54.5455 mA)
Resistance: 220 ohm
Power:      0.654545 W
```

The LED result is an ideal calculation. In a real circuit, choose the next higher standard resistor value and check resistor power and component ratings.

## Formulas

- Ohm's law: `V = I × R`; power: `P = V × I`
- Series: `R_total = R1 + R2 + ...`
- Parallel: `1 / R_total = 1/R1 + 1/R2 + ...`
- Divider: `V_out = V_in × R_bottom / (R_top + R_bottom)`
- LED resistor: `R = (V_supply - V_LED) / I_LED`

## Run the checks

```powershell
python -m unittest discover -s tests -v
```

## Project layout

```text
main.py                 Command-line interface
circuit_math.py         Reusable calculation functions
tests/test_circuit_math.py
```

## Learning goals

Practice functions, input validation, lists, command-line arguments, unit conversions, and automated tests while connecting each calculation to a familiar circuit.
