from src.house_invest_solution import HouseInvestSolution
from src.metrics import SingleYrMetric, CompoundMetric, Metric
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

LEGEND_CONTROL = 'control'
LEGEND_TREATMENT = 'treatment'

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, str(height), ha='center', va='bottom')


def plot_comparison_metrics(control: Metric, treatment: Metric, title, output):
    target_yr = len(control.house_price_change[0])
    target_yrs = np.arange(target_yr)
    width = 0.35
    figure(num=None, figsize=(target_yr * FIGURE_WIDTH, 100), dpi=100, facecolor='w', edgecolor='k')

    plt.title(f'{title}\n')
    plt.subplot(4, 1, 1)
    p_control_net_income = plt.bar(target_yrs - width, control.net_income[0], width)
    p_treatment_net_income = plt.bar(target_yrs, treatment.net_income[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'numbers/{control.net_income[1]}')
    plt.ylim(min(min(control.net_income[0]), min(treatment.net_income[0]), 0) * YLIM_OFFSET,
             max(max(control.net_income[0]), max(treatment.net_income[0])) * YLIM_OFFSET)
    plt.legend((p_control_net_income[0], p_treatment_net_income[0]), (LEGEND_CONTROL, LEGEND_TREATMENT))
    plt.title(f"{title}\n{control.des} net income")
    # autolabel(p_control_net_income)
    # autolabel(p_treatment_net_income)

    plt.subplot(4, 1, 2)
    p_control_roa_net_income = plt.bar(target_yrs - width, control.roa_net_income[0], width)
    p_treatment_roa_net_income = plt.bar(target_yrs, treatment.roa_net_income[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'rate/%')
    plt.ylim(min(min(control.roa_net_income[0]), min(treatment.roa_net_income[0]), 0) * YLIM_OFFSET,
             max(max(control.roa_net_income[0]), max(treatment.roa_net_income[0])) * YLIM_OFFSET)
    plt.legend((p_control_roa_net_income[0], p_treatment_roa_net_income[0]),
               (LEGEND_CONTROL, LEGEND_TREATMENT))
    plt.title(f"{control.des} roa of net income")
    # autolabel(p_control_roa_net_income)
    # autolabel(p_treatment_roa_net_income)

    plt.subplot(4, 1, 3)
    p_control_roa_house_price_change = plt.bar(target_yrs - width, control.roa_house_price_change[0], width)
    p_treatment_roa_house_price_change = plt.bar(target_yrs, treatment.roa_house_price_change[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'rate/%')
    plt.ylim(min(min(control.roa_house_price_change[0]), min(treatment.roa_house_price_change[0]), 0) * YLIM_OFFSET,
             max(max(control.roa_house_price_change[0]), max(treatment.roa_house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_control_roa_house_price_change[0], p_treatment_roa_house_price_change[0]),
               (LEGEND_CONTROL, LEGEND_TREATMENT))
    plt.title(f"{control.des} roa of house price change")
    # autolabel(p_control_roa_house_price_change)
    # autolabel(p_treatment_roa_house_price_change)

    plt.subplot(4, 1, 4)
    p_control_roa_total = plt.bar(target_yrs - width, control.roa_total[0], width)
    p_treatment_roa_total = plt.bar(target_yrs, treatment.roa_total[0], width)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'rate/%')
    plt.ylim(min(min(control.roa_total[0]), min(treatment.roa_total[0]), 0) * YLIM_OFFSET,
             max(max(control.roa_total[0]), max(treatment.roa_total[0])) * YLIM_OFFSET)
    plt.legend((p_control_roa_total[0], p_treatment_roa_total[0]),
               (LEGEND_CONTROL, LEGEND_TREATMENT))
    plt.title(f"{control.des} roa of net income plus house price change")
    # autolabel(p_control_roa_total)
    # autolabel(p_treatment_roa_total)
    # plt.show()

    plt.savefig(f"{output}/{control.des}__comparison_metrics.png")


def plot_self_metrics(single_yr_metric: SingleYrMetric, compound_metric: CompoundMetric, title, name, output):

    target_yr = len(single_yr_metric.house_price_change[0])
    target_yrs = np.arange(target_yr)
    is_mortgage = single_yr_metric.loan_balance[0][0] > 1
    total_plots = 2 + int(is_mortgage)

    width = 0.35
    figure(num=None, figsize=(target_yr * FIGURE_WIDTH, 100), dpi=100, facecolor='w', edgecolor='k')
    plt.subplot(total_plots, 1, 1)
    p_net_income = plt.bar(target_yrs, single_yr_metric.net_income[0], width, color=COLOR_NET_INCOME)
    p_house_price_change = plt.bar(target_yrs + width, single_yr_metric.house_price_change[0], width,
                                   color=COLOR_HOUSE_PRICE_CHANGE)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'numbers/{compound_metric.assets[1]}')
    plt.ylim(min(min(single_yr_metric.net_income[0]),
                 min(single_yr_metric.house_price_change[0]), 0) * YLIM_OFFSET,
             max(max(single_yr_metric.net_income[0]),
                 max(single_yr_metric.house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_net_income[0], p_house_price_change[0]), ("net income", "house price change"))
    plt.title(f"{title}\n{single_yr_metric.des} net income and house price change at Nth year")
    # autolabel(p_net_income)
    # autolabel(p_house_price_change)

    plt.subplot(total_plots, 1, 2)
    width = 0.28
    p_assets = plt.bar(target_yrs - width, compound_metric.assets[0], width, color=COLOR_EXPENSE)
    p_acc_net_income = plt.bar(target_yrs, compound_metric.net_income[0], width, color=COLOR_NET_INCOME)
    p_acc_house_price_change = plt.bar(target_yrs + width, compound_metric.house_price_change[0], width,
                                       color=COLOR_HOUSE_PRICE_CHANGE)
    plt.xticks(target_yrs, target_yrs + 1)
    plt.ylabel(f'numbers/{compound_metric.assets[1]}')
    plt.ylim(min(min(compound_metric.assets[0]),
                 min(compound_metric.net_income[0]),
                 min(compound_metric.house_price_change[0]), 0) * YLIM_OFFSET,
             max(max(compound_metric.assets[0]),
                 max(compound_metric.net_income[0]),
                 max(compound_metric.house_price_change[0])) * YLIM_OFFSET)
    plt.legend((p_assets[0], p_acc_net_income[0], p_acc_house_price_change[0]),
               ("assets", "net_income", "house_price_change"))
    plt.title(f"{compound_metric.des} assets, net income and house price change to Nth year")
    # autolabel(p_assets)
    # autolabel(p_acc_net_income)
    # autolabel(p_acc_house_price_change)

    if is_mortgage:
        plt.subplot(total_plots, 1, total_plots)
        width = 0.5
        p_principal = plt.bar(target_yrs, single_yr_metric.principal[0], width)
        p_interest = plt.bar(target_yrs, single_yr_metric.interest[0], width, bottom=single_yr_metric.principal[0])
        plt.xticks(target_yrs, target_yrs + 1)
        plt.ylabel(f'numbers/{single_yr_metric.principal[1]}')
        plt.ylim(0, max(max(single_yr_metric.principal[0]),
                        max(single_yr_metric.interest[0])) * YLIM_OFFSET)
        plt.legend((p_principal[0], p_interest[0]), ("principal", "interest"))
        plt.title(f"Principal and Interest at Nth year")

    plt.savefig(f"{output}/{name}_self_metrics.png")



def experiment(control: HouseInvestSolution, treatment: HouseInvestSolution=None, target_yr=30, output='img', debug=False):
    if control:
        if not os.path.exists(output):
            os.mkdir(output)
        else:
            for f in glob.glob(f'{output}/*'):
                os.remove(f)
        control_annual_flow_metrics, control_accumulative_metrics = control.experiment(target_yr, debug)
        title_control = control.short_description()
        plot_self_metrics(control_annual_flow_metrics, control_accumulative_metrics, title_control, 'control', output)
        if treatment:
            treatment_annual_flow_metrics, treatment_accumulative_metrics = treatment.experiment(target_yr, debug)
            title_treatment = treatment.short_description()
            plot_self_metrics(treatment_annual_flow_metrics, treatment_accumulative_metrics, title_treatment, 'treatment', output)
            title_comparison = f"control: {title_control}\ntreatment: {title_treatment}"
            plot_comparison_metrics(control_annual_flow_metrics, treatment_annual_flow_metrics, title_comparison, output)
            plot_comparison_metrics(control_accumulative_metrics, treatment_accumulative_metrics, title_comparison, output)
