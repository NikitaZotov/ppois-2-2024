from controller.web_controller import WebController
from web_app import WebApp


if __name__ == '__main__':
    web_app: WebApp = WebApp()
    web_controller: WebController = WebController(web_app)
    web_controller.run()
