
# || IMPORT LIBRARIES ||

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model
from scipy.stats import ttest_1samp

START_DATE = "2020-01-01"
SHORT_Z = 1.0
LONG_Z = -1.0

# || MAIN RESEARCH FUNCTION ||

def run_vol_study(index_symbol, vix_symbol, market_name, rolling_window):

    print(f"\n{'='*70}")
    print(f"{market_name} | Rolling Window = {rolling_window} Days")
    print(f"{'='*70}")

    
    #  DOWNLOAD DATA

    index = yf.download(index_symbol, start=START_DATE)
    vix = yf.download(vix_symbol, start=START_DATE)

    # Keep only close prices
    index = index[['Close']].rename(columns={'Close':'Index_Close'})
    vix = vix[['Close']].rename(columns={'Close':'VIX_Close'})

    # Merge datasets
    data = pd.merge(index, vix, left_index=True, right_index=True, how='inner').dropna()

    
    #  COMPUTE RETURNS
    # Log returns stabilize variance for GARCH modelling

    data['log_returns'] = np.log(data['Index_Close'] / data['Index_Close'].shift(1))
    data.dropna(inplace=True)

    # GARCH prefers % returns
    returns = data['log_returns'] * 100

    
    # || ROLLING GARCH FORECAST ||
    
    forecasts = []

    for i in range(rolling_window, len(returns)):

        # Use only historical data → avoids lookahead bias
        train = returns.iloc[i-rolling_window:i]

        # Student-T handles fat tails better
        model = arch_model(train, vol='Garch', p=1, q=1, dist='t', rescale=False)
        fit = model.fit(disp='off')

        # Forecast next 5-day variance
        forecast = fit.forecast(horizon=5)

        # Extract 5th day variance
        variance = forecast.variance.values[-1, 4]

        # Convert variance → annualized volatility
        vol = (np.sqrt(variance) / 100) * np.sqrt(252)

        forecasts.append(vol)

    # || ALIGN FORECASTS ||
    
    data = data.iloc[rolling_window:]
    data['garch_forecast_5d'] = forecasts
    data['vix'] = data['VIX_Close'] / 100


    # || BUILD VOLATILITY SPREAD ||
    # Positive spread = implied volatility overpriced

    data['spread_5d'] = data['vix'] - data['garch_forecast_5d']

    # || Z-SCORE NORMALIZATION ||
    # Detect statistical extremes in volatility spread

    data['spread_mean'] = data['spread_5d'].rolling(60).mean()
    data['spread_std'] = data['spread_5d'].rolling(60).std()
    data['z_score'] = (data['spread_5d'] - data['spread_mean']) / data['spread_std']

    # || SIGNAL GENERATION ||
   
    data['short_setup'] = (data['z_score'] > SHORT_Z).astype(int)
    data['long_setup'] = (data['z_score'] < LONG_Z).astype(int)

    # || FUTURE VOLATILITY MOVE ||
    # Measure actual VIX movement over next 5 trading days

    data['future_vix_move_5d'] = data['vix'].shift(-5) - data['vix']
    data.dropna(inplace=True)

    # || SHORT VOL ANALYSIS ||
 
    short_data = data[data['short_setup']==1]['future_vix_move_5d']
    short_avg = short_data.mean()
    short_hit = (short_data < 0).mean()

    # Short-vol profits when VIX falls → invert sign
    short_returns = -short_data
    short_sharpe = (short_returns.mean()/short_returns.std()) * np.sqrt(252/5)
    short_t, short_p = ttest_1samp(short_data, 0)

    # ||LONG VOL ANALYSIS ||
   
    long_data = data[data['long_setup']==1]['future_vix_move_5d']
    long_avg = long_data.mean()
    long_hit = (long_data > 0).mean()
    long_sharpe = (long_data.mean()/long_data.std()) * np.sqrt(252/5)
    long_t, long_p = ttest_1samp(long_data, 0)

    
    # || PRINT RESULTS ||
  
    print(f"\nSHORT VOL RESULTS")
    print(f"Total setups: {len(short_data)}")
    print(f"Average future VIX move: {short_avg:.4f}")
    print(f"Hit rate (VIX falling): {short_hit:.2%}")
    print(f"Sharpe ratio: {short_sharpe:.4f}")
    print(f"P-value: {short_p:.6f}")

    print(f"\nLONG VOL RESULTS")
    print(f"Total setups: {len(long_data)}")
    print(f"Average future VIX move: {long_avg:.4f}")
    print(f"Hit rate (VIX rising): {long_hit:.2%}")
    print(f"Sharpe ratio: {long_sharpe:.4f}")
    print(f"P-value: {long_p:.6f}")

    
    # || VIX vs GARCH PLOT ||
    # Compare implied volatility vs model forecast

    plt.figure(figsize=(12,6))
    plt.plot(data.index, data['vix'], label='VIX')
    plt.plot(data.index, data['garch_forecast_5d'], label='GARCH Forecast')
    plt.title(f"{market_name} | VIX vs GARCH | {rolling_window}D Window")
    plt.legend()
    plt.savefig(f"{market_name}_{rolling_window}_vix_vs_garch.png", dpi=300, bbox_inches='tight')
    plt.show()

    
    # || SPREAD PLOT ||
    # Shows volatility mispricing over time

    plt.figure(figsize=(12,6))
    plt.plot(data.index, data['spread_5d'], label='VIX - GARCH Spread')
    plt.axhline(0, linestyle='--')
    plt.title(f"{market_name} | Volatility Spread | {rolling_window}D Window")
    plt.legend()
    plt.savefig(f"{market_name}_{rolling_window}_spread.png", dpi=300, bbox_inches='tight')
    plt.show()

    # || RETURN SUMMARY ||

    return {
        'Market': market_name,
        'Window': rolling_window,
        'Short Setups': len(short_data),
        'Short Hit Rate': short_hit,
        'Short Sharpe': short_sharpe,
        'Short P-Value': short_p,
        'Long Setups': len(long_data),
        'Long Hit Rate': long_hit,
        'Long Sharpe': long_sharpe,
        'Long P-Value': long_p
    }


# || INDIA STUDIES ||

india_100 = run_vol_study("^NSEI", "^INDIAVIX", "India", 100)
india_252 = run_vol_study("^NSEI", "^INDIAVIX", "India", 252)
india_500 = run_vol_study("^NSEI", "^INDIAVIX", "India", 500)

# || US STUDIES ||

us_100 = run_vol_study("^GSPC", "^VIX", "US", 100)
us_252 = run_vol_study("^GSPC", "^VIX", "US", 252)
us_500 = run_vol_study("^GSPC", "^VIX", "US", 500)

# || SHORT VOL HIT RATE COMPARISON ||

plt.figure(figsize=(12,6))
windows = ['100D','252D','500D']
india_short = [
    india_100['Short Hit Rate']*100,
    india_252['Short Hit Rate']*100,
    india_500['Short Hit Rate']*100
]
us_short = [
    us_100['Short Hit Rate']*100,
    us_252['Short Hit Rate']*100,
    us_500['Short Hit Rate']*100
]
x = np.arange(len(windows))
width = 0.35
plt.bar(x - width/2, india_short, width, color='blue', label='NIFTY')
plt.bar(x + width/2, us_short, width, color='red', label='S&P500')
plt.xticks(x, windows)
plt.ylabel('Hit Rate (%)')
plt.title('Short Volatility Signal Hit Rate Comparison')
plt.legend()
plt.savefig("short_vol_hitrate_comparison.png", dpi=300, bbox_inches='tight')
plt.show()


# || SHORT VOL SETUP COUNT COMPARISON ||

plt.figure(figsize=(12,6))

india_setups = [
    india_100['Short Setups'],
    india_252['Short Setups'],
    india_500['Short Setups']
]
us_setups = [
    us_100['Short Setups'],
    us_252['Short Setups'],
    us_500['Short Setups']
]
plt.bar(x - width/2, india_setups, width, color='blue', label='NIFTY')
plt.bar(x + width/2, us_setups, width, color='red', label='S&P500')
plt.xticks(x, windows)
plt.ylabel('Number of Signals')
plt.title('Short Volatility Setup Count Comparison')
plt.legend()
plt.savefig("short_vol_setup_counts.png", dpi=300, bbox_inches='tight')
plt.show()


# || LONG VOL HIT RATE COMPARISON ||


plt.figure(figsize=(12,6))
india_long = [
    india_100['Long Hit Rate']*100,
    india_252['Long Hit Rate']*100,
    india_500['Long Hit Rate']*100
]

us_long = [
    us_100['Long Hit Rate']*100,
    us_252['Long Hit Rate']*100,
    us_500['Long Hit Rate']*100
]

plt.bar(x - width/2, india_long, width, color='blue', label='NIFTY')
plt.bar(x + width/2, us_long, width, color='red', label='S&P500')

plt.xticks(x, windows)
plt.ylabel('Hit Rate (%)')
plt.title('Long Volatility Signal Hit Rate Comparison')
plt.legend()

plt.savefig("long_vol_hitrate_comparison.png", dpi=300, bbox_inches='tight')
plt.show()

# || LONG VOL SETUP COUNT COMPARISON ||

plt.figure(figsize=(12,6))

india_long_setups = [
    india_100['Long Setups'],
    india_252['Long Setups'],
    india_500['Long Setups']
]

us_long_setups = [
    us_100['Long Setups'],
    us_252['Long Setups'],
    us_500['Long Setups']
]

x = np.arange(len(windows))
plt.bar(x - width/2, india_long_setups, width, color='blue', label='NIFTY')
plt.bar(x + width/2, us_long_setups, width, color='red', label='S&P500')
plt.xticks(x, windows)
plt.ylabel('Number of Signals')
plt.title('Long Volatility Setup Count Comparison')
plt.legend()
plt.savefig(
    "long_vol_setup_counts.png",
    dpi=300,
    bbox_inches='tight'
)
plt.show()