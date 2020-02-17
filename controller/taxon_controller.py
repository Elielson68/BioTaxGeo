from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller, form_controller
from model.hierarchy_taxon import Hierarchy_Taxon
from model.data_treatment import Data_Treatment
import json

Check_Data = Data_Treatment()
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

@taxon_blueprint.route("/taxon_list2", methods=["GET", "POST"])
def taxon_list2():
    if request.method == "POST":
        base_sheet = form_controller.base_sheet
        titles_check = request.form["selection_check"]
        titles_base = request.form["selection_base"]
        if("null" in titles_check):
            titles_check = titles_check.replace("null", "None")
        if("null" in titles_base):
            titles_base = titles_base.replace("null", "None")
        titles_check = eval(titles_check)
        titles_base = eval(titles_base)
        kingdom_value = base_sheet.Value_in_Column(titles_base['kingdom'])
        phylum_value = base_sheet.Value_in_Column(titles_base['phylum'])
        class_value = base_sheet.Value_in_Column(titles_base['class'])
        order_value = base_sheet.Value_in_Column(titles_base['order'])
        family_value = base_sheet.Value_in_Column(titles_base['family'])
        genus_value = base_sheet.Value_in_Column(titles_base['genus'])
        specie_value = base_sheet.Value_in_Column(titles_base['specie'])

        check_kingdom_value = used_sheet.Value_in_Column(titles_check['kingdom'])
        check_phylum_value = used_sheet.Value_in_Column(titles_check['phylum'])
        check_class_value = used_sheet.Value_in_Column(titles_check['class'])
        check_order_value = used_sheet.Value_in_Column(titles_check['order'])
        check_family_value = used_sheet.Value_in_Column(titles_check['family'])
        check_genus_value = used_sheet.Value_in_Column(titles_check['genus'])
        check_specie_value = used_sheet.Value_in_Column(titles_check['specie'])

        classification_taxon = {}
        for x in range(len(specie_value)):
            scientific_name = "{} {}".format(genus_value[x], specie_value[x])
            if scientific_name not in classification_taxon:
                classification_taxon[scientific_name] = {
                                                         "kingdom": kingdom_value[x],
                                                         "phylum" : phylum_value [x],
                                                         "class"  : class_value  [x],
                                                         "order"  : order_value  [x],
                                                         "family" : family_value [x],
                                                         "genus"  : genus_value  [x],
                                                         "specie" : specie_value [x]
                                                        }
        Fuzzy_Find = {}
        for specie in check_genus_value:
            score = Check_Data.String_Similarity_2(specie, genus_value)
            if specie not in Fuzzy_Find:
                    Fuzzy_Find[specie] = score
        hierarchy_base = Hierarchy_Taxon(k=kingdom_value, p=phylum_value, c=class_value, o=order_value, f=family_value, g=genus_value, e=specie_value)
        teste = {"kingdom": hierarchy_base.get_Kingdom(), "phylum": hierarchy_base.get_Phylum(), "class": hierarchy_base.get_Classs(),
                 "order": hierarchy_base.get_Order(), "family": hierarchy_base.get_Family(), "genus": hierarchy_base.get_Genus(), "specie": hierarchy_base.get_Specie()
                 }
        return Fuzzy_Find#render_template("list/taxon_list2.html")