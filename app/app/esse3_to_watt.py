from flask import flash, render_template, redirect, url_for, request, g
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError

import requests, base64
from .util import getLdapToken

url = "https://uniparthenope.esse3.cineca.it/e3rest/api/"

def getAuthToken(token):

    token = getLdapToken(g.user.username)

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

''' Returns a list of academic years for which an educational offer is registered.
    Example 2020 stands for 2020-21'''

def getAcademicYears():

    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    else:
        token = getAuthToken(token)

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + token
        }

        response = requests.request("GET", url + "/offerta-service-v1/offerte", headers=headers, timeout=60)
        data = response.json()
        size = len(data)
        uniqueAY = []
        for i in range(0, size, 1):
            if (data[i]["aaOffId"] not in uniqueAY and data[i]["aaOffId"]>=2017):
                uniqueAY.append(data[i]["aaOffId"])
        uniqueAY.sort()
        return uniqueAY

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500

    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500

    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

''' returns all courses on offer for the selected academic year '''
def getEducationalOffer(academicYear):
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    else:
        token = getAuthToken(token)

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + token
        }

        response = requests.request("GET", url + "/offerta-service-v1/offerte?aaOffId=" + str(academicYear), headers=headers, timeout=60)
        data = response.json()
        size = len(data)
        courses = []
        for i in range(0, size, 1):
            courses.append({'courseId':data[i]["cdsOffId"],
                            'courseCod':data[i]["cdsCod"],
                            'courseDes':data[i]["cdsDes"]})
        return courses

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500

    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500

    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

'''returns the information of the selected courses'''
def getCouseData(academicYear, courses):
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    else:
        token = getAuthToken(token)

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + token
        }

        for c in courses:
            flash(c)

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500

    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500

    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500