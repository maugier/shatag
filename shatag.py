#!/usr/bin/env python3
# Copyright 2010 Maxime Augier
# Distributed under the terms of the GNU General Public License

#import argparse
import hashlib
import os
import os.path
import socket
import sqlite3
import sys
import xattr

def chost():
    (canonical,aliases,addresses) = socket.gethostbyaddr(socket.gethostname())
    return canonical

def hashfile (filename):
    bs=4096
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as fd:    
        while True:
            data = fd.read(bs)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

class NoChecksum(Exception):
    pass

class File:
    def __init__(self, filename, db=None):
        self.filename = filename 
        self.db = db
        self.mtime = int(os.stat(filename).st_mtime)

        lsattr = xattr.listxattr(filename)

        self.ts = None
        self.shatag = None

        try:
            self.ts = int(xattr.getxattr(filename, 'user.shatag.ts'))
            self.shatag = xattr.getxattr(filename, 'user.shatag.sha256').decode('ascii')
        except IOError as e:
            if e.errno != 61:  # No data available
                raise


        if self.mtime == self.ts:
            self.state = 'good'
        elif self.ts is None:      
            self.state = 'missing'
        else:
            self.state = 'bad'

    def fullpath(self):
        return os.path.abspath(self.filename)

    def path(self, canonical=False):
        if canonical:
            return self.fullpath()
        else:
            return self.filename

    def update(self):
        if self.state == 'bad': 
            self.rehash()

    def tag(self):
        if self.state == 'missing' or self.state == 'bad':
            self.rehash()

    def show(self, canonical=False):
        if self.state == 'good':
            return self.shatag + '  ' + self.path(canonical)
        else:
            raise NoChecksum()


    def verbose(self, canonical=False):
        if self.state == 'missing':
            print('<missing>  {0}'.format(self.path(canonical)), file=sys.stderr)
        if self.state == 'bad':
            print('<outdated>  {0}'.format(self.path(canonical)), file=sys.stderr)


    def rehash(self):
        self.ts = self.mtime
        newsum = hashfile(self.filename)
        self.shatag = newsum
        xattr.setxattr(self.filename, 'user.shatag.sha256', newsum.encode('ascii'))
        xattr.setxattr(self.filename, 'user.shatag.ts', str(self.mtime).encode('ascii'))
        self.state = 'good'

class Store:

    def __init__(self, url=None, name=None):

        if url is None:
            url = '{0}/.shatagdb'.format(os.environ['HOME'])

        if name is None:
            name = chost()            

        self.name = name
        db = sqlite3.connect(url)
        self.db = db

        cursor = self.db.cursor()
        self.cursor = cursor

        try:
            cursor.execute('create table contents(hash text, name text, path text, primary key(hash,name,path))')
        except sqlite3.OperationalError as e:
            pass #table already created

    def clear(self, base='/'):
        self.cursor.execute('delete from contents where name = :name and substr(path,1,length(:base)) like :base', {'name': self.name, 'base': base})
        return self.cursor.rowcount

    def put(self, file):
        self.cursor.execute('insert into contents(hash,name,path) values(?,?,?)', (file.shatag, self.name, file.fullpath()))

    def lookup(self, file):

        local = list()
        remote = list()

        if file.state != 'good':
            raise NoChecksum()

        self.cursor.execute('select name,path from contents where hash=?',
            (file.shatag, ))
        for (name, path) in self.cursor:
            if name != self.name:
                remote.append((name,path))
            else:
                if path != file.fullpath():
                    local.append((name,path))

        return StoreResult(file, remote, local) 

    def commit(self):
        self.db.commit()

class StoreResult:
    def __init__(self,file,remote,local):
        self.file = file
        self.remote = remote
        self.local = local

        if self.local:
            self.status = 2
        elif self.remote:
            self.status = 1
        else:
            self.status = 0

    def pretty():
        prefix = '\x1b[33;1m- '
        if self.status == 2:
            prefix = '\x1b[31;1m+ '
        elif self.status == 1:
            prefix = '\x1b[32;1m= '

        return prefix + self.file.filename
        
