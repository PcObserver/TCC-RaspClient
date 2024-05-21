from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests
from flask import session
from flask_htmx import make_response
from application import api

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

            api.login(**data)

            response = make_response( 
                render_template("/components/topbar.html"),
                push_url=False,
                retarget="#topbar",
                reswap="outerHTML",
                trigger={"close-modal": "true", 
                         "store-token": {
                                        "access_token": session['access_token'],
                                        "refresh_token": session['refresh_token']
                                    }
                         }
                )
                
            flash("Login successful", 'success')
            return response
        except Exception as e:
            flash(str(e), 'error')
            return render_template("/auth/login_form.html")
        
        
@auth_blueprint.route("/logout", methods=['GET'])
def logout():
    try:
        api.logout()
        response = make_response(
            render_template("/components/topbar.html"),
            push_url=False, 
            trigger={"remove-token": "true"}
        )

        flash("Logout successful", 'success')
        return response
    except Exception as e:
        flash(str(e), 'error')
        return render_template("/components/topbar.html")
    

@auth_blueprint.route("/register", methods=['GET', 'POST'])
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

            api.register(**data)
          
            flash("User created successfully", 'success')
            response = make_response( 
                render_template("/components/topbar.html"),
                push_url=False,
                retarget="#topbar",
                reswap="outerHTML",
                trigger={"close-modal": "true", 
                         "store-token": {
                                        "access_token": session['access_token'],
                                        "refresh_token": session['refresh_token']
                                    }
                         }
                )
            return response
        except Exception as e:
            flash(str(e), 'error')
            return render_template("/auth/register_form.html")