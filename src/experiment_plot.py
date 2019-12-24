from src.house_invest_solution import HouseInvestSolution
from src.metrics import AnnualFlowMetric, AccumulativeMetric, Metric
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import os
import glob

YLIM_OFFSET = 1.25
FIGURE_WIDTH = 4
SMALL_SIZE = 80
MEDIUM_SIZE = 90
BIGGER_SIZE = 100

RC = {'font.size': SMALL_SIZE, 'axes.labelsize': MEDIUM_SIZE, 'legend.fontsize': MEDIUM_SIZE,
      'axes.titlesize': BIGGER_SIZE, 'xtick.labelsize': SMALL_SIZE, 'ytick.labelsize': SMALL_SIZE,
      'legend.loc': 'best'}
plt.rcParams.update(**RC)
COLOR_EXPENSE = 'grey'
COLOR_NET_INCOME = 'green'
COLOR_HOUSE_PRICE_CHANGE = 'orange'


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, str(height), ha='center', va='bottom')


def plot_comparison_metrics(control: Metric, treatment: Metric, output):
    target_yr = len(control.house_price_change[0])
    target_yrs = np.arange(target_yr)
    width = 0.35
    figure(num=None, figsize=(target_yr * FIGURE_WIDTH, 100), dpi=100, facecolor='w', edgecolor='k')

    plt.subplot(4, 1, 1)
    p_control_net_income = plt.bar(target_yrs - width, control.net_income[0], width)
    p_treatment_net_income = plt.bar(target_yrs, treatment.net_income[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'numbers/{control.net_income[1]}')
    plt.ylim(min(min(control.net_income[0]), min(treatment.net_income[0]), 0) * YLIM_OFFSET,
             max(max(control.net_income[0]), max(treatment.net_income[0])) * YLIM_OFFSET)
    plt.legend((p_control_net_income[0], p_treatment_net_income[0]), (control.invest_type, treatment.invest_type))
    plt.title(f"{control.des} net income: {control.invest_type} vs {treatment.invest_type}")
    # autolabel(p_control_net_income)
    # autolabel(p_treatment_net_income)

    plt.subplot(4, 1, 2)
    p_control_yield_income_ratio = plt.bar(target_yrs - width, control.yield_income_ratio[0], width)
    p_treatment_yield_income_ratio = plt.bar(target_yrs, treatment.yield_income_ratio[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'rate')
    plt.ylim(min(min(control.yield_income_ratio[0]), min(treatment.yield_income_ratio[0]), 0) * YLIM_OFFSET,
             max(max(control.yield_income_ratio[0]), max(treatment.yield_income_ratio[0])) * YLIM_OFFSET)
    plt.legend((p_control_yield_income_ratio[0], p_treatment_yield_income_ratio[0]),
               (control.invest_type, treatment.invest_type))
    plt.title(f"{control.des} net income yield: {control.invest_type} vs {treatment.invest_type}")
    # autolabel(p_control_yield_income_ratio)
    # autolabel(p_treatment_yield_income_ratio)

    plt.subplot(4, 1, 3)
    p_control_yield_house_price_change_ratio = plt.bar(target_yrs - width, control.yield_house_price_change_ratio[0], width)
    p_treatment_yield_house_price_change_ratio = plt.bar(target_yrs, treatment.yield_house_price_change_ratio[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'rate')
    plt.ylim(min(min(control.yield_house_price_change_ratio[0]), min(treatment.yield_house_price_change_ratio[0]), 0) * YLIM_OFFSET,
             max(max(control.yield_house_price_change_ratio[0]), max(treatment.yield_house_price_change_ratio[0])) * YLIM_OFFSET)
    plt.legend((p_control_yield_house_price_change_ratio[0], p_treatment_yield_house_price_change_ratio[0]),
               (control.invest_type, treatment.invest_type))
    plt.title(f"{control.des} house price change yield: {control.invest_type} vs {treatment.invest_type}")
    # autolabel(p_control_yield_house_price_change_ratio)
    # autolabel(p_treatment_yield_house_price_change_ratio)

    plt.subplot(4, 1, 4)
    p_control_yield_ratio = plt.bar(target_yrs - width, control.yield_ratio[0], width)
    p_treatment_yield_ratio = plt.bar(target_yrs, treatment.yield_ratio[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'rate')
    plt.ylim(min(min(control.yield_ratio[0]), min(treatment.yield_ratio[0]), 0) * YLIM_OFFSET,
             max(max(control.yield_ratio[0]), max(treatment.yield_ratio[0])) * YLIM_OFFSET)
    plt.legend((p_control_yield_ratio[0], p_treatment_yield_ratio[0]),
               (control.invest_type, treatment.invest_type))
    plt.title(f"{control.des} yield: {control.invest_type} vs {treatment.invest_type}")
    # autolabel(p_control_yield_ratio)
    # autolabel(p_treatment_yield_ratio)
    # plt.show()

    plt.savefig(f"{output}/{control.des}__metrics({control.invest_type}_vs_{treatment.invest_type}).png")


def plot_self_metrics(annual_flow_metric: AnnualFlowMetric, accumulative_metric: AccumulativeMetric, output):

    target_yr = len(annual_flow_metric.house_price_change[0])
    target_yrs = np.arange(target_yr)
    is_mortgage = annual_flow_metric.loan_balance[0][0] > 1
    total_plots = 2 + int(is_mortgage)

    width = 0.35
    figure(num=None, figsize=(target_yr * FIGURE_WIDTH, 100), dpi=100, facecolor='w', edgecolor='k')

    plt.subplot(total_plots, 1, 1)
    p_net_income = plt.bar(target_yrs, annual_flow_metric.net_income[0], width, color=COLOR_NET_INCOME)
    p_house_price_change = plt.bar(target_yrs + width, annual_flow_metric.house_price_change[0], width,
                                   color=COLOR_HOUSE_PRICE_CHANGE)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'numbers/{accumulative_metric.expenses[1]}')
    plt.ylim(min(min(annual_flow_metric.net_income[0]),
                 min(annual_flow_metric.house_price_change[0]), 0) * YLIM_OFFSET,
             max(max(annual_flow_metric.net_income[0]),
                 max(annual_flow_metric.house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_net_income[0], p_house_price_change[0]), ("net income", "house price change"))
    plt.title(f"{annual_flow_metric.des} net income and house price change at Nth year")
    # autolabel(p_net_income)
    # autolabel(p_house_price_change)

    plt.subplot(total_plots, 1, 2)
    width = 0.28
    p_expenses = plt.bar(target_yrs - width, accumulative_metric.expenses[0], width, color=COLOR_EXPENSE)
    p_acc_net_income = plt.bar(target_yrs, accumulative_metric.net_income[0], width, color=COLOR_NET_INCOME)
    p_acc_house_price_change = plt.bar(target_yrs + width, accumulative_metric.house_price_change[0], width,
                                       color=COLOR_HOUSE_PRICE_CHANGE)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'numbers/{accumulative_metric.expenses[1]}')
    plt.ylim(min(min(accumulative_metric.expenses[0]),
                 min(accumulative_metric.net_income[0]),
                 min(accumulative_metric.house_price_change[0]), 0) * YLIM_OFFSET,
             max(max(accumulative_metric.expenses[0]),
                 max(accumulative_metric.net_income[0]),
                 max(accumulative_metric.house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_expenses[0], p_acc_net_income[0], p_acc_house_price_change[0]),
               ("expense", "net_income", "house_price_change"))
    plt.title(f"{accumulative_metric.des} expense, net income and house price change to Nth year")
    # autolabel(p_expenses)
    # autolabel(p_acc_net_income)
    # autolabel(p_acc_house_price_change)

    if is_mortgage:
        plt.subplot(total_plots, 1, total_plots)
        width = 0.5
        p_principal = plt.bar(target_yrs, annual_flow_metric.principal[0], width)
        p_interest = plt.bar(target_yrs, annual_flow_metric.interest[0], width, bottom=annual_flow_metric.principal[0])
        plt.xticks(target_yrs, target_yrs + 1)
        plt.ylabel(f'numbers/{annual_flow_metric.principal[1]}')
        plt.ylim(0, max(max(annual_flow_metric.principal[0]),
                        max(annual_flow_metric.interest[0])) * YLIM_OFFSET)
        plt.legend((p_principal[0], p_interest[0]), ("principal", "interest"))
        plt.title(f"Principal and Interest at Nth year")

    plt.savefig(f"{output}/{annual_flow_metric.invest_type}_self.png")



def experiment(control: HouseInvestSolution, treatment: HouseInvestSolution=None, target_yr=30, output='img', debug=False):
    if control:
        if not os.path.exists(output):
            os.mkdir(output)
        else:
            for f in glob.glob(f'{output}/*'):
                os.remove(f)
        control_annual_flow_metrics, control_accumulative_metrics = control.experiment(target_yr, debug)
        plot_self_metrics(control_annual_flow_metrics, control_accumulative_metrics, output)
        if treatment:
            treatment_annual_flow_metrics, treatment_accumulative_metrics = treatment.experiment(target_yr, debug)
            plot_self_metrics(treatment_annual_flow_metrics, treatment_accumulative_metrics, output)
            plot_comparison_metrics(control_annual_flow_metrics, treatment_annual_flow_metrics, output)
            plot_comparison_metrics(control_accumulative_metrics, treatment_accumulative_metrics, output)
