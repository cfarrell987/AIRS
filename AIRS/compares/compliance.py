from . import compare


def compliance_filter(input_file, filter_column, filter_val, output_file):
    """
    This function takes in an input file and a filter value and outputs a new file with only the rows that meet the filter value.

    df = compare.read_csv(input_file)
    df = compare.filter_csv(df, "activation_lock", "FALSE")
    compare.write_csv(df, output_file)
    """
    df1 = compare.read_csv(input_file)
    df1 = compare.filter_csv(df1, filter_column, filter_val)
    compare.write_csv(df1, output_file)
    return output_file
