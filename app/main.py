from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.routers import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield      
    

app = FastAPI(lifespan=lifespan)

app.include_router(tasks.router)
