from .models import AnnoAccademico, CorsoDiStudio, AttivitaDidattica, \
    Docente, Aula, Offerta, LogisticaDocente, Modulo, Giorno, Slot, \
    OrarioTestata, OrarioDettaglio, Orario, StatoOrario
from .import appbuilder, db
from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from .solver_models import ModuloTt, AulaTt, CorsoDiStudioTt, SlotTt, GiornoTt

colori = {
    1:"#FF0000",
    2:"#4169E1",
    3:"#228B22",
    4:"#FFD800",
    5:"#993300"
}

giorni = []
slot = []
anni_accademici = []
corsi_di_studio = []
attivita_didattiche = []
aule = []
docenti = []
offerta = [] 
moduli = [] 
logistica_docenti = []
   
def __svuotaTabelle():
    db.session.query(OrarioDettaglio).delete()
    db.session.query(OrarioTestata).delete()
    db.session.query(Orario).delete()
    db.session.query(LogisticaDocente).delete()
    db.session.query(Modulo).delete()
    db.session.query(Offerta).delete()
    db.session.query(CorsoDiStudio).delete()
    db.session.query(AttivitaDidattica).delete()
    db.session.query(Docente).delete()
    db.session.query(Giorno).delete()
    db.session.query(AnnoAccademico).delete()
    db.session.query(Slot).delete()
    db.session.query(Aula).delete()
       
    db.session.execute('ALTER TABLE modulo AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE offerta AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE corso_di_studio AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE attivita_didattica AUTO_INCREMENT = 1')   
    db.session.execute('ALTER TABLE docente AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE giorno AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE anno_accademico AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE slot AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE aula AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE logistica_docente AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE orario AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE orario_testata AUTO_INCREMENT = 1')
    db.session.execute('ALTER TABLE orario_dettaglio AUTO_INCREMENT = 1')
    db.session.commit()
    
def __impostaDatiIniziali():
    giorni_i = ['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì']
    giorni.extend(giorni_i)
    
    slot_i = ['09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00',
            '14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00']
    slot.extend(slot_i)
    
    anni_accademici_i = [
        [2018,'2018-19'],
        [2019,'2019-20'],
        [2020,'2020-21'],
        [2021,'2021-22']
    ]
    anni_accademici.extend(anni_accademici_i)
    
    corsi_di_studio_i = [
        ['A08','INFORMATICA',180,3],
        ['A09','INFORMATICA APPLICATA',120,2],
        ['A10','SCIENZE BIOLOGICHE',180,3]
    ]
    corsi_di_studio.extend(corsi_di_studio_i)

    aule_i = [
        ['AN1','Aula 1',150,'N'],
        ['AN2','Aula 2',100,'N'],
        ['AN3','Aula 3',70,'N'],
        ['AN4','Aula 4',50,'N'],
        ['AN5','Aula 5',35,'N'],
        ['AN6','Aula 6',35,'N'],
        ['AN7','Aula 7',150,'N'],
        ['AL1','Aula LAB1',50,'L'],
        ['AL2','Aula LAB2',40,'L'],
        ['AL3','Aula LAB3',35,'L']
    ]
    aule.extend(aule_i)

    attivita_didattiche_i = [ 
        # PRIMO SEMESTRE INFORMATICA
        ['MAT1-1S','Matematica 1',9,'#E0FFFF'],
        ['ARCL','Architettura dei calcolatori e Laboratorio',12,'#FFFFE0'],
        ['PG1L','Programmazione 1 e Laboratorio',12,'#E6E6FA'],
        ['MAT2','Matematica 2',6,'#D8BFD8'],
        ['ECOA','Economia ed organizzazione aziendale',6,'#7FFFD4'],
        ['ASDL','Algoritmi e strutture dati e Laboratorio',12,'#FFA07A'],
        ['PG3L','Programmazione 3 e Laboratorio',9,'#E0FFFF'],
        ['RETL','Reti di calcolatori e Laboratorio',9,'#FFE4C4'],
        ['GISL','Sistemi informativi geografici e Laboratorio',6,'#F5F5F5'],
        # PRIMO SEMESTRE INFORMATICA APPLICATA
        ['SCCP-1S','Scientific computer',6,'#E0FFFF'],
        ['PHQU','Physic and Quantum',6,'#FFFFE0'],
        ['MACL-1S','Machine Learning',6,'#E6E6FA'],
        ['CPGR','Computer Graphics',6,'#D8BFD8'],
        ['HPCP','High Performance Computing',6,'#7FFFD4'],
        ['MMLE','Multimodal Machine Learning',6,'#FFA07A'],
        ['IOTH-1S','Internet of Things',6,'#E0FFFF'],
        # SECONDO SEMESTRE INFORMATICA
        ['LING','Lingua Inglese',3,'#E0FFFF'],
        ['MAT1-2S','Matematica 1',9,'#FFFFE0'],
        ['PG2L','Programmazione 2 e Laboratorio',12,'#E6E6FA'],
        ['FISI','Fisica',6,'#D8BFD8'],
        ['BASD','Base di dati e Laboratorio',9,'#7FFFD4'],
        ['SISO','Sistemi operativi e Laboratorio',12,'#FFA07A'],
        ['CNUM','Calcolo numerico',6,'#E0FFFF'],
        ['CPAR','Calcolo parallelo',9,'#FFE4C4'],
        ['ELAB','Elaborazione delle immagini',6,'#F5F5F5'],
        # SECONDO SEMESTRE INFORMATICA APPLICATA
        ['SCCP-2S','Scientific Computing PII',12,'#E0FFFF'],
        ['ITSP','Intelligent Signal Processing',12,'#FFFFE0'],
        ['MACL-2S','Machine Learning PII',12,'#E6E6FA'],
        ['DSTC','Data Science Technology',12,'#D8BFD8'],
        ['CLCP','Cloud Computing',12,'#7FFFD4'],
        ['IOTH-2S','Internet of Things PII',12,'#FFA07A'],
        # SECONDO SEMESTRE SCIENZE BIOLOGICHE
        ['BIOA','Biologia animale',3,'#E0FFFF'],
        ['BFVE','Biologia e Fisiologia vegetale',9,'#FFFFE0'],
        ['CHOR','Chimica organica e laboratorio',12,'#E6E6FA'],
        ['FISC','Fisica e laboratorio',6,'#D8BFD8'],
        ['MICB','Microbiologia e laboratorio',9,'#7FFFD4'],
        ['INDB','Indicatori biologici',12,'#FFA07A'],
        ['BFAN','Biologia e fisiologia animale',6,'#E0FFFF'],
        ['ACVI','Analisi ciclo di vita',9,'#FFE4C4'],
        ['FTOS','Farmacologia e tossicologia',6,'#F5F5F5']
    ]
    attivita_didattiche.extend(attivita_didattiche_i)

    docenti_i = [
        ['DNFLGU76D11F839P','DOC001','D\'Onofrio','Luigi'],
        ['MNTRFL76D11F839P','DOC002','Montella','Raffaele'],
        ['SLVGPP76D11F839P','DOC003','Salvi','Giuseppe'],
        ['GNTGLU76D11F839P','DOC004','Giunta','Giulio'],
        ['CRMNGL76D11F839P','DOC005','Ciaramella','Angelo'],
        ['VLZBRN76D11F839P','DOC006','Volzone','Bruno'],
        ['MTLCNT76D11F839P','DOC007','Metallo','Concetta'],
        ['CMTFRN76D11F839P','DOC008','Camastra','Francesco'],
        ['SCFRTO76D11F839P','DOC009','Scafuri','Umberto'],
        ['PRNCLD76D11F839P','DOC010','Parente','Claudio'],
        ['RTNLSS76D11F839P','DOC011','Rotundi','Alessandra'],
        ['DNNMRZ76D11F839P','DOC012','De Nino','Maurizio'],
        ['MRCLVA76D11F839P','DOC013','Marcellino','Livia'],
        ['DCPMHL76D11F839P','DOC014','Di Capua','Michele'],    
        ['RIZMRS76D11F839P','DOC015','Rizzardi','MariaRosaria'],
        ['MRTNTN76D11F839P','DOC016','Maratea','Antonio'],
        ['CSTNLL76D11F839P','DOC017','Castiglione','Aniello'],
        ['STNNTN76D11F839P','DOC018','Staiano','Antonino'],
        ['DMRMLI76D11F839P','DOC019','Di Martino','Emilia'],
        ['FRNLSS76D11F839P','DOC020','Ferone','Alessio'],
        ['MRCLVA76D11F839P','DOC021','Sandulli','Roberto'],
        ['DCPMHL76D11F839P','DOC022','Casoria','Paolo'],    
        ['RIZMRS76D11F839P','DOC023','Chianese','Elena'],
        ['MRTNTN76D11F839P','DOC024','Riccio','Angelo'],
        ['CSTNLL76D11F839P','DOC025','Pasquale','Vincenzo'],
        ['STNNTN76D11F839P','DOC026','Dumoulet','Stefano'],
        ['DMRMLI76D11F839P','DOC027','Franzese','Pier Paolo'],
        ['FRNLSS76D11F839P','DOC028','Mazzeo','Giovanni']
    ]
    docenti.extend(docenti_i)
    
    offerta_i = [
        # PRIMO SEMESTRE INFORMATICA
        [4, 1, 1, 1, 1, 1, 130],
        [4, 1, 2, 2, 1, 1, 130],
        [4, 1, 3, 4, 1, 1, 130],
        [4, 1, 4, 6, 2, 1, 90],
        [4, 1, 5, 7, 2, 1, 90],
        [4, 1, 6, 3, 2, 1, 90],
        [4, 1, 7, 5, 3, 1, 60],
        [4, 1, 8, 9, 3, 1, 60],
        [4, 1, 9, 10, 3, 1, 60],
        # PRIMO SEMESTRE INFORMATICA APPLICATA
        [4, 2, 10, 4, 1, 1, 70],
        [4, 2, 11, 11, 1, 1, 70],
        [4, 2, 12, 8, 1, 1, 70],
        [4, 2, 13, 12, 2, 1, 70],
        [4, 2, 14, 13, 2, 1, 35],
        [4, 2, 15, 8, 2, 1, 35],
        [4, 2, 16, 14, 2, 1, 35],
        # SECONDO SEMESTRE INFORMATICA
        [4, 1, 17, 19, 1, 2, 130],
        [4, 1, 18, 1, 1, 2, 130],
        [4, 1, 19, 15, 1, 2, 130],
        [4, 1, 20, 11, 2, 2, 90],
        [4, 1, 21, 16, 2, 2, 90],
        [4, 1, 22, 17, 2, 2, 90],
        [4, 1, 23, 4, 3, 2, 60],
        [4, 1, 24, 13, 3, 2, 60],
        [4, 1, 25, 18, 3, 2, 60],
        # SECONDO SEMESTRE INFORMATICA APPLICATA
        [4, 2, 26, 15, 1, 2, 70],
        [4, 2, 28, 5, 1, 2, 70],
        [4, 2, 27, 5, 1, 2, 70],
        [4, 2, 29, 16, 1, 2, 70],
        [4, 2, 30, 2, 2, 2, 35],
        [4, 2, 31, 20, 2, 2, 35],
        # SECONDO SEMESTRE SCIENZE BIOLOGICHE
        [4, 3, 32, 21, 1, 2, 100],
        [4, 3, 33, 22, 1, 2, 100],
        [4, 3, 34, 23, 1, 2, 100],
        [4, 3, 35, 24, 1, 2, 100],
        [4, 3, 36, 25, 2, 2, 50],
        [4, 3, 37, 26, 2, 2, 50],
        [4, 3, 38, 21, 2, 2, 50],
        [4, 3, 39, 27, 3, 2, 40],
        [4, 3, 40, 28, 3, 2, 40],
    ]
    offerta.extend(offerta_i)
        
    moduli_i = [
        # PRIMO SEMESTRE INFORMATICA
        ['MU','Teoria',1,1,'N',4,3,0],
        ['MT','Teoria',2,2,'N',2,2,0],
        ['ML','Laboratorio',2,3,'L',2,2,50],
        ['MU','Teoria',3,4,'N',2,2,0],
        ['ML','Laboratorio',3,5,'L',2,2,50],
        ['MU','Teoria',4,6,'N',3,2,0],
        ['MU','Teoria',5,7,'N',2,4,0],
        ['MU','Teoria',6,3,'N',2,2,0],
        ['ML','Laboratorio',6,7,'L',2,2,35],
        ['MU','Teoria',7,5,'N',1,2,0],
        ['ML','Laboratorio',7,2,'L',1,2,35],   
        ['MU','Teoria',8,9,'N',3,2,0],
        ['MU','Teoria',9,10,'N',2,2,0],
        ['ML','Laboratorio',9,10,'L',1,2,35],      
        # PRIMO SEMESTRE INFORMATICA APPLICATA
        ['MU','Teoria',10,4,'N',2,2,0],
        ['MU','Teoria',11,11,'N',2,2,0],
        ['MU','Teoria',12,8,'N',2,2,0],
        ['MU','Teoria',13,12,'N',2,2,0],
        ['MU','Teoria',14,13,'N',2,2,0],
        ['MU','Teoria',15,8,'N',2,2,0],
        ['MU','Teoria',16,14,'N',2,2,0],
        # SECONDO SEMESTRE INFORMATICA
        ['MU','Teoria',17,19,'N',2,2,0],
        ['MU','Teoria',18,18,'N',2,2,0],
        ['MU','Teoria',19,15,'N',1,2,0],        
        ['ML','Laboratorio',19,15,'L',2,2,50],
        ['MU','Teoria',20,11,'N',2,2,0],
        ['MU','Teoria',21,16,'N',1,2,0],        
        ['ML','Laboratorio',21,16,'L',2,2,50],
        ['MU','Teoria',22,17,'N',1,2,0],
        ['ML','Laboratorio',22,18,'L',2,2,50],
        ['MU','Teoria',23,4,'N',2,2,0],       
        ['MU','Teoria',24,13,'N',2,2,0],
        ['MU','Teoria',25,18,'N',2,2,0],
        # SECONDO SEMESTRE INFORMATICA APPLICATA
        ['MU','Teoria',26,15,'N',2,2,0],
        ['MU','Teoria',27,5,'N',2,2,0],
        ['MU','Teoria',28,5,'N',2,2,0],
        ['MU','Teoria',29,16,'N',2,2,0],
        ['MU','Teoria',30,2,'N',2,2,0],
        ['MU','Teoria',31,20,'N',2,2,0],
        # SECONDO SEMESTRE SCIENZE BIOLOGICHE
        ['MU','Teoria',32,21,'N',2,2,0],
        ['MU','Teoria',33,22,'N',2,2,0],
        ['MU','Teoria',34,23,'N',2,2,0],
        ['MU','Teoria',35,24,'N',2,2,0],
        ['MU','Teoria',36,25,'N',2,2,0],
        ['MU','Teoria',37,26,'N',2,2,0],
        ['MU','Teoria',38,21,'N',2,2,0],
        ['MU','Teoria',39,27,'N',2,2,0],
        ['MU','Teoria',40,28,'N',2,2,0]
    ]    
    moduli.extend(moduli_i)
    
    logistica_docenti_i=[]
    logistica_docenti.extend(logistica_docenti_i)
                   
def __registraDatiInDb():
    try:
        for g in giorni:
            row = Giorno(descrizione=g)
            db.session.add(row)
        db.session.flush()

        for s in slot:
            row = Slot(descrizione=s)
            db.session.add(row)
        db.session.flush()

        for a in anni_accademici:
            row = AnnoAccademico(anno = a[0],
                                 anno_esteso = a[1])
            db.session.add(row)
        db.session.flush()

        for c in corsi_di_studio:
            row = CorsoDiStudio(codice = c[0],
                                descrizione = c[1],
                                cfu = c[2],
                                durata_legale = c[3])
            db.session.add(row)
        db.session.flush()

        for a in attivita_didattiche:
            row = AttivitaDidattica(codice = a[0],
                                    descrizione = a[1],
                                    cfu = a[2],
                                    colore = a[3])
            db.session.add(row)
        db.session.flush()

        for a in aule:
            row = Aula(codice = a[0],
                       descrizione = a[1],
                       capienza = a[2],
                       tipo_aula = a[3])
            db.session.add(row)
        db.session.flush()

        for d in docenti:
            row = Docente(codice_fiscale = d[0],
                          matricola = d[1],
                          cognome = d[2],
                          nome = d[3])
            db.session.add(row)
        db.session.flush()

        for o in offerta:
            row = Offerta(anno_accademico_id = o[0],
                          corso_di_studio_id = o[1],
                          attivita_didattica_id = o[2],
                          docente_id = o[3],
                          anno_di_corso = o[4],
                          semestre = o[5],
                          max_studenti = o[6])
            db.session.add(row)
        db.session.flush()

        for m in moduli:
            row = Modulo(codice = m[0],
                         descrizione = m[1],
                         offerta_id = m[2],
                         docente_id = m[3],
                         tipo_aula = m[4],
                         numero_sessioni = m[5],
                         durata_sessioni = m[6],
                         max_studenti = m[7])
            db.session.add(row)
        db.session.flush()

        for l in logistica_docenti:
            row = LogisticaDocente(offerta_id = l[0],
                                   modulo_id = l[1],
                                   slot_id = l[2],
                                   giorno_id = l[3])
            db.session.add(row)
        db.session.flush()

        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("Errore di caricamento dati nel DB")
    return -1

def inizializzaDb():
    try:
        __svuotaTabelle()
        __impostaDatiIniziali()
        __registraDatiInDb()
        return 0
    except SQLAlchemyError:
        return -1

def svuotaDb():
    try:
        __svuotaTabelle()
        return 0
    except SQLAlchemyError:
        return -1

def caricaDatiDalDb(aa, semestre):
    try:
        corsi_tt=[]
        corsi=db.session.query(CorsoDiStudio).all()
        for c in corsi:
            corsi_tt.append(CorsoDiStudioTt(c.id, c.codice, c.descrizione, c.cfu, c.durata_legale))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Corsi di studio")
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
        # Recupero delle informazioni dal DB per la formazione degli oggetti Modulo da collocare nell'orario
        moduli=db.session.query(Modulo, Offerta, AttivitaDidattica, AnnoAccademico, CorsoDiStudio, Docente)\
        .join(Offerta, Modulo.offerta_id==Offerta.id)\
        .join(AttivitaDidattica, Offerta.attivita_didattica_id==AttivitaDidattica.id)\
        .join(CorsoDiStudio, Offerta.corso_di_studio_id==CorsoDiStudio.id)\
        .join(AnnoAccademico, Offerta.anno_accademico_id==AnnoAccademico.id)\
        .join(Docente, Offerta.docente_id==Docente.id)\
        .filter(AnnoAccademico.id==aa)\
        .filter(Offerta.semestre==semestre).all()   
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
        flash("Errore di caricamento dati LP -> Aule")
        return -1    
    
    return corsi_tt, giorni_tt, slot_tt, aule_tt, moduli_tt, logistica_tt

def getColori():
    return colori

def inizializza_db():
    try:
        db.session.query(StatoOrario).delete()
        db.session.execute('ALTER TABLE stato_orario AUTO_INCREMENT = 1')
        row = StatoOrario(codice='P', descrizione='Pubblicato')
        db.session.add(row)
        row = StatoOrario(codice='B', descrizione='Bozza')
        db.session.add(row)
        db.session.commit()
    except SQLAlchemyError:
        flash("Errore di inizializzazione del db")
        return -1