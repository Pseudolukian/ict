from typing import List, Union
from pydantic import root_validator, validator, BaseModel, Field, ValidationError, constr
from core.data_structures.One_cloud_API_structure import VDC_data,OS_data
from datetime import datetime


class VDC_config(VDC_data):
    """
    Configuration for VDC_config model.
    This class inherits from VDC_data and includes additional configurations specific to VDC_config.
    """
    
    class Config:
        """
        Configuration for VDC_config model.
        This section excludes fields from the parent class VDC_data.
        """
        fields = {'ID': {'exclude': True}, 'Country': {'exclude': True}, 'City': {'exclude': True},
                  'IsEnableBackup': {'exclude': True},'IsEnableIpV6': {'exclude': True},'IsOnlyForAdmins': {'exclude': True},
                  'HiddenToNewProjects': {'exclude': True},'IsFirewallEnabled': {'exclude': True}
                  }


class OS_template_config(OS_data):
    """
    Configuration for OS_template_config model.
    This class inherits from OS_data and includes additional configurations specific to OS_template_config.
    """
    
    class Config:
        """
        Configuration for OS_template_config model.
        This section excludes fields from the parent class OS_data.
        """
        fields = {'DCLocation':{'exclude':True},'Hdd':{'exclude':True},'Family':{'exclude':True},
                  'IsAvailableISP':{'exclude':True},'IsISPLiteEnabled':{'exclude':True},'IsISPBusinessEnabled':{'exclude':True},
                  'Type':{'exclude':True},'LinkedSshKeys':{'exclude':True},'OperatingSystemType':{'exclude':True},
                }


class Config_file(BaseModel):
    """
    Config_file model.
    This model represents the configuration file with specific fields and lists of VDC_config and OS_template_config.
    """
    def datestamp_creator() -> str:
        """
        Helper function to create a datestamp.
        This function returns the current date in the format '%d.%m'.

        Returns:
            str: The datestamp in the format '%d.%m'.
        """
        date_now = datetime.now().strftime('%d.%m')
        return date_now

    API_key:str = Field(min_length=64, max_length=64)
    Datestamp: str = Field(default_factory=datestamp_creator)
    VDC_list: List[VDC_config]
    OS_list: List[OS_template_config]
