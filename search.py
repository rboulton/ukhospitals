#!/usr/bin/env python

import xappy
import geoloc
try:
    import simplejson as json
except ImportError:
    import json

def search(indexpath, loc1, loc2=None, maxhits=10):
    loc = geoloc.get(loc1, loc2)
    if loc[0] is None:
        return None
    loc = loc[1] + " " + loc[0]
    conn = xappy.SearchConnection(indexpath)
    registries = []
    for result in conn.query_distance('location', loc).search(0, maxhits):
        data = json.loads(result.data['data'][0])
        dm = float(result.get_distance('location', loc)) / 1609.344
        data['dist_miles'] = "%.1f" % dm
        registries.append(data)
    return loc, registries

def all(indexpath):
    conn = xappy.SearchConnection(indexpath)
    registries = []
    for result in conn.iter_documents():
        data = json.loads(result.data['data'][0])
        registries.append(data)
    return registries

if __name__ == '__main__':
    print search('hospitals.db', "cambridge")
    print all('hospitals.db')
