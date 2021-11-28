from .models import AnnoAccademico, CorsoDiStudio, AttivitaDidattica, \
    Docente, Aula, Offerta, LogisticaDocente, Modulo, Giorno, Slot, \
    OrarioTestata, OrarioDettaglio, StatoOrario, NumerositaAnniCorso, Chiusura
from .import db
from flask import flash, session
from sqlalchemy.exc import SQLAlchemyError
from .solver_models import ModuloTt, AulaTt, CorsoDiStudioTt, SlotTt, GiornoTt

from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError, LDAPSocketOpenError
import config
from datetime import timedelta

colori={
    1:"#990000",
    2:"#FFCC00",
    3:"#009900",
    4:"#0066FF",
    5:"#800000",
    6:"#FF6666",
    7:"#999999",
    8:"#99FF99",
    9:"#660099",
    10:"#9999FF",
    11: "#FFCC99",
    12: "#CCFFCC",
    13: "#CCCCFF",
    14: "#FFCCFF"
}

def __svuotaTabelle():
    db.session.query(Chiusura).delete()
    db.session.query(OrarioDettaglio).delete()
    db.session.query(OrarioTestata).delete()
    db.session.query(LogisticaDocente).delete()
    db.session.query(Modulo).delete()
    db.session.query(Offerta).delete()
    db.session.query(CorsoDiStudio).delete()
    db.session.query(AttivitaDidattica).delete()
    db.session.query(NumerositaAnniCorso).delete()
    db.session.query(Docente).delete()
    db.session.query(Giorno).delete()
    db.session.query(AnnoAccademico).delete()
    db.session.query(Slot).delete()
    db.session.query(Aula).delete()
       
    db.session.execute("ALTER TABLE modulo AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE offerta AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE corso_di_studio AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE attivita_didattica AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE numerosita_anni_corso AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE docente AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE giorno AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE anno_accademico AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE slot AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE aula AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE logistica_docente AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE orario_testata AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE orario_dettaglio AUTO_INCREMENT=1")
    db.session.execute("ALTER TABLE chiusura AUTO_INCREMENT=1")
    db.session.commit()


def __impostaDatiBase():
    giorni=[]
    slot=[]
    aule=[]
    numerosita=[]

    giorni_i=["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    giorni.extend(giorni_i)

    slot_i=[
        ["09:00-10:00", 9],
        ["10:00-11:00", 10],
        ["11:00-12:00", 11],
        ["12:00-13:00", 12],
        ["14:00-15:00", 14],
        ["15:00-16:00", 15],
        ["16:00-17:00", 16],
        ["17:00-18:00", 17]
    ]
    slot.extend(slot_i)

    aule_i=[
        ["AN1", "Aula 1", 260, "N"],
        ["AN2", "Aula 2", 132, "N"],
        ["AN3", "Aula 3", 132, "N"],
        ["AN4", "Aula 4", 117, "N"],
        ["AN5", "Aula 5", 44, "N"],
        ["AN6", "Aula 6", 24, "N"],
        ["AN7", "Aula 7", 44, "N"],
        ["AN8", "Aula 8", 117, "N"],
        ["AN9", "Aula 9", 24, "N"],
        ["AN10", "Aula 10", 44, "N"],
        ["AN11", "Aula 11", 117, "N"],
        ["AN12", "Aula 12", 24, "N"],
        ["AN13", "Aula 13", 44, "N"],
        ["AN14", "Aula 14", 115, "N"],
        ["AN15", "Aula 15", 44, "N"],
        ["AN16", "Aula 16", 117, "N"],
        ["AN17", "Aula 17", 44, "N"],
        ["AN18", "Aula 18", 117, "N"],
        ["AL1", "Aula LAB1", 36, "L"],
        ["AL2", "Aula LAB2", 36, "L"],
        ["AL3", "Aula LAB3", 36, "L"],
        ["AL4", "Aula LAB4", 36, "L"]
    ]
    aule.extend(aule_i)

    numerosita_i=[
        ["0120", 1, 30],
        ["0120", 2, 15],
        ["0120", 3, 15],
        ["0121", 1, 40],
        ["0121", 2, 20],
        ["0121", 3, 15],
        ["0122", 1, 50],
        ["0122", 2, 30],
        ["0122", 3, 30],
        ["0123", 1, 60],
        ["0123", 2, 45],
        ["0123", 3, 25],
        ["0124", 1, 100],
        ["0124", 2, 70],
        ["0124", 3, 50],
        ["0125", 1, 40],
        ["0125", 2, 20],
        ["0125", 3, 15],
        ["0126", 1, 50],
        ["0126", 2, 30],
        ["0126", 3, 25]
    ]
    numerosita.extend(numerosita_i)

    return giorni, slot, aule, numerosita

def __impostaDati7Cds(tipoModuli):
    anni_accademici = []
    corsi_di_studio = []
    attivita_didattiche = []
    docenti = []
    offerta = []
    moduli = []

    giorni, slot, aule, numerosita = __impostaDatiBase()

    anni_accademici_i=[
        [2021,"2021-2022"]
    ]
    anni_accademici.extend(anni_accademici_i)

    corsi_di_studio_i=[
        ["0120", "INFORMATICA APPLICATA (MACHINE LEARNING E BIG DATA)", 120, 2],
        ["0124", "INFORMATICA", 180, 3],
        ["0123", "SCIENZE BIOLOGICHE", 180, 3],
        ["0122", "SCIENZE NAUTICHE, AERONAUTICHE E METEO-OCEANOGRAFICHE", 180, 3],
        ["0121", "SCIENZE E TECNOLOGIE DELLA NAVIGAZIONE", 120, 2],
        ["0125", "CONDUZIONE DEL MEZZO NAVALE", 180, 3],
        ["0126", "BIOLOGIA PER LA SOSTENIBILITA'", 120, 2]
    ]
    corsi_di_studio.extend(corsi_di_studio_i)

    attivita_didattiche_i=[
        ["A001018", "SCIENTIFIC COMPUTING", 12, "#FF0000"],
        ["A001019", "PHYSICS AND QUANTUM COMPUTING", 6, "#4169E1"],
        ["A001020", "MACHINE LEARNING", 12, "#228B22"],
        ["A001027", "COMPUTER GRAPHICS: ANIMATION AND SIMULATION", 6, "#FFD800"],
        ["A001022", "HIGH PERFORMANCE COMPUTING", 6, "#993300"],
        ["A001024", "INTERNET OF THINGS AND IOT LAB", 12, "#d4bf02"],
        ["A001025", "MULTIMODAL MACHINE LEARNING", 6, "#fa2d9a"],
        ["771", "MATEMATICA I", 12, "#FF0000"],
        ["ARC12", "ARCHITETTURA DEI CALCOLATORI E LABORATORIO DI ARCHITETTURA DEI CALCOLATORI CFU12", 12, "#4169E1"],
        ["PROGR12", "PROGRAMMAZIONE I E LABORATORIO DI PROGRAMMAZIONE I  CFU 12", 12, "#228B22"],
        ["ALGSTD12", "ALGORITMI E STRUTTURE DATI E LABORATORIO DI ALGORITMI E STRUTTURE DATI CFU 12", 12, "#FFD800"],
        ["INFO03", "ECONOMIA E ORGANIZZAZIONE AZIENDALE", 9, "#993300"],
        ["MATII9", "MATEMATICA II CFU 9", 9, "#d4bf02"],
        ["A001195", "INGEGNERIA DEL SOFTWARE E INTERAZIONE UOMO-MACCHINA", 9, "#fa2d9a"],
        ["PRGRIII9", "PROGRAMMAZIONE III E LABORATORIO DI PROGRAMMAZIONE III", 6, "#92b09e"],
        ["RCLRC9", "RETI DI CALCOLATORI E LABORATORIO DI RETI DI CALCOLATORI CFU 9", 9, "#7ec4ba"],
        ["0115021", "MATEMATICA E STATISTICA", 9, "#FF0000"],
        ["012301", "CHIMICA GENERALE ED INORGANICA CON LABORATORIO", 9, "#4169E1"],
        ["01230444", "BIOLOGIA E FISIOLOGIA VEGETALE CON LABORATORIO", 12, "#228B22"],
        ["01230445", "CITOLOGIA ED ISTOLOGIA CON LABORATORIO", 6, "#FFD800"],
        ["012305", "BIOCHIMICA CON LABORATORIO", 9, "#993300"],
        ["0115007", "ECOLOGIA", 9, "#d4bf02"],
        ["012340", "IGIENE", 9, "#fa2d9a"],
        ["01230004", "FISIOLOGIA GENERALE", 6, "#92b09e"],
        ["186", "GENETICA", 6, "#7ec4ba"],
        ["A000733", "INFORMATICA DI BASE E LABORATORIO", 6, "#FF0000"],
        ["ITL030", "TEORIA DEI SEGNALI", 9, "#4169E1"],
        ["A001004", "ANALISI MATEMATICA II", 9, "#228B22"],
        ["FISI26", "FISICA II CFU 6", 6, "#FFD800"],
        ["01200008", "APPLICAZIONI DI CALCOLO SCIENTIFICO E LAB. A.C.S.", 12, "#FF0000"],
        ["IT06", "RADAR", 6, "#4169E1"],
        ["CLIMA", "CLIMATOLOGIA", 6, "#228B22"],
        ["NAVSAT", "NAVIGAZIONE SATELLITARE", 6, "#FFD800"],
        ["TRASP", "TRASPORTO E DIFFUSIONE NELL'OCEANO E NELL'ATMOSFERA", 6, "#993300"],
        ["012105", "ECONOMIA ED ORGANIZZAZIONE AZIENDALE", 6, "#d4bf02"],
        ["A000984", "TENUTA DELLA GUARDIA E LABORATORIO", 6, "#4169E1"],
        ["526", "ANALISI MATEMATICA", 9, "#228B22"],
        ["A000982", "INGLESE TECNICO E LABORATORIO", 6, "#FFD800"],
        ["012109", "TECNOLOGIE DELLE COSTRUZIONI ED ALLESTIMENTO NAVALE", 6, "#993300"],
        ["A001367", "IGIENE DELL'AMBIENTE E DEL TERRITORIO", 6, "#FF0000"],
        ["A001368", "BIOCHIMICA APPLICATA", 6, "#4169E1"],
        ["A001369", "ECONOMIA DELL'AMBIENTE ED ECONOMIA CIRCOLARE", 6, "#228B22"],
        ["A001375", "ECOLOGIA SISTEMICA E VALUTAZIONE AMBIENTALE", 9, "#FFD800"],
        ["A001376", "ZOOLOGIA APPLICATA", 9, "#993300"]
    ]
    attivita_didattiche.extend(attivita_didattiche_i)

    docenti_i=[
        ["CF001903", "001903", "MARCELLINO", "LIVIA"],
        ["CF002347", "002347", "FERONE", "ALESSIO"],
        ["CF001854", "001854", "CAMASTRA", "FRANCESCO"],
        ["CF000292", "000292", "RIZZARDI", "MARIAROSARIA"],
        ["CF000296", "000296", "GIUNTA", "GIULIO"],
        ["CF000768", "000768", "ROTUNDI", "ALESSANDRA"],
        ["CF001969", "001969", "CIARAMELLA", "ANGELO"],
        ["CF001971", "001971", "STAIANO", "ANTONINO"],
        ["CF001713", "001713", "MONTELLA", "RAFFAELE"],
        ["CF001412", "001412", "METALLO", "CONCETTA"],
        ["CF002025", "002025", "VOLZONE", "BRUNO"],
        ["CF001708", "001708", "D'ONOFRIO", "LUIGI"],
        ["CF002006", "002006", "SALVI", "GIUSEPPE"],
        ["CF000716", "000716", "RUSSO", "GIOVANNI, FULVIO"],
        ["CF002602", "002602", "DI ONOFRIO", "VALERIA"],
        ["CF005922", "005922", "NAPOLITANO", "GAETANA"],
        ["CF002138", "002138", "DI DONATO", "PAOLA"],
        ["CF002318", "002318", "PASQUALE", "VINCENZO"],
        ["CF002159", "002159", "GALLETTI", "ARDELIO"],
        ["CF001954", "001954", "OLIVA", "ROMINA"],
        ["CF001528", "001528", "CASORIA", "PAOLO"],
        ["CF004015", "004015", "SIMONIELLO", "PALMA"],
        ["CF001871", "001871", "FERRAIOLI", "GIAMPAOLO"],
        ["CF001132", "001132", "PREZIOSO", "GIUSEPPINA"],
        ["CF000337", "000337", "ZAMBIANCHI", "ENRICO"],
        ["CF001141", "001141", "FUSCO", "GIANNETTA"],
        ["CF002844", "002844", "PISCOPO", "VINCENZO"],
        ["CF001711", "001711", "AMADORI", "ANNA LISA"],
        ["CF004663", "004663", "NISCO", "MARIA CRISTINA"],
        ["CF001909", "001909", "FRANZESE", "PIER PAOLO"],
        ["CF002651", "002651", "BUONOCORE", "ELVIRA"],
        ["CF002069", "002069", "SANDULLI", "ROBERTO"]
    ]
    docenti.extend(docenti_i)

    offerta_i=[
        [1, 1, 1, 4, 1, 1, 0],
        [1, 1, 2, 6, 1, 1, 0],
        [1, 1, 3, 3, 1, 1, 0],
        [1, 1, 5, 1, 2, 1, 0],
        [1, 1, 6, 2, 2, 1, 0],
        [1, 1, 7, 3, 2, 1, 0],
        [1, 2, 8, 4, 1, 1, 0],
        [1, 2, 9, 9, 1, 1, 0],
        [1, 2, 10, 12, 1, 1, 0],
        [1, 2, 11, 8, 2, 1, 0],
        [1, 2, 12, 10, 2, 1, 0],
        [1, 2, 13, 11, 2, 1, 0],
        [1, 3, 14, 14, 1, 1, 0],
        [1, 3, 15, 9, 2, 1, 0],
        [1, 3, 16, 13, 2, 1, 0],
        [1, 3, 17, 6, 2, 1, 0],
        [1, 4, 18, 20, 1, 1, 0],
        [1, 4, 19, 21, 1, 1, 0],
        [1, 4, 20, 22, 1, 1, 0],
        [1, 4, 21, 23, 1, 1, 0],
        [1, 4, 22, 18, 2, 1, 0],
        [1, 4, 23, 15, 3, 1, 0],
        [1, 4, 24, 16, 3, 1, 0],
        [1, 4, 25, 17, 3, 1, 0],
        [1, 4, 26, 19, 3, 1, 0],
        [1, 5, 27, 13, 1, 1, 0],
        [1, 5, 28, 14, 1, 1, 0],
        [1, 5, 29, 7, 1, 1, 0],
        [1, 5, 30, 3, 2, 1, 0],
        [1, 5, 31, 11, 2, 1, 0],
        [1, 5, 32, 26, 2, 1, 0],
        [1, 5, 33, 24, 3, 1, 0],
        [1, 5, 34, 25, 3, 1, 0],
        [1, 5, 35, 2, 3, 1, 0],
        [1, 6, 14, 14, 2, 1, 0],
        [1, 6, 36, 8, 1, 1, 0],
        [1, 6, 37, 28, 1, 1, 0],
        [1, 6, 38, 29, 1, 1, 0],
        [1, 6, 39, 27, 2, 1, 0],
        [1, 7, 40, 16, 1, 1, 0],
        [1, 7, 41, 18, 1, 1, 0],
        [1, 7, 43, 30, 2, 1, 0],
        [1, 7, 44, 32, 2, 1, 0]
    ]
    offerta.extend(offerta_i)

    if tipoModuli == "1":
        modulo_i=[
            ["MOD-1", "MOD-1", 1, 4, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 2, 6, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 3, 3, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 4, 1, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 5, 2, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 6, 3, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 7, 4, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 8, 9, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 9, 12, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 10, 8, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 11, 10, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 12, 11, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 13, 14, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 14, 9, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 15, 13, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 16, 6, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 17, 20, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 18, 21, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 19, 22, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 20, 23, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 21, 18, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 22, 15, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 23, 16, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 24, 17, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 25, 19, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 26, 13, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 27, 14, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 28, 7, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 29, 3, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 30, 11, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 31, 26, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 32, 24, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 33, 25, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 34, 2, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 35, 14, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 36, 8, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 37, 28, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 38, 29, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 39, 27, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 40, 16, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 41, 18, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 42, 30, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 43, 32, "N", 2, 2, 0]
        ]
    elif tipoModuli == "N":
        modulo_i = [
            ["MOD-1/2", "MOD12", 1, 4, "N", 2, 2, 0],
            ["MOD-2/2", "MOD22", 1, 5, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 2, 6, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 3, 3, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 3, 7, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 4, 1, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 5, 2, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 6, 3, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 7, 4, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 7, 5, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 8, 9, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 9, 12, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 10, 8, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 11, 10, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 12, 11, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 13, 14, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 14, 9, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 15, 13, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 16, 6, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 17, 20, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 18, 21, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 19, 22, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 20, 23, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 21, 18, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 22, 15, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 23, 16, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 24, 17, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 25, 19, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 26, 13, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 27, 14, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 27, 25, "L", 1, 2, 0],
            ["MOD-1/2", "MOD12", 28, 7, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 28, 5, "L", 1, 2, 0],
            ["MOD-1/2", "MOD12", 29, 3, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 29, 2, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 30, 11, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 31, 26, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 32, 24, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 33, 25, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 33, 7, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 34, 2, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 35, 14, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 36, 8, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 37, 28, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 38, 29, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 39, 27, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 40, 16, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 41, 18, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 42, 30, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 42, 31, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 43, 32, "N", 2, 2, 0]
        ]
    moduli.extend(modulo_i)
    return giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita,  attivita_didattiche, docenti, offerta, moduli, None

def __impostaDati13Cds(tipoModuli):
    anni_accademici = []
    corsi_di_studio = []
    attivita_didattiche = []
    docenti = []
    offerta = []
    moduli = []

    giorni, slot, aule, numerosita = __impostaDatiBase()

    anni_accademici_i=[
        [2021,"2021-2022"]
    ]
    anni_accademici.extend(anni_accademici_i)

    corsi_di_studio_i=[
        ["0120", "INFORMATICA APPLICATA (MACHINE LEARNING E BIG DATA)", 120, 2],
        ["0124", "INFORMATICA", 180, 3],
        ["0123", "SCIENZE BIOLOGICHE", 180, 3],
        ["0122", "SCIENZE NAUTICHE, AERONAUTICHE E METEO-OCEANOGRAFICHE", 180, 3],
        ["0121", "SCIENZE E TECNOLOGIE DELLA NAVIGAZIONE", 120, 2],
        ["0125", "CONDUZIONE DEL MEZZO NAVALE", 180, 3],
        ["0126", "BIOLOGIA PER LA SOSTENIBILITA'", 120, 2],
        ["0332", "INGEGNERIA CIVILE E AMBIENTALE PER LA MITIGAZIONE DEI RISCHI", 180, 3],
        ["0326", "INGEGNERIA GESTIONALE", 120, 2],
        ["0328", "INGEGNERIA GESTIONALE", 180, 3],
        ["0327", "INGEGNERIA INFORMATICA, BIOMEDICA E DELLE TELECOMUNICAZIONI", 180, 3],
        ["0330", "INGEGNERIA DELLA SICUREZZA DEI DATI E DELLE COMUNICAZIONI", 120, 2],
        ["0331", "INGEGNERIA CIVILE E PER LA TUTELA DELL'AMBIENTE COSTIERO", 120, 2]
    ]
    corsi_di_studio.extend(corsi_di_studio_i)

    attivita_didattiche_i=[
        ["A001018", "SCIENTIFIC COMPUTING", 12, "#FF0000"],
        ["A001019", "PHYSICS AND QUANTUM COMPUTING", 6, "#4169E1"],
        ["A001020", "MACHINE LEARNING", 12, "#228B22"],
        ["A001027", "COMPUTER GRAPHICS: ANIMATION AND SIMULATION", 6, "#FFD800"],
        ["A001022", "HIGH PERFORMANCE COMPUTING", 6, "#993300"],
        ["A001024", "INTERNET OF THINGS AND IOT LAB", 12, "#d4bf02"],
        ["A001025", "MULTIMODAL MACHINE LEARNING", 6, "#fa2d9a"],
        ["771", "MATEMATICA I", 12, "#FF0000"],
        ["ARC12", "ARCHITETTURA DEI CALCOLATORI E LABORATORIO DI ARCHITETTURA DEI CALCOLATORI CFU12", 12, "#4169E1"],
        ["PROGR12", "PROGRAMMAZIONE I E LABORATORIO DI PROGRAMMAZIONE I  CFU 12", 12, "#228B22"],
        ["ALGSTD12", "ALGORITMI E STRUTTURE DATI E LABORATORIO DI ALGORITMI E STRUTTURE DATI CFU 12", 12, "#FFD800"],
        ["INFO03", "ECONOMIA E ORGANIZZAZIONE AZIENDALE", 9, "#993300"],
        ["MATII9", "MATEMATICA II CFU 9", 9, "#d4bf02"],
        ["A001195", "INGEGNERIA DEL SOFTWARE E INTERAZIONE UOMO-MACCHINA", 9, "#fa2d9a"],
        ["PRGRIII9", "PROGRAMMAZIONE III E LABORATORIO DI PROGRAMMAZIONE III", 6, "#92b09e"],
        ["RCLRC9", "RETI DI CALCOLATORI E LABORATORIO DI RETI DI CALCOLATORI CFU 9", 9, "#7ec4ba"],
        ["0115021", "MATEMATICA E STATISTICA", 9, "#FF0000"],
        ["012301", "CHIMICA GENERALE ED INORGANICA CON LABORATORIO", 9, "#4169E1"],
        ["01230444", "BIOLOGIA E FISIOLOGIA VEGETALE CON LABORATORIO", 12, "#228B22"],
        ["01230445", "CITOLOGIA ED ISTOLOGIA CON LABORATORIO", 6, "#FFD800"],
        ["012305", "BIOCHIMICA CON LABORATORIO", 9, "#993300"],
        ["0115007", "ECOLOGIA", 9, "#d4bf02"],
        ["012340", "IGIENE", 9, "#fa2d9a"],
        ["01230004", "FISIOLOGIA GENERALE", 6, "#92b09e"],
        ["186", "GENETICA", 6, "#7ec4ba"],
        ["A000733", "INFORMATICA DI BASE E LABORATORIO", 6, "#FF0000"],
        ["ITL030", "TEORIA DEI SEGNALI", 9, "#4169E1"],
        ["A001004", "ANALISI MATEMATICA II", 9, "#228B22"],
        ["FISI26", "FISICA II CFU 6", 6, "#FFD800"],
        ["01200008", "APPLICAZIONI DI CALCOLO SCIENTIFICO E LAB. A.C.S.", 12, "#FF0000"],
        ["IT06", "RADAR", 6, "#4169E1"],
        ["CLIMA", "CLIMATOLOGIA", 6, "#228B22"],
        ["NAVSAT", "NAVIGAZIONE SATELLITARE", 6, "#FFD800"],
        ["TRASP", "TRASPORTO E DIFFUSIONE NELL'OCEANO E NELL'ATMOSFERA", 6, "#993300"],
        ["012105", "ECONOMIA ED ORGANIZZAZIONE AZIENDALE", 6, "#d4bf02"],
        ["A000984", "TENUTA DELLA GUARDIA E LABORATORIO", 6, "#4169E1"],
        ["526", "ANALISI MATEMATICA", 9, "#228B22"],
        ["A000982", "INGLESE TECNICO E LABORATORIO", 6, "#FFD800"],
        ["012109", "TECNOLOGIE DELLE COSTRUZIONI ED ALLESTIMENTO NAVALE", 6, "#993300"],
        ["A001367", "IGIENE DELL'AMBIENTE E DEL TERRITORIO", 6, "#FF0000"],
        ["A001368", "BIOCHIMICA APPLICATA", 6, "#4169E1"],
        ["A001369", "ECONOMIA DELL'AMBIENTE ED ECONOMIA CIRCOLARE", 6, "#228B22"],
        ["A001375", "ECOLOGIA SISTEMICA E VALUTAZIONE AMBIENTALE", 9, "#FFD800"],
        ["A001376", "ZOOLOGIA APPLICATA", 9, "#993300"],
        ["A001053", "CHIMICA E TECNOLOGIE DEI MATERIALI", 9, "#0000FF"],
        ["A001056", "DISEGNO ED ELEMENTI COSTRUTTIVI", 9, "#008000"],
        ["A000562", "MECCANICA RAZIONALE", 9, "#008080"],
        ["A000919", "GEOLOGIA", 6, "#FF0000"],
        ["A001007", "Statistica applicata alle osservazioni  per la valutazione del rischio", 6, "#800000"],
        ["A001006", "ELABORAZIONE DATI CON STRUMENTI INFORMATICI", 6, "#808000"],
        ["ICL042", "TECNICA DELLE COSTRUZIONI", 9, "#FF00FF"],
        ["ICL058", "MECCANICA DELLE TERRE", 9, "#800080"],
        ["IXL040", "COSTRUZIONI IDRAULICHE", 9, "#FF8C00"],
        ["A000438", "Qualità e Sicurezza Elettrica", 12, "#0000FF"],
        ["IGL059", "GESTIONE AZIENDALE", 9, "#0000FF"],
        ["IGL060", "PROBABILITA' E STATISTICA", 9, "#008000"],
        ["IGL043", "ELETTROTECNICA", 9, "#008080"],
        ["A000392", "LINGUA INGLESE", 3, "#0000FF"],
        ["INIBIT03", "FONDAMENTI DI INGEGNERIA BIOMEDICA", 9, "#008000"],
        ["ITL051", "INTRODUZIONE AI CIRCUITI", 6, "#008080"],
        ["ITL035", "ELETTRONICA", 12, "#FF0000"],
        ["ITL038", "PROPAGAZIONE", 6, "#800000"],
        ["A000849", "Analisi dei processi aziendali per la gestione del rischio", 6, "#0000FF"],
        ["A000850", "Reti di Telecomunicazioni e Internet", 6, "#008000"],
        ["ICMT080", "PROGETTAZIONE DEI CIRCUITI ELETTRONICI", 9, "#008080"],
        ["A000854", "Telerilevamento a Microonde", 9, "#FF0000"],
        ["A000893", "Sistemi di comunicazione ed Elaborazione Numerica dei Segnali e laboratorio", 12, "#800000"],
        ["A000971", "Sicurezza dei Sistemi Informatici", 9, "#808000"],
        ["A000991", "DINAMICA DELLE STRUTTURE E INGEGNERIA SISMICA", 9, "#0000FF"],
        ["ICS002", "MATERIALI INNOVATIVI PER L'INGEGNERIA CIVILE", 9, "#008000"],
        ["ICS003", "CARTOGRAFIA NUMERICA E GIS", 9, "#008080"],
        ["ICS007", "PROGETTAZIONE DELLE OPERE IDRAULICHE", 9, "#FF0000"],
        ["ICS008", "PROGETTAZIONE GEOTECNICA", 9, "#800000"],
        ["A000301", "REGIME E PROTEZIONE DEI LITORALI", 9, "#808000"],
        ["A000998", "MONITORAGGIO E VALUTAZIONI AMBIENTALI DELLE AREE COSTIERE", 9, "#FF00FF"],
        ["A000999", "OCEANOGRAFIA COSTIERA", 9, "#800080"]
    ]
    attivita_didattiche.extend(attivita_didattiche_i)

    docenti_i=[
        ["CF001903", "001903", "MARCELLINO", "LIVIA"],
        ["CF002347", "002347", "FERONE", "ALESSIO"],
        ["CF001854", "001854", "CAMASTRA", "FRANCESCO"],
        ["CF000292", "000292", "RIZZARDI", "MARIAROSARIA"],
        ["CF000296", "000296", "GIUNTA", "GIULIO"],
        ["CF000768", "000768", "ROTUNDI", "ALESSANDRA"],
        ["CF001969", "001969", "CIARAMELLA", "ANGELO"],
        ["CF001971", "001971", "STAIANO", "ANTONINO"],
        ["CF001713", "001713", "MONTELLA", "RAFFAELE"],
        ["CF001412", "001412", "METALLO", "CONCETTA"],
        ["CF002025", "002025", "VOLZONE", "BRUNO"],
        ["CF001708", "001708", "D'ONOFRIO", "LUIGI"],
        ["CF002006", "002006", "SALVI", "GIUSEPPE"],
        ["CF000716", "000716", "RUSSO", "GIOVANNI, FULVIO"],
        ["CF002602", "002602", "DI ONOFRIO", "VALERIA"],
        ["CF005922", "005922", "NAPOLITANO", "GAETANA"],
        ["CF002138", "002138", "DI DONATO", "PAOLA"],
        ["CF002318", "002318", "PASQUALE", "VINCENZO"],
        ["CF002159", "002159", "GALLETTI", "ARDELIO"],
        ["CF001954", "001954", "OLIVA", "ROMINA"],
        ["CF001528", "001528", "CASORIA", "PAOLO"],
        ["CF004015", "004015", "SIMONIELLO", "PALMA"],
        ["CF001871", "001871", "FERRAIOLI", "GIAMPAOLO"],
        ["CF001132", "001132", "PREZIOSO", "GIUSEPPINA"],
        ["CF000337", "000337", "ZAMBIANCHI", "ENRICO"],
        ["CF001141", "001141", "FUSCO", "GIANNETTA"],
        ["CF002844", "002844", "PISCOPO", "VINCENZO"],
        ["CF001711", "001711", "AMADORI", "ANNA LISA"],
        ["CF004663", "004663", "NISCO", "MARIA CRISTINA"],
        ["CF001909", "001909", "FRANZESE", "PIER PAOLO"],
        ["CF002651", "002651", "BUONOCORE", "ELVIRA"],
        ["CF002069", "002069", "SANDULLI", "ROBERTO"],
        ["CF003479", "003479", "CERONI", "FRANCESCA"],
        ["CF001523", "001523", "AVERSA", "STEFANO"],
        ["CF001668", "001668", "DELLA MORTE", "RENATA"],
        ["CF005536", "005536", "LUCIANO", "RAIMONDO"],
        ["CF002070", "002070", "PAPPONE", "GERARDO"],
        ["CF001692", "001692", "ROBUSTELLI", "UMBERTO"],
        ["CF002331", "002331", "D'ANTONIO", "SALVATORE"],
        ["CF002610", "002610", "FERONE", "CLAUDIO"],
        ["CF001670", "001670", "CIOFFI", "RAFFAELE"],
        ["CF001733", "001733", "MAGLIOCCOLA", "FRANCESCO"],
        ["CF002315", "002315", "CARAMIA", "PIERLUIGI"],
        ["CF002155", "002155", "BRACALE", "ANTONIO"],
        ["CF004809", "004809", "CERCHIONE", "ROBERTO"],
        ["CF000286", "000286", "PASCAZIO", "VITO"],
        ["CF006981", "006981", "DE MAGISTRIS", "MASSIMILIANO"],
        ["CF002191", "002191", "BASELICE", "FABIO"],
        ["CF001935", "001935", "IADICICCO", "AGOSTINO"],
        ["CF001870", "001870", "NUNZIATA", "FERDINANDO"],
        ["CF000288", "000288", "MIGLIACCIO", "MAURIZIO"],
        ["CF002306", "002306", "SCHIRINZI", "GILDA"],
        ["CF001763", "001763", "NAPOLITANO", "ANTONIO"],
        ["CF001347", "001347", "ROMANO", "LUIGI"],
        ["CF002270", "002270", "THOMAS", "ANTONIO"],
        ["CF001669", "001669", "BUDILLON", "ALESSANDRA"],
        ["CF001875", "001875", "CAMPOPIANO", "STEFANIA"],
        ["CF002052", "002052", "COZZOLINO", "LUCA"],
        ["CF002365", "002365", "DE SANCTIS", "LUCA"],
        ["CF000359", "000359", "BENASSAI", "GUIDO"],
        ["CF001878", "001878", "LEGA", "MASSIMILIANO"],
        ["CF002963", "002963", "DE RUGGIERO", "PAOLA"],
        ["CF002962", "002962", "CASTAGNO", "PASQUALE"],
        ["CF001936", "001936", "CATERINO", "NICOLA"],
        ["CF001939", "001939", "COLANGELO", "FRANCESCO"]
    ]
    docenti.extend(docenti_i)

    offerta_i=[
        [1, 1, 1, 4, 1, 1, 0],
        [1, 1, 2, 6, 1, 1, 0],
        [1, 1, 3, 3, 1, 1, 0],
        [1, 1, 5, 1, 2, 1, 0],
        [1, 1, 6, 2, 2, 1, 0],
        [1, 1, 7, 3, 2, 1, 0],
        [1, 2, 8, 4, 1, 1, 0],
        [1, 2, 9, 9, 1, 1, 0],
        [1, 2, 10, 12, 1, 1, 0],
        [1, 2, 11, 8, 2, 1, 0],
        [1, 2, 12, 10, 2, 1, 0],
        [1, 2, 13, 11, 2, 1, 0],
        [1, 3, 14, 14, 1, 1, 0],
        [1, 3, 15, 9, 2, 1, 0],
        [1, 3, 16, 13, 2, 1, 0],
        [1, 3, 17, 6, 2, 1, 0],
        [1, 4, 18, 20, 1, 1, 0],
        [1, 4, 19, 21, 1, 1, 0],
        [1, 4, 20, 22, 1, 1, 0],
        [1, 4, 21, 23, 1, 1, 0],
        [1, 4, 22, 18, 2, 1, 0],
        [1, 4, 23, 15, 3, 1, 0],
        [1, 4, 24, 16, 3, 1, 0],
        [1, 4, 25, 17, 3, 1, 0],
        [1, 4, 26, 19, 3, 1, 0],
        [1, 5, 27, 13, 1, 1, 0],
        [1, 5, 28, 14, 1, 1, 0],
        [1, 5, 29, 7, 1, 1, 0],
        [1, 5, 30, 3, 2, 1, 0],
        [1, 5, 31, 11, 2, 1, 0],
        [1, 5, 32, 26, 2, 1, 0],
        [1, 5, 33, 24, 3, 1, 0],
        [1, 5, 34, 25, 3, 1, 0],
        [1, 5, 35, 2, 3, 1, 0],
        [1, 6, 14, 14, 2, 1, 0],
        [1, 6, 36, 8, 1, 1, 0],
        [1, 6, 37, 28, 1, 1, 0],
        [1, 6, 38, 29, 1, 1, 0],
        [1, 6, 39, 27, 2, 1, 0],
        [1, 7, 40, 16, 1, 1, 0],
        [1, 7, 41, 18, 1, 1, 0],
        [1, 7, 43, 30, 2, 1, 0],
        [1, 7, 44, 32, 2, 1, 0],
        [1, 8, 45, 40, 1, 1, 0],
        [1, 8, 46, 42, 1, 1, 0],
        [1, 8, 47, 36, 2, 1, 0],
        [1, 8, 48, 37, 2, 1, 0],
        [1, 8, 49, 38, 2, 1, 0],
        [1, 8, 50, 39, 2, 1, 0],
        [1, 8, 51, 33, 3, 1, 0],
        [1, 8, 52, 34, 3, 1, 0],
        [1, 8, 53, 35, 3, 1, 0],
        [1, 9, 54, 43, 2, 1, 0],
        [1, 10, 55, 45, 2, 1, 0],
        [1, 10, 56, 46, 2, 1, 0],
        [1, 10, 57, 47, 2, 1, 0],
        [1, 11, 58, 29, 1, 1, 0],
        [1, 11, 59, 48, 2, 1, 0],
        [1, 11, 60, 47, 2, 1, 0],
        [1, 11, 61, 49, 3, 1, 0],
        [1, 11, 62, 50, 3, 1, 0],
        [1, 11, 27, 23, 2, 1, 0],
        [1, 12, 63, 55, 1, 1, 0],
        [1, 12, 64, 56, 1, 1, 0],
        [1, 12, 65, 57, 1, 1, 0],
        [1, 12, 66, 51, 2, 1, 0],
        [1, 12, 67, 52, 2, 1, 0],
        [1, 12, 68, 54, 2, 1, 0],
        [1, 13, 69, 64, 1, 1, 0],
        [1, 13, 70, 65, 1, 1, 0],
        [1, 13, 71, 38, 1, 1, 0],
        [1, 13, 72, 35, 2, 1, 0],
        [1, 13, 73, 59, 2, 1, 0],
        [1, 13, 74, 60, 2, 1, 0],
        [1, 13, 75, 61, 2, 1, 0],
        [1, 13, 76, 62, 2, 1, 0]
    ]
    offerta.extend(offerta_i)

    if tipoModuli == "1":
        modulo_i=[
            ["MOD-1", "MOD-1", 1, 4, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 2, 6, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 3, 3, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 4, 1, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 5, 2, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 6, 3, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 7, 4, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 8, 9, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 9, 12, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 10, 8, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 11, 10, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 12, 11, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 13, 14, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 14, 9, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 15, 13, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 16, 6, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 17, 20, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 18, 21, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 19, 22, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 20, 23, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 21, 18, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 22, 15, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 23, 16, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 24, 17, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 25, 19, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 26, 13, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 27, 14, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 28, 7, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 29, 3, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 30, 11, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 31, 26, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 32, 24, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 33, 25, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 34, 2, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 35, 14, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 36, 8, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 37, 28, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 38, 29, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 39, 27, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 40, 16, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 41, 18, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 42, 30, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 43, 32, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 44, 40, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 45, 42, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 46, 36, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 47, 37, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 48, 38, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 49, 39, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 50, 33, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 51, 34, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 52, 35, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 53, 43, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 54, 45, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 55, 46, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 56, 47, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 57, 29, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 58, 48, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 59, 47, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 60, 49, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 61, 50, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 62, 23, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 63, 55, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 64, 56, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 65, 57, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 66, 51, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 67, 52, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 68, 54, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 69, 64, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 70, 65, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 71, 38, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 72, 35, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 73, 59, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 74, 60, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 75, 61, "N", 2, 2, 0],
            ["MOD-1", "MOD-1", 76, 62, "N", 2, 2, 0]
        ]
    elif tipoModuli == "N":
        modulo_i = [
            ["MOD-1/2", "MOD12", 1, 4, "N", 2, 2, 0],
            ["MOD-2/2", "MOD22", 1, 5, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 2, 6, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 3, 3, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 3, 7, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 4, 1, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 5, 2, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 6, 3, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 7, 4, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 7, 5, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 8, 9, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 9, 12, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 10, 8, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 11, 10, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 12, 11, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 13, 14, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 14, 9, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 15, 13, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 16, 6, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 17, 20, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 18, 21, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 19, 22, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 20, 23, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 21, 18, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 22, 15, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 23, 16, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 24, 17, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 25, 19, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 26, 13, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 27, 14, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 27, 25, "L", 1, 2, 0],
            ["MOD-1/2", "MOD12", 28, 7, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 28, 5, "L", 1, 2, 0],
            ["MOD-1/2", "MOD12", 29, 3, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 29, 2, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 30, 11, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 31, 26, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 32, 24, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 33, 25, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 33, 7, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 34, 2, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 35, 14, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 36, 8, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 37, 28, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 38, 29, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 39, 27, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 40, 16, "N", 2, 2, 0],
            ["MOD-1/1", "MOD11", 41, 18, "N", 2, 2, 0],
            ["MOD-1/2", "MOD12", 42, 30, "N", 1, 2, 0],
            ["MOD-2/2", "MOD22", 42, 31, "L", 1, 2, 0],
            ["MOD-1/1", "MOD11", 43, 32, "N", 2, 2, 0],

        ]
    moduli.extend(modulo_i)
    return giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita,  attivita_didattiche, docenti, offerta, moduli, None


def __registraDatiInDb(giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita, attivita_didattiche, docenti, offerta, moduli, logistica_docenti):
    try:
        if giorni is not None:
            try:
                for g in giorni:
                    row = Giorno(descrizione=g)
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dei giorni", "danger")

        if slot is not None:
            try:
                for s in slot:
                    row = Slot(descrizione=s[0],
                               ora_slot_cal=s[1])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento degli slot", "danger")

        if anni_accademici is not None:
            try:
                for a in anni_accademici:
                    row = AnnoAccademico(anno=a[0],
                                         anno_esteso=a[1])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento degli anni accademici", "danger")

        if aule is not None:
            try:
                for a in aule:
                    row = Aula(codice=a[0],
                               descrizione=a[1],
                               capienza=a[2],
                               tipo_aula=a[3])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento delle aule", "danger")

        if numerosita is not None:
            try:
                for n in numerosita:
                    row = NumerositaAnniCorso(codice_corso=n[0],
                                              anno_di_corso=n[1],
                                              numerosita=n[2])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento delle numerosità", "danger")

        if corsi_di_studio is not None:
            try:
                for c in corsi_di_studio:
                    row = CorsoDiStudio(codice=c[0],
                                        descrizione=c[1],
                                        cfu=c[2],
                                        durata_legale=c[3])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dei corsi", "danger")

        if attivita_didattiche is not None:
            try:
                for a in attivita_didattiche:
                    row = AttivitaDidattica(codice=a[0],
                                            descrizione=a[1],
                                            cfu=a[2],
                                            colore=a[3])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento delle attività didattiche", "danger")

        if docenti is not None:
            try:
                for d in docenti:
                    row = Docente(codice_fiscale=d[0],
                                  matricola=d[1],
                                  cognome=d[2],
                                  nome=d[3])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dei docenti", "danger")

        if offerta is not None:
            try:
                for o in offerta:
                    row = Offerta(anno_accademico_id=o[0],
                                  corso_di_studio_id=o[1],
                                  attivita_didattica_id=o[2],
                                  docente_id=o[3],
                                  anno_di_corso=o[4],
                                  semestre=o[5],
                                  max_studenti=o[6])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dell'offerta", "danger")

        if moduli is not None:
            try:
                for m in moduli:
                    row = Modulo(codice=m[0],
                                 descrizione=m[1],
                                 offerta_id=m[2],
                                 docente_id=m[3],
                                 tipo_aula=m[4],
                                 numero_sessioni=m[5],
                                 durata_sessioni=m[6],
                                 max_studenti=m[7])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dei moduli", "danger")

        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("Errore di caricamento dati nel DB")
    return -1


def caricaDati7Cds(tipoModuli):
    try:
        __svuotaTabelle()
        giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita,  attivita_didattiche, docenti, offerta, moduli, logistica_docenti = __impostaDati7Cds(tipoModuli)
        __registraDatiInDb(giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita,  attivita_didattiche, docenti, offerta, moduli, logistica_docenti)
        flash("Caricamento effettuato correttamente!", "success")
    except SQLAlchemyError:
        flash("Errore nella fase di caricamento dei dati Esse3 preimpostati", "danger")


def caricaDati13Cds(tipoModuli):
    try:
        __svuotaTabelle()
        giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita,  attivita_didattiche, docenti, offerta, moduli, logistica_docenti = __impostaDati13Cds(tipoModuli)
        __registraDatiInDb(giorni, slot, anni_accademici, aule, corsi_di_studio, numerosita,  attivita_didattiche, docenti, offerta, moduli, logistica_docenti)
        flash("Caricamento effettuato correttamente!", "success")
    except SQLAlchemyError:
        flash("Errore nella fase di caricamento dei dati Esse3 preimpostati", "danger")


def svuotaDb():
    try:
        __svuotaTabelle()
        flash("DB svuotato correttamente!", "success")
        return 0
    except SQLAlchemyError:
        flash("Errore di svuotamento del DB!", "danger")
        return -1


def caricaDatiDalDb(aa, semestre):
    try:
        corsi_tt=[]
        corsi=db.session.query(CorsoDiStudio).all()
        for c in corsi:
            corsi_tt.append(CorsoDiStudioTt(c.id, c.codice, c.descrizione, c.cfu, c.durata_legale))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Corsi di studio", "danger")
        return -1   
    
    try:
        giorni_tt=[]
        giorni=db.session.query(Giorno).all()
        for g in giorni:
            giorni_tt.append(GiornoTt(g.id, g.descrizione))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Giorni")
        return -1    

    try:
        slot_tt=[]
        slot=db.session.query(Slot).all()    
        for s in slot:
            slot_tt.append(SlotTt(s.id, s.descrizione))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Slot")
        return -1    

    try:
        aule_tt=[]
        aule=db.session.query(Aula).all()
        for a in aule:
            aule_tt.append(AulaTt(a.id, a.codice, a.descrizione, a.capienza, a.tipo_aula))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Aule")
        return -1    
        
    try:
        moduli_tt=[]
        # Recupero delle informazioni dal DB per la formazione degli oggetti Modulo da collocare nell"orario
        moduli=db.session.query(Modulo, Offerta, AttivitaDidattica, AnnoAccademico, CorsoDiStudio, Docente)\
        .join(Offerta, Modulo.offerta_id == Offerta.id)\
        .join(AttivitaDidattica, Offerta.attivita_didattica_id == AttivitaDidattica.id)\
        .join(CorsoDiStudio, Offerta.corso_di_studio_id == CorsoDiStudio.id)\
        .join(AnnoAccademico, Offerta.anno_accademico_id == AnnoAccademico.id)\
        .join(Docente, Offerta.docente_id == Docente.id)\
        .filter(Offerta.anno_accademico_id == aa)\
        .filter(Offerta.semestre == semestre).all()
        for m in moduli:
            moduli_tt.append(ModuloTt(m.Modulo.id,m.Modulo.codice,m.Modulo.descrizione,m.AttivitaDidattica.codice,m.AttivitaDidattica.descrizione,\
                                      m.CorsoDiStudio.id,m.CorsoDiStudio.codice,m.CorsoDiStudio.descrizione,m.Docente.matricola,m.Docente.cognome,m.Docente.nome,\
                                      m.Modulo.numero_sessioni,m.Modulo.durata_sessioni,m.Offerta.id,m.Offerta.anno_di_corso,m.Offerta.semestre,\
                                      m.Offerta.max_studenti,m.Modulo.max_studenti,m.Modulo.tipo_aula))

    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Moduli")
        return -1    
    
    try:
        logistica_tt=[]
        logistica=db.session.query(LogisticaDocente).all()
        for l in logistica:
            logistica_tt.append([l.offerta_id,l.modulo_id,l.slot_id,l.giorno_id])
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Logistica Docenti")
        return -1    
    
    return corsi_tt, giorni_tt, slot_tt, aule_tt, moduli_tt, logistica_tt


def getColori():
    return colori


def caricaDatiBase():
    try:
        __svuotaTabelle()
        giorni, slot, aule, numerosita = __impostaDatiBase()
        __registraDatiInDb(giorni, slot, None, aule, None, numerosita, None, None, None, None, None)
        flash("Caricamento dei dati di base effettuato correttamente!", "success")
    except SQLAlchemyError:
        flash("Errore nella fase di caricamento dei dati di base", "danger")


def inizializza_db():
    try:
        db.session.query(StatoOrario).delete()
        db.session.execute("ALTER TABLE stato_orario AUTO_INCREMENT=1")
        row=StatoOrario(codice="P", descrizione="Pubblicato")
        db.session.add(row)
        row=StatoOrario(codice="B", descrizione="Bozza")
        db.session.add(row)
        db.session.commit()
    except:
        None


def getAttributiLDap(uid):
    try:
        ldap_server=Server(config.AUTH_LDAP_SERVER+":"+config.AUTH_LDAP_PORT, get_info=ALL)
        ldap_connection=Connection(ldap_server, user="cn=admin,dc=uniparthenope,dc=it",password="wattpw01")

        if ldap_connection.bind()==True:
            if ldap_connection.search(search_base=config.AUTH_LDAP_SEARCH, search_filter=f"(uid={uid})",search_scope=SUBTREE, attributes=["token","role"])==True:
                ent=ldap_connection.entries[0]
                ldap_connection.unbind()
                try:
                    role=ent["role"][0]
                    token=ent["token"][0]
                except IndexError:
                    role=None
                    token=None
                return token, role
            else:
                return None, None

    except LDAPSocketOpenError:
        print("Unabled to connect to the LDAP server!")
        return None


def getOrarioCorrente():

    orarioCorrente = []
    testata_id=session["testataId"]
    rows = db.session.query(OrarioDettaglio, Modulo, Giorno, Offerta, AttivitaDidattica, CorsoDiStudio, Docente, Slot, Aula) \
        .join(CorsoDiStudio, OrarioDettaglio.corso_di_studio_id == CorsoDiStudio.id) \
        .join(Modulo, OrarioDettaglio.modulo_id == Modulo.id) \
        .join(Offerta, Modulo.offerta_id == Offerta.id) \
        .join(Docente, Modulo.docente_id == Docente.id) \
        .join(Slot, OrarioDettaglio.slot_id == Slot.id) \
        .join(Giorno, OrarioDettaglio.giorno_id == Giorno.id) \
        .join(AttivitaDidattica, Offerta.attivita_didattica_id == AttivitaDidattica.id) \
        .join(Aula, OrarioDettaglio.aula_id == Aula.id) \
        .filter(OrarioDettaglio.testata_id == testata_id) \
        .order_by(CorsoDiStudio.codice.asc(), Giorno.id.asc(), Modulo.codice.asc(), Slot.id.asc(), Aula.codice.asc()).all()

    id = 0
    for r in rows:
        id += 1
        if r.Modulo.max_studenti > 0:
            numerosita = r.Modulo.max_studenti
        else:
            numerosita = r.Offerta.max_studenti

        rigaOrario = {
            "id": id,
            "testata_id": int(testata_id),
            "giorno_id": int(r.Giorno.id),
            "giorno": str(r.Giorno.descrizione),
            "corso_id": int(r.CorsoDiStudio.id),
            "codice_corso": str(r.CorsoDiStudio.codice),
            "descrizione_corso": str(r.CorsoDiStudio.descrizione),
            "colore_corso": str(getColori()[r.CorsoDiStudio.id]),
            "codice_attivita": str(r.AttivitaDidattica.codice),
            "descrizione_attivita": str(r.AttivitaDidattica.descrizione),
            "colore_attivita": str(r.AttivitaDidattica.colore),
            "modulo_id": int(r.Modulo.id),
            "descrizione_modulo": str(r.Modulo.descrizione),
            "numerosita_modulo": int(numerosita),
            "slot_id": int(r.Slot.id),
            "descrizione_slot": str(r.Slot.descrizione),
            "nome_docente": str(r.Docente.nome),
            "cognome_docente": str(r.Docente.cognome),
            "anno_corso": int(r.Offerta.anno_di_corso),
            "aula_id": int(r.Aula.id),
            "aula": str(r.Aula.descrizione),
            "capienza_aula": int(r.Aula.capienza) }

        orarioCorrente.append(rigaOrario)
    return orarioCorrente

def getChiusureOrarioCorrente():
    rows = db.session.query(Chiusura).filter(Chiusura.testata_id == session["testataId"]).all()
    chiusureOrarioCorrente = []

    for r in rows:
        cur = r.data_inizio
        end = r.data_fine + timedelta(days=1)
        while (cur < end):
            if cur.strftime("%Y/%m/%d") not in chiusureOrarioCorrente:
                chiusureOrarioCorrente.append(cur.strftime("%Y/%m/%d"))
            cur = cur + timedelta(days=1)

    return chiusureOrarioCorrente


