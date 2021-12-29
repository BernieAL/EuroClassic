"""


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


clean_output_file_CURRENT_LISTINGS= open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
clean_output_file_SOLD_DATA= open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")


for line in clean_output_file_SOLD_DATA:





# #makes dataframes from csv
# df_CURRENT_LISTINGS = pd.read_csv(clean_output_file_CURRENT_LISTINGS)
# df_SOLD_DATA = pd.read_csv(clean_output_file_SOLD_DATA)

# print(df_SOLD_DATA.describe())

# # df_x = pd.DataFrame(df_CURRENT_LISTINGS, columns = df_CURRENT_LISTINGS['Price'])
# # print(df_x)