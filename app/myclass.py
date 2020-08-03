from datetime import datetime
from settings import Debug, TypeRestrict
from mylogger import logger

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
            logger.info('==item_latest=={}'.format(item))
            e = EnergyItem(item)
            e.calc_item()
            self.power = e.power
        except Exception as e:
            logger.error(str(e))
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
        if deviceid not in (13, 27, 6, 21, 128, 129, 130, 131, 132):
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
                self.formula = formula_fullcolor_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_fullcolor_cct_low
                else:
                    self.formula = formula_fullcolor_cct_high

        ####################################
        # support extra five new device id #
        ####################################

        # 0x80
        elif deviceid == 128:
            self.formula = formula_0x80

        # 0x81
        elif deviceid == 129:
            # rgb mode
            if self.cct_raw > 100:
                self.formula = formula_0x81_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_0x81_cct_low
                else:
                    self.formula = formula_0x81_cct_high

        # 0x82
        elif deviceid == 130:
            # rgb mode
            if self.cct_raw > 100:
                self.formula = formula_0x82_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_0x82_cct_low
                else:
                    self.formula = formula_0x82_cct_high

        # 0x83
        elif deviceid == 131:
            # rgb mode
            if self.cct_raw > 100:
                self.formula = formula_0x83_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_0x83_cct_low
                else:
                    self.formula = formula_0x83_cct_high

        # 0x84
        elif deviceid == 132:
            # rgb mode
            if self.cct_raw > 100:
                self.formula = formula_0x84_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_0x84_cct_low
                else:
                    self.formula = formula_0x84_cct_high

        else:
            # todo
            raise Exception('unknown error')
            # pass

    def formula_run(self):
        # power in unit Watt
        self.power = self.formula(self.brightness, self.cct)
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
        logger.info('==deviceid=={}'.format(deviceid))
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

def formula_clife(x, cct):
    return 9.2707*x*x - 0.978*x + 0.6813

def formula_fullcolor_rgb(x, cct):
    return 3.7757*x + 0.2075

def formula_fullcolor_cct_low(x, cct):
    return (5.4057*x + 0.5807)*(2700-cct)/700 + (8.6608*x + 0.3294)*(cct-2000)/700

def formula_fullcolor_cct_high(x, cct):
    return 8.6608*x + 0.3294

def formula_0x80(x, cct):
    return 8.7503*x+0.1781

def formula_0x81_rgb(x, cct):
    return 8.4849*x + 0.1275

def formula_0x81_cct_low(x, cct):
    return (8.4849*x + 0.1275)*(2700-cct)/700 + (4.5038*x + 0.389)*(cct-2000)/700

def formula_0x81_cct_high(x, cct):
    return (8.4855*x + 0.1101)*(7000-cct)/4300 + (8.4849*x + 0.1275)*(cct-2700)/4300

def formula_0x82_rgb(x, cct):
    return 9.5321*x + 0.1206

def formula_0x82_cct_low(x, cct):
    return (9.5321*x + 0.1206)*(2700-cct)/700 + (4.9742*x + 0.3245)*(cct-2000)/700

def formula_0x82_cct_high(x, cct):
    return (9.4874*x + 0.1249)*(7000-cct)/4300 + (9.5321*x + 0.1206)*(cct-2700)/4300

def formula_0x83_rgb(x, cct):
    return 3.9704*x + 0.2362

def formula_0x83_cct_low(x, cct):
    return (5.5786*x + 0.6811)*(2700-cct)/700 + (8.9906*x + 0.3885)*(cct-2000)/700

def formula_0x83_cct_high(x, cct):
    return 8.944*x + 0.4095

def formula_0x84_rgb(x, cct):
    return 3.8855*x + 0.1387

def formula_0x84_cct_low(x, cct):
    return (5.4535*x + 0.5145)*(2700-cct)/700 + (8.7711*x + 0.2344)*(cct-2000)/700

def formula_0x84_cct_high(x, cct):
    return 9.4138*x + 0.2481

def formula_off(x, cct):
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
       
