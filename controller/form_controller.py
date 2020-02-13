from flask import render_template, request, Blueprint
from controller import home_controller

used_sheet = home_controller.used_sheet

form_blueprint = Blueprint('form', __name__, template_folder='templates')


@form_blueprint.route("/taxon_form", methods=["GET", "POST"])
def taxon_form():
    if request.method == 'GET':
        return render_template("form/taxon_form.html", titles=used_sheet.get_Sheet_Header())

@form_blueprint.route("/taxon_form2", methods=["GET", "POST"])
def taxon_form2():
    if request.method == 'GET':
        return render_template("form/taxon_form2.html", titles=used_sheet.get_Sheet_Header())

@form_blueprint.route("/coord_form", methods=["GET", "POST"])
def coord_form():
    if request.method == 'GET':
        return render_template("form/coord_form.html", titles=used_sheet.get_Sheet_Header())
