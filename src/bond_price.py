from bond_cashflows import cashflows
from datetime import datetime
import numpy as np
import pandas as pd
from typing import Union

def price_dirty(cf_df, settle_date: Union [str,pd.Timestamp],yld: float) -> float:

    settle_date = pd.to_datetime(settle_date)
    
    future_cf = cf_df[cf_df['Dates'] > settle_date]
    cashflows = future_cf['Cashflows']
    dates = future_cf['Dates']
    t_list = [(date - settle_date).days/365 for date in dates]


    dirty_price = sum(c/((1+yld)**t) for c,t in zip(cashflows,t_list))
    
    return dirty_price





def accrued_interest(cf_df,issue_date: Union [str, pd.Timestamp], settle_date:Union [str, pd.Timestamp],coupon_rate:float, frequency:int, nominal: float) -> float:
    
    df_Dates = cf_df['Dates']
    settle_date = pd.to_datetime(settle_date)
    issue_date = pd.to_datetime(issue_date)
    
    last_coupon = df_Dates[df_Dates <= settle_date].iloc[-1] if not df_Dates[df_Dates <= settle_date].empty else issue_date

    next_coupon = df_Dates[df_Dates > settle_date].iloc[0]

    coupon = (nominal * coupon_rate )/frequency
    ai = coupon * ((settle_date - last_coupon).days/(next_coupon-last_coupon).days)
    return ai



def price_clean(dirty: float, accrued: float) -> float:
    return dirty - accrued

if __name__ == '__main__':
    df = cashflows('2022-02-20','2025-03-25',0.05,2,nominal=1000)
    df_dirty = price_dirty(df,'2023-03-20',0.05)
    df_ai = accrued_interest(df, '2022-02-20', '2023-03-20', 0.05, 2, nominal=1000)
    df_clean = price_clean(df_dirty,df_ai)
    print(df_clean)





