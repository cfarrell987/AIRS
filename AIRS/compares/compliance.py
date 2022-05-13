from . import compare


# TODO - Modify function to take in a number of items needed to check then prompt for each item
# TODO - Modify function to take in a list of items to check then prompt for each item (Only if there is a list)
def compliance_filter(input_file, filter_column, filter_value):

    df1 = compare.read_csv(input_file)
    df_complete = compare.filter_csv(df1, filter_column, filter_value)
    return df_complete
