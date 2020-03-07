import csv
import re

import requests

from helpers import source_to_xml


url = 'https://raw.githubusercontent.com/datasets/dac-crs-codes/' + \
      'master/data/sectors.csv'
lookup = {
    'code': 'code',
    'category': 'category',
    'name_en': 'name_en',
    'name_fr': 'name_fr',
    'description_en': 'description_en',
    'description_fr': 'description_fr',
}
r = requests.get(url)
reader = csv.DictReader(r.iter_lines(decode_unicode=True))
sectors = []
for sector in reader:
    if sector['voluntary_code'] != '':
        sector['code'] = sector['voluntary_code']
    for txt in ['name_en', 'name_fr', 'description_en', 'description_fr']:
        sector[txt] = re.sub(r'  +', ' ', sector[txt])
    del sector['voluntary_code']
    sectors.append(sector)
sectors = sorted(sectors, key=lambda x: x['code'])
source_to_xml('Sector', None, lookup, source_data=sectors)
