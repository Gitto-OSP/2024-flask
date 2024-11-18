from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB=DBhandler()

@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('view_list'))

@application.route("/season")
def view_list():
    page = request.args.get("page",0,type=int)
    per_page = 10 #item count to display per page
    per_row = 5 #item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_items() #read the table
    item_counts = tot_count = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    
    for i in range(row_count): #last row
        if(i == row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template("season.html", 
                           datas=data.items(), 
                           row1 = locals()['data_0'].items(),
                           row2 = locals()['data_1'].items(),
                           limit=per_page,
                           page = page,
                           page_count = int((item_counts/per_page)+1),
                           total=item_counts)

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

@application.route("/signup")
def view_signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.insert_user(data,pw_hash):
        flash("successful signup") #추가
        return render_template("index.html")
    else:
        flash("user id already exist")
    return render_template("signup.html")

#아이디 중복체크
@application.route("/check_id", methods=['GET'])
def check_id():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"success": False, "message": "아이디를 제공해야 합니다."}), 400

    # Firebase에서 중복 아이디 확인
    result = DB.user_duplicate_check(user_id)
    if result:
        return jsonify({"success": True, "message": "사용 가능한 아이디입니다."})
    else:
        return jsonify({"success": False, "message": "이미 존재하는 아이디입니다."})

@application.route("/mypage")
def view_mypage():
    return render_template("mypage.html")

@application.route("/editProfile")
def view_editProfile():
    return render_template("editProfile.html")
@application.route("/myBookmark")
def view_myBookmark():
    return render_template("myBookmark.html")

@application.route("/myGroupBuy")
def view_myGroupBuy():
    return render_template("myGroupBuy.html")

@application.route("/myReview")
def view_myReview():
    return render_template("myReview.html")

@application.route("/mySale")
def view_mySale():
    return render_template("mySale.html")

@application.route("/reg_season")
def view_regseason():
    return render_template("reg_season.html")

@application.route("/reg_items")
def view_regitems():
    return render_template("reg_items.html")

@application.route("/reg_group_purchase")
def view_regGroupPurchase():
    return render_template("reg_group_purchase.html")

@application.route("/reg_brand")
def view_regbrand():
    return render_template("reg_brand.html")

@application.route("/reg_reviews")
def view_regreviews():
    return render_template("reg_reviews.html")

@application.route('/specificReview')
def specificReview():
    return render_template('specificReview.html')

@application.route('/writerReview')
def writerReview():
    return render_template('writerReview.html')

@application.route("/group_purchase")
def view_grouppurchase():
    return render_template("group_purchase.html")

@application.route("/brand_1")
def view_brand1():
    return render_template("brand_1.html")

@application.route("/mygroup_purchase")
def mygroup_purchase():
    return render_template("mygroup_purchase.html")

@application.route("/mySpecificReview")
def mySpecificReview():
    return render_template("mySpecificReview.html")

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
    DB.insert_item(data['name'],data,image_file.filename)
    return render_template("submit_item.html", data=data,  img_path="static/images/{}".format(image_file.filename))

@application.route("/submit_items")
def reg_items_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    price=request.args.get("price")
    addr=request.args.getlist("tradeRegions")
    status=request.args.get("choice")
    print(name, seller, addr, price, status)

@application.route("/info_item/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data=DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("submit_item_result.html",name=name,data=data)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
