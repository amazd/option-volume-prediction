# Estimating Options Gamma to Identify Directional Trading Opportunities in Underlying Stocks.

# Introduction:
The US listed option market has witnessed several episodic manias since the COVID-19 pandemic began.  Speculative trading was at times widespread, but often took aim at arcane corners of the market where the spike in volumes was highly disruptive.  Our anecdotal observation suggested the options had, in many cases, become the tail wagging the dog.  We set out with the goal to prove that extreme market gamma exposures can lead to profitable trading opportunities.  To accomplish this goal we built a python-based tool to validate our crude hypothesis that large option positions impact the direction of the underlying stock.

# Background:
Large option positions have the potential to powerfully impact the price of the underlying because market-makers are forced hedgers and end users are not.  Gamma hedging involves the buying or selling of shares (“deltas”) to neutralize the directional exposure of an option position.  Any time a market participant is short options, he or she is short gamma, and vice versa.  A short gamma hedger must buy shares as they rise in price and sell as they go down.  Likewise, a long gamma hedger buys low and sells high.  In sufficient magnitude, this net market gamma asymmetry can lead to extreme movements in the underlying stock.

It is easy to see how a large imbalance between hedger and speculator positions can lead to reflexive directional price action in the stock.  Consider that all market makers are categorically short call options on a stock that is rising.  Moreover, consider that speculators are not hedging.  Market-makers can be forced into a situation where they must lift higher and higher offers in the stock, causing large moves in the spot price.  

Market-makers typically hedge during the last half hour of trading, so we are most likely to find a pattern during this time interval.  If an informed party has a model to indicate the direction and magnitude of market-maker hedging, he or she may design a program that buys or sells deltas ahead of the closing 30 mins of trading, exiting the position immediately prior to the closing bell.


# Objective:
Build a python-based app to test our intuition about the market gamma phenomenon with the aid of statistical evidence and data visualizations. 
 

# Methods & analysis:

1.	Filtering & Screening: Starting with the universe of top 1200 most heavily optioned stocks on OCC member exchanges, we filter by several criteria to highlight only the most lopsided imbalances.  The data model will focus on call options inside three months to maturity with strikes at-the-money or higher.  We initially screened for names with a high degree of options open interest relative to the average daily volume of the stock.  < INSERT NEXT FILTERS >

2.	Curate subset data for analysis. 

3.	Screen filtered data by t-stat to identify eligible subset candidates.  Create a binary “buy” or “sell” signal for each final candidate.

4.	Each trade signal is weighted equally.

5.	Excess returns from the strategy will be calculated using SPX as a benchmark.

6.	If the strategy is consistently profitable, our assumptions about market gamma will be validated.


# Data:
OCC
Bloomberg historical option data


# Technologies:

JupyterLab IDE
Pandas
Numpy
Quandl
HvPlot
Seaborn
Bloomberg API
