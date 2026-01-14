from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import auth
app=FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
@app.get("/")
def health_check():
    return {"status": "API is running"}

    
    