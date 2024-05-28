import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time

crypto_csv_table = 'Crypto_Automated_Pull.csv'

def automated_crypto_pull():
    try:
        url = 'https://coinmarketcap.com/currencies/bitcoin/'
        page = requests.get(url)
        page.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(page.text, 'html.parser')

        crypto_name_tag = soup.find('span', class_ = 'sc-d1ede7e3-0 bEFegK').text
        crypto_price_tag = soup.find('span', class_ = 'sc-d1ede7e3-0 fsQm base-text').text

        if crypto_name_tag and crypto_price_tag:
            crypto_name = crypto_name_tag.replace('\\xa0', '').replace('price', '')
            crypto_price = crypto_price_tag.replace('$', '').replace(',', '')

            date_time = datetime.now()
            data = {'Crypto Name': crypto_name,
                    'Price': float(crypto_price),
                    'TimeStamp': date_time}
            df = pd.DataFrame([data])

            if os.path.exists(crypto_csv_table):
                df.to_csv(crypto_csv_table, mode='a', header=False, index=False)
            else:
                df.to_csv(crypto_csv_table, index=False)

            print(df)
        else:
            print("Failed to find the required tags on the page.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

while True:
    automated_crypto_pull()
    time.sleep(5)
