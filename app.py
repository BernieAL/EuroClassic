
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# https://stackoverflow.com/questions/52596200/badrequestkeyerror

from flask import Flask,render_template,request
# from scrape import scrape

app = Flask(__name__)

@app.route('/')
def homepage():
   return render_template('home.html')

@app.route('/search',methods=['GET','POST'])
def search():
   if request.method == 'POST':
      t = request.get_data('searchTerm')
      return render_template('data.html',t=t)
   else:
      return render_template('base.html')

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
