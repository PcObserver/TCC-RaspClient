from flask import Blueprint, render_template, request, flash, redirect,url_for, Response
from models.user_device import UserDevice
import utils.network as network
import requests
from flask import session
from flask_htmx import make_response
application_blueprint = Blueprint("application", __name__)


@application_blueprint.route("/")
def index():
    return render_template("index.html")


@application_blueprint.route("/home")
def home():
    context = {"user_devices": UserDevice.query.all()}
    return render_template("home.html", **context)


@application_blueprint.route("/setup", methods=['GET'])
def list_networks():
    wifi_device = "wlan0"
    if network.get_current_wifi_network() != "iot_hub":
        flash("Skiped setup network process", 'success')
        return redirect(url_for("application.home"))
    try:
        context = {
            "available_ssids": network.list_availabe_networks(wifi_device) 
        }
        return render_template("/setup/index.html", **context)
    except Exception as e:
        flash(e)
        return render_template("/setup/index.html")


@application_blueprint.route("/setup", methods=['POST'])
def connect_to_network():
    wifi_device = "wlan0"
    ssid = request.form['ssid']
    password = request.form['password']
    result = network.connect_to_network(wifi_device, ssid, password)

    if result.stderr:
        flash("Error: failed to connect to wifi network: %s" % result.stderr.decode(), 'error')
    elif result.stdout:
        flash("Success: %s" % result.stdout.decode(), 'success')
    else:
        flash("Error: failed to connect to wifi network", 'error')

    return render_template("/setup/index.html")

@application_blueprint.route("/settings", methods=['GET'])
def settings():
    return render_template("/settings/index.html")


@application_blueprint.after_request
def render_messages(response: Response) -> Response:
    if request.headers.get("HX-Request") and response.data.find(b"div id=\"alerts\"") == -1:
        messages = render_template("components/alerts.jinja2")
        response.data = response.data + messages.encode("utf-8")
    return response


@application_blueprint.route("/auth-modal", methods=['GET'])
def auth_modal():
    return render_template("/components/modal.html")


@application_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/auth/login_form.html")
    elif request.method == 'POST':
        try:
            data = {
                "email":  request.form['email'],
                "password": request.form['password']
            }
            response = requests.post('http://localhost:8000/api/users/log_in/', data=data)
            if response.json().get('detail'):
                flash(response.json()['detail'], 'error')
            else:
                session['access_token'] = response.json()['access']
                session['refresh_token'] = response.json()['refresh']
                flash("Login successful", 'success')
            return make_response(render_template("/auth/login_form.html"), push_url=False, trigger={"close-modal": "true"})
        except Exception as e:
            flash(str(e), 'error')
            return render_template("/auth/login_form.html")
        
    

@application_blueprint.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("/auth/register_form.html")
    elif request.method == 'POST':
        try:
            data = {
                "name": request.form['name'],
                "email": request.form['email'],
                "password": request.form['password'],
                "password_confirmation": request.form['password_confirmation']
            }
            response = requests.post('http://localhost:8000/api/users/sign_up/', data=data)
            if response.status_code != 201:
                raise Exception(response.json())
            else:
                flash("User created successfully", 'success')
            return make_response(render_template("/auth/register_form.html"), push_url=False, trigger={"close-modal": "true"})
        except Exception as e:
            flash(str(e), 'error')
            return render_template("/auth/register_form.html")