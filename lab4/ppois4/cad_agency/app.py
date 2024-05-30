from time import strptime

from flask import render_template, request, jsonify
from flask_bootstrap import Bootstrap
from cad_agency import get_app, service, Region
from cad_agency.model.entity.building import Building
from cad_agency.model.entity.cadastral_number import CadastralNumber
from cad_agency.model.entity.land_plot import LandPlot
from cad_agency.model.entity.owner import Owner
from cad_agency.validator.building_validator import BuildingValidator
from cad_agency.validator.land_plot_validator import LandPlotValidator
from cad_agency.validator.owner_validator import OwnerValidator
import atexit

app = get_app()
bootstrap = Bootstrap(app)
current_owner = None
atexit.register(service.save_all)


@app.route('/')
def main_menu():
    global current_owner
    current_owner = None
    return render_template('index.html')


@app.route('/authenticate_user', methods=['POST', 'GET'])
def authenticate_user():
    owners_ids = [o.passport_id for o in service.registered_owners]
    data = request.get_json()
    if data["passport_id"] in owners_ids:
        global current_owner
        current_owner = service.get_owner_by_id(data["passport_id"])
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})


@app.route('/submit_owner_form', methods=['POST', 'GET'])
def submit_owner_form():
    validator = OwnerValidator()
    try:
        pass_id = validator.validate_passport_id(request.form['passport_id'])
        name = validator.validate_name_or_surname(request.form['name'])
        surname = validator.validate_name_or_surname(request.form['surname'])
    except ValueError as e:
        return jsonify({"error": str(e)})
    service.register_owner(Owner(pass_id, name, surname))
    return jsonify("Registration successful")


@app.route('/owner_registration')
def owner_registration():
    return render_template('owner_registration.html')


@app.route('/update_region', methods=['POST', "GET"])
def update_region():
    data = request.get_json()
    match data["region"]:
        case "Grodno":
            service.current_region = Region.GRODNO
        case "Minsk":
            service.current_region = Region.MINSK
        case "Minsk Region":
            service.current_region = Region.MINSK_RG
        case "Gomel":
            service.current_region = Region.GOMEL
        case "Mogilev":
            service.current_region = Region.MOGILEV
        case "Vitebsk":
            service.current_region = Region.VITEBSK
        case "Brest":
            service.current_region = Region.BREST
    print("LOL")
    return jsonify("Region updated")


@app.route('/land_plot_registration')
def land_plot_registration():
    return render_template('land_plot_registration.html', current_region={
        "name": service.current_region.name,
        "terr_blocks": service.current_region.value["blocks"]
    })


@app.route('/unregister_land_plot', methods=['POST', "GET"])
def unregister_land_plot():
    land_docs = service.get_owner_land_documents(current_owner)
    land_plots = [doc.land_plot.to_dict() for doc in land_docs]
    if request.method == "POST":
        data = request.get_json()
        for doc in land_docs:
            if doc.land_plot.cadastral_number == data["land_plot_cad_num"]:
                service.unregister_land_plot(doc)
            return jsonify({"unregistered": True})
    return render_template("owner_land_plots.html",
                           land_plots=land_plots)


@app.route('/pick_unowned_land_plot', methods=['POST', "GET"])
def pick_unowned_land_plot():
    unowned_lands = [land.to_dict() for land in service.unregistered_land_plots]
    if request.method == "POST":
        data = request.get_json()
        for land in service.unregistered_land_plots:
            if land.cadastral_number == data["land_plot_cad_num"]:
                service.register_land_plot(land, current_owner)
                return jsonify({"owned": True})
    return render_template("unowned_land_plots.html", unowned_lands=unowned_lands)


@app.route('/submit_land_form', methods=['POST', 'GET'])
def submit_land_form():
    validator = LandPlotValidator()
    try:
        cad_number = CadastralNumber(service.current_region, int(request.form['land_plot_number']))
        coordinates = validator.validate_coordinates(request.form['coordinates'])
        area_in_hectares = validator.validate_area(request.form['area_in_hectares'])
        func_purpose = request.form['func_purpose']
        cad_number.cadastral_block_number = int(request.form['cadastral_block_number'])
        land = LandPlot(coordinates, area_in_hectares, func_purpose)
        land.cadastral_number = str(cad_number)
    except ValueError as e:
        return jsonify({"error": str(e)})
    service.register_land_plot(land, current_owner)
    return jsonify("Registration successful")


@app.route('/building_registration')
def building_registration():
    land_docs = service.get_owner_land_documents(current_owner)
    land_plots = [doc.land_plot.to_dict() for doc in land_docs]
    return render_template('building_registration.html',
                           current_region={
                               "name": service.current_region.name,
                           }, land_plots=land_plots)


@app.route('/submit_building_form', methods=['POST'])
def submit_building_form():
    validator = BuildingValidator()
    try:
        land_docs = service.get_owner_land_documents(current_owner)
        land = None
        for doc in land_docs:
            if doc.land_plot.cadastral_number == request.form['land_cad_num']:
                land = doc.land_plot
        name = validator.validate_building_name(request.form["name"])
        build_date = strptime(request.form['build_date'], "%d.%m.%Y")
        sq_area = validator.validate_area_in_square_meters(request.form['area_in_sq_m'], land)
        floors = validator.validate_floors(request.form['floors'])
    except ValueError as e:
        return jsonify({"error": str(e)})
    service.register_building(Building(name, land, build_date, sq_area, floors), current_owner)
    return jsonify("Registration successful")


@app.route('/unregister_building_form', methods=['POST', "GET"])
def unregister_building():
    build_docs = service.get_owner_building_documents(current_owner)
    buildings = [doc.building.to_dict() for doc in build_docs]
    if request.method == "POST":
        data = request.get_json()
        for doc in build_docs:
            if doc.building.name == data["build_name"]:
                service.unregister_building(doc)
            return jsonify({"unregistered": True})
    return render_template("owner_buildings.html",
                           buildings=buildings)


@app.route('/documents_and_information', methods=['POST', "GET"])
def documents_and_information():
    land_plots = [plot.to_dict() for plot in service.registered_land_plots]
    u_land_plots = [plot.to_dict() for plot in service.unregistered_land_plots]
    buildings = [building.to_dict() for building in service.registered_buildings]
    docs = [doc.to_dict() for doc in service.get_owner_documents(current_owner)]
    if request.method == "POST":
        data = request.get_json()
        for doc in service.get_owner_documents(current_owner):
            info: str = data["reg_info"]
            if doc.to_dict()["info"].split(':')[1] == info.split(':')[1]:
                doc.update()
                return jsonify({"updated": True})
    return render_template('info_and_docs.html',
                           land_plots=land_plots,
                           buildings=buildings,
                           registrations=docs,
                           u_land_plots=u_land_plots)


if __name__ == '__main__':
    app.run()
