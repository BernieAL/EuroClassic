
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

from dns import message
from flask import Flask, config,render_template,request
from flask_pymongo.wrappers import MongoClient
import pymongo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from flask_pymongo import PyMongo
from pymongo import InsertMany
# from scrape import test
# from config import Config


# from data_processing_scripts import handle_data


import os
import configparser



app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://admin:s15koukie39@cluster0.7sxfp.mongodb.net/EURO_CLASSIC?retryWrites=true&w=majority"
#set up mongodb
mongodb_client = PyMongo(app) 
db = mongodb_client.db


# db.cars.insert_many([
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

   
   
   #HIT DB AND RETRIEVE ALL MAKES AND MODELS
   
   # This gets all db entries excluding their ID's
   """
   {'year': 2001, 'make': 'BMW', 'model': 'M5', 'chassis': 'E39'}
   {'year': 1984, 'make': 'Ferrari', 'model': 'M3', 'chassis': 'E30'}
   {'year': 2007, 'make': 'Jaguar', 'model': 'M5', 'chassis': 'E60'}
   {'year': 2003, 'make': 'Keonigsegg', 'model': 'M5', 'chassis': 'E39'}
   """
   
   #MAKES QUERY
   all_db_entries = db.cars.find({},{"_id":0})
   all_db_entries_array = []

   for i in all_db_entries:
      all_db_entries_array.append(i)

   # print(all_db_entries_array)

   #display make options in dropdown
   makes_query = db.cars.find({},{"make":1,"_id":0})
   makes_array = set()
   #extract literal make name from returned cursor object
   for makes in makes_query:
      makes_array.add(makes['make'])
   # print(makes_array)
   

   # MODELS QUERY
   models_query = db.cars.find({},{"model":1,"_id":0})
   models_array = []
   #extract literal make name from returned cursor object
   for model in models_query:
      models_array.append(model['model'])
   print(models_array)


   """all_db_entries is sent to home template and actively filtered in JS 
      we listen for changes in makes dropdown, take the selected value in makes dropdown
      and use it to get models who have the selected make

      this is done by iterating all_entries and finding elements that have makes which match
      the selected target make, we then get the 'model' value from this matching element and store it in array
      we then iterate this models array and create html elements in the dropdown for each model that has the target make
   """
   return render_template('home.html',makes_directory = makes_array,models_directory = models_array,all_db_entries_array=json.dumps(all_db_entries_array))

@app.route('/search',methods=['GET','POST'])
def search():

   
  #get entered car entered in search form by user
   if request.method == 'POST':
      
      year = request.form['Year']
      make = request.form['Make']
      model = request.form['Model']
      # print(year)
      # print(make)
      # print(model)

      car = f"{year} {make} {model}" 

      car_object = {
         'year':year,
         'make':make,
         'model':model
      }

      #check db for last scrape data


      # if handle_data(car_object):
      #       pass
      #       # # current_listing_clean = open("cleaned_data_CURRENT_LISTINGS.csv","r",encoding="utf-8")
      #       # # sold_listings_clean = open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")
      #       # predictionsAndStats()
      


      #car results = predictionsAndStats()
   
      # hit backend API to retrieve results for the specific car
      # api_response = handle_data(car)

      # hit backend API to retrieve results for the specific car
      # Return results to here and pass this to template to be rendered

      car_results = {
          "Nissan": [
            {"model":"Sentra", "doors":4},
            {"model":"Maxima", "doors":4},
            {"model":"Skyline", "doors":2}
        ],
      }

      sold_listings_clean = open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")
      # print(sold_listings_clean)
      sold_prices_for_car = []
      
      for i in sold_listings_clean:
            indiv_line = i.split(',')
            try:
               sold_prices_for_car.append(indiv_line[3])
               
            except IndexError as e:
               pass
      # print(len(sold_prices_for_car))   
      return render_template('data.html',car=car, car_results=json.dumps(car_results))
      # return "hello"
   else:
      return "not post req"

@app.route('/about')
def about():

   veh_year = []
   veh_model = []
   veh_sale_price = []
   veh_sale_date = []
   
   sold_listings_clean = open("cleaned_data_SOLD_DATA.csv","r",encoding="utf-8")
   

   for line in sold_listings_clean:
      listing = line.split(',')
      try:
         veh_year.append(listing[0])
         veh_model.append(listing[2])
         veh_sale_price.append(listing[3])
         veh_sale_date.append(listing[4])
      except IndexError as E:
         pass
   
   # bulk = db.sale_data.initializeUnorderedBulkOp();
   # sale_data_collection = db.sale_data
   # for i in len(veh_model):
   #    data = [
   #       InsertMany({
   #             "model":veh_model[i],
   #             "year":veh_year[i],
   #             "Sale price": veh_sale_price[i],
   #             "Sale Date":veh_sale_date[i]
   #             })]
   # db.sale_date.bulk_write(data)
   db.sale_data.insert_many([{'model':veh_model[i]} for i in range(len(veh_model))])

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






if __name__ == "__main__":
   
    app.run(debug=True)
# from . import models