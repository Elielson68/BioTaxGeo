from flask import render_template, request, Blueprint
from model.sheet_treatment import Sheet
from werkzeug.utils import secure_filename

used_sheet = Sheet()
base_sheet = Sheet()
home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if(used_sheet.get_Path() == None):
            return render_template("index.html")
        else:
            return  render_template("Selecionar_Rota.html")
    if request.method == "POST":
        f = request.files['file']
        if(".xls" in f.filename):
            f.save("files/"+secure_filename(f.filename))
            used_sheet.set_Path(secure_filename(f.filename))
            return render_template("Selecionar_Rota.html")
        else:
            return render_template("errorscreen/InvalidFile.html")