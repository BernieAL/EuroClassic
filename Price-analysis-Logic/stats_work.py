import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



"""
Reads in csv to DF, drops na columns
gets unique years as array
set up dictionary where each key is a unique year
iterate unique years, for each year, find rows in Df that have matching year,
   push to dictionary under year as key

ideal structure for dictionary:
   mydict = {
         1988: [all car record rows for 1988],
         1991: [all car reords rows for 1991],
         .....
      }
"""
def sortByYear(file):

   data = file
   data = pd.read_csv('./cleaned_data_SOLD_DATA.csv')
   data.dropna()

   t = data.groupby(['Year'])
   print(t)
   # unique_years = np.unique(data['Year'])
   # # print(unique_years)

   # # populate dictionary with unique years
   # mydict = {}
   # for i in unique_years:
   #    mydict[i] = i
   # # print(mydict)

   # #for each year in dict, find all rows with matching year,
   # #store in in array under that key
   # for i in unique_years:
   #    t = data.loc[data['Year']==i]
   #    mydict[i] = t
   # print(mydict)
   

