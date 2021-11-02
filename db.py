from bson.objectid import ObjectId
import pymongo
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def check_password(password,hashed):
    return bcrypt.checkpw(password.encode('utf8'), hashed)

myclient = pymongo.MongoClient("mongodb+srv://subham:subham@cluster0.i3tcr.mongodb.net/FARMStack?retryWrites=true&w=majority")
mydb = myclient["FARMStack"]
mycol = mydb["users"]
todoCol = mydb["todos"]

def verify_login(data):
    data2 = mycol.find_one({"email":data["email"]})
    if data2==None:
        return False
    if check_password(data["password"],data2["password"]):
        return True
    else:
        return False

def insert_info(data):
    c1=mycol.find_one({"email":data["email"]})
    if c1!=None:
        return False
    c2=mycol.find_one({"username":data["username"]})
    if c2!=None:
        return False
    mycol.insert_one({"email":data["email"],"username":data["username"],"password":hash_password(data["password"]),"name":data['name'],"age":data['age'],"connections":data['connections']})
    return True

def get_all_info():
    data = mycol.find()
    a=[]
    for d in range(data.count()):
        a.append({"_id":str(data[d]["_id"]),"name":data[d]["name"],"age":data[d]["age"]})
    return a

def get_info_by_id(uid):
    data = mycol.find_one({"_id":ObjectId(uid)},{"name":1,"age":1,"_id":0})
    return data

def update_info_by_id(uid,body):
    a={}
    for key in body:
        if body[key]!=None:
            a[key]=body[key]
    mycol.update_one({"_id":ObjectId(uid)},{"$set":a})

def delete_info_by_id(uid):
    mycol.delete_one({"_id":ObjectId(uid)})

def post_todo(data):
    todoCol.insert_one(data)

def update_todo(uid,body):
    a={}
    for key in body:
        if body[key]!=None:
            a[key]=body[key]
    todoCol.update_one({"_id":ObjectId(uid)},{"$set":a})