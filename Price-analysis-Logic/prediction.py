"""


https://www.youtube.com/watch?v=vSzou5zRwNQ&ab_channel=ComputerScience
get data in as csv

split data:
    some for training 
    some for testing

"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
%matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

df = pd.read_csv("cleaned_data_CSV_dummy.csv")
df.head()


df["Price"]
