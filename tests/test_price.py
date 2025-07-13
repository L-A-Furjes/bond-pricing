import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from bond_price import price_clean, price_dirty, accrued_interest
from bond_cashflows import cashflows

import pandas as pd
from bond_price import price_clean, price_dirty, accrued_interest
from bond_cashflows import cashflows


def test_price_dirty_simple():
    df = cashflows('2024-01-01','2025-01-01',0.05,1,1000)
    dirty = price_dirty(df,'2024-01-01',0.05)
    assert abs(dirty - 1000) < 0.5
    print("✅ Test passed: clean price = dirty - accrued interest")


def test_accrued_interest_halfway():
    df = cashflows('2024-01-01', '2025-01-01', 0.05,1,1000)
    ai = accrued_interest(df, '2024-01-01', '2024-07-01',  0.05,1,1000)
    assert abs(ai - 25.0) < 0.5  # moitié d’un coupon annuel (50 * 0.5)
    print("✅ Test passed: accrued interest is correct")

def test_price_clean_consistency():
    df = cashflows('2024-01-01','2025-01-01',0.05,1,1000)
    dirty = price_dirty(df,'2024-01-01',0.05)
    df_clean = price_clean(df,'2024-01-01',0.05,'2024-01-01',0.05,1,1000)
    ai = accrued_interest(df,'2024-01-01','2024-01-01',0.05,1,1000)
    assert abs(dirty - (ai + df_clean)) < 1e-6
    print("✅ Test passed: clean = dirty - AI")


if __name__ == "__main__":
    test_price_dirty_simple()
    test_accrued_interest_halfway()
    test_price_clean_consistency()
