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


def unified_unit(rows, precision=1):
    '''
    find the min of max value of each row, then find its unit and uniform all the rows. Each transformed row returned
    with the unit.
    Ex. rows = [[111, 2222], [33,3333]] => [([0.111, 2.222], 'k'), ([0.033, 3.333], 'k')]
    '''
    min_max = min(map(lambda row: max(row), rows))
    if min_max >= 1e6:
        return [([round(x / 1e6, precision) for x in row], 'm') for row in rows]
    elif min_max >= 1e3:
        return [([round(x / 1e3, precision) for x in row], 'k') for row in rows]
    else:
        return [([round(x, precision) for x in row], '') for row in rows]