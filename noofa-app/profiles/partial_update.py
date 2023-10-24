from typing import Dict

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..db.utils import get_db
from ..db import partial_update as pu


router = APIRouter()


@router.post("/partial_update/{profile_id}/{target}/{target_id}")
def partial_update(
    profile_id: int,
    target: str,
    target_id: str,
    payload: Dict,
    db: Session = Depends(get_db),
):
    if target == 'dashboard':
        payload['profile_id'] = profile_id
        dash = pu.update_dashboard(db, target_id, payload)
        return {'result': 'success', 'id': dash.id}
    else:
        method = getattr(pu, f'update_{target}')
        method(db, profile_id, target_id, payload)
        db.commit()
    return {'result': 'success'}


@router.post("/partial_delete/{profile_id}/{target}/{target_id}")
def partial_delete(
    profile_id: int,
    target: str,
    target_id: str,
    db: Session = Depends(get_db),
):
    if target == 'dashboard':
        pu.delete_dashboard(db, target_id)
    else:
        method = getattr(pu, f'delete_{target}')
        method(db, profile_id, target_id)
        db.commit()
    return {'result': 'success'}