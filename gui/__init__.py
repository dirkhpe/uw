import os
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

bootstrap = Bootstrap()

del os.environ["http_proxy"]
del os.environ["https_proxy"]

def create_app(config_class=Config):
    """
    Create an application instance.
    :param config_class: Pointer to the configuration file.
    :return: the configured application object.
    """
    app = Flask(__name__)

    # import configuration
    app.config.from_object(config_class)

    # Configure Logger
    # my_env.init_loghandler(__name__, app.config.get('LOGDIR'), app.config.get('LOGLEVEL'))

    # initialize extensions
    bootstrap.init_app(app)

    # import blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
