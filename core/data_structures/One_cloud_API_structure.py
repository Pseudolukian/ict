from pydantic import root_validator, validator, BaseModel, Field, ValidationError, constr
from typing import Optional
from enum import Enum


#==============1cloud server API requests==============#
class Server_Disk_System(str,Enum):
    SAS = "SAS"
    SSD = "SSD"

class VDC_performance_level(str,Enum):
    FALSE = "false"
    TRUE = "true"

class Server_backup(str,Enum):
    FALSE = "false"
    TRUE = "true"

class Backup_period(str,Enum):
    zero_days = "0"
    seven_days = "7"
    forteen_days = "14"   
    twenty_eight = "28" 

class ServerData(BaseModel):
    Name: str = "Demo_API_Server"
    CPU: int = Field(default = 1, gt=1, le=16) #Value in vCPU
    RAM: int = Field(default = 1, gt=1023, le=16*1024) #Value in MB
    HDD: int = Field(default = 40, gt=40, le=240) #Value in GB
    NetworkID: Optional[str] = None
    NetworkBandwidth: Optional[str] = None
    ImageID: str = "ubuntu20.04x64"
    HDDType: Server_Disk_System = Server_Disk_System.SSD #Value maust be one of option: "SSD" or "SAS".
    isHighPerformance: VDC_performance_level = VDC_performance_level.FALSE #Performance level of VDC 
    DCLocation: str = "xelent" #Technical name of VDC
    isBackupActive: Server_backup = Server_backup.FALSE #Server backup option.
    BackupPeriod: Backup_period = Backup_period.zero_days #Saving period backup in days.
    SshKeys: list[str] = [] #SSH-keys list

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