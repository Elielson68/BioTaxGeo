from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet

base_sheet = Sheet()

form_blueprint = Blueprint('form', __name__, template_folder='templates')


@form_blueprint.route("/taxon_form", methods=["GET", "POST"])
def taxon_form():
    if request.method == 'GET':
        titles_cookie = request.cookies.get("titles_gbif")
        return render_template("form/taxon_form_gbif.html", titles=used_sheet.get_Sheet_Header(), cookies = titles_cookie)

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

@form_blueprint.route("/markers_form", methods=["GET", "POST"])
def markers_form():
    if request.method == 'GET':
        cookies = request.cookies.get("titles_marker")
        return render_template("form/markers_form.html", titles=used_sheet.get_Sheet_Header(), cookies=cookies)
