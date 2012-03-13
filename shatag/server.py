from shatag import *
import bottle
import json
from io import TextIOWrapper

def parse(r):
    encoding = 'utf-8'  #todo: get encoding from headers
    return json.load(TextIOWrapper(r.body, encoding=encoding))

class ShatagServer(bottle.Bottle):
    """A Bottle server that exposes a store trough a restful JSON-based API."""
    def __init__(self, store=None):
        super(ShatagServer, self).__init__()
        if store is None:
            store = Config().database
        self.shatag_store = Store(store)

        @self.get('/find/<hash:re:[a-f0-9]+>')
        def callback(hash):
            return {hash: [{'host':h, 'file':f} for (h,f) in self.shatag_store.fetch(hash)]}

        @self.get('/where/<hash:re:[a-f0-9]+>')
        def callback(hash):
            return {hash: [h for (h,f) in self.shatag_store.fetch(hash)]}

        @self.post('/host/<name:re:[a-z0-9.]+>')
        def callback(name):
            blob = parse(bottle.request)
            for item in blob:
                if 'clear' in item:
                    self.shatag_store.clear(item['clear'],name)
                elif 'path' in item:
                    self.shatag_store.record(name,item['path'],item['hash'])
            self.shatag_store.commit()
