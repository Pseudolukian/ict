from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union, Any, Dict, List, Optional

class CreateServer(BaseModel):
    """
    *Upload server data Pydantic model*
    This is Pydantic model describing a 1cloud API server create method and validating all required fields of server create method.
    Also model has a validor, each convert DCLocation data from public VDC name to inner tech name.
    """

    Name: str = "Demo_API_Server"
    CPU: int = Field(default=1, gt=0, le=16)  #Number of vCPUs (in units)
    RAM: int = Field(default=1 * 1024, gt=1 * 1023, le=16 * 1024)  #Value of RAM in MB.
    HDD: int = Field(default=40, gt=39, le=240)  #Value of HDD in GB.
    ImageID: str = "3492" #ID of OS template. Taking from config file.
    HDDType: str = Field(default="SSD", choices=["SSD", "HDD"]) #Type of HDD. May only a SSD or HDD.
    isHighPerformance: str = Field(default="false", choices=["false", "true"]) #VDC pull level. Can be false or true.
    DCLocation: str = Field(default="SdnSpb")  #Technical name of VDC. Automaticaly cahnging by validator.
    isBackupActive: str = Field(default="false", choices=["false", "true"]) #Option using by set a backup mechanism. Can be false or true.
    BackupPeriod: str = Field(default="0", choices=["0","7","14","28"]) #Option using by set a backup period. Can be 0,7,14, and 28 days.