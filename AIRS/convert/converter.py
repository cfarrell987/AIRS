import json
import pandas
from AIRS import main as air


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data


def create_dataframe(data):
    # Declare an empty dataframe to append records
    dataframe = pandas.DataFrame()

    dataframe = pandas.json_normalize(data)

    return dataframe

def convert(in_file, out_file):
    # Read the JSON file as python dictionary
    data = read_json(filename=in_file)

    # Generate the dataframe for the array items in
    # details key
    dataframe = create_dataframe(data=data['rows'])

    # Renaming columns of the dataframe
    print("Normalized Columns:", dataframe.columns.to_list())

    #Will look into renaming columns soon.
    dataframe.rename(columns={
        "model.name": "model_name"
    }, inplace=True)

    print("Renamed Columns:", dataframe.columns.to_list())

    # Convert dataframe to CSV
    dataframe.to_csv(out_file, index=False)

