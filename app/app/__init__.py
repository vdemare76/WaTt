import logging

from flask import Flask, session
from flask_appbuilder import AppBuilder, SQLA
from flask_session import Session
from .security import MySecurityManager
from datetime import timedelta

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = '\2\1thisismyscretkey\1\2\e\y\y\h'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_COOKIE_SECURE'] = True
app.config.from_object("config")

Session(app)
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, security_manager_class=MySecurityManager)

from . import models, views  # noqa
from . import util

@app.before_first_request
def before_request_func():
  #session.clear()
  util.inizializza_db()