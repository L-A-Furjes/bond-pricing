from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import DateOffset
import pandas_market_calendars as mcal

#business_day
#modified_following
#dates
#dataframe

Target = mcal.get_calendar('EUREX')

def is_business_day(date: pd.Timestamp) -> bool :
    return Target.valid_days(date, date).size > 0

def modified_following(date: pd.Timestamp) -> pd.Timestamp :
    actual_month = date.month

    if is_business_day(date):
        return date
    
    while not is_business_day(date):
        date = date + timedelta(days = 1)

    if date.month == actual_month:
        return date
    
    while not is_business_day(date):
        date = date - timedelta(days = 1)
    
    return date

def generate_coupon_dates(
    issue_date: str | datetime,
    maturity_date: str | datetime,
    frequency: float,
) -> list[pd.Timestamp]:
    

    issue_date = pd.to_datetime(issue_date)
    maturity_date = pd.to_datetime(maturity_date)

    step_months = 12//frequency # frequence des coupons

    dates = []

    while maturity_date > issue_date:
        dates.append(maturity_date)
        maturity_date = maturity_date - DateOffset(months=step_months)
    dates.append(issue_date)
    dates = dates[::-1]

    return [modified_following(d) for d in dates]

def cashflows(
    issue_date: str | datetime,
    maturity_date: str | datetime,
    coupon_rate: float,
    frequency: int,
    nominal: float = 100
) -> pd.DataFrame:

    dates = generate_coupon_dates(issue_date,maturity_date,frequency)
    datescf = dates[1:]
    fraction = []
    
    
    coupon = (nominal * coupon_rate )/frequency

    cash = [coupon] * (len(dates) - 2) + [coupon + nominal]

    for i in range(1,len(dates)):
        d_prev = dates[i-1]
        d_curr = dates[i]

        standard_period = (d_prev + DateOffset(months = 12//frequency))

        d_num = (d_curr - d_prev).days
        d_den = (standard_period - d_prev).days

        fraction.append(d_num/d_den)
    
    df = pd.DataFrame({
        'Dates':datescf,
        'Cashflows':cash,
        'Fraction':fraction
    })

    return df


        

if __name__ == '__main__':
    df = cashflows('2022-02-20','2025-03-25',0.05,2,nominal=1000)
    print(df)


