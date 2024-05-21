from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models.brand import Brand
from application import db, api
from uuid import UUID
from flask_htmx import make_response
from data.brand_dto import BrandDTO
from data.device_dto import DeviceDTO
from data.action_dto import ActionDTO

brand_blueprint = Blueprint("brand", __name__)


@brand_blueprint.route("/brands/remote/", methods=["GET"])
def list_remote():
    try:
        response = api.list_brands(page=request.args.get("page", 1))
        context = {
            "brands": [BrandDTO(**result) for result in response["results"]],
            "next_page": response["next"],
            "previous_page": response["previous"]
        }
        return render_template("brand/remote.html", **context)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("brand/remote.html")

@brand_blueprint.route("/brands/import/<brand_id>", methods=["GET"])
def import_remote(brand_id):
    try:
        response = api.get_brand(brand_id)
        brand = BrandDTO(**response).parse()
        db.session.add(brand)

        response = api.list_devices(q={"parent_brand": brand_id})
        devices = [DeviceDTO(**result).parse() for result in response["results"]]
        db.session.add_all(devices)
        
        response = api.list_actions(q={"parent_device_brand": brand_id})
        db.session.commit()
        actions = [ActionDTO(**result).parse() for result in response["results"]]
        db.session.add(actions[0])

        db.session.commit()
        flash("Marca importada com sucesso", "success")
        return redirect(url_for("brand.list_remote"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("brand.list_remote"))

@brand_blueprint.route("/brands")
def list_brands():
    context = {
        "brands": [brand.to_select2_dict() for brand in Brand.query.all()]
    }
    return jsonify(context)


@brand_blueprint.route("/brands/index")
def index():
    context = {
        "brands": Brand.query.all()
    }
    return render_template("brand/index.html", **context)


@brand_blueprint.route("/brand", methods=["GET"])
def new():
    return render_template("brand/new.html")


@brand_blueprint.route("/brand", methods=["POST"]) 
def create():
    try:
        brand_data = { 
            "name": request.form.get("name"),
            "prefix": request.form.get("prefix")
        }
        brand = Brand(**brand_data)

        if request.form.get("is_public"):
            response = api.publish_brand(brand_data)
            brand.id = UUID(response["id"])
            
        db.session.add(brand)
        db.session.commit()
        breakpoint()

        flash("Marca criada com sucesso", "success")
        return render_template("brand/show.html", brand=brand)
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("brand.new"))
    

@brand_blueprint.route("/brand/<brand_id>", methods=["GET"])
def show(brand_id):
    brand = Brand.query.get(UUID(brand_id))
    context = {
        "brand": brand
    }
    return render_template("brand/show.html", **context)


@brand_blueprint.route("/brand/<brand_id>", methods=["POST"])
def update(brand_id):
    try:
        brand = Brand.query.get(UUID(brand_id))
        brand.name = request.form.get("name")
        brand.prefix = request.form.get("prefix")
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
        db.session.delete(brand)
        db.session.commit()
        flash("Marca deletada com sucesso", "success")
        return render_template("brand/index.html", brands=Brand.query.all())
    except Exception as e:
        flash(str(e), "danger")
        return render_template("brand/show.html", brand=Brand.query.get(UUID(brand_id)))
