from fastapi import FastAPI, HTTPException, Depends,Request
from pydantic import BaseModel, Field
from uuid import UUID
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import auth
app=FastAPI()
templates=Jinja2Templates(directory="templates")
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
@app.get("/",response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request,user: str = Depends(auth.get_current_user)):
    return templates.TemplateResponse("dashboard.html",{"request": request, "user": user}
    )
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
  
    