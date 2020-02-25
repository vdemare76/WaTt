from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from . import appbuilder, db
from .models import AnniAccademici, CorsiDiStudio, AttivitaDidattiche, Docenti, Aule, OffertaDidattica, LogisticaDocenti

class AnniAccademiciView(ModelView):
    datamodel = SQLAInterface(AnniAccademici)
    list_columns = ["anno", "anno_esteso"]

class CorsiDiStudioView(ModelView):
    datamodel = SQLAInterface(CorsiDiStudio)
    list_columns = ["codice", "descrizione", "cfu", "durata_legale"]

class AttivitaDidatticheView(ModelView):
    datamodel = SQLAInterface(AttivitaDidattiche)
    list_columns = ["codice", "descrizione", "cfu"]

class AuleView(ModelView):
    datamodel = SQLAInterface(Aule)
    list_columns = ["codice", "descrizione", "capienza", "tipo_aula"]

class DocentiView(ModelView):
    datamodel = SQLAInterface(Docenti)
    list_columns = ["codice_fiscale", "cognome", "nome"]

class OffertaDidatticaView(ModelView):
    datamodel = SQLAInterface(OffertaDidattica)
    list_columns = ["anno_accademico", "corso_di_studio", "attivita_didattica", "docente", "anno_di_corso", "max_studenti", "semestre"]

class LogisticaDocentiView(ModelView):
    datamodel = SQLAInterface(LogisticaDocenti)
    list_columns = ["offerta", "durata_sessioni", "numero_sessioni"]

db.create_all()

appbuilder.add_view(
    AnniAccademiciView, "Anni accademici", icon="fa-font"
)

appbuilder.add_view(
    CorsiDiStudioView, "Corsi di studio", icon="fa-pencil"
)

appbuilder.add_view(
    AttivitaDidatticheView, "Attività didattiche", icon="fa-pencil-square-o"
)

appbuilder.add_view(
    DocentiView, "Docenti", icon="fa-black-tie"
)

appbuilder.add_view(
    AuleView, "Aule", icon="fa-th"
)

appbuilder.add_view(
    OffertaDidatticaView, "Offerta didattica", icon="fa-map"
)

appbuilder.add_view(
    LogisticaDocentiView, "Logistica docenti", icon="fa-wrench"
)
