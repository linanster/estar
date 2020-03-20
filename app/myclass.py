
class CookJson(object):
    def __init__(self, raw):
        self.raw = raw
        self.items = list()
        self.sum = 0

    def gen_items(self):
        p = RawParser(self.raw)
        p.gen_items()
        self.items = p.items

    def calc_sum(self):
        for item in self.items:
            e = EnergyItem(item)
            self.sum += e.calc_item()
        

class EnergyItem(object):  
    
    def __init__(self, item):
        self.consumption = 0
        self.item = item
        self.formula = None
        self.brightness = item.get('brightness')/100
        self.cct = item.get('cct') * 50
        self.cctrequired = False

    def formula_select(self):
        deviceid = self.item.get('deviceid')
        status = self.item.get('status')
        online = self.item.get('online')
        if status == 0 or online == 0:
            self.formula = formula_off
        # clife
        elif deviceid in (13, 27):
            self.formula = formula_clife
        # fullcolor
        elif deviceid in (6, 21):
            # rgb mode 
            if self.cct > 100:
                self.formula = formular_fullcolor_rgb
            # cct mode
            else:
                if self.cct < 2700:
                    self.formula = formula_fullcolor_cct_low
                    self.cctrequired = True
                else:
                    self.formula = formula_fullcolor_cct_high
        else:
            pass

    def formula_run(self):
        if self.cctrequired:
            cct = 50 * self.cct
            self.consumption = self.formula(self.brightness, cct)
        else:
            self.consumption = self.formula(self.brightness)
            

    def calc_item(self):
        self.formula_select()
        self.formula_run() 
        return self.consumption


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
        deviceid = self.get_deviceid()
        
        datapoints = self.raw.get('datapoints')
        for datapoint in datapoints:
            item = dict()
            item['status'] = datapoint.get('status')
            item['online'] = datapoint.get('online')
            item['cct'] = datapoint.get('cct')
            item['brightness'] = datapoint.get('brightness')
            item['deviceid'] = deviceid
            self.items.append(item) 


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
