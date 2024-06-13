import psycopg2

from simple_chalk import chalk
import os
from dotenv import load_dotenv, find_dotenv
import psycopg2
import time
import sys

     

#get parent dir 'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import DB_URI



"""Connection Option1 - This is a test connection function using DB URI from .env
"""
def test_connect_1():
    
    conn = None
    try:
        #connect to PostgreSQL server
        print('Connecting to PostgreSQL database..')
        # conn = psycopg2.connect(os.environ['DB_URI'])
        print(f"DB_URI {DB_URI}")
        conn = psycopg2.connect(DB_URI)    

        #create cursor
        cur = conn.cursor()

        #execute a statement
        print('postgreSQL database version:')
        cur.execute('SELECT version()')

        #display PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        #close communication with db server
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
# test_connect_1()


"""Connection Option2 - This is a test connection function using indiv .env vars
"""
def test_connect_2():
                                                                                      
    connection = psycopg2.connect(                                                  
        user = os.getenv("DATABASE_USERNAME"),                                      
        password = os.getenv("DATABASE_PASSWORD"),                                  
        host = os.getenv("DATABASE_IP"),                                            
        port = os.getenv("DATABASE_PORT"),                                          
        database = os.getenv("DATABASE_NAME")                                       
    )                                                                           
    cursor = connection.cursor()                                                    
    cursor.execute("SELECT version();")                                             
    record = cursor.fetchone()                                                      
    print(f"Database Version: {record}") 



"""This function returns an active PostgreSQL database connection instance 
    that functions can use to create a cursor object and perform database operations.

    Returns:
    psycopg2.extensions.connection: An active connection to the PostgreSQL database.
"""
def get_db_connection():
    
    conn = None
    try:
        print(chalk.green('Waiting before connecting to PostgreSQL database..'))
        time.sleep(10)  # Add a delay of 10 seconds (adjust as needed)

        #connect to PostgreSQL server
        print(chalk.green('Connecting to PostgreSQL database..'))
        conn = psycopg2.connect(DB_URI)

        #create cursor
        cur = conn.cursor()

        #execute a statement
        print(chalk.green('postgreSQL database version:'))
        cur.execute('SELECT version()')

        #display PostgreSQL database server version
        db_version = cur.fetchone()
        print(chalk.green(f"SUCCESS {db_version}"))

        return conn
    


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    

if __name__=='__main__':
    
    test_connect_1()