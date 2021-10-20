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
AUTH_LDAP_PORT = "389"
AUTH_LDAP_USE_TLS = False

AUTH_LDAP_SEARCH = "dc=uniparthenope,dc=it"
AUTH_LDAP_BIND_USER = "cn=admin,dc=uniparthenope,dc=it"
AUTH_LDAP_BIND_PASSWORD = "wattpw01"
AUTH_LDAP_UID_FIELD = "uid"

FAB_ROLES = {
# Profilo DOCENTE
    "doce_watt" : [
        ["Tabelle di base", "menu_access"],
        ["Didattica", "menu_access"],
        ["Offerta didattica", "menu_access"],
        ["Admin", "menu_access"],
       
        ["SlotView", "can_list"],["SlotView", "can_show"],["SlotView", "can_download"],
        ["Slot", "menu_access"],
        
        ["GiorniView", "can_list"],["GiorniView", "can_show"],["GiorniView", "can_download"],
        ["Giorni", "menu_access"],
               
        ["AnniAccademiciView", "can_list"],["AnniAccademiciView", "can_show"],["AnniAccademiciView", "can_download"],
        ["Anni Accademici", "menu_access"],
        
        ["AuleView", "can_list"],["AuleView", "can_show"],["AuleView", "can_download"],
        ["Aule", "menu_access"],
     
        ["CorsidistudioView", "can_list"],["CorsidistudioView", "can_show"],["CorsidistudioView", "can_download"],
        ["Corsi di studio", "menu_access"],
        
        ["DocentiView", "can_list"],["DocentiView", "can_show"],["DocentiView", "can_download"],
        ["Docenti", "menu_access"],
           
        ["AttivitaDidatticheView", "can_list"],["AttivitaDidatticheView", "can_show"],["AttivitaDidatticheView", "can_download"],
        ["Attività didattiche", "menu_access"], 
        
        ["OffertaView", "can_list"],["OffertaView", "can_show"],["OffertaView", "can_download"],
        ["Offerta", "menu_access"],
        
        ["ModuliView", "can_list"],["ModuliView", "can_show"],["ModuliView", "can_download"],
        ["Moduli", "menu_access"],
        
        ["LogisticaDocentiView", "can_list"],["LogisticaDocentiView", "can_show"],["LogisticaDocentiView", "can_add"],
        ["LogisticaDocentiView", "can_edit"],["LogisticaDocentiView", "can_delete"],["LogisticaDocentiView", "can_download"],
        ["Logistica docenti", "menu_access"],
        
        ["Calendario orario", "menu_access"],
        ["CalendarioView", "can_cld_home"]
    ],

    # Profilo PERSONALE TECNICO AMMINISTRATIVO
    "tamm_watt" : [
        ["Tabelle di base", "menu_access"],
        ["Didattica", "menu_access"],
        ["Offerta didattica", "menu_access"],
        ["Orario", "menu_access"],
        ["Utilità", "menu_access"],
       
        ["SlotView", "can_list"],["SlotView", "can_show"],["SlotView", "can_add"],
        ["SlotView", "can_edit"],["SlotView", "can_delete"],["SlotView", "can_download"],
        ["Slot", "menu_access"],
        
        ["GiorniView", "can_list"],["GiorniView", "can_show"],["GiorniView", "can_add"],
        ["GiorniView", "can_edit"],["GiorniView", "can_delete"],["GiorniView", "can_download"],
        ["Giorni", "menu_access"],
               
        ["AnniAccademiciView", "can_list"],["AnniAccademiciView", "can_show"],["AnniAccademiciView", "can_add"],
        ["AnniAccademiciView", "can_edit"],["AnniAccademiciView", "can_delete"],["AnniAccademiciView", "can_download"],
        ["Anni Accademici", "menu_access"],
        
        ["AuleView", "can_list"],["AuleView", "can_show"],["AuleView", "can_add"],
        ["AuleView", "can_edit"],["AuleView", "can_delete"],["AuleView", "can_download"],
        ["Aule", "menu_access"],
     
        ["CorsiDiStudioView", "can_list"],["CorsiDiStudioView", "can_show"],["CorsiDiStudioView", "can_add"],
        ["CorsiDiStudioView", "can_edit"],["CorsiDiStudioView", "can_delete"],["CorsiDiStudioView", "can_download"],
        ["Corsi di Studio", "menu_access"],
        
        ["DocentiView", "can_list"],["DocentiView", "can_show"],["DocentiView", "can_add"],
        ["DocentiView", "can_edit"],["DocentiView", "can_delete"],["DocentiView", "can_download"],
        ["Docenti", "menu_access"],

        ["NumerositaAnniCorsoView", "can_list"], ["NumerositaAnniCorsoView", "can_show"], ["NumerositaAnniCorsoView", "can_add"],
        ["NumerositaAnniCorsoView", "can_edit"], ["NumerositaAnniCorsoView", "can_delete"], ["NumerositaAnniCorsoView", "can_download"],
        ["Numerosità anni corso", "menu_access"],
           
        ["AttivitaDidatticheView", "can_list"],["AttivitaDidatticheView", "can_show"],["AttivitaDidatticheView", "can_add"],
        ["AttivitaDidatticheView", "can_edit"],["AttivitaDidatticheView", "can_delete"],["AttivitaDidatticheView", "can_download"],
        ["Attività didattiche", "menu_access"], 
        
        ["OffertaView", "can_list"],["OffertaView", "can_show"],["OffertaView", "can_add"],
        ["OffertaView", "can_edit"],["OffertaView", "can_delete"],["OffertaView", "can_download"],
        ["Offerta", "menu_access"],
        
        ["ModuliView", "can_list"],["ModuliView", "can_show"],["ModuliView", "can_add"],
        ["ModuliView", "can_edit"],["ModuliView", "can_delete"],["ModuliView", "can_download"],
        ["Moduli", "menu_access"],
        
        ["LogisticaDocentiView", "can_list"],["LogisticaDocentiView", "can_show"],["LogisticaDocentiView", "can_add"],
        ["LogisticaDocentiView", "can_edit"],["LogisticaDocentiView", "can_delete"],["LogisticaDocentiView", "can_download"],
        ["Logistica docenti", "menu_access"],

        ["ChiusuraView", "can_list"], ["ChiusuraView", "can_show"], ["ChiusuraView", "can_add"],
        ["ChiusuraView", "can_edit"], ["ChiusuraView", "can_delete"], ["ChiusuraView", "can_download"],
        ["Imposta chiusure", "menu_access"],

        ["OrariGeneratiView", "can_list"], ["OrariGeneratiView", "can_show"], ["OrariGeneratiView", "can_download"],
        ["OrariGeneratiView", "can_edit"], ["Orari generati", "menu_access"],
        ["OrariGeneratiView", "cancella"], ["OrariGeneratiView", "carica_schema"],
        ["OrariGeneratiView", "genera_calendario"],

        ["Funzioni utilità", "menu_access"],
        ["UtilitaView", "can_srv_home"], ["UtilitaView", "can_srv_util"],
        ["Connettore Esse3", "menu_access"],
        ["UtilitaEsse3View", "can_srv_esse3_home"], ["UtilitaEsse3View", "can_srv_esse3_util"],
        ["Elaborazione orario", "menu_access"],   
        ["PreferenzeView", "can_prf_home"], ["PreferenzeView", "can_prf_calc"],
        ["Schema settimanale", "menu_access"],
        ["SchemaSettimanaleView", "can_wsk_home"],
        ["Calendario orario", "menu_access"],
        ["CalendarioView", "can_cld_home"], ["CalendarioView", "can_cld_ver"],
        ["CalendarioView", "can_cld_mod"], ["CalendarioView", "can_cld_upd"],
        ["CalendarioView", "can_cld_room"]
    ],

    # Profilo STUDENTE
    "stud_watt" : [        
        ["Calendario orario", "menu_access"],
        ["CalendarioView", "can_cld_home"]
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
