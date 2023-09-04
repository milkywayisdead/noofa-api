from fastapi import FastAPI

from .db.database import engine
from .db import models
from .profiles.router import router as profiles_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(profiles_router)