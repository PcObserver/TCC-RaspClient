from flask import Blueprint, render_template, request, flash
import subprocess


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/setup", methods=['GET', 'POST'])
def setup():
    wifi_device = "wlan0"
    if request.method == 'GET':
        try:
            result = subprocess.check_output(["nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", wifi_device])
            ssids_list = result.decode().split('\n')
            available_ssids = [ssid.removeprefix("SSID:") for ssid in ssids_list if len(ssid.removeprefix("SSID:")) > 0] 
            context = {
                "available_ssids": available_ssids 
            }
            return render_template("setup.html", **context)
        except Exception as e:
            flash(e)
            return render_template("setup.html")

    
    elif request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        connection_command = ["nmcli", "--colors", "no", "device", "wifi", "connect", ssid, "ifname", wifi_device]
        
        if len(password) > 0:
            connection_command.append("password")
            connection_command.append(password)

        result = subprocess.run(connection_command, capture_output=True)

        if result.stderr:
            flash("Error: failed to connect to wifi network: %s" % result.stderr.decode(), 'error')
        elif result.stdout:
            flash("Success: %s" % result.stdout.decode(), 'success')
        else:
            flash("Error: failed to connect to wifi network", 'error')

        return render_template("setup.html")