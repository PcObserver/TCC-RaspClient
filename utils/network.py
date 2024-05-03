import subprocess

def get_current_wifi_network():
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi", "| egrep '^yes' | cut -d\' -f2"])
        return result.decode().strip().removeprefix("yes:")
    except Exception:
        return None


def list_availabe_networks(wifi_device):
    try:
        result = subprocess.check_output(["nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", wifi_device])
        ssids_list = result.decode().split('\n')
        available_ssids = [ssid.removeprefix("SSID:") for ssid in ssids_list if len(ssid.removeprefix("SSID:")) > 0] 
        return available_ssids
    except Exception:
        return []


def connect_to_network(wifi_device, ssid, password):
    connection_command = ["nmcli", "--colors", "no", "device", "wifi", "connect", ssid, "ifname", wifi_device]
    
    if len(password) > 0:
        connection_command.append("password")
        connection_command.append(password)

    return subprocess.run(connection_command, capture_output=True)