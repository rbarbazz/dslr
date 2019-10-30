import pandas as pd
import numpy as np
import argparse
import math

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
    df.apply(lambda x: round(x, 2))
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
        current_total = 0
        for cell in df[col_name]:
            if not np.isnan(cell):
                print(cell)
                current_total += math.pow((cell -
                                           describe.loc['Mean', col_name]), 2)
        describe.at['Std', col_name] = math.sqrt(
            (current_total / describe.loc['Count', col_name]))

    print(describe)
    print(df.describe())
