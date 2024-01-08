"""
simple moving average
exponential moving average over specific time window



"""


"""

Calculate moving average 

moving average = rolling or running avg
used to analyze time series data by calculating average of diff subsets of the complete dataaset
-it involves taking avg of dataset over time - also called moving mean or rolling mean

varius ways it can be calculated - one way is to take fixed subset from a complete
series of numbers - the first avg is calcualted by averaging the first fixed subset of nums and then subset is changed by moving forward to the next fixed subset

moving avg is mostly used with time series data to capture short-term fluctuations while focusing on longer trends

moving averages smoothens data

types of moving averages:
    simple moving average - uses sliding window to take avg over a set num of time periods - its an equally weighted mean of the previous n data
"""




"""
CALCULATE SMA FOR EACH MONTH
"""

#read in records from sold_data.csv

# "C:\Users\balma\Documents\Programming\Data Engineering\EuroClassic\backend_copy\Dummy_data_generator\sold_listings_dummy.csv"
import os
import pandas as pd
import numpy as np





file_path = os.path.join(os.path.dirname(__file__),'..','Dummy_data_generator/sold_listings_dummy.csv')
# print(os.path.isfile(file_path))

sold_data = pd.read_csv(file_path,header=None, names=['Year','Make','Model','Price','DateSold'])
 
#drop row 0  by index to remove text 
sold_data = sold_data.drop([0])
sold_data['Price'] = sold_data['Price'].astype(float)
sold_data['DateSold'] = pd.to_datetime(sold_data['DateSold'])

#extract month from each record in DateSold, and store in seperate col Sale_Month
sold_data['Sale_Month'] = sold_data['DateSold'].apply(lambda x:x.month)

#group all records by Sale_Month, from each group, get Price col and perform transform op
sold_data['SMA'] = sold_data.groupby('Sale_Month')['Price'].transform(lambda x:x.rolling(3,1).mean())
# print(sold_data)


"""
MAP final SMA val for each month to month number
#from each group, get the last sma val for the month group
#create df where we map the month number to the last sma value calcualted for that month

#first group by sale_month and select the sma col from each group
#get the last val of sma for each group
#reset the index, drop the sale_month index created by groupby
#.iloc[-1] retrieves last row of resulting series
"""

last_sma_val_each_month = sold_data.groupby('Sale_Month')['SMA'].last()
print(last_sma_val_each_month.tolist())

