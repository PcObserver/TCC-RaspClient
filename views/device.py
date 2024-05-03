from flask import Blueprint, render_template
from models.device import Device
from models.brand import Brand

device_blueprint = Blueprint("device", __name__)

@device_blueprint.route("/devices")
def list_registered_devices():
    devices = Device.query.all()
    return render_template("device/index.html", devices=devices)


@device_blueprint.route("/device/register")
def register_device():
    return render_template("device/register.html")