from flask import flash, render_template, redirect, url_for, request, g, session
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError

import requests, base64
from .util import getLdapToken

url = "https://uniparthenope.esse3.cineca.it/e3rest/api/"

def getAuthToken():

    token=getLdapToken(g.user.username)

    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + token
    }

    try:
        response=requests.request("GET", url + "login", headers=headers, timeout=60)
        authTokenString=response.json()['authToken']

        sample_string_bytes=authTokenString.encode("ascii")
        b64_bytes=base64.b64encode(sample_string_bytes)
        b64_token=b64_bytes.decode("ascii")

        return b64_token

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

def getHeaders():
    try:
        token=session['token']
    except:
        session['token']=getAuthToken()
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + session['token']
    }

''' Returns a list of academic years for which an educational offer is registered.
    Example 2020 stands for 2020-21. '''
def getAcademicYears():
    try:
        response=requests.request("GET", url+"offerta-service-v1/offerte", headers=getHeaders(), timeout=60)
        data=response.json()
        size=len(data)
        uniqueAY=[]
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

''' Returns all courses on offer for the selected academic year. '''
def getEducationalOffer(academicYear):
    try:
        response=requests.request("GET", url+"offerta-service-v1/offerte?aaOffId="+ str(academicYear), headers=getHeaders(), timeout=60)
        data=response.json()
        size=len(data)
        courses=[]
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

''' Returns the rules associated with the course. '''
def getRegScheme(cdsId):
    try:
        schemeSet=[]
        response=requests.request('GET', url+'regsce-service-v1/regsce?cdsId='+str(cdsId), headers=getHeaders(), timeout=60)
        dataRegSce=response.json()
        size=len(dataRegSce)
        if size > 0:
            for i in range(0, size, 1):
                response = requests.request('GET',url+'/regsce-service-v1/regsce/'+str(dataRegSce[i]['regsceId'])+'/schemi', headers=getHeaders(), timeout=60)
                dataScheme = response.json()
                if len(dataScheme) > 0 and dataScheme[0]['statutarioFlg'] == 1:
                    schemeSet.append({'regSceId': dataRegSce[i]['regsceId'], 'schemeId': dataScheme[0]['schemaId']})
        else:
            flash('regSceId could not be retrieved!','danger')
        return schemeSet

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

''' Returns the study plan outline associated with the course rules. '''
def getScheme(regScheme):
    try:
        scheme={}
        size=len(regScheme)
        if size>0:
            for i in range(0, size, 1):
                response = requests.request('GET', url+'regsce-service-v1/regsce/'+str(regScheme[i]['regSceId'])+'/schemi/'+str(regScheme[i]['schemeId']), headers=getHeaders(), timeout=60)
                data=response.json()
                sizeReg=len(data['regoleDiScelta'])
                for r in range(0, sizeReg, 1):
                    sizeBlk=len(data['regoleDiScelta'][r]['blocchi'])
                    for b in range(0, sizeBlk, 1):
                        sizeAct=len(data['regoleDiScelta'][r]['blocchi'][b]['attivita'])
                        for a in range(0, sizeAct, 1):
                            scheme[data['regoleDiScelta'][r]['blocchi'][b]['attivita'][a]['chiaveADContestualizzata']['adId']] = \
                                {'yearOfCourse': data['regoleDiScelta'][r]['annoCorso'],
                                 'cfu': data['regoleDiScelta'][r]['blocchi'][b]['attivita'][a]['peso']}
        return scheme

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

''' Returns the information of the selected courses. '''
def getTeachingOfCourse(academicYear, courses):
    try:
        acts=[]

        for cdsId in courses:
            scheme = getScheme(getRegScheme(cdsId))
            response = requests.request('GET', url+'offerta-service-v1/offerte/'+str(academicYear)+'/'+str(cdsId)+'/attivita', headers=getHeaders(), timeout=60)
            dataOff = response.json()
            size = len(dataOff)
            for i in range(0, size, 1):
                ad_id = dataOff[i]['chiaveAdContestualizzata']['adId']
                if dataOff[i]['nonErogabileOdFlg']==0:
                    response = requests.request('GET', url+'logistica-service-v1/logistica?aaOffId='+str(academicYear)+'&adId='+str(ad_id), headers=getHeaders(), timeout=60)
                    dataLog = response.json()
                    if len(dataLog) > 0:
                        adLogId = dataLog[0]['chiavePartizione']['adLogId']
                        if dataLog[0]['chiavePartizione']['partCod'] in ['S2','Q2']:
                            semester=2
                        else:
                            semester=1
                        try:
                            yearOfCourse=scheme[dataOff[i]['chiaveAdContestualizzata']['adId']]['yearOfCourse']
                            cfu=scheme[dataOff[i]['chiaveAdContestualizzata']['adId']]['cfu']
                        except:
                            yearOfCourse=-1
                            cfu=-1
                        acts.append({'cdsId': dataLog[0]['chiaveADFisica']['cdsId'],
                                     'adId': dataOff[i]['chiaveAdContestualizzata']['adId'],
                                     'adCod': dataOff[i]['chiaveAdContestualizzata']['adCod'],
                                     'adDes': dataOff[i]['chiaveAdContestualizzata']['adDes'],
                                     'adLogId': str(adLogId),
                                     'semester': str(semester),
                                     'tip': dataOff[i]['tipoInsCod'],
                                     'yearOfCourse': yearOfCourse,
                                     'cfu': cfu
                                    })
        getTeachers(acts)
        return acts

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

''' Returns the information of the selected courses to be loaded into the database. '''
def getCoursesInfo(courses):
    courseList=[]

    for cdsId in courses:
        course = {}
        found=False

        try:
            response=requests.request('GET', url+'struttura-service-v1/corsi/'+str(cdsId), headers=getHeaders(), timeout=60)
            dataCrs=response.json()
            response=requests.request('GET', url+'struttura-service-v1/corsi/'+str(cdsId)+'/ordinamenti', headers=getHeaders(), timeout=60)
            dataOrd=response.json()
        except requests.exceptions.Timeout as e:
            return {'errMsg': 'Timeout Error!'}, 500
        except requests.exceptions.TooManyRedirects as e:
            return {'errMsg': str(e)}, 500
        except requests.exceptions.RequestException as e:
            return {'errMsg': str(e)}, 500

        size=len(dataOrd)
        i=0
        while not found and i < size:
            if dataOrd[i]['statoCod']['value'] == 'A':
                course['cdsId']=dataCrs['cdsId']
                course['cdsCod']=dataCrs['cdsCod']
                course['cdsDes']=dataCrs['cdsDes']
                course['cfu']=dataOrd[i]['valoreMin']
                course['duration']=dataOrd[i]['durataAnni']
                found = True
            i+=1

        courseList.append(course)
    return courseList

def getTeachers(teachings):
    teachers={}
    teachersAct={}

    for t in teachings:
        try:
            response=requests.request('GET', url+'logistica-service-v1/logistica/'+str(t['adLogId'])+'/udLogConDettagli/', headers=getHeaders(), timeout=60)
            data=response.json()
            adLogId=str(t['adLogId'])
            size = len(data)
            for i in range(0, size, 1):
                for cd in data[i]['CaricoDocenti']:
                    badge=cd['docenteMatricola']
                    nameTch=cd['docenteNome']
                    surnameTch=cd['docenteCognome']
                    if badge not in teachers:
                        teachers[badge]={'name':nameTch, 'surname':surnameTch}
                    if adLogId not in teachersAct:
                        teachersAct[adLogId]=[badge]
                    else:
                        if badge not in teachersAct[adLogId]:
                            teachersAct[adLogId].append(badge)
        except requests.exceptions.Timeout as e:
            return {'errMsg': 'Timeout Error!'}, 500
        except requests.exceptions.TooManyRedirects as e:
            return {'errMsg': str(e)}, 500
        except requests.exceptions.RequestException as e:
            return {'errMsg': str(e)}, 500

    return teachers, teachersAct

def getAllData(academicYear,courses):
    coursesInfo=getCoursesInfo(courses)
    teachings=getTeachingOfCourse(academicYear,courses)
    teachers, teachersAct=getTeachers(teachings)

    flash(coursesInfo)
    flash(teachings)
    flash(teachers)
    flash(teachersAct)

def import_data():
    return 0


