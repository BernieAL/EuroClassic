
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# https://stackoverflow.com/questions/52596200/badrequestkeyerror
# https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
# https://dev.to/brunooliveira/flask-series-part-13-moving-our-recipes-data-source-to-the-server-4lm8
# https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo/
# https://github.com/akmamun/mvc-flask-pymongo

# https://www.mongodb.com/community/forums/t/keep-getting-serverselectiontimeouterror/126190/18
# https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo/
# https://www.mongodb.com/compatibility/setting-up-flask-with-mongodb

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


# db.cars.insert_many([
#       { "year": 2001, "make": "BMW", "Model": "M5", "Chassis":"E39"},
#       { "year": 1984, "make": "BMW", "Model": "M3", "Chassis":"E30"},
#       { "year": 2007, "make": "BMW", "Model": "M5", "Chassis":"E60"},
#       { "year": 2003, "make": "BMW", "Model": "M5", "Chassis":"E39"},
# ])


# #this calls function from data_processing_scripts which handles all the collecting and cleaning of data
# handle_data()






@app.route('/')
def homepage():

   #load full directory of cars and pass to template for autocomplete
   # car_directory = ['2000 BMW E39 m5', '2003 bmw e39 m5', '2001 bmw e39 m5']
   
   # user_collection = db.todos.drop()
   #hit db from here and load in all car brands and chasis
   query = [db.cars.aggregate("Make")]
   car_directory = db.cars.find({make.data})
   for i in car_directory:
      print (i)
   #retrieve car brands and send as object to be iterated through in template
   #is there a way to load models once a brand has been selected so that they show up when model tab is selected


   return render_template('home.html',car_directory=car_directory)

@app.route('/search',methods=['GET','POST'])
def search():

   
  
   if request.method == 'POST':
      
      year = request.form['Year']
      make = request.form['Make']
      model = request.form['Model']

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
      return render_template('data.html',car="test", car_results=json.dumps(car_results))
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