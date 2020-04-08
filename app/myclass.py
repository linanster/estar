from datetime import datetime
from settings import Debug, TypeRestrict

class CookJson(object):
    def __init__(self, raw):
        self.raw = raw
        self.items = list()
        self.sum = 0
        # for_power_calculation
        self.power = 0

    def gen_items(self):
        p = RawParser(self.raw)
        p.gen_items()
        self.items = p.items

    def calc_sum(self):
        for item in self.items:
            e = EnergyItem(item)
            e.calc_item()
            self.sum += e.consumption
    
    # for_power_calculation
    def calc_power(self):
        try:
            item = findlatest(self.items)
            if Debug:
                print('==item_latest==', item)
            e = EnergyItem(item)
            e.calc_item()
            self.power = e.power
        except Exception as e:
            print(str(e))
            raise PowerCalculationException(str(e))
        

class EnergyItem(object):  
    
    def __init__(self, item):
        self.consumption = 0
        self.power = 0
        # item type is dict
        # item format like: {'status': 1, 'online': 1, 'cct': 100, 'brightness': 100, 'deviceid': 13, 'time': '2020-03-24 04:00:00'}
        self.item = item
        self.formula = None
        self.brightness = item.get('brightness')/100
        self.cct_raw = self.item.get('cct') 
        self.cct = 2000 + item.get('cct') * 50
        self.cctrequired = False

    def formula_select(self):
        deviceid = self.item.get('deviceid')
        # initial variable type of xlink api json is str, not int. This is awesome bad!
        deviceid = int(deviceid)
        status = self.item.get('status')
        online = self.item.get('online')
        if not TypeRestrict:
            self.formula = formula_clife
            return
        # device type restriction, only support 4 types
        if deviceid not in (13,27,6,21):
            raise DeviceTypeException(deviceid)
        if status == 0 or online == 0:
            self.formula = formula_off
        # clife
        elif deviceid in (13, 27):
            self.formula = formula_clife
        # fullcolor
        elif deviceid in (6, 21):
            # rgb mode 
            if self.cct_raw > 100:
                self.formula = formular_fullcolor_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_fullcolor_cct_low
                    self.cctrequired = True
                else:
                    self.formula = formula_fullcolor_cct_high
        else:
            # todo
            raise Exception('unknown error')
            # pass

    def formula_run(self):
        # power in unit Watt
        if self.cctrequired:
            self.power = self.formula(self.brightness, self.cct)
        else:
            self.power = self.formula(self.brightness)
        # energy consumptoion in unit Joule
        # half one hour = 30 * 60 seconds
        self.consumption = self.power * 30 * 60
            

    def calc_item(self):
        self.formula_select()
        self.formula_run() 


class RawParser(object):
    
    def __init__(self, raw):
        self.raw = raw
        self.items = list()

    def get_errno(self):
        return self.raw.get('errno')

    def get_deviceid(self):
        return self.raw.get('deviceid')

    def get_timestamp(self):
        return self.raw.get('timestamp')

    def get_mac(self):
        return self.raw.get('mac')
        
    def gen_items(self):
        # errno handler
        # type of errno is <class 'int'>
        errno = self.get_errno()
        if errno == 400:
            raise DeviceNotFoundException()

        if errno == 401:
            raise NoDataException()

        if errno == 0:
            pass
        
        # shared property
        deviceid = self.get_deviceid()
        if Debug:
            print('==deviceid==',deviceid)
        datapoints = self.raw.get('datapoints')
        for datapoint in datapoints:
            item = dict()
            item['status'] = datapoint.get('status')
            item['online'] = datapoint.get('online')
            item['cct'] = datapoint.get('cct')
            item['brightness'] = datapoint.get('brightness')
            # for_power_calculation
            item['time'] = datapoint.get('time')
            # deviceid
            item['deviceid'] = deviceid
            self.items.append(item) 

# errno -2
class DeviceTypeException(Exception):
    def __init__(self,deviceid):
        self.deviceid = deviceid
        self.err_msg = "device type ( " + str(deviceid) + " ) " + " not supported"

# errno -3
class DeviceNotFoundException(Exception):
    def __init__(self):
        self.err_msg = "device not found"

# errno -4
class PowerCalculationException(Exception):
    def __init__(self, ori_msg):
        self.err_msg = "parse last 30 min datapoint error"
        self.ori_msg = ori_msg

# errno -5
class NoDataException(Exception):
    def __init__(self):
        self.err_msg = "no device state data"

def formula_clife(x):
    return 9.2707*x*x - 0.978*x + 0.6813

def formular_fullcolor_rgb(x):
    return 3.7757*x + 0.2075

def formula_fullcolor_cct_low(x, cct):
    return (5.4057*x + 0.5807)*(2700-cct)/700 + (8.6608*x + 0.3294)*(cct-2000)/700

def formula_fullcolor_cct_high(x):
    return 8.6608*x + 0.3294

def formula_off(x):
    return 0

# for_power_calculation
def findlatest(items):
    format_pattern = "%Y-%m-%d %H:%M:%S"
    item_latest = items[0]
    for item in items[1:]:
        d1 = datetime.strptime(item_latest.get('time'), format_pattern)
        d2 = datetime.strptime(item.get('time'), format_pattern)
        if d1 < d2:
            item_latest = item
        else:
            continue
    return item_latest
       
