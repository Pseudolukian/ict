from pydantic import root_validator, validator, BaseModel, Field, ValidationError, constr




#==============YAML data structures==============#

class Yaml_servers(BaseModel):
    template: str = "min_02"
    name: str = Field(default="Nginx") 
    value: int = Field(default=1, gt=1, le=10)

    @validator("template", pre=True, always=True)
    def inf_temp_valid(cls, v):
        if type(service.temp_opener(v)) == dict:
            return v         
        else:
            raise Exception (service.temp_opener(v))

class Yaml_VDC_options(BaseModel):
    DC: str = "xelent"
    pull: str = "base"

class Yaml_resources(BaseModel):
    VDC_options = Yaml_VDC_options()
    servers = Yaml_servers() 
    

class Yaml_infrastructure_template(BaseModel):
    task: dict[str, Yaml_resources]  