import time
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from wb_parser_configs.wb_selectors import WBSelectors as WBS
from wb_parser_configs.wb_types import ProductData as PD

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import undetected_chromedriver as uc


def get_atributes_for_product(driver:"uc.Chrome"):
    try:
        expan_tab_btn=driver.find_element(*WBS.EXPAND_INFO_BTN)
        driver.execute_script("arguments[0].click();",  expan_tab_btn)
        time.sleep(1)
    except:
        print("cant found button")
        pass

    attributes={}

    try:
        tables = driver.find_elements(*WBS.TABLE)
        
        for table in tables:
            rows = table.find_elements(*WBS.ROW)

            for row in rows:
                try:
                    raw_key=row.find_element(*WBS.ROW_KEY)
                    raw_val=row.find_element(*WBS.ROW_VAL)

                    key=raw_key.text.strip()
                    val=raw_val.text.strip()

                    if key and val:
                        attributes[key]=val
                except:
                    continue
    except Exception as e:
        print(f"Attribites parsing error {e}")
    
    time.sleep(1)
    try:
        about_text=driver.find_element(*WBS.ABOUT).text
    except Exception as e:
        print(f"About text parsing error {e}")

    return attributes,about_text





def get_product_card(driver:"uc.Chrome", url):
    
    driver.get(url)
    wait_time_limit=30
    print("OPEN LINK")
    try:
        WebDriverWait(driver,wait_time_limit).until(
            EC.presence_of_element_located(WBS.RATING)
            )
        
    except TimeoutException:
        print("Page load time out")
        return None
    
    print("Page loaded")
    time.sleep(5)


    product_data = {
        PD.LINK: url,
        PD.ARTICLE: "",
        PD.NAME: "",
        PD.PRICE: "",
        PD.ABOUT: "",
        PD.IMAGES: "",
        PD.ATTRIBUTES: {}, 
        PD.SELLER_NAME: "",
        PD.SELLER_LINK: "",
        PD.PRODUCT_NUM: "",
        PD.RATING: 0.0,
        PD.REVIEVS_NUM: 0
        }

    NOT_FOUND="NotFound"
    field=PD.NAME
    try:
        product_data[field] = driver.find_element(*WBS.TITLE).text
    except:
        product_data[field] = NOT_FOUND

    field=PD.ARTICLE
    try:
        article_element = driver.find_element(*WBS.ARTCLE)
        article = article_element.text.strip()
        product_data[field]=article
    except:
        product_data[field]=NOT_FOUND

    field=PD.PRICE
    try:
        price_text = driver.find_element(*WBS.PRICE).text
        price_digits="".join(filter(str.isdigit,price_text))
        product_data[field] = price_digits
    except:
        product_data[field] = NOT_FOUND
    
    field=PD.RATING
    try:
        rating_text=driver.find_element(*WBS.RATING).text
        clean_rating = rating_text.replace(",", ".")
        product_data[field] = float(clean_rating)
    except Exception as e:
        product_data[field]=NOT_FOUND

    saller_name=PD.SELLER_NAME
    saller_link=PD.SELLER_LINK
    try:
        print("Try to parse name")
        info_tab=driver.find_element(*WBS.SELLER_INFO)
        product_data[saller_name]=info_tab.find_element(*WBS.SELLER_NAME).text
        product_data[saller_link]=info_tab.find_element(*WBS.SELLER_LINK).get_attribute("href")
    except:
        print("ERROR Try to parse ALT")
        try:
            product_data[saller_name]=driver.find_element(*WBS.SELLER_NAME_ALT).text
            product_data[saller_link]=driver.find_element(*WBS.SELLER_LINK_ALT).get_attribute("href")
        except:
            product_data[saller_name]=NOT_FOUND
            product_data[saller_link]=NOT_FOUND

    field=PD.IMAGES
    try:
        images_urls=[]
        image_container=driver.find_element(*WBS.IMAGES_CONTAINER)
        imges=image_container.find_elements(*WBS.IMAGES_ITEM)
        for img in imges:
            src = img.get_attribute("src")
            if src:
                hd_link = re.sub(r'/images/[^/]+/', '/images/big/', src)
                images_urls.append(hd_link)

        unique_images = list(set(images_urls))
        product_data["images"] = ", ".join(unique_images)
    except:
        product_data[field]=NOT_FOUND
    
    field=PD.REVIEVS_NUM
    try:
        activity=driver.find_element(*WBS.REVIEWS).text
        product_data[field]=activity
    except:
        product_data[field]=NOT_FOUND
        
    attr=PD.ATTRIBUTES
    about=PD.ABOUT
    try:
        product_data[attr],product_data[about]=(get_atributes_for_product(driver))
    except:
        product_data[attr]=NOT_FOUND
        product_data[about]=NOT_FOUND

    return product_data