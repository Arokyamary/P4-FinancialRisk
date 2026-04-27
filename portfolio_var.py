import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

STOCKS = ['RELIANCE.NS','TCS.NS','INFY.NS','HDFCBANK.NS','ITC.NS',
'WIPRO.NS','LT.NS','ASIANPAINT.NS','MARUTI.NS','SUNPHARMA.NS']
PORTFOLIO_VALUE = 10_000_000

print('Fetching 5 years of NIFTY50 data...')
prices = yf.download(STOCKS, start='2019-01-01', progress=False)['Close']
returns = prices.pct_change().dropna()

weights = np.ones(len(STOCKS)) / len(STOCKS)
port_ret = returns.dot(weights)
var_hist = np.percentile(port_ret, 5)
print(f'Historical VaR 95%: {var_hist*100:.2f}%')
print(f'Max daily loss: Rs {abs(var_hist)*PORTFOLIO_VALUE:,.0f}')

print('Running 10,000 Monte Carlo simulations...')
n_sims = 10000
results = np.zeros((3, n_sims))
all_wts = []

for i in range(n_sims):
    w = np.random.random(len(STOCKS))
    w /= w.sum()
    all_wts.append(w)
    ret = np.sum(returns.mean() * w) * 252
    vol = np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
    results[0,i] = ret
    results[1,i] = vol
    results[2,i] = ret / vol

best = results[2].argmax()
print(f'Optimal Sharpe: {results[2,best]:.2f}')
print(f'Optimal Return: {results[0,best]*100:.1f}%')

plt.figure(figsize=(10, 6))
sc = plt.scatter(results[1], results[0], c=results[2], cmap='viridis', alpha=0.4, s=10)
plt.colorbar(sc, label='Sharpe Ratio')
plt.scatter(results[1,best], results[0,best], c='red', s=200, marker='*', label='Optimal')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.title('Efficient Frontier — 10K Monte Carlo Portfolios')
plt.legend()
plt.savefig('efficient_frontier.png', dpi=150, bbox_inches='tight')
print('Saved efficient_frontier.png')