import yfinance

df = yfinance.download("TSLA", start='2025-01-01', end='2025-08-01')
df.to_csv('TSLA.csv')