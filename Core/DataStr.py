from pydantic import BaseModel, Field, validator
from pydantic.types import constr
import json
from typing import Dict, Any, Optional




class CommandData(BaseModel):
    Data: str = Field(default=None)
        
class CorePort(BaseModel):
    APi_key: constr(strip_whitespace=True, min_length=64, max_length=64)
    Module: str
    Command: str
    Data: Optional[CommandData]


    @validator("Data", pre=True, always=True)
    def converter_to_dict(cls, value):
        if value is not None:
            return value.dict()

    
     
