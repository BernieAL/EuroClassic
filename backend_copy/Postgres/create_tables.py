import psycopg2
import os
import csv
from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk

load_dotenv(find_dotenv())     



""" this is the schema, it creates the tables in the db with a set of commands that we execute


    PK of vehicles table is composite key made of 
    make,model,year

    the rest of the tables have this pk as a foreign key
    this links the other tables to the vehicles table
"""

def create_tables(cur):

    
    commands = ( 
        #  # id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        """
        CREATE TABLE IF NOT EXISTS VEHICLES (
            ID UUID PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
            MAKE VARCHAR(50) NOT NULL,
            MODEL VARCHAR(50) NOT NULL,
            YEAR INTEGER NOT NULL,
            LAST_SCRAPE_DATE DATE
        );

        """,
        """
        CREATE TABLE IF NOT EXISTS SOLD_LISTINGS (
            ID UUID PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
            YEAR INTEGER NOT NULL,
            MAKE VARCHAR(50) NOT NULL,
            MODEL VARCHAR(50) NOT NULL,
            SALEPRICE FLOAT,
            DATESOLD DATE
        );

        """,
        """
        CREATE TABLE IF NOT EXISTS CURRENT_LISTINGS (
            ID UUID PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
            YEAR INTEGER NOT NULL,
            MAKE VARCHAR(50) NOT NULL,
            MODEL VARCHAR(50) NOT NULL,
            LISTPRICE FLOAT
        );

        """,
        """
        CREATE TABLE IF NOT EXISTS SOLD_LISTING_STATS (
            ID UUID PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
            YEAR INTEGER NOT NULL,
            MAKE VARCHAR(50) NOT NULL,
            MODEL VARCHAR(50) NOT NULL,
            SALEPRICE FLOAT,
            AVG_SALE_PRICE FLOAT,
            MAX_SALE_PRICE FLOAT,
            LOW_SALE_PRICE FLOAT,
            MOVING_AVG FLOAT
        );

        """,
        """
        CREATE TABLE IF NOT EXISTS CURRENT_LISTING_STATS (
            ID UUID PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
            YEAR INTEGER NOT NULL,
            MAKE VARCHAR(50) NOT NULL,
            MODEL VARCHAR(50) NOT NULL,
            LISTPRICE FLOAT, 
            VEHICLE_ID UUID
        );
        """
    )

    try:
        
        for command in commands:
                cur.execute(command)
                conn.commit()
        print(chalk.green("ALL TABLES CREATED SUCCESSFULLY - All statements completed successfully"))
        cur.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
             conn.close()

if __name__ == '__main__':
     
    conn = psycopg2.connect(os.getenv('DB_URI'))
    cur = conn.cursor()
    create_tables(cur)
