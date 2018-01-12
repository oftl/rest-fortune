#!/usr/bin/env python3

import bottle
from bottle import request, response, route, post, get, run, template
import logging
import json
import subprocess


#  def get_logger():
#      # TODO move to logfile
#      handler = logging.FileHandler ('./fortune.log')
#      handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
#  
#      logger = logging.getLogger ('fortune')
#      logger.addHandler (handler)
#      logger.setLevel (logging.INFO)
#  
#      return logger
#
# logger = get_logger()


mk_url = lambda path: '{scheme}://{host}/{path}'.format (
    scheme = request.urlparts[0],
    host   = request.urlparts[1],
    path   = path,
)

def res ():
    return dict (
        collection = dict (
            version = '1.0',
            href = '/',
            links = [
                dict (
                    # also prompt and name are allowed here!
                    href = mk_url ('/'),
                    rel = 'fortune',
                    render = 'link',
                ),
                dict (
                    href = mk_url ('/offensive'),
                    rel = 'offensive fortune',
                    render = 'link',
                ),
            ],
            queries = None,
            template = None,
            error = None,
        ),
    )

app = bottle.Bottle(autojson = False)

@app.get('/')
def root():
    fortune = subprocess.run (
        'fortune',
        stdout = subprocess.PIPE,
    ).stdout.decode()

    r = res()
    r.get('collection').update (dict (
        items = [
            dict (
                href  = mk_url ('/'),
                data = [
                    dict (name = 'fortune', value = fortune)
                ],
            )
        ],
    ))

    response.set_header ('Content-Type', 'application/vnd.collection+json')
    return json.dumps (r)

@app.get('/short')
def short():
    fortune = subprocess.run (
        ['fortune', '-s'],
        stdout = subprocess.PIPE,
    ).stdout.decode()

    r = res()
    r.get('collection').update (dict (
        items = [
            dict (
                href  = mk_url ('/'),
                data = [
                    dict (name = 'fortune', value = fortune)
                ],
            )
        ],
    ))

    response.set_header ('Content-Type', 'application/vnd.collection+json')
    return json.dumps (r)


@app.get('/offensive')
def root():
    fortune = subprocess.run (
        ('fortune', '-o'),
        stdout = subprocess.PIPE,
    ).stdout.decode()

    r = res()
    r.get('collection').update (dict (
        items = [
            dict (
                href  = mk_url ('/offensive'),
                data = [
                    dict (name = 'offensive fortune', value = fortune)
                ],
            )
        ],
    ))

    response.set_header ('Content-Type', 'application/vnd.collection+json')
    return json.dumps (r)

app.run (
    host = 'localhost',
    port = 8080,
)
