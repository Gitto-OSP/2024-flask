import pyrebase
import json 

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_item(self,name,data,img_path):
        item_info={
            "name":data['name'],
            "seller":data['seller'],
            "price":data['price'],
            "chat":data['chat'],
            "tradeRegions":data['tradeRegions'],
            "choice":data['choice'],
            "img_path":img_path,
            "userComments":data['userComments']
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
    def insert_booth(self, data):
        booth_name = data['name']
        self.db.child("season").child(booth_name).set(data)
        print(data)
        return True
    
    def insert_brand(self, data):
        brand_name = data['name']
        self.db.child("brand").child(brand_name).set(data)
        print(data)
        return True

    # 중고거래용 get db
    def get_items(self):
        # item 노드 아래 값들 가져오기
        items = self.db.child("item").get().val()
        return items
    
    # 시즌페이지 get db
    def get_seasons(self):
        seasons = self.db.child("season").get().val()
        return seasons
    
    def get_seasons_bycategory(self,cate):
        items = self.db.child("season").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['boothLocation']==cate:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value",target_value)
        new_dict={}

        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    # 공구페이지 get db
    def get_gp(self):
        gp = self.db.child("gp_item").get().val()
        return gp
    
    def get_gp_bycategory(self,cate):
        items = self.db.child("gp_item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['status']==cate:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value",target_value)
        new_dict={}

        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    # 동문브랜드 get db
    def get_brand(self):
        brand = self.db.child("brand").get().val()
        return brand
    
    def get_item_byname(self,name):
        items=self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value==name:
                target_value=res.val()
        return target_value
    
    def get_item_bycategory(self,cate):
        items = self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['tradeRegions']==cate:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value",target_value)
        new_dict={}

        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    def get_booth_byname(self,name):
        items=self.db.child("season").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value==name:
                target_value=res.val()
        return target_value
    
    def get_gp_byname(self,name):
        items=self.db.child("gp_item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value==name:
                target_value=res.val()
        return target_value
    
    def get_brand_byname(self,name):
        items=self.db.child("brand").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value==name:
                target_value=res.val()
        return target_value
    
    # 회원가입
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname'],
            "email": data['email'],
            "phone": data['phone'],
            "profile_image": "static/image/profile.png",
            "flower_index": data['flower_index']  # 배꽃지수 1.0으로 저장
        }
        
        if self.user_duplicate_check(data['id']):
            self.db.child("user").push(user_info)
            #print("New user registered:", user_info)
            return True
        else:
            return False

    # 회원가입 중복체크
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        
        if users.val() is None:
            return True
        
        for res in users.each():
            if res.val().get('id') == id_string:
                return False
        return True    

    # 로그인
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        #target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:    #입력받은 아이디와 비밀번호의 해시값이 동일한 경우가 있는지 확인
                return True
        return False
    
    def get_userInfo(self,id_, key):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id']==id_:
                return value[key]
        return -1
    
    # 닉네임 중복 체크
    def nickname_exists(self, nickname):
        users = self.db.child("user").get()
        for res in users.each():
            if res.val().get('nickname') == nickname:
                return True  # 닉네임이 존재하면 True 반환
        return False  # 닉네임이 존재하지 않으면 False 반환

    
    def get_items(self):
        # item 노드 아래 값들 가져오기
        items = self.db.child("item").get().val()
        return items
    
    def get_item_byname(self,name):
        items=self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value==name:
                target_value=res.val()
        return target_value
    
    def get_bookmark_byname(self,uid,name):
        bookmarks = self.db.child("bookmark").child(uid).get()
        target_value=""
        if bookmarks.val() == None:
            return target_value
        
        for res in bookmarks.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value
    
    def update_bookmark(self,user_id,isBookmark,item):
        bookmark_info = {
            "interested": isBookmark
        }
        self.db.child("bookmark").child(user_id).child(item).set(bookmark_info)
        return True
    #리뷰작성
    def reg_review(self,data,img_path):
        review_info={
            "name":data['name'], #상품이름
            "writer":data['seller'], #작성자
            "title":data['price'], #리뷰제목
            "rate":data['star'],
            "review":data['userComments'],
            "img_path":img_path
        }
        self.db.child("review").push(review_info)
        print(data)
        return True 
    
    def get_reviews(self):
        reviews=self.db.child("review").get().val()
        return reviews
    
    def get_review_byname(self,name):
        items=self.db.child("review").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value==name:
                target_value=res.val()
        return target_value
    
    def get_reviews_bywriter(self,writer):
        reviews=self.db.child("review").get()
        target_value=[]
        target_key=[]
        for res in reviews.each():
            value=res.val()
            key_value=res.key()

            if value['writer']==writer:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value",target_value)
        new_dict={}

        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict

    def get_liked_items(self, user_id):
        bookmarks = self.db.child("bookmark").child(user_id).get()
        linked_items = []
        if bookmarks.val():
            for res in bookmarks.each():
                if res.val().get("interested") == "Y":
                    item_data = self.db.child("item").child(res.key()).get().val()
                    if item_data:  # item_data가 None이 아닌 경우만 처리
                        img_list = item_data.get("img_path", [])
                        item = {
                            "id": res.key(),  # ID
                            "img_path": img_list,  # 첫 번째 이미지 경로
                            "tradeRegions": item_data.get("tradeRegions", ""),  # 거래 지역
                            "price": item_data.get("price", 0)  # 가격
                        }
                        linked_items.append(item)
        return linked_items or []
    
    #공동구매
    def insert_gp_item(self,name,data,img_path):
        gp_item_info={
            "name":data['name'],
            "seller":data['seller'],
            "price":data['price'],
            "company":data['company'],
            "provideRegions":data['provideRegions'],
            "options":data['options[]'],
            "startDate":data['startDate'],
            "endDate":data['endDate'],
            "status":data['status'],
            "img_path":img_path,
            "userComments":data['userComments']
        }
        self.db.child("gp_item").child(name).set(gp_item_info)
        return True

    def edit_profile(self,id_, data, img_path):
        key = -1
        val = {}
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id']==id_:
                key = res.key()
                val = value
        new_prof={
            "email": val["email"],
            "id":id_,
            "phone":data['phone'],
            "pw":data['pw'],
            "nickname":data['nickname'],
            "profile_image":img_path
        }
        self.db.child("user").child(key).set(new_prof)