import numpy as np
from datetime import datetime
import smtplib
import time
import pandas


#For prediction
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

# cleaned_data = open("cleaned_data.csv","r",encoding="utf-8")
predictions = open("prediction_output.csv","a",encoding="utf-8")

df = pd.read_csv('cleaned_data.csv',skipinitialspace=True)
# print(df)

# df.set_index(df['Year'],inplace=True)

plt.plot(df['Price'])
plt.show

# Split data into testing and training sets
# X = np.array(df.drop(['Year']),1)
# Y = np.array(df['Price'])
train,test = train_test_split(df[['Price']], test_size=.5)


model = LinearRegression()
model.fit(train,test)

