import threading
import pickle
from server import WebServer
from controller import CLIController, WebController
from hotel import Hotel


def hello_world():
    return 'Hello World!'


def run_web_server(hotel_instance: Hotel):
    server = WebServer()
    web_controller = WebController(hotel_instance, server)
    web_controller.perform()


def run_cli(hotel_instance: Hotel):
    cli = CLIController(hotel_instance)
    cli.perform()


if __name__ == '__main__':
    hotel: Hotel
    with open('resources/save.pkl', 'rb') as f:
        hotel = pickle.load(f)
    cli_thread = threading.Thread(target=run_cli, args=(hotel,))
    flask_thread = threading.Thread(target=run_web_server, args=(hotel,))

    cli_thread.start()
    flask_thread.start()

    cli_thread.join()
    flask_thread.join()
