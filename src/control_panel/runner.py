from flask import Flask, render_template, jsonify, request

from src.logger import logger

app = Flask(__name__)


@app.route("/logs", methods=["POST", "GET"])
def logs():
    if request.method == "GET":
        return render_template("index.html", logs=logger.logs)
    else:
        return "".join([log.get_html() for log in logger.logs[::-1]])


def run():
    app.run()


if __name__ == "__main__":
    run()
