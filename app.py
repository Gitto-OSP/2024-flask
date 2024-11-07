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
    return render_template("reg_reviews.html")

@application.route("/signin")
def view_signin():
    return render_template("signin.html")

@application.route('/specificReview')
def specificReview():
    return render_template('specificReview.html')

@application.route('/writerReview')
def writerReview():
    return render_template('writerReview.html')

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    form_data = request.form
    print("POST로 수신된 데이터:")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    print(form_data.getlist('tradeRegions'))
    
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form
    return render_template("submit_item_result.html", data=data,  img_path="static/images/{}".format(image_file.filename))

@application.route("/submit_items")
def reg_items_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    price=request.args.get("price")
    addr=request.args.getlist("tradeRegions")
    status=request.args.get("choice")
    print(name, seller, addr, price, status)

@application.route("/group_purchase")
def view_grouppurchase():
    return render_template("group_purchase.html")

@application.route("/brand_1")
def view_brand1():
    return render_template("brand_1.html")

@application.route("/mygroup_purchase")
def mygroup_purchase():
    return render_template("mygroup_purchase.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
