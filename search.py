#!/usr/bin/env python

import xappy
import geoloc
try:
    import simplejson as json
except ImportError:
    import json

def search(indexpath, loc1, loc2=None, maxhits=10, need_aande=False):
    loc = geoloc.get(loc1, loc2)
    if loc[0] is None:
        return None
    loc = loc[1] + " " + loc[0]
    conn = xappy.SearchConnection(indexpath)
    registries = []
    q = conn.query_distance('location', loc)
    if need_aande:
        q = q.filter(conn.query_field('hasaande', '1'))
    for result in q.search(0, maxhits):
        data = json.loads(result.data['data'][0])
        dm = float(result.get_distance('location', loc)) / 1609.344
        data['dist_miles'] = "%.1f" % dm
        registries.append(data)
    return loc, registries

def all(indexpath, need_aande=False):
    conn = xappy.SearchConnection(indexpath)
    registries = []
    if need_aande:
        it = conn.query_field('hasaande', '1').search(0, conn.get_doccount())
    else:
        it = conn.iter_documents()
    for result in it:
        data = json.loads(result.data['data'][0])
        registries.append(data)
    return registries

if __name__ == '__main__':
    print search('hospitals.db', "cambridge")
    print search('hospitals.db', "cambridge", need_aande=True)
    print all('hospitals.db')
    print all('hospitals.db', need_aande=True)
