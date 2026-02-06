import yfinance as yf 
import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

class PortfolioOptimizer:
    def __init__(self, tickers, start_date, end_date):
        """
        initialize portfolio optimizer

        tickers: list of stock symbols
        start_date: historical data start (string 'YYYY-MM-DD')
        end_date: historical data end
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.prices = None
        self.returns = None

    def fetch_data(self):
        """Download historical price data from Yahoo Finance"""
        print(f"Fetching data for {len(self.tickers)} tickers...")
        
        # Download with auto_adjust=True to get adjusted prices directly
        data = yf.download(
            self.tickers, 
            start=self.start_date, 
            end=self.end_date,
            auto_adjust=True,
            progress=False
        )
        
        # If single ticker, data is already a DataFrame with OHLCV columns
        if len(self.tickers) == 1:
            self.prices = data['Close'].to_frame()
            self.prices.columns = self.tickers
        else:
            # Multiple tickers - extract Close prices
            self.prices = data['Close']
        
        # Drop any missing values
        self.prices = self.prices.dropna()
        
        print(f"Downloaded {len(self.prices)} days of data")
        return self.prices
    
    def calculate_returns(self):
        """Calculate daily returns"""
        self.returns = self.prices.pct_change().dropna()
        return self.returns

    def equal_weight_portfolio(self):
        """Calculate equal-weight portfolio performance as baseline"""
        n_assets = len(self.tickers)
        weights = np.array([1/n_assets] * n_assets)

        portfolio_return = np.sum(self.returns.mean() * weights) * 252
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov() * 252, weights)))
        sharpe = portfolio_return / portfolio_std

        return {
            'weights': dict(zip(self.tickers, weights)),
            'return': portfolio_return,
            'volatility': portfolio_std,
            'sharpe': sharpe
        }

    def optimize_sharpe(self):
        """Find portfolio weights that maximize Sharpe ratio"""
        mu = expected_returns.mean_historical_return(self.prices)
        S = risk_models.sample_cov(self.prices)

        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        perf = ef.portfolio_performance(verbose=False)

        return {
            'weights': cleaned_weights,
            'return': perf[0],
            'volatility': perf[1],
            'sharpe': perf[2]
        }
    
    def optimize_min_volatility(self):
        """Find minimum volatility portfolio"""
        mu = expected_returns.mean_historical_return(self.prices)
        S = risk_models.sample_cov(self.prices)

        ef = EfficientFrontier(mu, S)
        weights = ef.min_volatility()
        cleaned_weights = ef.clean_weights()

        perf = ef.portfolio_performance(verbose=False)

        return {
            'weights': cleaned_weights,
            'return': perf[0],
            'volatility': perf[1],
            'sharpe': perf[2]
        }

    def calculate_efficient_frontier(self, n_points=100):
        """Calculate efficient frontier by solving for multiple target returns"""
        mu = expected_returns.mean_historical_return(self.prices)
        S = risk_models.sample_cov(self.prices)

        ef_min = EfficientFrontier(mu, S)
        ef_min.min_volatility()
        min_ret, min_vol, _ = ef_min.portfolio_performance()

        ef_max = EfficientFrontier(mu, S)
        ef_max.max_sharpe()
        max_ret, max_vol, _ = ef_max.portfolio_performance()

        target_returns = np.linspace(min_ret, max_ret, n_points)
        frontier_volatility = []

        for target in target_returns:
            try:
                ef = EfficientFrontier(mu, S)
                ef.efficient_return(target)
                _, vol, _ = ef.portfolio_performance()
                frontier_volatility.append(vol)
            except:
                frontier_volatility.append(np.nan)
        
        return target_returns, frontier_volatility