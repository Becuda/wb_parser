
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import re
import pandas as pd
from wb_parser_configs.wb_types import ProductData as PD

RAITING_LIMIT=4.5
PRICE_LIMIT=10000
COUNTRY_FILTER="Россия"

def csv_data_filter(input_file,output_file):

    def country_filter(attributes_string:str, target_country:str):
        target_country_low=target_country.lower()
        attributes_string_low=attributes_string.lower()
        
        pattern=fr"(?:(страна производства)[^|]*:\s*.*{target_country_low})"
       
        is_ok=re.search(pattern,attributes_string_low)

        return bool(is_ok)
    try:
        df=pd.read_csv(input_file, sep=";", encoding='utf-8-sig')
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    df[PD.RATING] = df[PD.RATING].astype(float)
    df[PD.PRICE] = df[PD.PRICE].astype(float)
   
    filter_by_rating=df[(df[PD.RATING]>=RAITING_LIMIT)]
    print(filter_by_rating[PD.RATING])
    filter_by_price=filter_by_rating[(filter_by_rating[PD.PRICE]<PRICE_LIMIT)]
    print(filter_by_rating[PD.PRICE])
    filter_by_country=filter_by_price[filter_by_price[PD.ATTRIBUTES].apply(lambda x: country_filter(x, COUNTRY_FILTER))]

    if not filter_by_country.empty:
        filter_by_country.to_excel(output_file, index=False, engine='openpyxl')
    else:
        print(f"ERROR: not found {COUNTRY_FILTER}")
        return

if __name__ == "__main__":
    csv_data_filter("wb_product_result.csv", "wb_filtered.xlsx")