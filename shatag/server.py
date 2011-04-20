from shatag import *
from bottle import get, post, request, debug
import bottle
import json
from io import TextIOWrapper

store = None
debug(True)

def parse(r):
    encoding = 'utf-8'
    return json.load(TextIOWrapper(request.body), encoding=encoding)

@get('/hash/:hash#[a-f0-9]+#')
def get(hash):
    return {hash: [{'host':h, 'file':f} for (h,f) in store.fetch(hash)]}

@post('/host/:name#[a-z0-9.]+#')
def add(name):
    blob = parse(request)
    for base, item in blob:
        for file, hash in item:
            store.record(name,file,hash)

def run(**kw):
    global store
    try:
        store = Store(kw['database'])
    except KeyError:
        store = Store(Config().database)

    bottle.run(**kw)
