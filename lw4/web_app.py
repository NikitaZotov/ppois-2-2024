# from flask import Flask, render_template, url_for
#
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/<string:operation_name>')
# def make_transaction(operation_name: str):
#     return render_template(f'{operation_name}.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, url_for


class WebApp:
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        self.host: str = host
        self.port: int = port
        self.app = Flask(__name__)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)

    def add_route(self, route: str, handler_func: callable, methods: list[str]):
        self.app.add_url_rule(route, view_func=handler_func, methods=methods)
