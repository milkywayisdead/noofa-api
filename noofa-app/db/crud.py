from datetime import datetime
from sqlalchemy.orm import Session

from . import schemas
from .proxy import ProfileProxy, DashboardProxy


def get_profile(db: Session, profile_id: int):
    return db.query(ProfileProxy).filter(ProfileProxy.id == profile_id).first()


def get_profiles(db: Session, limit: int = 10):
    return db.query(ProfileProxy).limit(limit).all()


def create_profile(db: Session, profile: schemas.ProfileCreate):
    kw = profile.dict()
    kw.pop('dashboards')
    db_profile = ProfileProxy(**kw)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile: dict):
    profile['last_update'] = datetime.now()
    db.query(ProfileProxy).filter(ProfileProxy.id == profile_id).update(profile)
    db.commit()
    return db.query(ProfileProxy).filter(ProfileProxy.id == profile_id).first()


# Yeah, this is stupid
def delete_profile_dashboards(db, profile_id: int):
    db.query(DashboardProxy).filter(DashboardProxy.profile_id == profile_id).delete()
    return True


def delete_profile(db: Session, profile_id: int):
    db.query(ProfileProxy).filter(ProfileProxy.id == profile_id).delete()

    # yeah, so stupid
    delete_profile_dashboards(db, profile_id)

    db.commit()
    return True


def get_dashboard(db: Session, dashboard_id: str):
    return db.query(DashboardProxy).filter(
        DashboardProxy.id == dashboard_id
    ).first()


def get_dashboards(db: Session, limit: int = 10):
    return db.query(DashboardProxy).limit(limit).all()


def create_dashboard(db: Session, dashboard: dict):
    db_dashboard = DashboardProxy(**dashboard)
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def update_dashboard(db: Session, dashboard_id: str, dashboard: dict):
    db.query(DashboardProxy).filter(DashboardProxy.id == dashboard_id).update(dashboard)
    db.commit()
    return db.query(DashboardProxy).filter(DashboardProxy.id == dashboard_id).first()


def delete_dashboard(db: Session, dashboard_id: str):
    db.query(DashboardProxy).filter(DashboardProxy.id == dashboard_id).delete()
    db.commit()
    return True