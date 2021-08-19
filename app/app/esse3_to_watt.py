from flask import flash, render_template, redirect, url_for, request
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError

import requests, base64
import ldap
from ldap.filter import escape_filter_chars

url = "https://uniparthenope.esse3.cineca.it/e3rest/api/"
headers = {
    'Content-Type': "application/json",
    "Authorization": "Basic " + "MDEwODAwMTY3MjoyMkxlb24wOQ=="
}

def getToken():
    s = Server(172.100.0.3, get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

    # the following is the user_dn format provided by the ldap server
    user_dn = "uid=" + user + ",ou=people,dc=uniparthenope,dc=it"

    # define the connection
    c = Connection(s, user=user_dn, password=passwd)
    # print(c)

    # perform the Bind operation
    c.bind()

    if c.result['result'] == 0:
        print("LDAP people!")

        c.result["user"] = {"grpDes": "PTA", "grpId": 99, "userId": user}
        return c.result