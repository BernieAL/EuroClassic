
import psycopg2
import os,sys
import csv
#from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk

#load_dotenv(find_dotenv())     

#get parent dir 'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import DB_URI

def drop_tables(cur):


    drop_commands = """
    DROP TABLE IF EXISTS vehicles CASCADE;
    DROP TABLE IF EXISTS sold_listings;
    DROP TABLE IF EXISTS current_listings;
    DROP TABLE IF EXISTS sold_listing_stats;
    DROP TABLE IF EXISTS current_listing_stats;
    """
    
    try:
        cur.execute(drop_commands)
        conn.commit()
        print(chalk.green("All Tables Dropped - All statements completed successfully"))
        cur.close()

    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':

    conn = psycopg2.connect(DB_URI))
    cur = conn.cursor()
    drop_tables(cur)