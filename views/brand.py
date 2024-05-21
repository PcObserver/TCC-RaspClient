from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models.brand import Brand
from application import db, api
from uuid import UUID
from data.brand_dto import BrandDTO
from data.device_dto import DeviceDTO
from data.action_dto import ActionDTO
from models.author import Author
from utils.db import get_or_create

brand_blueprint = Blueprint("brand", __name__)


@brand_blueprint.route("/brands/remote/", methods=["GET"])
def list_remote():
    try:
        response = api.list_brands(page=request.args.get("page", 1))
        imported_brands = [
            str(brand.contribution_id)
            for brand in Brand.query.filter(Brand.contribution_id.isnot(None))
        ]
        context = {
            "brands": [
                BrandDTO(**result)
                for result in response["results"]
                if result["id"] not in imported_brands
            ],
            "next_page": response["next"],
            "previous_page": response["previous"],
        }
        return render_template("brand/remote.html", **context)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("brand/remote.html")


@brand_blueprint.route("/brands/import/<brand_id>", methods=["GET"])
def import_remote(brand_id):
    try:
        response = BrandDTO(**api.get_brand(brand_id))
        brand = response.parse()
        get_or_create(db.session, Author, **response.user.parse().to_dict())
        db.session.add(brand)

        response = api.list_devices(q={"parent_brand": brand_id})
        devices = [DeviceDTO(**result).parse() for result in response["results"]]
        db.session.add_all(devices)

        response = api.list_actions(q={"parent_device_brand": brand_id})
        actions = [ActionDTO(**result).parse() for result in response["results"]]
        db.session.add_all(actions)

        db.session.commit()
        flash("Marca importada com sucesso", "success")
        return redirect(url_for("brand.list_remote"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("brand.list_remote"))


@brand_blueprint.route("/brands")
def list_brands():
    context = {"brands": [brand.to_select2_dict() for brand in Brand.query.all()]}
    return jsonify(context)


@brand_blueprint.route("/brands/index")
def index():
    context = {"brands": Brand.query.all()}
    return render_template("brand/index.html", **context)


@brand_blueprint.route("/brand", methods=["GET"])
def new():
    return render_template("brand/new.html")


@brand_blueprint.route("/brand", methods=["POST"])
def create():
    try:
        brand_data = {
            "name": request.form.get("name"),
            "prefix": request.form.get("prefix"),
            "description": request.form.get("description"),
        }
        brand = Brand(**brand_data)
        db.session.add(brand)
        db.session.commit()

        if request.form.get("is_public"):
            response = BrandDTO(**api.publish_brand(brand_data))
            brand.contribution_id = response.id
            author, was_created = get_or_create(
                db.session, Author, **response.user.parse().to_dict()
            )
            brand.author_id = author.id
            db.session.add(brand)
            db.session.commit()

        flash("Marca criada com sucesso", "success")
        return render_template("brand/show.html", brand=brand)
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("brand.new"))


@brand_blueprint.route("/brand/<brand_id>", methods=["GET"])
def show(brand_id):
    brand = Brand.query.get(UUID(brand_id))
    context = {"brand": brand}
    return render_template("brand/show.html", **context)


@brand_blueprint.route("/brand/<brand_id>", methods=["POST"])
def update(brand_id):
    try:
        brand = Brand.query.get(UUID(brand_id))
        brand.name = request.form.get("name")
        brand.prefix = request.form.get("prefix")
        brand.description = request.form.get("description")
        db.session.add(brand)
        db.session.commit()

        if request.form.get("is_public"):
            response = BrandDTO(**api.create_or_update_brand(brand.to_dict()))
            brand.contribution_id = response.id
            author, was_created = get_or_create(
                db.session, Author, **response.user.parse().to_dict()
            )
            brand.author_id = author.id
            db.session.add(brand)
            db.session.commit()

        flash("Marca atualizada com sucesso", "success")
        return render_template("brand/show.html", brand=brand)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("brand/show.html", brand=Brand.query.get(UUID(brand_id)))


@brand_blueprint.route("/brand/<brand_id>", methods=["DELETE"])
def delete(brand_id):
    try:
        brand = Brand.query.get(UUID(brand_id))
        if request.form.get("is_public") == "true" and api.brand_exists(
            brand.contribution_id
        ):
            api.delete_brand(brand.contribution_id)
        db.session.delete(brand)
        db.session.commit()
        flash("Marca deletada com sucesso", "success")
        return redirect(url_for("brand.index"), code=303)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("brand.show", brand_id=brand_id), code=303)
