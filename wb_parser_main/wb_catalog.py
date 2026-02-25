import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from wb_parser_configs.wb_selectors import WBSerachSelectors as WBS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import undetected_chromedriver as uc

def search_by_text(driver:"uc.Chrome",text:str):
    try:
#        search_input_filed=driver.find_element(*WBS.SEARCH_INPUT)
        wating_time=10
        search_input_filed = WebDriverWait(driver,wating_time).until(
            EC.element_to_be_clickable(WBS.SEARCH_INPUT)
        )

        search_input_filed.click()
        search_input_filed.clear()

        for char in text:
            search_input_filed.send_keys(char)
            time.sleep(0.1)

        search_input_filed.send_keys(Keys.ENTER)

        time.sleep(3)


    except Exception as e:
        print(f"ERROR: SEARCH ERROR: {e}")

def scroll_products(driver:"uc.Chrome"):

    print("Start scrolling")

    product_links = set()
    scroll_step=500

    last_height=driver.execute_script("return document.body.scrollHeight")
    
    while True:

        product_cards_container=driver.find_element(*WBS.PRODUCT_CARDS)
        product_cards=product_cards_container.find_elements(*WBS.PRODUCT_CARD)
   
        for card in product_cards:
            try:
                product_link=card.find_element(*WBS.PRODUCT_CARD_LINK).get_attribute("href")
                if product_link not in product_links:
                    product_links.add(product_link)
                    yield product_link
            except Exception as e:
                print(f"Ошибка функции {e}")
                continue

        current_position=driver.execute_script("return window.pageYOffset")
        
        while current_position<last_height:

            current_position+=scroll_step
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(0.2)
            
        time.sleep(3)
        new_height=driver.execute_script("return document.body.scrollHeight")
        
        if(new_height==last_height):
            break
        
        last_height=new_height