#!/usr/bin/env python3
# Copyright 2011 Maxime Augier
# Distributed under the terms of the GNU General Public License

import requests
import json
import shatag.base

class HTTPStore(shatag.base.IStore):
    def __init__(self,url,name):
        super().__init__(url, name)
        self.session = requests.session()
        self.buffer = []

    def get(self,url):
        return json.loads(self.session.get(url, prefetch=True).text)

    def fetch(self,hash):
        data = self.get(self.url + '/find/' + hash)
        for item in data[hash]:
            yield (item['host'], item['file'])

    def checkname(self,name):
        if name != self.name:
            raise Error("Store name {0} != {1}".format(name,self.name))

    def record(self,name,path,hash):
        self.checkname(name)
        self.buffer.append({'path':path, 'hash':hash})

    def clear(self,base,name):
        self.checkname(name)
        self.buffer.append({'clear': base})

    def commit(self):
        self.session.post(self.url + '/host/' + self.name, json.dumps(self.buffer))
        self.buffer = []

    def rollback(self):
        self.buffer = []


