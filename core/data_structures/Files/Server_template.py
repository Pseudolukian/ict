from pydantic import BaseModel, Field


class ServerTemplate(BaseModel):
    CPU:int = Field(default=1)
    RAM:int = Field(default=1024)
    HDD:int = Field(default= 40)
    HDDType:str = Field(default="SSD", choices = ["SSD","HDD"])
    ImageID:str = Field(default="3492")