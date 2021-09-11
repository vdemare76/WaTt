from flask import flash, render_template, redirect, url_for, request, g, session
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError
from .import db
from .models import AnnoAccademico, CorsoDiStudio

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
def getAnniAccademici():
    try:
        response=requests.request("GET", url+"offerta-service-v1/offerte", headers=getHeaders(), timeout=60)
        data=response.json()
        size=len(data)
        annoAccademiciDistinti=[]
        for i in range(0, size, 1):
            if (data[i]["aaOffId"] not in annoAccademiciDistinti and data[i]["aaOffId"]>=2017):
                annoAccademiciDistinti.append(data[i]["aaOffId"])
        annoAccademiciDistinti.sort()
        return annoAccademiciDistinti
    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

''' Returns all courses on offer for the selected academic year. '''
def getCorsiInOfferta(annoAccademico):
    try:
        response=requests.request("GET", url+"offerta-service-v1/offerte?aaOffId="+ str(annoAccademico), headers=getHeaders(), timeout=60)
        data=response.json()

        size=len(data)
        corsi=[]
        for i in range(0, size, 1):
            corsi.append({'idCorso':data[i]["cdsOffId"],
                          'codCorso':data[i]["cdsCod"],
                          'desCorso':data[i]["cdsDes"]})
        return corsi
    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500


''' Restituisce le regole di scelta relative ad un dato corso di studio '''
def getRegSchema(cdsId):
    try:
        schemeSet = []
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

''' Restituisce lo schema di piano associato alle regole inerenti al dato corso di studio '''
def getSchema(regSchema):
    try:
        schema={}
        size=len(regSchema)
        if size>0:
            for i in range(0, size, 1):
                response = requests.request('GET', url+'regsce-service-v1/regsce/'+str(regSchema[i]['regSceId'])+'/schemi/'+str(regSchema[i]['schemeId']), headers=getHeaders(), timeout=60)
                data=response.json()

            sizeReg=len(data['regoleDiScelta'])
            for r in range(0, sizeReg, 1):
                sizeBlk=len(data['regoleDiScelta'][r]['blocchi'])
                for b in range(0, sizeBlk, 1):
                    sizeAct=len(data['regoleDiScelta'][r]['blocchi'][b]['attivita'])
                    for a in range(0, sizeAct, 1):
                        schema[data['regoleDiScelta'][r]['blocchi'][b]['attivita'][a]['chiaveADContestualizzata']['adId']] = \
                            {'yearOfCourse': data['regoleDiScelta'][r]['annoCorso'],
                             'cfu': data['regoleDiScelta'][r]['blocchi'][b]['attivita'][a]['peso']}
        return schema
    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

''' Restituisce le attività didattiche dei corsi nell'ambito dell'offerta formativa selezionata '''
def getAttivitaDidattiche(annoAccademico, corsi):
    attivitaDidattiche=[]
    try:
        for cdsId in corsi:
            schema = getSchema(getRegSchema(cdsId))
            response = requests.request('GET', url+'offerta-service-v1/offerte/'+str(annoAccademico)+'/'+str(cdsId)+'/attivita', headers=getHeaders(), timeout=60)
            dataOff = response.json()
            size = len(dataOff)
            for i in range(0, size, 1):
                ad_id = dataOff[i]['chiaveAdContestualizzata']['adId']
                if dataOff[i]['nonErogabileOdFlg']==0:
                    response = requests.request('GET', url+'logistica-service-v1/logistica?aaOffId='+str(annoAccademico)+'&adId='+str(ad_id), headers=getHeaders(), timeout=60)
                    dataLog = response.json()

                if len(dataLog) > 0:
                    adLogId = dataLog[0]['chiavePartizione']['adLogId']
                    if dataLog[0]['chiavePartizione']['partCod'] in ['S2','Q2']:
                        semestre=2
                    else:
                        semestre=1
                    try:
                        annoCorso=schema[dataOff[i]['chiaveAdContestualizzata']['adId']]['yearOfCourse']
                        cfu=schema[dataOff[i]['chiaveAdContestualizzata']['adId']]['cfu']
                    except:
                        annoCorso=-1
                        cfu=-1
                    attivitaDidattiche.append({'cdsId': dataLog[0]['chiaveADFisica']['cdsId'],
                                 'adId': dataOff[i]['chiaveAdContestualizzata']['adId'],
                                 'adCod': dataOff[i]['chiaveAdContestualizzata']['adCod'],
                                 'adDes': dataOff[i]['chiaveAdContestualizzata']['adDes'],
                                 'adLogId': str(adLogId),
                                 'semestre': str(semestre),
                                 'tipo': dataOff[i]['tipoInsCod'],
                                 'annoCorso': annoCorso,
                                 'cfu': cfu
                                })

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500
    getDocenti(attivitaDidattiche)
    return attivitaDidattiche

''' Returns the information of the selected courses to be loaded into the database. '''
def getDatiCorsi(corsi):
    try:
        listaCorsi=[]

        for cdsId in corsi:
            corso = {}
            found=False
            response=requests.request('GET', url+'struttura-service-v1/corsi/'+str(cdsId), headers=getHeaders(), timeout=60)
            dataCrs=response.json()
            response=requests.request('GET', url+'struttura-service-v1/corsi/'+str(cdsId)+'/ordinamenti', headers=getHeaders(), timeout=60)
            dataOrd=response.json()

            size=len(dataOrd)
            i=0
            while not found and i < size:
                if dataOrd[i]['statoCod']['value'] == 'A':
                    corso['cdsId']=dataCrs['cdsId']
                    corso['cdsCod']=dataCrs['cdsCod']
                    corso['cdsDes']=dataCrs['cdsDes']
                    corso['cfu']=dataOrd[i]['valoreMin']
                    corso['durataLegale']=dataOrd[i]['durataAnni']
                    found = True
                i+=1
            listaCorsi.append(corso)
        return listaCorsi

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

def getDocenti(attivitaDidattiche):
    try:
        docenti={}
        docentiPerAttivita={}

        for t in attivitaDidattiche:
                response=requests.request('GET', url+'logistica-service-v1/logistica/'+str(t['adLogId'])+'/udLogConDettagli/', headers=getHeaders(), timeout=60)
                data=response.json()

        adLogId = str(t['adLogId'])
        size = len(data)
        for i in range(0, size, 1):
            for cd in data[i]['CaricoDocenti']:
                matricola = cd['docenteMatricola']
                nomeDocente = cd['docenteNome']
                cognomeDocente = cd['docenteCognome']
                if matricola not in docenti:
                    docenti[matricola] = {'name': nomeDocente, 'surname': cognomeDocente}
                if adLogId not in docentiPerAttivita:
                    docentiPerAttivita[adLogId] = [matricola]
                else:
                    if matricola not in docentiPerAttivita[adLogId]:
                        docentiPerAttivita[adLogId].append(matricola)

        return docenti, docentiPerAttivita

    except requests.exceptions.Timeout as e:
        return {'errMsg': 'Timeout Error!'}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {'errMsg': str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {'errMsg': str(e)}, 500

def importDatiEsse3(annoAccademico,corsi,flgSovrDatiCorsi,flgSovrDatiAD,flgSovrDatiDocenti,flgSovrDatiOfferta):
    datiCorsi=getDatiCorsi(corsi)
    attivitaDidattiche=getAttivitaDidattiche(annoAccademico,corsi)
    docenti, docentiPerAttivita=getDocenti(attivitaDidattiche)

    ''' Inserimento dell'anno accademico selezionato in DB se già non esiste '''
    year=db.session.query(AnnoAccademico).filter(AnnoAccademico.anno==int(annoAccademico)).first()
    if year is None:
        row = AnnoAccademico(anno=annoAccademico, anno_esteso=annoAccademico+'/'+str(int(annoAccademico)+1))
        db.session.add(row)
        db.session.flush()
        idAnno=row.id
    db.session.commit()

    ''' Inserimento dei dati dei corsi di studio selezionati in DB '''
    size = len(datiCorsi)
    for c in range(0, size, 1):
        global idCorso
        corso=db.session.query(CorsoDiStudio).filter(CorsoDiStudio.codice==datiCorsi[c]['cdsCod']).first()
        row = CorsoDiStudio(codice=datiCorsi[c]['cdsCod'], descrizione=datiCorsi[c]['cdsDes'], cfu=datiCorsi[c]['cfu'], durata_legale=datiCorsi[c]['durataLegale'])
        if corso is None:
            db.session.add(row)
            db.session.flush()
            idCorso=row.id
        else:
            if flgSovrDatiCorsi is None:
                idCorso=corso.id
            else:
                db.session.query(CorsoDiStudio).filter(CorsoDiStudio.codice==datiCorsi[c]['cdsCod']).delete()
                db.session.add(row)
                db.session.flush()
                idCorso = row.id
        datiCorsi[c]['id']=idCorso
    db.session.commit()




