import inspect
from typing import Type,Optional
from fastapi import Form
from pydantic import BaseModel


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
    age : int

@as_form
class updatenewbody(BaseModel):
    name : Optional[str]
    age : Optional[int]
   
        