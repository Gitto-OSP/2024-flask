from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys

import random
import string

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
    return render_template("./itemlist/season.html", 
                           datas=data.items(), 
                           row1 = locals()['data_0'].items(),
                           row2 = locals()['data_1'].items(),
                           limit=per_page,
                           page = page,
                           page_count = int((item_counts/per_page)+1),
                           total=item_counts)

@application.route("/review")
def view_review():
    page=request.args.get("page",0,type=int)
    per_page=10
    per_row=5
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_reviews() #read the table
    review_counts = tot_count = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    
    for i in range(row_count): #last row
        if(i == row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template("./itemlist/review.html", 
                           datas=data.items(), 
                           row1 = locals()['data_0'].items(),
                           row2 = locals()['data_1'].items(),
                           limit=per_page,
                           page = page,
                           page_count = int((review_counts/per_page)+1),
                           total=review_counts)

@application.route("/fleamarket")
def view_fleamarket():
    page = request.args.get("page",0,type=int)
    per_page = 25 #item count to display per page
    per_row = 5 #item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_items() #read the table
    item_counts = tot_count = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    rows=[]
    
    for i in range(row_count): #last row
        if(i == row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
        rows.append(locals()['data_{}'.format(i)].items())
    return render_template("./itemlist/fleamarket.html", 
                           datas=data.items(), 
                           rows = rows,
                           limit=per_page,
                           page = page,
                           page_count = int((item_counts/per_page)+1),
                           total=item_counts)

@application.route("/gonggu")
def view_gonggu():
    return render_template("./itemlist/gonggu.html")

@application.route("/graduatebrands")
def view_graduatebrands():
    return render_template("./itemlist/graduatebrands.html")

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
        flash("잘못된 아이디 혹은 비밀번호를 입력하셨습니다.")    #db에 매칭 정보가 없으면 플래시 메세지 생성
        return render_template("login.html")

# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()    #session에 세팅한 값들 모두 클리어, session id값 지워짐.
    return redirect(url_for('view_list'))

# DBhandler 인스턴스를 생성하고, 닉네임을 생성
db_handler = DBhandler()

# 랜덤 닉네임 생성
def generate_random_nickname(db_handler):
    while True:
        # 랜덤 문자열 생성 (예시로 8자리 닉네임)
        random_nickname = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # 닉네임 중복 체크
        if not db_handler.nickname_exists(random_nickname):
            return random_nickname  # 중복되지 않으면 반환

@application.route("/signup")
def view_signup():
    return render_template("signup.html")

# 성공 페이지 라우트 정의
@application.route('/success')
def success():
    #return "회원가입 성공!"
    return redirect(url_for('view_login'))

@application.route('/signup_post', methods=['POST'])
def register_user():
    
    user_data = {
        'id': request.form['id'],
        'email': request.form['email'],
        'phone': request.form['phone']
    }

    # 랜덤 닉네임 생성
    random_nickname = generate_random_nickname(db_handler)
    user_data['nickname'] = random_nickname
    
    # 디폴트 프로필 이미지 경로 추가
    default_profile_path = '/static/image/profile.png'
    user_data['profile_image'] = default_profile_path
    

    # 비밀번호 해시화
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    if db_handler.insert_user(user_data, password_hash):
        
        flash("회원가입 성공!", "success")
        return redirect(url_for('view_login'))  
    else:
        flash("회원가입 실패!", "error")
        return redirect(url_for('view_signup'))
    

#아이디 중복체크
@application.route("/check_id", methods=['GET'])
def check_id():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"success": False, "message": "아이디를 제공해야 합니다."}), 400

    # 중복 아이디 확인
    result = db_handler.user_duplicate_check(user_id)
    if result:
        return jsonify({"success": True, "message": "사용 가능한 아이디입니다."})
    else:
        return jsonify({"success": False, "message": "이미 존재하는 아이디입니다."})

@application.route("/mypage")
def view_mypage():
    return render_template("./mypage/mypage.html")

@application.route("/editProfile")
def view_editProfile():
    return render_template("./mypage/editProfile.html")
# @application.route("/myBookmark")
# def view_myBookmark():
#     return render_template("./mypage/myBookmark.html")

@application.route("/myGroupBuy")
def view_myGroupBuy():
    return render_template("./mypage/myGroupBuy.html")

@application.route("/myReview")
def view_myReview():
    return render_template("./mypage/myReview.html")

@application.route("/mySale")
def view_mySale():
    return render_template("./mypage/mySale.html")

@application.route("/reg_season")
def view_regseason():
    return render_template("./register/reg_season.html")

@application.route("/reg_items")
def view_regitems():
    return render_template("./register/reg_items.html")

@application.route("/reg_group_purchase")
def view_regGroupPurchase():
    return render_template("./register/reg_group_purchase.html")

@application.route("/reg_brand")
def view_regbrand():
    return render_template("./register/reg_brand.html")
#리뷰쓰기
@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("./register/reg_reviews.html",name=name)
#등록된 리뷰 DB 등록
@application.route("/reg_review",methods=['POST'])
def reg_review():
    data=request.form
    image_file=request.files["file"]
    image_file.save("static/DBimage/{}".format(image_file.filename))
    DB.reg_review(data,image_file.filename)
    return redirect(url_for('view_review'))

@application.route('/specificReview')
def specificReview():
    return render_template('./details/specificReview.html')

@application.route('/writerReview')
def writerReview():
    return render_template('./itemlist/writerReview.html')

@application.route("/group_purchase")
def view_grouppurchase():
    return render_template("./details/group_purchase.html")

@application.route("/brand_1")
def view_brand1():
    return render_template("./details/brand_1.html")

@application.route("/mygroup_purchase")
def mygroup_purchase():
    return render_template("./mypage/mygroup_purchase.html")

@application.route("/mySpecificReview")
def mySpecificReview():
    return render_template("./mypage/mySpecificReview.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    form_data = request.form
    files_data = request.files.getlist('selectedFile')
    img_path_list = []

    print("POST로 수신된 데이터:")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    print(form_data.getlist('tradeRegions'))
    
    for file in files_data:
        if file.filename: 
            img_path_format = f"static/DBimage/fleamarket{form_data['name']}{form_data['seller']}{file.filename}"
            file.save(img_path_format)
            img_path_list.append(img_path_format)

    DB.insert_item(form_data['name'], form_data, img_path_list)
    return render_template("./details/submit_item.html", data=form_data, img_path=img_path_list[0])

def process_season_data(form_data, form_files):
    main_image_file=form_files["boothMainImg"]
    main_image_path = f"static/DBimage/{form_data['name']}{form_data['boothNum']}{main_image_file.filename}"
    main_image_file.save(main_image_path)

    booth_data = {
        "name": form_data["name"],
        "seller": form_data["seller"],
        "boothLocation": form_data["boothLocation"],
        "boothNum": form_data["boothNum"],
        "openTime": form_data["openTime"],
        "closingTime": form_data["closingTime"],
        "boothComments": form_data["boothComments"],
        "boothMainImgPath" : main_image_path,
        "products": []
    }

    product_count = int(form_data["productNum"])

    for i in range(product_count):
        product_name = form_data[f"product{i}Name"]
        product_price = int(form_data[f"product{i}Price"])

        product_image_file = form_files.get(f"productImg{i}")
        product_img_path = f"static/DBimage/{booth_data['name']}{booth_data['boothNum']}{product_image_file.filename}"
        product_image_file.save(product_img_path)

        booth_data["products"].append({
            "name": product_name,
            "price": product_price,
            "img_path" : product_img_path
        })

    return booth_data


@application.route("/submit_season_post", methods=['POST'])
def reg_season_submit_post():
    form_data = request.form
    files_data = request.files
    
    print("POST로 수신된 데이터:")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    
    booth_data = process_season_data(form_data, files_data)  # 데이터 정제
    DB.insert_booth(booth_data)
    return render_template("./details/submit_item.html", data=booth_data,  img_path=booth_data['boothMainImgPath'])

def process_brand_data(form_data, files_data):
    brand_data = {
        "name": form_data["name"],
        "seller": form_data["seller"],
        "major": form_data["major"],
        "graduNum": form_data["graduNum"],
        "benefits": form_data["benefits"],
        "userComments": form_data["userComments"],
        "img_path" : [],
        "socials": []
    }

    for file in files_data:
        if file.filename: 
            img_path_format = f"static/DBimage/brand{form_data['name']}{form_data['seller']}{file.filename}"
            file.save(img_path_format)
            brand_data["img_path"].append(img_path_format)
    
    socialsType = ['instagram', 'x']
    for sns in socialsType:
        if(form_data.get(sns)): 
            brand_data["socials"].append({sns : form_data[sns]})
    
    etcUrls = form_data.getlist('etcUrl')
    etcNames = form_data.getlist('etcName')
    if etcUrls and etcNames:
        for name, url in zip(etcNames, etcUrls):  # 이름과 URL을 쌍으로 묶어서 처리
            brand_data["socials"].append({name: url})

    return brand_data

@application.route("/submit_brand_post", methods=['POST'])
def reg_brand_submit_post():
    form_data = request.form
    files_data = request.files.getlist('selectedFile')
    
    brand_data = process_brand_data(form_data, files_data)  # 데이터 정제
    DB.insert_brand(brand_data)
    return render_template("./details/brand_1.html", data=brand_data)

@application.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error", 500

@application.route("/submit_items")
def reg_items_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    price=request.args.get("price")
    addr=request.args.getlist("tradeRegions")
    status=request.args.get("choice")
    print(name, seller, addr, price, status)

@application.route("/submit_season")
def reg_season_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    boothLocation = request.args.get("boothLocation")
    boothNum=request.args.get("boothNum")
    openTime=request.args.get("openTime")
    closingTime=request.args.get("closingTime")
    addr=request.args.getlist("tradeRegions")
    status=request.args.get("choice")
    print(name, seller, addr, boothLocation, status)

@application.route("/submit_gpitem_post", methods=['POST'])
def reg_gpitem_submit_post(): 
    image_file=request.files["file"]
    image_file.save("static/DBimage/{}".format(image_file.filename))
    data=request.form
    DB.insert_gp_item(data['name'],data,image_file.filename)
    return render_template("./details/group_purchase.html", data=data,  img_path="static/DBimage/{}".format(image_file.filename))

@application.route("/info_item/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data=DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("./details/submit_item_result.html",name=name,data=data)
#리뷰 상세조회

@application.route("/submit_reviews")
def reg_reviews_submit():
    name=request.args.get("name")
    writer=request.args.get("writer")
    title=request.args.get("title")
    rate=request.args.getlist("rate")
    review=request.args.get("review")
    print(name, writer,title,rate,review)

@application.route("/info_review/<name>/")
def view_review_detail(name):
    print("###name:",name)
    data=DB.get_review_byname(str(name))
    print("####data:",data)
    return render_template("./details/specificReview.html",name=name,data=data)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)

@application.route('/show_bookmark/<name>/', methods=['GET'])
def show_bookmark(name):
    my_bookmark = DB.get_bookmark_byname(session['id'],name)
    return jsonify({'my_bookmark': my_bookmark})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_bookmark = DB.update_bookmark(session['id'],'Y',name)
    return jsonify({'msg': '관심글에 추가하였습니다.'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_bookmark = DB.update_bookmark(session['id'],'N',name)
    return jsonify({'msg': '관심글에서 삭제되었습니다.'})

@application.route("/myBookmark")
def view_liked_list():
    page = request.args.get("page",0,type=int)
    per_page = 15 #item count to display per page
    per_row = 5 #item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)

    user_id = session.get('id')
    if not user_id:
        return redirect('/login')
    
    data = DB.get_liked_items(user_id)
    like_counts = like_tot_count = len(data)

    if like_tot_count == 0:
        return render_template("./mypage/myBookmark.html", 
                               datas=[], 
                               rows=[], 
                               limit=per_page,
                               page=page,
                               page_count=1,
                               total=0)
    
    data = data[start_idx:end_idx]
    rows = [data[i:i + per_row] for i in range(0, len(data), per_row)]

    return render_template("mypage/myBookmark.html", 
                           datas=data, 
                           rows = rows,
                           limit=per_page,
                           page = page,
                           page_count = int((like_counts/per_page)+1),
                           total=like_tot_count)