# -*- coding: utf-8 -*-

# Usage:
# 1. clone lcddriver from https://github.com/the-raspberry-pi-guy/lcd/
# 2. modified for my LCD1602 address 0x3f (default is 0x2f)
# 3. put this file in
# 4. connect LCD to 40-pin GPIO: GND - PIN.9, Vcc - PIN.4, SCL - PIN.5, SDA - PIN.3
# 5. connect to network, easiest way is via on-board ethernet
# Note: It is too trouble to display Chinese on LCD1602, converting to Pinyin instead.

import lcddriver
import time
import requests
import json

display = lcddriver.lcd()
display.lcd_display_string('2019-nCoV Updates', 1)
display.lcd_display_string('Loading...', 2)

class DataSourceDingXiang():
    cities = {
        u"湖南":b"Hunan", u"河南":b"Henan", u"辽宁":b"Liaoning", u"广东":b"Guangdong", u"四川":b"Sicuan",
        u"山东":b"Shandong", u"河北":b"Hebei", u"湖北":b"Hubei", u"重庆":b"Chongqing", u"浙江":b"Zhejiang",
        u"马来西亚":b"Malai", u"海南":b"Hainan", u"江苏":b"Jiangsu", u"陕西":b"Shan3xi", u"法国":b"France",
        u"宁夏":b"Ningxia", u"云南":b"Yunnan", u"黑龙江":b"Heilongjiang", u"天津":b"Tianjing", u"福建":b"Fujian",
        u"安徽":b"Anhui", u"菲律宾":b"Philippines", u"越南":b"Vietlam", u"意大利":b"Italy", u"德国":b"German",
        u"山西":b"Shanxi", u"阿联酋":b"UAE", u"新加坡":b"Singapore", u"日本":b"Japan", u"贵州":b"Guizhou",
        u"上海":b"Shanghai", u"英国":b"UK", u"台湾":b"Taiwan", u"广西":b"Guangxi", u"内蒙古":b"Neimeng",
        u"新疆":b"Xinjiang", u"北京":b"Beijing", u"江西":b"Jiangxi", u"甘肃":b"Gansu", u"吉林":b"Jiling",
        u"香港":b"Hongkang", u"澳大利亚":b"Australia", u"韩国":b"Korea", u"澳门":b"Aomen", u"美国":b"USA",
        u"青海":b"Qinghai", u"加拿大":b"Canada", u"泰国":b"Thailand", u"印度":b"India", u"比利时":b"Belgium",
        u"西藏":b"Xizang", u"待明确地区":b"Unknown", u"斯里兰卡":b"Sri Lanka", u"瑞典":b"Sweden", u"俄罗斯":b"Russia",
        u"西班牙":b"Spanish", u"柬埔寨":b"Cambodia", u"尼泊尔":b"Napel", u"芬兰":b"Finland"
    }
    def get_url(self):
        return "http://lab.isaaclin.cn/nCoV/api/area?latest=1"
    def get_results(self, j):
        return j['results']
    def get_city(self, i):
        city = self.cities.get(i["provinceShortName"])
        if city is None :
            city = "New!!!"
        return city
    def get_confirmed(self, i):
        return i["confirmedCount"]
    def get_suspicious(self, i):
        return i["suspectedCount"]
    def success(self, j):
        return j["success"]

class DataSourceGov():
    cities = ["Beijing", "Tianjing", "Hebei", "Shan1xi", "Neimong", "Liaoling", "Jiling", "Heilongjiang",
        "Shanghai", "Jiangsu", "Zhejiang", "Anhui", "Fujian", "Jiangxi", "Shandong", "Henan", "Hubei", 
        "Hunan", "Guangdong", "Guangxi", "Hainan", "Chongqin", "Sicuan", "Guizhoug", "Yunnan", "Xizang", 
        "Shan3xi", "Gansu", "Qinghai", "Ningxia", "Xinjiang", "Taiwan", "Xianggang", "Aomen",
        "Unknown","Unknown","Unknown","Unknown","Unknown","Unknown","Unknown","Unknown","Unkown"]
    def get_url(self):
        t = time.gmtime(time.time() - 16*3600) # UTC+8 China yesterday
        strTime = time.strftime("%Y%m%d", t)
        str = "https://ncportal.esrichina.com.cn/JKZX/yq_{}.json".format(strTime)
        return str
    def get_results(self, j):
        return j['features'] 
    def get_city(self, i):
        p = i['properties']
        return self.cities[(int(p['OBJECTID'])-1)]
    def get_confirmed(self, i):
        p = i['properties']
        return p[u"新增确诊"]
    def get_suspicious(self, i):
        p = i['properties']
        return p[u"新增疑似"]
    def success(self, j):
        return True

def fetch_data():
    global latestUpdate, ds
    s = ds.get_url()
    c = requests.get(s).content
    latestUpdate = time.time()
    return json.loads( c )

dsSwitched = False
def switch_datasource():
    global ds, dsSwitched
    display.lcd_clear()
    display.lcd_display_string("switch source", 1)
    if ds is DataSourceGov:
        ds = DataSourceDingXiang()
    else :
        ds = DataSourceGov()

def time_to_refresh():
    now = time.time()
    return (now - latestUpdate) > 3600 * 4 # per 4 hours

def setupSwitch():
    # TODO: use a button to switch source
    pass

if __name__ == "__main__":
    print("Starting...")
    ds = DataSourceGov()
    latestUpdate = time.time()
    j = fetch_data()
    dsChanged = False

    while(True):
        if time_to_refresh() or dsSwitched :
            display.lcd_display_string("loading ...", 2)
            j = fetch_data()

        if ds.success(j) :
            for i in ds.get_results(j): 
                display.lcd_clear()
                msg = ds.get_city(i)
                display.lcd_display_string(msg, 1)
                msg = b"!{} ?{}".format(ds.get_confirmed(i), ds.get_suspicious(i))
                display.lcd_display_string(msg, 2)
                time.sleep(2)
        else:
            display.lcd_clear()
            display.lcd_display_string("fetch failed", 1)
        switch_datasource()