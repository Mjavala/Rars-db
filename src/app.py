"""
DB CRUD API
    - Ingests REST commands from state manager
"""

from flask import Flask, request
import db_methods as db
import json

app = Flask(__name__)
db = db.node()


@app.route("/create_film", methods=["POST"])
def film():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        result = db.create_films(data)

        return result


# flask post multiple keys
@app.route("/update_film", methods=["POST"])
def update_film():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        slot = data["slot"]
        print(slot)

        slot = db.update_film(data)
        result = db.update_film_slot(slot)

        return result


@app.route("/create_box", methods=["POST"])
def create_box():
    if request.method == "POST":
        data = request.form
        result = db.create_box(data["box_name"])
        db.create_slots(data)
        return result


@app.route("/get_slots", methods=["POST"])
def get_slots():
    if request.method == "POST":
        data = request.form
        print(data["box"])
        result = db.read_film_slot(data)
        return result


@app.route("/film_data", methods=["POST"])
def film_data():
    if request.method == "POST":

        data = request.get_json()
        print(data)
        film = data["id"]

        # returns film location relative to fixed box location
        data = db.get_film(film)

        return data


@app.route("/")
def hello():

    return json.dumps("hello world")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
