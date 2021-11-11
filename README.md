# Analyzing the Impact of Unusual Call Option Volumes on Underlying Stock Price Returns

Python-based application designed to identify the impact of call option volumes on price action in the underlying stock.  The application features flexible filtering and processing functionality that users can manipulate for various use cases.  

Our study sought to identify statistically meaningful patterns in option volumes, short interest and sector as predictive criteria for movement in stock price.


## Data:

OCC option volume data
Bloomberg historical closing stock and option prices


## Technologies:
JupyterLab IDE
Pandas
Numpy
HvPlot
Bloomberg API


## Methods & analysis:

1.	Filtering & Screening: Starting with the universe of top 1200 most heavily optioned stocks on OCC member exchanges, we filter by several criteria to to generate a subset of tickers perceived to be the most likely stocks to be impacted by option flows.  The data model will focus on call options inside three months to maturity with strikes at-the-money or higher.  We initially screened for names with a high degree of options open interest relative to the average daily volume of the stock.  < INSERT NEXT FILTERS >

2.	Curate subset data for analysis. 

3.	Screen filtered data by t-stat to identify eligible subset candidates.  Create a binary “buy” or “sell” signal for each final candidate.

4.	Each trade signal is weighted equally.

5.	Excess returns from the strategy will be calculated using SPX as a benchmark.

6.	If the strategy is consistently profitable, our assumptions about market gamma will be validated.


## Contibutors:

Ahmad Sadraei
Vishnu Kurella
Ling Zhou
Lee Copeland