from typing import Union
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from bond_price import price_clean  
from bond_cashflows import cashflows  

def YTM_calcuator(cf_df: pd.DataFrame, settle_date : Union[str,datetime], issue_date : Union[str,datetime],coupon_rate:float, frequency:int, nominal: float ,clean_price : float, y_low : float, y_high : float, tol : float = 1e-12) -> float:

    def objective(y: float) -> float:
        
        return price_clean(cf_df,settle_date,y,issue_date,coupon_rate,frequency,nominal) - clean_price

    return brentq(objective,y_low,y_high,xtol= tol)

if __name__ == "__main__":
    df = cashflows('2024-01-01','2025-01-01',0.05,2,1000)
    ytm = YTM_calcuator(df,'2024-01-01','2024-01-01',0.05,2,1000,1000,-0.1,0.2)
    print(f"YTM = {ytm:.6%}")