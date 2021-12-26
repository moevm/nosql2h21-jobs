from pathlib import Path

# from swagger_ui_bundle import swagger_ui_path
import connexion
import flask.app
from flask import send_file, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from hh_api.hh_api import Hh_api
from neo_api.neo_api import Neo_api
from . import settings

neo_api: Neo_api = None  # Neo_api()
hh_api: Hh_api = None  # Hh_api()


def create_app(config_filename: str = None):
    config = settings.read(config_filename)
    global neo_api
    global hh_api
    neo_api = Neo_api(config.NEO4J_HOST)
    hh_api = Hh_api()

    # SWAGGER_URL = '/api/ui'
    SWAGGER_DIR = "openapi/"
    SWAGGER_FILE = "swagger.yml"
    # SWAGGER_PATH = os.path.abspath('openapi/swagger.yml')
    # API_URL = 'http://127.0.0.1:5000/swagger'

    swagger_Path = (Path(__path__[0])/SWAGGER_DIR / SWAGGER_FILE).resolve()

    # print("Swagger path:", swagger_Path)

    connex_app = connexion.App(__name__, specification_dir=swagger_Path.parent.as_posix())
    connex_app.add_api(swagger_Path.name)

    # swaggerui_blueprint = get_swaggerui_blueprint(
    #         swagger_Path.as_posix(),
    #         # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    #         config.API_URL,
    #         config={  # Swagger UI config overrides
    #                 'app_name': config.APP_NAME
    #         },
    # )
    app:flask.app.Flask = connex_app.app

    # app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config)

    @app.errorhandler(HTTPException)
    def http_error_handler(err):
        return {'message': err.description}, err.code

    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get('headers')
        messages = err.data.get('messages', ['Invalid request.'])
        if headers:
            return jsonify({'errors': messages}), err.code, headers
        else:
            return jsonify({'errors': messages}), err.code

    @app.route('/swagger')
    def return_swagger():
        try:
            return send_file(swagger_Path.as_posix(),
                             attachment_filename='swagger.yml')
        except Exception as e:
            return str(e)

    with app.app_context():
        app
        # from webapp.models import db
        # db.app = app
        # db.init_app(app)
        # db.create_all()
        #
        # from webapp.main import routes
        # app.register_blueprint(routes.main_bp)

        return app

    # return app
