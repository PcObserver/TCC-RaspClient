from flask import Blueprint, render_template, request, flash
import requests
from flask import session
from flask_htmx import make_response

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/auth-modal", methods=['GET'])
def auth_modal():
    return render_template("/components/modal.html")


@auth_blueprint.route("/login", methods=['GET', 'POST'])
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
        
    

@auth_blueprint.route("/register", methods=['GET','POST'])
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