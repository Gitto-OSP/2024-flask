from flask import Flask, render_template
import sys

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/season")
def view_list():
    return render_template("season.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/fleamarket")
def view_fleamarket():
    return render_template("fleamarket.html")

@application.route("/gonggu")
def view_gonggu():
    return render_template("gonggu.html")

@application.route("/graduatebrands")
def view_graduatebrands():
    return render_template("graduatebrands.html")

@application.route("/login")
def view_login():
    return render_template("login.html")

@application.route("/mypage")
def view_mypage():
    return render_template("mypage.html")

@application.route("/reg_items")
def view_regitems():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def view_regreviews():
    return render_template("reg_revies.html")

@application.route("/signin")
def view_signin():
    return render_template("signin.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=Ture)
