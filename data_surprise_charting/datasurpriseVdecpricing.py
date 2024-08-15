import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Define the start and end dates for the data
start_date = (datetime.today() - relativedelta(months=12)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# Define the list of dependent variables and the independent variable
eur_sids = ["CESIEUR Index","EZ0BCH DEC2024 Index"]
usd_sids = ["CESIUSD Index","US0BCH DEC2024 Index"]

# Initialize the data manager
mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'

# Get the historical data for the dependent and independent variables
eur_data = mgr[eur_sids].get_historical(['PX_LAST'], start_date, end_date)  
# change to returns if needed
# independent_data = independent_data - independent_data.shift(1)
eur_data.columns = [col[0] for col in eur_data.columns]

usd_data = mgr[usd_sids].get_historical(['PX_LAST'], start_date, end_date) 
# change to returns if needed
# dependent_data = dependent_data.pct_change()
usd_data.columns = [col[0] for col in usd_data.columns]

combined_data = pd.merge(eur_data, usd_data, left_index=True, right_index=True)
combined_data = combined_data.dropna()


