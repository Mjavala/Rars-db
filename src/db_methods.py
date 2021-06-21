import json
from contextlib import contextmanager
from traceback import print_exc

import psycopg2
from psycopg2 import extras, pool  # noqa: F401


# TODO: Config file
class node:
    def __init__(self):
        self.conn = psycopg2.pool.SimpleConnectionPool(
            1,
            10,
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",  # postgres ~ docker config | 127.0.0.1 ~ local config
            port="5432",
        )

    @contextmanager
    def db(self):
        con = self.conn.getconn()
        cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield con, cur
        finally:
            cur.close()
            self.conn.putconn(con)

    def update_slide(self, data):
        print("update slide data: {}".format(data))
        sql = "UPDATE slides set location = %s where slideid = %s"
        slot = data["slot"]
        # box = data["box"]
        """ needs to be updated """
        slide = data["slide"]
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (slot, slide))
                # id = cursor.fetchone()[0]

                rowcount = cursor.rowcount
                if rowcount == 1:
                    connection.commit()
                else:
                    connection.rollback()

                return slot
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", e)

    def create_box(self, box):
        box_name = box
        sql = "INSERT INTO boxes (box_id) VALUES (%s) RETURNING box_id"
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (box_name,))
                id = cursor.fetchone()[0]

                rowcount = cursor.rowcount
                if rowcount == 1:
                    connection.commit()
                else:
                    connection.rollback()

                new_box = {"id": id, "target": box}
                print(new_box)
                return json.dumps(new_box["target"])
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", e)

    def get_slide(self, slide):
        print("get slide request...{}".format(slide))
        sql = "SELECT * from slides WHERE slideid = %s"
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (slide,))

                connection.commit()

                data = cursor.fetchone()
                return json.dumps(dict(data), default=str)
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", print_exc(e))

    def create_slots(self, target_box):
        slots = []
        # 100 slots per box
        for j in range(1, 101):
            slot_name = "{}_{}".format(target_box["box_name"], j)

            slots.append((slot_name, target_box["box_name"]))

        self.create_slide_slot(slots)

    def create_slide_slot(self, data):
        # target = "bfs_1_2"
        # target_box = "conv_1"
        with self.db() as (connection, cursor):
            try:
                extras.execute_values(
                    cursor,
                    "INSERT INTO slots (slot, box) VALUES %s RETURNING id",
                    data,
                )
                connection.commit()

                # new_slot = {"id": id, "target": target, "target_box": target_box}
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", e)

    def update_slide_slot(self, slot):
        print("full slot: {}".format(slot))
        full_slot = slot
        # Switches the slot filled status to opposite bool
        sql = "UPDATE slots SET filled = NOT filled WHERE slot = %s"
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (full_slot,))

                connection.commit()
                return slot
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", e)

    def read_slide_slot(self, box):
        req = box["box"]
        sql = "SELECT * from slots WHERE filled = false AND box = %s LIMIT 1"
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (req,))
                res = cursor.fetchall()

                rowcount = cursor.rowcount
                if rowcount == 1:
                    connection.commit()
                else:
                    connection.rollback()

                return res[0][1]
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", print_exc(e))


if __name__ == "__main__":
    db = node()
    db.get_slide("KL20-12031_B_2.35.1")
