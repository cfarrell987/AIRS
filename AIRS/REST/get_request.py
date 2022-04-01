import requests


# Sends GET request for hardware
def get_request(url, query_string, headers):
    response = requests.get(url=url, headers=headers, params=query_string).json()
    total_records = response['total']

    all_items = []
    for offset in range(0, total_records, 100):
        query_string['offset'] = offset

        response = requests.request("GET", url=url, headers=headers, params=query_string).json()

        all_items.extend(response['rows'])

    return all_items
