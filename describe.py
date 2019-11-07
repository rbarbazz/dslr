import pandas as pd
import numpy as np
import argparse
import math

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def percentile(sorted_serie, percentile):
    #Determine the position
    if percentile == 25:
        position = (describe.loc['Count', col_name] + 3) / 4
    elif percentile == 50:
        position = (describe.loc['Count', col_name] + 1) / 2
    elif percentile == 75:
        position = (describe.loc['Count', col_name] * 3 + 1) / 4

    # Find the position if it can or interpolation:
    if position.is_integer():
        return (sorted_serie[col_name][position - 1])
    elif position % 1 == 0.25:
        return ((sorted_serie[col_name][math.trunc(position) - 1] * 3 + sorted_serie[col_name][math.trunc(position)]) / 4)
    elif position % 1 == 0.5:
        return ((sorted_serie[col_name][math.trunc(position) - 1] + sorted_serie[col_name][math.trunc(position)]) / 2)
    elif position % 1 == 0.75:
        return ((sorted_serie[col_name][math.trunc(position) - 1] + sorted_serie[col_name][math.trunc(position)] * 3) / 4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Describe a set of data')
    parser.add_argument('filepath', type=str,
                        help='path to a file')
    args = parser.parse_args()
    col_to_skip = ['Index',  'Hogwarts House',
                   'First Name', 'Last Name', 'Birthday', 'Best Hand']
    df = pd.read_csv(args.filepath, usecols=lambda x: x not in col_to_skip)

    indexes = ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
    describe = pd.DataFrame(columns=df.columns, index=indexes, dtype=float)
    describe.loc['Count', :] = 0

    totals = {subject: 0 for subject in df.columns}

    # Iterate over df(row -> col) to find Count, Min and Max
    for row_index, row in df.iterrows():
        for col_name, cell in row.iteritems():
            if not np.isnan(cell):
                describe.at['Count', col_name] += 1
                totals[col_name] += cell
                current_min = describe.loc['Min', col_name]
                if cell < current_min or np.isnan(current_min):
                    describe.at['Min', col_name] = cell
                current_max = describe.loc['Max', col_name]
                if cell > current_max or np.isnan(current_max):
                    describe.at['Max', col_name] = cell

    # Iterate over columns to find Mean
    for col_name in df:
        describe.at['Mean', col_name] = totals[col_name] / \
            describe.loc['Count', col_name]

    # Iterate over df(col -> row) to find Std
    for col_name in df:
        tmp_total = 0
        for cell in df[col_name]:
            if not np.isnan(cell):
                tmp_calc = cell - describe.loc['Mean', col_name]
                tmp_total += math.pow(tmp_calc, 2)
        # Bessel's correction
        variance = (1 / (describe.loc['Count', col_name] - 1)) * tmp_total
        describe.at['Std', col_name] = math.sqrt(variance)

        #Find Quartile
        sorted_serie = df[col_name].sort_values().reset_index()
        describe.at['25%', col_name] = percentile(sorted_serie, 25)
        describe.at['50%', col_name] = percentile(sorted_serie, 50)
        describe.at['75%', col_name] = percentile(sorted_serie, 75)

    print(describe)
    print ("\n")
    print(df.describe())
