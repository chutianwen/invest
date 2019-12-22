from src.experiment_plot import experiment
from src.house_invest_solution import HouseInvestSolution

'''
You want to learn the investment return details, like net income, yield rate and etc.
If you only care investment plan/solution independently, uncomment "treatment_solution=None". Set the parameters 
in control_solution, then run the code.
If you want to learn by comparison, set parameters in both control and treatment solutions, then run the code.
'''
control_solution = HouseInvestSolution(price=200000, down_payment_ratio=0.2, mortgage_yr=15, interest_rate_yr=0.035,
                                       hoa_month=200, maintain_yr=1000, property_tax_yr=2000, rent_month=2500,
                                       house_price_change_yr=0.01)

treatment_solution = HouseInvestSolution(price=200000, down_payment_ratio=1, mortgage_yr=0, interest_rate_yr=0.02875,
                                         hoa_month=200, maintain_yr=1000, property_tax_yr=2000, rent_month=2500,
                                         house_price_change_yr=0.01)
# treatment_solution = None

experiment(control=control_solution, treatment=treatment_solution, target_yr=15)
print("Done")