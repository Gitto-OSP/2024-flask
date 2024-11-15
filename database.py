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
            "img_path":img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True

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






