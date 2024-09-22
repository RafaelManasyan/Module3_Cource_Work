import json
import os

from dotenv import load_dotenv

from utils import (
    get_card_info,
    get_currencies_info,
    get_greeting,
    get_stocks,
)

load_dotenv()


def main_list_func(pd_file):
    """Main list function"""
    greeting = get_greeting()
    card_info = get_card_info(pd_file)
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")) as user_setts:
        setts = json.load(user_setts)
    currencies_info = get_currencies_info(setts["user_currencies"])
    stocks_info = get_stocks(setts["user_stocks"])
    response = ({
        "greeting": greeting,
        "cards": card_info,
        "currency_rates": currencies_info,
        "stock_prices": stocks_info,
    })
    return json.dumps(response, ensure_ascii=False)
