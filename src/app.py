from src.experiment_plot import experiment
from src.house_invest_solution import HouseInvestSolution


solution_a = HouseInvestSolution(price=422500, down_payment_ratio=0.2, mortgage_yr=15, interest_rate_yr=0.02875,
                                 hoa_month=461, maintain_yr=1000, property_tax_yr=4000, rent_month=2500,
                                 house_price_change_yr=0.01)
solution_b = HouseInvestSolution(price=422500, down_payment_ratio=1, mortgage_yr=0, interest_rate_yr=0.02875,
                                 hoa_month=461, maintain_yr=1000, property_tax_yr=4000, rent_month=2500,
                                 house_price_change_yr=0.01)
experiment(solution_a, solution_b, 15)
print("Done")