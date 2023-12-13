import psycopg2
from config import config
from simple_chalk import chalk



""" 
    this is the schema, it creates the tables in the db with a set of commands that we execute


    PK of vehicles table is composite key made of 
    make,model,year

    the rest of the tables have this pk as a foreign key
    this links the other tables to the vehicles table
"""

def create_tables():

    
    commands = ( 
        #  # id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        """
        CREATE TABLE IF NOT EXISTS vehicles (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            make VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            year INTEGER NOT NULL,
            last_scrape_date date
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sold_listings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            year INTEGER NOT NULL,
            make VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            salePrice FLOAT,
            dateSold DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS current_listings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            year INTEGER  NOT NULL,
            make VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            listPrice FLOAT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sold_listing_stats (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            year INTEGER  NOT NULL,
            make VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            salePrice FLOAT,
            avg_sale_price FLOAT,
            max_sale_price FLOAT,
            low_sale_price FLOAT,
            moving_avg FLOAT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS current_listing_stats(
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            year INTEGER  NOT NULL,
            make VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            listPrice FLOAT, 
            vehicle_id UUID
        )
        
        """
        )

    conn = None
    try:
        #read the connectin params
        params = config()

        #connect to postgresql server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for command in commands:
                cur.execute(command)
                conn.commit()
        print(chalk.green("All statements completed successfully"))
        cur.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
             conn.close()

if __name__ == '__main__':
     create_tables()
