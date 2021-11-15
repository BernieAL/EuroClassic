
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# https://stackoverflow.com/questions/52596200/badrequestkeyerror

from flask import Flask,render_template,request
# from scrape import test
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
# from data_processing_scripts import handle_data
# from models import Car



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
if db:
   print('connected to db successfully')
migrate = Migrate(app,db)

# #this calls function from data_processing_scripts which handles all the collecting and cleaning of data
# handle_data()


@app.route('/')
def homepage():

   #load full directory of cars and pass to template for autocomplete
   car_directory = ['bmw e39 m5', '2003 bmw e39 m5', '2001 bmw e39 m5']
   return render_template('home.html',car_directory=json.dumps(car_directory))

@app.route('/search',methods=["GET","POST"])
def search():

   if request.method == 'POST':
      car = request.form

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


from . import models