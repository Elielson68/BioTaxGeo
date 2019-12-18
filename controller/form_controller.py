from flask import render_template, request, Blueprint
from controller import home_controller

Planilha_atual = home_controller.Planilha_atual

form_blueprint = Blueprint('form', __name__, template_folder='templates')


@form_blueprint.route("/taxon_form", methods=["GET", "POST"])
def taxon_form():
    if request.method == 'GET':
        return render_template("form/taxon_form.html", titulos=Planilha_atual.get_Cabecario_Planilha())

@form_blueprint.route("/coord_form", methods=["GET", "POST"])
def coord_form():
    if request.method == 'GET':
        return render_template("form/coord_form.html", titulos=Planilha_atual.get_Cabecario_Planilha())
