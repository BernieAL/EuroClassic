
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# https://stackoverflow.com/questions/52596200/badrequestkeyerror
# https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
# https://dev.to/brunooliveira/flask-series-part-13-moving-our-recipes-data-source-to-the-server-4lm8
# https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo/
# https://github.com/akmamun/mvc-flask-pymongo

# https://www.mongodb.com/community/forums/t/keep-getting-serverselectiontimeouterror/126190/18
# https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo/
# https://www.mongodb.com/compatibility/setting-up-flask-with-mongodb
# https://github.com/mongodb-developer/flask-pymongo-example/blob/main/mflix/db.py
# https://analyticsindiamag.com/guide-to-pymongo-a-python-wrapper-for-mongodb/

# BY ROWS BY COL VAL PANDAS - https://stackoverflow.com/a/17071908


from dns import message
from flask import Flask, config,render_template,request
from flask_pymongo.wrappers import MongoClient
import pymongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, current
import json
from flask_pymongo import PyMongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# from scrape import test
# from config import Config

from data_processing_scripts import handle_data


import os
import configparser



app = Flask(__name__)

#MONGO CONNECTION AND CONFIGURATION
app.config['MONGO_URI'] = "mongodb+srv://admin:s15koukie39@cluster0.7sxfp.mongodb.net/EURO_CLASSIC?retryWrites=true&w=majority"
mongodb_client = PyMongo(app) 
db = mongodb_client.db


# db.cars.insert_many([
#         { "year": 2014, "make": "Audi", "model": "RS5", "chassis":""},
#         { "year": 2015, "make": "Audi", "model": "R8", "chassis":""},
#         { "year": 2001, "make": "Porsche", "model": "911", "chassis":""},
#         { "year": 2001, "make": "Porsche", "model": "911 GT2", "chassis":""},
#       { "year": 2001, "make": "BMW", "model": "M3", "chassis":""},
#       { "year": 1984, "make": "Ferrari", "model": "Laferrari", "chassis":""},
#       { "year": 1993, "make": "Ferrari", "model": "f50", "chassis":""},
#       { "year": 1993, "make": "Ferrari", "model": "Dino", "chassis":""},
#       { "year": 2015, "make": "Jaguar", "model": "xqj", "chassis":""},
#       { "year": 2001, "make": "BMW", "model": "M3", "chassis":""},
#       { "year": 1984, "make": "Ferrari", "model": "Laferrari", "chassis":""},
#       { "year": 1993, "make": "Ferrari", "model": "f50", "chassis":""},
#       { "year": 1993, "make": "Ferrari", "model": "Dino", "chassis":""},
#       { "year": 2015, "make": "Jaguar", "model": "xqj", "chassis":""},
#       { "year": 2015, "make": "Jaguar", "model": "M Type", "chassis":""},
#       { "year": 2015, "make": "Jaguar", "model": "R Type", "chassis":""},
#       { "year": 2015, "make": "Jaguar", "model": "s90", "chassis":""},
#       { "year": 2020, "make": "Keonigsegg", "model": "Agera", "chassis":""},
#       { "year": 2021, "make": "Keonigsegg", "model": "ccx", "chassis":""},
#       { "year": 2021, "make": "Keonigsegg", "model": "cc", "chassis":""},
#       { "year": 2001, "make": "BMW", "model": "335i", "chassis":""},
#       { "year": 2001, "make": "BMW", "model": "745i", "chassis":""},
# ])



# db.car_makes.insert_many([
#    'Ferrar',
#    'BMW',
#    'Jaguar'
# ])


# db.last_updated.insert_many([
#     { "make": "BMW", "model": "M3", last_scraped='12-27-2021'}
# ])






@app.route('/')
def homepage():

   
   
   #HIT DB AND RETRIEVE ALL MAKES AND MODELS TO POPULATE JS DROPDROWN ON TEMPLATE
   
   """:::::::ALL ENTRIES RESULT FORMAT:::::
   {'year': 2001, 'make': 'BMW', 'model': 'M5', 'chassis': 'E39'}
   {'year': 1984, 'make': 'Ferrari', 'model': 'M3', 'chassis': 'E30'}
   {'year': 2007, 'make': 'Jaguar', 'model': 'M5', 'chassis': 'E60'}
   {'year': 2003, 'make': 'Keonigsegg', 'model': 'M5', 'chassis': 'E39'}
   """
   #RETRIEVE ALL VEHICLE SEARCH OPTIONS (MAKES,MODELS)
   all_db_entries = db.cars.find({},{"_id":0})
   all_db_entries_array = []

   for i in all_db_entries:
      all_db_entries_array.append(i)
   # print(all_db_entries_array)

   #MAKES QUERY - for dropdown MAKE options, 1 = include this attribute, 0 = exclude this attribute
   makes_query = db.cars.find({},{"make":1,"_id":0})
   # Using set to omit duplicates
   makes_array = set()
   #extract literal make name from returned cursor object
   for makes in makes_query:
      makes_array.add(makes['make'])
   # print(makes_array)
   

   # MODELS QUERY - for dropdown MODEL options 1 = include this attribute,0 = exclude this attribute
   models_query = db.cars.find({},{"model":1,"_id":0})
   models_array = set()
   #extract literal make name from returned cursor object
   for model in models_query:
      models_array.add(model['model'])
   print(models_array)


   """all_db_entries is sent to home template and actively filtered in JS 
      we listen for changes in makes dropdown, take the selected value in makes dropdown
      and use it to get models who have the selected make

      this is done by iterating all_entries and finding elements that have makes which match
      the selected target make, we then get the 'model' value from this matching element and store it in array
      we then iterate this models array and create html elements in the dropdown for each model that has the target make
   """
   return render_template('home.html',makes_directory = makes_array,models_directory = models_array,all_db_entries_array=json.dumps(all_db_entries_array))



def test():
   print("this is a test function call")
#SEARCH CALLED FROM FORM SUBMISSION ON HOMEPAGE
#SEARCH CHECKS IS POST REQ
#GETS THE PARAMETERS OFF THE FORM
#CHECKS DB FOR LAST SCRAPE OF VEHICLE
#RETRIEVES SALES_DATA FOR THE VEHICLE AND SEND TO TEMPLATE TO BE RENDERED IN GRAPH W/ JS
@app.route('/search',methods=['GET','POST'])
def search():

   sale_records_array = []
   current_listing_records_array = []
   
  #get entered car entered in search form by user
   if request.method == 'POST':
      
      year = request.form['Year']
      make = request.form['Make']
      model = request.form['Model']
      
      car = f"{year} {make} {model}" 

      car_object = {
         'year':year,
         'make':make,
         'model':model
      }

      #CHECK IF DB HAS RECORDS FOR VEHICLE
      #GET ALL SALES RECORDS and CURRENT LISTINGS FROM DB FOR VEHICLE IF THEY EXIST - TO BE SENT TO TEMPLATE AND USED IN JS FOR GRAPHING
      sale_records_array = get_all_sale_records_from_db(model)
      current_listing_records_array = get_all_current_listing_records_from_db(model)
      print(f"SALE RECORDS ARRAY {sale_records_array}")
      print(f"CURRENT LISTING RECORDS ARRAY {current_listing_records_array}")
      
      if len(sale_records_array) == 0 or len(current_listing_records_array) == 0:
         print("NO RECORDS FOR THIS VEHICLE - INITIAL SCRAPE NEEDED")
         
         #FOR PRICE PREDICTION
         #CALL TO SCRAPE AND CLEANING FUNCTION - HANDLEDATA
         #FILES WILL BE POPULATED ONCE HANDLEDATA RUNS
         #THEN PASS TO PERFORM PREDICTION
         
         handle_data(car_object)
         
         #After handle_data populates clean_data_SOLD_DATA.csv and cleaned_data_CURRENT_LISTINGS.csv, write all records from SOLD_DATA to Sold_listings_clean DB collection 
         #And from CURRENT_LISTINGS to current_listings_clean DB collection

         insert_cleaned_scraped_sale_records_from_csv_to_db()
         insert_cleaned_scraped_current_listings_from_csv_to_db()
         sale_records_array = print(get_all_sale_records_from_db(model))
         current_listing_records_array = get_all_current_listing_records_from_db(model)
         print(f"SALE RECORDS ARRAY {sale_records_array}")
         print(f"CURRENT LISTING RECORDS ARRAY {current_listing_records_array}")
   
     

   # AFTER SCRAPE AND INSERT OF ALL RECORDS TO DB, PERFORM STATS

      #  current_listing_clean = open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
      #  sold_listings_clean = open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")
      
      #  predictionsAndStats()
    
      car_results = {
          "Nissan": [
            {"model":"Sentra", "doors":4},
            {"model":"Maxima", "doors":4},
            {"model":"Skyline", "doors":2}
        ],
      }
      # ------------------
      # sold_listings_clean = open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")
      # # print(sold_listings_clean)
      # sold_prices_for_car = []
      
      # for i in sold_listings_clean:
      #       indiv_line = i.split(',')
      #       try:
      #          sold_prices_for_car.append(indiv_line[3])
      #       except IndexError as e:
      #          pass
      # # print(len(sold_prices_for_car)) 
      # ------------------
      
      #PANDAS WORK
      # sortByYear(sold_listings_clean)
      
      print(f"SALE RECORDS ARRAY {sale_records_array}")
      return render_template('data.html',car=car, car_results=json.dumps(car_results),sales_records=json.dumps(sale_records_array))
      
   else:
      return "not post req"














@app.route('/about')
def about():
   return render_template('data.html')
   
@app.route('/login')
def login():
   return render_template('data.html')

@app.route('/signup')
def signup():
   return render_template('data.html')
   

@app.route('/account')
def account():
   return render_template('data.html')

# :::: END ROUTE HANDLERS ::::


# :::: BEGIN HELPER FUNCTIONS ::::

#reads in cleaned data from SOLD_DATA.csv and inserts into SALE_DATA collection in DB
def insert_cleaned_scraped_sale_records_from_csv_to_db():
      
      veh_year = []
      veh_model = []
      veh_sale_price = []
      veh_sale_date = []
      veh_make = []

      sold_listings_clean = open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")
      
      #splits line into individual attributes all stored in their own arrays
      for line in sold_listings_clean:
         listing = line.split(',')
         try:
            veh_year.append(listing[0])
            veh_make.append(listing[1])
            veh_model.append(listing[2])
            veh_sale_price.append(listing[3])
            veh_sale_date.append(listing[4].rstrip()) 
         except IndexError as E:
            pass
      
   
      # This inserts all entries from arrays into db in one go. Using inner for loop in insert_many
      db.sold_listings_clean.insert_many([{'Year':veh_year[i],   
                                 'Make':veh_make[i],
                                 'Model':veh_model[i],
                                 'Sale_price':veh_sale_price[i],
                                 'SaleDate':veh_sale_date[i]} for i in range(len(veh_model))])


def insert_cleaned_scraped_current_listings_from_csv_to_db():
      veh_year = []
      veh_model = []
      veh_list_price = []
      veh_make = []

      current_listings_clean = open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
      
      #splits line into individual attributes all stored in their own arrays
      for line in current_listings_clean:
         listing = line.split(',')
         try:
            veh_year.append(listing[0])
            veh_make.append(listing[1])
            veh_model.append(listing[2])
            veh_list_price.append(listing[3].rstrip())
         except IndexError as E:
            pass
      
   
      # This inserts all entries from arrays into db in one go. Using inner for loop in insert_many
      db.current_listings_clean.insert_many([{'Year':veh_year[i],   
                                 'Make':veh_make[i],
                                 'Model':veh_model[i],
                                 'List_price':veh_list_price[i]}for i in range(len(veh_model))])
                                 


#retrieve all entries from db for specific model to be sent to template and used in JS
def get_all_sale_records_from_db(model):

      # Find by model exclude Make and ID fields ONLY
      sale_records_query = db.sold_listings_clean.find({'Model':model},{'_id':0,'make':0,})
      #check if query returned empty
      if(sale_records_query):
         sale_records_array = []

         for model in sale_records_query:
            sale_records_array.append(model)

      # print(sale_records_array)
      return sale_records_array

def get_all_current_listing_records_from_db(model):
      # Find by model exclude Make and ID fields ONLY
      current_listing_records_query = db.current_listings_clean.find({'Model':model},{'_id':0,'make':0,})
      #check if query returned empty
      if(current_listing_records_query):
         current_listing_records_array = []

         for model in current_listing_records_query:
               current_listing_records_array.append(model)
      print(current_listing_records_array)
      return current_listing_records_array




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
   



#  ::: END HELPERS :::



if __name__ == "__main__":
   
    app.run(debug=True)
# from . import models