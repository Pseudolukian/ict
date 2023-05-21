from pydantic import BaseModel, Field, validator
from pydantic.types import constr
import json
from typing import Dict, Any, Optional




class APIKEY(BaseModel):
    API_KEY:constr(strip_whitespace=True, min_length=64, max_length=64)

    def __str__(self):
        return self.API_KEY

    
     
