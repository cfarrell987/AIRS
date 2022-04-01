import requests

# ideas
# - maybe see if can append only everything nested in the rows

# Sends GET request for hardware
def get_request(url, querystring, headers):
    response = requests.get(url=url, headers=headers, params=querystring).json()
    total_records = response['total']

    all_items = []
    print(all_items)
    for offset in range(0, total_records, 100):
        response = requests.request("GET", url=url, headers=headers, params=querystring).json()

        querystring['offset'] = offset
        print(querystring)
        if (offset == 0):
            all_items.extend(response)
        else:
            all_items.extend(response['rows'])

    return all_items