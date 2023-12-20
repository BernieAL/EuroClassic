last_scrape_date_query = """
            SELECT *
            FROM vehicles
            WHERE MODEL = %s AND YEAR = %s and MAKE = %s
        """


# IF YEAR PROVIDED IN SEARCH QUERY
all_sales_records_with_year_query = """
    SELECT * 
    FROM sold_listings
    WHERE MAKE = %s AND MODEL = %s AND Year = %s
"""

all_current_records_with_year_query = """
    SELECT * 
    FROM current_listings
    WHERE MAKE = %s AND MODEL = %s AND Year = %s
"""

sold_stats_query_with_year = """
    SELECT * 
    FROM sold_listing_stats
    WHERE MAKE = %s AND MODEL = %s AND Year = %s              
"""

current_stats_query_with_year = """
    SELECT * 
    FROM current_listing_stats
    WHERE MAKE = %s AND MODEL = %s AND Year = %s
"""




#IF YEAR NOT PROVIDED IN SEARCH QUERY
all_sales_records_NO_YEAR_query = """
    SELECT * 
    FROM sold_listings
    WHERE MAKE = %s AND MODEL = %s 
"""

all_current_records_NO_YEAR_query = """
    SELECT * 
    FROM current_listings
    WHERE MAKE = %s AND MODEL = %s 
"""

sold_stats_query_NO_YEAR = """
    SELECT * 
    FROM sold_listing_stats
    WHERE MAKE = %s AND MODEL = %s              
"""

current_stats_query_NO_YEAR = """
    SELECT * 
    FROM current_listing_stats
    WHERE MAKE = %s AND MODEL = %s
"""

