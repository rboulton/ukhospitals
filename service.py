#!/usr/bin/env python

import wsgiwapi
import search

@wsgiwapi.jsonreturning
@wsgiwapi.allow_GETHEAD
@wsgiwapi.param("loc", 1, 1, None, [''],
                "The location to search for hospitals near.")
@wsgiwapi.param("maxhits", 1, 1, '[0-9]+', ['10'],
                "The maximum number of hospitals to return.")
@wsgiwapi.param("need_aande", 1, 1, '[01]', ['0'],
                "If 1, only return hospitals with an accident and emergency department.")
def find_hospital(request):
    loc = request.params['loc'][0]
    maxhits = int(request.params['maxhits'][0])
    need_aande = bool(int(request.params['need_aande'][0]))
    res = {}
    if loc == '':
        res['hospitals'] = search.all('hospitals.db', need_aande=need_aande)[:maxhits]
    else:
        res['query_location'] = loc
        res['query_latlong'], res['registries'] = \
            search.search('hospitals.db', loc, maxhits=maxhits,
                          need_aande=need_aande)
    return res

def docs(request):
    tmpl = '''
<html>
  <head>
    <title>Registry Office Locator, API documentation</title>
  </head>
  <body>
    <h1>Registry Office Locator, API documentation</h1>
    <h2>Find offices</h2>
    <p>
      <em>Base url</em>:
        <ul>
          <li>
            <code>http://tartarus.org/richard/registries/find</code>
          </li>
        </ul>
    </p>
    <p>
      <em>Parameters</em>:
      <ul>
        <li>
          <code>loc</code>: The location to centre the search on.  May be an
          address or a postcode.  If omitted, all registry offices will be
          returned (subject to the <code>maxhits</code> parameter).
        </li>
        <li>
          <code>maxhits</code>: The maximum number of matching centres to
          return.  If omitted, defaults to 10.
        </li>
      </ul>
    </p>
    <p>
      <em>Results</em>:
      Returns a JSON object, with the following attributes:
      <ul>
        <li>
          <q><code>query_location</code><q>: The location that was searched for
          (ie, the loc parameter supplied to the search).  Missing if no
          location was specified.
        </li><li>
          <q><code>query_latlong</code></q>: The latitude and longitude
          determined for the location (in decimal, separated by a space).
          Missing if no location was specified.
        </li><li>
          <q><code>registries</code></q>: A list of registries, in order of
          distance from the query location (unless no location specified, in
          which case the order is undefined).  Each registry is a JSON object,
          with the following attributes:
          <ul><li>
            <q><code>name</code></q>: The name of the registry office.
           </li><li>
            <q><code>addresss</code></q>: The address of the registry office.
           </li><li>
            <q><code>postcode</code></q>: The postcode of the registry office.
           </li><li>
            <q><code>longlat</code></q>: The location of the registry office,
            as a list of two items; longitude first.
           </li><li>
            <q><code>dist_miles</code></q>: Distance from the query location in
            miles: omitted if no location was specified.
          </li></ul>
          Other fields may be present, but aren't for all registry offices.
        </li>
      </ul>
    </p>
  </body>
</html>
'''.strip()
    return wsgiwapi.Response(tmpl, content_type='text/html')

def frontpage(request):
    tmpl = '''
<html>
  <head>
    <title>Hospital Locator</title>
  </head>
  <body>
    <ul>
    <li>
    <a href="find">Find offices API</a>
    </li>
    <li>
    <a href="docs">API documentation</a>
    </li></ul>
  </body>
</html>
'''.strip()
    return wsgiwapi.Response(tmpl, content_type='text/html')

def main():
    app = wsgiwapi.make_application({
        'find': find_hospital,
        'docs': docs,
        '': frontpage,
    })

    server = wsgiwapi.make_server(app, ('0.0.0.0', 10011))
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    main()
