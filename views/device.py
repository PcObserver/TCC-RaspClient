from uuid import UUID
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.device import Device
from models.brand import Brand
from application import db, api
from sqlalchemy.orm import joinedload
from data.device_dto import DeviceDTO
from data.brand_dto import BrandDTO
from data.action_dto import ActionDTO
from utils.db import get_or_create
from models.author import Author


device_blueprint = Blueprint("device", __name__)


@device_blueprint.route("/devices/remote/", methods=["GET"])
def list_remote():
    try:
        response = api.list_devices(page=request.args.get("page", 1))
        imported_devices = [
            str(device.contribution_id)
            for device in Device.query.filter(Device.contribution_id.isnot(None))
        ]
        context = {
            "devices": [
                DeviceDTO(**result)
                for result in response["results"]
                if result["id"] not in imported_devices
            ],
            "next_page": response["next"],
            "previous_page": response["previous"],
        }
        return render_template("device/remote.html", **context)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("device/remote.html")


@device_blueprint.route("/devices/import/<device_id>", methods=["GET"])
def import_remote(device_id):
    try:
        response = DeviceDTO(**api.get_device(device_id))
        device = response.parse()
        get_or_create(db.session, Author, **response.user.parse().to_dict())

        response = BrandDTO(**api.get_brand(device.brand_id))
        brand = response.parse().to_dict()
        brand.pop("id")
        brand, was_created = get_or_create(db.session, Brand, **brand)
        device.brand_id = brand.id
        db.session.add(device)

        response = api.list_actions(q={"parent_device": device_id})
        actions = [ActionDTO(**result).parse() for result in response["results"]]
        db.session.add_all(actions)

        db.session.commit()
        flash("Device imported successfully", "success")
        return redirect(url_for("device.list_remote"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("device.list_remote"))


@device_blueprint.route("/devices")
def list_devices():
    context = {"devices": [device.to_select2_dict() for device in Device.query.all()]}
    return jsonify(context)


@device_blueprint.route("/devices/index")
def index():
    context = {"devices": Device.query.all()}
    return render_template("device/index.html", **context)


@device_blueprint.route("/device", methods=["GET"])
def new():
    context = {
        "brands": Brand.query.all(),
        "selected_brand_id": (
            UUID(request.args.get("brand_id")) if request.args.get("brand_id") else None
        ),
    }
    return render_template("device/new.html", **context)


@device_blueprint.route("/device", methods=["POST"])
def create():
    try:

        device_data = {
            "name": request.form.get("name"),
            "brand_id": UUID(request.form.get("brand_id")),
            "description": request.form.get("device_description"),
            "prefix": request.form.get("device_prefix"),
        }
        device = Device(**device_data)
        db.session.add(device)
        db.session.commit()
        if request.form.get("is_public"):
            brand = Brand.query.get(device.brand_id)
            if brand and not api.brand_exists(brand.contribution_id):
                response = BrandDTO(api.publish_brand(brand.to_dict()))
                brand.contribution_id = response.id
                author, was_created = get_or_create(
                    db.session, Author, **response.user.parse().to_dict()
                )
                brand.author_id = author.id
                db.session.add(brand)
                db.session.commit()

            response = DeviceDTO(**api.publish_device(device.to_dict()))
            author, was_created = get_or_create(
                db.session, Author, **response.user.parse().to_dict()
            )
            device.contribution_id = response.id
            device.author_id = author.id
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
        device.prefix = request.form.get("device_prefix")
        db.session.commit()

        if request.form.get("is_public"):
            brand = Brand.query.get(device.brand_id)
            if brand and not api.brand_exists(brand.contribution_id):
                response = BrandDTO(api.publish_brand(brand.to_dict()))
                brand.contribution_id = response.id
                author, was_created = get_or_create(
                    db.session, Author, **response.user.parse().to_dict()
                )
                brand.author_id = author.id
                db.session.add(brand)
                db.session.commit()

            response = DeviceDTO(**api.create_or_update_device(device.to_dict()))
            author, was_created = get_or_create(
                db.session, Author, **response.user.parse().to_dict()
            )
            device.contribution_id = response.id
            device.author_id = author.id
            db.session.commit()

        flash("Device updated successfully", "success")
        return redirect(url_for("device.show", device_id=device.id))
    except Exception as e:
        flash(str(e), "danger")
        return render_template(
            "device/show.html", device=Device.query.get(UUID(device_id))
        )


@device_blueprint.route("/device/<device_id>", methods=["DELETE"])
def delete(device_id):
    try:
        device = Device.query.get(UUID(device_id))
        if request.form.get("is_public") == "true" and api.device_exists(
            device.contribution_id
        ):
            api.delete_device(device.contribution_id)

        db.session.delete(device)
        db.session.commit()
        flash("Device deleted successfully", "success")
        return redirect(url_for("device.index"), code=303)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("device.show", device_id=device_id), code=303)
