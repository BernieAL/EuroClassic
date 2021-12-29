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



clean_output_CURRENT_LISTINGS= open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
clean_output_SOLD_DATA= open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")

df_SOLD_DATA = pd.read_csv("cleaned_data_SOLD_DATA.csv")

# print(df_SOLD_DATA.dtypes)
# print(df_SOLD_DATA.describe(include='object'))

# print(df_SOLD_DATA['DateSold'])



df_x = df_SOLD_DATA['Price']
df_y = df_SOLD_DATA['DateSold']

# print(df_x.describe())
# print(df_y.describe())

# initialize linear regression model
reg = linear_model.LinearRegression()

x_train, x_test, y_train,y_test = train_test_split(df_x,df_y,test_size=0.33,random_state=42)
x_train = x_train.values.reshape(-1,1)
x_test = x_test.values.reshape(-1,1)
#train model
reg.fit(x_train,y_train)
