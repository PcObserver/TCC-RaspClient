from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models.action import Action, RequestMethod, ConnectionProtocol
from models.device import Device
from application import db
import json
from uuid import UUID

action_blueprint = Blueprint("action", __name__)


@action_blueprint.route("/actions", methods=["GET"])
def list_actions(device_id):
    context = {
        "actions": Action.query.filter_by(device_id=UUID(device_id)).all()
    }
    return render_template("action/index.html", **context)

@action_blueprint.route("/actions/index", methods=["GET"])
def index():
    context = {
        "actions": Action.query.all()
    }
    return render_template("action/index.html", **context)


@action_blueprint.route("/action", methods=["GET"])
def new():
    context = {
            "devices": Device.query.all(),
            "selected_device_id":  UUID(request.args.get("device_id")) if request.args.get("device_id") else Device.query.first().id,
            "request_methods": [method.value for method in RequestMethod],
            "connection_protocols": [protocol.value for protocol in ConnectionProtocol]
        }
    return render_template("action/new.html", **context)


@action_blueprint.route("/action", methods=["POST"])
def create():
    try:
        payload_data = request.form.get("payload_data")
        device_id = request.form.get("device_id")
        action = Action(name=request.form.get("name"),
                        description=request.form.get("description"),
                        path=request.form.get("path"), 
                        device_id=UUID(device_id),
                        payload=json.dumps(payload_data), 
                        request_method=request.form.get("request_method"),
                        connection_protocol=request.form.get("connection_protocol")
                        )
        db.session.add(action)
        db.session.commit()
        return redirect(url_for("application.home"))
    except Exception as e:
        flash(e)
        return render_template("action/new.html")


@action_blueprint.route("/action/<action_id>", methods=["GET"])
def show(action_id):
    action = Action.query.get(UUID(action_id))
    context = {
        "action": action
    }
    return render_template("action/show.html", **context)


@action_blueprint.route("/action/<action_id>", methods=["PUT"])
def update(action_id):
    try:
        action = Action.query.get(UUID(action_id))
        action.name = request.form.get("name")
        action.description = request.form.get("description")
        action.path = request.form.get("path")
        action.payload = request.form.get("payload")
        action.request_method = request.form.get("request_method")
        action.connection_protocol = request.form.get("connection_protocol")
        db.session.commit()
        flash("Action updated successfully", "success")
        return redirect(url_for("action.show", action_id=action.id))
    except Exception as e:
        flash(e)
        return redirect(url_for("action.show", action_id=action.id))


@action_blueprint.route("/action/<action_id>", methods=["DELETE"])
def delete(action_id):
    try:
        action = Action.query.get(UUID(action_id))
        db.session.delete(action)
        db.session.commit()
        flash("Action deleted successfully", "success")
        return redirect(url_for("action.index"), code=303)
    except Exception as e:
        flash(str(e), "error")
        return render_template("action/show.html", action=Action.query.get(UUID(action_id)))