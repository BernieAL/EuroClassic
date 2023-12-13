import csv
import random
from datetime import datetime, timedelta
import os



# Function to generate random date within a range
def generate_random_date(start_date, end_date):
    return start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )


def sold_listing_dummy_generator():

    # Define the CSV file path
    csv_file_path = 'Dummy_data_generator\sold_listings_dummy.csv'

    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Create a CSV writer
        csvwriter = csv.writer(csvfile)

        # Write the header
        csvwriter.writerow(['Year', 'Make', 'Model', 'Price', 'DateSold'])

        # Generate 30 random listings
        for _ in range(30):
            year = random.randint(2010, 2022)
            make = 'Audi'
            model = 'R8'
            price = round(random.uniform(80000, 120000), 2)
            date_sold = generate_random_date(datetime(2022, 1, 1), datetime.now()).strftime('%Y-%m-%d')

            # Write the data to the CSV file
            csvwriter.writerow([year, make, model, price, date_sold])

    print(f'CSV file "{csv_file_path}" has been generated.')


def current_listing_dummy_generator():
    
    # Define the CSV file path
    csv_file_path = 'Dummy_data_generator\current_listings_dummy.csv'

    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
     # Create a CSV writer
        csvwriter = csv.writer(csvfile)

        # Write the header
        csvwriter.writerow(['Year', 'Make', 'Model', 'Price'])

        # Generate 30 random listings
        for _ in range(30):
            year = random.randint(2010, 2022)
            make = 'Audi'
            model = 'R8'
            price = round(random.uniform(80000, 120000), 2)
           

            # Write the data to the CSV file
            csvwriter.writerow([year, make, model, price])

    print(f'CSV file "{csv_file_path}" has been generated.')

sold_listing_dummy_generator()
# current_listing_dummy_generator()