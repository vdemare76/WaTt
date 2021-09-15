from flask import flash, render_template, redirect, url_for, request, g, session
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError
from .import db
from .util import getColori
from .models import AnnoAccademico, CorsoDiStudio, AttivitaDidattica, Docente

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
def getAttivitaDidattiche(annoAccademico, corsi, semestre):
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
                            semestreAttivita=2
                        else:
                            semestreAttivita=1
                        try:
                            annoCorso=schema[dataOff[i]['chiaveAdContestualizzata']['adId']]['yearOfCourse']
                            cfu=schema[dataOff[i]['chiaveAdContestualizzata']['adId']]['cfu']
                        except:
                            annoCorso=-1
                            cfu=-1
                        if semestreAttivita==int(semestre[0]):
                            attivitaDidattiche.append({'cdsId': dataLog[0]['chiaveADFisica']['cdsId'],
                                         'adId': dataOff[i]['chiaveAdContestualizzata']['adId'],
                                         'adCod': dataOff[i]['chiaveAdContestualizzata']['adCod'],
                                         'adDes': dataOff[i]['chiaveAdContestualizzata']['adDes'],
                                         'adLogId': str(adLogId),
                                         'semestre': str(semestreAttivita),
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
                        docenti[matricola] = {'nome': nomeDocente, 'cognome': cognomeDocente}
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

def myFunc(e):
    return e['cdsId','annoCorso']

def importDatiEsse3(annoAccademico,corsiDiStudio,semestre,flgSovrDatiCorsi,flgSovrDatiAD,flgSovrDatiDocenti,flgSovrDatiOfferta):
    global idAnnoAccademico
    from operator import itemgetter

    colori=getColori()
    corsi=getDatiCorsi(corsiDiStudio)
    attivitaDidattiche=getAttivitaDidattiche(annoAccademico,corsiDiStudio,semestre)
    docenti, docentiPerAttivita=getDocenti(attivitaDidattiche)

    ''' Inserimento dell'anno accademico selezionato in DB se già non esiste '''
    annoAccademico=db.session.query(AnnoAccademico).filter(AnnoAccademico.anno==int(annoAccademico)).first()
    if annoAccademico is None:
        row = AnnoAccademico(anno=annoAccademico, anno_esteso=annoAccademico+'/'+str(int(annoAccademico)+1))
        db.session.add(row)
        db.session.flush()
        idAnnoAccademico=row.id
    else:
        idAnnoAccademico=annoAccademico.id
    db.session.commit()

    ''' Inserimento dei dati dei corsi di studio selezionati in DB '''
    size = len(corsi)
    for c in range(0, size, 1):
        global idCorso
        corso=db.session.query(CorsoDiStudio).filter(CorsoDiStudio.codice==corsi[c]['cdsCod']).first()
        row = CorsoDiStudio(codice=corsi[c]['cdsCod'], descrizione=corsi[c]['cdsDes'], cfu=corsi[c]['cfu'], durata_legale=corsi[c]['durataLegale'])
        if corso is None:
            db.session.add(row)
            db.session.flush()
            idCorso=row.id
        else:
            if flgSovrDatiCorsi is None:
                idCorso=corso.id
            else:
                db.session.query(CorsoDiStudio).filter(CorsoDiStudio.codice==corsi[c]['cdsCod']).delete()
                db.session.add(row)
                db.session.flush()
                idCorso = row.id
        corsi[c]['id']=idCorso
    db.session.commit()

    ''' Inserimento dei dati delle attività didattiche relative ai corsi di studio selezionati in DB '''
    attivitaDidattiche = sorted(attivitaDidattiche, key=lambda k: (k['cdsId'], k['annoCorso']))
    size = len(attivitaDidattiche)

    clr=1
    for c in range(0, size, 1):
        global idAD
        ad=db.session.query(AttivitaDidattica).filter(AttivitaDidattica.codice==attivitaDidattiche[c]['adCod']).first()
        row = AttivitaDidattica(codice=attivitaDidattiche[c]['adCod'], descrizione=attivitaDidattiche[c]['adDes'], cfu=attivitaDidattiche[c]['cfu'], colore=colori[clr])
        if ad is None:
            db.session.add(row)
            db.session.flush()
            idAD=row.id
        else:
            if flgSovrDatiAD is None:
                idAD=ad.id
            else:
                db.session.query(AttivitaDidattica).filter(AttivitaDidattica.codice==attivitaDidattiche[c]['adCod']).delete()
                db.session.add(row)
                db.session.flush()
                idAD = row.id
        if clr==10:
            clr=1
        else:
            clr+=1
        attivitaDidattiche[c]['id']=idAD
    db.session.commit()

    ''' Inserimento dei docenti nel db '''
    for d in docenti:
        global idDocente
        docente=db.session.query(Docente).filter(Docente.matricola==d).first()
        row = Docente(codice_fiscale=d, matricola=d, cognome=docenti[d]['cognome'], nome=docenti[d]['nome'])
        if docente is None:
            db.session.add(row)
            db.session.flush()
            idDocente=row.id
        else:
            if flgSovrDatiDocenti is None:
                idDocente=docente.id
            else:
                db.session.query(Docente).filter(Docente.matricola==d).delete()
                db.session.add(row)
                db.session.flush()
                idDocente = row.id
        docenti[d]['id']=idDocente
    db.session.commit()

    size = len(corsi)
    for c in range(0, size, 1):
        db.session.query(Offerta).filter(Offerta.anno_accademico_id==idAnnoAccademico).delete()
    db.session.commit()