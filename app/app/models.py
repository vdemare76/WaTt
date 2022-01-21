from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, DateTime, Date
from sqlalchemy.orm import relationship


class AnnoAccademico(Model):
    id = Column(Integer, primary_key = True)
    anno = Column(Integer)
    anno_esteso = Column(String(15))
    
    def __repr__(self):
        return self.anno_esteso


class StatoOrario(Model):
    id = Column(Integer, primary_key = True)
    codice = Column(String(1))
    descrizione = Column(String(25))

    def __repr__(self):
        return self.descrizione


class Slot(Model):
    id = Column(Integer, primary_key = True)
    descrizione = Column(String(30))
    ora_slot_cal = Column(Integer)
    
    def __repr__(self):
        return self.descrizione


class Giorno(Model):
    id=Column(Integer, primary_key = True)
    descrizione = Column(String(30))
    
    def __repr__(self):
        return self.descrizione
    

class CorsoDiStudio(Model):
    id = Column(Integer, primary_key = True)
    codice = Column(String(15))
    descrizione = Column(String(150))
    cfu = Column(Integer)
    durata_legale = Column(Integer)

    def __repr__(self):
        return self.codice + " " + self.descrizione


class AttivitaDidattica(Model):
    id = Column(Integer, primary_key = True)
    codice = Column(String(15))
    descrizione = Column(String(150))
    cfu = Column(Integer)
    colore = Column(String(7))

    def __repr__(self):
        return self.codice +  " " + self.descrizione


class Docente(Model):
    id = Column(Integer, primary_key = True)
    codice_fiscale = Column(String(16))
    matricola = Column(String(6))
    cognome = Column(String(100))
    nome = Column(String(100))
    offerta = relationship("Offerta", back_populates = "docente")

    def __repr__(self):
        return self.cognome + " " + self.nome


class Aula(Model):
    id = Column(Integer, primary_key = True)
    codice = Column(String(25))
    descrizione = Column(String(150))
    capienza = Column(Integer)
    tipo_aula = Column(String(10))

    def to_dict(self):
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_")])


class NumerositaAnniCorso(Model):
    id = Column(Integer, primary_key = True)
    codice_corso = Column(String(15))
    anno_di_corso = Column(Integer)
    numerosita = Column(Integer)

    def __repr__(self):
        return str(self.codice_corso)


class Offerta(Model):
    id=Column(Integer, primary_key = True)
    anno_accademico_id = Column(Integer, ForeignKey("anno_accademico.id"), nullable = False)
    anno_accademico = relationship("AnnoAccademico")
    corso_di_studio_id = Column(Integer, ForeignKey("corso_di_studio.id"), nullable = False)
    corso_di_studio = relationship("CorsoDiStudio")
    attivita_didattica_id = Column(Integer, ForeignKey("attivita_didattica.id"), nullable = False)
    attivita_didattica = relationship("AttivitaDidattica")
    docente_id = Column(Integer, ForeignKey("docente.id"), nullable = False)
    docente = relationship("Docente")
    anno_di_corso = Column(Integer)
    semestre = Column(Integer)
    max_studenti = Column(Integer)
    
    def __repr__(self):
        return str(self.anno_accademico) + " " + str(self.corso_di_studio) + " " + str(self.attivita_didattica)


class Modulo(Model):
    id = Column(Integer, primary_key = True)
    codice = Column(String(15))
    descrizione = Column(String(30))
    offerta_id = Column(Integer, ForeignKey("offerta.id"), nullable = False)
    offerta = relationship("Offerta")
    docente_id = Column(Integer, ForeignKey("docente.id"), nullable = False)
    docente = relationship("Docente")
    tipo_aula = Column(String(1))
    numero_sessioni = Column(Integer)
    durata_sessioni = Column(Integer)
    max_studenti = Column(Integer)
    
    def __repr__(self):
        return self.codice +  " " + self.descrizione


class LogisticaDocente(Model):
    id = Column(Integer, primary_key=True)
    offerta_id = Column(Integer, ForeignKey("offerta.id"), nullable = False)
    offerta = relationship("Offerta")
    modulo_id = Column(Integer, ForeignKey("modulo.id"), nullable = False)
    modulo = relationship("Modulo")
    slot_id = Column(Integer, ForeignKey("slot.id"), nullable = False)
    slot = relationship("Slot")
    giorno_id = Column(Integer, ForeignKey("giorno.id"), nullable = False)
    giorno = relationship("Giorno")
    
    def __repr__(self):
        return self.offerta_id


class OrarioTestata(Model):
    id=Column(Integer, primary_key = True)
    descrizione = Column(String(100))
    anno_accademico_id = Column(Integer, ForeignKey("anno_accademico.id"), nullable = False)
    anno_accademico = relationship("AnnoAccademico")
    semestre = Column(Integer)
    data_creazione = Column(DateTime)
    data_ultima_modifica = Column(DateTime)
    vincolo_sessione_unica = Column(Integer)
    vincolo_sessioni_consecutive = Column(Integer)
    vincolo_max_slot = Column(Integer)
    vincolo_logistica_docenti = Column(Integer)
    stato_orario_id = Column(Integer, ForeignKey("stato_orario.id"), nullable = False)
    stato_orario = relationship("StatoOrario")

    def __repr__(self):
        return self.descrizione


class OrarioDettaglio(Model):
    id = Column(Integer, primary_key = True)
    testata_id = Column(Integer, ForeignKey("orario_testata.id"), nullable = False)
    corso_di_studio_id = Column(Integer, ForeignKey("corso_di_studio.id"), nullable = False)
    corso_di_studio = relationship("CorsoDiStudio")
    modulo_id = Column(Integer, ForeignKey("modulo.id"), nullable = False)
    modulo = relationship("Modulo")
    slot_id = Column(Integer, ForeignKey("slot.id"), nullable = False)
    slot = relationship("Slot")
    giorno_id = Column(Integer, ForeignKey("giorno.id"), nullable = False)
    giorno = relationship("Giorno")
    aula_id = Column(Integer, ForeignKey("aula.id"), nullable = False)
    aula = relationship("Aula")

    def __repr__(self):
        return self.descrizione

class Chiusura(Model):
    id = Column(Integer, primary_key = True)
    testata_id=Column(Integer, ForeignKey("orario_testata.id"), nullable = False)
    testata=relationship("OrarioTestata")
    data_inizio = Column(Date)
    data_fine = Column(Date)
    nota = Column(String(100))