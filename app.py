from flask import Flask, render_template, request
import sys

application = Flask(__name__)

@application.route("/")
def hello():
    render_template("index.html")
    return render_template("season.html")

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


@application.route("/submit_item")
def reg_item_submit():
    idInput=request.args.get("idInput")
    productNameInput=request.args.get("productNameInput")
    priceInput=request.args.get("priceInput")
    reginInput=request.args.get("tradeRegions[]")
    productStateInput=request.args.get("choice")
    description=request.args.get("description")

    print(idInput,productNameInput,priceInput,reginInput,productStateInput)
    #return render_template("reg_items.html")


@application.route("/submit_item_post",methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    print(data)
    return render_template("submit_item_result.html",data=data,img_path="static/image/{}".format(image_file.filename))

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=Ture)
