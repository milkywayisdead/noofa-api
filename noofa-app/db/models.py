import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer, 
    String,
    JSON,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

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

    dashboards = relationship(
        'Dashboard',
        back_populates='profile',
    )


def _get_uuid():
    return str(uuid.uuid4())


class Dashboard(Base):
    __tablename__ = 'dashboards'

    id = Column(String, primary_key=True, default=_get_uuid)
    contextual_id = Column(String)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    name = Column(String)
    description = Column(Text)
    properties = Column(JSON, default=dict)
    widgets = Column(JSON, default=dict)

    profile = relationship('Profile', back_populates='dashboards')

    def to_dict(self):
        dash_dict = {}
        for attr in [
            'id', 'name', 'description', 'contextual_id',
            'profile_id', 'properties', 'widgets',
        ]:
            dash_dict[attr] = getattr(self, attr)
        return dash_dict