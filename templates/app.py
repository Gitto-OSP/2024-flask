from flask import Flask, render_template,request
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
@application.route("/reg_items")
def view_reg_items():
    return render_template("reg_items.html")

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
        data=request.form
        return render_template("submit_item_result.html",data=data)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
