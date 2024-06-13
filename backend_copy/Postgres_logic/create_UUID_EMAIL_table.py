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

"""

This table maps UUID, user Email, and user requested veh
The purpose of it is for when a vehicle isnt found and the client prompts the user for their email, which we need to associate with the requested veh
"""
def create_table(cur):

    command = """
    CREATE TABLE IF NOT EXISTS EMAIL_VEH_TABLE(
        UUID UUID PRIMARY KEY,
        EMAIL VARCHAR(50) NOT NULL,
        MAKE VARCHAR(50) NOT NULL,
        MODEL VARCHAR(50) NOT NULL,
        YEAR INTEGER NOT NULL
    );
    """

    try:
        cur.execute(command)
        conn.commit()
        print(chalk.green("UUID_EMAIL_TABLE CREATED SUCCESSFULLY"))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    conn = psycopg2.connect(DB_URI))
    cur = conn.cursor()
    create_table(cur)