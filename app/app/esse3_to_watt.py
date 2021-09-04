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

        response = requests.request("GET", url + "offerta-service-v1/offerte", headers=headers, timeout=60)
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

        response = requests.request("GET", url + "offerta-service-v1/offerte?aaOffId=" + str(academicYear), headers=headers, timeout=60)
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
def getCourseData(academicYear, courses):
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

        acts = []
        for c in courses:
            response = requests.request('GET', url + 'offerta-service-v1/offerte/' + str(academicYear) +'/' + str(c) + '/attivita',
                                    headers=headers, timeout=60)
            data = response.json()
            size = len(data)
            for i in range(0, size, 1):
                if data[i]['nonErogabileOdFlg']==0:
                    response = requests.request('GET', url + 'logistica-service-v1/logistica?aaOffId=' + str(academicYear) +'&adId=' + str(data[i]['chiaveAdContestualizzata']['adId']),
                                            headers=headers, timeout=60)
                    data_log = response.json()
                    if len(data_log) > 0:
                        adLogId = data_log[0]['chiavePartizione']['adLogId']
                        if data_log[0]['chiavePartizione']['partCod']=='S2':
                            semester=2
                        else:
                            semester=1
                        '''response = requests.request('GET', url + 'logistica-service-v1/logistica?adLogId=' + str(adLogId) + '/udLogConDettagli',
                                                    headers=headers, timeout=60)'''
                        acts.append({'id': data[i]['chiaveAdContestualizzata']['adId'],
                                     'cod': data[i]['chiaveAdContestualizzata']['adCod'],
                                     'des': data[i]['chiaveAdContestualizzata']['adDes'],
                                     'adLogId': str(adLogId),
                                     'semester': str(semester),
                                     'tip': data[i]['tipoInsCod']})

        for a in acts:
            flash(a)

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500

    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500

    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500