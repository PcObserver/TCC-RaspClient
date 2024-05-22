from flask import Flask, session, flash
import requests
from uuid import UUID


class ApiAdapter:
    def __init__(
        self, app: Flask = None, hostname: str = "localhost", port: int = 8000
    ):
        self.app = app
        self.url = f"http://{hostname}:{port}/api"
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialise the extension with the Flask app object."""
        app.htmx = self

    def login(self, email: str, password: str):
        response = requests.post(
            self.url + "/users/log_in/",
            data={"email": email, "password": password},
        )
        response.raise_for_status()
        session["access_token"] = response.json()["access"]
        session["refresh_token"] = response.json()["refresh"]
        session["user_name"] = response.json()["user"]["name"]
        session["user_id"] = UUID(response.json()["user"]["id"])

    def logout(self):
        response = requests.post(
            self.url + "/users/log_out/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data={"refresh": session["refresh_token"]},
        )
        response.raise_for_status()
        session.pop("access_token")
        session.pop("refresh_token")
        session.pop("user_name")
        session.pop("user_id")

    def register(
        self, name: str, email: str, password: str, password_confirmation: str
    ):
        response = requests.post(
            self.url + "/users/sign_up/",
            data={
                "name": name,
                "email": email,
                "password": password,
                "password_confirmation": password_confirmation,
            },
        )
        response.raise_for_status()
        self.login(email, password)

    def publish_brand(self, data: dict):

        data.update({"contribution_type": "Brand", "display_name": data["name"]})
        data.pop("name")
        response = requests.post(
            self.url + "/contributions/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data,
        )

        if response.status_code != 201:
            flash(response.json(), "error")
        else:
            flash("Brand published successfully", "success")

        response.raise_for_status()
        return response.json()

    def publish_device(self, data: dict):
        data.update(
            {
                "contribution_type": "Device",
                "display_name": data["name"],
                "parent_brand": data["brand_id"],
            }
        )
        data.pop("name")
        data.pop("brand_id")

        response = requests.post(
            self.url + "/contributions/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data,
        )

        if response.status_code != 201:
            flash(response.json(), "error")
        else:
            flash("Device published successfully", "success")

        response.raise_for_status()
        return response.json()

    def publish_action(self, data: dict):
        data.update({"contribution_type": "Action", "parent_device": data["device_id"]})
        data.pop("device_id")

        response = requests.post(
            self.url + "/contributions/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data,
        )
        if response.status_code != 201:
            flash(response.json(), "error")
        else:
            flash("Action published successfully", "success")

        response.raise_for_status()
        return response.json()

    def list_brands(self, page: int, q: dict = {}):
        params = ["&{}={}".format(k, v) for k, v in q.items()]
        params = "".join(params)
        response = requests.get(
            self.url + "/devices/brands/?page={}".format(page) + params,
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def list_devices(self, page: int = 1, q: dict = {}):
        params = ["&{}={}".format(k, v) for k, v in q.items()]
        params = "".join(params)
        response = requests.get(
            self.url + "/devices/devices/?page={}".format(page) + params,
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def list_actions(self, page: int = 1, q: dict = {}):
        params = ["&{}={}".format(k, v) for k, v in q.items()]
        params = "".join(params)
        response = requests.get(
            self.url + "/devices/actions/?page={}".format(page),
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def get_brand(self, brand_id: str):
        response = requests.get(
            self.url + f"/devices/brands/{brand_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def get_device(self, device_id: str):
        response = requests.get(
            self.url + f"/devices/devices/{device_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def get_action(self, action_id: str):
        response = requests.get(
            self.url + f"/devices/actions/{action_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def update_brand(self, data: dict):
        data.update({"contribution_type": "Brand", "display_name": data["name"]})
        data.pop("name")
        response = requests.patch(
            self.url + f"/devices/brands/{data['id']}/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def update_device(self, data: dict):
        data.update(
            {
                "contribution_type": "Device",
                "display_name": data["name"],
                "parent_brand": data["brand_id"],
            }
        )
        data.pop("name")
        data.pop("brand_id")

        response = requests.patch(
            self.url + f"/devices/devices/{data['id']}/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def update_action(self, data: dict):
        data.update({"contribution_type": "Action", "parent_device": data["device_id"]})
        data.pop("device_id")
        response = requests.patch(
            self.url + f"/devices/actions/{data['id']}/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def brand_exists(self, brand_id: str):
        response = requests.get(
            self.url + f"/devices/brands/{brand_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        return response.status_code == 200

    def device_exists(self, device_id: str):
        response = requests.get(
            self.url + f"/devices/devices/{device_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        return response.status_code == 200

    def action_exists(self, action_id: str):
        response = requests.get(
            self.url + f"/devices/actions/{action_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        return response.status_code == 200

    def create_or_update_brand(self, data: dict):
        if self.brand_exists(data["id"]):
            return self.update_brand(data)
        return self.publish_brand(data)

    def create_or_update_device(self, data: dict):
        if self.device_exists(data["id"]):
            return self.update_device(data)
        return self.publish_device(data)

    def create_or_update_action(self, data: dict):
        if self.action_exists(data["id"]):
            return self.update_action(data)
        return self.publish_action(data)

    def delete_brand(self, brand_id: str):
        response = requests.delete(
            self.url + f"/devices/brands/{brand_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()

    def delete_device(self, device_id: str):
        response = requests.delete(
            self.url + f"/devices/devices/{device_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        return response

    def delete_action(self, action_id: str):
        response = requests.delete(
            self.url + f"/devices/actions/{action_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        return response
