import pytest
from src.services import investment_bank


@pytest.mark.parametrize(
    "month, trans_list, limit, expected",
    [('2020-04', [{'2020-04-07 19:41:58': 1342}, {'2021-12-31 16:42:04': 451}], 100, "58"),
     ('2021-12', [{'2020-04-07 19:41:58': 1342}, {'2021-12-31 16:42:04': 451}], 10, "9")])
def test_investment_bank(month, trans_list, limit, expected):
    assert investment_bank(month, trans_list, limit) == expected
