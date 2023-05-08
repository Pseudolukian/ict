from ..NET.DataStr import LinkedNetwork
from pydantic import BaseModel, validator, Field
from typing import List, Optional, Any

class ServerCreate(BaseModel):
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
    SshKeys:List[int] = Field(default=None)


class ServerChange(BaseModel):
    """
    This Pydantic model describing the data needing to change server configuration.
   
    """
    ID:int
    CPU:int = Field(default=1, gt=0, le=16)  #Number of vCPUs (in units)
    RAM:int = Field(default=1, gt=1023, le=16 * 1024)  #Value of RAM in MB.
    HDD:int = Field(default=40, gt=39, le=240)  #Value of HDD in GB.
    HDDType: str = Field(default="SSD", choices=["SSD", "HDD"]) #Type of HDD. May only a SSD or HDD.
    isHighPerformance: str = Field(default="false", choices=["false", "true"]) #VDC pull level. Can be false or true.

class ServerStatus(BaseModel):
    """
    This Pydantic model describing the data recived from 1cloud API server when server status api calling.
   
    """
    ID:int
    Name:str
    State:str = Field(choices = ["Active", "New", "Blocked", "NeedMoney"])
    IsPowerOn:bool = Field(choises = [True, False])
    CPU:int 
    RAM:int
    HDD:int
    HDDType:str
    IP:str
    AdminUserName:str
    AdminPassword:str
    Image:str
    IsHighPerformance:bool = Field(choises = [True, False])
    PrimaryNetworkIp:str
    DCLocation:str
    ImageFamily:str
    LinkedSshKeys:Optional[List[Any]]
    LinkedNetworks:List[LinkedNetwork]

class ServersList(BaseModel):
    ServersList:List[ServerStatus]  

class ServerDelete(BaseModel):
    ID:int

class ServerRebuild(BaseModel):
    ID:int
    ImageId:int

class ServerAction(BaseModel):
    ID:int
    Type:str = Field(choices = ["PowerOn","PowerOff","ShutDownGuestOS", "RebootGuestOS","PowerReboot"])

class ServerConnectToNET(BaseModel):
    ID:int
    Type:str = Field(choices = ["AddNetwork", "RemoveNetwork"])
    NetworkID:int


class ServerChangeAnswer(BaseModel):
    ID:int
    Type:str
    State:str
    StartDate:str
    EndDate:str
