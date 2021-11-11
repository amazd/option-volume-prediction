import sys
import fire
import questionary
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from pathlib import Path

def get_shift_amount():

    action = questionary.select(
        "How many days of return should we look forward to?",
        choices=["1", "5", "10"],
    ).ask()
    return action

def intersection (lst1, lst2):
    return list (set(lst1) & set(lst2))

def union (lst1, lst2):
    return list (set(lst1) | set(lst2))

def run():
    """The main function for running the script."""

    call_volume = Path("./data/Call_Volume_20211102.csv")
    returns = Path("./data/Stock_Returns_20211102.csv")
    put_volume = Path("./data/Put_Volume_20211102.csv")

    call_volume_df = pd.read_csv(
        call_volume, 
        index_col="date", 
        infer_datetime_format=True, 
        parse_dates=True
    )

    price_df = pd.read_csv(
        returns, 
        index_col="date", 
        infer_datetime_format=True, 
        parse_dates=True
    )

    put_volume_df = pd.read_csv(
        put_volume, 
        index_col="date", 
        infer_datetime_format=True, 
        parse_dates=True
    )

    start_date = "2020-04-01"
    end_date = "2021-06-30"

    call_volume_df = call_volume_df.loc[start_date:end_date]
    put_volume_df = put_volume_df.loc[start_date:end_date]

    #nDay Return
    shift = get_shift_amount()
    #shift = 3

    # Call/Put Ratio Threshold
    call_put_ratio_threshold = 2

    sixty_day_rolling_volume_df = call_volume_df.rolling(60).mean()

    price_df.apply(pd.to_numeric)

    shift_amt = shift * -1
    shifted = price_df.shift(periods=shift_amt, axis="rows")
    period_day_return = shifted/price_df-1

    ticker_names = list(period_day_return)

    trailing_sixty_day = sixty_day_rolling_volume_df.shift(periods=-1, axis="rows")
    volume_indicator = 4 * trailing_sixty_day

    good_vol_signal = {}
    no_vol_signal = {}

    for ticker in ticker_names:
        i = 0
        good_vol_signal[ticker] = []
        no_vol_signal[ticker] = []

        for value in call_volume_df[ticker]:
            date = call_volume_df.index[i]
            if(value > volume_indicator[ticker][i]):
                good_vol_signal[ticker].append(date)
            else:
                no_vol_signal[ticker].append(date)
            i+= 1


    call_put_ratio = call_volume_df / put_volume_df


    good_ratio_signal = {}
    no_ratio_signal = {}

    for ticker in ticker_names:
        i = 0
        good_ratio_signal[ticker] = []
        no_ratio_signal[ticker] = []

        for ratio in call_put_ratio[ticker]:
            date = call_put_ratio.index[i]
            if(ratio > call_put_ratio_threshold):
                good_ratio_signal[ticker].append(date)
            else:
                no_ratio_signal[ticker].append(date)
            i+= 1


    good_final_signal = {}
    no_final_signal = {}

    for ticker in ticker_names:
        good_final_signal[ticker] = intersection(good_vol_signal[ticker], good_ratio_signal[ticker])

    for ticker in ticker_names:
        no_final_signal[ticker] = union(no_vol_signal[ticker], no_ratio_signal[ticker])

    good_signal_returns = {}
    no_signal_returns = {}

    for ticker in ticker_names:
        good_signal_returns[ticker] = []
        no_signal_returns[ticker] = []
        for date in good_final_signal[ticker]:
            change = period_day_return.loc[date][ticker]
            good_signal_returns[ticker].append(change)
        for date in no_final_signal[ticker]:
            change = period_day_return.loc[date][ticker]
            no_signal_returns[ticker].append(change)
        
    total=0
    for ticker in ticker_names:
        total = total + len(good_signal_returns[ticker])
    print(total)


    totalno=0
    for ticker in ticker_names:
        totalno = totalno + len(no_signal_returns[ticker])

    good_signal_returns_list = []
    for ticker in ticker_names:
        good_signal_returns_list = good_signal_returns_list  + good_signal_returns[ticker]

    no_signal_returns_gross_list = []
    for ticker in ticker_names:
        no_signal_returns_gross_list = no_signal_returns_gross_list  + no_signal_returns[ticker]
    no_signal_returns_list = [x for x in no_signal_returns_gross_list if np.isnan(x) == False]
    len(no_signal_returns_list)



    print(np.var(good_signal_returns_list))
    print(np.mean(good_signal_returns_list))

    print(np.var(no_signal_returns_list))
    print(ttest_ind(a=good_signal_returns_list, b=no_signal_returns_list, equal_var=True))


# Entry point for the application. Initiates the run() function.
if __name__ == "__main__":
    fire.Fire(run)
