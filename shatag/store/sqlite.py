#!/usr/bin/env python3
# Copyright 2010 Maxime Augier
# Distributed under the terms of the GNU General Public License

import shatag.base
import sqlite3

class LocalStore(shatag.base.SQLStore):
    def __init__(self, url=None, name=None):
        db = sqlite3.connect(url)
        self.db = db

        cursor = self.db.cursor()
        self.cursor = cursor

        super().__init__(url, name)

        try:
            cursor.execute('create table contents(hash text, name text, path text, primary key(name,path))')
            cursor.execute('create index contents_hash on contents(hash)')
        except sqlite3.OperationalError as e:
            pass #table already created

    def record(self, name, path, tag):
        self.cursor.execute('insert or replace into contents(hash,name,path) values (?,?,?)', (tag,name,path))


