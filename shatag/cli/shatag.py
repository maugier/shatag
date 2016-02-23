#!/usr/bin/env python3
# Copyright 2010 Maxime Augier
# Distributed under the terms of the GNU General Public License

import argparse
import os
import os.path
import shatag
import sys

config = shatag.Config()

parser = argparse.ArgumentParser( description='Display and update xattr-based checksums.')
parser.add_argument('-c','--canonical', action='store_true', help='Output canonical file names.')
parser.add_argument('-t','--tag', action='store_true', help='add checksums to untagged files')
parser.add_argument('-u','--update', action='store_true', help='update outdated checksum')
parser.add_argument('-f','--force', action='store_true', help='recompute all checksums, even on good files')
parser.add_argument('-q','--quiet', action='store_true', help='do not output checksums')
parser.add_argument('-v','--verbose', action='store_true', help='report missing/invalid checksums')
parser.add_argument('-r','--recursive', action='store_true', help='inspect directories recursively')
parser.add_argument('-0','--null', action='store_true', help='separate output records with NULLs instead of newlines')
parser.add_argument('-l','--lookup', action='store_true', help='look up files in the database, color/symbol-code them')
parser.add_argument('-L','--lookup-verbose', action='store_true', help='verbosely list duplicate locations')
parser.add_argument('-p','--put', action='store_true', help='add tags to database')
parser.add_argument('-d','--database', metavar='DB', help='database path for -l/-L mode', default=config.database)
parser.add_argument('-b','--backend', metavar='BACKEND', help='backend for local tag storage', default=config.backend)
parser.add_argument('-n','--name', metavar='NAME', help='name of local storage for -l/-L mode', default=config.name)
parser.add_argument('-R','--remote', metavar='NAME', action='append', help='remote storage to consider for -r/-R mode')
parser.add_argument('files', metavar='FILE', nargs='*', help='files to checksum')
    
def main():

    args = parser.parse_args()
    
    
    if args.files == []:
        if args.tag or args.update:
            print ('shatag: Error: file name(s) required when using -t or -u', file=sys.stderr)
        else:
            args.files = filter(lambda x: (args.recursive or os.path.isfile(x)) 
                                          and not x.startswith('.'), os.listdir('.'))
    
    
    if (args.quiet and (not args.verbose) and not (args.update or args.tag or args.put)):
        print ('shatag: Warning: this combination of flags does not do anything.', file=sys.stderr)
        exit(1)
    
    if (args.quiet and args.null):
        print ('shatag: Warning: --null useless when using --quiet', file=sys.stderr)
    
    
    end = args.null and '\0' or '\n'
    store = None
    
    if args.lookup or args.lookup_verbose or args.put:
        store = shatag.Store(name=args.name, url=args.database)
    
    backend = shatag.backend(args.backend)
    
    def process(filename):
        try:
    
            if args.recursive:
                if os.path.isdir(filename) and not os.path.islink(filename):
                    [ process(os.path.join(filename, e)) for e in os.listdir(filename) if not e.startswith('.') ]
                    return
    
            else:
                if not os.path.isfile(filename) :
                    print ('shatag: Warning: {0} is not a file'.format(filename), file=sys.stderr)
                    return
    
            file = backend.file(filename)
            if args.verbose:
                file.verbose()
    
            if args.force and (args.update or args.tag):
                file.rehash()
    
            if args.update:
                file.update()
    
            if args.tag:
                file.tag()
    
            try:
                if not (args.quiet or args.lookup or args.lookup_verbose):
                    file.fsprint(file.show(canonical = args.canonical), end=end)
    
                if args.put:
                    store.put(file)
    
                if args.lookup:
                    print(store.lookup(file, remotenames=args.remote).pretty())
    
                if args.lookup_verbose:
                    r = store.lookup(file)
                    print ("{0}:".format(file.path(canonical=args.canonical)))
                    for (name,path) in (r.local + r.remote):
                        print("\t{0}:{1}".format(name,path))
    
            except shatag.NoChecksum:
                pass
    
        except IOError as e:
            print ('shatag: "{0}": IOError {1}: {2}'.format(filename, e.errno, e.strerror), file=sys.stderr) 
            if e.errno == 32:
                raise
            if e.errno == 95:
                print ('shatag: "{0}": Operation Unsupported. Did you forget to enable user_xattr ?', file=sys.stderr)
        except OSError as e:
            print ('shatag: {0}'.format(e), file=sys.stderr)
    
    for filename in args.files:
        if args.put and args.recursive:
            store.clear(os.path.abspath(filename))
        process(filename)
    
    if args.put:
    	store.commit()
