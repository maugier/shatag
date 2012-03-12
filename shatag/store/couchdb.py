#!/usr/bin/env python3
# Copyright 2010 Maxime Augier
# Distributed under the terms of the GNU General Public License

#import argparse
from shatag import *
import json
import couchdb


class CouchStore(IStore):

    def __init__(self, url=None, name=None):
        super().__init__(url, name)

        server = couchdb.Server(url)
        self.db = server['shatag']


    def clear(self, base='/'):
        pass

    def record(self, name, path, tag):
        self.db.save({'hash':tag, 'name':name, 'path':path})

    def lookup(self, file, remotenames=None):

        local = list()
        remote = list()

        if file.state != 'good':
            raise NoChecksum()

        for (name, path) in self.fetch():
        
            if ((remotenames is None and name != self.name) or
               (remotenames is not None and name in remotenames)):
                    remote.append((name,path))
            elif path != file.fullpath():
                local.append((name,path))

        return StoreResult(file, remote, local) 

    def fetch(self, hash):
        pass    

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

