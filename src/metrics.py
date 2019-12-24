from src.util import unit_transform


class Metric:
    def __init__(self, des, net_income, house_price_change, roa_net_income, roa_house_price_change, roa_total):
        self.des = des
        self.net_income = net_income
        self.house_price_change = house_price_change
        self.roa_net_income = unit_transform(roa_net_income)
        self.roa_house_price_change = unit_transform(roa_house_price_change)
        self.roa_total = unit_transform(roa_total)


class SingleYrMetric(Metric):
    def __init__(self, loan_balance, principal, interest, net_income, house_price_change,
                 single_yr_roa_net_income, single_yr_roa_house_price_change, single_yr_roa_total):
        self.loan_balance = loan_balance
        self.principal = principal
        self.interest = interest
        des = 'Single year'
        super().__init__(des, net_income, house_price_change, single_yr_roa_net_income,
                         single_yr_roa_house_price_change, single_yr_roa_total)


class CompoundMetric(Metric):
    def __init__(self, assets, compound_net_income, compound_house_price_change,
                 compound_roa_net_income, compound_roa_house_price, compound_roa_total):
        self.assets = assets
        des = 'Compound'
        super().__init__(des, compound_net_income, compound_house_price_change, compound_roa_net_income,
                         compound_roa_house_price, compound_roa_total)
