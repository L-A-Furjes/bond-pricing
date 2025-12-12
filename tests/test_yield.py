import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest

from bond_cashflows import cashflows
from bond_price import price_clean
from bond_yield import YTM_calculator


@pytest.mark.parametrize(
    "coupon_rate,yield_rate,frequency,nominal",
    [
        (0.05, 0.05, 2, 1000),  # par bond
        (0.05, 0.04, 2, 1000),  # premium bond
        (0.05, 0.06, 2, 1000),  # discount bond
    ],
)
def test_ytm_recovers_expected_yield(coupon_rate, yield_rate, frequency, nominal):
    df = cashflows("2024-01-01", "2026-01-01", coupon_rate, frequency, nominal)
    clean_price = price_clean(df, "2024-01-01", yield_rate, "2024-01-01", coupon_rate, frequency, nominal)

    ytm = YTM_calculator(df, "2024-01-01", "2024-01-01", coupon_rate, frequency, nominal, clean_price, -0.1, 0.2)

    assert abs(ytm - yield_rate) < 1e-6
