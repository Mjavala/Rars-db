import json
import time
import psycopg2

def add_slide(data):
    # init data ~ slide ID, Box ID(null), Cabinet (null), Timestamp
    # if box == null & cabinet == null then the slide is being staged for storage or has been retrived by an operator
    db = db_conn()
    cursor = db.cursor()

    # uid = data['slide_id']
    strSlideID = data['slideid']
    strBlockID = data['blockid']
    strAccID = data['accessionid']
    strStain = data['stain']
    strStainOrderDate = data['stainorderdate']
    strSiteLabel = data['sitelabel']
    strCaseType = data['casetype']
    strYear = data['year']
    location = data['location']
    box = data['box_id']
    timestamp = time.time()

    # query = "INSERT INTO slides (slide_id, location, box_id, ts) VALUES (%s, %s, %s, %s)"
    query = """INSERT INTO public.slides(
	slideid, blockid, accessionid, stain, stainorderdate, sitelabel, casetype, year, location, box_id, ts)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    # print("Query:", query)

    try:
        cursor.execute(query, (strSlideID, strBlockID, strAccID, strStain, strStainOrderDate, strSiteLabel, strCaseType, strYear, location, box, timestamp))
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
        print("Database error:", error, query)
    except Exception as e:
        print("General Error:", e)

def add_initial_data(file):
    # add test_data.json to database
    with open(file) as f:
        data = json.load(f)

        add_box(data['boxes'][0])
        add_box(data['boxes'][1])

        
        #add_slide(data['slides'][0])
        #add_slide(data['slides'][1])

        for i in range(500):
          add_slide(data['slides'][i-1])

def db_conn():
    try:
        conn = psycopg2.connect("dbname=postgres user=postgres host=localhost password=postgres")
        return conn
    except psycopg2.Error as error:
        print("Database error:", error) 

if __name__ == '__main__':
    add_initial_data('test_data.json')