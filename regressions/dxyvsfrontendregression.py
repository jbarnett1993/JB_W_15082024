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

# Define the list of dependent variables and the independent variable
dependent_variable = ["DXY Curncy"]
independent_variables = ["USGG2YR Index"]

# Initialize the data manager
mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'

# Get the historical data for the dependent and independent variables
independent_data = mgr[independent_variables].get_historical(['PX_LAST'], start_date, end_date) * 100 
# change to returns if needed
# independent_data = independent_data - independent_data.shift(1)
independent_data.columns = [col[0] for col in independent_data.columns]

dependent_data = mgr[dependent_variable].get_historical(['PX_LAST'], start_date, end_date) 
# change to returns if needed
# dependent_data = dependent_data.pct_change()
dependent_data.columns = [col[0] for col in dependent_data.columns]

combined_data = pd.merge(dependent_data, independent_data, left_index=True, right_index=True)
combined_data = combined_data.dropna()

# Define the independent and dependent variables for the regression
X = combined_data[independent_variables]
y = combined_data[dependent_variable]

# Add a constant term to the independent variables
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(combined_data[independent_variables], combined_data[dependent_variable], color='#1f77b4',alpha=0.5)  # solid blue dots
most_recent_x = X[independent_variables].iloc[-1]
most_recent_y = y.iloc[-1]
plt.scatter(most_recent_x, most_recent_y, color='#ff0000', s=50)  # most recent data point in bright red

# Plot regression line
predictions = model.predict(X)
plt.plot(X[independent_variables], predictions, color='red', linewidth=1)  # regression line in bright red

# Regression equation and R^2
slope = model.params[independent_variables[0]]
intercept = model.params['const']
r_squared = model.rsquared
regression_eq = f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r_squared:.3f}"
print(model.summary())

# Place the regression equation on the plot
plt.text(0.05, 0.95, regression_eq, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', color='black')

plt.title('EURUSD vs 1y1y US-EU rates')
plt.xlabel('1y1y US-EU Rates')
plt.ylabel('EURUSD Curncy')
plt.grid(True)
plt.show()

# Print the summary of the model
print(model.summary())