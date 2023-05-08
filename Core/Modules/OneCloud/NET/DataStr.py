from pydantic import BaseModel, Field

class LinkedNetwork(BaseModel):
    """
    Networks connected to Server.
    """
    LinkID:int
    NetworkID:int
    LinkState:str
    NetworkType:str
    NetworkName:str
    IP:str
    MAC:str
    Mask:str
    Gateway:str
    Bandwidth:int