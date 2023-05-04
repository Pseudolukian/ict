from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union, Any, Dict, List, Optional

from ..OneCloud.Requests.Get_VDC_list import VDC_data
from ..OneCloud.Requests.Get_OS_list import OS_data

class VDC_config(VDC_data):
    
    
    class Config:
        """
        This section excluding fields from parent class VDC_data.
        """
        fields = {'ID': {'exclude': True}, 'Country': {'exclude': True}, 'City': {'exclude': True},
                  'IsEnableBackup': {'exclude': True},'IsEnableIpV6': {'exclude': True},'IsOnlyForAdmins': {'exclude': True},
                  'HiddenToNewProjects': {'exclude': True},'IsFirewallEnabled': {'exclude': True}
                  }


class OS_template_config(OS_data):
    
    
    class Config:
        fields = {'DCLocation':{'exclude':True},'Hdd':{'exclude':True},'Family':{'exclude':True},
                  'IsAvailableISP':{'exclude':True},'IsISPLiteEnabled':{'exclude':True},'IsISPBusinessEnabled':{'exclude':True},
                  'Type':{'exclude':True},'LinkedSshKeys':{'exclude':True},'OperatingSystemType':{'exclude':True},
                }


class Config_file(BaseModel):
    
    def datestamp_creator() -> str:
        date_now = datetime.now().strftime('%d.%m')
        return date_now

    API_key: str = Field(default=None, min_length=64, max_length=64)
    Datestamp: str = Field(default_factory=datestamp_creator)
    VDC_list: List[VDC_config]
    OS_list: List[OS_template_config]