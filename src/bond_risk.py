from bond_cashflows import cashflows
from bond_price import price_dirty
import pandas as pd
from datetime import datetime
from typing import Union

def dv01(cf_df: pd.DataFrame, settle_date : Union[str,datetime],yld: float ) -> float:
    dirty_price_up = price_dirty(cf_df,settle_date,yld - (1/10000))
    dirty_price_low = price_dirty(cf_df,settle_date,yld + (1/10000))
    return 0.5 * (dirty_price_low - dirty_price_up)


def modified_duration(dirty_price : float,dv01 : float) -> float :
    return ((-dv01 * 10000)/dirty_price)


if __name__ == '__main__':
    df = cashflows('2024-01-01','2029-01-01',0.05,2,nominal=1000)
    df_dirty = price_dirty(df,'2024-01-01',0.02)
    risk = dv01(df,'2024-01-01',0.02)
    risk2 = modified_duration(df_dirty,risk)
    print(df_dirty)
    print(risk)
    print(risk2)
    
