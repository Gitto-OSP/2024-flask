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
            "tradeRegions":data['tradeRegions'],
            "choice":data['choice'],
            "img_path":img_path,
            "userComments":data['userComments']
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
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

    # 회원가입
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            #"nickname": data['nickname'],
            "email": data['email'],
            "phone": data['phone']
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
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:    #입력받은 아이디와 비밀번호의 해시값이 동일한 경우가 있는지 확인
                return True
        return False
    
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
        self.db.child("review").child(data['name']).set(review_info)
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