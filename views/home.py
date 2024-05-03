from flask import Blueprint, render_template, request, flash, redirect
import utils.network as network

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/setup", methods=['GET', 'POST'])
def setup():
    wifi_device = "wlan0"
    if network.get_current_wifi_network() != "pi_hub":
        flash("Skip setup network process", 'success')
        return redirect("/")
   
    if request.method == 'GET':
        try:
            context = {
                "available_ssids": network.list_availabe_networks(wifi_device) 
            }
            return render_template("setup.html", **context)
        except Exception as e:
            flash(e)
            return render_template("setup.html")

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

        return render_template("setup.html")