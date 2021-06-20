import psycopg2
from psycopg2 import extras
import json
from contextlib import contextmanager
from traceback import print_exc


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
        cur = con.cursor()
        try:
            yield con, cur
        finally:
            cur.close()
            self.conn.putconn(con)

    def create_films(self, films):
        payload = self.unpack_films(films)
        sql = "INSERT INTO films (id) VALUES %s RETURNING id"
        with self.db() as (connection, cursor):
            try:
                # Initially a film is not in a slot
                # TODO: Add film pos
                extras.execute_values(cursor, sql, payload)

                connection.commit()

                return films

            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General error:", e)

    # helper function
    # unpack list of film ids from object
    def unpack_films(self, data):
        payload = []
        for i in data:
            id = list(data[i][0:6])
            id = "".join(map(str, id))
            payload.append((id,))

        return payload

    def update_film(self, data):
        print("update film data: {}".format(data))
        sql = "UPDATE slides set location = %s where slideid = %s"
        slot = data["slot"]
        # box = data["box"]
        film = data["film"]
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (slot, film))
                # id = cursor.fetchone()[0]

                rowcount = cursor.rowcount
                if rowcount == 1:
                    connection.commit()
                else:
                    connection.rollback()

                # new_film = {"id": id, "target": target}

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

    # TODO: Fix to add stored
    def update_box(self, update):
        with self.db() as (connection, cursor):
            try:
                cursor.execute(
                    "Update boxes set name = %s RETURNING id", (update,)
                )
                id = cursor.fetchone()[0]

                rowcount = cursor.rowcount
                if rowcount == 1:
                    connection.commit()
                else:
                    connection.rollback()

                new_box = {"id": id, "target": update}
                return new_box
            except psycopg2.Error as error:
                print("Database error:", error)
            except Exception as e:
                print("General Error:", e)

    def get_box(self):
        pass

    def get_film(self, film):
        print("get film request...{}".format(film))
        sql = "SELECT location from slides WHERE slideid = %s"
        with self.db() as (connection, cursor):
            try:
                cursor.execute(sql, (film,))

                connection.commit()

                data = cursor.fetchone()

                return data[0]
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

        self.create_film_slot(slots)

    def create_film_slot(self, data):
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

    def update_film_slot(self, slot):
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

    def read_film_slot(self, box):
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
