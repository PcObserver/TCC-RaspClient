from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.network import list_available_devices
from models.user_device import UserDevice
from models.action import Action, RequestMethod
from application import db
from uuid import UUID
import requests
import json

user_device_blueprint = Blueprint("user_device", __name__)


@user_device_blueprint.route("/user_device", methods=["GET"])
def new():
    context = {
        "devices": list_available_devices()
    }
    return render_template("user_device/new.html", **context)


@user_device_blueprint.route("/user_device", methods=["POST"])
def create():
    try:
        hostname = request.form.get("hostname")
        nickname = request.form.get("nickname")
        device_model_id = request.form.get("model")
        port = request.form.get("port")
        address = request.form.get("address")
        user_device = UserDevice(hostname=hostname, nickname=nickname, device_id=UUID(device_model_id), user_id=None, port=port, address=address)
        db.session.add(user_device)
        db.session.commit()

        flash("Device created successfully", "success")
        return redirect(url_for("application.home"))
    except Exception as e:

        flash(e)
        return render_template("user_device/new.html")
    

@user_device_blueprint.route("/user_device/<user_device_id>")
def show(user_device_id):
    user_device = UserDevice.query.get(UUID(user_device_id))
    context = {
        "user_device": user_device,
        "commands": Action.query.filter_by(device_id=user_device.device_id).all()
    }
    return render_template("user_device/show.html", **context)


@user_device_blueprint.route("/user_device/<user_device_id>", methods=["PUT"])
def update(device_id):
    try:
        user_device = UserDevice.query.get(UUID(device_id))
        user_device.hostname = request.form.get("hostname")
        user_device.nickname = request.form.get("nickname")
        user_device.device_id = UUID(request.form.get("model"))
        user_device.port = request.form.get("port")
        user_device.address = request.form.get("address")
        db.session.commit()
        flash("Device updated successfully", "success")
        return redirect(url_for("user_device.show", device_id=user_device.id))
    except Exception as e:
        flash(e)
        return redirect(url_for("user_device.show", device_id=user_device.id))
    

@user_device_blueprint.route("/user_device/<user_device_id>", methods=["DELETE"])
def delete(device_id):
    try:
        user_device = UserDevice.query.get(UUID(device_id))
        db.session.delete(user_device)
        db.session.commit()
        flash("Device deleted successfully", "success")
        return redirect(url_for("user_device.list_user_devices"))
    except Exception as e:
        flash(e)
        return redirect(url_for("user_device.list_user_devices"))


@user_device_blueprint.route("/user_device/<user_device_id>/action/<action_id>/", methods=["GET"])
def call_action(user_device_id, action_id):
    action = Action.query.get(UUID(action_id))
    device = UserDevice.query.get(UUID(user_device_id))

    url = f"http://{device.address}:{device.port}{action.path}"
    if action.request_method == RequestMethod.GET:
        response = requests.get(url)
    else:
        payload = json.loads(action.payload.replace('\r\n', ''))
        response = requests.post(url, data=payload)

    flash(f"Action {action.name} called on device {device.nickname} with response {response.text}")    
    return redirect(url_for("user_device.show", user_device_id=user_device_id))