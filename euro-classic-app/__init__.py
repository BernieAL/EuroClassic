
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# https://stackoverflow.com/questions/52596200/badrequestkeyerror

from flask import Flask,render_template,request
# from scrape import test
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from data_processing_scripts import handle_data
# from models import Car



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


handle_data()


@app.route('/')
def homepage():
   return render_template('home.html')

@app.route('/search',methods=["GET","POST"])
def search():

   if request.method == 'POST':
      #  car = request.form
       
      # return render_template('data.html',car=car)
      return "hello"
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