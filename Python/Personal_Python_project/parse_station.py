import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
response = requests.get(url, verify=False)
stations = re.findall(r'([\u4e00-\u9fa5]+).*?([a-z]+)', response.text)
print(stations)
#pprint(dict(stations), indent=4)