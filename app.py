import fire
import questionary
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from pathlib import Path
import matplotlib.pyplot as plt
import hvplot.pandas 

ALL_SECTOR_STRING = "All Sectors"

def get_user_input():

    # Multiple of Avg Daily Vol
    adv_multiple = questionary.select(
        "What multiple of trailing call options volume do you want to use for a call option volume trigger?",
        choices=["2", "3", "4"],
    ).ask()

    # nDay Return
    shift = questionary.select(
        "What period of returns would you like to use after the signal is triggered (# of days)?",
        choices=["1", "5", "10"],
    ).ask()

    # Call/Put Ratio Threshold
    call_put_ratio_threshold = questionary.select(
        "What call/put ratio threshold would you like to use for the signal to be triggered?",
        choices=["3", "2", "1"],
    ).ask()

    # Short interest threshold
    short_interest_threshold = questionary.select(
        "What short interest percentage threshold do you want to filter for?",
        choices=["5", "10", "20"],
    ).ask()

    all_sectors_df = pd.read_csv(Path("./data/Sectors_20211102.csv"))
    all_sector_names = all_sectors_df['value'].dropna().unique().tolist()
    all_sector_names.insert(0, ALL_SECTOR_STRING)

    filter_input_sector = questionary.select(
        "Which Sector would you like to filter by?",
        choices=all_sector_names,
    ).ask()

    return [int(shift), int(call_put_ratio_threshold), int(short_interest_threshold), int(adv_multiple), filter_input_sector]

def intersection (lst1, lst2):
    return list (set(lst1) & set(lst2))

def run():

    call_volume = Path("./data/Call_Volume_20211102.csv")
    prices = Path("./data/Stock_Prices_20211102.csv")
    put_volume = Path("./data/Put_Volume_20211102.csv")
    SPY_prices = Path("./data/SPY_Price_20211102.csv")
    short_interest = Path("./data/Short_Interest_20211102.csv")
    all_sectors = Path("./data/Sectors_20211102.csv")

    # Read in csv files
    call_volume_df = pd.read_csv(
        call_volume, 
        index_col="date", 
        infer_datetime_format=True, 
        parse_dates=True
    )

    price_df = pd.read_csv(
        prices, 
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

    SPY_prices_df = pd.read_csv(
        SPY_prices, 
        index_col="date", 
        infer_datetime_format=True, 
        parse_dates=True
    )

    short_interest_df = pd.read_csv(
        short_interest, 
        index_col="date", 
        infer_datetime_format=True, 
        parse_dates=True
    )

    all_sectors_df = pd.read_csv(
        all_sectors
    )

    # Get user input
    [shift, call_put_ratio_threshold, short_interest_threshold, adv_multiple, filter_input_sector] = get_user_input()

    print(f"Calculating the rolling avgs...")

    # Calculate the 60d trailing volue and daily percent changes
    sixty_day_rolling_volume_df = call_volume_df.rolling(60).mean()
    pct_change_one_day = price_df.pct_change()

    start_date = "2020-04-01"
    end_date = "2021-11-09"

    #filtering the data down by date range
    call_volume_df = call_volume_df.loc[start_date:end_date]
    put_volume_df = put_volume_df.loc[start_date:end_date]
    SPY_prices_df = SPY_prices_df.loc[start_date:end_date]
    price_df = price_df.loc[start_date:end_date]

    spy_pct_change = SPY_prices_df.pct_change()
    spy_roll_var = spy_pct_change.rolling(60).var()

    #Generating new dataframe for 60d rolling covariance
    rolling_cov = pct_change_one_day.rolling(60).cov(spy_pct_change['SPY'])
    rolling_beta = rolling_cov.copy()

    #Calculating rolling 60d betas for each ticker
    for ticker in rolling_cov:
        rolling_beta[ticker] = rolling_cov[ticker]/spy_roll_var['SPY']

    #Incorporating the n-day return shift to calc daily period returns
    shift_amt = shift * -1
    shifted = price_df.shift(periods=shift_amt, axis="rows")
    period_day_return = shifted/price_df-1

    ticker_names = list(period_day_return)

    #defining trailing 60d volume df and the volume threshold
    trailing_sixty_day = sixty_day_rolling_volume_df.shift(periods=-1, axis="rows")
    volume_indicator = adv_multiple * trailing_sixty_day

    #starting with empty dictionaries
    good_vol_signal = {}
    no_vol_signal = {}

    print(f"Finding signal based on option volumes...")

    #creating the dictionary with the key being the ticker and the value being a list of triggered dates
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

    #Calculating Call / Put Ratio
    call_put_ratio = call_volume_df / put_volume_df

    #Creating empty dictionaries for call put ratio signal
    good_ratio_signal = {}
    no_ratio_signal = {}

    print(f"Finding signal based on call/put ratio...")

    #Creating dictionary for call put ratio signal
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


    #Starting with empty dictionaries
    good_final_signal = {}
    no_final_signal = {}

    #Defining intersection function
    def intersection (lst1, lst2):
        return list (set(lst1) & set(lst2))

    #Creating final signal date list within dictionaries
    for ticker in ticker_names:
        good_final_signal[ticker] = intersection(good_vol_signal[ticker], good_ratio_signal[ticker])

    for ticker in ticker_names:
        no_final_signal[ticker] = no_vol_signal[ticker] + no_ratio_signal[ticker]

    #Creating SPY n-day returns
    spy_shifted = SPY_prices_df.shift(periods=shift_amt, axis="rows")
    spy_period_day_return = spy_shifted/SPY_prices_df-1

    #Calculating beta-adjusted outperformance as stock return minus beta * SPY return

    beta_adj_outperf = period_day_return.copy()
    for ticker in ticker_names:
        beta_adj_outperf[ticker] = period_day_return[ticker] - (spy_period_day_return['SPY'] * rolling_beta[ticker])

    good_signal_returns = {}
    no_signal_returns = {}

    print(f"Filtering down signal by beta adjusted outperf (this part will take a min)...")

    for ticker in ticker_names:
        good_signal_returns[ticker] = []
        no_signal_returns[ticker] = []
        for date in good_final_signal[ticker]:
            change = beta_adj_outperf.loc[date][ticker]
            good_signal_returns[ticker].append(change)
        for date in no_final_signal[ticker]:
            change = beta_adj_outperf.loc[date][ticker]
            no_signal_returns[ticker].append(change)

    print(f"Preparing results... \n")

    #Calculating number of observations for signal triggered
    total=0
    for ticker in ticker_names:
        total = total + len(good_signal_returns[ticker]) 

    totalno=0
    for ticker in ticker_names:
        totalno = totalno + len(no_signal_returns[ticker])

    #Employing short interest filter
    short_interest_max  = {}
    for ticker in short_interest_df:
        short_interest_max[ticker] = short_interest_df[ticker].max()

    filtered_short_interest = []
    for ticker in short_interest_max:
        if(short_interest_max[ticker] > short_interest_threshold):
            filtered_short_interest.append(ticker)

    #Employing sector selection filter
    if(filter_input_sector != ALL_SECTOR_STRING):
        filtered_tickers_df = all_sectors_df[all_sectors_df.value == filter_input_sector]
        sector_filtered_list = filtered_tickers_df['ticker'].tolist()
    else:
        sector_filtered_list = ticker_names

    #Creating final list of returns for statistical analysis
    good_signal_returns_list = []

    #Using filters to create list of subset of tickers based on user inputs
    filtered_ticker_names = intersection(sector_filtered_list, filtered_short_interest)

    for ticker in filtered_ticker_names:
        good_signal_returns_list = good_signal_returns_list + good_signal_returns[ticker]

    no_signal_returns_gross_list = []
    for ticker in filtered_ticker_names:
        no_signal_returns_gross_list = no_signal_returns_gross_list  + no_signal_returns[ticker]

    #filter out the nan
    no_signal_returns_list = [x for x in no_signal_returns_gross_list if np.isnan(x) == False]
    good_signal_returns_list = [x for x in good_signal_returns_list if np.isnan(x) == False]

    good_signal_returns_list_df = pd.DataFrame(good_signal_returns_list, columns=['Beta-Adjusted Outperformance Returns'])
    print(f"Signal Triggered {good_signal_returns_list_df.describe()}") 
    #good_signal_returns_list_df.hvplot.hist(bins=700, xlim=(-1,2), title="Frequency of Outperformance Returns in Signalled Dates")

    no_signal_returns_list_df = pd.DataFrame(no_signal_returns_list)
    no_signal_returns_list_df.columns = ["Beta-Adjusted Outperformance Returns (for July 2020 to Nov 2021)"]
    print(f"Signal Not Triggered {no_signal_returns_list_df.describe()}") 
    #no_signal_returns_list_df.hvplot.hist(bins=700, xlim=(-1,2), title="Frequency of Outperformance Returns in Control Dates")

    good_mean = np.mean(good_signal_returns_list)
    bad_mean = np.mean(no_signal_returns_gross_list)

    #T-test
    tt, pvalue = ttest_ind(a=good_signal_returns_list, b=no_signal_returns_list, equal_var=True)
    print(f"The T-test T-stat is {tt :.2f}")
    print(f"The T-test p-value is {100*pvalue :.2f}%")
    print(f"The mean return of our signal is {100*good_mean :.2f}%")
    print(f"The mean return of no signal is {100*bad_mean :.2f}%")

# Entry point for the application. Initiates the run() function.
if __name__ == "__main__":
    fire.Fire(run)
