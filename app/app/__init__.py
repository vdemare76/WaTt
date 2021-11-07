import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from .security import MySecurityManager

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True

db = SQLA(app)
appbuilder = AppBuilder(app, db.session, security_manager_class=MySecurityManager)

from . import models, views  # noqa
from . import util

@app.before_first_request
def before_request_func():
  util.inizializza_db()