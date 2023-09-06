from datetime import datetime
import json
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import schemas
from .proxy import ProfileProxy


def update_source(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='sources')


def update_query(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='queries')


def update_dataframe(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='dataframes')


def update_table(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='tables')


def update_figure(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='figures')


def update_doc(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='docs')


def update_value(db: Session, profile_id: int, target_id: str, payload: dict):
    args = (db, profile_id, target_id, payload)
    _update_target(*args, target='values')


def _update_target(
        db: Session,
        profile_id: int,
        target_id: str,
        payload: dict,
        target: str = None,
    ):
    if target is None:
        return
    
    key = f'$.{target_id}'
    if target in ['tables', 'figures']:
        target = 'components'

    db.query(ProfileProxy).filter(
        ProfileProxy.id == profile_id
    ).update({target: func.json_set(
        getattr(ProfileProxy, target),
        key,
        func.json(json.dumps(payload)),
    )})