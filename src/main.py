from flask import Flask, request

import db_methods as db


def create_app():
    app = Flask(__name__)
    con = db.node()

    @app.route("/create_slide", methods=["POST"])
    def create_slide():
        if request.method == "POST":
            data = request.get_json()
            result = con.create_films(data)

            return result

    # flask post multiple keys
    @app.route("/update_slide", methods=["POST"])
    def update_slide():
        if request.method == "POST":
            data = request.get_json()
            slot = data["slot"]

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
            result = con.read_film_slot(data)
            return result

    @app.route("/get_slide", methods=["POST"])
    def get_slide():
        if request.method == "POST":

            data = request.get_json()
            slide = data["payload"]
            # returns entire slide row data
            data = con.get_slide(slide)

            return data

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8888)
