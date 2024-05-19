from flask import Blueprint, render_template, Response, request
signals_blueprint = Blueprint("signals", __name__)


@signals_blueprint.after_app_request
def render_messages(response: Response) -> Response:
    if request.headers.get("HX-Request") and response.data.find(b"div id=\"alerts\"") == -1:
        messages = render_template("components/alerts.jinja2")
        response.data = response.data + messages.encode("utf-8")
    return response
