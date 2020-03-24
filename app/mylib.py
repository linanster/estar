from requests import request
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from myclass import CookJson, DeviceTypeException
 
disable_warnings(InsecureRequestWarning)

# prefix = r'http://10.30.30.101:5001/estar?mac='
prefix = r'https://api-iot-ge.xlink.cloud/ge/v1/find_device_state?mac='

def _get_json(mac):
    endpoint = prefix + str(mac)
    response = request(method='GET', url=endpoint, verify=False)
    return response.json()

def _cook_json(raw):
    c = CookJson(raw)
    c.gen_items()
    c.calc_sum()
    return c.sum

def get_consumption(mac):
    consumption = 0
    errno = 0
    errmsg = str()
    try:
        raw = _get_json(mac)
        consumption = _cook_json(raw)
    except DeviceTypeException as e:
        errno = -2
        errmsg = e.err_msg
    except Exception as e:
        errno = -1
        errmsg = str(e) 
    finally:
        return (consumption, errno, errmsg)

