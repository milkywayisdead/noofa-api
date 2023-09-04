from sqlalchemy.orm import Session

from . import schemas
from .proxy import ProfileProxy


def get_profile(db: Session, profile_id: int):
    return db.query(ProfileProxy).filter(ProfileProxy.id == profile_id).first()


def get_profiles(db: Session, limit: int = 10):
    return db.query(ProfileProxy).limit(limit).all()


def create_profile(db: Session, profile: schemas.ProfileCreate):
    kw = profile.dict()
    db_profile = ProfileProxy(**kw)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile