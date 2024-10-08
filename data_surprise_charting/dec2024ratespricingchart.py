import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
from dateutil.relativedelta import relativedelta

start_date = (datetime.today() - relativedelta(months=12)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

eur_sids = ["EZ0BCH DEC2024 Index"]
usd_sids = ["US0BCH DEC2024 Index"]

NFPdate = datetime(2024,8,2)

# Initialize the data manager
mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'

eur_data = mgr[eur_sids].get_historical(['PX_LAST'], start_date, end_date)  
eur_data.columns = [col[0] for col in eur_data.columns]

usd_data = mgr[usd_sids].get_historical(['PX_LAST'], start_date, end_date) 
usd_data.columns = [col[0] for col in usd_data.columns]

plt.figure(figsize=(10, 6))

plt.plot(eur_data.index, eur_data['EZ0BCH DEC2024 Index'], label='EUR Dec24 Pricing', color='blue')
plt.plot(usd_data.index, usd_data['US0BCH DEC2024 Index'], label='USD Dec24 Pricing', color='green')

plt.axvline(pd.to_datetime(NFPdate), color='red', linestyle='--', label='NFP')

plt.title('Dec2024 Pricing. EUR v USD')
plt.xlabel('Date')
plt.ylabel('Cuts Priced (%)')
plt.legend()
plt.grid(True)

plt.show()