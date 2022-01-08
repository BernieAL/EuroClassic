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
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,LSTM
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates

clean_output_CURRENT_LISTINGS= open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
clean_output_SOLD_DATA= open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")

df_SOLD_DATA = pd.read_csv("cleaned_data_SOLD_DATA.csv")


# Dropping Make and Model
data = df_SOLD_DATA.drop(df_SOLD_DATA.columns[[1,2]],axis=1)

#dropping any NA rows
data = data.dropna()
print(data)


data = df_SOLD_DATA
data['DateSold'] = pd.to_datetime(df_SOLD_DATA['DateSold'])
data.sort_values('DateSold',inplace = True)
price_date = data['DateSold']
price_sold = data['Price']

plt.plot_date(price_date,price_sold,linestyle='solid')
plt.gcf().autofmt_xdate()
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_formatter(date_format)
plt.tight_layout()
plt.title('Sale Prices')
plt.xlabel('Date')
plt.ylabel('Sale Price')
plt.show()













# start = dt.datetime(2015,1,1)
# end = dt.datetime(2020,1,1)

# # data = web.DataReader()

# scaler = MinMaxScaler(feature_range=(0,1))
# scaled_data = scaler.fit_transform(df_SOLD_DATA['Price'].values.reshape(-1,1))

# prediction_days = 20

# x_train = []
# y_train = []







# for x in range(prediction_days,len(scaled_data)):
#     x_train.append(scaled_data[x-prediction_days:x,0])
#     y_train.append(scaled_data[x,0])

# x_train,y_train = np.array(x_train), np.array(y_train)
# x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

# # model = Sequential()
# model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1],1)))
# model.add(Dropout(0.2))
# model.add(LSTM(units=50,return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(units=50))
# model.add(Dropout(0.2))
# model.add(Dense(units=1))

# model.compile(optimizer='adam',loss='mean_squaured_errors')
# model.fit(x_train,y_train,epochs=8,batch_size=32)




# # LOAD TEST DATA
# test_start = dt.datetime(2020,1,1)
# test_end = dt.datetime.now()

# test_data = df_SOLD_DATA
# actual_prices = test_data['Price'].values

# total_dataset = pd.concat((df_SOLD_DATA['Price'],test_data['Price']),axis=0)
# model_inputs = total_dataset[len(total_dataset)-len(test_data)-prediction_days:].values
# model_inputs = model_inputs.reshape(-1,1)
# model_inputs = scaler.transform(model_inputs)


# #make prediction on test data
# x_test = []
# for x in range(prediction_days,len(model_inputs)):
#     x_test.append(model_inputs[x-prediction_days:x,0])

# x_test = np.array(x_test)
# x_test = np.reshape(x_test,x_test.shape[0],x_test.shape[1],1)

# predicted_prices = model.predict(x_test)

# predicted_prices = scaler.inverse_transform(predicted_prices)

# plt.plot(actual_prices,color="black")
# plt.plot(predicted_prices,color="green")
# plt.xlabel('Time')
# plt.ylabel('price')

# plt.show()
# print(df_SOLD_DATA.dtypes)
# print(df_SOLD_DATA.describe(include='object'))

# print(df_SOLD_DATA['DateSold'])
 


# df_x = df_SOLD_DATA['Price']
# df_y = df_SOLD_DATA['DateSold']

# print(df_x.describe())
# print(df_y.describe())

# # initialize linear regression model
# reg = linear_model.LinearRegression()

# x_train, x_test, y_train,y_test = train_test_split(df_x,df_y,test_size=0.33,random_state=42)
# x_train = x_train.values.reshape(-1,1)
# x_test = x_test.values.reshape(-1,1)
# #train model
# reg.fit(x_train,y_train)
