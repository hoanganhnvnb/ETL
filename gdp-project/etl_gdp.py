import requests
import pandas as pd
import sqlite3
import numpy as np

from datetime import datetime
from bs4 import BeautifulSoup


def extract(url:str, table_attribs:list):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''
    response = requests.get(url)
    data = ""
    if response.status_code == 200:
        data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = soup.find_all('tbody')
    rows = tables[2].find_all('tr')
    for index, row in enumerate(rows):
        columns = row.find_all('td')
        if index == 0 or not columns:
            continue
        gdp = columns[2].get_text()
        if '—' in gdp or not columns[0].find('a'):
            continue
        country = columns[0].a.get_text()
        if country and gdp:
            data_insert = {
                'Country': country,
                'GDP_USD_millions': gdp
            }
            df_insert = pd.DataFrame(data_insert, index=[0])
            df = pd.concat([df, df_insert], ignore_index=True)
    return df


def transform(df:pd.DataFrame):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    gdp_list = df['GDP_USD_millions'].to_list()
    gdp_list = [float(gdp.replace(",", "")) for gdp in gdp_list]
    gdp_list = [np.round(gdp/1000, 2) for gdp in gdp_list]
    df['GDP_USD_millions'] = gdp_list
    df.rename(columns={'GDP_USD_millions': 'GDP_USD_billions'})
    return df


def load_to_csv(df:pd.DataFrame, csv_path:str):
    ''' This function saves the final dataframe as a `CSV` file
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path, index=False)


def load_to_db(df:pd.DataFrame, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    df = pd.read_sql(query_statement, sql_connection)
    print(df)

def log(msg:str, file_name:str):
    msg = str(msg)
    date_time_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(date_time_format)
    with open(file_name, "a") as log_file:
        log_file.write(f"{timestamp}: {msg}\n")

if __name__ == '__main__':
    url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
    table_attribs = ["Country", "GDP_USD_millions"]
    db_name = r'./data/World_Economies.db'
    table_name = 'Countries_by_GDP'
    csv_path = r'./data/Countries_by_GDP.csv'

    df = extract(url, table_attribs)
    df = transform(df)
    load_to_csv(df, csv_path)
    sql_connection = sqlite3.connect(db_name)
    load_to_db(df, sql_connection, table_name)

    query = f"SELECT * FROM {table_name} WHERE GDP_USD_millions >= 100"
    run_query(query, sql_connection)
