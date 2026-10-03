import pandas as pd
import numpy as np

# Load Walmart_Sales.csv
df = pd.read_csv('Walmart_Sales.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

weekly = df.groupby('Date')['Weekly_Sales'].sum().reset_index().sort_values('Date')
weekly_ts = weekly.set_index('Date')['Weekly_Sales']

# YoY weekly growth rate across historical weeks (week_t vs week_{t-52})
yoy_growth_rates = []
for i in range(52, len(weekly_ts)):
    growth = (weekly_ts.iloc[i] - weekly_ts.iloc[i-52]) / weekly_ts.iloc[i-52]
    yoy_growth_rates.append(growth)

avg_yoy = np.mean(yoy_growth_rates)
std_yoy = np.std(yoy_growth_rates)

print(f"Mean YoY Growth: {avg_yoy*100:.2f}%")
print(f"Std YoY Growth: {std_yoy*100:.2f}%")

# Historical weekly forecast error backtest (residuals)
test_actual = weekly_ts.loc['2011-11-04':'2012-10-26']
test_pred = weekly_ts.loc['2010-11-05':'2011-10-28'].values * (1 + avg_yoy)
pct_errors = (test_actual - test_pred) / test_pred

print(f"Mean Percentage Error: {np.mean(pct_errors)*100:.2f}%")
print(f"Std of Percentage Error: {np.std(pct_errors)*100:.2f}%")

# Base weeks
nov_11_sales = weekly_ts.loc[['2011-11-04', '2011-11-11', '2011-11-18', '2011-11-25', '2011-12-02']].values
dec_11_sales = weekly_ts.loc[['2011-12-09', '2011-12-16', '2011-12-23', '2011-12-30']].values
jan_12_sales = weekly_ts.loc[['2012-01-06', '2012-01-13', '2012-01-20', '2012-01-27']].values

# Baseline Expected (1.25% growth)
exp_nov = (nov_11_sales * (1 + avg_yoy)).sum()
exp_dec = (dec_11_sales * (1 + avg_yoy)).sum()
exp_jan = (jan_12_sales * (1 + avg_yoy)).sum()

# Optimistic (+1 std or +3% margin from backtest error / optimistic growth of +3.5%)
# Using confidence interval bounds on growth rate / MAPE bounds
# Pessimistic: YoY growth = -1.5% (or -2.84% MAPE downside)
# Optimistic: YoY growth = +4.0% (or +2.84% MAPE upside)

pess_growth = avg_yoy - 0.025 # -1.25% growth (downside macro pressures)
opt_growth = avg_yoy + 0.025 # +3.75% growth (strong holiday demand)

pess_nov = (nov_11_sales * (1 + pess_growth)).sum()
pess_dec = (dec_11_sales * (1 + pess_growth)).sum()
pess_jan = (jan_12_sales * (1 + pess_growth)).sum()

opt_nov = (nov_11_sales * (1 + opt_growth)).sum()
opt_dec = (dec_11_sales * (1 + opt_growth)).sum()
opt_jan = (jan_12_sales * (1 + opt_growth)).sum()

print("\n--- RESULTS ---")
print(f"Pessimistic Nov: {pess_nov:,.2f} | Expected: {exp_nov:,.2f} | Optimistic: {opt_nov:,.2f}")
print(f"Pessimistic Dec: {pess_dec:,.2f} | Expected: {exp_dec:,.2f} | Optimistic: {opt_dec:,.2f}")
print(f"Pessimistic Jan: {pess_jan:,.2f} | Expected: {exp_jan:,.2f} | Optimistic: {opt_jan:,.2f}")

tot_pess = pess_nov + pess_dec + pess_jan
tot_exp = exp_nov + exp_dec + exp_jan
tot_opt = opt_nov + opt_dec + opt_jan

print(f"\nTotal Trimestre -> Pesimista: {tot_pess:,.2f} | Esperado: {tot_exp:,.2f} | Optimista: {tot_opt:,.2f}")