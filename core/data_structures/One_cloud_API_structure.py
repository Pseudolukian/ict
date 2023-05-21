import json
from typing import Optional
from pathlib import Path
from pydantic import validator, BaseModel, Field



#==============1cloud server API requests==============#
class ServerData(BaseModel):
    """
    Pydantic model for uploading server data.

    This model describes the server create method and validates all the required fields.
    It includes a validator that converts the DCLocation data from the public VDC name to the inner technical name.
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
        Function to convert human-readable VDC name to the technical name required to create the server.

        Returns:
            str: Technical name of the VDC.
        """
        conf_path = Path("./data/ict_conf.json")
        conf_data = json.load(open(conf_path, 'r'))
        for vdc in conf_data["VDC_list"]:
            if vdc["Title"] == value:
                return vdc["TechTitle"]

#======1cloud API servers_list=============

class ServerDataFilter(BaseModel):
    """
    Pydantic model for filtering server data.
    This model is used to filter server data based on various criteria.
    """
    ID:Optional[str]
    Name:str
    CPU:int
    RAM:int
    HDD:int
    HDDType:str

class Server_VDC_data_saver(BaseModel):
    """_
    Pydantic model for saving server VDC data.
    This model represents the VDC data for a server and includes additional options.
    """
    Name:str
    isHighPerformance: str = Field(default="false", choices=["false", "true"]) #VDC pull level. Can be false or true.
    DCLocation: str = Field(default="Xelent")  #Technical name of VDC. Automaticaly cahnging by validator.
    isBackupActive: str = Field(default="false", choices=["false", "true"]) #Option using by set a backup mechanism. Can be false or true.
    BackupPeriod: str = Field(default="0", choices=["0","7","14","28"]) #Option using by set a backup period. Can be 0,7,14, and 28 days.
    ImageID: str = "3492" #ID of OS template. Taking from config file.



#==============1cloud VDC API requests==============#      

class VDC_data(BaseModel):
    """
    Pydantic model for VDC (Virtual Data Center) data.
    This model represents the data for a VDC.
    """
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
    """
    Pydantic model for OS (Operating System) data.
    This model represents the data for an operating system.
    """
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


