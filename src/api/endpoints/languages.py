from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import crud, schemas, models
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/languages", response_model=List[schemas.Language])
def get_languages(db: Session = Depends(get_db)):
    """Returns a list of supported languages for learning."""
    return crud.get_languages(db)


@router.post("/add-language", response_model=schemas.Language)
def add_language(language: schemas.LanguageBase, db: Session = Depends(get_db)):
    """Adds a new language to the list of supported languages for learning."""
    db_language = (
        db.query(models.Language).filter(models.Language.name == language.name.capitalize()).first()
    )
    if db_language:
        raise HTTPException(status_code=400, detail="Language already in list")
    return crud.create_language(db=db, name=language.name.capitalize())
