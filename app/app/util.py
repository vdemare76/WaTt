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
    2:"#997A00",
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
        ["0126", 3, 25],
        ["0332", 1, 30],
        ["0332", 2, 30],
        ["0332", 3, 20],
        ["0326", 1, 45],
        ["0326", 2, 25],
        ["0328", 1, 50],
        ["0328", 2, 40],
        ["0328", 3, 35],
        ["0327", 1, 40],
        ["0327", 2, 35],
        ["0327", 3, 30],
        ["0330", 1, 45],
        ["0330", 2, 30],
        ["0331", 1, 35],
        ["0331", 2, 20]
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
        [1, "0120", "INFORMATICA APPLICATA (MACHINE LEARNING E BIG DATA) ", 120, 2],
        [2, "0121", "SCIENZE E TECNOLOGIE DELLA NAVIGAZIONE", 120, 2],
        [3, "0122", "SCIENZE NAUTICHE, AERONAUTICHE E METEO-OCEANOGRAFICHE", 180, 3],
        [4, "0123", "SCIENZE BIOLOGICHE", 180, 3],
        [5, "0124", "INFORMATICA", 180, 3],
        [6, "0125", "CONDUZIONE DEL MEZZO NAVALE", 180, 3],
        [7, "0126", "BIOLOGIA PER LA SOSTENIBILITA'", 120, 2]
    ]
    corsi_di_studio.extend(corsi_di_studio_i)

    attivita_didattiche_i=[
        [1, "A001018", "SCIENTIFIC COMPUTING", 12, "#990000"],
        [2, "A001019", "PHYSICS AND QUANTUM COMPUTING", 6, "#997A00"],
        [3, "A001020", "MACHINE LEARNING", 12, "#009900"],
        [4, "A001027", "COMPUTER GRAPHICS: ANIMATION AND SIMULATION", 6, "#0066FF"],
        [5, "A001022", "HIGH PERFORMANCE COMPUTING", 6, "#800000"],
        [6, "A001024", "INTERNET OF THINGS AND IOT LAB", 12, "#FF6666"],
        [7, "A001025", "MULTIMODAL MACHINE LEARNING", 6, "#999999"],
        [8, "01200008", "APPLICAZIONI DI CALCOLO SCIENTIFICO E LAB. A.C.S.", 12, "#990000"],
        [9, "IT06", "RADAR", 6, "#997A00"],
        [10, "CLIMA", "CLIMATOLOGIA", 6, "#009900"],
        [11, "NAVSAT", "NAVIGAZIONE SATELLITARE", 6, "#0066FF"],
        [12, "TRASP", "TRASPORTO E DIFFUSIONE NELL'OCEANO E NELL'ATMOSFERA", 6, "#800000"],
        [13, "012105", "ECONOMIA ED ORGANIZZAZIONE AZIENDALE", 6, "#FF6666"],
        [14, "A000733", "INFORMATICA DI BASE E LABORATORIO", 6, "#990000"],
        [15, "A001004", "ANALISI MATEMATICA II", 9, "#997A00"],
        [16, "FISI26", "FISICA II CFU 6", 6, "#009900"],
        [17, "0115021", "MATEMATICA E STATISTICA", 9, "#990000"],
        [18, "012301", "CHIMICA GENERALE ED INORGANICA CON LABORATORIO", 9, "#997A00"],
        [19, "01230444", "BIOLOGIA E FISIOLOGIA VEGETALE CON LABORATORIO", 12, "#009900"],
        [20, "01230445", "CITOLOGIA ED ISTOLOGIA CON LABORATORIO", 6, "#0066FF"],
        [21, "012305", "BIOCHIMICA CON LABORATORIO", 9, "#800000"],
        [22, "0115007", "ECOLOGIA", 9, "#FF6666"],
        [23, "012340", "IGIENE", 9, "#999999"],
        [24, "186", "GENETICA", 6, "#99FF99"],
        [25, "ARC12", "ARCHITETTURA DEI CALCOLATORI E LABORATORIO DI ARCHITETTURA DEI CALCOLATORI CFU12", 12, "#990000"],
        [26, "PROGR12", "PROGRAMMAZIONE I E LABORATORIO DI PROGRAMMAZIONE I  CFU 12", 12, "#997A00"],
        [27, "ALGSTD12", "ALGORITMI E STRUTTURE DATI E LABORATORIO DI ALGORITMI E STRUTTURE DATI CFU 12", 12, "#009900"],
        [28, "INFO03", "ECONOMIA E ORGANIZZAZIONE AZIENDALE", 9, "#0066FF"],
        [29, "MATII9", "MATEMATICA II CFU 9", 9, "#800000"],
        [30, "A001195", "INGEGNERIA DEL SOFTWARE E INTERAZIONE UOMO-MACCHINA", 9, "#FF6666"],
        [31, "PRGRIII9", "PROGRAMMAZIONE III E LABORATORIO DI PROGRAMMAZIONE III", 6, "#999999"],
        [32, "RCLRC9", "RETI DI CALCOLATORI E LABORATORIO DI RETI DI CALCOLATORI CFU 9", 9, "#99FF99"],
        [33, "771", "MATEMATICA I", 12, "#660099"],
        [34, "A000984", "TENUTA DELLA GUARDIA E LABORATORIO", 6, "#997A00"],
        [35, "526", "ANALISI MATEMATICA", 9, "#009900"],
        [36, "A000982", "INGLESE TECNICO E LABORATORIO", 6, "#0066FF"],
        [37, "012109", "TECNOLOGIE DELLE COSTRUZIONI ED ALLESTIMENTO NAVALE", 6, "#800000"],
        [38, "A001367", "IGIENE DELL'AMBIENTE E DEL TERRITORIO", 6, "#990000"],
        [39, "A001368", "BIOCHIMICA APPLICATA", 6, "#997A00"],
        [40, "A001369", "ECONOMIA DELL'AMBIENTE ED ECONOMIA CIRCOLARE", 6, "#009900"],
        [41, "A001850", "BIOLOGIA DELLA CONSERVAZIONE II", 9, "#0066FF"],
        [42, "A001376", "ZOOLOGIA APPLICATA", 9, "#800000"]
    ]
    attivita_didattiche.extend(attivita_didattiche_i)

    docenti_i=[
        [1, "CF001903", "001903", "MARCELLINO", "LIVIA"],
        [2, "CF002347", "002347", "FERONE", "ALESSIO"],
        [3, "CF001854", "001854", "CAMASTRA", "FRANCESCO"],
        [4, "CF000292", "000292", "RIZZARDI", "MARIAROSARIA"],
        [5, "CF000296", "000296", "GIUNTA", "GIULIO"],
        [6, "CF000768", "000768", "ROTUNDI", "ALESSANDRA"],
        [7, "CF001969", "001969", "CIARAMELLA", "ANGELO"],
        [8, "CF005314", "005314", "DE NINO", "MAURIZIO"],
        [9, "CF001132", "001132", "PREZIOSO", "GIUSEPPINA"],
        [10,"CF001871", "001871", "FERRAIOLI", "GIAMPAOLO"],
        [11, "CF000337", "000337", "ZAMBIANCHI", "ENRICO"],
        [12, "CF001412", "001412", "METALLO", "CONCETTA"],
        [13, "CF001141", "001141", "FUSCO", "GIANNETTA"],
        [14, "CF001708", "001708", "D'ONOFRIO", "LUIGI"],
        [15, "CF002006", "002006", "SALVI", "GIUSEPPE"],
        [16, "CF000716", "000716", "RUSSO", "GIOVANNI, FULVIO"],
        [17, "CF002602", "002602", "DI ONOFRIO", "VALERIA"],
        [18, "CF002138", "002138", "DI DONATO", "PAOLA"],
        [19, "CF002318", "002318", "PASQUALE", "VINCENZO"],
        [20, "CF002159", "002159", "GALLETTI", "ARDELIO"],
        [21, "CF001954", "001954", "OLIVA", "ROMINA"],
        [22, "CF001528", "001528", "CASORIA", "PAOLO"],
        [23, "CF004015", "004015", "SIMONIELLO", "PALMA"],
        [24, "CF001971", "001971", "STAIANO", "ANTONINO"],
        [25, "CF001713", "001713", "MONTELLA", "RAFFAELE"],
        [26, "CF002025", "002025", "VOLZONE", "BRUNO"],
        [27, "CF001535", "001535", "FORMICA", "MARIA ROSARIA"],
        [28, "CF002844", "002844", "PISCOPO", "VINCENZO"],
        [29, "CF001711", "001711", "AMADORI", "ANNA LISA"],
        [30, "CF004663", "004663", "NISCO", "MARIA CRISTINA"],
        [31, "CF002069", "002069", "SANDULLI", "ROBERTO"],
        [32, "CF001136", "001136", "APRILE", "MARIA CARMELA"]
    ]
    docenti.extend(docenti_i)

    offerta_i=[
        [1, 1, 1, 1, 4, 1, 1, 30],
        [2, 1, 1, 2, 6, 1, 1, 30],
        [3, 1, 1, 3, 3, 1, 1, 30],
        [4, 1, 1, 4, 8, 1, 1, 30],
        [5, 1, 1, 5, 1, 2, 1, 15],
        [6, 1, 1, 6, 2, 2, 1, 15],
        [7, 1, 1, 7, 3, 2, 1, 15],
        [8, 1, 2, 8, 4, 1, 1, 40],
        [9, 1, 2, 9, 10, 1, 1, 40],
        [10, 1, 2, 10, 13, 1, 1, 40],
        [11, 1, 2, 11, 9, 2, 1, 20],
        [12, 1, 2, 12, 11, 2, 1, 20],
        [13, 1, 2, 13, 12, 2, 1, 20],
        [14, 1, 3, 14, 15, 1, 1, 50],
        [15, 1, 3, 15, 14, 2, 1, 30],
        [16, 1, 3, 16, 6, 2, 1, 30],
        [17, 1, 4, 17, 20, 1, 1, 60],
        [18, 1, 4, 18, 21, 1, 1, 60],
        [19, 1, 4, 19, 22, 1, 1, 60],
        [20, 1, 4, 20, 23, 1, 1, 60],
        [21, 1, 4, 21, 18, 2, 1, 45],
        [22, 1, 4, 22, 16, 3, 1, 25],
        [23, 1, 4, 23, 17, 3, 1, 25],
        [24, 1, 4, 24, 19, 3, 1, 25],
        [25, 1 , 5, 25, 15, 1, 1, 100],
        [26, 1, 5, 26, 7, 1, 1, 100],
        [27, 1, 5, 27, 3, 2, 1, 70],
        [28, 1, 5, 28, 12, 2, 1, 70],
        [29, 1, 5, 29, 26, 2, 1, 70],
        [30, 1, 5, 30, 24, 3, 1, 50],
        [31, 1, 5, 31, 25, 3, 1, 50],
        [32, 1, 5, 32, 2, 3, 1, 50],
        [33, 1, 5, 33, 27, 1, 1, 100],
        [34, 1, 6, 14, 15, 2, 1, 20],
        [35, 1, 6, 34, 9, 1, 1, 40],
        [36, 1, 6, 35, 29, 1, 1, 40],
        [37, 1, 6, 36, 30, 1, 1, 40],
        [38, 1, 6, 37, 28, 2, 1, 20],
        [39, 1, 7, 38, 17, 1, 1, 50],
        [40, 1, 7, 39, 18, 1, 1, 50],
        [41, 1, 7, 40, 32, 1, 1, 50],
        [42, 1, 7, 41, 16, 1, 1, 50],
        [43, 1, 7, 42, 31, 2, 1, 30]
    ]
    offerta.extend(offerta_i)

    if tipoModuli == "1":
        modulo_i=[
            [1, "MOD-1", "MOD-1", 1, 4, "N", 2, 2, 0],
            [2, "MOD-1", "MOD-1", 2, 6, "N", 2, 2, 0],
            [3, "MOD-1", "MOD-1", 3, 3, "N", 2, 2, 0],
            [4, "MOD-1", "MOD-1", 4, 8, "N", 2, 2, 0],
            [5, "MOD-1", "MOD-1", 5, 1, "N", 2, 2, 0],
            [6, "MOD-1", "MOD-1", 6, 2, "N", 2, 2, 0],
            [7, "MOD-1", "MOD-1", 7, 3, "N", 2, 2, 0],
            [8, "MOD-1", "MOD-1", 8, 4, "N", 2, 2, 0],
            [9, "MOD-1", "MOD-1", 9, 10, "N", 2, 2, 0],
            [10, "MOD-1", "MOD-1", 10, 13, "N", 2, 2, 0],
            [11, "MOD-1", "MOD-1", 11, 9, "N", 2, 2, 0],
            [12, "MOD-1", "MOD-1", 12, 11, "N", 2, 2, 0],
            [13, "MOD-1", "MOD-1", 13, 12, "N", 2, 2, 0],
            [14, "MOD-1", "MOD-1", 14, 15, "N", 2, 2, 0],
            [15, "MOD-1", "MOD-1", 15, 14, "N", 2, 2, 0],
            [16, "MOD-1", "MOD-1", 16, 6, "N", 2, 2, 0],
            [17, "MOD-1", "MOD-1", 17, 20, "N", 2, 2, 0],
            [18, "MOD-1", "MOD-1", 18, 21, "N", 2, 2, 0],
            [19, "MOD-1", "MOD-1", 19, 22, "N", 2, 2, 0],
            [20, "MOD-1", "MOD-1", 20, 23, "N", 2, 2, 0],
            [21, "MOD-1", "MOD-1", 21, 18, "N", 2, 2, 0],
            [22, "MOD-1", "MOD-1", 22, 16, "N", 2, 2, 0],
            [23, "MOD-1", "MOD-1", 23, 17, "N", 2, 2, 0],
            [24, "MOD-1", "MOD-1", 24, 19, "N", 2, 2, 0],
            [25, "MOD-1", "MOD-1", 25, 15, "N", 2, 2, 0],
            [26, "MOD-1", "MOD-1", 26, 7, "N", 2, 2, 0],
            [27, "MOD-1", "MOD-1", 27, 3, "N", 2, 2, 0],
            [28, "MOD-1", "MOD-1", 28, 12, "N", 2, 2, 0],
            [29, "MOD-1", "MOD-1", 29, 26, "N", 2, 2, 0],
            [30, "MOD-1", "MOD-1", 30, 24, "N", 2, 2, 0],
            [31, "MOD-1", "MOD-1", 31, 25, "N", 2, 2, 0],
            [32, "MOD-1", "MOD-1", 32, 2, "N", 2, 2, 0],
            [33, "MOD-1", "MOD-1", 33, 27, "N", 2, 2, 0],
            [34, "MOD-1", "MOD-1", 34, 15, "N", 2, 2, 0],
            [35, "MOD-1", "MOD-1", 35, 9, "N", 2, 2, 0],
            [36, "MOD-1", "MOD-1", 36, 29, "N", 2, 2, 0],
            [37, "MOD-1", "MOD-1", 37, 30, "N", 2, 2, 0],
            [38, "MOD-1", "MOD-1", 38, 28, "N", 2, 2, 0],
            [39, "MOD-1", "MOD-1", 39, 17, "N", 2, 2, 0],
            [40, "MOD-1", "MOD-1", 40, 18, "N", 2, 2, 0],
            [41, "MOD-1", "MOD-1", 41, 32, "N", 2, 2, 0],
            [42, "MOD-1", "MOD-1", 42, 16, "N", 2, 2, 0],
            [43, "MOD-1", "MOD-1", 43, 31, "N", 2, 2, 0]
        ]
    elif tipoModuli == "N":
        modulo_i = [
            [1, "MOD-1/2", "MOD12", 1, 4, "N", 2, 2, 0],
            [2, "MOD-2/2", "MOD22", 1, 5, "L", 1, 2, 25],
            [3, "MOD-1/1", "MOD11", 2, 6, "N", 2, 2, 0],
            [4, "MOD-1/2", "MOD12", 3, 3, "N", 2, 2, 0],
            [5, "MOD-2/2", "MOD22", 3, 7, "L", 1, 2, 25],
            [6, "MOD-1/1", "MOD11", 4, 8, "N", 2, 2, 0],
            [7, "MOD-1/1", "MOD11", 5, 1, "N", 2, 2, 0],
            [8, "MOD-1/1", "MOD11", 6, 2, "N", 2, 2, 0],
            [9, "MOD-1/1", "MOD11", 7, 3, "N", 2, 2, 0],
            [10, "MOD-1/2", "MOD12", 8, 4, "N", 2, 2, 0],
            [11, "MOD-2/2", "MOD22", 8, 5, "L", 1, 2, 25],
            [12, "MOD-1/1", "MOD11", 9, 10, "N", 2, 2, 0],
            [13, "MOD-1/1", "MOD11", 10, 13, "N", 2, 2, 0],
            [14, "MOD-1/1", "MOD11", 11, 9, "N", 2, 2, 0],
            [15, "MOD-1/1", "MOD11", 12, 11, "N", 2, 2, 0],
            [16, "MOD-1/1", "MOD11", 13, 12, "N", 2, 2, 0],
            [17, "MOD-1/1", "MOD11", 14, 15, "N", 2, 2, 0],
            [18, "MOD-1/1", "MOD11", 15, 14, "N", 2, 2, 0],
            [19, "MOD-1/1", "MOD11", 16, 6, "N", 2, 2, 0],
            [20, "MOD-1/1", "MOD11", 17, 20, "N", 2, 2, 0],
            [21, "MOD-1/1", "MOD11", 18, 21, "N", 2, 2, 0],
            [22, "MOD-1/1", "MOD11", 19, 22, "N", 2, 2, 0],
            [23, "MOD-1/1", "MOD11", 20, 23, "N", 2, 2, 0],
            [24, "MOD-1/1", "MOD11", 21, 18, "N", 2, 2, 0],
            [25, "MOD-1/1", "MOD11", 22, 16, "N", 2, 2, 0],
            [26, "MOD-1/1", "MOD11", 23, 17, "N", 2, 2, 0],
            [27, "MOD-1/1", "MOD11", 24, 19, "N", 2, 2, 0],
            [28, "MOD-1/2", "MOD12", 25, 15, "N", 2, 2, 0],
            [29, "MOD-2/2", "MOD22", 25, 25, "L", 1, 2, 25],
            [30, "MOD-1/2", "MOD12", 26, 7, "N", 2, 2, 0],
            [31, "MOD-2/2", "MOD22", 26, 5, "L", 1, 2, 25],
            [32, "MOD-1/2", "MOD12", 27, 3, "N", 2, 2, 0],
            [33, "MOD-2/2", "MOD22", 27, 2, "L", 1, 2, 25],
            [34, "MOD-1/1", "MOD11", 28, 12, "N", 2, 2, 0],
            [35, "MOD-1/1", "MOD11", 29, 26, "N", 2, 2, 0],
            [36, "MOD-1/1", "MOD11", 30, 24, "N", 2, 2, 0],
            [37, "MOD-1/2", "MOD12", 31, 25, "N", 2, 2, 0],
            [38, "MOD-2/2", "MOD22", 31, 7, "L", 1, 2, 25],
            [39, "MOD-1/1", "MOD11", 32, 2, "N", 2, 2, 0],
            [40, "MOD-1/1", "MOD11", 33, 27, "N", 2, 2, 0],
            [41, "MOD-1/1", "MOD11", 34, 15, "N", 2, 2, 0],
            [42, "MOD-1/1", "MOD11", 35, 9, "N", 2, 2, 0],
            [43, "MOD-1/1", "MOD11", 36, 29, "N", 2, 2, 0],
            [44, "MOD-1/1", "MOD11", 37, 30, "N", 2, 2, 0],
            [45, "MOD-1/1", "MOD11", 38, 28, "N", 2, 2, 0],
            [46, "MOD-1/1", "MOD11", 39, 17, "N", 2, 2, 0],
            [47, "MOD-1/1", "MOD11", 40, 18, "N", 2, 2, 0],
            [48, "MOD-1/1", "MOD11", 41, 32, "N", 2, 2, 0],
            [49, "MOD-1/1", "MOD11", 42, 16, "N", 2, 2, 0],
            [50, "MOD-1/1", "MOD11", 43, 31, "N", 2, 2, 0]
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
        [1, "0120", "INFORMATICA APPLICATA (MACHINE LEARNING E BIG DATA) ", 120, 2],
        [2, "0121", "SCIENZE E TECNOLOGIE DELLA NAVIGAZIONE", 120, 2],
        [3, "0122", "SCIENZE NAUTICHE, AERONAUTICHE E METEO-OCEANOGRAFICHE", 180, 3],
        [4, "0123", "SCIENZE BIOLOGICHE", 180, 3],
        [5, "0124", "INFORMATICA", 180, 3],
        [6, "0125", "CONDUZIONE DEL MEZZO NAVALE", 180, 3],
        [7, "0126", "BIOLOGIA PER LA SOSTENIBILITA'", 120, 2],
        [8, "0332", "INGEGNERIA CIVILE E AMBIENTALE PER LA MITIGAZIONE DEI RISCHI", 180, 3],
        [9, "0326", "INGEGNERIA GESTIONALE", 120, 2],
        [10, "0328", "INGEGNERIA GESTIONALE", 180, 3],
        [11, "0327", "INGEGNERIA INFORMATICA, BIOMEDICA E DELLE TELECOMUNICAZIONI", 180, 3],
        [12, "0330", "INGEGNERIA DELLA SICUREZZA DEI DATI E DELLE COMUNICAZIONI", 120, 2],
        [13, "0331", "INGEGNERIA CIVILE E PER LA TUTELA DELL'AMBIENTE COSTIERO", 120, 2]
    ]
    corsi_di_studio.extend(corsi_di_studio_i)

    attivita_didattiche_i=[
        [1, "A001018", "SCIENTIFIC COMPUTING", 12, "#990000"],
        [2, "A001019", "PHYSICS AND QUANTUM COMPUTING", 6, "#997A00"],
        [3, "A001020", "MACHINE LEARNING", 12, "#009900"],
        [4, "A001027", "COMPUTER GRAPHICS: ANIMATION AND SIMULATION", 6, "#0066FF"],
        [5, "A001022", "HIGH PERFORMANCE COMPUTING", 6, "#800000"],
        [6, "A001024", "INTERNET OF THINGS AND IOT LAB", 12, "#FF6666"],
        [7, "A001025", "MULTIMODAL MACHINE LEARNING", 6, "#999999"],
        [8, "01200008", "APPLICAZIONI DI CALCOLO SCIENTIFICO E LAB. A.C.S.", 12, "#990000"],
        [9, "IT06", "RADAR", 6, "#997A00"],
        [10, "CLIMA", "CLIMATOLOGIA", 6, "#009900"],
        [11, "NAVSAT", "NAVIGAZIONE SATELLITARE", 6, "#0066FF"],
        [12, "TRASP", "TRASPORTO E DIFFUSIONE NELL'OCEANO E NELL'ATMOSFERA", 6, "#800000"],
        [13, "012105", "ECONOMIA ED ORGANIZZAZIONE AZIENDALE", 6, "#FF6666"],
        [14, "A000733", "INFORMATICA DI BASE E LABORATORIO", 6, "#990000"],
        [15, "A001004", "ANALISI MATEMATICA II", 9, "#997A00"],
        [16, "FISI26", "FISICA II CFU 6", 6, "#009900"],
        [17, "0115021", "MATEMATICA E STATISTICA", 9, "#990000"],
        [18, "012301", "CHIMICA GENERALE ED INORGANICA CON LABORATORIO", 9, "#997A00"],
        [19, "01230444", "BIOLOGIA E FISIOLOGIA VEGETALE CON LABORATORIO", 12, "#009900"],
        [20, "01230445", "CITOLOGIA ED ISTOLOGIA CON LABORATORIO", 6, "#0066FF"],
        [21, "012305", "BIOCHIMICA CON LABORATORIO", 9, "#800000"],
        [22, "0115007", "ECOLOGIA", 9, "#FF6666"],
        [23, "012340", "IGIENE", 9, "#999999"],
        [24, "186", "GENETICA", 6, "#99FF99"],
        [25, "ARC12", "ARCHITETTURA DEI CALCOLATORI E LABORATORIO DI ARCHITETTURA DEI CALCOLATORI CFU12", 12, "#990000"],
        [26, "PROGR12", "PROGRAMMAZIONE I E LABORATORIO DI PROGRAMMAZIONE I  CFU 12", 12, "#997A00"],
        [27, "ALGSTD12", "ALGORITMI E STRUTTURE DATI E LABORATORIO DI ALGORITMI E STRUTTURE DATI CFU 12", 12, "#009900"],
        [28, "INFO03", "ECONOMIA E ORGANIZZAZIONE AZIENDALE", 9, "#0066FF"],
        [29, "MATII9", "MATEMATICA II CFU 9", 9, "#800000"],
        [30, "A001195", "INGEGNERIA DEL SOFTWARE E INTERAZIONE UOMO-MACCHINA", 9, "#FF6666"],
        [31, "PRGRIII9", "PROGRAMMAZIONE III E LABORATORIO DI PROGRAMMAZIONE III", 6, "#999999"],
        [32, "RCLRC9", "RETI DI CALCOLATORI E LABORATORIO DI RETI DI CALCOLATORI CFU 9", 9, "#99FF99"],
        [33, "771", "MATEMATICA I", 12, "#660099"],
        [34, "A000984", "TENUTA DELLA GUARDIA E LABORATORIO", 6, "#997A00"],
        [35, "526", "ANALISI MATEMATICA", 9, "#009900"],
        [36, "A000982", "INGLESE TECNICO E LABORATORIO", 6, "#0066FF"],
        [37, "012109", "TECNOLOGIE DELLE COSTRUZIONI ED ALLESTIMENTO NAVALE", 6, "#800000"],
        [38, "A001367", "IGIENE DELL'AMBIENTE E DEL TERRITORIO", 6, "#990000"],
        [39, "A001368", "BIOCHIMICA APPLICATA", 6, "#997A00"],
        [40, "A001369", "ECONOMIA DELL'AMBIENTE ED ECONOMIA CIRCOLARE", 6, "#009900"],
        [41, "A001850", "BIOLOGIA DELLA CONSERVAZIONE II", 9, "#0066FF"],
        [42, "A001376", "ZOOLOGIA APPLICATA", 9, "#800000"],
        [43, "A001053", "CHIMICA E TECNOLOGIE DEI MATERIALI", 9, "#990000"],
        [44, "A001056", "DISEGNO ED ELEMENTI COSTRUTTIVI", 9, "#997A00"],
        [45, "A000562", "MECCANICA RAZIONALE", 9, "#009900"],
        [46, "A000919", "GEOLOGIA", 6, "#0066FF"],
        [47, "A001007", "Statistica applicata alle osservazioni  per la valutazione del rischio", 6, "#800000"],
        [48, "A001006", "ELABORAZIONE DATI CON STRUMENTI INFORMATICI", 6, "#FF6666"],
        [49, "ICL042", "TECNICA DELLE COSTRUZIONI", 9, "#999999"],
        [50, "ICL058", "MECCANICA DELLE TERRE", 9, "#99FF99"],
        [51, "IXL040", "COSTRUZIONI IDRAULICHE", 9, "#660099"],
        [52, "A000438", "Qualità e Sicurezza Elettrica", 12, "#990000"],
        [53, "IGL059", "GESTIONE AZIENDALE", 9, "#990000"],
        [54, "IGL060", "PROBABILITA' E STATISTICA", 9, "#997A00"],
        [55, "IGL043", "ELETTROTECNICA", 9, "#009900"],
        [56, "A000392", "LINGUA INGLESE", 3, "#990000"],
        [57, "INIBIT03", "FONDAMENTI DI INGEGNERIA BIOMEDICA", 9, "#997A00"],
        [58, "ITL051", "INTRODUZIONE AI CIRCUITI", 6, "#009900"],
        [59, "ITL035", "ELETTRONICA", 12, "#0066FF"],
        [60, "ITL038", "PROPAGAZIONE", 6, "#800000"],
        [61, "A000849", "Analisi dei processi aziendali per la gestione del rischio", 6, "#990000"],
        [62, "A000850", "Reti di Telecomunicazioni e Internet", 6, "#997A00"],
        [63, "ICMT080", "PROGETTAZIONE DEI CIRCUITI ELETTRONICI", 9, "#009900"],
        [64, "A000854", "Telerilevamento a Microonde", 9, "#0066FF"],
        [65, "A000893", "Sistemi di comunicazione ed Elaborazione Numerica dei Segnali e laboratorio", 12, "#800000"],
        [66, "A000971", "Sicurezza dei Sistemi Informatici", 9, "#FF6666"],
        [67, "A000991", "DINAMICA DELLE STRUTTURE E INGEGNERIA SISMICA", 9, "#990000"],
        [68, "ICS002", "MATERIALI INNOVATIVI PER L'INGEGNERIA CIVILE", 9, "#997A00"],
        [69, "ICS003", "CARTOGRAFIA NUMERICA E GIS", 9, "#009900"],
        [70, "ICS007", "PROGETTAZIONE DELLE OPERE IDRAULICHE", 9, "#0066FF"],
        [71, "ICS008", "PROGETTAZIONE GEOTECNICA", 9, "#800000"],
        [72, "A000301", "REGIME E PROTEZIONE DEI LITORALI", 9, "#FF6666"],
        [73, "A000998", "MONITORAGGIO E VALUTAZIONI AMBIENTALI DELLE AREE COSTIERE", 9, "#999999"],
        [74, "A000999", "OCEANOGRAFIA COSTIERA", 9, "#99FF99"]
    ]
    attivita_didattiche.extend(attivita_didattiche_i)

    docenti_i=[
        [1, "CF001903", "001903", "MARCELLINO", "LIVIA"],
        [2, "CF002347", "002347", "FERONE", "ALESSIO"],
        [3, "CF001854", "001854", "CAMASTRA", "FRANCESCO"],
        [4, "CF000292", "000292", "RIZZARDI", "MARIAROSARIA"],
        [5, "CF000296", "000296", "GIUNTA", "GIULIO"],
        [6, "CF000768", "000768", "ROTUNDI", "ALESSANDRA"],
        [7, "CF001969", "001969", "CIARAMELLA", "ANGELO"],
        [8, "CF005314", "005314", "DE NINO", "MAURIZIO"],
        [9, "CF001132", "001132", "PREZIOSO", "GIUSEPPINA"],
        [10, "CF001871", "001871", "FERRAIOLI", "GIAMPAOLO"],
        [11, "CF000337", "000337", "ZAMBIANCHI", "ENRICO"],
        [12, "CF001412", "001412", "METALLO", "CONCETTA"],
        [13, "CF001141", "001141", "FUSCO", "GIANNETTA"],
        [14, "CF001708", "001708", "D'ONOFRIO", "LUIGI"],
        [15, "CF002006", "002006", "SALVI", "GIUSEPPE"],
        [16, "CF000716", "000716", "RUSSO", "GIOVANNI, FULVIO"],
        [17, "CF002602", "002602", "DI ONOFRIO", "VALERIA"],
        [18, "CF002138", "002138", "DI DONATO", "PAOLA"],
        [19, "CF002318", "002318", "PASQUALE", "VINCENZO"],
        [20, "CF002159", "002159", "GALLETTI", "ARDELIO"],
        [21, "CF001954", "001954", "OLIVA", "ROMINA"],
        [22, "CF001528", "001528", "CASORIA", "PAOLO"],
        [23, "CF004015", "004015", "SIMONIELLO", "PALMA"],
        [24, "CF001971", "001971", "STAIANO", "ANTONINO"],
        [25, "CF001713", "001713", "MONTELLA", "RAFFAELE"],
        [26, "CF002025", "002025", "VOLZONE", "BRUNO"],
        [27, "CF001535", "001535", "FORMICA", "MARIA ROSARIA"],
        [28, "CF002844", "002844", "PISCOPO", "VINCENZO"],
        [29, "CF001711", "001711", "AMADORI", "ANNA LISA"],
        [30, "CF004663", "004663", "NISCO", "MARIA CRISTINA"],
        [31, "CF002069", "002069", "SANDULLI", "ROBERTO"],
        [32, "CF001136", "001136", "APRILE", "MARIA CARMELA"],
        [33, "CF003479", "003479", "CERONI", "FRANCESCA"],
        [34, "CF001523", "001523", "AVERSA", "STEFANO"],
        [35, "CF001668", "001668", "DELLA MORTE", "RENATA"],
        [36, "CF005536", "005536", "LUCIANO", "RAIMONDO"],
        [37, "CF002070", "002070", "PAPPONE", "GERARDO"],
        [38, "CF001692", "001692", "ROBUSTELLI", "UMBERTO"],
        [39, "CF002331", "002331", "D'ANTONIO", "SALVATORE"],
        [40, "CF002610", "002610", "FERONE", "CLAUDIO"],
        [41, "CF001670", "001670", "CIOFFI", "RAFFAELE"],
        [42, "CF001733", "001733", "MAGLIOCCOLA", "FRANCESCO"],
        [43, "CF002315", "002315", "CARAMIA", "PIERLUIGI"],
        [44, "CF002155", "002155", "BRACALE", "ANTONIO"],
        [45, "CF004809", "004809", "CERCHIONE", "ROBERTO"],
        [46, "CF000286", "000286", "PASCAZIO", "VITO"],
        [47, "CF006981", "006981", "DE MAGISTRIS", "MASSIMILIANO"],
        [48, "CF002191", "002191", "BASELICE", "FABIO"],
        [49, "CF001935", "001935", "IADICICCO", "AGOSTINO"],
        [50, "CF001870", "001870", "NUNZIATA", "FERDINANDO"],
        [51, "CF000288", "000288", "MIGLIACCIO", "MAURIZIO"],
        [52, "CF001763", "001763", "NAPOLITANO", "ANTONIO"],
        [53, "CF002306", "002306", "SCHIRINZI", "GILDA"],
        [54, "CF001347", "001347", "ROMANO", "LUIGI"],
        [55, "CF002270", "002270", "THOMAS", "ANTONIO"],
        [56, "CF001669", "001669", "BUDILLON", "ALESSANDRA"],
        [57, "CF001875", "001875", "CAMPOPIANO", "STEFANIA"],
        [58, "CF002052", "002052", "COZZOLINO", "LUCA"],
        [59, "CF002365", "002365", "DE SANCTIS", "LUCA"],
        [60, "CF000359", "000359", "BENASSAI", "GUIDO"],
        [61, "CF001878", "001878", "LEGA", "MASSIMILIANO"],
        [62, "CF002963", "002963", "DE RUGGIERO", "PAOLA"],
        [63, "CF002962", "002962", "CASTAGNO", "PASQUALE"],
        [64, "CF001936", "001936", "CATERINO", "NICOLA"],
        [65, "CF001939", "001939", "COLANGELO", "FRANCESCO"]
    ]
    docenti.extend(docenti_i)

    offerta_i=[
        [1, 1, 1, 1, 4, 1, 1, 30],
        [2, 1, 1, 2, 6, 1, 1, 30],
        [3, 1, 1, 3, 3, 1, 1, 30],
        [4, 1, 1, 4, 8, 1, 1, 30],
        [5, 1, 1, 5, 1, 2, 1, 15],
        [6, 1, 1, 6, 2, 2, 1, 15],
        [7, 1, 1, 7, 3, 2, 1, 15],
        [8, 1, 2, 8, 4, 1, 1, 40],
        [9, 1, 2, 9, 10, 1, 1, 40],
        [10, 1, 2, 10, 13, 1, 1, 40],
        [11, 1, 2, 11, 9, 2, 1, 20],
        [12, 1, 2, 12, 11, 2, 1, 20],
        [13, 1, 2, 13, 12, 2, 1, 20],
        [14, 1, 3, 14, 15, 1, 1, 50],
        [15, 1, 3, 15, 14, 2, 1, 30],
        [16, 1, 3, 16, 6, 2, 1, 30],
        [17, 1, 4, 17, 20, 1, 1, 60],
        [18, 1, 4, 18, 21, 1, 1, 60],
        [19, 1, 4, 19, 22, 1, 1, 60],
        [20, 1, 4, 20, 23, 1, 1, 60],
        [21, 1, 4, 21, 18, 2, 1, 45],
        [22, 1, 4, 22, 16, 3, 1, 25],
        [23, 1, 4, 23, 17, 3, 1, 25],
        [24, 1, 4, 24, 19, 3, 1, 25],
        [25, 1, 5, 25, 15, 1, 1, 100],
        [26, 1, 5, 26, 7, 1, 1, 100],
        [27, 1, 5, 27, 3, 2, 1, 70],
        [28, 1, 5, 28, 12, 2, 1, 70],
        [29, 1, 5, 29, 26, 2, 1, 70],
        [30, 1, 5, 30, 24, 3, 1, 50],
        [31, 1, 5, 31, 25, 3, 1, 50],
        [32, 1, 5, 32, 2, 3, 1, 50],
        [33, 1, 5, 33, 27, 1, 1, 100],
        [34, 1, 6, 14, 15, 2, 1, 20],
        [35, 1, 6, 34, 9, 1, 1, 40],
        [36, 1, 6, 35, 29, 1, 1, 40],
        [37, 1, 6, 36, 30, 1, 1, 40],
        [38, 1, 6, 37, 28, 2, 1, 20],
        [39, 1, 7, 38, 17, 1, 1, 50],
        [40, 1, 7, 39, 18, 1, 1, 50],
        [41, 1, 7, 40, 32, 1, 1, 50],
        [42, 1, 7, 41, 16, 1, 1, 50],
        [43, 1, 7, 42, 31, 2, 1, 30],
        [44, 1, 8, 43, 40, 1, 1, 30],
        [45, 1, 8, 44, 42, 1, 1, 30],
        [46, 1, 8, 45, 36, 2, 1, 30],
        [47, 1, 8, 46, 37, 2, 1, 30],
        [48, 1, 8, 47, 38, 2, 1, 30],
        [49, 1, 8, 48, 39, 2, 1, 30],
        [50, 1, 8, 49, 33, 3, 1, 20],
        [51, 1, 8, 50, 34, 3, 1, 20],
        [52, 1, 8, 51, 35, 3, 1, 20],
        [53, 1, 9, 52, 43, 2, 1, 45],
        [54, 1, 10, 53, 45, 2, 1, 40],
        [55, 1, 10, 54, 46, 2, 1, 4],
        [56, 1, 10, 55, 47, 2, 1, 4],
        [57, 1, 11, 56, 30, 1, 1, 40],
        [58, 1, 11, 57, 48, 2, 1, 35],
        [59, 1, 11, 58, 47, 2, 1, 35],
        [60, 1, 11, 59, 49, 3, 1, 30],
        [61, 1, 11, 60, 50, 3, 1, 30],
        [62, 1, 12, 61, 55, 1, 1, 45],
        [63, 1, 12, 62, 56, 1, 1, 45],
        [64, 1, 12, 63, 57, 1, 1, 45],
        [65, 1, 12, 64, 51, 2, 1, 30],
        [66, 1, 12, 65, 52, 2, 1, 30],
        [67, 1, 12, 66, 54, 2, 1, 30],
        [68, 1, 13, 67, 64, 1, 1, 35],
        [69, 1, 13, 68, 65, 1, 1, 35],
        [70, 1, 13, 69, 38, 1, 1, 35],
        [71, 1, 13, 70, 35, 2, 1, 20],
        [72, 1, 13, 71, 59, 2, 1, 20],
        [73, 1, 13, 72, 60, 2, 1, 20],
        [74, 1, 13, 73, 61, 2, 1, 20],
        [75, 1, 13, 74, 62, 2, 1, 20]
    ]
    offerta.extend(offerta_i)

    if tipoModuli == "1":
        modulo_i=[
            [1, "MOD-1", "MOD-1", 1, 4, "N", 2, 2, 0],
            [2, "MOD-1", "MOD-1", 2, 6, "N", 2, 2, 0],
            [3, "MOD-1", "MOD-1", 3, 3, "N", 2, 2, 0],
            [4, "MOD-1", "MOD-1", 4, 8, "N", 2, 2, 0],
            [5, "MOD-1", "MOD-1", 5, 1, "N", 2, 2, 0],
            [6, "MOD-1", "MOD-1", 6, 2, "N", 2, 2, 0],
            [7, "MOD-1", "MOD-1", 7, 3, "N", 2, 2, 0],
            [8, "MOD-1", "MOD-1", 8, 4, "N", 2, 2, 0],
            [9, "MOD-1", "MOD-1", 9, 10, "N", 2, 2, 0],
            [10, "MOD-1", "MOD-1", 10, 13, "N", 2, 2, 0],
            [11, "MOD-1", "MOD-1", 11, 9, "N", 2, 2, 0],
            [12, "MOD-1", "MOD-1", 12, 11, "N", 2, 2, 0],
            [13, "MOD-1", "MOD-1", 13, 12, "N", 2, 2, 0],
            [14, "MOD-1", "MOD-1", 14, 15, "N", 2, 2, 0],
            [15, "MOD-1", "MOD-1", 15, 14, "N", 2, 2, 0],
            [16, "MOD-1", "MOD-1", 16, 6, "N", 2, 2, 0],
            [17, "MOD-1", "MOD-1", 17, 20, "N", 2, 2, 0],
            [18, "MOD-1", "MOD-1", 18, 21, "N", 2, 2, 0],
            [19, "MOD-1", "MOD-1", 19, 22, "N", 2, 2, 0],
            [20, "MOD-1", "MOD-1", 20, 23, "N", 2, 2, 0],
            [21, "MOD-1", "MOD-1", 21, 18, "N", 2, 2, 0],
            [22, "MOD-1", "MOD-1", 22, 16, "N", 2, 2, 0],
            [23, "MOD-1", "MOD-1", 23, 17, "N", 2, 2, 0],
            [24, "MOD-1", "MOD-1", 24, 19, "N", 2, 2, 0],
            [25, "MOD-1", "MOD-1", 25, 15, "N", 2, 2, 0],
            [26, "MOD-1", "MOD-1", 26, 7, "N", 2, 2, 0],
            [27, "MOD-1", "MOD-1", 27, 3, "N", 2, 2, 0],
            [28, "MOD-1", "MOD-1", 28, 12, "N", 2, 2, 0],
            [29, "MOD-1", "MOD-1", 29, 26, "N", 2, 2, 0],
            [30, "MOD-1", "MOD-1", 30, 24, "N", 2, 2, 0],
            [31, "MOD-1", "MOD-1", 31, 25, "N", 2, 2, 0],
            [32, "MOD-1", "MOD-1", 32, 2, "N", 2, 2, 0],
            [33, "MOD-1", "MOD-1", 33, 27, "N", 2, 2, 0],
            [34, "MOD-1", "MOD-1", 34, 15, "N", 2, 2, 0],
            [35, "MOD-1", "MOD-1", 35, 9, "N", 2, 2, 0],
            [36, "MOD-1", "MOD-1", 36, 29, "N", 2, 2, 0],
            [37, "MOD-1", "MOD-1", 37, 30, "N", 2, 2, 0],
            [38, "MOD-1", "MOD-1", 38, 28, "N", 2, 2, 0],
            [39, "MOD-1", "MOD-1", 39, 17, "N", 2, 2, 0],
            [40, "MOD-1", "MOD-1", 40, 18, "N", 2, 2, 0],
            [41, "MOD-1", "MOD-1", 41, 32, "N", 2, 2, 0],
            [42, "MOD-1", "MOD-1", 42, 16, "N", 2, 2, 0],
            [43, "MOD-1", "MOD-1", 43, 31, "N", 2, 2, 0],
            [44, "MOD-1", "MOD-1", 44, 40, "N", 2, 2, 0],
            [45, "MOD-1", "MOD-1", 45, 42, "N", 2, 2, 0],
            [46, "MOD-1", "MOD-1", 46, 36, "N", 2, 2, 0],
            [47, "MOD-1", "MOD-1", 47, 37, "N", 2, 2, 0],
            [48, "MOD-1", "MOD-1", 48, 38, "N", 2, 2, 0],
            [49, "MOD-1", "MOD-1", 49, 39, "N", 2, 2, 0],
            [50, "MOD-1", "MOD-1", 50, 33, "N", 2, 2, 0],
            [51, "MOD-1", "MOD-1", 51, 34, "N", 2, 2, 0],
            [52, "MOD-1", "MOD-1", 52, 35, "N", 2, 2, 0],
            [53, "MOD-1", "MOD-1", 53, 43, "N", 2, 2, 0],
            [54, "MOD-1", "MOD-1", 54, 45, "N", 2, 2, 0],
            [55, "MOD-1", "MOD-1", 55, 46, "N", 2, 2, 0],
            [56, "MOD-1", "MOD-1", 56, 47, "N", 2, 2, 0],
            [57, "MOD-1", "MOD-1", 57, 30, "N", 2, 2, 0],
            [58, "MOD-1", "MOD-1", 58, 48, "N", 2, 2, 0],
            [59, "MOD-1", "MOD-1", 59, 47, "N", 2, 2, 0],
            [60, "MOD-1", "MOD-1", 60, 49, "N", 2, 2, 0],
            [61, "MOD-1", "MOD-1", 61, 50, "N", 2, 2, 0],
            [62, "MOD-1", "MOD-1", 62, 55, "N", 2, 2, 0],
            [63, "MOD-1", "MOD-1", 63, 56, "N", 2, 2, 0],
            [64, "MOD-1", "MOD-1", 64, 57, "N", 2, 2, 0],
            [65, "MOD-1", "MOD-1", 65, 51, "N", 2, 2, 0],
            [66, "MOD-1", "MOD-1", 66, 52, "N", 2, 2, 0],
            [67, "MOD-1", "MOD-1", 67, 54, "N", 2, 2, 0],
            [68, "MOD-1", "MOD-1", 68, 64, "N", 2, 2, 0],
            [69, "MOD-1", "MOD-1", 69, 65, "N", 2, 2, 0],
            [70, "MOD-1", "MOD-1", 70, 38, "N", 2, 2, 0],
            [71, "MOD-1", "MOD-1", 71, 35, "N", 2, 2, 0],
            [72, "MOD-1", "MOD-1", 72, 59, "N", 2, 2, 0],
            [73, "MOD-1", "MOD-1", 73, 60, "N", 2, 2, 0],
            [74, "MOD-1", "MOD-1", 74, 61, "N", 2, 2, 0],
            [75, "MOD-1", "MOD-1", 75, 62, "N", 2, 2, 0],
        ]
    elif tipoModuli == "N":
        modulo_i = [
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
                    row = CorsoDiStudio(id=c[0],
                                        codice=c[1],
                                        descrizione=c[2],
                                        cfu=c[3],
                                        durata_legale=c[4])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dei corsi", "danger")

        if attivita_didattiche is not None:
            try:
                for a in attivita_didattiche:
                    row = AttivitaDidattica(id=a[0],
                                            codice=a[1],
                                            descrizione=a[2],
                                            cfu=a[3],
                                            colore=a[4])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento delle attività didattiche", "danger")

        if docenti is not None:
            try:
                for d in docenti:
                    row = Docente(id=d[0],
                                  codice_fiscale=d[2],
                                  matricola=d[2],
                                  cognome=d[3],
                                  nome=d[4])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dei docenti", "danger")

        if offerta is not None:
            try:
                for o in offerta:
                    row = Offerta(id=o[0],
                                  anno_accademico_id=o[1],
                                  corso_di_studio_id=o[2],
                                  attivita_didattica_id=o[3],
                                  docente_id=o[4],
                                  anno_di_corso=o[5],
                                  semestre=o[6],
                                  max_studenti=o[7])
                    db.session.add(row)
                db.session.flush()
            except:
                flash("Errore di caricamento dell'offerta", "danger")

        if moduli is not None:
            try:
                for m in moduli:
                    row = Modulo(id=m[0],
                                 codice=m[1],
                                 descrizione=m[2],
                                 offerta_id=m[3],
                                 docente_id=m[4],
                                 tipo_aula=m[5],
                                 numero_sessioni=m[6],
                                 durata_sessioni=m[7],
                                 max_studenti=m[8])
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


def caricaDatiDalDb(aa, semestre, cod_cds):
    try:
        corsi_tt=[]
        if cod_cds == -1:
            corsi = db.session.query(CorsoDiStudio).all()
        else:
            corsi = db.session.query(CorsoDiStudio).filter(CorsoDiStudio.id == cod_cds).all()
        for c in corsi:
            corsi_tt.append(CorsoDiStudioTt(c.id, c.codice, c.descrizione, c.cfu, c.durata_legale))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Corsi di studio", "danger")
        return -1   
    
    try:
        giorni_tt = []
        giorni = db.session.query(Giorno).all()
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
        if cod_cds == -1:
            moduli=db.session.query(Modulo, Offerta, AttivitaDidattica, AnnoAccademico, CorsoDiStudio, Docente)\
            .join(Offerta, Modulo.offerta_id == Offerta.id)\
            .join(AttivitaDidattica, Offerta.attivita_didattica_id == AttivitaDidattica.id)\
            .join(CorsoDiStudio, Offerta.corso_di_studio_id == CorsoDiStudio.id)\
            .join(AnnoAccademico, Offerta.anno_accademico_id == AnnoAccademico.id)\
            .join(Docente, Offerta.docente_id == Docente.id)\
            .filter(Offerta.anno_accademico_id == aa)\
            .filter(Offerta.semestre == semestre).all()
        else:
            moduli = db.session.query(Modulo, Offerta, AttivitaDidattica, AnnoAccademico, CorsoDiStudio, Docente) \
            .join(Offerta, Modulo.offerta_id == Offerta.id) \
            .join(AttivitaDidattica, Offerta.attivita_didattica_id == AttivitaDidattica.id) \
            .join(CorsoDiStudio, Offerta.corso_di_studio_id == CorsoDiStudio.id) \
            .join(AnnoAccademico, Offerta.anno_accademico_id == AnnoAccademico.id) \
            .join(Docente, Offerta.docente_id == Docente.id) \
            .filter(Offerta.anno_accademico_id == aa) \
            .filter(CorsoDiStudio.id == cod_cds) \
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
            "capienza_aula": int(r.Aula.capienza),
            "docente_id": int(r.Docente.id)}

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


