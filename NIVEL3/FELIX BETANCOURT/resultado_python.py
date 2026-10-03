import pandas as pd
import numpy as np

# Load dataset and prepare calculations
df = pd.read_csv("Walmart_Sales.csv")
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
weekly = df.groupby('Date')['Weekly_Sales'].sum().reset_index()

# 2011 equivalent weeks
# Weeks 44 to 48 (5 weeks for Nov 2012)
# Weeks 49 to 52 (4 weeks for Dec 2012)
# Weeks 1 to 4 (4 weeks for Jan 2013)
# Base sales in 2011/2012:
w_2011_post = weekly[(weekly['Date'] >= '2011-11-04') & (weekly['Date'] <= '2012-01-27')].copy().reset_index(drop=True)

# Historical growth:
# 2011/2010 YoY: +1.86%
# 2012/2011 YoY: +2.52% (Expected scenario)
# In Q3 2012, there was a slight slowdown or variance. Let's look at historical YoY variations per week or standard error of weekly residuals.

# Residuals of YoY model between 2010 and 2011:
w_2010_post = weekly[(weekly['Date'] >= '2010-11-05') & (weekly['Date'] <= '2011-01-28')].copy().reset_index(drop=True)
errors_2011 = (w_2011_post['Weekly_Sales'] - w_2010_post['Weekly_Sales'] * 1.0186) / w_2011_post['Weekly_Sales']
std_err = errors_2011.std()
print("Std of weekly forecasting errors:", std_err)

# Base weekly sales:
base_weeks = w_2011_post['Weekly_Sales'].values

# Scenarios definition:
# Expected: +2.52% YoY (consistent with 2012 YTD growth)
# Optimistic: High consumer spending, strong Black Friday / Christmas, e.g. +5.0% YoY (or +2 std dev, around +5.5% to +6.0%)
# Pessimistic: Macro headwinds, higher unemployment/gas prices or weather disruption, e.g. 0.0% growth (flat vs 2011) or slight contraction (-2.0% YoY)

growth_pessimistic = 0.000   # Flat vs 2011 (0% growth) or e.g. -1.5%
growth_expected = 0.0252     # +2.52% YoY
growth_optimistic = 0.050    # +5.00% YoY (strong holiday season)

# Let's compute monthly:
# Nov: 5 weeks (indices 0 to 4)
# Dec: 4 weeks (indices 5 to 8)
# Jan: 4 weeks (indices 9 to 12)

nov_base = base_weeks[:5].sum()
dec_base = base_weeks[5:9].sum()
jan_base = base_weeks[9:13].sum()
tot_base = base_weeks.sum()

print(f"Base 2011 Nov: {nov_base:,.2f}")
print(f"Base 2011 Dec: {dec_base:,.2f}")
print(f"Base 2011 Jan: {jan_base:,.2f}")
print(f"Base Total: {tot_base:,.2f}")

scenarios = {
    'Pesimista (0.0% / Plano)': 0.00,
    'Esperado (+2.52%)': 0.0252,
    'Optimista (+5.0%)': 0.050
}

results = []
for name, g in scenarios.items():
    nov = nov_base * (1 + g)
    dec = dec_base * (1 + g)
    jan = jan_base * (1 + g)
    tot = nov + dec + jan
    results.append({'Escenario': name, 'Tasa': f"{g*100:+.2f}%", 'Nov 2012': nov, 'Dec 2012': dec, 'Jan 2013': jan, 'Total': tot})

df_res = pd.DataFrame(results)
print(df_res.to_string())
