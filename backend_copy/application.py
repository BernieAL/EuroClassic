# https://www.freecodecamp.org/news/how-to-dockerize-a-flask-application/


from datetime import date,datetime
from flask import Flask, redirect, url_for, request,flash,jsonify,session
import requests
from flask_cors import CORS
from flask import render_template
import json

from simple_chalk import chalk
import pandas as pd
import os




from Web_Scrape_Logic.scrape import run_scrape
from Data_Clean_Logic.clean_data import clean_all_data
from Analysis_Logic.sold_data_transformation import SOLD_max_and_avg_price_per_veh_year

from config import Config

from Postgres.connect import get_db_connection
import psycopg2
from Postgres.config import config

application = Flask(__name__)
CORS(application)
application.config.from_object(Config)
application.secret_key = 'secret_key'

#test db connection
conn = get_db_connection()
cur = conn.cursor()

#import queries
from Postgres.queries import (
    all_sales_records_NO_YEAR_query,
    all_current_records_NO_YEAR_query,
    sold_stats_query_NO_YEAR,
    current_stats_query_NO_YEAR
)


cache_file_path = os.path.join(os.getcwd(),'Cache/makes_cache.json')
# print(os.path.isfile(cache_file_path))


""" Veh manufacturer cache initialization
on flask application startup - request is made to api to retrieve all car makes
this is then written to a cache file for later use on client side for input tokenization

On Client side - when form submitted
    user input is tokenized
        -year token is identified using regex
        -make token is identified by making request to flask application 
            and checking if the entered make exists in cache
            if exists: return True, we now know that this token is the make
            if didnt exist: check remaining token in user input
                if exists: this token is the make
    Once year is identified, the remaining tokens can be make or model
        so we check if a token applicationears in the makes cache
"""

def initialize_cache():
    try:
        
        """check date of last api requests
        New car manufacturers dont applicationear too often, we dont need to run this often - maybe once a month
        Opens cache file with read context, gets lastRetrievedDate which is first value in file
        closes file
        """
        with open(cache_file_path,'r') as cache_file:
            print(chalk.blue(':::::CHECKING FRESHNESS OF CACHE DATA:::::'))
            existing_data = json.load(cache_file)
            
            # convert retrieved string date value to specified format and then to a date obj
            lastRetrievedDate = datetime.strptime(existing_data[0], "%Y-%m-%d").date()

        """compare lastRetrievedDate with current date
           This tells us if we need to make a request to the api for new makes
        """
        date_difference_days = abs(lastRetrievedDate - date.today()).days
        if date_difference_days > 30:
            print(chalk.red(':::::CACHE DATA OLD - REQUESTING NEW DATA:::::'))
            response = requests.get('https://vpic.nhtsa.dot.gov/api//vehicles/GetMakesForVehicleType/car?format=json')

            new_data = response.json()['Results']

            """return record['MakeName'] from each record where
            record['VehicleTypeName'] == 'Passenger Car'], put results into a list
            """
            passenger_car_makes= [record['MakeName'] for record in new_data if record['VehicleTypeName'] == 'Passenger Car']
            
            # prepend current date
            passenger_car_makes.insert(0,f"{date.today()}")

            with open(cache_file_path,'w') as cache_file:
                json.dump(passenger_car_makes,cache_file)
            print(chalk.blue(':::::NEW DATA SUCCESSFULLY WRITTEN TO CACHE:::::'))

        print(chalk.blue(':::::CACHE DATA NOT OLD:::::'))
    except requests.RequestException as e:
        print(f"Error making API requst: {e}")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON:{e}")

    except IOError as e:
        print(f" Error writing to file: {e}")
initialize_cache()

# pd_result = process_cleaned_data()
# print(pd_result)

    



        # return redirect(url_for('home'))

    # otherwise reqeust == get, return search_form to use to be populated
    # return render_template('search_form.html', form=form)
    
    # car  = {
    # 'year':2017,
    # 'make':'Audi',
    # 'model':'Rs6'
    # }
    # scrapeFunc(car)
    


@application.route('/get_data',methods=['GET'])
def return_data():
   """TESTING
    endpoint for js script to request  non db data
    returned data will be used to populate the graphs/charts etc
   """
#    print(session['db_data'])
   pd_result = SOLD_max_and_avg_price_per_veh_year()
   print(pd_result)
   return pd_result
   

@application.route('/get_db_data',methods=['GET'])
def return_db_data():
    """
    endpoint for js script to request db data
    returned data will be used to populate the graphs/charts etc
    """

    #get params off request
    make = request.args.get('make')
    model = request.args.get('model')
    year = request.args.get('year')

    data = DB_execute_queries_and_store_results(cur,make,model,year)

    return jsonify(data)


@application.route('/',methods=['GET'])
def home():

    return "Hello"

@application.route('/vehicle-query',methods=['POST'])
def vehicleQuery():
    """end point called when form submitted on front end
       recieves user search query
    """
    try:
        
        data = request.json
        
        veh = {
            'year' : (data.get('year')),
            'make': (data.get('make')).upper(),
            'model': (data.get('model')).upper()
        }
        #TESTING
        # print(f"vehicleQuery {veh}")
        
        """ veh_scrape_status is obj
            
            veh_scrape_status = {
                'veh_found':False,
                'last_scrape_date': None,
                'scrape_needed':False
            }
        """
        veh_scrape_status = DB_check_new_scrape_needed(veh)
        # print(veh_scrape_status)
        
       #TESTING
        # veh_scrape_status['scrape_needed'] = False
        
        if veh_scrape_status['scrape_needed'] == False:
            """ If scrape not needed - means data isnt old, go to db and retrieve all records from all tables for this veh
            Then return to front end
            """     
            #get veh records from all tables and return
            print(chalk.green("::::::VEH SCRAPE NOT NEEDED::::::"))
            data_from_db = DB_execute_queries_and_store_results(cur,veh['make'],veh['model'])
            print(data_from_db)
            t = jsonify(data_from_db)
            print(t)
            return jsonify(data_from_db)
             
        
        else:
            """perform new scrape
               store new data into db
               retrieve from db and return to front end
            """
            
            # PERFORM SCAPE HERE 
            print(chalk.red("::::::VEH SCRAPE NEEDED::::::"))
            
            #this retrieves records from various tables in db matching make and model
            """ returns this 
                {
                "all_sales_records": all_sales_records_result,
                "current_records": current_records_result,
                "sold_stats": sold_stats_result,
                "current_stats": current_stats_result
                }
            """
            veh_data_from_db = DB_execute_queries_and_store_results(cur,veh['make'],veh['model'])
            
            VEH_EXISTS = veh_data_from_db['VEH_EXISTS']
            if VEH_EXISTS == False:
                print("veh doesnt exist in DB - will perform scrape and email when ready")
                return jsonify(veh_data_from_db)
            else:    
                print(veh_data_from_db)
                t = jsonify(data_from_db)
                # print(t)
                return jsonify(veh_data_from_db)
            
        

    except Exception as e:
        print('Error',str(e))
        return jsonify({'error':str(e)})
        
@application.route('/retrieve_cache',methods=['GET'])
def retrieve_cache():

    with open(cache_file_path,'r') as cache_file:
        print(chalk.blue(':::::CHECKING FRESHNESS OF CACHE DATA:::::'))
        cache_data = json.load(cache_file)

    return cache_data

# ==============================================================
# HELPER FUNCTIONS

def DB_check_new_scrape_needed(veh:object):

    """ Accepts: user request veh (year,make,model)

        Performs: 
            queries vehicles directory table in db to find target vehicle and get the last_scraped_date

            See CASES below


        Returns: 
                veh_scrape_status = {
                    'veh_found':True or False,
                    'last_scrape_date': None or found date,
                    'scrape_needed':True or False
                }
        
        Cases:
            -veh not found in db , return initial obj with default values
                {
                    'veh_found':False,
                    'last_scrape_date': None,
                    'scrape_needed':False
                }
            -veh found, last_scrape_date > 7 days ago, return initial obj with modified values
                {
                'veh_found':True,
                'last_scrape_date': date,
                'scrape_needed':True
                }
            
            -veh found, last_scrape_date < 7 days ago, return initial obj with modified values
            {
                'veh_found':True,
                'last_scrape_date': date,
                'scrape_needed':False
            }
            
    """

    veh_scrape_status={
                'veh_found':False,
                'last_scrape_date': None,
                'scrape_needed':False
            }
    
    year = veh['year']
    make = veh['make']
    model = veh['model']

    #TESTING
    print(f"DB_check_new_scrape_needed- {veh}")
    
    #check for last_scrape date of veh
    #returns datetime object in tuple -> (datetime.date(2021, 10, 5),)
    #to get date, use [0]
    last_scrape_date_query = """
            SELECT MAKE,MODEL,YEAR,LAST_SCRAPE_DATE
            FROM vehicles
            WHERE MODEL = %s AND YEAR = %s and MAKE = %s
    """

    try:
        cur.execute(last_scrape_date_query,(model,year,make))
        
        retrieved_veh = cur.fetchone() #returns tuple
        #TESTING
        # print(f"retrieved_veh - {retrieved_veh}")

        #if veh found
        if retrieved_veh:
            
            #get last_scrape_date off returned tuple 
            last_scrape_date = (retrieved_veh[3])

            #update veh_scrape_status indicating veh was found
            veh_scrape_status['veh_found']=True

            #update veh_scrape_status with last_scrape_date
            veh_scrape_status['last_scrape_date']= last_scrape_date


            curr_date = date.today()
            date_difference_days = (abs(last_scrape_date - curr_date)).days

            #if last_scrape_date older than 7 days
            if date_difference_days > 7:
              veh_scrape_status['scrape_needed']=True
              return veh_scrape_status
        
        #if veh not found, default obj values already set to False, return obj as is
        else:
            return veh_scrape_status
    
    except Exception as e:
        # Handle exceptions (print or log the error, or take applicationropriate action)
        print(f"Error: {str(e)}")
    

def DB_execute_queries_and_store_results(cur, make, model):
    """
    This function passes params to imported queries and executes them
    cur.fetchall() returns a list
    """  
    
    # Execute the queries
    cur.execute(all_sales_records_NO_YEAR_query, (make, model))
    all_sales_records_result = cur.fetchall() #returns list
    # print(all_sales_records_result)

    cur.execute(all_current_records_NO_YEAR_query, (make, model))
    current_records_result = cur.fetchall() #returns list

    """EMPTY CHECK
        if theres no sales records or current records for vehicle - return early with indication that vehicle doesnt exist in DB and do not execute rest of queries
    """
    if len(current_records_result) == 0 or len(all_sales_records_result) == 0:
        return {"VEH_EXISTS": False,
                "all_sales_records": [],
                "current_records": [],
                "sold_stats": [],
                "current_stats": []}
    

    cur.execute(sold_stats_query_NO_YEAR, (make, model))
    sold_stats_result = cur.fetchall() #returns list

    cur.execute(current_stats_query_NO_YEAR, (make, model))
    current_stats_result = cur.fetchall() #returns list
    
    # Return the results as a dictionary
    return {
        "VEH_EXISTS": True,
        "all_sales_records": all_sales_records_result,
        "current_records": current_records_result,
        "sold_stats": sold_stats_result,
        "current_stats": current_stats_result
    }


def custom_encoder(obj):
    """
    custom encoder for handle serialization of date objects
    puts it in iso formatted string representation
    if obj isnt date, raise TypeError

    what is iso formatted? -> YYYY-MM-DD
                    iso 8601 standardized date and time representation
                    way to express dates and time in universal format
    """
    if isinstance(obj,date):
        return obj.isoformat()
    raise TypeError("Type not serializable")


    


if __name__ == "__main__":
    application.run(debug=True,host='127.0.0.1', port=5000)

