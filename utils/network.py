import subprocess


def get_current_wifi_network():
    try:
        result = subprocess.check_output(
            ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"]
        )
        ssids_list = result.decode().split("\n")
        filtered_list = list(filter(lambda x: x.startswith("yes:"), ssids_list))
        return filtered_list[0].removeprefix("yes:")
    except Exception:
        return None


def list_availabe_networks(wifi_device):
    try:
        result = subprocess.check_output(
            [
                "nmcli",
                "--colors",
                "no",
                "-m",
                "multiline",
                "--get-value",
                "SSID",
                "dev",
                "wifi",
                "list",
                "ifname",
                wifi_device,
            ]
        )
        ssids_list = result.decode().split("\n")
        available_ssids = [
            ssid.removeprefix("SSID:")
            for ssid in ssids_list
            if len(ssid.removeprefix("SSID:")) > 0
        ]
        return available_ssids
    except Exception:
        return []


def connect_to_network(wifi_device, ssid, password):
    connection_command = [
        "nmcli",
        "--colors",
        "no",
        "device",
        "wifi",
        "connect",
        ssid,
        "ifname",
        wifi_device,
    ]

    if len(password) > 0:
        connection_command.append("password")
        connection_command.append(password)

    return subprocess.run(connection_command, capture_output=True)


def strip_value(string):
    return string.split("=")[1].strip()[1:-1]


def list_available_devices(device_type=None):
    try:
        command = ["avahi-browse", "-art"]
        if device_type:
            command.append(device_type)

        result = subprocess.check_output(command)
        result = result.decode().split("\n= ")
        # pop first element because it is not a device
        result.pop(0)
        # list of devices
        devices = dict()
        for i in range(len(result)):
            data = list(map(str.strip, result[i].split("\n")))
            data.pop(0)
            devices[data[0].split("=")[1].strip()[1:-7]] = {
                "hostname": strip_value(data[0]),
                "ip": strip_value(data[1]),
                "port": strip_value(data[2]),
                "txt": strip_value(data[3]),
            }

        return devices
    except Exception:
        return []
