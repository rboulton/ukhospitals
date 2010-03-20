#!/usr/bin/env python

import os
import shutil
import xappy
try:
    import simplejson as json
except ImportError:
    import json

def build(indexpath, jsonpath):
    conn = xappy.IndexerConnection(indexpath)
    conn.add_field_action('location', xappy.FieldActions.GEOLOCATION)
    conn.add_field_action('data', xappy.FieldActions.STORE_CONTENT)
    conn.add_field_action('hasaande', xappy.FieldActions.INDEX_EXACT)
    data = json.loads(open(jsonpath).read())
    for item in data:
        doc = xappy.UnprocessedDocument()
        doc.id = item['name'] + ' ' + item['postcode']
        if bool(item.get('hasaande', False)):
            doc.append('hasaande', '1')
        doc.append('location', item['latitude'] + ' ' + item['longitude'])
        doc.append('data', json.dumps(item))
        conn.replace(doc)
    conn.flush()

if __name__ == '__main__':
    if os.path.exists('hospitals.db.tmp'):
        shutil.rmtree('hospitals.db.tmp')
    build('hospitals.db.tmp', 'hosplocs.json')
    if os.path.exists('hospitals.db'):
        os.rename('hospitals.db', 'hospitals.db.old')
    os.rename('hospitals.db.tmp', 'hospitals.db')
    if os.path.exists('hospitals.db.old'):
        shutil.rmtree('hospitals.db.old')
