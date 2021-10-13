import pulp as pl
import datetime
from sqlalchemy.exc import SQLAlchemyError
from pulp.pulp import LpVariable, lpSum
from abc import ABC, abstractmethod
from flask import flash, request
from .util import caricaDatiDalDb, getColori
from .solver_models import ModuloTt, AulaTt, CorsoDiStudioTt, SlotTt, GiornoTt
from amply.amply import ParamDefStmt
from .import db
import pytz

from .models import Orario, OrarioTestata, OrarioDettaglio

class DatiDiBase(object):

    def __init__(self, corsi, giorni, slot, aule, moduli, logistica):
        #{}
        self.__slot = slot
        #[]
        self.__corsi = corsi
        self.__giorni = giorni
        self.__aule = aule
        self.__moduli = moduli
        self.__logistica = logistica
        
    def get_corsi(self):
        return self.__corsi    
    
    def get_giorni(self):
        return self.__giorni
    
    def get_slot(self):
        return self.__slot
    
    def get_aule(self):
        return self.__aule
    
    def get_moduli(self):
        return self.__moduli
    
    def get_logistica(self):
        return self.__logistica
    
class StruttureAusiliarie(object):
        
    def __init__(self, docenti, titolari_moduli, compatibilita_aule, schedulazione):
        #Set
        self.__docenti = docenti
        #LpVariable.dicts()
        self.__titolari_moduli = titolari_moduli
        self.__compatibilita_aule = compatibilita_aule
        self.__schedulazione = schedulazione

    def get_docenti(self):
        return self.__docenti
    
    def get_titolari_moduli(self):
        return self.__titolari_moduli
    
    def get_compatibilita_aule(self):
        return self.__compatibilita_aule
    
    def get_schedulazione(self):
        return self.__schedulazione

class TemplateCalcoloOrario(ABC):
    
    def genera_orario(self, aa, semestre, desc_orario, registra, vincoli):
        # Modello risolutivo di calcolo del timetable

        # Step 1
        # CARICAMENTO DEI DATI su cui viene effettuato il calcolo dell'orario
        dati = self.carica_dati(aa, semestre)
        
        # Step 2
        # GENERA LE STRUTTURE DATI DI SUPPORTO AL CALCOLO dell'orario
        model, strutture_ausiliarie = self.genera_strutture_ausiliarie(dati)
        
        # Step 3
        # IMPLEMENTA I VINCOLI OBBLIGATORI
        self.imposta_vincoli_obbligatori(model, dati, strutture_ausiliarie)
        
        # Step 4 - abstract
        # IMPLEMENTA EVENTUALMENTE I VINCOLI FACOLTATIVI
        self.imposta_vincoli_facoltativi(model, dati, strutture_ausiliarie, vincoli)
        
        # Step 5 - abstract
        # IMPLEMENTA EVENTUALMENTE I VINCOLI ADDIZIONALI
        self.imposta_vincoli_addizionali(model, dati, strutture_ausiliarie, vincoli)
        
        # Step 6
        ris = self.calcola_orario(model, dati, strutture_ausiliarie)
        
        # Step 7 - abstract
        if registra==True:
            self.registra_orario(model, dati, strutture_ausiliarie, aa, semestre, desc_orario)

        return ris

    def carica_dati(self, aa, semestre):
        corsi, giorni, slot, aule, moduli, logistica = caricaDatiDalDb(aa, semestre)
        return DatiDiBase(corsi, giorni, slot, aule, moduli, logistica)

    def genera_strutture_ausiliarie(self, dati) -> None:
        
        model = pl.LpProblem("CalcolaOrario", pl.LpMaximize)

        # set dei docenti che hanno insegnamenti tra i moduli da fissare in orario
        doc = set(m.get_matricola() for m in dati.get_moduli())
    
        # dict che mantiene l'associazione tra i moduli e i docenti titolari degli stessi
        tit = LpVariable.dicts("assign", [(m,d) for m in dati.get_moduli() for d in doc],
                            lowBound=0,
                            upBound=1,
                            cat=pl.LpInteger)
        
        # dict che mantiene l'associazione tra i moduli e le aule compatibili in relazione alla numerosità attesa
        cpt = LpVariable.dicts("assign", [(m,a) for m in dati.get_moduli() for a in dati.get_aule()],
                            lowBound=0,
                            upBound=1,
                            cat=pl.LpInteger)
        
        # valore 1 -> docente ha la titolarità di un dato modulo
        for m in dati.get_moduli():
            for d in doc:
                if d==m.get_matricola():
                    tit[m,d]=1
                else:
                    tit[m,d]=0
            
        # valore 1 -> l'aula è compatibile con la numerosità di un dato corso    
        for m in dati.get_moduli():
            for a in dati.get_aule():
                if a.get_tipo()==m.get_tipo_aula() and a.get_capienza()>=m.get_max_studenti():
                    cpt[m,a]=1
                else:    
                    cpt[m,a]=0
        
        # Le variabili skd valgono uno se per un dato slot di un dato giorno viene assegnata la lezione di un modulo 
        # di una dato corso in un data aula
        skd = LpVariable.dicts("assign", [(c,m,a,g,s) for c in dati.get_corsi() for m in dati.get_moduli() for a in dati.get_aule() 
                                                    for g in dati.get_giorni() for s in dati.get_slot()], 
                                lowBound=0,
                                upBound=1,
                                cat=pl.LpInteger)
                    
        return model, StruttureAusiliarie(doc, tit, cpt, skd)
        
    def imposta_vincoli_obbligatori(self, model, dati, str_aux):
        
        skd=str_aux.get_schedulazione()
        
        # Vincolo che evita il sovrapporsi di moduli insegnati dagli stessi docenti
        for d in str_aux.get_docenti():
            for s in dati.get_slot():
                for g in dati.get_giorni():
                    model += lpSum(skd[(c,m,a,g,s)]*str_aux.get_titolari_moduli()[(m,d)] for m in dati.get_moduli() for a in dati.get_aule() for c in dati.get_corsi())<=1
        
        # Vincolo che fissa il numero di slot da assegnare per un modulo di un'attività didattica in una settimana
        for m in dati.get_moduli():
            model += lpSum(skd[(c,m,a,g,s)] for a in dati.get_aule() for g in dati.get_giorni() for s in dati.get_slot() for c in dati.get_corsi())==(m.get_num_sessioni()*m.get_dur_sessioni())
        
        # Vincolo che impedisce che ad un aula venga assegnato più di un corso in uno slot di un dato giorno     
        for a in dati.get_aule():
            for g in dati.get_giorni():
                for s in dati.get_slot():
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() for c in dati.get_corsi())<=1  
        
        # Vincoli che permettono di assegnare ad un corso solo aule compatibili con la numerosità del corso stesso       
        for c in dati.get_corsi():
            for m in dati.get_moduli():
                for g in dati.get_giorni():
                    for s in dati.get_slot():
                        for a in dati.get_aule():
                            if str_aux.get_compatibilita_aule()[(m,a)]==0:
                                model+=skd[(c,m,a,g,s)]==0
                            
        # Vincolo che non consente la sovrapposizione di attivita_didattiche relativi allo stenno anno di corso                              
        for c in dati.get_corsi():
            for g in dati.get_giorni():
                for s in dati.get_slot():
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() if m.get_anno_corso()==1 for a in dati.get_aule())<=1
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() if m.get_anno_corso()==2 for a in dati.get_aule())<=1
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() if m.get_anno_corso()==3 for a in dati.get_aule())<=1
        
        # Rende impossibili gli abbinamenti di assegnazioni di moduli di codici corso diversi dal codice del corso in esame
        for c in dati.get_corsi():
            for g in dati.get_giorni():
                for s in dati.get_slot():
                    for m in dati.get_moduli():
                        for a in dati.get_aule():
                            if c.get_codice()!=m.get_cod_corso():
                                model+=skd[(c,m,a,g,s)]==0
               
    def calcola_orario(self, model, dati, str_aux):
        skd=str_aux.get_schedulazione()
        
         # Funzione obiettivo
        model+=lpSum(skd[(c,m,a,g,s)] for c in dati.get_corsi() for m in dati.get_moduli() for a in dati.get_aule() 
                                      for g in dati.get_giorni() for s in dati.get_slot()) 
        
        model.solve()
        return pl.LpStatus[model.status]

    @abstractmethod
    def imposta_vincoli_facoltativi(self, model, dati, str_aux, vincoli):
        pass
        
    @abstractmethod
    def imposta_vincoli_addizionali(self, model, dati, str_aux, vincoli):
        pass
    
    @abstractmethod
    def registra_orario(self, model, dati, str_aux, aa, desc_orario):
        pass
    
    
class AlgoritmoCalcolo(TemplateCalcoloOrario):
    def imposta_vincoli_facoltativi(self, model, dati, str_aux, vincoli):
        skd=str_aux.get_schedulazione()

        if vincoli["chkSessioneUnica"]=="1":
            # Per ogni giorno, ogni corso ed ogni aula il numero di slot massimo consentito è pari alla durata delle sessioni
            # ciò evita che ci possano essere due sessioni nello stesso giorno    
            for c in dati.get_corsi():   
                for m in dati.get_moduli():
                    for g in dati.get_giorni():
                        model+= lpSum(skd[(c,m,a,g,s)] for s in dati.get_slot() for a in dati.get_aule())<=m.get_dur_sessioni()

        if vincoli["chkSessioniConsecutive"]=="1":
            # Un corso per un dato giorno in un dato slot può essere assegnato ad una sola aula
            for c in dati.get_corsi():   
                for m in dati.get_moduli():
                    for g in dati.get_giorni():
                        for s in dati.get_slot():
                           model+=lpSum(skd[(c,m,a,g,s)] for a in dati.get_aule())<=1
                        
            # Vincoli che permettono di assegnare ad un corso solo aule compatibili con la numerosità del corso stesso       
            for c in dati.get_corsi():   
                for m in dati.get_moduli():
                    for g in dati.get_giorni():
                        for s in dati.get_slot():
                            for a in dati.get_aule():
                                if str_aux.get_compatibilita_aule()[(m,a)]==0:
                                    model+=skd[(c,m,a,g,s)]==0
                                
            # Vincoli di consecutività delle sessioni
            for c in dati.get_corsi():
                for m in dati.get_moduli():
                    dur_sessione=m.get_dur_sessioni()
                    if dur_sessione==2:
                        for a in dati.get_aule():
                            for g in dati.get_giorni():
                                for s in (0,4):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]<=0
                                for s in (1,2,5,6):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]-skd[(c,m,a,g,dati.get_slot()[s-1])]<=0 
                                for s in (3,7):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]<=0
                    elif dur_sessione==3:
                        for a in dati.get_aule():
                            for g in dati.get_giorni():                   
                                for s in (0,4):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]<=0 
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+2])]<=0
                                for s in (1,5):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]-skd[(c,m,a,g,dati.get_slot()[s+2])]<=0   
                                for s in (2,6):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]-skd[(c,m,a,g,dati.get_slot()[s-2])]<=0      
                                for s in (3,7):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]<=0 
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-2])]<=0
                    elif dur_sessione==4:
                        for a in dati.get_aule():
                            for g in dati.get_giorni():                   
                                for s in (0,4):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]<=0 
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+2])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+3])]<=0
                                for s in (1,5):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+2])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]-skd[(c,m,a,g,dati.get_slot()[s+2])]<=0   
                                for s in (2,6):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s+1])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]<=0 
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-2])]<=0      
                                for s in (3,7):
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-1])]<=0 
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-2])]<=0
                                    model+=skd[(c,m,a,g,dati.get_slot()[s])]-skd[(c,m,a,g,dati.get_slot()[s-3])]<=0

        # Vincolo che fissa  il numero massimo di slot per giorno per un anno di corso
        if vincoli["chkMaxOre"]=="1":
            limsup=vincoli["selMaxOre"]
            for c in dati.get_corsi():
                for g in dati.get_giorni():
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() if m.get_anno_corso()==1 for s in dati.get_slot() for a in dati.get_aule())<=limsup
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() if m.get_anno_corso()==2 for s in dati.get_slot() for a in dati.get_aule())<=limsup
                    model+=lpSum(skd[(c,m,a,g,s)] for m in dati.get_moduli() if m.get_anno_corso()==3 for s in dati.get_slot() for a in dati.get_aule())<=limsup

                                                                  
    def imposta_vincoli_addizionali(self, model, dati, str_aux, vincoli):
        if vincoli["chkPreferenzeDocenti"]=="1":
            skd=str_aux.get_schedulazione()    
            for l in dati.get_logistica():
                s = l[2]
                for m in dati.get_moduli():
                    if (m.get_offerta_id()==l[0] and m.get_id()==l[1]):
                        break
                for c in dati.get_corsi():
                    if c.get_id()==m.get_corso_id():
                        break
                g=dati.get_giorni()
                model+=lpSum(skd[(c,m,a,g[l[3]-1],dati.get_slot()[s-1])] for a in dati.get_aule())==1

        if vincoli["posizioniFisse"]==None:
            None
        else:
            skd = str_aux.get_schedulazione()
            posizioniFisse=vincoli["posizioniFisse"]
            for p in posizioniFisse:
                if (p["extendedProps"]["corso_id"]!=-1 and p["extendedProps"]["modulo_id"]!=-1 and
                    p["extendedProps"]["aula_id"]!=-1 and p["extendedProps"]["giorno_id"]!=-1 and
                    p["extendedProps"]["slot_id"]!=-1):
                    for c in dati.get_corsi():
                        if c.get_id()==p["extendedProps"]["corso_id"]:
                            break
                    for m in dati.get_moduli():
                        if m.get_id()==p["extendedProps"]["modulo_id"]:
                            break
                    for a in dati.get_aule():
                        if a.get_id()==p["extendedProps"]["aula_id"]:
                            break
                    for g in dati.get_giorni():
                        if g.get_id()==p["extendedProps"]["giorno_id"]:
                            break
                    for s in dati.get_slot():
                        if s.get_id()==p["extendedProps"]["slot_id"]:
                            break
                    model+=skd[(c,m,a,g,s)]==1

    def registra_orario(self, model, dati, str_aux, aa, semestre, desc_orario):
        skd=str_aux.get_schedulazione()  
        if (pl.LpStatus[model.status]) == 'Optimal':
            try:
                tz = pytz.timezone('Europe/Rome')

                vincolo_sessione_unica=0
                if request.form.get('chk_sessione_unica')=='1':
                    vincolo_sessione_unica=1

                vincolo_sessioni_consecutive=0
                if request.form.get('chk_slot_sessioni_consecutive') == '1':
                    vincolo_sessioni_consecutive=1

                vincolo_max_slot=0
                if request.form.get('chk_max_ore') == '1':
                    vincolo_max_slot=request.form.get('sel_max_ore')

                vincolo_logistica_docenti=0
                if request.form.get('chk_preferenze_docenti') == '1':
                    vincolo_logistica_docenti=1

                row_test = OrarioTestata(descrizione = desc_orario,
                                         anno_accademico_id = aa,
                                         semestre = semestre,
                                         data_creazione = datetime.datetime.now(tz),
                                         vincolo_sessione_unica = vincolo_sessione_unica,
                                         vincolo_sessioni_consecutive = vincolo_sessioni_consecutive,
                                         vincolo_max_slot = vincolo_max_slot,
                                         vincolo_logistica_docenti = vincolo_logistica_docenti,
                                         stato_orario_id = 2)
                db.session.add(row_test)
                db.session.flush()

                id_testata = row_test.id

                for c in dati.get_corsi():
                    for g in dati.get_giorni():
                        for m in dati.get_moduli():
                            for s in dati.get_slot():
                                for a in dati.get_aule():
                                    if skd[(c,m,a,g,s)].varValue>0:
                                        row_dett = OrarioDettaglio(testata_id = id_testata,
                                                                   corso_di_studio_id = c.get_id(),
                                                                   modulo_id = m.get_id(),
                                                                   slot_id = s.get_id(),
                                                                   giorno_id = g.get_id(),
                                                                   aula_id = a.get_id())
                                        db.session.add(row_dett)

                db.session.commit()
                flash('Orario correttamente registrato nel db','success')
            except SQLAlchemyError:
                db.session.rollback()
                flash("Errore di registrazione dell'orario generato nel db","danger")
