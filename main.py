from fastapi import FastAPI

from .db.database import engine
from .db import models
from .profiles.router import router as profiles_router
from .profiles.partial_update import router as pu_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
prefix = '/api/v1'
app.include_router(profiles_router, prefix=prefix)
app.include_router(pu_router, prefix=prefix)