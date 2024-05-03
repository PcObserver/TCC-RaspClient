from flask import Blueprint, render_template
from models.brand import Brand

brand_blueprint = Blueprint("brand", __name__)

@brand_blueprint.route("/device/brands")
def list_brands():
    brands =  Brand.query.all()
    return render_template("brand/index.html", brands=brands)