from flask import flash, render_template, redirect, url_for, request, g, session
from flask_appbuilder import ModelView, BaseView, expose, has_access, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError

from flask_appbuilder.fieldwidgets import Select2AJAXWidget, Select2SlaveAJAXWidget
from flask_appbuilder.fields import AJAXSelectField
from wtforms import validators

from .import appbuilder, db
import requests
from .models import AnnoAccademico, CorsoDiStudio, AttivitaDidattica, Docente, Aula, NumerositaAnniCorso, Offerta, \
                    LogisticaDocente, Modulo, Giorno, Slot, Orario, OrarioTestata, OrarioDettaglio, Chiusura

from flask.templating import render_template
from .util import svuotaDb, caricaDatiTest, caricaDati7Cds, caricaDatiBase, getColori
from .esse3_to_watt import getAnniAccademici, getCorsiInOfferta, importDatiEsse3
from .solver import AlgoritmoCompleto
from datetime import timedelta

class AnniAccademiciView(ModelView):
    datamodel = SQLAInterface(AnnoAccademico)
    label_columns = {"anno":"Anno accademico",
                     "anno_esteso":"Anno accademico esteso"}
    list_columns = ["anno", 
                    "anno_esteso"]


class SlotView(ModelView):
    datamodel = SQLAInterface(Slot)
    label_columns = {"descrizione":"Descrizione"}
    list_columns = ["descrizione"]


class GiorniView(ModelView):
    datamodel = SQLAInterface(Giorno)
    label_columns = {"descrizione":"Descrizione"}
    list_columns = ["descrizione"]


class CorsiDiStudioView(ModelView):
    datamodel = SQLAInterface(CorsoDiStudio)
    label_columns = {"codice":"Codice CdS",
                     "descrizione":"Descrizione",
                     "cfu":"Cfu",
                     "durata_legale":"Durata legale"}
    list_columns = ["codice", 
                    "descrizione", 
                    "cfu", 
                    "durata_legale"]


class AttivitaDidatticheView(ModelView):
    datamodel = SQLAInterface(AttivitaDidattica)
    label_columns = {"codice":"Codice AD",
                     "Descrizione":"Descrizione",
                     "cfu":"Cfu",
                     "colore":"Colore"}
    list_columns = ["codice", 
                    "descrizione", 
                    "cfu",
                    "colore"]


class AuleView(ModelView):
    datamodel = SQLAInterface(Aula)
    label_columns = {"codice":"Codice aula",
                     "descrizione":"Descrizione",
                     "capienza":"Capienza",
                     "tipo_aula":"Tipo aula"}
    list_columns = ["codice", 
                    "descrizione", 
                    "capienza",
                    "tipo_aula"]


class NumerositaAnniCorsoView(ModelView):
    datamodel = SQLAInterface(NumerositaAnniCorso)
    label_columns = {"codice_corso":"Corso di studio",
                     "anno_di_corso":"Anno di corso",
                     "numerosita":"Numerosità"}
    list_columns = ["codice_corso",
                    "anno_di_corso",
                    "numerosita"]


class DocentiView(ModelView):
    datamodel = SQLAInterface(Docente)
    label_columns = {"codice_fiscale":"Codice fiscale",
                     "cognome":"Cognome",
                     "nome":"Nome"}
    list_columns = ["codice_fiscale", 
                    "cognome", 
                    "nome"]
    search_filters = ["codice_fiscale", 
                    "cognome", 
                    "nome"] 


class OffertaView(ModelView):
    datamodel = SQLAInterface(Offerta)
    label_columns = {"anno_accademico.anno_esteso":"Anno accademico",
                     "corso_di_studio.descrizione":"Corso di studio",
                     "attivita_didattica.descrizione":"Attività didattica",
                     "docente.cognome":"Cognome docente",
                     "docente.nome":"Nome docente",
                     "anno_di_corso":"Anno di corso",
                     "semestre":"Semestre",
                     "max_studenti":"Numerosità studenti"}
    list_columns = ["anno_accademico.anno_esteso",
                    "corso_di_studio.descrizione",
                    "attivita_didattica.descrizione",
                    "docente.cognome","docente.nome",
                    "anno_di_corso",
                    "semestre",
                    "max_studenti"]


class ModuliView(ModelView):
    datamodel = SQLAInterface(Modulo)
    label_columns = {"codice":"Codice modulo",
                     "descrizione":"Descrizione",
                     "offerta.anno_accademico":"A.A. Offerta",
                     "offerta.corso_di_studio":"C.d.S Offerta",
                     "offerta.attivita_didattica":"AD Offerta",
                     "tipo_aula":"Tipo aula",
                     "docente.cognome":"Cognome docente",
                     "docente.nome":"Nome docente",
                     "numero_sessioni":"Numero di sessioni",
                     "durata_sessioni":"Durata sessioni",
                     "max_studenti":"Numerosità massima studenti"}
    list_columns = ["codice",
                    "descrizione",
                    "offerta.anno_accademico",
                    "offerta.corso_di_studio",
                    "offerta.attivita_didattica",
                    "tipo_aula",
                    "docente.cognome",
                    "docente.nome",
                    "numero_sessioni",
                    "durata_sessioni",
                    "max_studenti"]
    order_columns = ["codice",
                    "descrizione",
                    "tipo_aula",
                    "docente.cognome",
                    "docente.nome",
                    "numero_sessioni",
                    "durata_sessioni",
                    "max_studenti"]


class ChiusuraView(ModelView):
    datamodel = SQLAInterface(Chiusura)
    label_columns = {"orario_testata.descrizione":"Descrizione orario",
                     "data_inizio":"Data chiusura",
                     "data_fine":"Data fine",
                     "nota":"Nota"}
    list_columns = ["testata",
                    "data_inizio",
                    "data_fine",
                    "nota"]


class LogisticaDocentiView(ModelView):
    datamodel = SQLAInterface(LogisticaDocente)
    label_columns = {"offerta.attivita_didattica":"Offerta",
                     "modulo.descrizione":"Modulo",
                     "slot.descrizione":"Slot",
                     "giorno.descrizione":"Giorno"}
    
    list_columns = ["offerta.attivita_didattica",
                    "modulo.descrizione",
                    "slot.descrizione",
                    "giorno.descrizione"]
       
    add_form_extra_fields = {
         "offerta": AJAXSelectField(
            "Offerta",
            datamodel=datamodel,
            validators=[validators.DataRequired()],
            col_name="offerta",
            widget=Select2AJAXWidget(
                endpoint="/logisticadocentiview/api/column/add/offerta"
            ),
        ),
        'modulo': AJAXSelectField(
            'Modulo',
            datamodel=datamodel,
            validators=[validators.DataRequired()],
            col_name="modulo",
            widget=Select2SlaveAJAXWidget(
                master_id="offerta",
                endpoint="/logisticadocentiview/api/column/add/modulo?_flt_0_offerta_id={{ID}}",
            )
        )
    }
    
    edit_form_extra_fields = add_form_extra_fields 


class OrariGeneratiView(ModelView):
    datamodel = SQLAInterface(OrarioTestata)
    label_columns = {"id":"identificativo",
                     "descrizione":"Descrizione",
                     "anno_accademico.anno_esteso":"Anno Accademico",
                     "semestre":"Semestre",
                     "data_creazione":"Data creazione",
                     "note_creazione":"Note",
                     "stato_orario.descrizione":"Stato"}
    list_columns = ["id",
                    "descrizione",
                    "anno_accademico.anno_esteso",
                    "semestre",
                    "data_creazione",
                    "note_creazione",
                    "stato_orario.descrizione"]
    edit_exclude_columns = ["id",
                            "anno_accademico",
                            "semestre",
                            "data_creazione",
                            "note_creazione"]

    @action("cancella", "Elimina", "Vuoi eliminare gli orari selezionati?", "fa-trash-alt", single=False)
    def cancella(self, items):
        for i in items:
            try:
                db.session.query(OrarioDettaglio).filter(OrarioDettaglio.testata_id == i.id).delete()
                db.session.query(OrarioTestata).filter(OrarioTestata.id == i.id).delete()
                db.session.commit()
            except SQLAlchemyError:
                db.sessione.rollback()
                flash('Errore durante la cancellazione degli orari selezionati','danger')
                return -1
        return redirect(self.get_redirect())

    @action("carica_schema", "Carica orario", "Vuoi visualizzare lo schema orario selezionato?", "fa-trash-alt", multiple=False, single=True)
    def carica_schema(self, item):
        try:
            db.session.query(Orario).delete()
            db.session.execute('ALTER TABLE orario AUTO_INCREMENT = 1')

            rows=db.session.query(OrarioDettaglio, Modulo, Giorno, Offerta, AttivitaDidattica, CorsoDiStudio, Docente, Slot, Aula) \
            .join(CorsoDiStudio, OrarioDettaglio.corso_di_studio_id == CorsoDiStudio.id) \
            .join(Modulo, OrarioDettaglio.modulo_id == Modulo.id) \
            .join(Offerta, Modulo.offerta_id == Offerta.id) \
            .join(Docente, Modulo.docente_id == Docente.id) \
            .join(Slot, OrarioDettaglio.slot_id == Slot.id) \
            .join(Giorno, OrarioDettaglio.giorno_id == Giorno.id) \
            .join(AttivitaDidattica, Offerta.attivita_didattica_id == AttivitaDidattica.id) \
            .join(Aula, OrarioDettaglio.aula_id==Aula.id)\
            .filter(OrarioDettaglio.testata_id==item.id)\
            .order_by(CorsoDiStudio.codice.asc(), Giorno.id.asc(), Modulo.codice.asc(), Slot.id.asc(), Aula.codice.asc()).all()

            for r in rows:
                row = Orario(testata_id=item.id,
                             giorno=r.Giorno.descrizione,
                             corso_id=r.CorsoDiStudio.id,
                             codice_corso=r.CorsoDiStudio.codice,
                             colore_corso=getColori()[r.CorsoDiStudio.id],
                             codice_attivita=r.AttivitaDidattica.codice,
                             descrizione_attivita=r.AttivitaDidattica.descrizione,
                             colore_attivita=r.AttivitaDidattica.colore,
                             descrizione_modulo=r.Modulo.descrizione,
                             numerosita_modulo=r.Modulo.max_studenti,
                             slot_id=r.Slot.id,
                             descrizione_slot=r.Slot.descrizione,
                             nome_docente=r.Docente.nome,
                             cognome_docente=r.Docente.cognome,
                             anno_corso=r.Offerta.anno_di_corso,
                             aula=r.Aula.descrizione,
                             capienza_aula=r.Aula.capienza)
                db.session.add(row)
            db.session.commit()
            flash('Orario caricato correttamente! (Puoi visualizzarlo con Orario -> Schema settimanale','success')
        except SQLAlchemyError:
            db.sessione.rollback()
            flash('Errore durante la cancellazione degli orari selezionati','danger')
            return -1
        return redirect(self.get_redirect())


class UtilitaView(BaseView):
    default_view = 'srv_home'

    @expose('/srv_home/')
    @has_access
    def srv_home(self, name=None):
        return render_template("utility.html", base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/srv_initdb', methods=['GET','POST'])
    @has_access
    def srv_util(self):
        target=request.form.get("target")
        if target=="svuotaDB":
            svuotaDb()
        elif target=="caricaDatiBase":
            caricaDatiBase()
        elif target=="carica7Cds1Mod":
            caricaDati7Cds("1")
        elif target=="carica7CdsNMod":
            caricaDati7Cds("N")
        elif target=="inizializzaAllDB":
            caricaDatiTest()

        return render_template("utility.html", base_template=appbuilder.base_template, appbuilder=appbuilder)


class UtilitaEsse3View(BaseView):
    default_view = 'srv_esse3_home'

    @expose('/srv_esse3_home/')
    @has_access
    def srv_esse3_home(self, name=None):
        return render_template("utility_esse3.html", base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/srv_esse3_util', methods=['GET','POST'])
    @has_access
    def srv_esse3_util(self):
        target=request.form.get("target")

        if target == "caricaAnniAccademici":
            session['anniAccademici']=getAnniAccademici()
            return render_template("utility_esse3.html",
                                   base_template=appbuilder.base_template,
                                   appbuilder=appbuilder,
                                   annoAccademicoSelezionato=1000,
                                   anniAccademici=session['anniAccademici'])

        elif target == "caricaCorsiOffertaFormativa":
            try:
                anniAccademici=session['anniAccademici']
                session['corsiInOfferta']=getCorsiInOfferta(request.form.get("anniAccademici"))
                return render_template("utility_esse3.html",
                                       base_template=appbuilder.base_template,
                                       appbuilder=appbuilder,
                                       anniAccademici=anniAccademici,
                                       annoAccademicoSelezionato=request.form.get('anniAccademici'),
                                       corsiInOfferta=session['corsiInOfferta'])
            except:
                flash("Non sono stati caricati gli anni accademici per cui è disponibile un'offerta didattica!",'danger')

        elif target == "caricaDatiCorsi":
            try:
                anniAccademici=session['anniAccademici']
                corsiInOfferta=session['corsiInOfferta']
                corsi=request.form.getlist('corsi')
            except:
                flash('Bisogna effettuare almeno una selezione nelle precedenti sezioni!', 'warning')

            if len(corsi)>0:
                importDatiEsse3(request.form.get('anniAccademici'),request.form.getlist('corsi'), request.form.get('semestre'),
                                request.form.get('cbSovrDatiCorsi'),request.form.get('cbSovrDatiAD'), request.form.get('cbSovrDatiDocenti'),
                                request.form.get('cbSovrDatiOfferta'),request.form.get('cbImportaADObbligatorie'),request.form.get('cbImportaDatiIncompleti'),
                                request.form.get('moduli'))
            else:
                flash('Selezionare almeno un corso da importare!', 'warning')

            return render_template("utility_esse3.html",
                                   base_template=appbuilder.base_template,
                                   appbuilder=appbuilder,
                                   anniAccademici=anniAccademici,
                                   annoAccademicoSelezionato=request.form.get('anniAccademici'),
                                   corsiInOfferta=corsiInOfferta)

        return render_template("utility_esse3.html", base_template=appbuilder.base_template, appbuilder=appbuilder)


class PreferenzeView(BaseView):
    default_view = 'prf_home'

    @expose('/prf_home/', methods=['GET','POST'])
    @has_access
    def prf_home(self):
        anni_accademici=db.session.query(AnnoAccademico.id, AnnoAccademico.anno, AnnoAccademico.anno_esteso)\
        .join(Offerta, Offerta.anno_accademico_id==AnnoAccademico.id).distinct()
        semestri=db.session.query(Offerta.semestre).distinct()
        return render_template("preferences.html",
                                base_template=appbuilder.base_template, 
                                appbuilder=appbuilder,
                                anni_accademici=anni_accademici, 
                                semestri=semestri)
    
    @expose('/prf_calc/', methods=['GET','POST'])
    @has_access
    def prf_calc(self):
        target = request.form.get("target")
        if target=="genera_orario" :
            algoritmo=AlgoritmoCompleto()
            algoritmo.genera_orario(request.form.get('aa'),
                                    request.form.get('semestre'),
                                    request.form.get('txt_desc_orario'))
        return redirect(url_for('PreferenzeView.prf_home'));  


class SchemaSettimanaleView(BaseView):
    default_view = 'wsk_home'

    @expose('/wsk_home/')
    @has_access
    def wsk_home(self, name=None):
        slot=db.session.query(Slot).all()
        orario=db.session.query(Orario).all()
        return render_template("timetable.html",
                               base_template=appbuilder.base_template,
                               appbuilder=appbuilder,
                               slot=slot,
                               orario=orario)


class CalendarioView(BaseView):
    default_view = 'cld_home'

    @expose('/cld_home/')
    @has_access
    def cld_home(self, name=None):
        corsi = db.session.query(Orario.corso_id, Orario.codice_corso, CorsoDiStudio.descrizione) \
            .join(CorsoDiStudio, Orario.corso_id == CorsoDiStudio.id) \
            .order_by(CorsoDiStudio.codice.asc()).distinct().all()

        anni_corso = db.session.query(Orario.corso_id, Orario.codice_corso, Orario.anno_corso)\
            .order_by(Orario.corso_id.asc(), Orario.anno_corso.asc()).distinct().all()
        vAnniCorso = []
        for a in anni_corso:
            vAnniCorso.append({"corso_id":a[0],"codice_corso":a[1],"anno_corso":a[2]})

        orario = db.session.query(Orario).all()
        vOrario = []
        for o in orario:
            vOrario.append(o.to_dict())

        chiusure = db.session.query(Chiusura).filter(Chiusura.testata_id==Orario.testata_id).all()
        vChiusure = []
        for c in chiusure:
            cur = c.data_inizio
            end = c.data_fine + timedelta(days=1)
            while (cur<end):
                if cur.strftime('%Y/%m/%d') not in vChiusure:
                    vChiusure.append(cur.strftime('%Y/%m/%d'))
                cur = cur + timedelta(days=1)

        return render_template("calendar.html",
                               base_template=appbuilder.base_template,
                               appbuilder=appbuilder,
                               corsi=corsi,
                               anni_corso=vAnniCorso,
                               orario=vOrario,
                               chiusure=vChiusure)

db.create_all()

appbuilder.add_view(SlotView, "Slot", icon="fa-clock-o", category="Tabelle di base")

appbuilder.add_view(GiorniView, "Giorni", icon="fa-calendar-check-o", category="Tabelle di base")

appbuilder.add_separator("Tabelle di base")

appbuilder.add_view(AnniAccademiciView, "Anni Accademici", icon="fa-font", category="Tabelle di base")

appbuilder.add_view(AuleView, "Aule", icon="fa-th", category="Tabelle di base")

appbuilder.add_view(CorsiDiStudioView, "Corsi di Studio", icon="fa-pencil", category="Didattica")

appbuilder.add_view(NumerositaAnniCorsoView, "Numerosità anni corso", icon="fa-users", category="Didattica")

appbuilder.add_view(DocentiView, "Docenti", icon="fa-user-circle", category="Didattica")

appbuilder.add_view(AttivitaDidatticheView, "Attività didattiche", icon="fa-book", category="Didattica")

appbuilder.add_view(OffertaView, "Offerta", icon="fa-university", category="Offerta didattica")

appbuilder.add_view(ModuliView, "Moduli", icon="fa-puzzle-piece", category="Offerta didattica")

appbuilder.add_view(LogisticaDocentiView, "Logistica docenti", icon="fa-hand-o-up", category="Offerta didattica")

appbuilder.add_view(UtilitaView, "Funzioni utilità",  icon="fa-briefcase", category="Utilità")

appbuilder.add_view(UtilitaEsse3View, "Connettore Esse3",  icon="fa-share-square", category="Utilità")

appbuilder.add_view(PreferenzeView, "Elaborazione orario",  icon="fa-cogs", category="Orario")

appbuilder.add_view(OrariGeneratiView, "Orari generati",  icon="fa-table", category="Orario")

appbuilder.add_view(ChiusuraView, "Imposta chiusure", icon="fa-home", category="Orario")

appbuilder.add_view(SchemaSettimanaleView, "Schema settimanale",  icon="fa-calendar", category="Orario")

appbuilder.add_view(CalendarioView, "Calendario orario",  icon="fa-clipboard", category="Orario")

