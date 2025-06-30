from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import DateOffset


def is_business_day(date):
    return date.weekday() < 5

def modified_following(date):
    current_date = date

    if is_business_day(current_date):
        return current_date
    
    while True:
        current_date = current_date + timedelta(days = 1)
        if is_business_day(current_date):
            break
    if current_date.month == date.month:
        return current_date
    
    while True:
        current_date = current_date - timedelta(days = 1)
        if is_business_day(current_date):
            return current_date
    


def cashflows(issue_date, maturity_date, coupon_rate, annual_frequency, nominal=100):
    issue_date = pd.to_datetime(issue_date)
    maturity_date = pd.to_datetime(maturity_date)

    months = 12 // annual_frequency
    actual_date = issue_date

    dates = [issue_date]
    while actual_date < maturity_date:
        actual_date += DateOffset(months=months)
        dates.append(actual_date)

    # Ajustement calendrier
    dates = [modified_following(d) for d in dates]

    # Coupon fixe par période
    coupon = (coupon_rate / 100) * nominal / annual_frequency

    # Cashflows
    cashflows = [coupon] * (len(dates) - 2) + [coupon + nominal]

    # Fractions ACT/ACT
    fractions = []
    for i in range(1, len(dates)):
        d_prev = dates[i - 1]
        d_curr = dates[i]
        d_next = dates[i + 1] if i + 1 < len(dates) else d_curr + (d_curr - d_prev)

        num = (d_curr - d_prev).days
        denom = (d_next - d_prev).days
        f = num / denom
        fractions.append(f)

    df = pd.DataFrame({
        'date': dates[1:],
        'cashflow': cashflows,
        'fraction': fractions
    })

    return df

            
if __name__ == "__main__":
    df = cashflows(
        issue_date="2024-02-15",
        maturity_date="2027-02-20",
        coupon_rate=5,             # 5% annuel
        annual_frequency=2,        # semi-annuel
        nominal=100                # nominal
    )
    print(df)





        

