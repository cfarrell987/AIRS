import pandas as pd


def read_csv(file):
    df = pd.read_csv(file)
    return df


def filter_df(df, column, value):
    df = df[df[column] == value]
    return df


def compare_df(df1, df2, column):
    df1 = df1[df1[column].isin(df2[column])]
    return df1


def compare(infile1):
    read_csv(infile1)
    df1 = read_csv(infile1)
    df1 = filter_df(df1, 'category_name', 'Macbook')
    print(df1)
    return df1

def write_csv(df, outfile):
    df.to_csv(outfile, index=False)