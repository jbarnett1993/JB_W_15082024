import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from matplotlib import gridspec
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from tia.bbg import LocalTerminal

mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=3)).strftime('%Y-%m-%d')
end_date = (datetime.today())
# end_date = datetime.today().strftime('%Y-%m-%d')
# end_date = datetime.strptime('2023-12-15','%Y-%m-%d')

sid = ["EURUSD", "USDNOK", "GBPUSD", "USDCAD", "USDJPY", "USDSEK", "AUDUSD", "USDCHF", "NZDUSD","EURGBP","USDMXN","USDBRL" ]
dates = ["1W","1M","2M","3M","4M","6M","9M","1Y"]


with PdfPages ('charts/vol_term_structures.pdf') as pdf:
    for sid in sid:
        sids = []
        for date in dates:
            ticker = sid + "25R" + date + " Curncy" 
            sids.append(ticker)

        df = mgr.get_historical(sids, ['PX_LAST'], start_date, end_date)
        if df.isna().any().any():
            print("filling NaN values")
            df.fillna(method="ffill",inplace=True)


        percentiles = df.quantile([0.1, 0.25, 0.5,0.75,0.9])


        if len(dates) != len(df.columns):
            print(f"lenght mismatch between dates and columns, dates is {len(dates)} and columns is {len(df.columns)}")
            
        current_vol = df.iloc[-1]
        plt.figure(figsize=(10,7))
        plt.plot(dates,current_vol,label="current vol",marker="o")
        plt.fill_between(dates,percentiles.iloc[0],percentiles.iloc[4],color="blue",alpha=0.1,label="10/90 percentile")
        plt.fill_between(dates,percentiles.iloc[1],percentiles.iloc[3],color="blue",alpha=0.15,label="25/75 percentile")
        plt.plot(dates,percentiles.iloc[2],label="50th percentile",linestyle="--",color="red")
        plt.title(f"{sid} 25d RR Term Structure vs historical level (3y lookback)")
        plt.xlabel("Tenor")
        plt.ylabel("Risk Reversal")
        plt.legend()
        plt.grid(True)
        pdf.savefig()
        plt.close()