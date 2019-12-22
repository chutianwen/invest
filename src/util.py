# compute
PRECISION = 2

def unit_transform(x, precision=PRECISION):
    if type(x) == list:
        ref = max(x)
        if ref >= 1e6:
            return list(map(lambda y: round(y / 1e6, precision), x)), 'm'
        elif ref >= 1e3:
            return list(map(lambda y: round(y / 1e3, precision), x)), 'k'
        else:
            return list(map(lambda y: round(y, precision), x)), ''
    else:
        if x >= 1e6:
            res = round(x / 1e6, precision)
            return res, f'{res}m'
        elif x >= 1e3:
            res = round(x / 1e3, precision)
            return res, f'{res}k'
        else:
            res = round(x, precision)
            return res, f'{res}'