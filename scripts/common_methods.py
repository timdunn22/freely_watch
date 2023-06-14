import pandas as pd
from collections import ChainMap
import yaml
from yaml import SafeLoader

def merged_dicts(the_list, item_function=None):
    if item_function is None:
        return dict(ChainMap(*[item for item in the_list]))
    return dict(ChainMap(*[item_function(item) for item in the_list]))

def not_null_value(value):
    return not pd.isnull(value) and value not in ['None', 'nan', None, '\\N']

def flatten(some_list):
    return [item for sublist in some_list for item in sublist]

def convert_xy_columns(df):
    xy_columns = [column for column in df.columns if column.endswith('_x') or column.endswith('_y')]
    for column in xy_columns:
        for split_var in ['_x', '_y', '_z']:
            if split_var in column:
                column_split = split_var
        new_column = column.split(column_split)[0]
        df[new_column] = df.loc[nonnull_columns(df, column), [column]]
    df.drop(xy_columns, inplace=True, axis=1)

def nonnull_columns(df, column):
    return ~df[column].isnull() & ~(df[column] == '\\N')

def load_yaml_file(file):
    with open(file) as f:
        data = yaml.load(f, Loader=SafeLoader)
    return data