#!/usr/bin/env python3

import json, functools, logging
import redis
import tornado.web, tornado.ioloop
import sys

def search(query):
    return functools.reduce(lambda a, b: a & b, [r.smembers(word) for word in query.split()])

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_query_argument("query", default="None")
        if query:
            self.write(json.dumps({"results" : [r.get(result).decode() for result in search(query)]}))

if __name__ == "__main__":
    print(sys.argv)
    r= redis.Redis(host=sys.argv[1] if len(sys.argv)>1 else "localhost")
    tornado.web.Application([(r"/", MainHandler),]).listen(80)
    tornado.ioloop.IOLoop.current().start()
