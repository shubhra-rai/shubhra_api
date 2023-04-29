from fastapi import FastAPI
from .import models
from .database import engine
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import post,user,auth,vote


models.Base.metadata.create_all(bind= engine)



app=FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


    

