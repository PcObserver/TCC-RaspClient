from flask import Blueprint, render_template, request, redirect, url_for
from models.user_device import UserDevice
from models.action import Action
from application import db
from uuid import UUID

user_device_blueprint = Blueprint("user_device", __name__)


@user_device_blueprint.route("/devices")
def list_registered_devices():
    context = {
        "devices": UserDevice.query.all()
    }
    return render_template("device/index.html", **context)


@user_device_blueprint.route("/device/find", methods=["GET", "POST"])
def find_devices():
    return render_template("device/find.html")


@user_device_blueprint.route("/user/device/resgiter", methods=["POST"])
def register_devices():
    if request.method == "POST":
        print(request.form)
        hostname = request.form.get("hostname")
        nickname = request.form.get("nickname")
        device_model_id = request.form.get("model")
        port = request.form.get("port")
        address = request.form.get("address")
        user_device = UserDevice(hostname=hostname, nickname=nickname, device_id=UUID(device_model_id), user_id=None, port=port, address=address)
        db.session.add(user_device)
        db.session.commit()
        return redirect(url_for("user_device.list_registered_devices"))
    
@user_device_blueprint.route("/device/<device_id>")
def show_device(device_id):
    user_device = UserDevice.query.get(UUID(device_id))
    context = {
        "device": user_device,
        "commands": Action.query.filter_by(device_id=user_device.device_id).all()
    }
    return render_template("user_device/show.html", **context)