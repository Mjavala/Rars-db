from flask import Flask, request
import db_methods as db
import json


def create_app():
    app = Flask(__name__)
    con = db.node()

    @app.route("/create_film", methods=["POST"])
    def film():
        if request.method == "POST":
            data = request.get_json()
            print(data)
            result = con.create_films(data)

            return result


    # flask post multiple keys
    @app.route("/update_film", methods=["POST"])
    def update_film():
        if request.method == "POST":
            data = request.get_json()
            print(data)
            slot = data["slot"]
            print(slot)

            slot = con.update_film(data)
            result = con.update_film_slot(slot)

            return result


    @app.route("/create_box", methods=["POST"])
    def create_box():
        if request.method == "POST":
            data = request.form
            result = con.create_box(data["box_name"])
            con.create_slots(data)
            return result


    @app.route("/get_slots", methods=["POST"])
    def get_slots():
        if request.method == "POST":
            data = request.form
            print(data["box"])
            result = con.read_film_slot(data)
            return result


    @app.route("/film_data", methods=["POST"])
    def film_data():
        if request.method == "POST":

            data = request.get_json()
            print(data)
            film = data["id"]

            # returns film location relative to fixed box location
            data = con.get_film(film)

            return data

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8888)
