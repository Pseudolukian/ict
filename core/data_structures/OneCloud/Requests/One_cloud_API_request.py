from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union, Any, Dict, List, Optional

class Urls(BaseModel):
    base_url: str = Field(default="https://api.1cloud.ru/")
    server_url:str = Field(default="server/")
    vdc_url:str = Field(default="dcLocation/")
    os_url:str = Field(default="image/")

    def server(self) -> str:
        return self.base_url + self.server_url
    
    def vdc(self) ->str:
        return self.base_url + self.vdc_url
    
    def os(self) -> str:
        return self.base_url + self.os_url


class Headers(BaseModel):
    Authorization:str = Field(default="Bearer ")

    @validator("Authorization", pre=True, always=True)
    def add_bearer_prefix(cls, value):
        if not value.startswith("Bearer "):
            return f"Bearer {value}"
        return value

class Request(BaseModel):
    headers:Headers
    data:Optional[Any] = Field(default=None)

    @validator("data")
    def json_render(cls,v):
        if v is None:
            pass
        else:
            return v.dict()
        
    @validator("headers")
    def dict_render(cls,v):
        return v.dict()