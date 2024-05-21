from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models.action import Action, RequestMethod, ConnectionProtocol
from models.device import Device
from models.brand import Brand
from models.author import Author
from application import db, api
import json
from uuid import UUID
from data.action_dto import ActionDTO
from data.device_dto import DeviceDTO
from data.brand_dto import BrandDTO
from utils.db import get_or_create

action_blueprint = Blueprint("action", __name__)


@action_blueprint.route("/actions/remote", methods=["GET"])
def list_remote():
    try:
        response = api.list_actions(page=request.args.get("page", 1))
        context = {
            "actions": [ActionDTO(**result) for result in response["results"]],
            "next_page": response["next"],
            "previous_page": response["previous"],
        }
        return render_template("action/remote.html", **context)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("action/remote.html")


@action_blueprint.route("/actions", methods=["GET"])
def list_actions(device_id):
    context = {"actions": Action.query.filter_by(device_id=UUID(device_id)).all()}
    return render_template("action/index.html", **context)


@action_blueprint.route("/actions/index", methods=["GET"])
def index():
    context = {"actions": Action.query.all()}
    return render_template("action/index.html", **context)


@action_blueprint.route("/action", methods=["GET"])
def new():
    context = {
        "devices": Device.query.all(),
        "selected_device_id": (
            UUID(request.args.get("device_id"))
            if request.args.get("device_id")
            else None
        ),
        "request_methods": [method.value for method in RequestMethod],
        "connection_protocols": [protocol.value for protocol in ConnectionProtocol],
    }
    return render_template("action/new.html", **context)


@action_blueprint.route("/action", methods=["POST"])
def create():
    try:
        action = Action(
            name=request.form.get("name"),
            description=request.form.get("description"),
            path=request.form.get("path"),
            device_id=UUID(request.form.get("device_id")),
            payload=json.dumps(json.loads(request.form.get("payload"))),
            request_method=request.form.get("request_method"),
            connection_protocol=request.form.get("connection_protocol"),
        )
        db.session.add(action)
        db.session.commit()

        if request.form.get("is_public"):
            device = Device.query.get(action.device_id)
            if device and not api.device_exists(device.contribution_id):
                brand = Brand.query.get(device.brand_id)
                if brand and not api.brand_exists(brand.contribution_id):
                    breakpoint()
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

            response = ActionDTO(api.publish_action(action.to_dict()))
            author, was_created = get_or_create(
                db.session, Author, **response.user.parse().to_dict()
            )
            action.contrituion_id = response.id
            action.author_id = author.id
            db.session.commit()
        flash("Action created successfully", "success")
        return redirect(url_for("action.show", action_id=action.id))
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("action.new"))


@action_blueprint.route("/action/<action_id>", methods=["GET"])
def show(action_id):
    action = Action.query.get(UUID(action_id))
    context = {
        "action": action,
        "request_methods": [method.value for method in RequestMethod],
        "connection_protocols": [protocol.value for protocol in ConnectionProtocol],
    }
    return render_template("action/show.html", **context)


@action_blueprint.route("/action/<action_id>", methods=["POST"])
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
        return render_template(
            "action/show.html", action=Action.query.get(UUID(action_id))
        )
