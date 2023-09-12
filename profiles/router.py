from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..db import crud, schemas
from ..db.utils import get_db


router = APIRouter()


@router.post("/create_profile/", response_model=schemas.Profile)
def create_profile(
    profile: schemas.ProfileCreate,
    db: Session = Depends(get_db),
):
    return crud.create_profile(db=db, profile=profile)


@router.get("/get_profile/{profile_id}/", response_model=schemas.Profile)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = crud.get_profile(db, profile_id=profile_id)
    return profile


@router.get("/get_profiles/", response_model=List[schemas.Profile])
def get_profiles(limit: int = 10, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, limit=limit)
    return profiles


@router.get("/profile_details/{profile_id}/", response_model=schemas.ProfileDetails)
def profile_details(profile_id: int, db: Session = Depends(get_db)):
    profile = crud.get_profile(db, profile_id=profile_id)
    return profile


@router.get("/profiles_details/", response_model=List[schemas.ProfileDetails])
def profiles_details(limit: int = 10, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, limit=limit)
    return profiles


@router.post("/update_profile/{profile_id}", response_model=schemas.Profile)
def update_profile(
    profile_id: int,
    profile: dict,
    db: Session = Depends(get_db)
):
    profile = crud.update_profile(db, profile_id=profile_id, profile=profile)
    return profile


@router.post("/delete_profile/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    result = crud.delete_profile(db, profile_id)
    return {'result': result, 'msg': f'Profile {profile_id} has been deleted'}


@router.get("/test_connection/{profile_id}/{source_id}")
def test_connection(
    profile_id: int,
    source_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()

    result = False
    try:
        source = rb.get_source(source_id)
        source.open()
        result = source.connection.test()
    except:
        pass
    finally:
        source.close()
    return {'result': result}


@router.get("/get_query_data/{profile_id}/{query_id}")
def get_query_data(
    profile_id: int,
    query_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    return rb.get_data(query_id)


@router.get("/get_df_data/{profile_id}/{df_id}")
def get_df_data(
    profile_id: int,
    df_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    return rb.get_data(df_id)


@router.get("/get_table/{profile_id}/{table_id}")
def get_table(
    profile_id: int,
    table_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    return rb.get_component(table_id)


@router.get("/get_figure/{profile_id}/{figure_id}")
def get_figure(
    profile_id: int,
    figure_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    return rb.get_component(figure_id)