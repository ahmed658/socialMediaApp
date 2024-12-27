from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

socialMediaApp = FastAPI()

# using Almebic now instead
# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

socialMediaApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



socialMediaApp.include_router(post.router)
socialMediaApp.include_router(user.router)
socialMediaApp.include_router(auth.router)
socialMediaApp.include_router(vote.router)

