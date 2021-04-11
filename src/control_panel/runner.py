from flask import Flask, render_template, redirect, request
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from src.logger import logger

load_dotenv()
cluster = MongoClient(os.getenv("MONGO"))
db = cluster["toxic"]

app = Flask(__name__)


@app.route("/")
def home():
    return redirect("/logs", code=302)


@app.route("/logs", methods=["POST", "GET"])
def logs():
    if request.method == "GET":
        return render_template("logs.html", logs=logger.logs)
    else:
        return "".join([log.get_html() for log in logger.logs[::-1]])


@app.route("/db", methods=["POST", "GET"])
def db_():
    if request.method == "GET":
        return render_template("db.html")
    else:
        d = {}

        for name in db.collection_names(include_system_collections=False):
            d[name] = []
            for c in db[name].find({}):
                d[name].append(c)

        return d


def run():  # run from main.py
    app.run()


if __name__ == "__main__":
    run()
