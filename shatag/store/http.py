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

    def call(self,url):
        return json.loads(self.session.get(url, prefetch=True).text)

    def fetch(self,hash):
        data = self.call(self.url + '/find/' + hash)
        for item in data[hash]:
            yield (item['host'], item['file'])


