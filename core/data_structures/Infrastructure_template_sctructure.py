from pydantic import root_validator, validator, BaseModel, Field, ValidationError, constr
from typing import List, Dict

class Servers_options_structure(BaseModel):
    """
    Servers options structure.
    This model represents the options structure for servers.
    """
    template: str = "min_02"
    playbook: str = "Nginx_install"
    value: int = Field(default=1, le=10)

class VDC_options_structure(BaseModel):
    """
    VDC options structure.
    This model represents the options structure for VDC (Virtual Data Center).
    """
    DC: str = "Xelent"
    pull: str = "base"

class Infrastructure_template(BaseModel):
    """
    Infrastructure template.
    This model represents the infrastructure template, which includes VDC options and a list of server options.
    """
    VDC_options: VDC_options_structure = Field(default_factory=lambda: VDC_options_structure())
    Servers: List[Dict[str, Servers_options_structure]] = Field(default_factory=dict)

class Infrastructure_task(BaseModel):
    """
    Infrastructure task.
    This model represents the infrastructure task, which contains a dictionary of infrastructure templates.
    """
    def dict_without_root(self):
        return {key: value.dict() for key, value in self.__root__.items()}
    
    __root__: Dict[str, Infrastructure_template] = Field(default_factory=dict)