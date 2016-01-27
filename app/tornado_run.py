#coding=utf-8
#!/usr/bin/python

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from Dtoy import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(15000)  
IOLoop.instance().start()