from fastapi import FastAPI
from database import engine
import models
from routers import post, user, auth, vote


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)