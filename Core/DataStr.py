from pydantic import BaseModel, Field, validator
from pydantic.types import constr
import json
from typing import Dict, Any, Optional

class CommandData(BaseModel):
    Data: str

    def __str__(self):
        return self.Data
        
class CorePort(BaseModel):
    APi_key:constr(strip_whitespace=True, min_length=64, max_length=64)
    Module:str = Field(choises = ["Server"])
    Command:str = Field(choises = ["create","GetList","GetStatus"])
    Data: Optional[CommandData]

    @validator("Data")
    def json_to_dict_converter(cls, value) -> Dict[str, Any]:
        data_out = json.loads(value)
        return data_out
        


