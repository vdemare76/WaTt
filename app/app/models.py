from flask import url_for
from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, DateTime, Date
from sqlalchemy.orm import relationship
        
class AnnoAccademico(Model):
    id = Column(Integer, primary_key=True)
    anno = Column(Integer)
    anno_esteso = Column(String(15))
    
    def __repr__(self):
        return self.anno_esteso

class Slot(Model):
    id = Column(Integer, primary_key=True)
    descrizione = Column(String(30))
    
    def __repr__(self):
        return self.descrizione

class Giorno(Model):
    id = Column(Integer, primary_key=True)
    descrizione = Column(String(30))
    
    def __repr__(self):
        return self.descrizione
    
class CorsoDiStudio(Model):
    id = Column(Integer, primary_key=True)
    codice = Column(String(15))
    descrizione = Column(String(150))
    cfu = Column(Integer)
    durata_legale = Column(Integer)
    #offerta = relationship("Offerta", back_populates="corso_di_studio")

    def __repr__(self):
        return self.codice + ' ' + self.descrizione

class AttivitaDidattica(Model):
    id = Column(Integer, primary_key=True)
    codice = Column(String(15))
    descrizione = Column(String(150))
    cfu = Column(Integer)
    offerta = relationship("Offerta", back_populates="attivita_didattica")

    def __repr__(self):
        return self.codice +  ' ' + self.descrizione

class Docente(Model):
    id = Column(Integer, primary_key=True)
    codice_fiscale = Column(String(16))
    matricola = Column(String(6))
    cognome = Column(String(100))
    nome = Column(String(100))
    offerta = relationship("Offerta", back_populates="docente")

    def __repr__(self):
        return self.cognome + ' ' + self.nome

class Aula(Model):
    id = Column(Integer, primary_key=True)
    codice = Column(String(25))
    descrizione = Column(String(150))
    capienza = Column(Integer)
    tipo_aula = Column(String(10))

    def __repr__(self):
        return self.codice +  ' ' + self.descrizione
   
class Offerta(Model):
    id = Column(Integer, primary_key=True)
    anno_accademico_id = Column(Integer, ForeignKey('anno_accademico.id'), nullable=False)
    anno_accademico = relationship("AnnoAccademico")
    corso_di_studio_id = Column(Integer, ForeignKey('corso_di_studio.id'), nullable=False)
    corso_di_studio = relationship("CorsoDiStudio")
    attivita_didattica_id = Column(Integer, ForeignKey('attivita_didattica.id'), nullable=False)
    attivita_didattica = relationship("AttivitaDidattica")
    docente_id = Column(Integer, ForeignKey('docente.id'), nullable=False)
    docente = relationship("Docente")
    anno_di_corso = Column(Integer)
    semestre = Column(Integer)
    max_studenti = Column(Integer)
    
    def __repr__(self):
        return str(self.anno_accademico) + ' ' + str(self.corso_di_studio) + ' ' + str(self.attivita_didattica)

class Modulo(Model):
    id = Column(Integer, primary_key=True)
    codice = Column(String(15))
    descrizione = Column(String(30))
    offerta_id = Column(Integer, ForeignKey('offerta.id'), nullable=False)
    offerta = relationship("Offerta")
    docente_id = Column(Integer, ForeignKey('docente.id'), nullable=False)
    docente = relationship("Docente")
    tipo_aula = Column(String(1))
    numero_sessioni = Column(Integer)
    durata_sessioni = Column(Integer)
    max_studenti = Column(Integer)
    
    def __repr__(self):
        return self.codice +  ' ' + self.descrizione   
    
class LogisticaDocente(Model):
    id = Column(Integer, primary_key=True)
    offerta_id = Column(Integer, ForeignKey('offerta.id'), nullable=False)
    offerta = relationship("Offerta")
    modulo_id = Column(Integer, ForeignKey('modulo.id'), nullable=False)
    modulo = relationship("Modulo")
    slot_id = Column(Integer, ForeignKey('slot.id'), nullable=False)
    slot = relationship("Slot")
    giorno_id = Column(Integer, ForeignKey('giorno.id'), nullable=False)
    giorno = relationship("Giorno")
    
    def __repr__(self):
        return self.offerta_id

class OrarioTestata(Model):
    id = Column(Integer, primary_key=True)
    descrizione = Column(String(100))
    anno_accademico_id = Column(Integer, ForeignKey('anno_accademico.id'), nullable=False)
    anno_accademico = relationship("AnnoAccademico")
    semestre = Column(Integer)
    data_creazione = Column(DateTime)

    def __repr__(self):
        return self.descrizione

class OrarioDettaglio(Model):
    id = Column(Integer, primary_key=True)
    testata_id = Column(Integer, ForeignKey('orario_testata.id'), nullable=False)
    corso_di_studio_id = Column(Integer, ForeignKey('corso_di_studio.id'), nullable=False)
    corso_di_studio = relationship("CorsoDiStudio")
    modulo_id = Column(Integer, ForeignKey('modulo.id'), nullable=False)
    modulo = relationship("Modulo")
    slot_id = Column(Integer, ForeignKey('slot.id'), nullable=False)
    slot = relationship("Slot")
    giorno_id = Column(Integer, ForeignKey('giorno.id'), nullable=False)
    giorno = relationship("Giorno")
    aula_id = Column(Integer, ForeignKey('aula.id'), nullable=False)
    aula = relationship("Aula")

    def __repr__(self):
        return self.descrizione

class Orario(Model):
    id = Column(Integer, primary_key=True)
    giorno = Column(String(10))
    id_corso = Column(Integer)
    codice_corso = Column(String(10))
    colore_corso = Column(String(10))
    codice_attivita = Column(String(25))
    descrizione_modulo = Column(String(100))
    numerosita_modulo = Column(Integer)
    slot_id = Column(Integer)
    descrizione_slot = Column(String(20))
    nome_docente = Column(String(50))
    cognome_docente = Column(String(50))
    anno_corso = Column(Integer)
    aula = Column(String(35))
    capienza_aula = Column(Integer)

class Chiusura(Model):
    id = Column(Integer, primary_key=True)
    testata_id = Column(Integer, ForeignKey('orario_testata.id'), nullable=False)
    data = Column(Date)
    nota = Column(String(100))