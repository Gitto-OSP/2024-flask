from flask import Flask, render_template
import sys

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/season")
def view_list():
    return render_template("season.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=Ture)