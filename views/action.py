from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.action import Action
from application import db
import json
from uuid import UUID

action_blueprint = Blueprint("action", __name__)

@action_blueprint.route("/device/<device_id>/action/register", methods=["GET", "POST"])
def register(device_id):
    if request.method == "GET":
        context = {
            "device_id": device_id
        }
        return render_template("action/new.html", **context)
    elif request.method == "POST":
        print(request.form)
        name = request.form.get("name")
        description = request.form.get("description")
        path = request.form.get("path")
        payload_data = request.form.get("payload_data")
        action = Action(name=name, description=description, path=path, device_id=UUID(device_id), payload=json.dumps(payload_data))
        db.session.add(action)
        db.session.commit()
        return redirect(url_for("user_device.list_registered_devices"))
