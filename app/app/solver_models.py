class GiornoTt(object):
    def __init__(self, id, descrizione):
        self.__id = id
        self.__descrizione = descrizione

    def get_id(self):
        return self.__id

    def get_descrizione(self):
        return self.__descrizione

class CorsoDiStudioTt(object):
    def __init__(self, id, codice, descrizione, cfu, durata_legale):
        self.__id = id
        self.__codice = codice
        self.__descrizione = descrizione
        self.__cfu = cfu
        self.__durata_legale = durata_legale
             
    def get_id(self):
        return self.__id
       
    def get_codice(self):
        return self.__codice
    
    def get_descrizione(self):
        return self.__descrizione
    
    def get_cfu(self):
        return self.__cfu
    
    def get_durata_legale(self):
        return self.__durata_legale
        
class ModuloTt(object):
    def __init__(self, id, codice, descrizione, cod_attivita, desc_attivita, corso_id, cod_corso, desc_corso, matricola, cognome_doc, nome_doc, num_sessioni, dur_sessioni, offerta_id, anno_corso, semestre, max_stud_anno, max_stud_modulo, tipo_aula):
        self.__id = id
        self.__codice = codice
        self.__descrizione = descrizione
        self.__cod_attivita = cod_attivita
        self.__desc_attivita = desc_attivita
        self.__corso_id = corso_id
        self.__cod_corso = cod_corso
        self.__desc_corso = desc_corso
        self.__matricola = matricola
        self.__cognome_doc = cognome_doc
        self.__nome_doc = nome_doc
        self.__num_sessioni = num_sessioni
        self.__dur_sessioni = dur_sessioni
        self.__offerta_id = offerta_id
        self.__anno_corso = anno_corso
        self.__semestre = semestre
        if max_stud_modulo == 0:
            self.__max_studenti = max_stud_anno
        else:
            self.__max_studenti = max_stud_modulo
        self.__tipo_aula = tipo_aula
    
    def get_id(self):
        return self.__id
        
    def get_codice(self):
        return self.__codice
    
    def get_descrizione(self):
        return self.__descrizione

    def get_cod_attivita(self):
        return self.__cod_attivita    
    
    def get_desc_attivita(self):
        return self.__desc_attivita
    
    def get_corso_id(self):
        return self.__corso_id
    
    def get_cod_corso(self):
        return self.__cod_corso
    
    def get_desc_corso(self):
        return self.__desc_corso
    
    def get_matricola(self):
        return self.__matricola
    
    def get_cognome_doc(self):
        return self.__cognome_doc
    
    def get_nome_doc(self):
        return self.__nome_doc
    
    def get_num_sessioni(self):
        return self.__num_sessioni
    
    def get_dur_sessioni(self):
        return self.__dur_sessioni  
    
    def get_offerta_id(self):
        return self.__offerta_id
    
    def get_anno_corso(self):
        return self.__anno_corso
    
    def get_semestre(self):
        return self.__semestre
    
    def get_max_studenti(self):
        return self.__max_studenti
    
    def get_tipo_aula(self):
        return self.__tipo_aula
    
class AulaTt(object):
    
    def __init__(self, id, codice, descrizione, capienza, tipo):
        self.__id=id
        self.__codice=codice
        self.__descrizione=descrizione
        self.__capienza=capienza
        self.__tipo=tipo
        
    def get_id(self):
        return self.__id
        
    def get_codice(self):
        return self.__codice
    
    def get_descrizione(self):
        return self.__descrizione
    
    def get_capienza(self):
        return self.__capienza
    
    def get_tipo(self):
        return self.__tipo
    
class SlotTt(object):
    
    def __init__(self, id, descrizione):
        self.__id=id
        self.__descrizione=descrizione
        
    def get_id(self):
        return self.__id
        
    def get_descrizione(self):
        return self.__descrizione
