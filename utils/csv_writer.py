import csv
import os

from wb_parser_configs.wb_types import ProductData as PD

def append_to_csv(data: dict, filename: str = "wb_product_data.csv"):
        
        exists_file=os.path.isfile(filename)
        try:
            with open(filename, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=PD.HEADERS, delimiter=';')        
                if not exists_file:
                     writer.writeheader()

                data_copy=data.copy()
                attributes=data_copy.get(PD.ATTRIBUTES)

                if isinstance(attributes,dict):
                    fix_string="|".join([f"{key}: {val}" for key, val in attributes.items()])
                    data_copy[PD.ATTRIBUTES]=fix_string


                writer.writerow(data_copy)
        except Exception as e:
            print(f" Some error bt write csv function: {e}")