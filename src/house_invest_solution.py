from src.metrics import AnnualFlowMetric, AccumulativeMetric
from src.util import unit_transform, unified_unit


class HouseInvestSolution:

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

    def description(self):
        des = f"investment type: {self.invest_type()}\n" \
            f"house price:{unit_transform(self.price)[1]}\tdown payment ratio:{self.down_payment_ratio * 100}%\t" \
            f"interest rate:{self.interest_rate_yr * 100}%\tmortgage year:{self.mortgage_yr}\t " \
            f"yearly hoa:{unit_transform(self.hoa_yr)[1]}\tyearly maintain:{unit_transform(self.maintain_yr)[1]}\t" \
            f"yearly property tax:{unit_transform(self.property_tax_yr)[1]}\t "\
            f"monthly rent:{unit_transform(self.rent_month)[1]}\trental home price ratio:{unit_transform(self.rent_home_price_ratio_yr * 100)[0]}%\t" \
            f"total loan:{unit_transform(self.loan)[1]}\ttotal interest:{unit_transform(self.interest_total)[1]}\t" \
            f"monthly loan payment:{unit_transform(self.loan_payment)[1]}\n "
        print(des)
        return des

    def loan_payment(self):
        if self.mortgage_yr == 0:
            return 0
        else:
            # discount Factor (D) = {[(1 + i) ^n] - 1} / [i(1 + i)^n]
            discount_factor = ((1 + self.interest_rate_month) ** self.num_payment - 1) / \
                              (self.interest_rate_month * (1 + self.interest_rate_month) ** self.num_payment)
            return self.loan / discount_factor

    def invest_type(self):
        if self.mortgage_yr == 0:
            return "full_cash"
        else:
            return f"{self.mortgage_yr}-year_mortgage"

    def experiment(self, target_yr, debug=False):
        # data for each month
        loan_balance = []  # remaining loan at current month
        principal_paid_month = []  # paid principal at each month
        interest_paid_month = []  # paid interest at each month
        income_month = []  # income at each month, deduct hoa, interest
        expenses = []  # total paid house price till current month
        # data for each year
        loan_balance_yr = []  # remaining loan at current year
        principal_paid_yr = []  # paid principal at each year
        interest_paid_yr = []  # paid interest at each year
        net_income_yr = []  # net income at each year
        house_price_change_yr = []  # house price change at each year compared to last year
        expenses_yr = []  # total paid house price till current year
        yield_income_ratio_yr = []  # net_incomes_yr / expense
        yield_house_price_change_yr = []  # house_price_change_yr / expense
        # accumulate n years back.
        acc_net_income_yr = []  # sum of net incomes till current year when doing mortgage
        acc_house_price_change_yr = []  # house_price at current year - initial price
        acc_income_yield_ratio_yr = []  # acc_net_income_yr / expense
        acc_house_price_yield_ratio_yr = []  # acc_house_price_change_yr / expense
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
                loan_balance.append(loan_cur)
                expenses.append(principal_paid_month[-1] + (expenses[-1] if expenses else self.down_payment))
                income_month.append(self.rent_month - interest_part)
            else:
                assert loan_cur < 1e-3
                loan_balance.append(0)
                principal_paid_month.append(0)
                interest_paid_month.append(0)
                expenses.append(expenses[-1] if expenses else self.down_payment)
                income_month.append(self.rent_month)

            # gather for year data
            if idx % 12 == 0:
                # loan part
                loan_balance_yr.append(loan_balance[idx - 1])
                principal_paid_yr.append(sum(principal_paid_month[idx - 12: idx]))
                interest_paid_yr.append(sum(interest_paid_month[idx - 12: idx]))
                expenses_yr.append(expenses[idx - 1])
                # income part
                net_income_yr.append(sum(income_month[idx - 12: idx]) - self.hoa_yr - self.property_tax_yr - self.maintain_yr)
                # house price change part
                house_price_change_yr.append(house_price_cur * self.house_price_change_yr)
                house_price_cur *= (1 + self.house_price_change_yr)
                # yield each year
                yield_income_ratio_yr.append(net_income_yr[-1] / expenses_yr[-1] * 100)
                yield_house_price_change_yr.append(house_price_change_yr[-1] / expenses_yr[-1] * 100)
                # acc data
                acc_net_income_yr.append(sum(net_income_yr))
                acc_income_yield_ratio_yr.append(acc_net_income_yr[-1] / expenses_yr[-1] * 100)
                acc_house_price_change_yr.append(house_price_cur - self.price)
                acc_house_price_yield_ratio_yr.append(acc_house_price_change_yr[-1] / expenses_yr[-1] * 100)

        if debug:
            print(f"\n{self.invest_type()}")
            print(f"loan_balance_yr:{unit_transform(loan_balance_yr)[0]}")
            print(f"principal_paid_yr:{unit_transform(principal_paid_yr)[0]}")
            print(f"interest_paid_yr:{unit_transform(interest_paid_yr)[0]}")
            print(f"net_income_yr:{unit_transform(net_income_yr)[0]}")
            print(f"house_price_change_yr:{unit_transform(house_price_change_yr)[0]}")
            print(f"yield_income_ratio_yr:{unit_transform(yield_income_ratio_yr)[0]}")
            print(f"yield_house_price_change_yr:{unit_transform(yield_house_price_change_yr)[0]}")
            print(f"expenses_yr:{unit_transform(expenses_yr)[0]}")
            print(f"acc_net_income_yr:{unit_transform(acc_net_income_yr)[0]}")
            print(f"acc_house_price_change_yr:{unit_transform(acc_house_price_change_yr)[0]}")
            print(f"acc_income_yield_ratio_yr:{unit_transform(acc_income_yield_ratio_yr)[0]}")
            print(f"acc_house_price_yield_ratio_yr:{unit_transform(acc_house_price_yield_ratio_yr)[0]}")

        # unified unit
        expenses_yr, net_income_yr, house_price_change_yr, acc_net_income_yr, acc_house_price_change_yr = \
            unified_unit([expenses_yr, net_income_yr, house_price_change_yr, acc_net_income_yr, acc_house_price_change_yr])
        loan_balance_yr, principal_paid_yr, interest_paid_yr = unified_unit([loan_balance_yr, principal_paid_yr, interest_paid_yr])
        annualFlowMetric = AnnualFlowMetric(self.invest_type(), loan_balance_yr, principal_paid_yr, interest_paid_yr,
                                            net_income_yr,house_price_change_yr, yield_income_ratio_yr,
                                            yield_house_price_change_yr)

        accumulativeMetrics = AccumulativeMetric(self.invest_type(), expenses_yr, acc_net_income_yr,
                                                 acc_house_price_change_yr, acc_income_yield_ratio_yr,
                                                 acc_house_price_yield_ratio_yr)
        return annualFlowMetric, accumulativeMetrics