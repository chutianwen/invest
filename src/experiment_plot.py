from src.house_invest_solution import HouseInvestSolution
from src.metrics import AnnualFlowMetric, AccumulativeMetric, Metric
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

YLIM_OFFSET = 1.3
FIGURE_WIDTH = 4
SMALL_SIZE = 30
MEDIUM_SIZE = 50
BIGGER_SIZE = 80
plt.subplots_adjust(hspace=0.35)


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, str(height), ha='center', va='bottom', fontsize=SMALL_SIZE)


def plot_comparison_metrics(control: Metric, treatment: Metric, output):
    target_yr = len(control.house_price_change[0])
    target_yrs = np.arange(target_yr)
    figure(num=None, figsize=(target_yr * FIGURE_WIDTH, 100), dpi=100, facecolor='w', edgecolor='k')
    width = 0.35
    plt.subplot(4, 1, 1)
    p_control_net_income = plt.bar(target_yrs - width, control.net_income[0], width)
    p_treatment_net_income = plt.bar(target_yrs, treatment.net_income[0], width)
    plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
    plt.ylabel(f'net income/{control.net_income[1]}', fontsize=MEDIUM_SIZE)
    plt.ylim(0, max(max(control.net_income[0]), max(treatment.net_income[0])) * YLIM_OFFSET)
    plt.legend((p_control_net_income[0], p_treatment_net_income[0]), (control.invest_type, treatment.invest_type), fontsize=MEDIUM_SIZE)
    plt.title(f"{control.des} net income: {control.invest_type} vs {treatment.invest_type}", fontsize=BIGGER_SIZE)
    autolabel(p_control_net_income)
    autolabel(p_treatment_net_income)

    plt.subplot(4, 1, 2)
    p_control_yield_income_ratio = plt.bar(target_yrs - width, control.yield_income_ratio[0], width)
    p_treatment_yield_income_ratio = plt.bar(target_yrs, treatment.yield_income_ratio[0], width)
    plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
    plt.ylabel(f'rate', fontsize=MEDIUM_SIZE)
    plt.ylim(0, max(max(control.yield_income_ratio[0]), max(treatment.yield_income_ratio[0])) * YLIM_OFFSET)
    plt.legend((p_control_yield_income_ratio[0], p_treatment_yield_income_ratio[0]),
               (control.invest_type, treatment.invest_type), fontsize=MEDIUM_SIZE)
    plt.title(f"{control.des} net income yield: {control.invest_type} vs {treatment.invest_type}", fontsize=BIGGER_SIZE)
    autolabel(p_control_yield_income_ratio)
    autolabel(p_treatment_yield_income_ratio)

    plt.subplot(4, 1, 3)
    p_control_yield_house_price_change_ratio = plt.bar(target_yrs - width, control.yield_house_price_change_ratio[0], width)
    p_treatment_yield_house_price_change_ratio = plt.bar(target_yrs, treatment.yield_house_price_change_ratio[0], width)
    plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
    plt.ylabel(f'rate', fontsize=MEDIUM_SIZE)
    plt.ylim(0, max(max(control.yield_house_price_change_ratio[0]),
                    max(treatment.yield_house_price_change_ratio[0])) * YLIM_OFFSET)
    plt.legend((p_control_yield_house_price_change_ratio[0], p_treatment_yield_house_price_change_ratio[0]),
               (control.invest_type, treatment.invest_type), fontsize=MEDIUM_SIZE)
    plt.title(f"{control.des} house price change yield: {control.invest_type} vs {treatment.invest_type}", fontsize=BIGGER_SIZE)
    autolabel(p_control_yield_house_price_change_ratio)
    autolabel(p_treatment_yield_house_price_change_ratio)

    plt.subplot(4, 1, 4)
    p_control_yield_ratio = plt.bar(target_yrs - width, control.yield_ratio[0], width)
    p_treatment_yield_ratio = plt.bar(target_yrs, treatment.yield_ratio[0], width)
    plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
    plt.ylabel(f'rate', fontsize=MEDIUM_SIZE)
    plt.ylim(0, max(max(control.yield_ratio[0]), max(treatment.yield_ratio[0])) * YLIM_OFFSET)
    plt.legend((p_control_yield_ratio[0], p_treatment_yield_ratio[0]),
               (control.invest_type, treatment.invest_type), fontsize=MEDIUM_SIZE)
    plt.title(f"{control.des} yield: {control.invest_type} vs {treatment.invest_type}", fontsize=BIGGER_SIZE)
    autolabel(p_control_yield_ratio)
    autolabel(p_treatment_yield_ratio)
    # plt.show()
    plt.savefig(f"{output}/{control.des}_{control.invest_type}_vs_{treatment.invest_type}_metrics.png")


def plot_self_metrics(annual_flow_metric: AnnualFlowMetric, accumulative_metric: AccumulativeMetric, output):
    target_yr = len(annual_flow_metric.house_price_change[0])
    target_yrs = np.arange(target_yr)
    figure(num=None, figsize=(target_yr * FIGURE_WIDTH, 100), dpi=100, facecolor='w', edgecolor='k')
    plt.subplots_adjust(hspace=0.35)
    width = 0.28
    is_mortgage = annual_flow_metric.loan_balance[0][0] > 1
    total_plots = 2 + int(is_mortgage)
    plt.subplot(total_plots, 1, 1)
    p_expenses = plt.bar(target_yrs - width, accumulative_metric.expenses[0], width, color='grey')
    p_net_income = plt.bar(target_yrs, annual_flow_metric.net_income[0], width, color='green')
    p_house_price_change = plt.bar(target_yrs + width, annual_flow_metric.house_price_change[0], width, color='orange')
    plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
    plt.ylabel(f'expense, net-income, hours_price_change/{accumulative_metric.expenses[1]}', fontsize=MEDIUM_SIZE)
    plt.ylim(0, max(max(accumulative_metric.expenses[0]),
                    max(annual_flow_metric.net_income[0]),
                    max(annual_flow_metric.house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_expenses[0], p_net_income[0], p_house_price_change[0]),
               ("expense", "net_income", "house_price_change"), fontsize=MEDIUM_SIZE)
    plt.title(f"{annual_flow_metric.des} expense, net income and house price change at Nth year", fontsize=BIGGER_SIZE)
    autolabel(p_expenses)
    autolabel(p_net_income)
    autolabel(p_house_price_change)

    plt.subplot(total_plots, 1, 2)
    p_expenses = plt.bar(target_yrs - width, accumulative_metric.expenses[0], width, color='grey')
    p_acc_net_income = plt.bar(target_yrs, accumulative_metric.net_income[0], width, color='green')
    p_acc_house_price_change = plt.bar(target_yrs + width, accumulative_metric.house_price_change[0], width, color='orange')
    plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
    plt.ylabel(f'expense, net-income, hours_price_change/{accumulative_metric.expenses[1]}', fontsize=MEDIUM_SIZE)
    plt.ylim(0, max(max(accumulative_metric.expenses[0]),
                    max(accumulative_metric.net_income[0]),
                    max(accumulative_metric.house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_expenses[0], p_acc_net_income[0], p_acc_house_price_change[0]),
               ("expense", "net_income", "house_price_change"), fontsize=MEDIUM_SIZE)
    plt.title(f"{accumulative_metric.des} expense, net income and house price change to Nth year", fontsize=BIGGER_SIZE)
    autolabel(p_expenses)
    autolabel(p_acc_net_income)
    autolabel(p_acc_house_price_change)

    if is_mortgage:
        plt.subplot(total_plots, 1, total_plots)
        width = 0.5
        p_principal = plt.bar(target_yrs, annual_flow_metric.principal[0], width)
        p_interest = plt.bar(target_yrs, annual_flow_metric.interest[0], width, bottom=annual_flow_metric.principal[0])
        plt.xticks(target_yrs, target_yrs + 1, fontsize=MEDIUM_SIZE)
        plt.ylabel(f'principal, interest/{annual_flow_metric.principal[1]}', fontsize=MEDIUM_SIZE)
        plt.legend((p_principal[0], p_interest[0]), ("principal", "interest"), fontsize=MEDIUM_SIZE)
        plt.title(f"Principal and Interest at Nth year", fontsize=BIGGER_SIZE)

    plt.savefig(f"{output}/{annual_flow_metric.invest_type}_self_metrics.png")



def experiment(control: HouseInvestSolution, treatment: HouseInvestSolution=None, target_yr=30):
    if control:
        control_annual_flow_metrics, control_accumulative_metrics = control.experiment(target_yr, True)
        plot_self_metrics(control_annual_flow_metrics, control_accumulative_metrics, ".")
        if treatment:
            treatment_annual_flow_metrics, treatment_accumulative_metrics = treatment.experiment(target_yr, True)
            plot_self_metrics(treatment_annual_flow_metrics, treatment_accumulative_metrics, ".")
            plot_comparison_metrics(control_annual_flow_metrics, treatment_annual_flow_metrics, ".")
            plot_comparison_metrics(control_accumulative_metrics, treatment_accumulative_metrics, ".")
