from sqlmodel import Field, SQLModel
from typing import Optional


class Profile_data(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    api_key: str = Field()
    

class OS_templates(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    pub_name: str = Field()
    tech_number: int = Field()

class VDC(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    public_name: str = Field()
    technical_name: str = Field()
    low_pull_enable: bool = Field()
    high_pull_enable: bool = Field()

