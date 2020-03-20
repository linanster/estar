from requests import request

def _get_endpoint(mac):
    return 'http://10.30.30.101:5001/estar?mac={}'.format(mac)

def _get_json(mac):
    endpoint = _get_endpoint(mac)
    response = request(method='GET', url=endpoint)
    return response.json()

def _cook_json(raw):
    # todo
    consumption = 99
    return consumption

def get_consumption(mac):
    raw = _get_json(mac)
    consumption = _cook_json(raw)
    return consumption

def get_errno(raw):
    pass

def get_device_id(raw):
    pass

def caculate_clife(raw):
    pass

def caculate_fullcolor(raw):
    pass


def formula_clife(x):
    return 9.2707*x*x - 0.978*x + 0.6813
 
def formular_fullcolor_rgb(x):
    return 3.7757*x + 0.2075

def formula_fullcolor_cct_low(x, cct):
    return (5.4057*x + 0.5807)*(2700-cct)/700 + (8.6608*x + 0.3294)*(cct-2000)/700

def formula_fullcolor_cct_high(x):
    return 8.6608*x + 0.3294



