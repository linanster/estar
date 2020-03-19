from requests import request

def _get_endpoint(mac):
    return 'http://10.30.30.101:5001/estar?mac={}'.format(mac)

def _get_json(mac):
    endpoint = _get_endpoint(mac)
    response = request(method='GET', url=endpoint)
    return response.json()

def _cook_json(rawdata):
    # TODO
    consumption = 99
    return consumption

def get_consumption(mac):
    raw = _get_json(mac)
    consumption = _cook_json(raw)
    return consumption


