import json

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(get_operations_df):
    actual = spending_by_category(get_operations_df, 'Фастфуд', '07.06.2020 14:10:18')
    expected = pd.DataFrame({'Дата операции': ['2020-04-07 19:41:58'],
                             'Дата платежа': ['07.04.2020'],
                             'Номер карты': ['*7197'],
                             'Статус': ['OK'],
                             'Сумма операции': [-100.00],
                             'Валюта операции': ['RUB'],
                             'Сумма платежа': [-100.00],
                             'Валюта платежа': ['RUB'],
                             'Кэшбэк': [0],
                             'Категория': ['Фастфуд'],
                             'MCC': ['5814'],
                             'Описание': ['IP Yakubovskaya M. V.'],
                             'Бонусы (включая кэшбэк)': [2.00],
                             'Округление на инвесткопилку': [0.00],
                             'Сумма операции с округлением': [100.00]}, index=[1])
    expected['Дата операции'] = pd.to_datetime(expected['Дата операции'])
    expected_json = expected.to_json(orient='records', date_format='iso')
    assert json.loads(actual) == json.loads(expected_json)
