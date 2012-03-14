#!/usr/bin/env python3
# Copyright 2011 Maxime Augier
# Distributed under the terms of the GNU General Public License

import requests
import json
import shatag.base

class HTTPStore(shatag.base.IStore):
    def __init__(self,url,name):
        verify=True

        if url.startswith('insecure-https://'):
            url = url[9:]
            verify=False
		
        super().__init__(url, name)
        self.session = requests.session(verify=verify)
        self.buffer = []
        info = self.get(url)

        version = self.get(url).get('shatag-version')
        if version is None:
            raise Exception('Configured URL does not answer like a shatag endpoint: {0}'.format(url))
        if version != 1:
            raise Exception('Configured URL uses incompatible protocol version {0}: {1}'.format(version,url))

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
        self.session.post(self.url + '/host/' + self.name, json.dumps(self.buffer)).raise_for_status()
        self.buffer = []

    def rollback(self):
        self.buffer = []


