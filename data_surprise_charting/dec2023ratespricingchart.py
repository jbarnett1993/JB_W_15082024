import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
from dateutil.relativedelta import relativedelta

start_date = datetime(2023,3,1)
end_date = datetime(2023,12,30)

eur_sids = ["EZ0BCH DEC2023 Index"]
usd_sids = ["US0BCH DEC2023 Index"]
fx_sids = ["EURUSD Curncy"]

mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'

eur_data = mgr[eur_sids].get_historical(['PX_LAST'], start_date, end_date)  
eur_data.columns = [col[0] for col in eur_data.columns]

usd_data = mgr[usd_sids].get_historical(['PX_LAST'], start_date, end_date) 
usd_data.columns = [col[0] for col in usd_data.columns]

fx_data = mgr[fx_sids].get_historical(['PX_LAST'], start_date, end_date)
fx_data.columns = [col[0] for col in fx_data.columns]

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(eur_data.index, eur_data['EZ0BCH DEC2023 Index'], label='EUR Dec23 Pricing', color='blue')
ax1.plot(usd_data.index, usd_data['US0BCH DEC2023 Index'], label='USD Dec23 Pricing', color='green')
ax1.set_title('Dec2023 Pricing. EUR vs USD')
ax1.set_xlabel('Date')
ax1.set_ylabel('Cuts Priced (%)')
ax1.legend(loc='upper left')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(fx_data.index, fx_data['EURUSD Curncy'], label='EURUSD FX Rate', color='red', linestyle='--')
ax2.set_ylabel('EURUSD FX Rate')
ax2.legend(loc='upper right')

# Show the plot
plt.show()