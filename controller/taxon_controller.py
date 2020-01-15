from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller
import json

used_sheet = home_controller.used_sheet
taxon_blueprint = Blueprint('taxon', __name__, template_folder='templates')

@taxon_blueprint.route("/taxon_list", methods=["GET", "POST"])
def taxon_list():
    if request.method == "POST":
        titles = request.form["selection"]
        if("null" in titles):
            titles = titles.replace("null", "None")
        titles = eval(titles)
        used_sheet.set_Check_Columns(titles)
        used_sheet.data_treatment.set_Verified_Hierarchy(used_sheet.get_Columns_Checked())
        verification = json.dumps(used_sheet.data_treatment.get_Verified_Hierarchy())
        return render_template("list/taxon_list.html", verification=verification, total_rows = used_sheet.get_Row_Total())

@taxon_blueprint.route("/taxon_validation", methods=["GET", "POST"])
def taxon_validation():
    if request.method == "POST":
        data = request.form["data"]
        data = eval(data)
        used_sheet.Change_Data_Spreadsheet(data)
        used_sheet.Save_Formatted_Spreadsheet()
        return redirect(url_for("home.home"))