from flask import Blueprint, render_template, request, redirect, url_for
from models.brand import Brand
from sqlalchemy.orm import Session 

brand_blueprint = Blueprint("brand", __name__)

@brand_blueprint.route("/device/brands")
def list_brands():
    brands =  Brand.query.all()
    return render_template("brand/index.html", brands=brands)

@brand_blueprint.route("/device/brand", methods=["GET", "POST"])
def create_brand():
    if request.method == "GET":
        return render_template("brand/new.html")
    
    elif request.method == "POST":
        with Session() as session:
            name = request.form.get("name")
            prefix = request.form.get("prefix")
            brand = Brand(name= name, prefix= prefix)
            session.add(brand)
            session.commit()
        return redirect(url_for("brand.list_brands", selected_brand=brand.id))