import json
from datetime import datetime
from typing import Optional
import logging

import pandas as pd
from dateutil.relativedelta import relativedelta


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../data/reports.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(asctime)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Function for filter transactions by category of spending"""
    logger.info('Попытка фильтрации транзакций по категории')
    last_day = pd.to_datetime(date, dayfirst=True) if date else datetime.today()
    first_day = last_day - relativedelta(months=3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    filtered_trans_by_date = transactions[
        (transactions["Дата операции"] >= first_day) & (transactions["Дата операции"] <= last_day)
    ]
    filtered_trans_by_cat = pd.DataFrame(filtered_trans_by_date[filtered_trans_by_date["Категория"] == category])
    return filtered_trans_by_cat.to_json(orient='records', date_format='iso')


df = pd.DataFrame({'Дата операции': ['31.12.2021 16:42:04', '07.04.2020 19:41:58'],
                   'Дата платежа': ['31.12.2021', '07.04.2020'],
                   'Номер карты': ['*7197', '*7197'],
                   'Статус': ['OK', 'OK'],
                   'Сумма операции': [-64.00, -100.00],
                   'Валюта операции': ['RUB', 'RUB'],
                   'Сумма платежа': [-64.00, -100.00],
                   'Валюта платежа': ['RUB', 'RUB'],
                   'Кэшбэк': [0, 0],
                   'Категория': ['Супермаркеты', 'Фастфуд'],
                   'MCC': ['5411', '5814'],
                   'Описание': ['Колхоз', 'IP Yakubovskaya M. V.'],
                   'Бонусы (включая кэшбэк)': [1.00, 2.00],
                   'Округление на инвесткопилку': [0.00, 0.00],
                   'Сумма операции с округлением': [64.00, 100.00]})
print(spending_by_category(df, 'Фастфуд', '07.06.2020 14:10:18'))
