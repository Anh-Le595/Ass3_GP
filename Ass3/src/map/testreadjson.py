

import json
from pprint import pprint

with open('map1_1.json') as data_file:
    data = json.load(data_file)
pprint(data[0]["objects"])