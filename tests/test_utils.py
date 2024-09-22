import json
from unittest.mock import patch, MagicMock

import certifi

from src.utils import get_greeting, get_currencies_info, get_stocks, get_card_info


@patch('datetime.datetime')
def test_get_greeting(mock_date):
    mock_date = MagicMock
    mock_date.return_value = '2021-12-31 16:42:04'
    assert get_greeting() == 'Добрый день'
    mock_date.return_value = '2021-12-31 10:42:04'
    assert get_greeting() == 'Доброе утро'
    mock_date.return_value = '2021-12-31 23:42:04'
    assert get_greeting() == 'Доброй ночи'
    mock_date.return_value = '2021-12-31 20:42:04'
    assert get_greeting() == 'Добрый вечер'


def test_get_card_info(get_operations_df):
    assert get_card_info(get_operations_df) == [
        {'cashback': -1.64, 'last_digits': '*7197', 'total_spent': -164.0},
        {'amount': -64.0,
         'category': 'Супермаркеты',
         'date': '31.12.2021',
         'description': 'Колхоз'},
        {'amount': -100.0,
         'category': 'Фастфуд',
         'date': '07.04.2020',
         'description': 'IP Yakubovskaya M. V.'}]


@patch('src.utils.requests.get')
def test_get_currencies_info(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'Valute': {
            'USD': {'Value': 92.6962},
            'EUR': {'Value': 103.249}
        }
    }
    mock_get.return_value = mock_response
    assert get_currencies_info(["USD", "EUR"]) == [{'currency': 'USD', 'rate': 92.6962},
                                                   {'currency': 'EUR', 'rate': 103.249}]
    mock_get.assert_called_once_with("https://www.cbr-xml-daily.ru/daily_json.js")


@patch('src.utils.urlopen')
@patch('src.utils.os.getenv')
def test_get_stocks(mock_getenv, mock_urlopen):
    mock_getenv.return_value = 'test_api_key'
    stocks_list = ['AAPL', 'GOOGL']
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps([{"price": 100.5}]).encode('utf-8')
    mock_urlopen.return_value = mock_response
    expected_result = [
        {"stock": "AAPL", "price": "100.5"},
        {"stock": "GOOGL", "price": "100.5"}
    ]
    result = get_stocks(stocks_list)
    assert result == expected_result
    mock_urlopen.assert_called_with('https://financialmodelingprep.com/api/v3/profile/GOOGL?apikey=test_api_key',
                                         cafile=certifi.where())
