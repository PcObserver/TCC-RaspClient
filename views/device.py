from uuid import UUID
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.device import Device
from models.brand import Brand
from application import db
from utils.network import list_available_devices
import json

device_blueprint = Blueprint("device", __name__)

@device_blueprint.route("/api/devices")
def list_devices_api():
    devices = Device.query.all()
    return {"devices": [device.to_select2_dict() for device in devices]}

@device_blueprint.route("/device/find", methods=["GET", "POST"])
def find_devices():
    if request.method == "GET":
        context = {
            "devices": list_available_devices()
        }
        print(context)
        return render_template("device/find.html", **context)
    elif request.method == "POST":
        context = {
            "device": dict(json.loads(request.form.get("device")))
        }
        print(context)
        return redirect(url_for("user_device.list_registered_devices", **context))
    
@device_blueprint.route("/device/add", methods=["GET", "POST"])
def add_device():
    if request.method == "GET":
        context = {
            "brands": Brand.query.all()
        }
        return render_template("device/add.html", **context)
    elif request.method == "POST":
        name = request.form.get("name")
        brand_id = request.form.get("brand_id")
        device = Device(name=name, brand_id=brand_id)
        db.session.add(device)
        db.session.commit()
        return redirect(url_for("user_device.list_registered_devices"))


@device_blueprint.route("/device/register", methods=["GET", "POST"])
def create_device():
    if request.method == "GET":
        if not request.args.get('brand_id'):
            flash("Selecione uma marca", "error")
            return redirect(url_for("device.find_devices"))
        context = {
            "brand": Brand.query.get(UUID(request.args.get('brand_id')))
        }
        return render_template("device/register.html", **context)
    elif request.method == "POST":
        name = request.form.get("name")
        brand_id = request.form.get("brand_id")
        description = request.form.get("device_description")
        device = Device(brand_id=UUID(brand_id), name=name, description=description)
        db.session.add(device)
        db.session.commit()
        return redirect(url_for("device.list_devices_by_brand", brand_id=brand_id, selected_device=device.id))


@device_blueprint.route("/brand/devices")
def list_devices_by_brand():
    context = {
        "devices": Device.query.filter_by(brand_id=UUID(request.args.get('brand_id'))).all(),
        "brand_id": request.args.get('brand_id')
    }

    return render_template("device/devices.html", **context)