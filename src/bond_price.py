from bond_cashflows import cashflows
from datetime import datetime
import numpy as np
import pandas as pd
from typing import Union


"""
Exercise 2
===========================
Dirty price, accrued interest and clean price for a fixed-rate bullet bond.

We re-use the `cashflows` function from bond_cashflows.py (Exercise 1).

Conventions
-----------
* `yld` is an annual yield in decimal (e.g. 0.0375 = 3.75 %).
* Present-value day-count: ACT/365.25 (simple).
* Accrued-interest day-count: ACT/ACT ICMA.
"""


# ---------------------------------------------------------------------
# 1. Dirty price
# ---------------------------------------------------------------------

def price_dirty(cf_df:pd.DataFrame, settle_date: Union [str,pd.Timestamp],yld: float) -> float:

    settle_date = pd.to_datetime(settle_date)
    
    future_cf = cf_df[cf_df['Dates'] >= settle_date]
    if future_cf.empty:
        return 0.0

    cashflows = future_cf['Cashflows']
    dates = future_cf['Dates']
    t_list = [(date - settle_date).days/365.25 for date in dates]


    dirty_price = sum(c/((1+yld)**t) for c,t in zip(cashflows,t_list))
    
    return dirty_price



# ---------------------------------------------------------------------
# 2. Accrued interest (coupon couru)
# ---------------------------------------------------------------------

def accrued_interest(cf_df:pd.DataFrame,issue_date: Union [str, pd.Timestamp], settle_date:Union [str, pd.Timestamp],coupon_rate:float, frequency:int, nominal: float) -> float:
    
    df_Dates = cf_df['Dates']
    settle_date = pd.to_datetime(settle_date)
    issue_date = pd.to_datetime(issue_date)
    
    last_coupon = df_Dates[df_Dates <= settle_date].iloc[-1] if not df_Dates[df_Dates <= settle_date].empty else issue_date

    next_coupon = df_Dates[df_Dates > settle_date].iloc[0]



    coupon = (nominal * coupon_rate )/frequency
    ai = coupon * ((settle_date - last_coupon).days/(next_coupon-last_coupon).days)
    return ai




# ---------------------------------------------------------------------
# 3. Clean price
# ---------------------------------------------------------------------
def price_clean(cf_df: pd.DataFrame, settle_date : Union[str,datetime],yld: float, issue_date : Union[str,datetime],coupon_rate:float, frequency:int, nominal: float ) -> float:
    dirty = price_dirty(cf_df,settle_date,yld)
    ai = accrued_interest(cf_df,issue_date,settle_date,coupon_rate,frequency,nominal)
    return dirty - ai




# ---------------------------------------------------------------------
# 4.test 
# ---------------------------------------------------------------------

if __name__ == '__main__':
    df = cashflows('2024-01-01','2029-01-01',0.05,2,nominal=1000)
    df_clean = price_clean(df,'2024-01-01',0.02,'2024-01-01',0.05,2,1000)
    print(df_clean)




