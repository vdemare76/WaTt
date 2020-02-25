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
# Profilo DOCENTE
    "doce_watt" : [
        ["AnniAccademiciView", "can_list"],
        ["AnniAccademiciView", "can_show"],
	    ["Anni accademici", "menu_access"],

        ["CorsiDiStudioView", "can_list"],
        ["CorsiDiStudioView", "can_show"],
	    ["Corsi di studio", "menu_access"],

        ["AttivitaDidatticheView", "can_list"],
        ["AttivitaDidatticheView", "can_show"],
	    ["Attività didattiche", "menu_access"],

        ["AuleView", "can_list"],
        ["AuleView", "can_show"],
	["Aule", "menu_access"],

        ["DocentiView", "can_list"],
        ["DocentiView", "can_show"],
	["Docenti", "menu_access"],

        ["OffertaDidatticaView", "can_list"],
        ["OffertaDidatticaView", "can_show"],
	["Offerta Didattica", "menu_access"],

        ["LogisticaDocentiView", "can_list"],
        ["LogisticaDocentiView", "can_show"],
	["LogisticaDocentiView", "can_get"],
	["LogisticaDocentiView", "can_info"],
        ["LogisticaDocentiView", "can_add"],
        ["LogisticaDocentiView", "can_edit"],
	["LogisticaDocentiView", "can_delete"],
	["Logistica docenti", "menu_access"]
    ],

    # Profilo PERSONALE TECNICO AMMINISTRATIVO
    "tamm_watt" : [
        ["AnniAccademiciView", "can_list"],
        ["AnniAccademiciView", "can_show"],
        ["AnniAccademiciView", "can_get"],
        ["AnniAccademiciView", "can_info"],
        ["AnniAccademiciView", "can_add"],
        ["AnniAccademiciView", "can_edit"],
        ["AnniAccademiciView", "can_delete"],
        ["Anni accademici", "menu_access"],

        ["CorsiDiStudioView", "can_list"],
        ["CorsiDiStudioView", "can_show"],
        ["CorsiDiStudioView", "can_get"],
        ["CorsiDiStudioView", "can_info"],
        ["CorsiDiStudioView", "can_add"],
        ["CorsiDiStudioView", "can_edit"],
        ["CorsiDiStudioView", "can_delete"],
        ["Corsi di studio", "menu_access"],

        ["AttivitaDidatticheView", "can_list"],
        ["AttivitaDidatticheView", "can_show"],
        ["AttivitaDidatticheView", "can_get"],
        ["AttivitaDidatticheView", "can_info"],
        ["AttivitaDidatticheView", "can_add"],
        ["AttivitaDidatticheView", "can_edit"],
        ["AttivitaDidatticheView", "can_delete"],
        ["Attività didattiche", "menu_access"],

        ["AuleView", "can_list"],
        ["AuleView", "can_show"],
        ["AuleView", "can_get"],
        ["AuleView", "can_info"],
        ["AuleView", "can_add"],
        ["AuleView", "can_edit"],
        ["AuleView", "can_delete"],
        ["Aule", "menu_access"],

        ["DocentiView", "can_list"],
        ["DocentiView", "can_show"],
        ["DocentiView", "can_get"],
        ["DocentiView", "can_info"],
        ["DocentiView", "can_add"],
        ["DocentiView", "can_edit"],
        ["DocentiView", "can_delete"],
        ["Docenti", "menu_access"],

        ["OffertaDidatticaView", "can_list"],
        ["OffertaDidatticaView", "can_show"],
        ["OffertaDidatticaView", "can_get"],
        ["OffertaDidatticaView", "can_info"],
        ["OffertaDidatticaView", "can_add"],
        ["OffertaDidatticaView", "can_edit"],
        ["OffertaDidatticaView", "can_edit"],
        ["Offerta Didattica", "menu_access"],

        ["LogisticaDocentiView", "can_list"],
        ["LogisticaDocentiView", "can_show"],
        ["LogisticaDocentiView", "can_get"],
        ["LogisticaDocentiView", "can_info"],
        ["LogisticaDocentiView", "can_add"],
        ["LogisticaDocentiView", "can_edit"],
        ["LogisticaDocentiView", "can_delete"],
        ["Logistica docenti", "menu_access"]
    ],

    # Profilo STUDENTE
    "stud_watt" : [
        ["OffertaDidatticaView", "can_list"],
        ["OffertaDidatticaView", "can_show"],
        ["Offerta Didattica", "menu_access"]
    ],

    # Profilo AMMINISTRATORE
    "admin_watt" : [
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
