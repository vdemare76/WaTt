from .models import AnnoAccademico, CorsoDiStudio, AttivitaDidattica, Docente, Aula, Offerta, LogisticaDocente, Modulo, Giorno, Slot
from .import appbuilder, db
from flask import flash
from sqlalchemy import engine, MetaData, select
from sqlalchemy.exc import SQLAlchemyError
from .solver_models import ModuloTt, AulaTt, CorsoDiStudioTt, SlotTt
                  
def __svuotaTabelle(): 
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

    db.session.commit()
    
def __caricaDatiIniziali():
    giorni = ['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì']
    
    slot = ['09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00',
            '14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00']

    anni_accademici = [
        [2018,'2018-19'],
        [2019,'2019-20'],
        [2020,'2020-21'],
        [2021,'2021-22']
    ]
    
    corsi_di_studio = [
        ['A08','INFORMATICA',180,3],
        ['A09','INFORMATICA APPLICATA',120,2]
    ]
    
    attivita_didattiche = [ 
        ['MAT1-1','Matematica 1',9],
        ['ARCL-1','Architettura dei calcolatori e Laboratorio',12],
        ['PG1L-1','Programmazione 1 e Laboratorio',12],
        ['MAT2-2','Matematica 2',6],
        ['ECOA-2','Economia ed organizzazione aziendale',6],
        ['ASDL-2','Algoritmi e strutture dati e Laboratorio',12],
        ['PG3L-3','Programmazione 3 e Laboratorio',9],
        ['RETL-3','Reti di calcolatori e Laboratorio',9],
        ['GISL-3','Sistemi informativi geografici e Laboratorio',6],
        ['SCCP-1','Scientific computer',6],
        ['PHQU-1','Physic and Quantum',6],
        ['MACL-1','Machine Learning',6],
        ['CPGR-1','Computer Graphics',6],
        ['HPCP-2','High Performance Computing',6],
        ['MMLE-2','Multimodal Machine Learning',6],
        ['IOTH-2','Internet of Things',6]
    ]

    aule = [
        ['AN1','Aula 1',150,'N'],
        ['AN2','Aula 2',100,'N'],
        ['AN3','Aula 3',70,'N'],
        ['AN4','Aula 4',50,'N'],
        ['AN5','Aula 5',30,'N'],
        ['AN6','Aula 6',30,'N'],
        ['AN7','Aula 7',150,'N'],
        ['AL1','Aula L1',50,'L'],
        ['AL2','Aula L2',40,'L'],
        ['AL3','Aula L3',30,'L']
    ]   
    
    docenti = [
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
        ['DCPMHL76D11F839P','DOC014','Di Capua','Michele']
    ]
 
    offerta = [
        [4, 1, 1, 1, 1, 1, 130],
        [4, 1, 2, 2, 1, 1, 130],
        [4, 1, 3, 4, 1, 1, 130],
        [4, 1, 4, 6, 2, 1, 90],
        [4, 1, 5, 7, 2, 1, 90],
        [4, 1, 6, 3, 2, 1, 90],
        [4, 1, 7, 5, 3, 1, 60],
        [4, 1, 8, 9, 3, 1, 60],
        [4, 1, 9, 10, 3, 1, 60],
        [4, 2, 10, 4, 1, 1, 70],
        [4, 2, 11, 11, 1, 1, 70],
        [4, 2, 12, 8, 1, 1, 70],
        [4, 2, 13, 12, 2, 1, 70],
        [4, 2, 14, 13, 2, 1, 35],
        [4, 2, 15, 8, 2, 1, 35],
        [4, 2, 16, 14, 2, 1, 35],
    ]
    
    moduli = [
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
        ['MU','Teoria',10,4,'N',2,2,0],
        ['MU','Teoria',11,11,'N',2,2,0],
        ['MU','Teoria',12,8,'N',2,2,0],
        ['MU','Teoria',13,12,'N',2,2,0],
        ['MU','Teoria',14,13,'N',2,2,0],
        ['MU','Teoria',15,8,'N',2,2,0],
        ['MU','Teoria',16,14,'N',2,2,0]
    ]    
          
    for g in giorni:
        row = Giorno(descrizione=g)
        db.session.add(row)
    db.session.commit() 

    for s in slot:
        row = Slot(descrizione=s) 
        db.session.add(row)
    db.session.commit()    
            
    for a in anni_accademici:
        row = AnnoAccademico(anno=a[0], anno_esteso=a[1])
        db.session.add(row)
    db.session.commit()
    
    for c in corsi_di_studio:
        row = CorsoDiStudio(codice=c[0], descrizione=c[1], cfu=c[2], durata_legale=c[3])
        db.session.add(row)
    db.session.commit()    
    
    for a in attivita_didattiche:
        row = AttivitaDidattica(codice=a[0], descrizione=a[1], cfu=a[2])
        db.session.add(row)
    db.session.commit()
        
    for a in aule:
        row = Aula(codice=a[0], descrizione=a[1], capienza=a[2], tipo_aula=a[3])
        db.session.add(row)
    db.session.commit()    
    
    for d in docenti:
        row = Docente(codice_fiscale=d[0], matricola=d[1], cognome = d[2], nome=d[3])
        db.session.add(row)
    db.session.commit()
    
    for o in offerta:
        row = Offerta(anno_accademico_id=o[0], corso_di_studio_id=o[1], attivita_didattica_id=o[2],
                    docente_id=o[3], anno_di_corso=o[4], semestre=o[5], max_studenti=o[6])
        db.session.add(row)
    db.session.commit()
               
    for m in moduli:
        row = Modulo(codice=m[0], descrizione=m[1], offerta_id=m[2], docente_id=m[3],
                    tipo_aula=m[4], numero_sessioni=m[5], durata_sessioni=m[6], max_studenti=m[7])
        db.session.add(row)
    db.session.commit()
    
    #for l in logistica_docenti:
    #    row = LogisticaDocente(offerta_id=l[0], modulo_id=l[1], slot_id=l[2], giorno_id=l[3])
    #    db.session.add(row)
    #db.session.commit()       
                
def inizializzaDb():
    try:
        __svuotaTabelle()
        __caricaDatiIniziali()
        return 0
    except SQLAlchemyError:
        return -1

def caricaDatiDalDb():
    try:
        corsi_tt=[]
        corsi=db.session.query(CorsoDiStudio).all()
        for c in corsi:
            corsi_tt.append(CorsoDiStudioTt(c.id,c.codice,c.descrizione,c.cfu,c.durata_legale))            
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Corsi di studio")
        return -1   
    
    try:
        giorni_tt=[]
        giorni=db.session.query(Giorno).all()
        for g in giorni:
            giorni_tt.append(g.descrizione)
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Giorni")
        return -1    

    try:
        slot_tt=[]
        slot=db.session.query(Slot).all()    
        for s in slot:
            slot_tt.append(SlotTt(s.id,s.descrizione))
    except SQLAlchemyError:
        flash("Errore di caricamento dati LP -> Slot")
        return -1    

    try:
        aule_tt=[]
        aule=db.session.query(Aula).all()
        for a in aule:
            aule_tt.append(AulaTt(a.id,a.codice,a.descrizione,a.capienza,a.tipo_aula))
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
        .filter(AnnoAccademico.anno==2021).all()   
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