import logging
import os

from flask import Flask


class WebServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def add_route(self, route, handler_func, methods):
        self.app.add_url_rule(route, view_func=handler_func, methods=methods)
