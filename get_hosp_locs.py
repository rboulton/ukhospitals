#!/usr/bin/env python

import csv
import urllib2
try:
    import simplejson as json
except ImportError:
    import json

mapping = {
    'address1': 'address',
    'address2': 'address',
    'address3': 'address',
    'address4': 'address',
    'address5': 'address',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'name': 'name',
    'hasaande': 'hasaande',
    'postcode': 'postcode',
    'telephone': 'telephone',
    'website': 'url',
    'provider': 'provider',
}

def get():
    csvurl = "http://scraperwiki.com/scrapers/export/nhs-hospital-locations/"
    fd = urllib2.urlopen(csvurl)
    result = []
    cols = None
    for row in csv.reader(fd.readlines()):
        if cols is None:
            cols = row
            continue
        data = {}
        for col, val in zip(cols, row):
            val = val.strip()
            if val == '':
                continue
            col = mapping.get(col, None)
            if col is None:
                continue
            if col == 'hasaande':
                if val == 'false':
                    val = False
                elif val == 'true':
                    val = True
                else:
                    raise ValueError("Base hasaande value: %r" % val)
            if col in data:
                data[col] += ', ' + val
            else:
                data[col] = val
        result.append(data)
    return result

if __name__ == '__main__':
    data = get()
    fd = open('hosplocs.json', 'w')
    fd.write(json.dumps(data, indent=True))
    fd.close()
