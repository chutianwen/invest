from src.util import unit_transform
import numpy as np


class Metric:
    def __init__(self, des, net_income, house_price_change, yield_income_ratio, yield_house_price_change_ratio):
        self.des = des
        self.net_income = unit_transform(net_income)[0]
        self.house_price_change = unit_transform(house_price_change)[0]
        self.yield_income_ratio = unit_transform(yield_income_ratio)[0]
        self.yield_house_price_change_ratio = unit_transform(yield_house_price_change_ratio)[0]
        self.yield_ratio = unit_transform(list(np.array(yield_income_ratio) + np.array(yield_house_price_change_ratio)))[0]

class AnnualFlowMetric(Metric):
    def __init__(self, invest_type, loan_balance, principal, interest, net_income, house_price_change,
                 yield_income_ratio, yield_house_price_change_ratio):
        self.invest_type = invest_type
        self.loan_balance = unit_transform(loan_balance)[0]
        self.principal = unit_transform(principal)[0]
        self.interest = unit_transform(interest)[0]
        des = f"{invest_type}_annual"
        super().__init__(des, net_income, house_price_change, yield_income_ratio, yield_house_price_change_ratio)


class AccumulativeMetric(Metric):
    def __init__(self, invest_type, expenses, net_income, house_price_change, yield_income_ratio,
                 yield_house_price_change_ratio):
        self.invest_type = invest_type
        self.expenses = unit_transform(expenses)[0]
        des = f"{invest_type}_accumulative"
        super().__init__(des, net_income, house_price_change, yield_income_ratio, yield_house_price_change_ratio)
