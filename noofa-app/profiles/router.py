from typing import List

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..db import crud, schemas
from ..db.utils import get_db
from .encoder import noofa_encoder
from .utils import DfPreparer

from noofa.utils import get_df_descriptor


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

    source = rb.get_source(source_id)
    result = False
    try:
        with source.connection as conn:
            result = conn.test()
    except:
        pass
    return {'result': result}


@router.get("/get_tables_list/{profile_id}/{source_id}")
def get_tables_list(
    profile_id: int,
    source_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()

    tables = []
    try:
        source = rb.get_source(source_id)
        with source.connection as conn:
            tables = conn.get_tables()
    except:
        pass
    return {'tables': tables}


@router.get("/get_fields_list/{profile_id}/{source_id}/{table_name}")
def get_tables_list(
    profile_id: int,
    source_id: str,
    table_name: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()

    fields = []
    try:
        source = rb.get_source(source_id)
        with source.connection as conn:
            fields = conn.get_fields(table_name)
    except:
        pass
    return {'fields': fields}


@router.get("/get_db_structure/{profile_id}/{source_id}")
def get_tables_list(
    profile_id: int,
    source_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()

    db_struct = {}
    try:
        source = rb.get_source(source_id)
        with source.connection as conn:
            db_struct = conn.get_db_structure()
    except:
        pass
    return {'db': db_struct}


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
    df = rb.get_or_build_dataframe(df_id)
    desc = get_df_descriptor(df)
    prep = DfPreparer(df)
    resp = {
        'data': prep.records,
        'columns': desc.columns,
        'dtypes': desc.dtypes,
    }
    resp = jsonable_encoder(resp, custom_encoder=noofa_encoder)
    return JSONResponse(content=resp)


@router.get("/get_table_data/{profile_id}/{table_id}")
def get_table_data(
    profile_id: int,
    table_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    table = rb.build_table(table_id)
    df = table.df
    desc = get_df_descriptor(df)
    prep = DfPreparer(df)
    resp = {
        'data': prep.records,
        'columns': desc.columns,
        'dtypes': desc.dtypes,
    }
    resp = jsonable_encoder(resp, custom_encoder=noofa_encoder)
    return JSONResponse(content=resp)


@router.get("/get_figure_data/{profile_id}/{figure_id}")
def get_figure_data(
    profile_id: int,
    figure_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    figure = rb.build_figure(figure_id)
    data = figure.to_dict()
    resp = jsonable_encoder(data, custom_encoder=noofa_encoder)
    return JSONResponse(content=resp)


@router.get("/get_value/{profile_id}/{value_name}")
def get_value(
    profile_id: int,
    value_name: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    rb = profile.get_report_builder()
    value = rb.get_value(value_name)

    return {
        'is_simple': value.is_simple,
        'value': 'This value is not so simple!' if not value.is_simple else value.value
    }


@router.get("/get_document/{profile_id}/{doc_id}")
def get_document(
    profile_id: int,
    doc_id: str,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile(db, profile_id=profile_id)
    doc = profile.make_pdf(doc_id)

    return Response(
        doc.getvalue(),
        headers={'Content-Disposition': 'attachment; filename="document.pdf"'},
        media_type='application/pdf',
    )