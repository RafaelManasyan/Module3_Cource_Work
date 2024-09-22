import json
from datetime import datetime
from typing import Optional
import logging

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import xlsx_converting

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
    return json.dumps(filtered_trans_by_cat.to_dict(orient='records'), ensure_ascii=False, default=str)
