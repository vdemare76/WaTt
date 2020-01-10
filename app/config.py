import os

from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
    AUTH_OID,
    AUTH_REMOTE_USER
)

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"

SQLALCHEMY_DATABASE_URI =  'mysql+mysqlconnector://watt:wwaatttt@172.100.0.2:3306/wattdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

BABEL_DEFAULT_LOCALE = "it"

LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
    "it": {"flag": "it", "name": "Italiano"}
}

# ------------------------------
# GLOBALS FOR GENERAL APP's
# ------------------------------

AUTH_TYPE = AUTH_LDAP

AUTH_LDAP_SERVER = "ldap://172.100.0.3"
AUTH_LDAP_USE_TLS = False

AUTH_LDAP_SEARCH = "dc=uniparthenope,dc=it"
AUTH_LDAP_BIND_USER = "cn=admin,dc=uniparthenope,dc=it"
AUTH_LDAP_BIND_PASSWORD = "wattpw01"
AUTH_LDAP_UID_FIELD = "uid"

FAB_ROLES = {
    "doce_watt" : [
        [".*", "can_list"],
        [".*", "can_show"],
	    [".*", "menu_access"],
	    [".*", "can_get"],
	    [".*", "can_info"]
    ],
    "tamm_watt" : [
        [".*", "can_list"],
        [".*", "can_show"],
	    [".*", "menu_access"],
	    [".*", "can_get"],
	    [".*", "can_info"],
        [".*", "can_add"],
        [".*", "can_edit"],
	    [".*", "can_delete"]
    ],
    "stud_watt" : [
        [".*", "can_list"],
        [".*", "can_show"],
	    [".*", "menu_access"],
	    [".*", "can_get"],
	    [".*", "can_info"]
    ]
}

AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Admin"

AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"

APP_NAME = "WaTt - Webapp Timetable"
APP_THEME = ""  # default



# APP_THEME = "cerulean.css"      # COOL
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"       # COOL
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"          # COOL
# APP_THEME = "spacelab.css"      # NICE
# APP_THEME = "united.css"
