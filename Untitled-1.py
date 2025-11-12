import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define your companies
companies = ['RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'AAPL', 'TSLA']

# Download last 2 months of daily data
data = yf.download(companies, start="2025-09-11", end="2025-11-11")['Close']

print("stock closing price for the last few days")

# Preview data
print(data.tail())

# Plot the stock prices
data.plot(figsize=(10,5), title="Stock Prices - Last 2 Months")
plt.show()
print("\n")

# assume 'data' is a DataFrame with daily Close prices, DateTime index
# Example columns: ['RELIANCE.NS','HDFCBANK.NS','INFY.NS','AAPL','TSLA']

# 1) ensure index is datetime
data.index = pd.to_datetime(data.index)          # (a) make sure index is timestamps

# 2) weekly last (end-of-week closing price)
weekly_last = data.resample('W').last()         # (b) resample by calendar week, take last obs

# 3) weekly mean (average price during week)
weekly_mean = data.resample('W').mean()         # (c) resample by week, take mean

# 4) quick peek
print("\n")
print("closing price of stock every week")
print("\n")
print(weekly_last.head())
print("\n")
print("mean closing price of stock every week")
print("\n")
print(weekly_mean.head())

# Compute weekly percent change using weekly_last (end-of-week returns)
weekly_returns = weekly_last.pct_change() * 100  # (d) percent change between end-of-week prices
weekly_returns = weekly_returns.dropna()         # (e) drop the NaN row for the first week

# Alternative: percent change on weekly_mean if you prefer averages
weekly_mean_returns = weekly_mean.pct_change() * 100
print("\n")
print("percentage change:")
print("\n")
print(weekly_returns)
print("\n")
print("mean percentage change:")
print("\n")
print(weekly_mean_returns)

# weekly_returns is wide (columns = tickers). Convert to long format (tidy)
weekly_returns_long = weekly_returns.reset_index().melt(id_vars='Date', var_name='company', value_name='weekly_return')
weekly_returns_long = weekly_returns_long.rename(columns={'Date':'week_end'})   # (h)
weekly_returns_long.head()

# Load your news data
news_df = pd.read_csv('weekly_news.csv')

# Ensure correct data types
news_df['week_end'] = pd.to_datetime(news_df['week_end'])

# Preview to confirm
print(news_df.head())

merged = pd.merge(news_df, weekly_returns_long, on=['week_end','company'], how='left')  # (i)
merged.head()
# map sentiments consistently (optional)
merged['sentiment'] = merged['sentiment'].str.title()  # ensures 'positive', 'Positive' unify

summary = merged.groupby('sentiment')['weekly_return'].agg(['count','mean','std'])
print(summary)
summary['mean'].plot(kind='bar', yerr=summary['std'], figsize=(6,4), title='Mean Weekly Return by Sentiment')
plt.ylabel('Weekly Return (%)')
plt.show()

merged[merged['sentiment']=='Negative'].sort_values('weekly_return').head(10)