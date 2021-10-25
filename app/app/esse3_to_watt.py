from flask import flash, render_template, redirect, url_for, request, g, session
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError
from .import db
from .util import getColori
from .models import AnnoAccademico, CorsoDiStudio, AttivitaDidattica, Docente, Offerta, Modulo, NumerositaAnniCorso

import requests, base64
from .util import getAttributiLDap

url="https://uniparthenope.esse3.cineca.it/e3rest/api/"

def getAuthToken():

    token, role=getAttributiLDap(g.user.username)

    headers={
        "Content-Type": "application/json",
        "Authorization": "Basic " + token
    }

    try:
        response=requests.request("GET", url + "login", headers=headers, timeout=60)
        authTokenString=response.json()["authToken"]

        sample_string_bytes=authTokenString.encode("ascii")
        b64_bytes=base64.b64encode(sample_string_bytes)
        b64_token=b64_bytes.decode("ascii")

        return b64_token

    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500

def getHeaders():
    try:
        token=session["token"]
    except:
        session["token"]=getAuthToken()
    return {
        "Content-Type": "application/json",
        "Authorization": "Basic " + session["token"]
    }

# Restituisce una lista di anni accademici per i quali è disponibile un"offerta in ESSE3
# Esempio 2020 stands for 2020-21.
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
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500

# Returns all courses on offer for the selected academic year.
def getCorsiInOfferta(annoAccademico):
    try:
        response=requests.request("GET", url+"offerta-service-v1/offerte?aaOffId="+ str(annoAccademico), headers=getHeaders(), timeout=60)
        data=response.json()

        size=len(data)
        corsi=[]
        for i in range(0, size, 1):
            corsi.append({"idCorso":data[i]["cdsOffId"],
                          "codCorso":data[i]["cdsCod"],
                          "desCorso":data[i]["cdsDes"]})
        return sorted(corsi, key=lambda k: (k["codCorso"]))
    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500


# Restituisce le regole di scelta relative ad un dato corso di studio
def getRegSchema(cdsId):
    try:
        schemeSet=[]
        response=requests.request("GET", url+"regsce-service-v1/regsce?cdsId="+str(cdsId), headers=getHeaders(), timeout=60)
        dataRegSce=response.json()

        sizeDataRegSce=len(dataRegSce)
        if sizeDataRegSce > 0:
            for i in range(0, sizeDataRegSce, 1):
                try:
                    response=requests.request("GET",url+"/regsce-service-v1/regsce/"+str(dataRegSce[i]["regsceId"])+"/schemi", headers=getHeaders(), timeout=60)
                    dataScheme=response.json()
                    sizeDataScheme = len(dataScheme)
                    for s in range(0, sizeDataScheme, 1):
                        try:
                            #if len(dataScheme) > 0:
                            #and dataScheme[0]["statutarioFlg"]==1:
                            schemeSet.append({"regSceId": dataRegSce[i]["regsceId"], "schemeId": dataScheme[s]["schemaId"]})
                        except:
                            None
                except:
                    None
        else:
            flash("regSceId could not be retrieved!","danger")
        return schemeSet
    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500

# Restituisce lo schema di piano associato alle regole inerenti al dato corso di studio
def getSchema(regSchema):
    try:
        schema={}
        size=len(regSchema)
        if size>0:
            for i in range(0, size, 1):
                response=requests.request("GET", url+"regsce-service-v1/regsce/"+str(regSchema[i]["regSceId"])+"/schemi/"+str(regSchema[i]["schemeId"]), headers=getHeaders(), timeout=60)
                data=response.json()
            try:
                sizeReg=len(data["regoleDiScelta"])
                for r in range(0, sizeReg, 1):
                    sizeBlk=len(data["regoleDiScelta"][r]["blocchi"])
                    for b in range(0, sizeBlk, 1):
                        sizeAct=len(data["regoleDiScelta"][r]["blocchi"][b]["attivita"])
                        for a in range(0, sizeAct, 1):
                            schema[data["regoleDiScelta"][r]["blocchi"][b]["attivita"][a]["chiaveADContestualizzata"]["adId"]]=\
                                {"annoDiCorso": data["regoleDiScelta"][r]["annoCorso"],
                                 "cfu": data["regoleDiScelta"][r]["blocchi"][b]["attivita"][a]["peso"]}
            except:
                None
        return schema
    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500

# Restituisce le attività didattiche dei corsi nell"ambito dell"offerta formativa selezionata
def getAttivitaDidattiche(annoAccademico, corsi, semestre, flgImportaADObbligatorie, flgImportaDatiIncompleti):
    attivitaDidattiche=[]
    try:
        for cdsId in corsi:
            schema=getSchema(getRegSchema(cdsId))
            response=requests.request("GET", url+"offerta-service-v1/offerte/"+str(annoAccademico)+"/"+str(cdsId)+"/attivita", headers=getHeaders(), timeout=60)
            dataOff=response.json()
            sizeDataOff=len(dataOff)
            for i in range(0, sizeDataOff, 1):
                try:
                    if flgImportaADObbligatorie is None or (flgImportaADObbligatorie=="1" and dataOff[i]["tipoInsCod"]=="OBB") :
                        ad_id=dataOff[i]["chiaveAdContestualizzata"]["adId"]
                        if dataOff[i]["nonErogabileOdFlg"]==0:
                            response = requests.request("GET", url+"logistica-service-v1/logistica?adId="+str(ad_id), headers=getHeaders(), timeout=60)
                            maxRow = max(response.json(), key=lambda x: x["chiaveADFisica"]["aaOffId"])
                            try:
                                adLogId=maxRow["chiavePartizione"]["adLogId"]
                                if maxRow["chiavePartizione"]["partCod"] in ["S2","Q2"]:
                                    semestreAttivita=2
                                else:
                                    semestreAttivita=1
                                try:
                                    annoCorso=schema[dataOff[i]["chiaveAdContestualizzata"]["adId"]]["annoDiCorso"]
                                except:
                                    annoCorso=-1
                                try:
                                    cfu=schema[dataOff[i]["chiaveAdContestualizzata"]["adId"]]["cfu"]
                                except:
                                    cfu=-1
                                if annoCorso>0 or flgImportaDatiIncompleti=="1":
                                    if semestreAttivita==int(semestre):
                                        ad=list(filter(lambda adc: adc["cdsId"]==maxRow["chiaveADFisica"]["cdsId"] and adc["adId"]==dataOff[i]["chiaveAdContestualizzata"]["adId"], attivitaDidattiche))
                                        if len(ad)==0:
                                            attivitaDidattiche.append({"cdsId": maxRow["chiaveADFisica"]["cdsId"],
                                                         "adId": dataOff[i]["chiaveAdContestualizzata"]["adId"],
                                                         "adCod": dataOff[i]["chiaveAdContestualizzata"]["adCod"],
                                                         "adDes": dataOff[i]["chiaveAdContestualizzata"]["adDes"],
                                                         "adLogId": str(adLogId),
                                                         "semestre": str(semestreAttivita),
                                                         "tipo": dataOff[i]["tipoInsCod"],
                                                         "annoCorso": annoCorso,
                                                         "cfu": cfu
                                                        })
                            except:
                                None
                except:
                    None
    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500
    return attivitaDidattiche

# Returns the information of the selected courses to be loaded into the database.
def getDatiCorsi(corsi):
    try:
        listaCorsi=[]

        for cdsId in corsi:
            corso={}
            found=False
            response=requests.request("GET", url+"struttura-service-v1/corsi/"+str(cdsId), headers=getHeaders(), timeout=60)
            dataCrs=response.json()
            response=requests.request("GET", url+"struttura-service-v1/corsi/"+str(cdsId)+"/ordinamenti", headers=getHeaders(), timeout=60)
            dataOrd=response.json()

            size=len(dataOrd)
            i=0
            while not found and i < size:
                if dataOrd[i]["statoCod"]["value"]=="A":
                    corso["cdsId"]=dataCrs["cdsId"]
                    corso["cdsCod"]=dataCrs["cdsCod"]
                    corso["cdsDes"]=dataCrs["cdsDes"]
                    corso["cfu"]=dataOrd[i]["valoreMin"]
                    corso["durataLegale"]=dataOrd[i]["durataAnni"]
                    found=True
                i+=1
            listaCorsi.append(corso)
        return listaCorsi

    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500

def getDocenti(attivitaDidattiche):
    try:
        docenti={}
        docentiPerAttivita={}

        for t in attivitaDidattiche:
            response=requests.request("GET", url+"logistica-service-v1/logistica/"+str(t["adLogId"])+"/udLogConDettagli/", headers=getHeaders(), timeout=60)
            data=response.json()

            adLogId=str(t["adLogId"])
            size=len(data)
            for i in range(0, size, 1):
                try:
                    carico=data[i]["CaricoDocenti"]
                    for cd in carico:
                        matricola=cd["docenteMatricola"]
                        nomeDocente=cd["docenteNome"]
                        cognomeDocente=cd["docenteCognome"]
                        if matricola not in docenti:
                            docenti[matricola]={"nome": nomeDocente, "cognome": cognomeDocente}
                        if adLogId not in docentiPerAttivita:
                            try:
                                carico=cd["frazioneCarico"]
                            except:
                                carico=0
                            if carico>=50:
                                docentiPerAttivita[adLogId]=[{"matricola": matricola, "titolare": "SI"}]
                            else:
                                docentiPerAttivita[adLogId]=[{"matricola": matricola, "titolare": "NO"}]
                        else:
                            if matricola not in docentiPerAttivita[adLogId]:
                                if carico>=50:
                                    docentiPerAttivita[adLogId].append({"matricola": matricola, "titolare":"SI"})
                                else:
                                    docentiPerAttivita[adLogId].append({"matricola": matricola, "titolare": "NO"})
                except:
                    None
        return docenti, docentiPerAttivita

    except requests.exceptions.Timeout as e:
        return {"errMsg": "Timeout Error!"}, 500
    except requests.exceptions.TooManyRedirects as e:
        return {"errMsg": str(e)}, 500
    except requests.exceptions.RequestException as e:
        return {"errMsg": str(e)}, 500

def importDatiEsse3(annoAccademico,corsiDiStudio,semestre,flgSovrDatiCorsi,flgSovrDatiAD,flgSovrDatiDocenti,flgSovrDatiOfferta,flgImportaADObbligatorie,flgImportaDatiIncompleti,flgGenModuli):
    global idAnnoAccademico
    global found;

    colori=getColori()
    corsi=getDatiCorsi(corsiDiStudio)
    attivitaDidattiche=getAttivitaDidattiche(annoAccademico,corsiDiStudio,semestre,flgImportaADObbligatorie,flgImportaDatiIncompleti)
    docenti, docentiPerAttivita=getDocenti(attivitaDidattiche)
    numerositaAnniCorso=db.session.query(NumerositaAnniCorso.id, NumerositaAnniCorso.codice_corso, NumerositaAnniCorso.anno_di_corso, NumerositaAnniCorso.numerosita).all()

    # Inserimento dell"anno accademico selezionato in DB se già non esiste
    aa=db.session.query(AnnoAccademico).filter(AnnoAccademico.anno==int(annoAccademico)).first()
    if aa is None:
        row=AnnoAccademico(anno=annoAccademico, anno_esteso=annoAccademico+"-"+str(int(annoAccademico)+1))
        db.session.add(row)
        db.session.flush()
        idAnnoAccademico=row.id
    else:
        idAnnoAccademico=aa.id
    db.session.commit()

    # Inserimento dei dati dei corsi di studio selezionati in DB
    size=len(corsi)
    for c in range(0, size, 1):
        corso=db.session.query(CorsoDiStudio).filter(CorsoDiStudio.codice==corsi[c]["cdsCod"]).first()
        row=CorsoDiStudio(codice=corsi[c]["cdsCod"], descrizione=corsi[c]["cdsDes"], cfu=corsi[c]["cfu"], durata_legale=corsi[c]["durataLegale"])
        if corso is None:
            db.session.add(row)
            db.session.flush()
            corsi[c]["id"]=row.id
        else:
            if flgSovrDatiCorsi is None:
                db.session.query(CorsoDiStudio).filter(CorsoDiStudio.id==corso.id).update\
                    (dict(codice=corsi[c]["cdsCod"], descrizione=corsi[c]["cdsDes"], cfu=corsi[c]["cfu"], durata_legale=corsi[c]["durataLegale"]))
                db.session.flush()
            corsi[c]["id"]=corso.id
    db.session.commit()

    # Inserimento dei dati delle attività didattiche relative ai corsi di studio selezionati in DB
    attivitaDidattiche=sorted(attivitaDidattiche, key=lambda k: (k["cdsId"], k["annoCorso"]))
    size=len(attivitaDidattiche)

    clr=1
    for c in range(0, size, 1):
        ad=db.session.query(AttivitaDidattica).filter(AttivitaDidattica.codice==attivitaDidattiche[c]["adCod"]).first()
        row=AttivitaDidattica(codice=attivitaDidattiche[c]["adCod"], descrizione=attivitaDidattiche[c]["adDes"],
                                cfu=attivitaDidattiche[c]["cfu"], colore=colori[clr])
        if ad is None:
            db.session.add(row)
            db.session.flush()
            attivitaDidattiche[c]["id"]=row.id
        else:
            if flgSovrDatiAD is None:
                db.session.query(AttivitaDidattica).filter(AttivitaDidattica.id==ad.id).update\
                    (dict(codice=attivitaDidattiche[c]["adCod"], descrizione=attivitaDidattiche[c]["adDes"],
                        cfu=attivitaDidattiche[c]["cfu"], colore=colori[clr]))
                db.session.flush()
            attivitaDidattiche[c]["id"]=ad.id
        if clr==10:
            clr=1
        else:
            clr+=1
    db.session.commit()

    # Inserimento dei docenti nel db
    for d in docenti:
        docente=db.session.query(Docente).filter(Docente.matricola==d).first()
        row=Docente(codice_fiscale=d, matricola=d, cognome=docenti[d]["cognome"], nome=docenti[d]["nome"])
        if docente is None:
            db.session.add(row)
            db.session.flush()
            docenti[d]["id"]=row.id
        else:
            if flgSovrDatiDocenti is None:
                db.session.query(Docente).filter(Docente.id==docente.id).update\
                    (dict(codice_fiscale=d, matricola=d, cognome=docenti[d]["cognome"], nome=docenti[d]["nome"]))
                db.session.flush()
            docenti[d]["id"]=docente.id
    db.session.commit()

    sizeCorsi=len(corsi)
    for c in range(0, sizeCorsi, 1):
        corsoPresente = db.session.query(Offerta).filter(Offerta.anno_accademico_id==int(idAnnoAccademico)). \
                                                  filter(Offerta.semestre == semestre). \
                                                  filter(Offerta.corso_di_studio_id==corsi[c]["id"]).first()
        if corsoPresente is None or flgSovrDatiOfferta=="1":
            # Cancellazione delle offerte e dei moduli collegati relativi ai corsi e all"A.A. selezionato
            off_id = db.session.query(Offerta.id).\
                filter(Offerta.anno_accademico_id == int(idAnnoAccademico)).\
                filter(Offerta.semestre == semestre).\
                filter(Offerta.corso_di_studio_id == corsi[c]["id"]).subquery()
            db.session.query(Modulo).filter(Modulo.offerta_id.in_(off_id)).delete(synchronize_session="fetch")
            db.session.query(Offerta).filter(Offerta.anno_accademico_id==int(idAnnoAccademico)). \
                                      filter(Offerta.semestre == semestre). \
                                      filter(Offerta.corso_di_studio_id==corsi[c]["id"]).delete()
            db.session.commit()

            attivitaDidatticheCorso=attivitaDidattiche
            #Inserimento delle offerte dei corsi selezionati
            sizeAD=len(attivitaDidatticheCorso)
            for a in range(0, sizeAD, 1):
                try:
                    doc=list(filter(lambda dpa: dpa["titolare"]=="SI", docentiPerAttivita[attivitaDidatticheCorso[a]["adLogId"]]))[0]["matricola"]
                    found=True
                except:
                    try:
                        doc=list(filter(lambda dpa: dpa["titolare"]=="NO", docentiPerAttivita[attivitaDidatticheCorso[a]["adLogId"]]))[0]["matricola"]
                        found=True
                    except:
                        found=False
                if (found==True):
                    try:
                        numAnnoCorso=list(filter(lambda nac: nac[1]==corsi[c]["cdsCod"] and nac[2]==attivitaDidatticheCorso[a]["annoCorso"], numerositaAnniCorso))[0][3]
                    except:
                        numAnnoCorso=0
                    row=Offerta(anno_accademico_id=idAnnoAccademico, corso_di_studio_id=corsi[c]["id"], attivita_didattica_id=attivitaDidatticheCorso[a]["id"],
                                docente_id=docenti[doc]["id"], anno_di_corso=attivitaDidatticheCorso[a]["annoCorso"], semestre=attivitaDidatticheCorso[a]["semestre"],
                                max_studenti=numAnnoCorso)
                    db.session.add(row)
                    db.session.flush()
                    idOfferta=row.id

                    # Inserimento dei moduli in base alla politica scelta - Un modulo per AD oppure un modulo per ogni docente legato alla logistica dell"AD
                    if flgGenModuli=="1":
                        row=Modulo(codice="MOD-1", descrizione="MOD-1", offerta_id=idOfferta, docente_id=docenti[doc]["id"],
                                   tipo_aula="N", numero_sessioni=2, durata_sessioni=2, max_studenti=0)
                        db.session.add(row)
                        db.session.flush()
                    else:
                        docAD=docentiPerAttivita[attivitaDidatticheCorso[a]["adLogId"]]
                        sizeDocAD=len(docAD)
                        for r in range(0, sizeDocAD, 1):
                            row=Modulo(codice="MOD-"+str(r+1)+"/"+str(sizeDocAD), descrizione="MOD"+str(r+1)+str(sizeDocAD), offerta_id=idOfferta, docente_id=docenti[docAD[r]["matricola"]]["id"],
                                         tipo_aula="N", numero_sessioni=2, durata_sessioni=2, max_studenti=0)
                            db.session.add(row)
                            db.session.flush()
            flash("L'offerta per il corso selezionato è stata inserita/aggiornata!", "success")
        else:
            flash("L'offerta per il corso selezionato è già presente in DB e, come richiesto, non è stata aggiornata!", "warning")

        db.session.commit()