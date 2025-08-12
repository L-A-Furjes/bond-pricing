import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
from bond_yield import YTM_calcuator
from bond_cashflows import cashflows  

def test_ytm():
    df = cashflows('2024-01-01','2025-01-01',0.05,2,1000)
    ytm = YTM_calcuator(df,'2024-01-01','2024-01-01',0.05,2,1000,1000,-0.1,0.2)
    print(abs(0.05 - ytm))
    assert abs(0.05 - ytm) < 0.001
    print("✅ Test passed: ytm = coupon rate on par")

if __name__ == "__main__":
    test_ytm()