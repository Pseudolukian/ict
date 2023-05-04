from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union, Any, Dict, List, Optional

class OS_data(BaseModel):
    ID: int =2169
    DisplayName: str ='Ubuntu 18.04 x64'
    Name: str ='Ubuntu18.04x64'
    DCLocation: str = ""
    Hdd: int = 10
    Family: str ='Linux'
    IsAvailableISP: bool =True
    IsISPLiteEnabled: bool =True
    IsISPBusinessEnabled: bool =True
    Type: str ='GoldServer'
    LinkedSshKeys: list = []
    OperatingSystemType: str ='Ubuntu'