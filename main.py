from fastapi import FastAPI,Depends,Header
from fastapi.middleware.cors import CORSMiddleware
from model import (newbody,updatenewbody,loginbody,todo,todoupdate)
from db import (insert_info,get_all_info,get_info_by_id,update_info_by_id,delete_info_by_id,verify_login,post_todo,update_todo)
from jose import jwt

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = "thisIsA32CharactersLongSecretKey"
ALGO = "HS256"

def jwt_decode(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGO])

def jwt_encode(data: dict):
    token = jwt.encode(data, SECRET, algorithm=ALGO)
    return token


@app.get("/")
def Testing_the_API():
    return {"Message":"This is working"}

@app.get("/new")
def Testing_a_new_route():
    return {"Message":"This is a new route"}

@app.get("/infos")
def Get_all_information(authorization: str = Header(None)):
    a=check_token(authorization)
    if(a["Status"]):
        return {"Message":a["Message"],"Body":get_all_info()}
    else:
        return {"Message":a["Message"]}
    
@app.get("/info")
def Get_info_by_id(authorization: str = Header(None)):
    a=check_token(authorization)
    if(a["Status"]):
        return {"Message":"Retrieved Successfully","Body":get_info_by_id(a["Email"])}
    else:
        return {"Message":a["Message"]}
   

@app.post("/register")
def Upload_info(body : newbody = Depends(newbody.as_form)):
    a=insert_info(body.dict())
    if a:
        return {"Message":"Successfully Registered","Token":jwt_encode({"email":body.dict()['email']})}
    else:
        return {"Message":"Failed to Register"}

@app.post("/login")
def Verify_login(body : loginbody = Depends(loginbody.as_form)):
    a=verify_login(body.dict())
    if a:
        return {"Message":"Successfully Logged in","Token":jwt_encode({"email":body.dict()['email']})}
    else:
        return {"Message":"Failed to Log in"}

@app.put("/info")
def Update_info_by_id(body : updatenewbody = Depends(updatenewbody.as_form),authorization: str = Header(None)):
    a=check_token(authorization)
    if(a["Status"]):
        update_info_by_id(a["Email"],body.dict())
        return {"Message":"Updated Successfully"}
    else:
        return {"Message":a["Message"]}

@app.delete("/info")
def Delete_info_by_id(authorization: str = Header(None)):
    a=check_token(authorization)
    if(a["Status"]):
        delete_info_by_id(a["Email"])
        return {"Message":"Deleted Successfully"}
    else:
        return {"Message":a["Message"]}

@app.post("/todo")
def Post_todo(body : todo = Depends(todo.as_form),authorization: str = Header(None)):
    a=check_token(authorization)
    if(a["Status"]):
        post_todo(body.dict())
        return {"Message":"Successfully Posted"}
    else:
        return {"Message":a["Message"]}

@app.put("/todo/{uid}")
def Update_todo(uid:str,body : todoupdate = Depends(todoupdate.as_form),authorization: str = Header(None)):
    a=check_token(authorization)
    if(a["Status"]):
        update_todo(uid,body.dict())
        return {"Message":"Updated Successfully"}
    else:
        return {"Message":a["Message"]}

def check_token(token: str):
    if token:
        try:
            data = jwt_decode(token)
            return {"Message":"You are logged in as {}".format(data["email"]),"Status":True,"Email":data["email"]}
        except:
            return {"Message":"Invalid Token","Status":False}
    else:
        return {"Message":"Please provide a Token","Status":False}