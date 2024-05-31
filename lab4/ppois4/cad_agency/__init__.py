from flask import Flask
from flask_bootstrap import Bootstrap

from cad_agency import model
from cad_agency.model import CadastralAgency, Region

service = CadastralAgency()
service.load()


def get_app():
    app = Flask(__name__)
    service.current_region = Region.MINSK
    app.config['STATIC_FOLDER'] = 'static'
    app.config['STATIC_URL_PATH'] = 'static'
    app.secret_key = "Baccan00!"
    return app