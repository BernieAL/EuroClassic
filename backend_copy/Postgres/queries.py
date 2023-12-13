last_scrape_date_query = """
            SELECT last_scrape_date
            FROM vehicles
            WHERE MAKE = make AND MODEL = model AND Year = year 
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