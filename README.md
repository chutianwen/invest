# Real estate invest calculator
Author: Tianwen (chutianwen123@gmail.com)

## Introduction
This is a simple calculator to help you visualize investment details like net-income, yield rate and etc. By setting target paramters, you can cleary see how investment looks like and even find the better one by comparison. You will understand why people saying "mortage is the most common way of applying financial leverage"(CAREFUL, sometimes worse).

## Requirement
Strongly recommend to install the latest Anaconda in local environment, so you can rebuild the same environment by
```shell 
conda env create -f environment.yml
```
If you are a conda hater, then just make sure `numpy, matplot` are installed in python path.

## Manual
Modify investment parameters inside `./app.py` as described in the comment, then

```shell
# if mac
source activate py37
# if windows
activate py37
python app.py
```

You expect to see 1 or 4 images created in the project root directory depending on if you set a treatment solution for comparison study. They should look like below
- 15-year_mortgage_self_metrics.png (control)

_if you do set treatment_
- full_cash_self_metrics.png (treatment)
- 15-year_mortgage_annual_vs_full_cash_annual_metrics.png
- 15-year_mortgage_accumulative_vs_full_cash_accumulative_metrics.png

Usually good comparison study is like AB testing, you only have one "treatment(invest solution difference)" like
- **mortagae** vs **full cash** on same house: treatment on financial plan
- **shorter term mortage** vs **longer term mortage** on same house: treatment on financial plan
- **A house** vs **B house** with same(or similar) mortgage plan like 15 year fixed rate: treatment on house selection

But nothing stops you to apply compound treatment of **house selection** pluse **financial plan**. 

