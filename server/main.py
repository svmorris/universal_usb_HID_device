import time
import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
DATABASE = "db.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                time INTEGER NOT NULL
            )
        """)


def insert_new(text: str, etime: int):
    """ Insert a new row to the table """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (text, time) VALUES (?,?)", (text, etime))
        conn.commit()
        return cur.lastrowid


def get_last():
    """ Fetch the last entry in the table """
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        return dict(row) if row else None


class typeData(Resource):
    def get(self):
        data = get_last()
        if data:
            return data, 200
        else:
            return {"error", "error fetching the last item in the database"}, 500

    def post(self):
        data = request.get_json()
        text = data.get("text")
        if not text:
            return {"error": "no text provided"}, 400

        etime = int(time.time())
        ret = insert_new(text, etime)

        if ret:
            return {"status": "ok"}, 200
        else:
            return {"error": "Unknown error while inserting in the database"}, 500



api.add_resource(typeData, "/68d26871-87e0-8330-9f47-f4fafb389302/typedata")



if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=31337)



