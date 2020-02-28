from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename

from controller import home_controller
from model.sheet_treatment import Sheet

used_sheet = home_controller.used_sheet
base_sheet = Sheet()
form_blueprint = Blueprint('form', __name__, template_folder='templates')


@form_blueprint.route("/taxon_form", methods=["GET", "POST"])
def taxon_form():
    if request.method == 'GET':
        return render_template("form/taxon_form_gbif.html", titles=used_sheet.get_Sheet_Header())

@form_blueprint.route("/taxon_form2", methods=["GET", "POST"])
def taxon_form2():
    if request.method == 'POST':
        f = request.files['file']
        if (".xls" in f.filename):
            f.save("files/"+secure_filename(f.filename))
            base_sheet.set_Path(secure_filename(f.filename))
            return render_template("form/taxon_form_localsheet.html", titles_check=used_sheet.get_Sheet_Header(), titles_base=base_sheet.get_Sheet_Header())
        else:
            return render_template("errorscreen/InvalidFile.html")

@form_blueprint.route("/coord_form", methods=["GET", "POST"])
def coord_form():
    if request.method == 'GET':
        return render_template("form/markers_form.html", titles=used_sheet.get_Sheet_Header())
