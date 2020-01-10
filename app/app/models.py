from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

class AnniAccademici(Model):
    __tablename__ = 'anni_accademici'
    id = Column(Integer, primary_key=True)
    anno = Column(Integer)
    anno_esteso = Column(String(15))
    # offerta = relationship("OffertaDidattica", back_populates="anni_accademici")

    def __repr__(self):
        return self.anno_esteso


class CorsiDiStudio(Model):
    __tablename__ = 'corsi_di_studio'
    id = Column(Integer, primary_key=True)
    codice = Column(String(15))
    descrizione = Column(String(150))
    cfu = Column(Integer)
    durata_legale = Column(Integer)

    def __repr__(self):
        return self.codice + ' ' + self.descrizione


class AttivitaDidattiche(Model):
    __tablename__ = 'attivita_didattiche'
    id = Column(Integer, primary_key=True)
    codice = Column(String(15))
    descrizione = Column(String(150))
    cfu = Column(Integer)

    def __repr__(self):
        return self.codice +  ' ' + self.descrizione


class Docenti(Model):
    __tablename__ = 'docenti'
    id = Column(Integer, primary_key=True)
    codice_fiscale = Column(String(16))
    cognome = Column(String(100))
    nome = Column(String(100))

    def __repr__(self):
        return self.cognome + ' ' + self.nome

class Aule(Model):
    __tablename__ = 'aule'
    id = Column(Integer, primary_key=True)
    codice = Column(String(25))
    descrizione = Column(String(150))
    capienza = Column(Integer)
    tipo_aula = Column(String(10))

    def __repr__(self):
        return self.codice +  ' ' + self.descrizione


class OffertaDidattica(Model):
    __tablename__ = 'offerta_didattica'
    id = Column(Integer, primary_key=True)
    id_aa = Column(Integer, ForeignKey('anni_accademici.id'), nullable=False)
    id_cdl = Column(Integer, ForeignKey('corsi_di_studio.id'), nullable=False)
    id_att_did = Column(Integer, ForeignKey('attivita_didattiche.id'), nullable=False)
    id_doc = Column(Integer, ForeignKey('docenti.id'), nullable=False)
    anno_di_corso = Column(Integer)
    max_studenti = Column(Integer)
    semestre = Column(Integer)
    anno_accademico = relationship("AnniAccademici")
    corso_di_studio = relationship("CorsiDiStudio")
    attivita_didattica = relationship("AttivitaDidattiche")
    docente = relationship("Docenti")

    def __repr__(self):
        return self.name