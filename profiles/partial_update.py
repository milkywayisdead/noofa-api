from typing import Dict

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..db.utils import get_db
from ..db import partial_update as pu


router = APIRouter()


@router.post("/partial_update/{profile_id}")
def partial_update(
    profile_id: int,
    target: str,
    target_id: str,
    payload: Dict,
    db: Session = Depends(get_db),
):

    method = getattr(pu, f'update_{target}')
    method(db, profile_id, target_id, payload)
    db.commit()
    return {'result': 'success'}