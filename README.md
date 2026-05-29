# Statistical-Analysis-of-Volatility-Mispricing-in-India-and-US-Markets--A-cross-Market-Garch-Study
A quant research project that tests whether **implied volatility** tends to be overpriced relative to **model-estimated volatility**.   The study compares **India (NIFTY + India VIX)** and **US (S&amp;P 500 + VIX)** using rolling GARCH forecasts, volatility spreads, and forward 5-day outcome testing.

---

## Overview

Financial markets continuously price uncertainty through options markets. One of the most widely followed measures of market uncertainty is the **Volatility Index (VIX)**, which represents the market's expectation of future volatility.

However, an important question remains:
> **Does the market systematically overprice or underprice future volatility?**
This project investigates that question by comparing **market-implied volatility (VIX)** with **model-estimated volatility forecasts generated using GARCH models** across Indian and US equity markets.
The objective is to identify periods where implied volatility appears statistically mispriced and determine whether those mispricings contain predictive information about future volatility movements.

---

# Research Motivation

Volatility is one of the most important variables in finance.
It influences:

* Option pricing
* Portfolio risk management
* Position sizing
* Hedging decisions
* Systematic trading strategies
* 
Despite its importance, volatility cannot be directly observed and must instead be estimated.
Market participants typically rely on two different measures:

### Implied Volatility (VIX)- Derived from option prices.
Represents: What the market expects volatility to be in the future.

### Forecasted Volatility (GARCH)- Generated from historical price behavior.
Represents: What statistical models estimate future volatility will be.
When these two measures diverge significantly, a potential mispricing may exist.

---

# Research Gap

Most introductory volatility studies focus on:

* Historical volatility
* Realized volatility
* Simple moving averages

## Few studies examine whether:
Extreme deviations between implied volatility and statistically forecasted volatility contain predictive information about future volatility direction.
Additionally, many retail studies focus on a single market.
This project extends the analysis by testing:

* India (NIFTY + India VIX)
* United States (S&P 500 + VIX)

and evaluating robustness across multiple rolling estimation windows.

---

# Understanding VIX

The VIX is often called the market's "fear gauge."
A higher VIX generally indicates:
* Greater uncertainty
* Higher demand for protection
* More expensive option premiums

For example:
* VIX = 12 → relatively calm market
* VIX = 30 → elevated uncertainty
* VIX = 50+ → extreme market stress

The VIX reflects what traders are willing to pay for protection against future market movements.

---

# Understanding GARCH

GARCH (Generalized Autoregressive Conditional Heteroskedasticity) is a statistical model designed to forecast future volatility.
Financial markets exhibit a phenomenon known as:
### Volatility Clustering

Periods of:

* High volatility tend to follow high volatility
* Low volatility tend to follow low volatility

GARCH models capture this behavior by estimating future volatility using past returns and past volatility.

In this project:

* Rolling GARCH(1,1) models are fitted
* Volatility forecasts are generated dynamically
* Forecasts are compared against market-implied volatility

---

# Research Hypothesis

The central hypothesis is:
## When implied volatility becomes significantly higher than model-estimated volatility, volatility may be overpriced and subsequently mean revert lower.

Mathematically:

Volatility Spread

Spread = VIX − GARCH Forecast

Large positive spreads imply:

* Market fear is elevated
* Implied volatility may be overpriced

Large negative spreads imply:

* Market complacency
* Implied volatility may be underpriced

---

# Methodology

## 1- Data Collection

Market Data:
* NIFTY 50 Index
* India VIX
* S&P 500 Index
* CBOE VIX
  
Data Source:
* Yahoo Finance

---

## 2- Return Calculation

Daily log returns are calculated:

rₜ = ln(Pₜ / Pₜ₋₁)

Log returns are preferred because they:

* Are additive through time
* Improve statistical properties
* Are commonly used in volatility modeling

---

## 3- Rolling GARCH Forecasting

Rolling windows tested:

* 100 Days
* 252 Days
* 500 Days

For each day:

1. Fit GARCH(1,1) using only historical data
2. Forecast 5-day future volatility
3. Convert forecast to annualized volatility

This avoids look-ahead bias.

---

## 4- Construct Volatility Spread

Spread = VIX − GARCH Forecast
This spread measures:
> The difference between market expectations and model expectations.

---

## 5- Statistical Normalization

The spread is transformed into a Z-Score:
Z = (Spread − Mean Spread) / Standard Deviation
This identifies statistically extreme volatility mispricings.

---

## 6- Signal Generation

### Short Volatility Setup
Z-Score > +1
Interpretation:
* Market volatility appears overpriced
* Expect volatility to decline

---

### Long Volatility Setup
Z-Score < -1
Interpretation:
* Market volatility appears underpriced
* Expect volatility to rise

---

## 7- Forward Testing

Future volatility movement is measured over the next:
* 5 Trading Days
Metrics evaluated:
* Average future VIX movement
* Hit rate
* Sharpe ratio
* T-statistic
* P-value

---

# 8- Results Summary

The strongest and most consistent finding across all experiments was:
> Short-volatility setups significantly outperformed long-volatility setups.
> 
### Key Findings
### India

Short-volatility signals:
* Hit rates between 55–60%
* Statistically significant
* Positive Sharpe ratios

Long-volatility signals:
* Weak predictive power
* Inconsistent results
* Limited statistical significance

---

### United States

Short-volatility signals:
* Hit rates between 58–63%
* Strong statistical significance
* Consistent across all rolling windows

Long-volatility signals:
* Failed to generate reliable forecasts
* Often performed worse than random chance

---

# Interpretation

The results suggest:
Markets tend to overprice fear more consistently than they underprice risk.
This aligns with the concept of the:
Volatility Risk Premium- Investors are often willing to pay a premium for downside protection.

As a result:
Implied Volatility > Realized Volatility, on average.
The observed mean reversion in volatility is consistent with decades of academic and practitioner research on volatility risk premia.

---

# Visual Outputs

The project generates:
### Volatility Forecast Analysis

* VIX vs GARCH Forecast (100D, 252D, 500D)
* India
* United States

### Mispricing Analysis

* Volatility Spread Plots
* Z-Score Behavior

### Signal Analysis

* Short Volatility Hit Rate Comparison
* Long Volatility Hit Rate Comparison
* Setup Count Comparisons

### Research Tables

* India vs US Comparison
* Rolling Window Robustness Analysis

---

# Technology Stack
* Python
* pandas
* numpy
* yfinance
* arch
* scipy
* matplotlib

---

# Key Takeaways

This study provides evidence that:

1. Volatility mispricing contains predictive information.
2. Short-volatility opportunities are more reliable than long-volatility opportunities.
3. The effect exists in both Indian and US markets.
4. Results remain robust across multiple rolling estimation windows.
5. Market participants appear to systematically overpay for volatility during periods of elevated fear.

---

# Future Improvements

Potential extensions include:

* EGARCH and GJR-GARCH models
* Future realized volatility forecasting
* Regime-based analysis
* Volatility term structure modeling
* Options strategy backtesting
* Machine learning volatility forecasts
* Volatility surface analysis

---

# Conclusion

This project demonstrates a complete quantitative research workflow:

* Data acquisition
* Feature engineering
* Volatility forecasting
* Statistical signal construction
* Hypothesis testing
* Cross-market validation

### The findings suggest that extreme positive deviations between implied and model-estimated volatility contain meaningful information about future volatility behavior, particularly for short-volatility opportunities. 

### The average move was about -0.3 percent in the next 5 days, which in its entirety cannot be considered as a strong alpha, but neverthless it sure add another layer of confirmation to our systems.

### The strongest evidence was observed in the US market, where periods of elevated implied volatility were followed by statistically significant volatility declines over the subsequent trading week.

