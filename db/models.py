from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer, 
    String,
    JSON,
    DateTime,
    Text,
)

from .database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now)
    sources = Column(JSON, default=dict)
    queries = Column(JSON, default=dict)
    dataframes = Column(JSON, default=dict)
    components = Column(JSON, default=dict)
    docs = Column(JSON, default=dict)
    values = Column(JSON, default=dict)
    is_template = Column(Boolean, default=False)