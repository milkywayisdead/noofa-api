import datetime
from typing import Dict

from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str
    description: str
    sources: Dict
    queries: Dict
    dataframes: Dict
    components: Dict
    docs: Dict
    values: Dict


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    created: datetime.datetime
    last_update: datetime.datetime

    class Config:
        orm_mode = True


class ProfileDetails(BaseModel):
    name: str
    description: str
    created: datetime.datetime
    last_update: datetime.datetime


class ProfileUpdate(ProfileBase):
    last_update: datetime.datetime