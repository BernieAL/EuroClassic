
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

# from scrape import test
# from config import Config


# from data_processing_scripts import handle_data
# from models import Car

import os
import configparser



app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://admin:s15koukie39@cluster0.7sxfp.mongodb.net/EURO_CLASSIC?retryWrites=true&w=majority"
#set up mongodb
mongodb_client = PyMongo(app) 
db = mongodb_client.db


db.cars.insert_many([
      { "year": 2001, "make": "BMW", "model": "M5", "chassis":"E39"},
      { "year": 1984, "make": "Ferrari", "model": "M3", "chassis":"E30"},
      { "year": 2007, "make": "Jaguar", "model": "M5", "chassis":"E60"},
      { "year": 2003, "make": "Keonigsegg", "model": "M5", "chassis":"E39"},
])


# db.car_makes.insert_many([
#    'Ferrar',
#    'BMW',
#    'Jaguar'
# ])

# #this calls function from data_processing_scripts which handles all the collecting and cleaning of data
# handle_data()






@app.route('/')
def homepage():

   #load full directory of cars and pass to template for autocomplete
   # car_directory = ['2000 BMW E39 m5', '2003 bmw e39 m5', '2001 bmw e39 m5']
   
   
   #hit db from here and load in all car brands and models
   
   #display brand options in dropdown
   makes_query = db.cars.find({},{"make":1,"_id":0})
   makes_array = []
   #extract literal make name from returned cursor object
   for makes in makes_query:
      makes_array.append(makes['make'])
   print(makes_array)
   
   
   # MODELS QUERY
   """If we send all models in db to template, we can use autocomplete in js
   to match to a model but first we have to pull all models from db and send to the template"""
   # models_query = db.cars.find({},{"make":1,"_id":0})
   # makes_array = []
   # #extract literal make name from returned cursor object
   # for makes in makes_query:
   #    makes_array.append(makes['make'])
   # print(makes_array)


   return render_template('home.html',makes_directory = makes_array)

@app.route('/search',methods=['GET','POST'])
def search():

   
  
   if request.method == 'POST':
      
      year = request.form['Year']
      make = request.form['Make']
      model = request.form['Model']

      car = f"{year} {make} {model}" 
      print(year)
      print(make)
      print(model)
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
      return render_template('data.html',car=car, car_results=json.dumps(car_results))
      # return "hello"
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






if __name__ == "__main__":
   
    app.run(debug=True)
# from . import models