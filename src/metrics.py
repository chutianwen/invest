from src.util import unit_transform
import numpy as np


class Metric:
    def __init__(self, invest_type, des, net_income, house_price_change, yield_income_ratio, yield_house_price_change_ratio):
        self.invest_type = invest_type
        self.des = des
        self.net_income = unit_transform(net_income)
        self.house_price_change = unit_transform(house_price_change)
        self.yield_income_ratio = unit_transform(yield_income_ratio)
        self.yield_house_price_change_ratio = unit_transform(yield_house_price_change_ratio)
        self.yield_ratio = unit_transform(list(np.array(yield_income_ratio) + np.array(yield_house_price_change_ratio)))

class AnnualFlowMetric(Metric):
    def __init__(self, invest_type, loan_balance, principal, interest, net_income, house_price_change,
                 yield_income_ratio, yield_house_price_change_ratio):
        self.invest_type = invest_type
        self.loan_balance = unit_transform(loan_balance)
        self.principal = unit_transform(principal)
        self.interest = unit_transform(interest)
        des = 'Annual'
        super().__init__(invest_type, des, net_income, house_price_change, yield_income_ratio, yield_house_price_change_ratio)


class AccumulativeMetric(Metric):
    def __init__(self, invest_type, expenses, net_income, house_price_change, yield_income_ratio,
                 yield_house_price_change_ratio):
        self.invest_type = invest_type
        self.expenses = unit_transform(expenses)
        des = 'Accumulative'
        super().__init__(invest_type, des, net_income, house_price_change, yield_income_ratio, yield_house_price_change_ratio)
