import json
from typing import Optional
from pathlib import Path
from pydantic import validator, BaseModel, Field



#==============1cloud server API requests==============#
class ServerData(BaseModel):
    """
    *Upload server data Pydantic model*
    This is Pydantic model describing a 1cloud API server create method and validating all required fields of server create method.
    Also model has a validor, each convert DCLocation data from public VDC name to inner tech name.
    """

    Name: str = "Demo_API_Server"
    CPU: int = Field(default=1, gt=0, le=16)  #Number of vCPUs (in units)
    RAM: int = Field(default=1, gt=1023, le=16 * 1024)  #Value of RAM in MB.
    HDD: int = Field(default=40, gt=39, le=240)  #Value of HDD in GB.
    ImageID: str = "3492" #ID of OS template. Taking from config file.
    HDDType: str = Field(default="SSD", choices=["SSD", "HDD"]) #Type of HDD. May only a SSD or HDD.
    isHighPerformance: str = Field(default="false", choices=["false", "true"]) #VDC pull level. Can be false or true.
    DCLocation: str = Field(default="Xelent")  #Technical name of VDC. Automaticaly cahnging by validator.
    isBackupActive: str = Field(default="false", choices=["false", "true"]) #Option using by set a backup mechanism. Can be false or true.
    BackupPeriod: str = Field(default="0", choices=["0","7","14","28"]) #Option using by set a backup period. Can be 0,7,14, and 28 days.

    @validator("DCLocation", pre=True, always=True)
    def vdc_name_changer(cls, value) -> str:
        """
        The function changes human understandably VDC name to technical name needing to create the server.
        Returns:
            str: VDC tech name.
        """
        conf_path = Path("./data/ict_conf.json")
        conf_data = json.load(open(conf_path, 'r'))
        for vdc in conf_data["VDC_list"]:
            if vdc["Title"] == value:
                return vdc["TechTitle"]

#======1cloud API servers_list=============

class ServerDataFilter(BaseModel):
    ID:Optional[str]
    Name:str
    CPU:int
    RAM:int
    HDD:int
    HDDType:str

class Server_VDC_data_saver(BaseModel):
    Name:str
    isHighPerformance: str = Field(default="false", choices=["false", "true"]) #VDC pull level. Can be false or true.
    DCLocation: str = Field(default="Xelent")  #Technical name of VDC. Automaticaly cahnging by validator.
    isBackupActive: str = Field(default="false", choices=["false", "true"]) #Option using by set a backup mechanism. Can be false or true.
    BackupPeriod: str = Field(default="0", choices=["0","7","14","28"]) #Option using by set a backup period. Can be 0,7,14, and 28 days.
    ImageID: str = "3492" #ID of OS template. Taking from config file.



#==============1cloud VDC API requests==============#      

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

#==============1cloud OS API requests==============#       

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


