#!/usr/bin/env python3
# Copyright 2010 Maxime Augier
# Distributed under the terms of the GNU General Public License

import shatag
import couchdb


class CouchStore(shatag.IStore):

    def __init__(self, url=None, name=None):
        super(CouchStore,self).__init__(url, name)

        server = couchdb.Server(url)
        self.db = server['shatag']


    def clear(self, base='/'):
        pass

    def record(self, name, path, tag):
        self.db.save({'hash':tag, 'name':name, 'path':path})

    def fetch(self, hash):
        pass    

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

