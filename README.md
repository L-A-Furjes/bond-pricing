# bond-pricing

Python utilities to generate bond cash flows, compute accrued interest, and price fixed-rate bullet bonds.

## Requirements

The project targets Python 3.10+ and relies on the following packages:

- numpy
- pandas
- pandas_market_calendars
- scipy
- pytest (for running the test suite)

A `requirements.txt` file is provided for convenience.

## Setup

1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running tests

Execute the test suite with:

```bash
pytest -q
```

## Usage example

The modules under `src/` can be imported directly. For example, to price a bond and compute its yield-to-maturity:

```python
from bond_cashflows import cashflows
from bond_price import price_clean
from bond_yield import YTM_calculator

cf = cashflows("2024-01-01", "2026-01-01", 0.05, 2, 1000)
clean = price_clean(cf, "2024-01-01", 0.04, "2024-01-01", 0.05, 2, 1000)
ytm = YTM_calculator(cf, "2024-01-01", "2024-01-01", 0.05, 2, 1000, clean, -0.1, 0.2)
```
