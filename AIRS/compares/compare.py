import os

import pandas as pd


def read_csv(file):
    df = pd.read_csv(file)
    return df


def filter_df(df, column, value):
    df = df[df[column] == value]
    return df


def compare_df(df1, df2, column):
    df1 = df1[~df1[column].isin(df2[column])].reset_index(drop=True)
    return df1


def filter_csv(df1, column, value):
    df = filter_df(df1, column, value)
    return df


def compare(infile1, infile2):
    df1 = infile1
    df2 = infile2
    output = compare_df(df1, df2, 'serial')
    return output


def write_csv(df, outfile):
    if os.path.exists(outfile):
        os.remove(outfile)
    df.to_csv(outfile, index=False)
