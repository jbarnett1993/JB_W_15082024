import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Define the start and end dates for the data
start_date = (datetime.today() - relativedelta(years=2)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# define sids
eur_sids = ["CESIEUR Index"]
usd_sids = ["CESIUSD Index"]

# Initialize the data manager
mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'

eur_data = mgr[eur_sids].get_historical(['PX_LAST'], start_date, end_date)  
eur_data.columns = [col[0] for col in eur_data.columns]

usd_data = mgr[usd_sids].get_historical(['PX_LAST'], start_date, end_date) 
usd_data.columns = [col[0] for col in usd_data.columns]

# Plot
plt.figure(figsize=(10, 6))

plt.plot(eur_data.index, eur_data['CESIEUR Index'], label='EUR Data Surprise Index', color='blue')
plt.plot(usd_data.index, usd_data['CESIUSD Index'], label='USD Data Surprise Index', color='green')


plt.title('Data Surprise - EUR v USD')
plt.xlabel('Date')
plt.ylabel('Data Surprise')
plt.legend()
plt.grid(True)

plt.show()