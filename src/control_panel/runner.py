from json import JSONDecodeError

from flask import Flask, render_template, redirect, request
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import pymongo

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
        return render_template("db.html", data=None, collections=db.list_collection_names())
    else:
        query = request.form.get("query")
        collection = request.form.get("collection")

        if not (query or collection) or collection not in db.list_collection_names():
            d = {}

            for name in db.collection_names(include_system_collections=False):
                d[name] = []
                for c in db[name].find({}):
                    d[name].append(c)

            return d
        else:
            try:
                data = [doc for doc in db[collection].find(json.loads(query))]
            except (JSONDecodeError, TypeError):
                data = [doc for doc in db[collection].find({"_id": query})]
            return render_template("db.html", data=data, collections=db.list_collection_names())


def run():  # run from main.py
    app.run()


if __name__ == "__main__":
    run()
