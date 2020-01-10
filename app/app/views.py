from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from . import appbuilder, db
from .models import AnniAccademici, CorsiDiStudio, AttivitaDidattiche, Docenti, Aule, OffertaDidattica

class AnniAccademiciView(ModelView):
    datamodel = SQLAInterface(AnniAccademici)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["anno", "anno_esteso"]

class CorsiDiStudioView(ModelView):
    datamodel = SQLAInterface(CorsiDiStudio)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["codice", "descrizione", "cfu", "durata_legale"]

class AttivitaDidatticheView(ModelView):
    datamodel = SQLAInterface(AttivitaDidattiche)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["codice", "descrizione", "cfu"]

class AuleView(ModelView):
    datamodel = SQLAInterface(Aule)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["codice", "descrizione", "capienza", "tipo_aula"]

class DocentiView(ModelView):
    datamodel = SQLAInterface(Docenti)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["codice_fiscale", "cognome", "nome"]

class OffertaDidatticaView(ModelView):
    datamodel = SQLAInterface(OffertaDidattica)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["anno_accademico", "corso_di_studio", "attivita_didattica", "docente", "anno_di_corso", "max_studenti", "semestre"]
    # related_views = [AnniAccademiciView]

""" 
class EmployeeView(ModelView):
    datamodel = SQLAInterface(Employee)

    list_columns = ["full_name", "department.name", "employee_number"]
    edit_form_extra_fields = {
        "department": QuerySelectField(
            "Department",
            query_factory=department_query,
            widget=Select2Widget(extra_classes="readonly"),
        )
    }

    related_views = [EmployeeHistoryView]
    show_template = "appbuilder/general/model/show_cascade.html"


class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)
    related_views = [EmployeeView]


class BenefitView(ModelView):
    datamodel = SQLAInterface(Benefit)
    add_columns = ["name"]
    edit_columns = ["name"]
    show_columns = ["name"]
    list_columns = ["name"] """

db.create_all()

# appbuilder.add_view_no_menu(EmployeeHistoryView, "EmployeeHistoryView")
appbuilder.add_view(
    AnniAccademiciView, "Anni accademici", icon="fa-font"
)
# appbuilder.add_separator("Company")

appbuilder.add_view(
    CorsiDiStudioView, "Corsi di studio", icon="fa-pencil"
)

appbuilder.add_view(
    AttivitaDidatticheView, "Attivita didattiche", icon="fa-pencil-square-o"
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
