from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller, form_controller
from model.hierarchy_taxon import Hierarchy_Taxon
from model.data_treatment import Data_Treatment
import json

Check_Data = Data_Treatment()
used_sheet = home_controller.used_sheet

taxon_blueprint = Blueprint("taxon", __name__, template_folder="templates")

@taxon_blueprint.route("/taxon_list", methods=["GET", "POST"])
def taxon_list():
    if request.method == "POST":
        titles = request.form["selection"]
        if("null" in titles):
            titles = titles.replace("null", "None")
        titles = eval(titles)
        used_sheet.set_Check_Columns(titles)
        used_sheet.data_treatment.Verified_Hierarchy(used_sheet.get_Columns_Checked())
        verification = json.dumps(used_sheet.data_treatment.get_Verified_Hierarchy())
        return render_template("list/taxon_list_gbif.html", verification=verification, total_rows=used_sheet.get_Row_Total())

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

        kingdom_value = base_sheet.Value_in_Column(titles_base["kingdom"])
        phylum_value = base_sheet.Value_in_Column(titles_base["phylum"])
        class_value = base_sheet.Value_in_Column(titles_base["class"])
        order_value = base_sheet.Value_in_Column(titles_base["order"])
        family_value = base_sheet.Value_in_Column(titles_base["family"])
        genus_value = base_sheet.Value_in_Column(titles_base["genus"])
        specie_value = base_sheet.Value_in_Column(titles_base["specie"])

        check_kingdom_value = used_sheet.Value_in_Column(titles_check["kingdom"])
        check_phylum_value = used_sheet.Value_in_Column(titles_check["phylum"])
        check_class_value = used_sheet.Value_in_Column(titles_check["class"])
        check_order_value = used_sheet.Value_in_Column(titles_check["order"])
        check_family_value = used_sheet.Value_in_Column(titles_check["family"])
        check_genus_value = used_sheet.Value_in_Column(titles_check["genus"])
        check_specie_value = used_sheet.Value_in_Column(titles_check["specie"])

        base_classification_taxon = {}
        for x in range(len(specie_value)):
            scientific_name = "{} {}".format(genus_value[x], specie_value[x])
            if scientific_name not in base_classification_taxon:
                base_classification_taxon[scientific_name] = {
                                                         "kingdom": kingdom_value[x],
                                                         "phylum" : phylum_value [x],
                                                         "class"  : class_value  [x],
                                                         "order"  : order_value  [x],
                                                         "family" : family_value [x],
                                                         "genus"  : genus_value  [x],
                                                         "specie" : specie_value [x]
                                                        }
        check_classification_taxon = {}
        for x in range(len(check_specie_value)):
            scientific_name = "{} {}".format(check_genus_value[x], check_specie_value[x])
            if scientific_name not in check_classification_taxon:
                check_classification_taxon[scientific_name] = {
                                                         "kingdom": check_kingdom_value[x],
                                                         "phylum" : check_phylum_value [x],
                                                         "class"  : check_class_value  [x],
                                                         "order"  : check_order_value  [x],
                                                         "family" : check_family_value [x],
                                                         "genus"  : check_genus_value  [x],
                                                         "specie" : check_specie_value [x]
                                                        }
        Fuzzy_Find = {}
        for specie in check_classification_taxon:
            sn_score = Check_Data.String_Similarity_2(specie, base_classification_taxon.keys())
            def Same(a):
                if a[1] > 60:
                    return a
            sn_score = list(filter(Same, sn_score))
            if len(sn_score) > 0:
                key = sn_score[0][0]
                kingdom_score = "FUZZY"
                phylum_score  = "FUZZY"
                class_score   = "FUZZY"
                order_score   = "FUZZY"
                family_score  = "FUZZY"
                genus_score   = "FUZZY"
                specie_score  = "FUZZY"

                kingdom_suggest = []
                phylum_suggest  = []
                class_suggest   = []
                order_suggest   = []
                family_suggest  = []
                genus_suggest   = []
                specie_suggest  = []

                for i in sn_score:
                    if check_classification_taxon[specie]["kingdom"] == base_classification_taxon[i[0]]["kingdom"]:
                        kingdom_score = "EXACT"
                    else:
                        kingdom_suggest.append(base_classification_taxon[i[0]]["kingdom"])

                    if check_classification_taxon[specie]["phylum"] == base_classification_taxon[i[0]]["phylum"]:
                        phylum_score = "EXACT"
                    else:
                        phylum_suggest.append(base_classification_taxon[i[0]]["phylum"])

                    if check_classification_taxon[specie]["class"] == base_classification_taxon[i[0]]["class"]:
                        class_score = "EXACT"
                    else:
                        class_suggest.append(base_classification_taxon[i[0]]["class"])

                    if check_classification_taxon[specie]["order"] == base_classification_taxon[i[0]]["order"]:
                        order_score = "EXACT"
                    else:
                        order_suggest.append(base_classification_taxon[i[0]]["order"])
                    if check_classification_taxon[specie]["family"] == base_classification_taxon[i[0]]["family"]:
                        family_score = "EXACT"
                    else:
                        family_suggest.append(base_classification_taxon[i[0]]["family"])

                    if check_classification_taxon[specie]["genus"] == base_classification_taxon[i[0]]["genus"]:
                        genus_score = "EXACT"
                    else:
                        genus_suggest.append(base_classification_taxon[i[0]]["genus"])

                    if check_classification_taxon[specie]["specie"] == base_classification_taxon[i[0]]["specie"]:
                        specie_score = "EXACT"
                    else:
                        specie_suggest.append(base_classification_taxon[i[0]]["specie"])

                Fuzzy_Find[specie] = {
                "kingdom": {"amount": check_kingdom_value.count(check_classification_taxon[specie]["kingdom"]),
                            "correctness": kingdom_score,
                            "suggestion": kingdom_suggest,
                            "title": titles_check["kingdom"],
                            "type": check_classification_taxon[specie]["kingdom"]},

                "phylum": {"amount": check_phylum_value.count(check_classification_taxon[specie]["phylum"]),
                            "correctness": phylum_score,
                            "suggestion": phylum_suggest,
                            "title": titles_check["phylum"],
                            "type": check_classification_taxon[specie]["phylum"]},

                "class": {"amount": check_class_value.count(check_classification_taxon[specie]["class"]),
                            "correctness": class_score,
                            "suggestion": class_suggest,
                            "title": titles_check["class"],
                            "type": check_classification_taxon[specie]["class"]},

                "order": {"amount": check_order_value.count(check_classification_taxon[specie]["order"]),
                            "correctness": order_score,
                            "suggestion": order_suggest,
                            "title": titles_check["order"],
                            "type": check_classification_taxon[specie]["order"]},

                "family": {"amount": check_family_value.count(check_classification_taxon[specie]["family"]),
                            "correctness": family_score,
                            "suggestion": family_suggest,
                            "title": titles_check["family"],
                            "type": check_classification_taxon[specie]["family"]},

                "genus": {"amount": check_genus_value.count(check_classification_taxon[specie]["genus"]),
                            "correctness": genus_score,
                            "suggestion": genus_suggest,
                            "title": titles_check["genus"],
                            "type": check_classification_taxon[specie]["genus"]},

                "specie": {"amount": check_specie_value.count(check_classification_taxon[specie]["specie"]),
                            "correctness": specie_score,
                            "suggestion": specie_suggest,
                            "title": titles_check["specie"],
                            "type": check_classification_taxon[specie]["specie"]},

                "scientific name": {"correctness": "100%",
                                    "font": "Planilha",
                                    "suggestion": "NONE",
                                    "synonymous": "false",
                                    "type": specie},
                }

            else:
                kingdom_score = "Not found"
                phylum_score  = "Not found"
                class_score   = "Not found"
                order_score   = "Not found"
                family_score  = "Not found"
                genus_score   = "Not found"
                specie_score  = "Not found"
                precision     = "Not found"

                Fuzzy_Find[specie] = {
                    "kingdom": {"amount": check_kingdom_value.count(check_classification_taxon[specie]["kingdom"]),
                                "correctness": kingdom_score,
                                "suggestion": "",
                                "title": titles_check["kingdom"],
                                "type": check_classification_taxon[specie]["kingdom"]},

                    "phylum": {"amount": check_phylum_value.count(check_classification_taxon[specie]["phylum"]),
                               "correctness": phylum_score,
                               "suggestion": "",
                               "title": titles_check["phylum"], "type": check_classification_taxon[specie]["phylum"]},

                    "class": {"amount": check_class_value.count(check_classification_taxon[specie]["class"]),
                              "correctness": class_score,
                              "suggestion": "",
                              "title": titles_check["class"], "type": check_classification_taxon[specie]["class"]},

                    "order": {"amount": check_order_value.count(check_classification_taxon[specie]["order"]),
                              "correctness": order_score,
                              "suggestion": "",
                              "title": titles_check["order"], "type": check_classification_taxon[specie]["order"]},

                    "family": {"amount": check_family_value.count(check_classification_taxon[specie]["family"]),
                               "correctness": family_score,
                               "suggestion": "",
                               "title": titles_check["family"],
                               "type": check_classification_taxon[specie]["family"]},

                    "genus": {"amount": check_genus_value.count(check_classification_taxon[specie]["genus"]),
                              "correctness": genus_score,
                              "suggestion": "",
                              "title": titles_check["genus"],
                              "type": check_classification_taxon[specie]["genus"]},

                    "specie": {"amount": check_specie_value.count(check_classification_taxon[specie]["specie"]),
                               "correctness": specie_score,
                               "suggestion": "",
                               "title": titles_check["specie"],
                               "type": check_classification_taxon[specie]["specie"]},

                    "scientific name": {"correctness": precision,
                                        "font": "Planilha",
                                        "suggestion": "NONE",
                                        "synonymous": "false",
                                        "type": specie},
                }
        used_sheet.data_treatment.set_Verified_Hierarchy(Fuzzy_Find)
        Fuzzy_Find  = json.dumps(Fuzzy_Find)
        return render_template("list/taxon_list_localsheet.html", verification=Fuzzy_Find, total_rows=used_sheet.get_Row_Total())