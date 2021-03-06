import errno
import json
import os
from pathlib import Path

import pandas as pd

from REST import get_request as getter
from compares import compare as comp
from convert import converter as conv
from convert import tableclean as clean


# TODO Create initial startup check and function.
# TODO Create front end with fancy buttons for management to use
# TODO Use Pandas to generate Reports for Management to better understand our deployed environment


def get_res_path():
    res_dir = os.getcwd() + str(Path("/resources/"))
    return res_dir


def get_out_path():
    out_path = os.getcwd() + str(Path("/output/"))
    return out_path


# on first run, create a config file called config.json with the following: {'api_key': '<API_KEY>'}
# and place it in the resources folder
# if the config file does not exist, create it and place the API key in the file
def config():
    res_path = get_res_path()
    config_path = Path(res_path + "/config.json")

    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config_data = json.load(file)
            apikey = config_data['api_key']
            domain = config_data['domain']
    else:
        with open(config_path, "w") as file:
            apikey = input("Please enter your API Key: ")
            domain = input("Please enter your org name: ")
            config_data = {'api_key': apikey,
                           'domain': domain}
            json.dump(config_data, file)

    return apikey, domain


# Define Settings needed for authenticating and sending a GET request. Will Change this later as querystring will be
# fairly specific to each GET request
def rest_settings(apiKey):
    res_path = get_res_path()
    querystring = {
        "limit": "100",
        "offset": "0",
        "sort": "asset_tag",
        "order": "asc"
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + apiKey.rstrip("'\n\"")
    }
    return querystring, headers


# TODO Look into handling multiple files with one call
def parser(json_dump, output_file):
    curr_path = os.path.dirname(os.path.realpath(__file__))
    out_path = get_out_path()
    parsed_path = Path(out_path) / Path(output_file)
    try:
        os.makedirs(out_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print(parsed_path)

    if os.path.exists(parsed_path):
        os.remove(Path(out_path) / output_file)
        print("Deleted old json")

    with open(parsed_path, "w") as file:
        print("Writing to json")
        json.dump(json_dump, file)


def snipe_to_jamf(snipe_file, jamf_file, output_file):
    df1 = comp.read_csv(snipe_file)
    df1 = comp.filter_csv(df1, "category_name", "Macbook")
    df1 = comp.filter_csv(df1, "status_label_status_meta", "deployed")
    df2 = comp.read_csv(jamf_file)
    snipetojamf = comp.compare(df1, df2)

    comp.write_csv(snipetojamf, output_file)
    return snipetojamf


def jamf_to_snipe(jamf_file, snipe_file, output_file):
    df1 = comp.read_csv(jamf_file)
    df2 = comp.read_csv(snipe_file)
    df2 = comp.filter_csv(df2, "category_name", "Macbook")
    df2 = comp.filter_csv(df2, "status_label_status_meta", "deployed")
    jamftosnipe = comp.compare(df1, df2)

    comp.write_csv(jamftosnipe, output_file)
    return jamftosnipe

def jamf_compliance(jamf_file, output_file):

    df1 = comp.read_csv(jamf_file)
    df2 = comp.filter_csv(df1, "firewall_enabled", False)
    df3 = comp.filter_csv(df1, "sip_status", False)
    df4 = comp.filter_csv(df1, "boot_partition_filevault2_status", "Not Encrypted")
    df5 = comp.filter_csv(df1, "boot_partition_filevault2_status", "Pending")
    df6 = comp.filter_csv(df1, "av_not_running", True)
    df_complete = pd.concat([df2, df3, df4, df5, df6], join='inner')
    comp.write_csv(df_complete, output_file)

if __name__ == '__main__':
    json_models = "models.json"
    json_hardware = "hardware.json"
    out_path = get_out_path()

    apiKey, domain = config()

    query_string, headers = rest_settings(apiKey)

    # Hardcode for testing, will have a config file for the snipe-IT url
    url = "https://" + domain + ".snipe-it.io/api/v1/"
    hardware = getter.get_request(url + "hardware", query_string, headers)
    models = getter.get_request(url + "models", query_string, headers)

    # Parse Test
    # parsed_hardware = parser(hardware, json_hardware)
    # parsed_models = parser(models, json_models)

    # CSV Convert Test
    conv.convert(hardware, str(Path(out_path) / "hardware.csv"))
    # conv.convert(models, str(Path(out_path) / "models.csv"))
    clean.table_clean(str(Path(out_path) / "hardware.csv"))

    # Compare Test
    snipe_to_jamf(str(Path(out_path) / "hardware.csv"), str(Path(out_path) / "jamf_export.csv"),
                  str(Path(out_path) / "snipe_to_jamf.csv"))
    jamf_to_snipe(str(Path(out_path) / "jamf_export.csv"), str(Path(out_path) / "hardware.csv"),
                  str(Path(out_path) / "jamf_to_snipe.csv"))
    jamf_compliance(str(Path(out_path) / "jamf_export.csv"), str(Path(out_path) / "jamf_compliance.csv"))