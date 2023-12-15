last_scrape_date_query = """
            SELECT *
            FROM vehicles
            WHERE MODEL = %s AND YEAR = %s and MAKE = %s
        """


all_sales_records_query = """
    SELECT * 
    FROM sold_listings
    WHERE MAKE = %s AND MODEL = %s AND Year = %s
"""

all_current_records_query = """
    SELECT * 
    FROM current_listings
    WHERE MAKE = %s AND MODEL = %s AND Year = %s
"""

sold_stats_query = """
    SELECT * 
    FROM sold_listing_stats
    WHERE MAKE = %s AND MODEL = %s AND Year = %s              
"""

current_stats_query = """
    SELECT * 
    FROM current_listing_stats
    WHERE MAKE = %s AND MODEL = %s AND Year = %s
"""