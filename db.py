from bson.objectid import ObjectId
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://subham:subham@cluster0.i3tcr.mongodb.net/FARMStack?retryWrites=true&w=majority")
mydb = myclient["FARMStack"]
mycol = mydb["users"]
todoCol = mydb["todos"]

def insert_info(data):
    mycol.insert_one({"name":data['name'],"age":data['age']})

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