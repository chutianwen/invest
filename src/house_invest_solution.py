from src.metrics import SingleYrMetric, CompoundMetric
from src.util import unit_transform, unified_unit


class HouseInvestSolution:
    a = 1
    def __init__(self, price, down_payment_ratio=0.0, mortgage_yr=0.0, interest_rate_yr=0.0,
                 hoa_month=0.0, maintain_yr=0.0, property_tax_yr=0.0, rent_month=0.0, house_price_change_yr=0.0):
        """
        Fundamental properties of this invest strategy
        """
        self.price = price
        self.down_payment_ratio = down_payment_ratio
        self.down_payment = down_payment_ratio * price
        self.mortgage_yr = mortgage_yr
        self.num_payment = self.mortgage_yr * 12
        self.interest_rate_yr = interest_rate_yr
        self.interest_rate_month = interest_rate_yr / 12
        self.hoa_month = hoa_month
        self.hoa_yr = hoa_month * 12
        self.maintain_yr = maintain_yr
        self.property_tax_yr = property_tax_yr
        self.rent_month = rent_month
        self.rent_yr = rent_month * 12
        self.rent_home_price_ratio_yr = self.rent_yr / self.price
        self.house_price_change_yr = house_price_change_yr
        self.loan = self.price - self.down_payment
        self.loan_payment = self.loan_payment()
        self.interest_total = self.loan_payment * self.num_payment - self.loan
        self.description()

    def short_description(self):
        return f"investment type: {self.invest_type()}\n" \
            f"house price:{unit_transform(self.price)[1]},down payment ratio:{self.down_payment_ratio * 100}%," \
            f"interest rate:{self.interest_rate_yr * 100}%,mortgage year:{self.mortgage_yr}, " \
            f"yearly hoa:{unit_transform(self.hoa_yr)[1]},yearly maintain:{unit_transform(self.maintain_yr)[1]}," \
            f"yearly property tax:{unit_transform(self.property_tax_yr)[1]},monthly rent:{unit_transform(self.rent_month)[1]}"

    def description(self):
        des = f"{self.short_description()},rental home price ratio:{unit_transform(self.rent_home_price_ratio_yr * 100)[0]}%," \
            f"total loan:{unit_transform(self.loan)[1]},total interest:{unit_transform(self.interest_total)[1]}," \
            f"monthly loan payment:{unit_transform(self.loan_payment)[1]}\n "
        print(des)
        return des

    def loan_payment(self):
        if self.mortgage_yr == 0 or self.down_payment_ratio == 1.0:
            return 0
        else:
            # discount Factor (D) = {[(1 + i) ^n] - 1} / [i(1 + i)^n]
            discount_factor = ((1 + self.interest_rate_month) ** self.num_payment - 1) / \
                              (self.interest_rate_month * (1 + self.interest_rate_month) ** self.num_payment)
            return self.loan / discount_factor

    def invest_type(self):
        if self.mortgage_yr == 0 or self.down_payment_ratio == 1.0:
            return f"full_cash"
        else:
            return f"{self.mortgage_yr}-year_mortgage"

    def experiment(self, target_yr, debug=False):
        # data for each month
        loan_balance_month = []  # remaining loan at current month
        principal_paid_month = []  # paid principal at each month
        interest_paid_month = []  # paid interest at each month
        income_month = []  # income at each month, deduct hoa, interest
        asset_month = []  # total paid house price till current month
        # data for each year
        loan_balances = []  # remaining loan at current year
        principals = []  # paid principal at each year
        interests = []  # paid interest at each year
        net_incomes = []  # net income at each year
        house_price_changes = []  # house price change at each year compared to last year
        assets = []  # total paid house price till current year
        single_yr_roa_net_incomes = []  # net_incomes_yr / assets_yr at Nth year
        single_yr_roa_house_price_changes = []  # house_price_change_yr / assets_yr at Nth year
        single_yr_roa_totals = []
        # accumulate n years back.
        compound_net_incomes = []  # sum of net incomes till current year when doing mortgage
        compound_house_price_changes = []  # house_price at current year - initial price
        compound_roa_net_income_yr = []  # acc_net_income_yr / assets_yr to Nth year
        compound_roa_house_price_yr = []  # acc_house_price_change_yr / assets_yr to Nth year
        compound_roa_totals = []

        # init value
        loan_cur = self.loan
        house_price_cur = self.price
        for idx in range(1, target_yr * 12 + 1):
            if idx <= self.num_payment:
                interest_part = loan_cur * self.interest_rate_month
                interest_paid_month.append(interest_part)
                principal_part = self.loan_payment - interest_part
                principal_paid_month.append(principal_part)
                loan_cur -= principal_part
                loan_balance_month.append(loan_cur)
                asset_month.append(principal_paid_month[-1] + (asset_month[-1] if asset_month else self.down_payment))
                income_month.append(self.rent_month - interest_part)
            else:
                assert loan_cur < 1e-3
                loan_balance_month.append(0)
                principal_paid_month.append(0)
                interest_paid_month.append(0)
                asset_month.append(asset_month[-1] if asset_month else self.down_payment)
                income_month.append(self.rent_month)

            # gather for year data
            if idx % 12 == 0:
                # loan part
                loan_balances.append(loan_balance_month[idx - 1])
                principals.append(sum(principal_paid_month[idx - 12: idx]))
                interests.append(sum(interest_paid_month[idx - 12: idx]))
                assets.append(asset_month[idx - 1])
                # income part
                net_incomes.append(sum(income_month[idx - 12: idx]) - self.hoa_yr - self.property_tax_yr - self.maintain_yr)
                # house price change part
                house_price_changes.append(house_price_cur * self.house_price_change_yr)
                house_price_cur *= (1 + self.house_price_change_yr)
                # roa each year
                single_yr_roa_net_incomes.append(net_incomes[-1] / assets[-1] * 100)
                single_yr_roa_house_price_changes.append(house_price_changes[-1] / assets[-1] * 100)
                single_yr_roa_totals.append(single_yr_roa_net_incomes[-1] + single_yr_roa_house_price_changes[-1])
                # acc and compound roa
                compound_net_incomes.append(sum(net_incomes))
                compound_house_price_changes.append(house_price_cur - self.price)
                yrs = idx / 12
                compound_roa_net_income_yr.append(((1 + (compound_net_incomes[-1] / assets[-1])) ** (1/yrs) - 1) * 100)
                compound_roa_house_price_yr.append(((1 + (compound_house_price_changes[-1] / assets[-1])) ** (1/yrs) - 1) * 100)
                compound_roa_totals.append(((1 + ((compound_net_incomes[-1] + compound_house_price_changes[-1])/assets[-1])) ** (1 /yrs) - 1) * 100)

        if debug:
            print(f"\n{self.invest_type()}")
            print(f"loan_balance_yr:{unit_transform(loan_balances)[0]}")
            print(f"principal_paid_yr:{unit_transform(principals)[0]}")
            print(f"interest_paid_yr:{unit_transform(interests)[0]}")
            print(f"net_income_yr:{unit_transform(net_incomes)[0]}")
            print(f"house_price_change_yr:{unit_transform(house_price_changes)[0]}")
            print(f"single_yr_roa_net_income_yr:{unit_transform(single_yr_roa_net_incomes)[0]}")
            print(f"single_yr_roa_house_price_change_yr:{unit_transform(single_yr_roa_house_price_changes)[0]}")
            print(f"asset_yr:{unit_transform(assets)[0]}")
            print(f"acc_net_income_yr:{unit_transform(compound_net_incomes)[0]}")
            print(f"acc_house_price_change_yr:{unit_transform(compound_house_price_changes)[0]}")
            print(f"compound_roa_net_income_yr:{unit_transform(compound_roa_net_income_yr)[0]}")
            print(f"compound_roa_house_price_yr:{unit_transform(compound_roa_house_price_yr)[0]}")
            print(f"compound_yr_roas:{unit_transform(compound_roa_totals)[0]}")

        # unified unit
        assets, net_incomes, house_price_changes, compound_net_incomes, compound_house_price_changes = \
            unified_unit([assets, net_incomes, house_price_changes, compound_net_incomes, compound_house_price_changes])
        loan_balances, principals, interests = unified_unit([loan_balances, principals, interests])
        annualFlowMetric = SingleYrMetric(loan_balances,
                                          principals,
                                          interests,
                                          net_incomes,
                                          house_price_changes,
                                          single_yr_roa_net_incomes,
                                          single_yr_roa_house_price_changes,
                                          single_yr_roa_totals)

        accumulativeMetrics = CompoundMetric(assets,
                                             compound_net_incomes,
                                             compound_house_price_changes,
                                             compound_roa_net_income_yr,
                                             compound_roa_house_price_yr,
                                             compound_roa_totals)
        return annualFlowMetric, accumulativeMetrics