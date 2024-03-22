from Web_Scrape_Logic.scrape_runner_main import run_scapers
from Data_Clean_Logic.clean_ebay_data import ebay_clean_data_runner
from Data_Clean_Logic.clean_bat_data import bat_clean_data_runner




def main_runner():

    run_scapers()
    ebay_clean_data_runner()

    #insert data to db
    