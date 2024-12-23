from fastapi import FastAPI
from . import models
from .config import settings
from .database import engine
from .routers import post, user, auth, vote

socialMediaApp = FastAPI()

models.Base.metadata.create_all(bind=engine)


socialMediaApp.include_router(post.router)
socialMediaApp.include_router(user.router)
socialMediaApp.include_router(auth.router)
socialMediaApp.include_router(vote.router)

