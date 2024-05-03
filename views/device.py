from flask import Blueprint, render_template

device_blueprint = Blueprint("device", __name__)


@device_blueprint.route("/devices")
def list_available_devices():
    return render_template("device/index.html")


@device_blueprint.route("/devices/mine")
def list_registered_devices():
    return render_template("device/index.html")


@device_blueprint.route("/device/register")
def register_device():
    return render_template("device/register.html")