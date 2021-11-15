## **Analyzing the Impact of Unusual Call Option Volumes on Underlying Stock Price Returns**


### Project Overview:

Identify statistically impactful patterns in unusual option volumes, short interest, call/put ratio, and sector as predictive indicators for movement in underlying stock prices.  As a first step in our exploratory data analysis we developed a python-based application to manage filtering and analytical routines for 1100+ tickers.  The key user features of the application are the filters, statistical output tables and data visualizations.  The app is designed to facilitate randomized hypothesis testing using this combination of objective (visual), and quantitative (statistical) outputs.  

---

### Data:

  - OCC option volume data
  - Bloomberg historical closing stock and option prices


### Technologies:

  - JupyterLab IDE
  - Pandas
  - Numpy
  - Matplotlib
  - Bloomberg API (requires Bloomberg software and terminal access)
  - Fire
  - Questionary


### Installation Guide:
Before running the app, ensure that the libraries above are imported, then install the following dependencies on a command line interface.

  - pip install fire
  - pip install questionary
  - Bloomberg API:
    1. python -m pip install — index-url=https://bloomberg.bintray.com/pip/simple blpapi
    2. python import blpapi


### Usage: To use the application, clone the repository and run **app.py** with:

  - python app.py

When app.py is opened, the following welcome screen will appear:

![AppIntro](Images/AppIntro.PNG)

A series of questionary prompts will need to be populated with numerical values:

![AppQuestions](Images/AppQuestions.PNG)


### Data Filtering & Analytical Criteria:

1. Filtering & Screening: Starting with the universe of the top 1200 most heavily optioned stocks on OCC member exchanges, we filter by four key variables:

   - Call/Put ratio
   - High Short Interest as a % of free float
   - Ratio of call option volume vs trailing average call option volume (unusual volume filter)
   - Subsequent measurement window expressed as # of trading days 

2. Statistical analysis:   The application performs a t-test on the daily returns of >1,100 stocks from 7/1/20 to 11/9/21 to see if the returns on days that fall within the parameters defined above exhibit greater positive returns than on days the signal was not live.  These groups of data represent our random variable and our control sample.  To check the veracity of the t-test value we look to the p-value.  The lower the p-value, the lower the probability that our t-stat was driven by random chance.

3. Data visualization:     Histograms, line charts and density plots are generated in matplotlib to display the empirical distribution of returns for a stock or group of stocks.  To objectively confirm the statistical significance of our data, we will expect to observe right-tail skewness in the distribution of returns for the filtered sample vs the "no signal" sample.  


### Results:
  - Using heavily shorted names as a filter, our analysis indicated significant results.  
  - The t-test showed that increased call option volume was a leading indicator for positive stock returns.  
  - Summary data indicates that the mean for the "Signal" returns is clearly higher than the mean for the "No Signal" population.  
  - The T-Stat is over 4 and the probabilty that the result is signfiicant is almost 100% (p value close to 0).

![Return Summary Stats](Images/ReturnSummaryStats.PNG)

  - Visual affirmation of the data in the histogram below clearly shows a positive skewness of returns for the "Signal" population with a long right-tailed distribution.

![Histogram of Returns](Images/Histogram.PNG)
