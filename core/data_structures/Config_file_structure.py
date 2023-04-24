from typing import List, Union
from pydantic import root_validator, validator, BaseModel, Field, ValidationError, constr
from core.data_structures.One_cloud_API_structure import VDC_data,OS_data
from datetime import datetime


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

    API_key:str = Field(min_length=64, max_length=64)
    Datestamp: str = Field(default_factory=datestamp_creator)
    VDC_list: List[VDC_config]
    OS_list: List[OS_template_config]
