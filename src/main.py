from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import xlsx_converting
from src.views import main_list_func


def main_function():
    py_file = xlsx_converting()
    main_list = main_list_func(py_file)
    categ_list = spending_by_category(py_file, 'Супермаркеты', '07.06.2020 14:10:18')
    # invest_cashback = investment_bank()
    return f'{main_list}\n{categ_list}'


print(main_function())
