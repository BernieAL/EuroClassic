import psycopg2
from Postgres.config import config
from simple_chalk import chalk

# this is a test connection file

def connect():
    """Connect to postgresql DB server"""

    conn = None
    try:

        #read in connection params from config.py, using config()
        params = config()

        #connect to PostgreSQL server
        print('Connecting to PostgreSQL database..')
        conn = psycopg2.connect(**params)

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


# callable function to create and return db connection
def get_db_connection():
    
    conn = None
    try:

        #read in connection params from config.py, using config()
        params = config()

        #connect to PostgreSQL server
        print(chalk.green('Connecting to PostgreSQL database..'))
        conn = psycopg2.connect(**params)

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
    

# if __name__=='__main__':
#     connect()