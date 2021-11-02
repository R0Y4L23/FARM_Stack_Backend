import inspect
from typing import Type,Optional,List
from fastapi import Form
from pydantic import BaseModel
from datetime import datetime


def as_form(cls: Type[BaseModel]):
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]
    async def _as_form(**data):
        return cls(**data)
    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


@as_form
class newbody(BaseModel):
    name : str
    username : str
    password : str
    email : str
    age : int
    connections : List[str] = []

@as_form
class updatenewbody(BaseModel):
    name : Optional[str]
    age : Optional[int]

@as_form
class loginbody(BaseModel):
    email : str
    password : str

@as_form
class todo(BaseModel):
    title : str
    description : str
    status : str = "Pending"
    deadline : str
    createdon: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    createdby: str
    sharedto: List[str]=[]
    updated : bool = False

@as_form
class todoupdate(BaseModel):
    title : Optional[str]
    description : Optional[str]
    status : Optional[str]
    deadline : Optional[str]
    createdon: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    updated : bool = True
    sharedto: Optional[List[str]]

   
        