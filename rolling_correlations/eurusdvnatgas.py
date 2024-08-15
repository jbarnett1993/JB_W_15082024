import pandas as pd
import matplotlib.pyplot as plt
from tia.bbg import LocalTerminal
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

# List of securities
sids = ['EURUSD Curncy', 'TZT1 Comdty']

# Retrieve historical price data for the past 5 years
pxs = LocalTerminal.get_historical(sids, "PX_LAST", dt.datetime.today() - relativedelta(years=5), dt.datetime.today())
pxs = pxs.as_frame()

rets = pd.DataFrame()
for sid in sids:
    rets[sid] = pxs[sid].pct_change()

rets.dropna(inplace=True)

window_size = 60

rolling_corrs = rets.rolling(window=window_size).corr()

base_security = sids[0]
other_securities = [sid for sid in sids if sid != base_security]

plt.figure(figsize=(14, 8))

for sid in other_securities:
    rolling_corr = rolling_corrs[base_security].unstack()[sid]
    plt.plot(rolling_corr)

    # Calculate and plot the average correlation as a horizontal red line
    avg_corr = rolling_corr.mean()
    plt.axhline(avg_corr, color='red', linestyle='--', )

plt.title(f'Rolling {window_size}-Day Correlations with Average Correlation')
plt.xlabel('Date')
plt.ylabel('Correlation')
# plt.legend(loc='upper center', bbox_to_anchor=(0.1, 1.15))
plt.grid(True)
plt.show()