from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models.brand import Brand
from application import db
from uuid import UUID

brand_blueprint = Blueprint("brand", __name__)


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
        name = request.form.get("name")
        prefix = request.form.get("prefix")
        brand = Brand(name=name, prefix=prefix)
        db.session.add(brand)
        db.session.commit()

        return redirect(url_for("brand.show", brand_id=brand.id))
    except Exception as e:
        flash(e)
        return render_template("brand/new.html")
    

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
        return redirect(url_for("brand.show", brand_id=brand.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("brand.show", brand_id=brand.id))


@brand_blueprint.route("/brand/<brand_id>", methods=["DELETE"])
def delete(brand_id):
    try:
        brand = Brand.query.get(UUID(brand_id))
        db.session.delete(brand)
        db.session.commit()
        flash("Marca deletada com sucesso", "success")
        return redirect(url_for("brand.index"), code=303)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("brand/show.html", brand=Brand.query.get(UUID(brand_id)))