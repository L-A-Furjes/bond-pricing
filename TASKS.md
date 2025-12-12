# Maintenance Task Proposals

## 1) Fix typographical error
- **Issue:** The yield-to-maturity helper is spelled `YTM_calcuator` in both its definition and call sites, which is a typo and makes the public API name non-standard.
- **Task:** Rename the function to `YTM_calculator` in `src/bond_yield.py` and update every reference (including tests) to use the corrected name.

## 2) Guard against accrued-interest edge case
- **Issue:** `accrued_interest` blindly selects the next coupon date and will raise an `IndexError` when the settlement date is on or after the final cash flow, preventing pricing of matured or nearly matured bonds.
- **Task:** Add a safe fallback when no future coupon exists (e.g., return 0 or handle maturity cash flow explicitly) so the function behaves predictably past the last payment date.

## 3) Improve documentation for environment setup
- **Issue:** The README only contains the project title and omits installation or dependency instructions, even though running the code requires packages like `pandas`, `numpy`, `pandas_market_calendars`, and `scipy` that are not specified anywhere. This makes the repository non-reproducible out of the box.
- **Task:** Expand `README.md` with setup steps (e.g., virtualenv creation and `pip install -r requirements.txt`) and list the required Python dependencies.

## 4) Strengthen yield test coverage
- **Issue:** `tests/test_yield.py` uses a single par bond scenario and prints diagnostic output but does not cover off-par pricing or root-finding tolerance issues.
- **Task:** Add parametrized cases (premium/discount prices and tighter tolerance expectations) and remove console prints so the test suite validates the YTM solver across realistic scenarios without noisy output.
