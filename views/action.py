from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models.action import Action, RequestMethod, ConnectionProtocol
from application import db
import json
from uuid import UUID
from models.user_device import UserDevice
import requests

action_blueprint = Blueprint("action", __name__)

@action_blueprint.route("/device/<device_id>/action/register", methods=["GET", "POST"])
def register(device_id):
    if request.method == "GET":
        context = {
            "device_id": device_id,
            "request_methods": [method.value for method in RequestMethod],
            "connection_protocols": [protocol.value for protocol in ConnectionProtocol]
        }
        return render_template("action/new.html", **context)
    elif request.method == "POST":
        print(request.form)
        name = request.form.get("name")
        description = request.form.get("description")
        path = request.form.get("path")
        payload_data = request.form.get("payload_data")
        request_method = request.form.get("request_method")
        connection_protocol = request.form.get("connection_protocol")
        action = Action(name=name, description=description, path=path, device_id=UUID(device_id),
                        payload=json.dumps(payload_data), request_method=request_method, connection_protocol=connection_protocol)
        db.session.add(action)
        db.session.commit()
        return redirect(url_for("user_device.list_registered_devices"))
    
@action_blueprint.route("/user_device/<device_id>/action/<action_id>/", methods=["GET"])
def call_action(device_id, action_id):
    action = Action.query.get(UUID(action_id))
    device = UserDevice.query.get(UUID(device_id))

    url = f"http://{device.address}:{device.port}{action.path}"
    if action.request_method == RequestMethod.GET:
        response = requests.get(url)
    else:
        payload = json.loads(action.payload.replace('\r\n', ''))
        response = requests.post(url, data=payload)

    flash(f"Action {action.name} called on device {device.nickname} with response {response.text}")    
    return redirect(url_for("user_device.show_device", device_id=device_id))
