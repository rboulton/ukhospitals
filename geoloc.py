#!/usr/bin/env python

import urllib
import urllib2
import simplejson
import private_passwords
import threading
import time
import csv

cache = {}
cache_lock = threading.Lock()
cache_file = 'locations.csv'
cache_fd = open(cache_file, 'a+')
cache_dump_writer = csv.writer(cache_fd)
for row in csv.reader(open(cache_file)):
    cache[row[0]] = row[1:]

def fetch(url, params):
    url += '?' + urllib.urlencode(params)
    result = urllib2.urlopen(url).read()
    json = simplejson.loads(result)
    return json
                 
def get_loc(location):
    """Get the (longitude, latitude) for a postcode.

    """
    time.sleep(0.5)
    url = "http://maps.google.com/maps/geo"
    if not location.lower().endswith('uk'):
        location += ', UK'
    params = {
        'q': location,
        'output': 'json',
        'sensor': 'false',
        'key': private_passwords.GOOGLE_MAPS_KEY,
    }
    location = fetch(url, params)
    status = location["Status"]["code"]
    if status != 200:
        return '', ''
    try:
        country_code = location["Placemark"][0]["AddressDetails"]["Country"]["CountryNameCode"]
        if country_code != "GB":
	    return '', ''
    except KeyError:
        pass
    longitude, latitude, height = location["Placemark"][0]["Point"]["coordinates"]
    if longitude is None:
        return '', ''
    return str(longitude), str(latitude)

def cached_get_loc(loc):
    cache_lock.acquire()
    try:
        try:
            coords = cache[loc]
        except KeyError:
            cache_lock.release()
            try:
                coords = get_loc(loc)
            finally:
                cache_lock.acquire()
            cache[loc] = coords
            cache_dump_writer.writerow((loc, coords[0], coords[1]))
        return coords
    finally:
        cache_lock.release()

def get(loc1, loc2=None):
    loc = cached_get_loc(loc1)
    if loc[0] == '':
        if loc2 is not None:
            loc = cached_get_loc(loc2)
    return loc

if __name__ == '__main__':
    print get('cb224qn')
    print get('58 Kingsway, Duxford')
