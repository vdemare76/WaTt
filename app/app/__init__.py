import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy import event
from sqlalchemy.engine import Engine
from .security import MySecurityManager

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, security_manager_class=MySecurityManager)

from . import models, views  # noqa
from . import util

util.inizializza_db()