from flask import Blueprint, render_template
from utils import network
main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    device_list = network.list_devices("127.0.0.1/24")
    print(device_list)
    return render_template("index.html")
