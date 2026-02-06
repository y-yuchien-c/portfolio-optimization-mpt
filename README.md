# Portfolio Optimization using Modern Portfolio Theory

A quantitative framework for optimal portfolio allocation using mean-variance optimization and efficient frontier analysis. This project demonstrates risk-return tradeoffs and capital allocation strategies using real market data.

## Overview

This tool implements Harry Markowitz's Modern Portfolio Theory to construct optimal portfolios that maximize risk-adjusted returns. By analyzing historical price data across diversified equity holdings, the optimizer identifies portfolio weights that achieve superior Sharpe ratios compared to naive equal-weight strategies.

**Key Results:**
- **23.3% improvement** in Sharpe ratio vs. equal-weight baseline
- **16.1% reduction** in portfolio volatility using minimum variance strategy
- Interactive visualizations of the efficient frontier and allocation strategies

## Business Context

Modern Portfolio Theory addresses a fundamental challenge in asset management: **how to optimally allocate capital across multiple assets to achieve the best risk-adjusted returns**. This has direct applications to:

- **Wealth Management**: Constructing client portfolios aligned with risk tolerance
- **Proprietary Trading**: Allocating capital across trading strategies or market segments  
- **Risk Management**: Understanding diversification benefits and portfolio risk exposure
- **Product Strategy**: Evaluating tradeoffs in multi-product capital allocation decisions

The efficient frontier visualization reveals a critical insight: **there is no single "optimal" portfolio**, only optimal portfolios for a given risk tolerance. This framework enables data-driven conversations about risk-return preferences.

## Methodology

### 1. Data Collection
Historical adjusted closing prices retrieved via `yfinance` for a diversified portfolio:
- **Technology**: AAPL, MSFT, GOOGL
- **Financials**: JPM, GS
- **Healthcare**: JNJ, UNH
- **Consumer**: PG, KO
- **Energy**: XOM

**Time Period**: 3 years (2022-2025) to capture recent market regimes

### 2. Portfolio Optimization Approaches

**Equal-Weight Baseline**
- Naive diversification: 10% allocation to each asset
- Benchmark for measuring optimization value-add

**Maximum Sharpe Ratio**
- Optimization objective: Maximize return per unit of risk
- Uses mean-variance optimization with historical return estimates
- **Result**: 19.3% expected return, 19.4% volatility, 0.994 Sharpe ratio

**Minimum Volatility**  
- Optimization objective: Minimize portfolio variance
- Identifies the least risky combination given correlations
- **Result**: 5.5% expected return, 12.3% volatility, 0.445 Sharpe ratio

**Efficient Frontier**
- Trace the set of optimal portfolios across risk levels
- Reveals geometric relationship between risk and return
- Any portfolio below the frontier is suboptimal (dominated)

### 3. Statistical Assumptions & Limitations

**Assumptions:**
- Returns are normally distributed (may not hold during crisis periods)
- Historical correlations persist into the future
- No transaction costs or liquidity constraints
- Assets are infinitely divisible

**Known Limitations:**
- Mean-variance optimization is sensitive to return estimate errors (estimation risk)
- Historical volatility may understate tail risk
- Optimization can lead to concentrated positions without constraints
- Does not account for regime changes or structural breaks

**Production Considerations:**
- Add robust covariance estimators (e.g., shrinkage, exponential weighting)
- Implement position limits and diversification constraints
- Incorporate transaction cost modeling
- Use out-of-sample backtesting for validation

## Results

### Portfolio Allocation Comparison

The maximum Sharpe portfolio concentrates in higher-return assets (tech, financials) while the minimum volatility portfolio favors defensive sectors (consumer staples, healthcare). The efficient frontier analysis reveals the quantifiable cost of reducing risk: moving from max Sharpe (0.994) to min vol (0.445) cuts expected return by 71% while reducing volatility by only 37%.

**See visualizations:**
- [`weight_comparison.html`](visualizations/weight_comparison.html) - Interactive allocation breakdown
- [`efficient_frontier.html`](visualizations/efficient_frontier.html) - Risk-return tradeoff surface

### Performance Metrics

| Strategy | Expected Return | Volatility | Sharpe Ratio |
|----------|----------------|------------|--------------|
| Equal Weight | 11.84% | 14.69% | 0.806 |
| Max Sharpe | 19.31% | 19.43% | 0.994 |
| Min Volatility | 5.49% | 12.32% | 0.445 |

## Installation & Usage
```bash