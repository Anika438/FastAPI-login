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
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Item(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1,max_length=100)
    description: str = Field(min_length=1,max_length=300)
    rating: int = Field(gt=-1,lt=101)
books = []
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.User).all()
# @app.post("/")
# def create_book(item: Item, db: Session = Depends(get_db)):
#     user_model = models.User()
#     user_model.title = item.title
#     user_model.author = item.author
#     user_model.description = item.description
#     user_model.rating = item.rating
#     db.add(user_model)
#     db.commit()
#     return item
# @app.put("/{item_id}")
# def update_book(item_id: int, item: Item,  db: Session = Depends(get_db)):
#     user_model = db.query(models.User).filter(models.User.id == item_id).first()
#     if user_model is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     user_model.title = item.title
#     user_model.author = item.author
#     user_model.description = item.description
#     user_model.rating = item.rating
#     db.commit()
#     return item
# @app.delete("/{item_id}")
# def delete_book(item_id: int, db: Session = Depends(get_db)):
#     user_model = db.query(models.User).filter(models.User.id == item_id).first()
#     if user_model is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     db.delete(user_model)
#     db.commit()
#     return "ok"
    
    