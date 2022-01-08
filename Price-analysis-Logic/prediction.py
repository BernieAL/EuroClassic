"""
linear regression visualized
https://stackoverflow.com/a/68733086

https://www.youtube.com/watch?v=vSzou5zRwNQ&ab_channel=ComputerScience
get data in as csv

split data:
    some for training 
    some for testing

"""

import pandas as pd

import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import lines
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,LSTM
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates

clean_output_CURRENT_LISTINGS= open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
clean_output_SOLD_DATA= open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")

df_SOLD_DATA = pd.read_csv("cleaned_data_SOLD_DATA.csv")

year_distribution = df_SOLD_DATA['Year'].value_counts()
print(year_distribution)

# Dropping Make and Model
data = df_SOLD_DATA.drop(df_SOLD_DATA.columns[[1,2]],axis=1)

# dropping any NA rows
data = data.dropna()
print(data)

x = pd.to_datetime(df_SOLD_DATA['DateSold'],'%d-%m-%Y')
y = df_SOLD_DATA['Price']


print(x.shape)
print(y.shape)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.1,random_state=2)

lin_reg_model = LinearRegression()
lin_reg_model.fit(x_train,y_train)










# data = df_SOLD_DATA
# data['DateSold'] = pd.to_datetime(df_SOLD_DATA['DateSold'])
# data.sort_values('DateSold',inplace = True)
# price_date = data['DateSold']
# price_sold = data['Price']

# plt.plot_date(price_date,price_sold,linestyle='solid')
# plt.gcf().autofmt_xdate()
# date_format = mpl_dates.DateFormatter('%d-%m-%Y')
# plt.gca().xaxis.set_major_formatter(date_format)
# plt.tight_layout()
# plt.title('Sale Prices For vehicle')
# plt.xlabel('Date')
# plt.ylabel('Sale Price')
# # plt.show()




# #plot sale avg as line in graph
# avg_price = price_sold.mean()
# print(avg_price)

# #plot inflationary rate as line in graph
# cum_inflation_rate = 17.4

# plt.plot(avg_price,cum_inflation_rate,linestyle='solid')
# plt.title('Avg sale Price vs Inflationary Price')
# plt.xlabel=('avg sale price')
# plt.ylabel=('avg inflation price')
# plt.show()



