from bond_cashflows import cashflows
from datetime import datetime
import numpy as np
import pandas as pd

def accrued_interet(cf_df,issue_date:str| pd.Timestamp, settle_date:str| pd.Timestamp,coupon_rate:float, frequency:int, nominal: float) -> float:
    
    df_Dates = cf_df['Dates']
    settle_date = pd.to_datetime(settle_date)
    issue_date = pd.to_datetime(issue_date)
    
    last_coupon = df_Dates[df_Dates <= settle_date].iloc[-1] if not df_Dates[df_Dates <= settle_date].empty else issue_date

    next_coupon = df_Dates[df_Dates > settle_date].iloc[0]

    coupon = (nominal * coupon_rate )/frequency
    ai = coupon * ((settle_date - last_coupon).days/(next_coupon-last_coupon).days)
    return ai

if __name__ == '__main__':
    df = cashflows('2022-02-20','2025-03-25',0.05,2,nominal=1000)
    af = accrued_interet(df,'2022-02-20','2022-03-20',0.05,2,nominal=1000)
    print(af)





