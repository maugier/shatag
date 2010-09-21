#!/usr/bin/python

import web
import psycopg2

conn = psycopg2.connect("dbname=shatag")

urls = ( '/hash/([a-f0-9]{64})', 'Hash')
#         '/base/(.*)/(.*)', 'Base' )

app = web.application(urls, globals())

class Hash:
    def GET(self, hash):
        return "Got hash {0}".format(hash)

    def POST(self, hash):
        return "Posted {0}".format(hash)


class Base:
    def GET(self, name, file):
        return "Got name {0} file {1}".format(name,file)


if __name__ == '__main__':
    app.run()
