from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller
import json

Planilha_atual = home_controller.Planilha_atual
taxon_blueprint = Blueprint('taxon', __name__, template_folder='templates')

@taxon_blueprint.route("/taxon_list", methods=["GET", "POST"])
def taxon_list():
    if request.method == "POST":
        titulos = request.form["selecao"]
        if("null" in titulos):
            titulos = titulos.replace("null","None")
        titulos = eval(titulos)
        Planilha_atual.set_Colunas_para_verificar(titulos)
        Planilha_atual.tratamento_de_dados.set_Hierarquia_verificada(Planilha_atual.get_Colunas_para_verificar())
        verificacao = json.dumps(Planilha_atual.tratamento_de_dados.get_Hierarquia_verificada())
        return render_template("list/taxon_list.html", verificacao=verificacao, total_linhas = Planilha_atual.get_Total_de_linhas())

@taxon_blueprint.route("/taxon_validation", methods=["GET", "POST"])
def taxon_validation():
    if request.method == "POST":
        dados = request.form["dados"]
        dados = eval(dados)
        Planilha_atual.AlterandoDadosPlanilha(dados)
        Planilha_atual.SalvarPlanilhaFormatada()
        return redirect(url_for("home.home"))