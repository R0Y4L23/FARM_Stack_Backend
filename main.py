from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from model import (newbody,updatenewbody,loginbody,todo,todoupdate)
from db import (insert_info,get_all_info,get_info_by_id,update_info_by_id,delete_info_by_id,verify_login,post_todo,update_todo)

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

@app.get("/")
def Testing_the_API():
    return {"Message":"This is working"}

@app.get("/new")
def Testing_a_new_route():
    return {"Message":"This is a new route"}

@app.get("/info")
def Get_all_information():
    return {"Message":"Retrieved Successfully","Body":get_all_info()}
  

@app.get("/info/{uid}")
def Get_info_by_id(uid : str):
    return {"Message":"Retrieved Successfully","Body":get_info_by_id(uid)}
   

@app.post("/register")
def Upload_info(body : newbody = Depends(newbody.as_form)):
    a=insert_info(body.dict())
    if a:
        return {"Message":"Successfully Registered"}
    else:
        return {"Message":"Failed to Register"}

@app.post("/login")
def Verify_login(body : loginbody = Depends(loginbody.as_form)):
    a=verify_login(body.dict())
    if a:
        return {"Message":"Successfully Logged in"}
    else:
        return {"Message":"Failed to Log in"}

@app.put("/info/{uid}")
def Update_info_by_id(uid:str,body : updatenewbody = Depends(updatenewbody.as_form)):
    update_info_by_id(uid,body.dict())
    return {"Message":"Updated Successfully"}

@app.delete("/info/{uid}")
def Delete_info_by_id(uid : str):
    delete_info_by_id(uid)
    return {"Message":"Deleted Successfully"}

@app.post("/todo")
def Post_todo(body : todo = Depends(todo.as_form)):
    post_todo(body.dict())
    return {"Message":"Successfully Posted"}

@app.put("/todo/{uid}")
def Update_todo(uid:str,body : todoupdate = Depends(todoupdate.as_form)):
    update_todo(uid,body.dict())
    return {"Message":"Updated Successfully"}