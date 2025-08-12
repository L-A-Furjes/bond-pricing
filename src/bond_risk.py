from bond_cashflows import cashflows
from bond_price import price_dirty
import pandas as pd
from datetime import datetime
from typing import Union

def dv01(cf_df: pd.DataFrame, settle_date : Union[str,datetime],yld: float ) -> float:
    settle_date = pd.to_datetime(settle_date)
    dirty_price_up = price_dirty(cf_df,settle_date,yld - (1/10000)) # yield down -> price up
    dirty_price_low = price_dirty(cf_df,settle_date,yld + (1/10000)) # yield up -> price down
    return 0.5 * (dirty_price_up - dirty_price_low )


def modified_duration(dirty_price : float,dv01 : float) -> float :
    return ((dv01 * 10000)/dirty_price)

def convexity(cf_df: pd.DataFrame, settle_date : Union[str,datetime],yld: float, h : float = 1e-4)-> float:
    settle_date = pd.Timestamp(settle_date)
    p0 = price_dirty(cf_df, settle_date, yld)
    pm = price_dirty(cf_df, settle_date, yld - h)
    pp = price_dirty(cf_df, settle_date, yld + h)
    return (pp + pm - 2.0 * p0) / (p0 * h * h)

def price_change(price_dirty : float, modified_duration : float,convexity : float,h : float = 0.01) -> float:
    variation = -modified_duration * h + (convexity/2) * h*h
    new_price = price_dirty * (1 + variation)
    return new_price



    
if __name__ == "__main__":

    cf = cashflows("2024-01-01", "2029-01-01", 0.05, 2, nominal=1_000)
    settle = "2024-01-01"
    y = 0.02  

    p_dirty = price_dirty(cf, settle, y)
    bpv     = dv01(cf, settle, y)                     # € / bp (positif)
    md      = modified_duration(p_dirty, bpv)         # années (positive)
    cx      = convexity(cf, settle, y)                # années^2

    p_plus100bp = price_change(p_dirty, md, cx,0.01)

    print(f"Dirty : {p_dirty:.6f}")
    print(f"DV01  : {bpv:.6f} €/bp")
    print(f"MD    : {md:.6f} ans")
    print(f"Cx    : {cx:.6f} ans^2")
    print(f"Prix approx après +100 bp : {p_plus100bp:.6f}")