import psycopg2
from config import config
from simple_chalk import chalk


def drop_tables():


    commands = """
    DROP TABLE IF EXISTS vehicles CASCADE;
    DROP TABLE IF EXISTS sold_listings;
    DROP TABLE IF EXISTS current_listings;
    DROP TABLE IF EXISTS sold_listing_stats;
    DROP TABLE IF EXISTS current_listing_stats;
    """
    

    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(commands)
        conn.commit()
        print(chalk.green("All statements completed successfully"))
        cur.close()

    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    drop_tables()