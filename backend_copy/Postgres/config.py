from configparser import ConfigParser


"""

-This reads database.ini file and returns connection params
-section is used to specify section name in a config file that contains the the required db connection details
-section here refers to [postgres] in database.ini
"""

# database_ini_path = 
    
def config(filename='Postgres/database.ini', section='postgresql'):

    #create a parser
    parser = ConfigParser()

    #read config file
    parser.read(filename)

    #get section, default to postgresql
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('section {0} not found in the {1} file'.format(section,filename))
    
    return db