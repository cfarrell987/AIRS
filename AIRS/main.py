import requests
import os
import errno
import json
import sys
from pathlib import Path
from REST import get_request as getter
if sys.platform != 'win32':
    import pwd
    import getpass


def get_logged_user():
    try:
        return os.getlogin()
    except:
        pass

    try:
        user = os.environ['USER']
    except KeyError:
        return getpass.getuser()

    if user == 'root':
        try:
            return os.environ['SUDO_USER']
        except KeyError:
            pass

        try:
            pkexec_uid = int(os.environ['PKEXEC_UID'])
            return pwd.getpwuid(pkexec_uid).pw_name
        except KeyError:
            pass
    return user


def get_res_path():
    res_dir = os.getcwd() + str(Path("/resources/"))
    return res_dir


def get_out_path():
    out_path = os.getcwd() + str(Path("/output/"))
    return out_path


# Define Settings needed for authenticating and sending a GET request. Will Change this later as querystring will be
# fairly specific to each GET request
def rest_settings(resources):
    res_path = resources
    api_key = Path(res_path + "/api_key.txt")

    with open(api_key, "r") as file:
        api_key = file.read()

    querystring = {
        "limit": "50",
        "offset": "0",
        "sort": "model",
        "order": "desc"
    }
    headers = {
        "Accept": "application/json",
        "Authorization": api_key.rstrip("'\n\"")
    }

    return querystring, headers


# Sends GET request for models


#TODO Look into handling multiple files with one call
def parser(json_dump, output_file):
    curr_path = os.path.dirname(os.path.realpath(__file__))
    out_path = get_out_path()
    parsed_path = Path(out_path + output_file)
    try:
        os.makedirs(out_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print(parsed_path)

    if os.path.exists(parsed_path):
        os.remove(Path(out_path + output_file))
        print("Deleted old json")

    with open(parsed_path, "w") as file:
        print("Writing to json")
        json.dump(json_dump, file)

if __name__ == '__main__':
    resource_path = get_res_path()
    #output_path = get_out_path()

    json_models = "\models.json"
    json_hardware = "\hardware.json"

    querystring, headers = rest_settings(resource_path)

    print(headers)
    #Hardcode for testing, will have a config file for the snipe-IT url
    url = "https://introhive.snipe-it.io/api/v1/"
    hardware = getter.get_request(url+"hardware", querystring, headers)
    models = getter.get_request(url + "models", querystring, headers)

    parsed_hardware = parser(hardware, json_hardware)
    parsed_models = parser(models, json_models)

