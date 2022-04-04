import errno
import json
import os
from pathlib import Path

from REST import get_request as getter
from convert import converter as conv
from convert import tableclean as clean


# TODO create config file to read in
# TODO create config file to read in
# TODO Create initial startup check and function.
# TODO Test filtering SnipeIT Data to only macs or pc's
# TODO Test comparing Jamf data to SnipeIT data with csv-diff and/or pandas
# TODO Create front end with fancy buttons for management to use


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
    api_key = Path(res_path + "/api_key.txt")

    with open(api_key, "r") as file:
        api_key = file.read()

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
    print(headers)
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
