from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller


used_sheet = home_controller.used_sheet
markers_blueprint = Blueprint('markers', __name__, template_folder='templates')

@markers_blueprint .route("/markers_validation", methods=["GET", "POST"])
def markers_validation():
    if request.method == "POST":
        coord = request.form["selection"]
        coord = eval(coord)
        used_sheet.coordinate.set_Latitude_Column_values(coord["latitude"])
        used_sheet.coordinate.set_Longitude_Column_values(coord["longitude"])
        return redirect(url_for("markers.markers_list"))

@markers_blueprint .route("/markers_list",methods=["GET","POST"])
def markers_list():
    if request.method == "POST":
        polygons = request.form['vertices']
        polygons = eval(polygons)
        coord_lat = used_sheet.coordinate.get_Latitude_Column_values()
        coord_lng = used_sheet.coordinate.get_Longitude_Column_values()
        row_coord_lat = used_sheet.coordinate.get_Index_Row_Lat()
        row_coord_lng = used_sheet.coordinate.get_Index_Row_Lng()
        coord_lat = used_sheet.coordinate.Convert_Lat_Decimal(coord_lat)
        coord_lng = used_sheet.coordinate.Convert_Lng_Decimal(coord_lng)
        return render_template("list/markers_list.html", polygons=polygons, latitude=coord_lat, longitude=coord_lng, row_coord_lat=row_coord_lat, row_coord_lng=row_coord_lng)
    else:
        return render_template("form/markers_form.html")
