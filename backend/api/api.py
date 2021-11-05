from datetime import datetime
import json
from flask import Flask, request, render_template
from flask.helpers import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from db.access_database import AccessDataBase
import db.queries as db


def init_app(app: Flask):

    """--- GET methods ---"""
    ### swagger specific ###
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Cowork-Reservation"}
    )

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    @app.route("/static/<path:path>")
    def send_static(path):
        return send_from_directory("static", path)

    @app.route("/organizations", methods=["GET"])
    def get_companies():
        companies = db.getCompanies()
        return json.dumps(companies)

    @app.route("/", methods=["GET"])
    def get_webPage():
        # TODO: Replace with correct html file
        return render_template("base.html")

    @app.route("/admin", methods=["GET"])
    def get_adminPage():
        # TODO: Replace with correct html file
        return render_template("base.html")

    """ --- POST methods --- """

    @app.route("/organizations", methods=["POST"])
    def insert_company():
        try:
            if request.method == "POST":
                print(request)
                message_json = {}
                message_json["name"] = request.form.get("name")
                message_json["location"] = request.form.get("location")
                message_json["email"] = request.form.get("email")
                print(
                    db.addCompany(
                        message_json["name"],
                        message_json["location"],
                        message_json["email"],
                    )
                )
                return render_template("base.html")
        except Exception as err:
            return str(err)
