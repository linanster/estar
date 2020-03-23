from requests import request
from myclass import CookJson

prefix = r'http://10.30.30.101:5001/estar?mac='

def _get_json(mac):
    endpoint = prefix + str(mac)
    response = request(method='GET', url=endpoint)
    return response.json()

def _cook_json(raw):
    c = CookJson(raw)
    c.gen_items()
    c.calc_sum()
    return c.sum

def get_consumption(mac):
    try:
        raw = _get_json(mac)
        return _cook_json(raw)
    except Exception as e:
        print("[error]",str(e))
        return -1
    

