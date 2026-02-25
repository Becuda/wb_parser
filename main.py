import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import wb_parser_main.wb_catalog as wb_catalog
import wb_parser_main.wb_product as wb_product
from  wb_parser_configs.wb_settings import Settings as wb_settings
import utils.csv_writer as CSV
import utils.driver as Driver

import time

def run_parsing():
    print("CREATE_DRIVER")
    driver = Driver.get_driver(wb_settings.HEADLESS_MODE)
    
    try:
        url=wb_settings.WB_HOME_URL
        print(f"DRIVER GET: {url}")
        driver.get(url)
        
        time.sleep(3)

        limit=wb_settings.MAX_PRODUCT_FOR_PARSSING
        if limit == 0:
            limit = 9999999
        count=0

        main_window=driver.current_window_handle
        wb_catalog.search_by_text(driver,wb_settings.SEARCH_TEXT)

        for link in wb_catalog.scroll_products(driver):

            if count >= limit:
                break

            driver.switch_to.new_window("tab")
            try:
                product_parsing(driver,link)
                count+=1

            except Exception as e:
                print(f"ERROR URL: {e}")
            
            finally:
                driver.close()
                driver.switch_to.window(main_window)
                time.sleep(1)

    except Exception as e:
        print(f"ERROR: {e}")
        
    finally:
        try:
            driver.quit()
        except OSError:
            print(f"ERROR: {e}") 

def product_parsing(driver, url):
    try:    
        product_data=wb_product.get_product_card(driver,url)
        CSV.append_to_csv(product_data,wb_settings.OUTPUT_FILE)
       
    except Exception as e:
        print(f"ERROR: {e}")
        
    

if __name__ == "__main__":
    run_parsing()