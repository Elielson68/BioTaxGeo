from flask import render_template, request, Blueprint
from planilha import Planilha
from werkzeug.utils import secure_filename

Planilha_atual = Planilha()

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if(Planilha_atual.get_Diretorio() == None):
            return render_template("index.html")
        else:
            return  render_template("Selecionar_Rota.html")
    if request.method == "POST":
        f = request.files['file']
        f.save("files/"+secure_filename(f.filename))
        Planilha_atual.set_Diretorio(secure_filename(f.filename))
        return render_template("Selecionar_Rota.html")