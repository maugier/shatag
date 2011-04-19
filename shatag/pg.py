#!/usr/bin/env python3
# Copyright 2010 Maxime Augier
# Distributed under the terms of the GNU General Public License


from shatag import *
import psycopg2

class PgStore(SQLStore):
    def __init__(self, url=None, name=None):
        db = psycopg2.connect(url[3:])
        self.db = db

        cursor = db.cursor()
        self.cursor = cursor

        super().__init__(url, name)

        try:
            cursor.execute('create table contents(hash varchar(64), name varchar(50), path varchar(100), primary key (name, path))')
            cursor.execute('create index content_hash on contents(hash)')
        except psycopg2.ProgrammingError as e:
            pass

