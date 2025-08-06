from dotenv import load_dotenv
import os
import urllib.parse
import pandas as pd
import requests

load_dotenv()
api_key = os.getenv("float_api")
excelFile = os.getenv("excelFilePath")
print(excelFile)


if excelFile is None:
    raise ValueError("EXCEL_FILE not found in .env")

#print(f"API Key: {api_key}")

def skin_enconding(item):
    encoded_name = urllib.parse.quote(item)
    return encoded_name

def get_data_from_excel(excel):
    df = pd.read_excel(excel)
    #create a dictionary from the dataFrame
    return dict(zip(df.Nome, df.Quantidade))

def get_skin_price(inspect_link):
    link = os.getenv("float_link") + inspect_link
    headers = {
        "Accept": "application/json",
        "Authorization": os.getenv("float_api"),
    }

    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = data.get("data", [])
        price = results[0].get("price")
        return price/100

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except ValueError:
        print("Failed to parse JSON.")
    except Exception as e:
        print("Unexpected error:", e)



skins_dict = get_data_from_excel(excelFile)
#print(skins_dict)

for x in skins_dict:
    enconded_name = skin_enconding(x)
    price = get_skin_price(enconded_name)
    total_number_items = skins_dict[x]
    skins_dict["Total"] = price*total_number_items
    print(f"Skin: " + enconded_name + ": " + str(total_number_items))
    print(f"Price: " + str(price) + ", TOTAL: " + str(price*total_number_items))


print(skins_dict)
