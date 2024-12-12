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
    
    def get_gp_item_for_calendar(self, start_date, end_date):
        gps = self.db.child("gp_item").order_by_child("startDate").start_at(start_date).end_at(end_date).get()
        return gps
    
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
            "flower_index": data['flower_index']
        }
        
        if self.user_duplicate_check(data['id']):
            self.db.child("user").push(user_info)
            return True
        else:
            return False
    
    # 사용자 정보 조회
    def get_userInfo(self, user_id, column=None):
        all_users = self.get_all_users()
        user = next((user for user in all_users if user['id'] == user_id), None)
        if user:
            if column:
                return user.get(column, None)
            return user
        return None 

    # 사용자의 flower_index를 반환
    def get_user_flower_index(self, user_id):
        user_info = self.get_userInfo(user_id, 'flower_index')  # column 인자로 'flower_index' 전달
        if user_info is not None:
            return user_info  # flower_index 반환
        return None
    
    """  
    
    # 사용자 정보 업데이트
    def update_userInfo(self, user_id, column, value):
        users = self.db.child("user").get()
        for res in users.each():
            user = res.val()
            if user['id'] == user_id:
                # 해당 사용자의 column을 업데이트
                user[column] = value
                # 변경된 사용자 정보 DB에 반영
                self.db.child("user").child(res.key()).update(user)
                return True
        return False """

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
        
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:    #입력받은 아이디와 비밀번호의 해시값이 동일한지 확인
                return True
        return False
            
            
            #if value.get('id') == id_ and value.get('pw') == pw_:    
            #    return True
        #return False
    
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
    def insert_gp_item(self,name,data,img_path, image_paths):
        gp_item_info={
            "name":data['name'],
            "seller":data['seller'],
            "price":data['price'],
            "company":data['company'],
            "provideRegions":data['provideRegions'],
            "options":data.getlist('options[]'),
            "startDate":data['startDate'],
            "endDate":data['endDate'],
            "status":data['status'],
            "img_path":img_path,
            "img_paths" : image_paths,
            "userComments":data['userComments'],
            "participants": {}
        }
        self.db.child("gp_item").child(name).set(gp_item_info)
        return name
    
    def add_participant(self, gp_item_name, user_info, selected_option):
        participant_data = {
            "user_id": user_info['id'],
            "email": user_info['email'],
            "option": selected_option
        }
        # 참여자 데이터 추가
        self.db.child("gp_item").child(gp_item_name).child("participants").push(participant_data)

        # 참여자 수 업데이트
        participants = self.db.child("gp_item").child(gp_item_name).child("participants").get().val()

        if participants:
            participant_count = len(participants)
        else:
            participant_count = 0

        return participant_count
    
    def get_gp_byseller(self, seller):
        gps = self.db.child("gp_item").get()
        target_values = []
        target_keys = []

        for gp in gps.each():
            value = gp.val()
            key_value = gp.key

            if value['seller'] == seller:
                gp_item_name = value['name']
                participants = self.db.child("gp_item").child(gp_item_name).child("participants").get().val()

                if participants:
                    participant_count = len(participants)
                else:
                    participant_count = 0

                value['participant_count'] = participant_count

                target_values.append(value)
                target_keys.append(key_value)
                

        print("###### Target Values:", target_values)

        # 새로운 딕셔너리 생성
        new_dict = {k: v for k, v in zip(target_keys, target_values)}
        return new_dict
    
    def get_gp_bybuyer(self, buyer):
        gps = self.db.child("gp_item").get()
        target_values = []
        target_keys = []

        for gp in gps.each():
            value = gp.val()
            key_value = gp.key

            # participants 목록 가져오기
            participants = self.db.child("gp_item").child(value['name']).child("participants").get().val()

            # participants 목록에 buyer ID가 있는지 확인
            if participants and buyer in participants:
                participant_count = len(participants)
                
                # 참가자 수 추가
                value['participant_count'] = participant_count
                target_values.append(value)
                target_keys.append(key_value)

        print("###### Target Values:", target_values)

        # 새로운 딕셔너리 생성
        new_dict = {k: v for k, v in zip(target_keys, target_values)}
        return new_dict


    def edit_profile(self,id_, data, img_path,flower_index):
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
            "flower_index": flower_index,
            "pw":data['pw'],
            "nickname":data['nickname'],
            "profile_image":img_path
        }
        self.db.child("user").child(key).set(new_prof)
    
    # db 연결 바꾸기...
    def get_sale_byname(self,uid,name):
        sales = self.db.child("item").child(uid).get()
        target_value=""
        if sales.val() == None:
            return target_value
        
        for res in sales.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value
    
    # db 연결 바꾸기...
    def get_sale_items(self, user_id):
        sales = self.db.child("item").get()
        linked_items = []
        if sales.val():
            for res in sales.each():
                if res.val().get("seller") == user_id:
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