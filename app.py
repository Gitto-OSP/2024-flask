from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB=DBhandler()

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

#로그인: id,pw 대조
@application.route("/login_confirm", methods=['POST'])
def view_login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()    # db에 저장된 비밀번호 해시값으로 비교위한 해시값 생성
    if DB.find_user(id_,pw_hash):
        session['id']=id_    # session에 id 정보 삽입
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")    #db에 매칭 정보가 없으면 플래시 메세지 생성
        return render_template("login.html")

# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()    #session에 셋팅한 값들 모두 클리어, session id값 지워짐.
    return redirect(url_for('view_list'))

#여기까지(p9까지 완료)

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

@application.route("/reg_items")
def view_regitems():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def view_regreviews():
    return render_template("reg_reviews.html")

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
    DB.insert_item(data['name'],data,image_file.filename)
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
