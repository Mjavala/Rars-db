import json
import time

import psycopg2


def add_slide(con, cur, data):
    # init data ~ slide ID, Box ID(null), Cabinet (null), Timestamp
    # if box == null & cabinet == null then the slide is being staged for storage or has been retrived by an operator

    # uid = data['SlideId']
    strSlideID = data["slideid"]
    strBlockID = data["blockid"]
    strAccID = data["accessionid"]
    strStain = data["stain"]
    strStainOrderDate = data["stainorderdate"]
    strSiteLabel = data["sitelabel"]
    strCaseType = data["casetype"]
    strYear = data["year"]
    location = data["location"]
    box = data["box_id"]
    timestamp = time.time()

    # query = "INSERT INTO slides (SlideId, location, box_id, ts) VALUES (%s, %s, %s, %s)"
    query = """INSERT INTO public.slides(
	slideid, blockid, accessionid, stain, stainorderdate, sitelabel, casetype, year, location, box_id, ts)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    # print("Query:", query)

    try:
        cur.execute(
            query,
            (
                strSlideID,
                strBlockID,
                strAccID,
                strStain,
                strStainOrderDate,
                strSiteLabel,
                strCaseType,
                strYear,
                location,
                box,
                timestamp,
            ),
        )
        con.commit()
    except (Exception, psycopg2.Error) as error:
        print("Database error adding a slide:", error)


def add_box(con, cur, file):
    # init data ~ Box ID, Cabinet ID (null), Timestamp

    with open(file) as f:
        data = json.load(f)
        uid = data["boxes"][0]["box_id"]
        cabinet = data["boxes"][0]["cabinet_id"]
        timestamp = time.time()

        query = (
            "INSERT INTO boxes (box_id, cabinet_id, ts) VALUES (%s, %s, %s)"
        )
        try:
            cur.execute(query, (uid, cabinet, timestamp))
            con.commit()

        except (Exception, psycopg2.Error) as error:
            print("Database error adding box: {0}".format(error))


def add_initial_data(con, cur, file):
    # add test_data.json to database
    with open(file) as f:
        data = json.load(f)

        # add_box(data['boxes'][0])

        for slide in data["slides"]:
            add_slide(con, cur, slide)


def db_conn():
    try:
        con = psycopg2.connect(
            "dbname=postgres user=postgres host=localhost password=postgres"
        )
        return con
    except psycopg2.Error as error:
        print("Database connection error: {0}".format(error))


def add_tables(con, cur):
    commands = (
        """
        DROP TABLE IF EXISTS SLIDES;
        """,
        """
        DROP TABLE IF EXISTS BOXES;
        """,
        """
        CREATE TABLE BOXES (
        TR_ID SERIAL NOT NULL PRIMARY KEY,    /* Table row ID */
        TS NUMERIC,
        BOX_ID TEXT NOT NULL UNIQUE,          /* Need to find out string length */
        CABINET_ID TEXT UNIQUE
        );
        """,
        """
        CREATE TABLE slides (
        SlideID TEXT NOT NULL PRIMARY KEY,                         /* Need to find out string length */
        BlockID TEXT,
        AccessionID TEXT,
        Stain TEXT,
        StainOrderDate TIMESTAMP,
        SiteLabel TEXT,
        CaseType TEXT,
        Year VARCHAR(4),
        TS NUMERIC,
        LOCATION TEXT,
        RetrievalRequest BOOLEAN,
        RequestedBy  TEXT,
        RequestTS Numeric,                        /* 100 slots per box */
        BOX_ID TEXT,
        CONSTRAINT box_constraint
        FOREIGN KEY (BOX_ID)
        REFERENCES BOXES (BOX_ID)
        );
        """,
    )
    try:
        for command in commands:
            cur.execute(command)

        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in creating tables: {0}".format(error))


def setup():
    con = db_conn()
    cur = con.cursor()

    # add tables to database
    add_tables(con, cur)

    # add box
    add_box(con, cur, "test_data_single.json")

    # add test data for testing & simulation
    add_initial_data(con, cur, "test_data.json")

    cur.close()
    con.close()


if __name__ == "__main__":
    setup()
