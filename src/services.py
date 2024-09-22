import json
from math import ceil
import logging


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../data/services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(asctime)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def investment_bank(month: str, transactions: list[dict[str, any]], limit: int):
    """Function for summing a period cashback"""
    cashback = 0
    logger.info('Попытка подсчета кешбека')
    for trans in transactions:
        for k, v in trans.items():
            if k[0:7] == month and v > 0:
                cashback += round((ceil(v / limit)) * limit - v, 2)
    return json.dumps(cashback)
