from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union, Any, Dict, List, Optional

class VDC_data(BaseModel):
    Title: str = "Xelent"
    TechTitle: str = "SdnSpb"
    IsEnableLowPool: bool = True
    IsEnableHighPool: bool = True
    ShortTitle: str = "СПБ"
    ID: int = 1
    Country: str = "Россия"
    City: str = "Санкт-Петербург"
    IsEnableBackup: bool = True
    IsEnableIpV6: bool = False
    IsOnlyForAdmins: bool = False
    HiddenToNewProjects: Optional[str | bool] = ""
    IsFirewallEnabled: bool = True