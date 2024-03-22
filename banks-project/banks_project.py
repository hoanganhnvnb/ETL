import pandas as pd
import numpy as np
import requests
import sqlite3

from datetime import datetime
from bs4 import BeautifulSoup

def extract(url:str, columns_table:list) -> pd.DataFrame:
    data = requests.get(url)
    df = pd.DataFrame(columns=columns_table)
    if data.status_code == 200:
        soup = BeautifulSoup(data.text, 'html.parser')
        tables = soup.find_all('tbody')
        rows = tables[0].find_all('tr')
        for index, row in enumerate(rows):
            if index != 0:
                columns = row.find_all('td')
                if not (names := columns[1].find_all('a')):
                    continue
                name = names[1].get_text()
                mc_usd = columns[2].get_text()
                data_insert = {
                    'Name': name,
                    'MC_USD_Billion': float(mc_usd)
                }
                df_insert = pd.DataFrame(data_insert, index=[0])
                df = pd.concat([df, df_insert], ignore_index=True)
    return df

def transform(df:pd.DataFrame) -> pd.DataFrame:
    # read exchange rate
    exchange = pd.read_csv("./data/source/exchange_rate.csv")
    usds = df['MC_USD_Billion']

    for currency, rate in exchange.values:
        df[f"MC_{currency}_Billion"] = [np.round(float(rate) * usd, 2) for usd in usds]

    return df

def load_to_csv(df:pd.DataFrame, csv_path:str):
    df.to_csv(csv_path, index=False)

def load_to_database(df:pd.DataFrame, sql_connector, table_name):
    df.to_sql(table_name, sql_connector, if_exists='replace', index=False)

def run_query(sql_connector, query):
    print(query)
    df = pd.read_sql(query, sql_connector)
    print(df)

def log(msg:str, file_name:str):
    date_format = "%y-%m-%d %H:%M:%S"
    date = datetime.now()
    date = date.strftime(date_format)
    path_log = f"./log/{file_name}.log"
    with open(path_log, 'a') as log_file:
        content = f"{date}: {msg}"
        log_file.write(content)


if __name__ == '__main__':
    url_extract = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
    csv_target_path = "./data/target/Largest_banks_data.csv"
    database_name = "./data/target/Banks.db"
    table_name = "Largest_banks"
    columns_extract = ['Name', 'MC_USD_Billion']

    df = extract(url=url_extract, columns_table=columns_extract)
    df = transform(df)
    load_to_csv(df, csv_target_path)
    sql_connector = sqlite3.connect(database_name)
    load_to_database(df, sql_connector, table_name)
    query = f"SELECT * FROM {table_name} LIMIT 5"
    run_query(sql_connector, query)