from flask import Blueprint, render_template, request, flash, redirect,url_for
import utils.network as network

setup_blueprint = Blueprint("setup", __name__)


@setup_blueprint.route("/")
def index():
    return render_template("index.html")


@setup_blueprint.route("/setup", methods=['GET', 'POST'])
def setup():
    wifi_device = "wlan0"
    if network.get_current_wifi_network() != "iot_hub":
        flash("Skiped setup network process", 'success')
        return redirect(url_for("user_device.list_registered_devices"))
    
    if request.method == 'GET':
        try:
            context = {
                "available_ssids": network.list_availabe_networks(wifi_device) 
            }
            return render_template("/setup/index.html", **context)
        except Exception as e:
            flash(e)
            return render_template("/setup/index.html")

    elif request.method == 'POST':
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