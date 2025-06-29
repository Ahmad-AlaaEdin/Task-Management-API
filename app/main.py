from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.routers import tasks
from fastapi.exceptions import RequestValidationError
from .core.exceptions import validation_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield      
    

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(RequestValidationError,validation_exception_handler)


@app.get("/")
def root():
    return {"message": "Task Management API", "endpoints": ["/tasks", "/health", "/docs","/redoc"]}

# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(tasks.router)



