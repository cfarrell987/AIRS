import requests


# Sends GET request for hardware
def get_request(url, querystring, headers):
    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()
