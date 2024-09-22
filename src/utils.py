import json
import os
from urllib.request import urlopen
import logging
import datetime

import certifi
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename='../data/utils.log', mode='w')
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(asctime)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


# functions for main_page
def xlsx_converting():
    """Function for converting excel-file to dataframe"""
    PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", 'operations.xlsx')
    logger.info('Попытка конвертации эксель-файла в датафрейм')
    try:
        py_from_xlsx = pd.read_excel(PATH)
        logger.info('Успешная конвертация')
        return py_from_xlsx
    except FileNotFoundError:
        logger.error('Некорректный путь')
        return ["Path is not correct"]


def get_greeting():
    """Function for identify part of day"""
    logger.info('Определение времени дня')
    hour_of_day = int(str(datetime.datetime.now())[11:13])
    greeting = ""
    if 4 <= hour_of_day <= 10:
        greeting = "Доброе утро"
    elif 11 <= hour_of_day <= 16:
        greeting = "Добрый день"
    elif 17 <= hour_of_day <= 22:
        greeting = "Добрый вечер"
    elif 23 <= hour_of_day or hour_of_day <= 3:
        greeting = "Доброй ночи"
    return greeting


def get_card_info(operations_df):
    """Function for getting info about cards"""
    logger.info('Получение информации по карте...')
    cards_list = operations_df["Номер карты"].unique()
    cards_dict = {}
    for card in cards_list:
        card_sum = operations_df.loc[operations_df["Номер карты"] == card, "Сумма платежа"].sum()
        cards_dict[f"{card}"] = {
            "last_digits": f"{card}",
            "total_spent": round(float(card_sum), 2),
            "cashback": round((float(card_sum) / 100), 2),
        }
    highest_five_operas = operations_df.sort_values(by="Сумма платежа", ascending=False).head()
    highest_five_list = []
    for i, column in highest_five_operas.iterrows():
        highest_five_list.append(
            {
                "date": column["Дата платежа"],
                "amount": column["Сумма платежа"],
                "category": column["Категория"],
                "description": column["Описание"],
            }
        )
    result_list = [value for key, value in cards_dict.items()] + [*highest_five_list]
    return result_list


def get_currencies_info(currencies_list):
    """Function for getting currencies information"""
    try:
        logger.info('Получение информации из валютного рынка')
        currency_info = []
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        courses = response.json()
        for valute in currencies_list:
            if courses["Valute"].get(valute):
                currency_info.append({"currency": valute, "rate": courses["Valute"][valute]["Value"]})
        return currency_info
    except ConnectionError:
        logger.error('Отсутствует подключение...')
        return 'Отсутствует подключение...'


def get_stocks(stocks_list):
    """Function for getting stocks information"""
    stocks_prices = []
    api_key = os.getenv("STOCKS_API_KEY")
    for stock in stocks_list:
        url = f"https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api_key}"
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        stock_info = json.loads(data)
        stock_price = stock_info[0].get("price")
        stocks_prices.append({"stock": f"{stock}", "price": f"{stock_price}"})
    return stocks_prices


print(get_stocks(['AAPL', 'GOOGL']))
