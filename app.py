from flask import Flask,render_template,request
from scrape import scrape

app = Flask(__name__)

@app.route('/')
def homepage():
   return render_template('base.html')

@app.route('/search')
def search():
   return scrape()
   
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
