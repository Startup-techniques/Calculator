from flask import Flask, request, abort, g
import sqlite3
import math as m

app = Flask(__name__)

DATABASE = 'calculator.db'
ENV = {
    "__builtins__": {},
    "pi": m.pi,
    "e": m.e,
    "sin": m.sin,
    "cos": m.cos,
    "tan": m.tan,
    "asin": m.asin,
    "acos": m.acos,
    "atan": m.atan,
    "sqrt": m.sqrt,
    "sinh": m.sinh,
    "cosh": m.cosh,
    "tanh": m.tanh,
    "asinh": m.asinh,
    "acosh": m.acosh,
    "atanh": m.atanh,
}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        db.execute("CREATE TABLE IF NOT EXISTS history (exp TEXT, res TEXT);")
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


@app.route("/history", methods=["GET"])
def history():
    buffer = []
    try:
        for row in query_db("SELECT * FROM history"):
            buffer.append(row[0] + " = " + row[1])
        return buffer
    except Exception as e:
        abort(500, description=e)


@app.route("/submit", methods=["POST"])
def submit():
    exp = request.form.get("exp")
    if exp is None:
        abort(400, description="Failed to get expression")
    try:
        res = str(eval(exp, ENV))
        db = get_db()
        db.execute(f"INSERT INTO history(exp, res) VALUES ('{exp}', '{res}');")
        db.commit()
        return res
    except Exception as e:
        abort(500, description=e)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    init_db()
    app.run()
