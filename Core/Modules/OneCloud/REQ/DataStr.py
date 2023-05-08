from pydantic import BaseModel, Field

class URLS(BaseModel):
    base:str = "https://api.1cloud.ru/"
    server:str = base + "server/"
    vdc:str = base + "dcLocation/"
    os:str = base + "image/"

class HEADERS(BaseModel):
    Authorization:str = Field(default="Bearer ")

    def __init__(self, Api_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Authorization = self.bound(Api_key)

    def bound(self, Api_key: str) -> str:
        return f"{self.Authorization}{Api_key}"
    