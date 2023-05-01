from pydantic import root_validator, validator, BaseModel, Field, ValidationError, constr
from typing import List, Dict

class Servers_options_structure(BaseModel):
    template: str = "min_02"
    playbook: str = "Nginx_install"
    value: int = Field(default=1, le=10)

class VDC_options_structure(BaseModel):
    DC: str = "Xelent"
    pull: str = "base"

class Infrastructure_template(BaseModel):
    VDC_options: VDC_options_structure = Field(default_factory=lambda: VDC_options_structure())
    Servers: List[Dict[str, Servers_options_structure]] = Field(default_factory=dict)

class Infrastructure_task(BaseModel):
    def dict_without_root(self):
        return {key: value.dict() for key, value in self.__root__.items()}
    
    __root__: Dict[str, Infrastructure_template] = Field(default_factory=dict)