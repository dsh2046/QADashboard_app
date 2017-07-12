import re
from collections import Counter


x = '123456s7890 ew3ewe323 2015-08-13'
com = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
data = com.findall(x)
print data
