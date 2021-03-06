import os
import json
import pandas
from pathlib import Path
from AIRS import main as air


def create_dataframe(data):
    dataframe = pandas.json_normalize(data)

    return dataframe


def convert(data, out_file):
    # Generate the dataframe for the array items in
    # details key
    dataframe = create_dataframe(data=data)

    # Renaming columns of the dataframe
    print("Normalized Columns:", dataframe.columns.to_list())

    # Will look into renaming columns soon.
    dataframe.rename(columns={
        "model.name": "model_name",
        "status_label.name": "status_label_name",
        "status_label.status_meta": "status_label_status_meta",
        "category.name": "category_name",
        "manufacturer.name": "manufacturer_name",
        "location.name": "location_name",
        "assigned_to.username": "assigned_to_username",
        "assigned_to.name": "assigned_to_name",

    }, inplace=True)

    print("Renamed Columns:", dataframe.columns.to_list())

    if os.path.exists(out_file):
        os.remove(out_file)
        print("Deleted old csv")
    else:
        pass

    # Convert dataframe to CSV
    dataframe.to_csv(out_file, index=False)
