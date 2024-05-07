# https://www.freecodecamp.org/news/how-to-dockerize-a-flask-application/


from datetime import date,datetime
from flask import Flask, redirect, url_for, request,flash,jsonify,session
import requests
from flask_cors import CORS
from flask import render_template
import json

from simple_chalk import chalk
# import pandas as pd
import os,sys
import uuid

#from Web_Scrape_Logic.scrape_runner_main import run_scapers
# from Data_Clean_Logic.clean_ebay_data import ebay_clean_data_runner
# from Data_Clean_Logic.clean_bat_data import bat_clean_data_runner

# from Analysis_Logic.sold_data_transformation import SOLD_max_and_avg_price_per_veh_year

import psycopg2
from Postgres_logic.connect import get_db_connection
from Postgres_logic.insert_data import populate_vehicles_dir_table
from forms import SearchForm

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

#get parent dir 'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from RabbitMQ_queues.scrape_producer import add_veh_to_queue

#import queries
from Postgres_logic.queries import (
    all_sales_records_NO_YEAR_query,
    all_current_records_NO_YEAR_query,
    sold_stats_query_NO_YEAR,
    current_stats_query_NO_YEAR
)


current_script_dir = os.path.dirname(os.path.abspath(__file__)) #backend/

BACKEND_ROOT = current_script_dir   #backend
VEH_REQ_QUEUE_DIR = os.path.join(BACKEND_ROOT,'Veh_Request_Queue') #backend/
VEH_REQ_QUEUE_FILE_PATH = os.path.join(VEH_REQ_QUEUE_DIR,'Veh_Request_Queue.csv')
CACHE_FILE_PATH = os.path.join(BACKEND_ROOT,'Cache','makes_cache.json')
# print(os.path.isfile(cache_file_path))


application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "http://localhost:3000"}})

application.secret_key =  os.getenv('APPLICATION_SECRET_KEY')

#test db connection
conn = get_db_connection()
cur = conn.cursor()



""" VEH MANUFACTURER CACHE INITIALIZATION
    On flask application startup - request is made to NHTSA api to retrieve all car makes
    this is then written to a cache file for later use on client side for input tokenization

    On Client side - when form submitted
        user input is tokenized
            -'year' token is identified using regex
            -'make' token is identified by checking if it occurs in cache file of makes
                if match found: return True, we now know that this token is the make
                if no match found: check remaining tokens in user input
                    if exists: this token is the make
        Once year is identified, the remaining tokens can be make or model
            so we check if a token appears in the makes cache
"""
def initialize_cache():
    try:
        
        """check date of last api requests
        New car manufacturers dont applicationear too often, we dont need to run this often - maybe once a month
        Opens cache file with read context, gets lastRetrievedDate which is first value in file
        closes file
        """
        with open(CACHE_FILE_PATH,'r') as cache_file:
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

            with open(CACHE_FILE_PATH,'w') as cache_file:
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

@application.route('/api', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        # If form is submitted and valid, make a POST request to the 'vehicleQuery' route with form data
        data = {
            'year': form.vehicle_year.data,
            'make': form.vehicle_make.data,
            'model': form.vehicle_model.data
        }
        response = requests.post(url_for('vehicleQuery', _external=True), json=data)
        # Process the response
        # if response.status_code == 200:
        #     return response.text  # Or any other appropriate response
        # # Process the response if needed

        if response.status_code == 200:
            if 'application/json' in response.headers.get('content-type',''):
                json_data = response.json()
                print(json_data)
                return json_data
            else:
                response_text = response.text
                print(response_text)
                return response_text
        else:
            print(f"error: {response.status_code}")
        
    return render_template('index.html', form=form)

@application.route('/api/vehicle-query',methods=['POST'])
def vehicleQuery():
    """end point called when form submitted on front end
       recieves user search query
    """
    try:
        #FOR TESTING WITHOUT REACT - uses form class for data
        #data = request.form 

        #FOR TESTING WITH REACT - recieves  as json object from client
        data = request.get_json()
        print(data)
        reqeusted_veh = {
            'year' : (data.get('year')),
            'make': (data.get('make')).upper(),
            'model': (data.get('model')).upper()
        }
       
        
        #checks if veh scrape is needed - if veh isnt in db or data is old, new scrape needed
        veh_scrape_status = DB_check_new_scrape_needed(reqeusted_veh)
        print(chalk.green(f"veh_scrape_status: {veh_scrape_status}"))
        
        """DB_check_new_scrape_needed returns obj:
            {
                'veh_found':True/False,
                'last_scrape_date': date obj,
                'scrape_needed':True/False
            }
        """
        
        """if scrape_needed == False -> veh is in db, and veh data IS NOT old
           retrieve all records  from DB for this veh
           Then return to front end
        """
        if veh_scrape_status['scrape_needed'] == False:   
            #get veh records from all tables and return as response
            print(chalk.green("::::::VEH SCRAPE NOT NEEDED::::::"))
            data_from_db = DB_execute_queries_and_store_results(cur,reqeusted_veh['make'],reqeusted_veh['model'])
            print(chalk.green(f"data from db{data_from_db}"))
            return jsonify(data_from_db)
        
        else:
            """new scrape needed - put veh in queue to perform scrape and email user the results

            write vehicle to queue file
            get email from user
                to get email, create uuid for this request,
                 and store requested veh data using uuid,  
                 then send uuid back to client in response

                on client side, prompt user for email, put email and uuid in obj and send back over to api

                in api, use uuid to find existing 
            initiate scrape,clean,analyze,push to db process

            """
            #gen uuid
            user_uuid = uuid.uuid4()
            
            #store uuid and requested veh info in db
            DB_insert_UUID_veh_request_NO_EMAIL(cur,user_uuid,reqeusted_veh)
            print(chalk.red("::::::VEH SCRAPE NEEDED::::::"))

            #return user_uuid in res to be used on client side
            res = {
                'status':'Not Found',
                'uuid': user_uuid,
                'msg': "Whoops, We Dont Have Any Stats For That Vehicle Right Now, We Just initiated a new analysis process just for you - and we'll email you with the results",
                'veh':reqeusted_veh,
            }

            #OLD - USING FILE AS QUEUE 
            # VEH_REQ_QUEUE_FILE = open(VEH_REQ_QUEUE_FILE_PATH,'w')
            # VEH_REQ_QUEUE_FILE.write(f"{veh['year']},{veh['make']},{veh['model']}")
            
            #TEMP SNIPPET - FOR TESTING W/O REACT - ADDED FOR TESTING 4-25-24
            #publish veh as message to VEH_QUEUE (RMQ PRODUCER) 
            user_record_email_and_veh_obj = {
                'email':'balmanzar883@gmail.com',
                'veh': {
                    'year': reqeusted_veh['year'],
                    'make': reqeusted_veh['make'],
                    'model': reqeusted_veh['model']         
                }
            }   
            add_veh_to_queue(user_record_email_and_veh_obj)
            # END TEST SNIPPET

            return jsonify(res)
            
           
    except Exception as e:
        print('Error',str(e))
        return jsonify({'error':str(e)})
        
@application.route('/api/update_email',methods=['POST'])
def update_email():
    try:
            
        data = request.get_json()
        print(chalk.green(f"(update_email) values rec'd: {data}"))
        uuid =  data['uuid']
        email = data['email']
        
        #update user record with new captured email recd from client
        DB_update_user_email_by_uuid(cur,uuid,email)
        
        #retrieve full record (email and veh) from db now that email has been updated
        user_record_email_and_veh_obj = retrieve_record_by_uuid(uuid)
        print(chalk.green(f"(update_email) retrieved record - {user_record_email_and_veh_obj}"))
        
        # #publish veh as message to VEH_QUEUE (RMQ PRODUCER)    
        add_veh_to_queue(user_record_email_and_veh_obj)
        
        return jsonify("SUCCESS")
        
    except Exception as e:
        print('Error',str(e))
        return jsonify({'error':str(e)})

@application.route('/api/retrieve_cache',methods=['GET'])
def retrieve_cache():

    with open(CACHE_FILE_PATH,'r') as cache_file:
        print(chalk.blue(':::::CHECKING FRESHNESS OF CACHE DATA:::::'))
        cache_data = json.load(cache_file)

    return cache_data

@application.route('/api/get_db_data',methods=['GET'])
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

@application.route('/api/get_data',methods=['GET'])
def return_data():
   """TESTING
    endpoint for js script to request non db data
    returned data will be used to populate the graphs/charts etc
   """
#    print(session['db_data'])
#    pd_result = SOLD_max_and_avg_price_per_veh_year()
#    print(pd_result)
#    return pd_result

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
    
    veh['year']
    make = veh['make']
    model = veh['model']
    print('make: '+make)
    print('model: '+model)

    #TESTING
    print(chalk.green(f"(check_new_scrape_needed)DB_check_new_scrape_needed- {veh}"))
    
    #check for last_scrape date of veh
    #returns datetime object in tuple -> (datetime.date(2021, 10, 5),)
    #to get date, use [0]
    last_scrape_date_query = """
            SELECT MAKE,MODEL,YEAR,LAST_SCRAPE_DATE
            FROM vehicles
            WHERE MODEL = %s AND MAKE = %s
    """

    try:
        cur.execute(last_scrape_date_query,(model,make))
        
        retrieved_veh_record = cur.fetchone() #returns tuple
        #TESTING
        print(chalk.green(f"(check_new_scrape_needed)retrieved_veh - {retrieved_veh_record}"))

        #if veh found
        if retrieved_veh_record != None:
            
            #get last_scrape_date off returned tuple 
            last_scrape_date = (retrieved_veh_record [3])
            print(chalk.green(f"(check_new_scrape_needed)LAST SCRAPED DATE: + {last_scrape_date}"))

            #update veh_scrape_status indicating veh was found
            veh_scrape_status['veh_found']=True

            #update veh_scrape_status with last_scrape_date
            veh_scrape_status['last_scrape_date']= last_scrape_date
            print(chalk.green(f"veh_scrape_status: {veh_scrape_status}"))

            curr_date = date.today()
            date_difference_days = (abs(last_scrape_date - curr_date)).days
            print(chalk.red(date_difference_days))
            #if last_scrape_date older than 7 days
            if date_difference_days > 7:
                veh_scrape_status['scrape_needed']=True
                return veh_scrape_status
            else:
                veh_scrape_status['scrape_needed']=False
                return veh_scrape_status
        
        #if veh not found, set scrape_needed to true
        else:

            veh_scrape_status['scrape_needed']=True
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
    print(f"sales records {all_sales_records_result}")

    cur.execute(all_current_records_NO_YEAR_query, (make, model))
    current_records_result = cur.fetchall() #returns list
    print(f"current records {current_records_result}")

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

def DB_insert_UUID_veh_request_NO_EMAIL(cur,user_uuid,veh):
    """
    This function inserts an entry into the EMAIL_VEH_TABLE table
    It maps a UUID to the user reqeusted vehicle
    Purpose being - to later add in the user entered email to map the requested vehicle to the users email - for use in emailing results to the user when scrape completed
    """
     
    EMAIL = 'NONE'
    MAKE = veh['make'].upper()
    MODEL = veh['model'].upper()
    YEAR = veh['year']
    user_uuid = str(user_uuid)
    # print(f"{EMAIL}{MAKE}{MODEL}{YEAR}{user_uuid}")
    try:

        sql="""
            INSERT INTO EMAIL_VEH_TABLE(UUID,EMAIL,MAKE,MODEL,YEAR)
            values(%s,%s,%s,%s,%s)
            """
        cur.execute(sql,(user_uuid,EMAIL,MAKE,MODEL,YEAR))
        print("SUCCESSFULLY CREATED ENTRY - MAPPING UUID AND VEH")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

def DB_update_user_email_by_uuid(cur,uuid,email):

    """
    find existing record by uuid, then update the email value to be rec'd  user_email value
    """

    sql = """
          UPDATE EMAIL_VEH_TABLE
          SET EMAIL = %s
          WHERE UUID = %s;
          """   
    try:
        cur.execute(sql,(email,uuid))
        print(f"SUCCESSFULLY UPDATED EMAIL FOR UUID {uuid}")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

def retrieve_record_by_uuid(user_uuid):
    """this retrieves the entire record from EMAIL_VEH_TABLE
       using uuid. Gets us email and veh to then be encapsulated as an object and returned
    """
    sql="""
         SELECT EMAIL,YEAR,MAKE,MODEL
         FROM EMAIL_VEH_TABLE
         WHERE UUID = %s
        """
    try:
        cur.execute(sql,(user_uuid,))

        """fetchone returns tuple
           Returned tuple from EMAIL_VEH_TABLE -> ('useremail@...com', 1995, 'BMW', 'M5') 
           DATA TYPE of Tuple values (email<str>, year<int>,make<str>,model<str>)
        """
        #retrive record matching uuid
        record = cur.fetchone()
        
        #get values off tuple and put into object 
        retrieved_record_obj = {
            'email':record[0],
            'veh':{
                'year':record[1],
                'make':record[2],
                'model':record[3]
            }
        }
        
        return retrieved_record_obj
    except (Exception, psycopg2.DatabaseError) as e:
            print(chalk.green(f"(retrieve_record_by_uuid) error: {e}"))


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

