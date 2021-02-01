import json
import time
import psycopg2

def add_film(data):
    # init data ~ Film ID, Box ID(null), Cabinet (null), Timestamp
    # if box == null & cabinet == null then the film is being staged for storage or has been retrived by an operator
    db = db_conn()
    cursor = db.cursor()

    uid = data['film_id']
    location = data['location']
    box = data['box_id']
    timestamp = time.time()

    query = "INSERT INTO films (film_id, location, box_id, ts) VALUES (%s, %s, %s, %s)"

    try:
        cursor.execute(query, (uid, location, box, timestamp))
        db.commit()
    except psycopg2.Error as error:
        print("Database error:", error)
    except Exception as e:
        print("General Error:", e)

def add_box(data):
    # init data ~ Box ID, Cabinet ID (null), Timestamp
    db = db_conn()
    cursor = db.cursor()

    uid = data['box_id']
    cabinet = data['cabinet_id']
    timestamp = time.time()

    query = "INSERT INTO boxes (box_id, cabinet_id, ts) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (uid, cabinet, timestamp))
        db.commit()

    except psycopg2.Error as error:
        print("Database error:", error)
    except Exception as e:
        print("General Error:", e)

def add_initial_data(file):
    # add test_data.json to database
    with open(file) as f:
        data = json.load(f)

        add_box(data['boxes'][0])
        add_box(data['boxes'][1])

        add_film(data['films'][0])
        add_film(data['films'][1])

def db_conn():
    try:
        conn = psycopg2.connect("dbname=postgres user=postgres host=localhost password=postgres")
        return conn
    except psycopg2.Error as error:
        print("Database error:", error) 

if __name__ == '__main__':
    add_initial_data('test_data.json')