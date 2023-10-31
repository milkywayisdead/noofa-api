from datetime import datetime
import json
from sqlalchemy.orm import Session
from sqlalchemy import func

#from . import schemas
from .import crud
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


def update_dashboard(db: Session, dashboard_id: str, dashboard: dict):
    if dashboard_id == 'null':
        dash = crud.create_dashboard(db, dashboard)
    else:
        args = (db, dashboard_id, dashboard)
        dash = crud.update_dashboard(*args)
    return dash


def delete_source(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='sources')


def delete_query(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='queries')


def delete_dataframe(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='dataframes')


def delete_table(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='tables')


def delete_figure(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='figures')


def delete_doc(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='docs')


def delete_value(db: Session, profile_id: int, target_id: str):
    args = (db, profile_id, target_id)
    _delete_target(*args, target='values')


def delete_dashboard(db: Session, dashboard_id: str):
    crud.delete_dashboard(db, dashboard_id)


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
        ),
        'last_update': datetime.now(),
    })


def _delete_target(
        db: Session,
        profile_id: int,
        target_id: str,
        target: str = None,
    ):
    if target is None:
        return
    
    key = f'$.{target_id}'
    if target in ['tables', 'figures']:
        target = 'components'

    db.query(ProfileProxy).filter(
        ProfileProxy.id == profile_id
    ).update({target: func.json_remove(
            getattr(ProfileProxy, target),
            key,
        ),
        'last_update': datetime.now(),
    })