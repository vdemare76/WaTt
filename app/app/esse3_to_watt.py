from flask import flash, render_template, redirect, url_for, request
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError

import requests, base64

url = "https://uniparthenope.esse3.cineca.it/e3rest/api/"

def getAuthToken(token):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + token
        }

        response = requests.request("GET", url + "login", headers=headers, timeout=60)
        authTokenString = response.json()['authToken']

        sample_string_bytes = authTokenString.encode("ascii")
        b64_bytes = base64.b64encode(sample_string_bytes)
        b64_token = b64_bytes.decode("ascii")

        return b64_token

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500

    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500

    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

def getAnniAccademici(token):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + token
        }

        response = requests.request("GET", url + "/offerta-service-v1/offerte", headers=headers, timeout=60)
        return response.json()

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500

    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500

    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500