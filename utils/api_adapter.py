from flask import Flask, session, flash
import requests


class ApiAdapter:
    def __init__(self, app: Flask = None, hostname: str = "localhost", port: int = 8000):
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
    
    def logout(self):
        response = requests.post(
            self.url + "/users/log_out/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data={"refresh": session["refresh_token"]}
        )
        response.raise_for_status()
        session.pop("access_token")
        session.pop("refresh_token")
    
    def register(self, name: str, email: str, password: str, password_confirmation: str):
        response = requests.post(
            self.url + "/users/sign_up/",
            data={"name": name, "email": email, "password": password, "password_confirmation": password_confirmation}
        )
        response.raise_for_status()
        self.login(email, password)

    def publish_brand(self, data: dict):
        data.update({"contribution_type": "Brand", "display_name": data["name"]})
        data.pop("name")
        response = requests.post(
            self.url + "/contributions/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data)
                
        if response.status_code != 201:
            flash(response.json(), "error")

        response.raise_for_status()
        return response.json()
    
    def publish_device(self, data: dict):
        data.update({"contribution_type": "Device", 
                     "display_name": data["name"],
                    "parent_brand": data["brand_id"]})
        data.pop("name")
        data.pop("brand_id")

        response = requests.post(
            self.url + "/contributions/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data)
                
        if response.status_code != 201:
            flash(response.json(), "error")
            
        response.raise_for_status()
        return response.json()
    
    def list_brands(self):
        response = requests.get(
            self.url + "/devices/brands/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()
    
    def list_devices(self):
        response = requests.get(
            self.url + "/devices/devices/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        response.raise_for_status()
        return response.json()
    
    def list_actions(self):
        response = requests.get(
            self.url + "/devices/actions/",
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
    
    def brand_exists(self, brand_id: str):
        response = requests.get(
            self.url + f"/devices/brands/{brand_id}",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
        )
        return response.status_code == 200