from uuid import UUID
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.device import Device
from models.brand import Brand
from application import db, api
from sqlalchemy.orm import joinedload
from data.device_dto import DeviceDTO


device_blueprint = Blueprint("device", __name__)


@device_blueprint.route("/devices/remote/", methods=["GET"])
def list_remote():
    try:
        response = api.list_devices(page=request.args.get("page", 1))
        context = {
            "devices": [DeviceDTO(**result) for result in response["results"]],
            "next_page": response["next"],
            "previous_page": response["previous"]
        }
        return render_template("device/remote.html", **context)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("device/remote.html")
    

@device_blueprint.route("/devices")
def list_devices():
    context = {"devices": [device.to_select2_dict() for device in Device.query.all()]}
    return jsonify(context)


@device_blueprint.route("/devices/index")
def index():
    context = {
        "devices": Device.query.all()
    }
    return render_template("device/index.html", **context)
    

@device_blueprint.route("/device", methods=["GET"])
def new():
    context = {
        "brands": Brand.query.all(),
        "selected_brand_id": UUID(request.args.get("brand_id")) if request.args.get("brand_id") else None
    }
    return render_template("device/new.html", **context)


@device_blueprint.route("/device", methods=["POST"])
def create():
    try:

        device_data = {
            "name": request.form.get("name"),
            "brand_id": UUID(request.form.get("brand_id")),
            "description": request.form.get("device_description")
        }
        device = Device(**device_data)
        if request.form.get("is_public"):
            if not api.brand_exists(device.id):
                brand = Brand.query.get(device.brand_id)
                response = api.publish_brand({"name": brand.name, "prefix": brand.prefix})
                
                brand.id = UUID(response['id'])
                device.brand_id = brand.id
                db.session.add(brand)

            response = api.publish_device(device.to_dict())
            device.id = UUID(response["id"])

        db.session.add(device)
        db.session.commit()
        

        flash("Device created successfully", "success")
        return redirect(url_for("device.show", device_id=device.id))
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("device.new"))


@device_blueprint.route("/device/<device_id>", methods=["GET"])
def show(device_id):
    device = Device.query.options(joinedload(Device.brand)).get(UUID(device_id))
    context = {
        "device": device,
    }
    return render_template("device/show.html", **context)


@device_blueprint.route("/device/<device_id>", methods=["POST"])
def update(device_id):
    try:
        device = Device.query.get(UUID(device_id))
        device.name = request.form.get("name")
        device.description = request.form.get("description")
        device.brand_id = UUID(request.form.get("brand_id"))
        db.session.commit()
        flash("Device updated successfully", "success")
        return redirect(url_for("device.show", device_id=device.id))
    except Exception as e:
        flash(str(e), "danger")
        return render_template('device/show.html', device=Device.query.get(UUID(device_id)))
    

@device_blueprint.route("/device/<device_id>", methods=["DELETE"])
def delete(device_id):
    try:
        device = Device.query.get(UUID(device_id))
        db.session.delete(device)
        db.session.commit()
        flash("Device deleted successfully", "success")
        return redirect(url_for("device.index"), code=303)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("device/show.html", device=Device.query.get(device_id))