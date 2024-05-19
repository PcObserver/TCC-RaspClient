from flask import Flask, session
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

    def make_contribuition(self, data: dict, type: str):
        data.update({"contribution_type": type, "display_name": data["name"]})
        data.pop("name")
        response = requests.post(
            self.url + "/contributions/",
            headers={"Authorization": "Bearer {}".format(session["access_token"])},
            data=data)
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

